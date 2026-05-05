#!/usr/bin/env python3
"""Recompute key_collaborators[].papers_count and since/until from each
person's publications list.

This fixes a long-standing bug: papers_count was hand-typed during initial
data entry and never updated, so the UI shows stale numbers (e.g. liu-xiaobo
listed yang-chenglang as "5 篇" while the actual publications list has 4
joint papers).

Usage:
  python3 scripts/recompute-collaborator-counts.py            # dry-run
  python3 scripts/recompute-collaborator-counts.py --write
"""

import argparse
import os
import re
import sys
from collections import defaultdict
import yaml

PEOPLE_DIR = 'data/people'


def load_all():
    out = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            out[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}
    return out


def build_name_to_slug_index(all_people):
    """Map normalized English names to slugs for resolving raw-name coauthors."""
    idx = {}
    for slug, p in all_people.items():
        en = ((p.get('name') or {}).get('en') or '').strip()
        if en:
            idx[en.lower()] = slug
            # Also add "first last" lowercase no-punct variant
            simple = re.sub(r'[^a-z ]', ' ', en.lower())
            simple = re.sub(r'\s+', ' ', simple).strip()
            idx[simple] = slug
    return idx


def resolve_coauthor(ca, name_to_slug):
    """Map a coauthor entry (slug or raw name) to a slug if possible."""
    if not isinstance(ca, str) or not ca:
        return None
    if '-' in ca and ca.islower() and ca.replace('-', '').replace('_', '').isalnum():
        return ca  # already a slug
    # Try name match
    cleaned = re.sub(r'\([^)]*\)', '', ca)
    cleaned = re.sub(r'[^\x20-\x7e]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return name_to_slug.get(cleaned)


def coauthor_stats(person, name_to_slug):
    """For a person, return {coauthor_slug: {count, since, until}}.
    Aggregates raw-name coauthors with slug coauthors when name resolves."""
    stats = defaultdict(lambda: {'count': 0, 'years': []})
    for pub in (person.get('publications') or []):
        year = pub.get('year')
        seen_in_pub = set()  # avoid double-count if both slug and name appear
        for ca in (pub.get('coauthors') or []):
            slug = resolve_coauthor(ca, name_to_slug)
            if not slug or slug in seen_in_pub:
                continue
            seen_in_pub.add(slug)
            stats[slug]['count'] += 1
            if year:
                stats[slug]['years'].append(year)
    out = {}
    for slug, s in stats.items():
        years = sorted(set(s['years']))
        out[slug] = {
            'count': s['count'],
            'since': years[0] if years else None,
            'until': years[-1] if years else None,
        }
    return out


def patch_yaml_text(text, slug, kc_list, stats):
    """Update papers_count, since (and add a 'until' if reasonable) for each
    key_collaborator in `text`. We do regex line-level edits to preserve
    formatting.

    For each kc entry, find its block and update papers_count to the actual
    count from publications. Also overwrite `since` only if missing or wrong.
    Mark with a `papers_count_source: arxiv` line so UI/users know origin."""
    new_text = text
    changes = []

    for kc in kc_list:
        co = kc.get('person')
        if co is None or co not in stats:
            continue
        actual = stats[co]
        if actual['count'] == 0:
            # Don't touch entries that have zero co-authored publications
            # in our list (could be social/email contact, or all coauthored
            # papers are pre-arXiv era). We'll log but not edit.
            changes.append((co, kc.get('papers_count'), 0, 'kept (0 in pubs)'))
            continue

        # Find the block: starts with `- person: <co>` (kc list is `- person:` indented)
        # Use a regex that captures the block until the next `- person:` or end-of-list
        pattern = re.compile(
            rf'(- person:\s*{re.escape(str(co))}\s*\n(?:[ \t]+[^\n]*\n)*)',
            re.MULTILINE
        )
        m = pattern.search(new_text)
        if not m:
            changes.append((co, kc.get('papers_count'), actual['count'], 'block not found'))
            continue
        block = m.group(1)

        # Update or insert papers_count
        new_block, did = re.subn(
            r'(papers_count:\s*)\d+',
            lambda _m: f'papers_count: {actual["count"]}',
            block, count=1
        )
        if did == 0:
            # No papers_count line; need to detect indent of existing fields and
            # insert a new line at matching indent right after `- person:` line.
            indent_m = re.search(r'\n([ \t]+)\w', block)
            indent = indent_m.group(1) if indent_m else '    '
            new_block = re.sub(
                r'(- person:[^\n]*\n)',
                lambda _m: _m.group(1) + f'{indent}papers_count: {actual["count"]}\n',
                block, count=1
            )

        # Don't touch `since` if it's already set; only fill if missing
        if 'since:' not in new_block and actual['since']:
            indent_m = re.search(r'\n([ \t]+)\w', new_block)
            indent = indent_m.group(1) if indent_m else '    '
            new_block = re.sub(
                r'(- person:[^\n]*\n)',
                lambda _m: _m.group(1) + f'{indent}since: {actual["since"]}\n',
                new_block, count=1
            )

        if new_block != block:
            new_text = new_text[:m.start()] + new_block + new_text[m.end():]
            changes.append((co, kc.get('papers_count'), actual['count'], 'updated'))
        else:
            changes.append((co, kc.get('papers_count'), actual['count'], 'no-change'))

    return new_text, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--slug', help='Only process this slug (for testing)')
    args = parser.parse_args()

    people = load_all()
    name_to_slug = build_name_to_slug_index(people)
    targets = [args.slug] if args.slug else sorted(people.keys())

    total_changed_files = 0
    total_changed_entries = 0
    summary_lines = []

    for slug in targets:
        person = people.get(slug)
        if not person:
            continue
        kc = person.get('key_collaborators') or []
        if not kc:
            continue
        stats = coauthor_stats(person, name_to_slug)
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        new_text, changes = patch_yaml_text(text, slug, kc, stats)
        diffs = [(co, old, new, status) for co, old, new, status in changes
                  if status == 'updated' and old != new]
        if diffs:
            summary_lines.append(f'{slug}:')
            for co, old, new, _ in diffs:
                summary_lines.append(f'  {co}: {old} -> {new}')
            total_changed_entries += len(diffs)
            total_changed_files += 1
            if args.write:
                with open(path, 'w') as f:
                    f.write(new_text)

    print('\n'.join(summary_lines))
    print(f'\n{total_changed_files} files, {total_changed_entries} entries '
          f'{"updated" if args.write else "would update (dry-run)"}')


if __name__ == '__main__':
    main()
