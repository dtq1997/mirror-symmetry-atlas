#!/usr/bin/env python3
"""Enrich a person YAML's publications field with disambiguated arXiv candidates.

Adds new high-score papers, fills journal/doi from arXiv journal_ref, and
computes activity.published_count / activity.preprint_only_count.

Usage:
  python3 scripts/enrich-publications.py <slug> [--threshold 10] [--write]
  python3 scripts/enrich-publications.py --all [--threshold 10] [--write]

Without --write, prints a dry-run summary of what would change.
"""

import argparse
import os
import sys
import yaml
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_disambiguate import (
    load_all_people, fetch_candidates_for_person, disambiguate, normalize_name,
)

PEOPLE_DIR = 'data/people'


def slugify_coauthor(author_name, all_people):
    """Try to map an arXiv author name to a known slug. Returns slug or normalized name string."""
    norm = normalize_name(author_name).lower()
    for slug, p in all_people.items():
        en = (p.get('name') or {}).get('en', '')
        if not en:
            continue
        en_parts = normalize_name(en).lower().split()
        if en_parts and all(part in norm for part in en_parts if len(part) > 1):
            return slug
    return normalize_name(author_name)


def enrich_person(slug, person, all_people, threshold=10, fetch_delay=4, target_self=None):
    target_name = target_self or (person.get('name') or {}).get('en', '')
    if not target_name:
        return None, 'no name'

    candidates = fetch_candidates_for_person(target_name, max_results=300,
                                              math_only=True, delay=fetch_delay)
    if not candidates:
        return None, 'no candidates'

    existing = {(p.get('id') or '').split('v')[0]: p
                for p in (person.get('publications') or [])}

    # Score & accept
    accepted = []
    for c in candidates:
        score, signals = disambiguate(person, c, all_people, target_name=target_name)
        if score >= threshold:
            # Drop self from coauthors
            coauthors = []
            for a in c['authors']:
                if normalize_name(a).lower() == normalize_name(target_name).lower():
                    continue
                coauthors.append(slugify_coauthor(a, all_people))
            entry = {
                'id': c['id'],
                'title': c['title'],
                'year': c['year'],
                'coauthors': coauthors,
            }
            if c.get('doi'):
                entry['doi'] = c['doi']
            if c.get('journal_ref'):
                entry['journal'] = c['journal_ref']
            if c.get('primary_category'):
                entry['primary_category'] = c['primary_category']
            accepted.append((c['id'], entry, score, signals))

    accepted_ids = {aid for aid, *_ in accepted}

    # Merge: keep existing manual fields where present, add new
    merged = []
    seen = set()
    for aid, entry, _, _ in accepted:
        prev = existing.get(aid)
        if prev:
            # Preserve any human-edited fields not in entry
            merged_entry = {**entry, **{k: v for k, v in prev.items() if v not in (None, '', [])}}
            # But always overwrite journal/doi from arxiv fresh data if newly available
            if entry.get('journal'):
                merged_entry['journal'] = entry['journal']
            if entry.get('doi'):
                merged_entry['doi'] = entry['doi']
            if entry.get('primary_category'):
                merged_entry['primary_category'] = entry['primary_category']
            merged.append(merged_entry)
        else:
            merged.append(entry)
        seen.add(aid)

    # Keep existing publications that didn't show up in math query (could be old / cross-cat)
    kept_extra = []
    for aid, prev in existing.items():
        if aid not in accepted_ids:
            kept_extra.append(prev)

    merged.sort(key=lambda x: -(x.get('year') or 0))

    published_count = sum(1 for p in merged + kept_extra
                          if p.get('journal') or p.get('doi'))
    preprint_count = (len(merged) + len(kept_extra)) - published_count

    return {
        'merged_publications': merged,
        'kept_extra': kept_extra,
        'new_count': len([1 for aid, *_ in accepted if aid not in existing]),
        'existing_count': len(existing),
        'final_count': len(merged) + len(kept_extra),
        'published_count': published_count,
        'preprint_count': preprint_count,
    }, None


def write_back(slug, person, result):
    new_publications = result['merged_publications'] + result['kept_extra']
    person2 = deepcopy(person)
    person2['publications'] = new_publications
    activity = person2.get('activity') or {}
    activity['total_papers'] = result['final_count']
    activity['published_count'] = result['published_count']
    activity['preprint_only_count'] = result['preprint_count']
    person2['activity'] = activity
    path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
    with open(path, 'w') as f:
        yaml.dump(person2, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slug', nargs='?')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--threshold', type=int, default=10)
    parser.add_argument('--delay', type=int, default=4)
    parser.add_argument('--write', action='store_true', help='Write changes back to YAML')
    args = parser.parse_args()

    all_people = load_all_people()
    targets = list(all_people.keys()) if args.all else ([args.slug] if args.slug else [])
    if not targets:
        print('Specify slug or --all', file=sys.stderr)
        sys.exit(1)

    summary = []
    for i, slug in enumerate(targets):
        person = all_people.get(slug)
        if not person:
            print(f'[{i+1}/{len(targets)}] {slug} NOT FOUND', file=sys.stderr)
            continue
        print(f'[{i+1}/{len(targets)}] {slug} ...', file=sys.stderr)
        result, err = enrich_person(slug, person, all_people,
                                     threshold=args.threshold, fetch_delay=args.delay)
        if err:
            print(f'  skipped: {err}', file=sys.stderr)
            continue
        summary.append({
            'slug': slug,
            'before': result['existing_count'],
            'after': result['final_count'],
            'new': result['new_count'],
            'published': result['published_count'],
            'preprint': result['preprint_count'],
        })
        print(f"  {result['existing_count']} -> {result['final_count']} ({result['new_count']} new); "
              f"{result['published_count']} published / {result['preprint_count']} preprint",
              file=sys.stderr)
        if args.write:
            write_back(slug, person, result)

    print('\n=== SUMMARY ===')
    print(f"{'slug':<25} {'before':>7} {'after':>7} {'+new':>5} {'pub':>5} {'arxiv':>5}")
    for s in summary:
        print(f"{s['slug']:<25} {s['before']:>7} {s['after']:>7} {s['new']:>5} {s['published']:>5} {s['preprint']:>5}")


if __name__ == '__main__':
    main()
