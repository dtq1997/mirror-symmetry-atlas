#!/usr/bin/env python3
"""SSOT: canonicalize publications. ONE paper = ONE record per yaml.

This script supersedes:
- scripts/dedup-publications.py
- the per-script merge logic inside enrich-from-openalex-v2.py / crossref-supplementary-enrich.py

Authoritative rules:
1. Group entries within each yaml by canonical paper key:
   - Real journal DOI (not arXiv self-DOI 10.48550/arxiv.X)
   - OR arxiv id (without v-suffix)
   - OR normalized title (LaTeX/MathML stripped, lowercase, alnum tokens)
2. Within each group merge to ONE record:
   - id: arxiv id if available, else doi:DOI, else openalex:OAid
   - doi: real journal DOI (skip arxiv self-DOI)
   - journal: from any entry that has it
   - year: max (final published year wins)
   - title: longest of the variants (likely the polished version)
   - coauthors: union, prefer slug-resolved
   - sources: union (arxiv + openalex + crossref)
   - status: 'published' iff doi (real) OR journal exists; else 'preprint'
3. Cross-yaml sync: for each pair of authors A, B both in our index, if a
   paper has both as coauthors, the same canonical record must appear in
   BOTH A.yaml and B.yaml with identical journal/doi/sources status.

Computes activity:
  total_papers = len(canonical pubs)
  published_count = len([p for p in pubs if p has real-doi or journal])
  preprint_only_count = total - published_count

Usage:
  python3 scripts/canonicalize-publications.py [--dry-run]
"""

import argparse
import os
import re
import sys
from collections import defaultdict
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_identity import (
    canonical_title, canonical_doi, canonical_arxiv_id, paper_identity_keys,
)

PEOPLE_DIR = 'data/people'


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def is_arxiv_doi(d):
    return bool(d and str(d).lower().startswith('10.48550/arxiv.'))


# Use paper_identity module's canonicals where the previous local versions had bugs
normalize_doi = canonical_doi  # already excludes arxiv self-DOI by returning None
normalize_title = canonical_title


def get_arxiv_id_strict(pub):
    return canonical_arxiv_id(pub.get('id', ''))


def paper_key(pub):
    """Triple of keys (real_doi, arxiv_id, title) for cross-matching.
    Each can be None. Uses canonical_* from paper_identity module."""
    return paper_identity_keys(pub)


def keys_match(a, b):
    """Two paper keys match if ANY non-None component is equal."""
    for i in range(3):
        if a[i] and b[i] and a[i] == b[i]:
            return True
    return False


def merge_group(group):
    """Merge multiple entries (same paper) into one canonical record."""
    # Pick id: arxiv id > doi: > openalex:
    arxiv_ids = [pid for e in group if (pid := get_arxiv_id_strict(e))]
    primary_id = arxiv_ids[0] if arxiv_ids else None
    if not primary_id:
        doi_ids = [e['id'] for e in group if (e.get('id') or '').startswith('doi:')]
        if doi_ids:
            primary_id = doi_ids[0]
        else:
            other_ids = [e['id'] for e in group if e.get('id')]
            primary_id = other_ids[0] if other_ids else None

    real_dois = [normalize_doi(e.get('doi')) for e in group if e.get('doi')]
    real_dois = [d for d in real_dois if d and not is_arxiv_doi(d)]
    journal_doi = real_dois[0] if real_dois else None

    journals = [e.get('journal') for e in group if e.get('journal')]
    journal = journals[0] if journals else None

    years = [e.get('year') for e in group if isinstance(e.get('year'), int)]
    year = max(years) if years else None

    titles = [e.get('title', '') for e in group if e.get('title')]
    title = max(titles, key=len) if titles else ''

    # Coauthors: union, prefer slug-resolved entries
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

    src_set = set()
    for e in group:
        for s in (e.get('sources') or []):
            src_set.add(s)
    sources = sorted(src_set)

    pcs = [e.get('primary_category') for e in group if e.get('primary_category')]
    pc = pcs[0] if pcs else None

    oa_ids = [e.get('openalex_id') for e in group if e.get('openalex_id')]
    oa_id = oa_ids[0] if oa_ids else None

    has_arxiv = bool(arxiv_ids)
    no_arxiv = (not has_arxiv) and any(e.get('no_arxiv') for e in group)

    out = {
        'id': primary_id,
        'title': title,
        'year': year,
        'coauthors': merged_coauthors,
    }
    if journal_doi:
        out['doi'] = journal_doi
    if journal:
        out['journal'] = journal
    if pc:
        out['primary_category'] = pc
    if oa_id:
        out['openalex_id'] = oa_id
    if sources:
        out['sources'] = sources
    if no_arxiv:
        out['no_arxiv'] = True
    return out


def is_published(pub):
    """A pub counts as published when there's a real journal-DOI or a journal name."""
    raw = normalize_doi(pub.get('doi'))
    if raw and not is_arxiv_doi(raw):
        return True
    if pub.get('journal'):
        return True
    return False


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


def collapse_within_yaml(pubs):
    """Group pubs by canonical paper key (any of doi/arxiv/title matches),
    merge each group. Returns list of canonical pubs."""
    # We use a union-find by linking entries that share any non-null key
    n = len(pubs)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    keys = [paper_key(p) for p in pubs]
    # link pairs that share any non-null key
    by_doi = {}
    by_arxiv = {}
    by_title = {}
    for i, k in enumerate(keys):
        d, a, t = k
        if d:
            if d in by_doi:
                union(i, by_doi[d])
            else:
                by_doi[d] = i
        if a:
            if a in by_arxiv:
                union(i, by_arxiv[a])
            else:
                by_arxiv[a] = i
        if t:
            if t in by_title:
                union(i, by_title[t])
            else:
                by_title[t] = i

    groups = defaultdict(list)
    for i, p in enumerate(pubs):
        groups[find(i)].append(p)
    return [merge_group(g) if len(g) > 1 else g[0] for g in groups.values()]


def cross_yaml_sync(all_people):
    """Build a global canonical paper registry. For each paper coauthored by
    >=1 indexed slugs, the canonical record (post-merge) propagates to ALL
    coauthors' yamls."""
    # IMPORTANT: We deliberately do NOT auto-resolve raw English names to slugs.
    # English-name match alone is not identity (multiple "Ao Li", "Wei Zhang",
    # "Si Li" exist). Slug binding must happen upstream in the enrichment step
    # (lib_disambiguate_v2.py) using ORCID / affiliation / coauthor circle as
    # corroborating evidence. Here we only pass through fields that are
    # ALREADY recorded as slugs.
    def resolve_coauthor(s):
        if isinstance(s, str) and s in all_people:
            return s
        return s

    # Step 1: collect ALL pub entries across all yamls. Then union-find
    # merge by any-shared-key (real-doi OR arxiv-id OR canonical-title).
    # This is critical — the same paper might appear with id=doi:... in one yaml
    # and id=arxivid in another. Single-key indexing misses such duplicates.
    all_entries = []  # list of (slug, pub)
    for slug, person in all_people.items():
        for pub in (person.get('publications') or []):
            all_entries.append((slug, pub))

    n = len(all_entries)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    by_doi = {}
    by_arxiv = {}
    by_title = {}
    keys_per_entry = []
    for i, (_slug, pub) in enumerate(all_entries):
        d, a, t = paper_key(pub)
        keys_per_entry.append((d, a, t))
        if d:
            if d in by_doi:
                union(i, by_doi[d])
            else:
                by_doi[d] = i
        if a:
            if a in by_arxiv:
                union(i, by_arxiv[a])
            else:
                by_arxiv[a] = i
        if t:
            if t in by_title:
                union(i, by_title[t])
            else:
                by_title[t] = i

    # Step 2: group by component root.
    paper_sources = defaultdict(list)
    for i, (slug, pub) in enumerate(all_entries):
        if not any(keys_per_entry[i]):
            continue
        paper_sources[find(i)].append((slug, pub))

    # Step 3: for each paper, merge all variants into ONE canonical record;
    # determine the full coauthor set.
    canonical = {}  # group-root -> canonical pub dict
    paper_owners = {}  # paper-key -> set(slugs)
    for k, entries in paper_sources.items():
        merged = merge_group([p for _, p in entries])
        # Resolve raw-name coauthors to slugs where possible
        resolved = []
        seen = set()
        for c in (merged.get('coauthors') or []):
            r = resolve_coauthor(c) if isinstance(c, str) else c
            if r and r not in seen:
                seen.add(r)
                resolved.append(r)
        merged['coauthors'] = resolved

        # Owners = slugs that have this paper now or are coauthors
        owners = {slug for slug, _ in entries}
        for c in resolved:
            if isinstance(c, str) and c in all_people:
                owners.add(c)
        canonical[k] = merged
        paper_owners[k] = owners

    # Step 3: rebuild each yaml's publications list from canonical.
    new_pubs_by_slug = defaultdict(list)
    for k, owners in paper_owners.items():
        canon = canonical[k]
        for slug in owners:
            # Build the per-yaml entry: drop self from coauthors
            entry = dict(canon)
            entry['coauthors'] = [c for c in (canon.get('coauthors') or []) if c != slug]
            new_pubs_by_slug[slug].append(entry)
    return new_pubs_by_slug


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    all_people = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            all_people[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}

    new_pubs_by_slug = cross_yaml_sync(all_people)

    files_changed = 0
    total_pubs = 0
    for slug, person in all_people.items():
        new_pubs = new_pubs_by_slug.get(slug, [])
        # Sort newest first
        new_pubs.sort(key=lambda p: -(p.get('year') or 0))
        old_pubs = person.get('publications') or []

        # Compare: if final list differs (in count or content) → write
        old_ids = sorted((p.get('id') or '') for p in old_pubs)
        new_ids = sorted((p.get('id') or '') for p in new_pubs)
        if old_ids == new_ids and len(old_pubs) == len(new_pubs):
            # Even if id list identical, fields might differ; do a deeper check
            if all(
                (a.get('id'), a.get('doi'), a.get('journal'), tuple(sorted(a.get('coauthors') or [])))
                == (b.get('id'), b.get('doi'), b.get('journal'), tuple(sorted(b.get('coauthors') or [])))
                for a, b in zip(sorted(old_pubs, key=lambda x: x.get('id') or ''),
                                 sorted(new_pubs, key=lambda x: x.get('id') or ''))
            ):
                continue

        files_changed += 1
        total_pubs += len(new_pubs)

        delta = len(new_pubs) - len(old_pubs)
        if args.dry_run:
            print(f'  {slug}: {len(old_pubs)} → {len(new_pubs)} ({"+" if delta >= 0 else ""}{delta})')
            continue

        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        text = replace_block(text, 'publications', render_pubs(new_pubs))
        # Recompute activity
        try:
            p2 = yaml.safe_load(text)
            pubs2 = p2.get('publications') or []
            pc = sum(1 for p in pubs2 if is_published(p))
            prc = len(pubs2) - pc
            activity = dict(p2.get('activity') or {})
            activity['total_papers'] = len(pubs2)
            activity['published_count'] = pc
            activity['preprint_only_count'] = prc
            text = replace_block(text, 'activity', render_activity(activity))
        except Exception as e:
            print(f'  warn: {slug} activity recompute failed: {e}', file=sys.stderr)
        with open(path, 'w') as f:
            f.write(text)
        print(f'  {slug}: {len(old_pubs)} → {len(new_pubs)} ({"+" if delta >= 0 else ""}{delta})')

    print(f'\n{files_changed} files {"would be changed (dry-run)" if args.dry_run else "changed"}, '
          f'{total_pubs} total canonical pub entries')


if __name__ == '__main__':
    main()
