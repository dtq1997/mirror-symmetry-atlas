#!/usr/bin/env python3
"""Use Crossref to verify "preprint-only" arXiv papers are actually published.

Background: arXiv API's <arxiv:journal_ref> field requires authors to update
manually after publication, and most don't. So our enrich pipeline reports
many papers as "preprint" that are in fact published. This script queries
Crossref by title to fill the gap.

Usage:
  python3 scripts/verify-published-via-crossref.py [slug1 slug2 ...] [--all]
  python3 scripts/verify-published-via-crossref.py --all --write [--mailto your@email]

Output:
  - Without --write: prints how many would be reclassified
  - With --write: updates each person YAML in place
  - Caches Crossref responses in .cache/msa/papers/_crossref_cache/{arxiv_id}.json

Heuristic: a Crossref hit counts as "published" iff
  (a) result.score >= 50 AND
  (b) normalized title similarity >= 0.85 (token-set ratio) AND
  (c) result.type == 'journal-article' OR result.container-title nonempty AND
      result.published-print/online has a year matching paper.year ± 1
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
from urllib.parse import quote
import yaml

from cache_paths import cache_path

PEOPLE_DIR = 'data/people'
CACHE_DIR = cache_path('_crossref_cache')


def normalize_title(s):
    s = (s or '').lower()
    s = re.sub(r'\$[^$]*\$', ' ', s)  # strip inline math
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def token_set_similarity(a, b):
    ta, tb = set(a.split()), set(b.split())
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta), len(tb))


def query_crossref(title, year, mailto=None, delay=0.3):
    """Returns dict with {doi, container, year, type} on confident match, else None."""
    norm_q = normalize_title(title)
    if not norm_q:
        return None
    url = f'https://api.crossref.org/works?query.bibliographic={quote(norm_q[:200])}&rows=3'
    if mailto:
        url += f'&mailto={quote(mailto)}'
    time.sleep(delay)
    try:
        r = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', '15', url],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        data = json.loads(r.stdout or '{}')
    except (json.JSONDecodeError, subprocess.SubprocessError):
        return None
    items = (data.get('message') or {}).get('items') or []
    for it in items:
        score = it.get('score', 0)
        cand_title = ' '.join((it.get('title') or [''])[:1])
        sim = token_set_similarity(normalize_title(cand_title), norm_q)
        if score < 50 or sim < 0.85:
            continue
        # Year check
        years = []
        for k in ('published-print', 'published-online', 'issued', 'created'):
            d = it.get(k)
            if isinstance(d, dict):
                parts = d.get('date-parts') or [[]]
                if parts and parts[0]:
                    years.append(parts[0][0])
        if year and years and not any(abs(int(y) - int(year)) <= 2 for y in years):
            continue
        ctype = it.get('type', '')
        container = ' '.join(it.get('container-title') or [])
        if ctype != 'journal-article' and not container:
            continue
        return {
            'doi': it.get('DOI'),
            'container': container,
            'year': years[0] if years else None,
            'type': ctype,
        }
    return None


def cached_query(arxiv_id, title, year, mailto):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f'{arxiv_id}.json')
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    res = query_crossref(title, year, mailto=mailto)
    with open(path, 'w') as f:
        json.dump(res or {}, f, ensure_ascii=False)
    return res or {}


def process_person(slug, mailto):
    path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
    with open(path) as f:
        person = yaml.safe_load(f)
    pubs = person.get('publications') or []
    upgraded = []
    for p in pubs:
        if p.get('journal') or p.get('doi'):
            continue
        aid = p.get('id', '')
        title = p.get('title', '')
        year = p.get('year')
        if not aid or not title:
            continue
        hit = cached_query(aid, title, year, mailto)
        if hit and hit.get('doi'):
            upgraded.append({
                'id': aid,
                'title': title[:60],
                'doi': hit['doi'],
                'container': hit.get('container'),
            })
    return person, upgraded


def write_back(slug, upgraded):
    """Patch the YAML text to inject doi: and journal: lines for upgraded papers."""
    if not upgraded:
        return 0
    path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
    with open(path) as f:
        text = f.read()
    count = 0
    for u in upgraded:
        aid = u['id']
        # Find the publication block by id, then inject doi/journal after coauthors line
        pattern = re.compile(
            rf"(  - id: '{re.escape(aid)}'.*?coauthors:.*?\n)",
            re.DOTALL
        )
        m = pattern.search(text)
        if not m:
            continue
        insert_lines = []
        if u.get('doi'):
            insert_lines.append(f"    doi: '{u['doi']}'")
        if u.get('container'):
            j = u['container'].replace("'", "''")
            insert_lines.append(f"    journal: '{j}'")
        if not insert_lines:
            continue
        injection = m.group(1) + '\n'.join(insert_lines) + '\n'
        text = text[:m.start()] + injection + text[m.end():]
        count += 1
    if count > 0:
        # Recompute activity counts
        person = yaml.safe_load(text)
        pubs = person.get('publications') or []
        published = sum(1 for p in pubs if p.get('journal') or p.get('doi'))
        preprint = len(pubs) - published
        # Replace activity block totals
        text = re.sub(
            r"^(\s*published_count:)\s*\d+",
            lambda _m: f"  published_count: {published}", text, flags=re.MULTILINE
        )
        text = re.sub(
            r"^(\s*preprint_only_count:)\s*\d+",
            lambda _m: f"  preprint_only_count: {preprint}", text, flags=re.MULTILINE
        )
        with open(path, 'w') as f:
            f.write(text)
    return count


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slugs', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--mailto', default='qiantang@tsinghua.edu.cn',
                        help='Crossref polite-pool mailto (gets higher rate limit)')
    args = parser.parse_args()

    if args.all:
        targets = sorted(s.replace('.yaml','') for s in os.listdir(PEOPLE_DIR) if s.endswith('.yaml'))
    elif args.slugs:
        targets = args.slugs
    else:
        print('Specify slugs or --all', file=sys.stderr)
        sys.exit(1)

    total_upgraded = 0
    for i, slug in enumerate(targets):
        print(f'[{i+1}/{len(targets)}] {slug} ...', file=sys.stderr)
        try:
            _, upgraded = process_person(slug, args.mailto)
        except Exception as e:
            print(f'  error: {e}', file=sys.stderr)
            continue
        if upgraded:
            print(f'  {len(upgraded)} preprints upgrade to published', file=sys.stderr)
            for u in upgraded[:3]:
                print(f"    {u['id']} -> {u['doi']} ({u.get('container','')[:50]})", file=sys.stderr)
            if len(upgraded) > 3:
                print(f'    ... +{len(upgraded)-3} more', file=sys.stderr)
            total_upgraded += len(upgraded)
            if args.write:
                n = write_back(slug, upgraded)
                print(f'  wrote {n} entries', file=sys.stderr)

    print(f'\nTOTAL: {total_upgraded} preprints reclassified as published')


if __name__ == '__main__':
    main()
