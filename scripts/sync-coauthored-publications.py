#!/usr/bin/env python3
"""Sync coauthored publications across YAML pairs.

Problem: a paper coauthored by A and B may exist in A.yaml but not B.yaml,
or with mismatched ids (arxiv id on one side, doi: id on other), causing
duplicate counting in the front-end coauthor reverse-derivation.

Strategy:
For each pair (A, B) where A.yaml's publications has a paper with B in coauthors:
- If B.yaml's publications doesn't have this paper (by arxiv-id OR by DOI OR by
  normalized-title), copy the entry into B.yaml's publications.
- Resolve coauthor name strings to slugs where possible.

Also handles the inverse case (paper in B.yaml not in A.yaml).

Usage:
  python3 scripts/sync-coauthored-publications.py [--dry-run]
"""

import argparse
import os
import re
import sys
import yaml

PEOPLE_DIR = 'data/people'


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def normalize_doi(d):
    if not d:
        return None
    s = str(d).lower().strip()
    return re.sub(r'^https?://(dx\.)?doi\.org/', '', s) or None


def is_arxiv_doi(d):
    return bool(d and d.startswith('10.48550/arxiv.'))


def normalize_title_key(t):
    s = (t or '').lower()
    s = re.sub(r'\$[^$]*\$', ' ', s)
    s = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', ' ', s)
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def load_all():
    out = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            out[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}
    return out


def name_to_slug_index(all_people):
    idx = {}
    for slug, p in all_people.items():
        en = ((p.get('name') or {}).get('en') or '').strip()
        if en:
            k = re.sub(r'[^a-z ]', ' ', en.lower()).strip()
            if k:
                idx[k] = slug
    return idx


def resolve_coauthor(s, all_people, name_idx):
    if not isinstance(s, str) or not s:
        return s
    if s in all_people:
        return s
    cleaned = re.sub(r'\([^)]*\)', '', s)
    cleaned = re.sub(r'[^\x20-\x7e]', ' ', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
    return name_idx.get(cleaned, s)


def paper_key(pub):
    """Strict key for matching same paper across yaml files."""
    doi = normalize_doi(pub.get('doi'))
    if doi and not is_arxiv_doi(doi):
        return ('doi', doi)
    pid = (pub.get('id') or '').split('v')[0]
    if pid and not pid.startswith(('doi:', 'openalex:', 'cr:')):
        return ('arxiv', pid)
    title_key = normalize_title_key(pub.get('title') or '')
    if title_key:
        return ('title', title_key)
    return None


def render_pubs(pubs):
    lines = ['publications:']
    for p in pubs:
        if not p.get('id'):
            continue
        lines.append(f'  - id: {squote(p["id"])}')
        lines.append(f'    title: {squote(p.get("title") or "")}')
        if p.get('year') is not None:
            lines.append(f'    year: {p["year"]}')
        cas = p.get('coauthors') or []
        if cas:
            inner = ', '.join(c if re.fullmatch(r'[a-z][a-z0-9_-]*', str(c)) else squote(c) for c in cas)
            lines.append(f'    coauthors: [{inner}]')
        else:
            lines.append('    coauthors: []')
        if p.get('doi'):
            lines.append(f'    doi: {squote(p["doi"])}')
        if p.get('journal'):
            lines.append(f'    journal: {squote(p["journal"])}')
        if p.get('primary_category'):
            lines.append(f'    primary_category: {p["primary_category"]}')
        if p.get('openalex_id'):
            lines.append(f'    openalex_id: {p["openalex_id"]}')
        if p.get('sources'):
            lines.append(f'    sources: [{", ".join(p["sources"])}]')
        if p.get('no_arxiv'):
            lines.append('    no_arxiv: true')
    return '\n'.join(lines)


def render_activity(activity):
    order = ['total_papers', 'published_count', 'preprint_only_count', 'h_index',
             'mathscinet_citations', 'google_scholar_citations',
             'active_period', 'peak_period', 'phd_students',
             'academic_descendants', 'last_arxiv_paper', 'confidence']
    lines = ['activity:']
    keys = order + [k for k in activity if k not in order]
    for k in keys:
        v = activity.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            lines.append(f'  {k}: {squote(v)}')
        elif isinstance(v, list):
            lines.append(f'  {k}: {v}')
        else:
            lines.append(f'  {k}: {v}')
    return '\n'.join(lines)


def replace_block(text, name, new_block):
    pat = re.compile(rf'^{name}:.*?(?=^[A-Za-z_][\w]*:|\Z)', re.MULTILINE | re.DOTALL)
    if pat.search(text):
        return pat.sub(lambda _m: new_block + '\n', text, count=1)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    all_people = load_all()
    name_idx = name_to_slug_index(all_people)

    # Iterate multiple passes since adding to one yaml could create new
    # cross-references, but in practice 1 pass enough since we sync immediately.
    additions_per_yaml = {}  # slug -> [pub-entry]
    for slug, person in all_people.items():
        for pub in (person.get('publications') or []):
            cas = pub.get('coauthors') or []
            for ca in cas:
                co_slug = resolve_coauthor(ca, all_people, name_idx)
                if not isinstance(co_slug, str) or co_slug not in all_people:
                    continue
                if co_slug == slug:
                    continue
                # Check if co_slug yaml has this paper
                co_pubs = all_people[co_slug].get('publications') or []
                target_key = paper_key(pub)
                if not target_key:
                    continue
                already = False
                for cp in co_pubs:
                    cpk = paper_key(cp)
                    if cpk == target_key:
                        already = True
                        break
                if already:
                    continue
                # Need to add this pub to co_slug yaml
                # Resolve coauthors from this pub: replace `slug` slot with `slug` (the writer),
                # remove `co_slug` itself, normalize others
                new_coauthors = []
                target_slug_added = False
                for c in cas:
                    cs = resolve_coauthor(c, all_people, name_idx)
                    if cs == co_slug:
                        continue  # don't list self
                    if isinstance(cs, str):
                        new_coauthors.append(cs)
                if slug not in new_coauthors:
                    new_coauthors.insert(0, slug)
                additions_per_yaml.setdefault(co_slug, []).append({
                    **pub,
                    'coauthors': new_coauthors,
                })

    total_added = 0
    files_changed = 0
    for co_slug, additions in additions_per_yaml.items():
        # Dedup additions within themselves
        seen = set()
        unique = []
        for a in additions:
            k = paper_key(a)
            if k and k not in seen:
                seen.add(k)
                unique.append(a)
        if not unique:
            continue
        files_changed += 1
        total_added += len(unique)

        if args.dry_run:
            print(f'  {co_slug}: +{len(unique)} papers')
            for a in unique[:3]:
                print(f'    + [{a.get("year")}] {(a.get("title") or "")[:60]}')
            continue

        path = os.path.join(PEOPLE_DIR, f'{co_slug}.yaml')
        with open(path) as f:
            text = f.read()
        person = yaml.safe_load(text)
        existing_pubs = person.get('publications') or []
        merged = existing_pubs + unique
        merged.sort(key=lambda p: -(p.get('year') or 0))
        text = replace_block(text, 'publications', render_pubs(merged))
        # Recompute activity counts
        try:
            p2 = yaml.safe_load(text)
            pubs2 = p2.get('publications') or []
            pc = sum(1 for p in pubs2 if p.get('journal') or (
                p.get('doi') and not is_arxiv_doi(p.get('doi'))))
            prc = len(pubs2) - pc
            activity = dict(p2.get('activity') or {})
            activity['total_papers'] = len(pubs2)
            activity['published_count'] = pc
            activity['preprint_only_count'] = prc
            text = replace_block(text, 'activity', render_activity(activity))
        except Exception as e:
            print(f'  warn: activity recompute failed for {co_slug}: {e}', file=sys.stderr)
        with open(path, 'w') as f:
            f.write(text)
        print(f'  {co_slug}: +{len(unique)} papers reflected from coauthors')

    print(f'\n{files_changed} files updated, {total_added} cross-reflected entries')


if __name__ == '__main__':
    main()
