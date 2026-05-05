#!/usr/bin/env python3
"""Dedup publications within each YAML.

Problem: a paper may exist as both an arXiv preprint entry AND a separate
journal/DOI entry (after Crossref/OpenAlex enrichment created a doi:... id
without merging back to the arXiv id).

Strategy:
1. Group entries by normalized title within each yaml.
2. If a group has multiple entries, merge them into one:
   - Keep the arXiv id as primary (so abs link works) when present
   - Take the latest year (final published year)
   - Union coauthors (keep slugs, prefer slug-resolved ones)
   - Take DOI + journal from the entry that has them
   - Union sources
   - Drop no_arxiv flag if any entry has an arXiv id

This eliminates duplicate-counting in publications, activity counts,
coauthored_papers reverse-derivation, etc.
"""

import argparse
import os
import re
import sys
import yaml

PEOPLE_DIR = 'data/people'


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def normalize_title_key(t):
    s = (t or '').lower()
    s = re.sub(r'\$[^$]*\$', ' ', s)
    s = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', ' ', s)  # \mathbb{P}, \mathbf{...} etc.
    s = re.sub(r'\\[a-zA-Z]+', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def normalize_doi(d):
    if not d:
        return None
    s = str(d).lower().strip()
    s = re.sub(r'^https?://(dx\.)?doi\.org/', '', s)
    return s or None


def is_arxiv_doi(doi):
    """The 10.48550/arxiv.X DOI is the arXiv-assigned auto-DOI; not a real
    journal publication."""
    return bool(doi and doi.startswith('10.48550/arxiv.'))


def merge_group(group):
    """Merge a list of entries (same paper) into one. Returns dict."""
    # Pick primary id: prefer arXiv-style id (no prefix, has digit-dot-digit)
    arxiv_ids = [e['id'] for e in group
                  if e.get('id') and not e['id'].startswith(('doi:', 'openalex:', 'cr:'))]
    if arxiv_ids:
        primary_id = arxiv_ids[0]
    else:
        # No arXiv id; prefer doi:
        doi_ids = [e['id'] for e in group if e.get('id', '').startswith('doi:')]
        primary_id = doi_ids[0] if doi_ids else group[0].get('id')

    # Real journal DOI: not the arXiv auto-DOI
    real_dois = [normalize_doi(e.get('doi')) for e in group
                  if e.get('doi') and not is_arxiv_doi(normalize_doi(e.get('doi')))]
    journal_doi = real_dois[0] if real_dois else None
    # Fallback: any DOI (might still be arXiv self-DOI)
    if not journal_doi:
        any_dois = [normalize_doi(e.get('doi')) for e in group if e.get('doi')]
        journal_doi = any_dois[0] if any_dois else None

    journals = [e.get('journal') for e in group if e.get('journal')]
    journal = journals[0] if journals else None

    # Year: prefer the latest (final publication year > preprint)
    years = [e.get('year') for e in group if isinstance(e.get('year'), int)]
    year = max(years) if years else None

    # Title: prefer the most "polished" — longest after strip + the journal version usually
    titles = [e.get('title') for e in group if e.get('title')]
    title = max(titles, key=len) if titles else ''

    # Coauthors: union, prefer slug-shaped tokens
    seen_slug = set()
    seen_name_norm = set()
    merged_coauthors = []
    for e in group:
        for c in (e.get('coauthors') or []):
            if not isinstance(c, str):
                continue
            if re.fullmatch(r'[a-z][a-z0-9_-]*', c):
                if c not in seen_slug:
                    seen_slug.add(c)
                    merged_coauthors.append(c)
            else:
                k = re.sub(r'[^a-z]', '', c.lower())
                if k and k not in seen_name_norm:
                    seen_name_norm.add(k)
                    merged_coauthors.append(c)

    # Sources union
    src_set = set()
    for e in group:
        for s in (e.get('sources') or []):
            src_set.add(s)
    sources = sorted(src_set)

    # primary_category: prefer entries that have it
    pcs = [e.get('primary_category') for e in group if e.get('primary_category')]
    pc = pcs[0] if pcs else None

    # openalex_id
    oa_ids = [e.get('openalex_id') for e in group if e.get('openalex_id')]
    oa_id = oa_ids[0] if oa_ids else None

    has_arxiv = bool(arxiv_ids)
    no_arxiv = (not has_arxiv) and any(e.get('no_arxiv') for e in group)

    merged = {
        'id': primary_id,
        'title': title,
        'year': year,
        'coauthors': merged_coauthors,
    }
    if journal_doi:
        merged['doi'] = journal_doi
    if journal:
        merged['journal'] = journal
    if pc:
        merged['primary_category'] = pc
    if oa_id:
        merged['openalex_id'] = oa_id
    if sources:
        merged['sources'] = sources
    if no_arxiv:
        merged['no_arxiv'] = True
    return merged


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
            lines.append(f'    no_arxiv: true')
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
    parser.add_argument('slugs', nargs='*')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    targets = (sorted(f.replace('.yaml', '') for f in os.listdir(PEOPLE_DIR) if f.endswith('.yaml'))
                if args.all or not args.slugs else args.slugs)

    total_merged = 0
    affected_files = 0
    for slug in targets:
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            person = yaml.safe_load(f)
        if not person:
            continue
        pubs = person.get('publications') or []
        if not pubs:
            continue

        # Group by (real-DOI) OR (normalized-title)
        groups = {}  # key -> list[entry]
        unkeyed = []
        for p in pubs:
            doi = normalize_doi(p.get('doi'))
            if doi and not is_arxiv_doi(doi):
                key = ('doi', doi)
            else:
                key = ('title', normalize_title_key(p.get('title') or ''))
                if not key[1]:
                    unkeyed.append(p)
                    continue
            groups.setdefault(key, []).append(p)

        merged_pubs = []
        merges_count = 0
        for key, group in groups.items():
            if len(group) == 1:
                merged_pubs.append(group[0])
            else:
                merged_pubs.append(merge_group(group))
                merges_count += len(group) - 1
        merged_pubs.extend(unkeyed)

        # Cross-merge: title key may match across DOI and non-DOI entries
        # (i.e. same paper, one with DOI and one without). Re-group by title:
        title_groups = {}
        no_title = []
        for p in merged_pubs:
            t = normalize_title_key(p.get('title') or '')
            if not t:
                no_title.append(p)
                continue
            title_groups.setdefault(t, []).append(p)
        final_pubs = []
        for t, group in title_groups.items():
            if len(group) == 1:
                final_pubs.append(group[0])
            else:
                final_pubs.append(merge_group(group))
                merges_count += len(group) - 1
        final_pubs.extend(no_title)
        # Sort newest first
        final_pubs.sort(key=lambda p: -(p.get('year') or 0))

        if merges_count == 0:
            continue
        affected_files += 1
        total_merged += merges_count

        if args.dry_run:
            print(f'  {slug}: {len(pubs)} -> {len(final_pubs)} ({merges_count} merges)')
            continue

        with open(path) as f:
            text = f.read()
        text = replace_block(text, 'publications', render_pubs(final_pubs))
        # Recompute activity
        try:
            p2 = yaml.safe_load(text)
            pubs2 = p2.get('publications') or []
            pc = sum(1 for p in pubs2 if p.get('journal') or (
                p.get('doi') and not is_arxiv_doi(p['doi'])))
            prc = len(pubs2) - pc
            activity = dict(p2.get('activity') or {})
            activity['total_papers'] = len(pubs2)
            activity['published_count'] = pc
            activity['preprint_only_count'] = prc
            text = replace_block(text, 'activity', render_activity(activity))
        except Exception as e:
            print(f'  warn: activity recompute failed for {slug}: {e}', file=sys.stderr)
        with open(path, 'w') as f:
            f.write(text)
        print(f'  {slug}: merged {merges_count} duplicates -> {len(final_pubs)} pubs')

    print(f'\n{affected_files} files, {total_merged} duplicate entries merged')


if __name__ == '__main__':
    main()
