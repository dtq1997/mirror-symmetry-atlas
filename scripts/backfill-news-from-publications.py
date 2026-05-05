#!/usr/bin/env python3
"""Backfill 10 years of arXiv news (2016-now) by aggregating from per-person
publications already collected by enrich-publications.py.

Why this approach:
- arXiv API can't easily paginate by submittedDate window (paging works but
  hits the 30k result cap), and we'd query ~10 categories × 120 months.
- Person-level disambiguator already filtered out homonym contamination.
- Coverage = papers by anyone in our 92-person index, which matches the news
  feed's purpose (领域核心动态).

Output: one file per month at data/news/YYYY-MM.yaml (in addition to existing
daily files at data/news/YYYY-MM-DD.yaml).

Usage:
  python3 scripts/backfill-news-from-publications.py [--from 2016-01] [--to 2026-05]
  python3 scripts/backfill-news-from-publications.py --dry-run
"""

import argparse
import os
import sys
from collections import defaultdict
from datetime import datetime
import yaml

PEOPLE_DIR = 'data/people'
NEWS_DIR = 'data/news'


def load_all_publications():
    """Returns list of {id, title, year, month, primary_category, doi, journal,
    matched_people_slugs}. Pubs appearing in multiple persons' YAML get merged."""
    by_id = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            person = yaml.safe_load(fh) or {}
        for pub in (person.get('publications') or []):
            aid = (pub.get('id') or '').split('v')[0]
            if not aid:
                continue
            month = arxiv_id_to_month(aid)
            if not month:
                continue
            entry = by_id.setdefault(aid, {
                'id': aid,
                'title': pub.get('title', ''),
                'year': pub.get('year'),
                'month': month,
                'primary_category': pub.get('primary_category'),
                'doi': pub.get('doi'),
                'journal': pub.get('journal'),
                'matched_people': set(),
            })
            entry['matched_people'].add(slug)
            # Prefer richer metadata
            for k in ('doi', 'journal', 'primary_category'):
                if pub.get(k) and not entry.get(k):
                    entry[k] = pub[k]
    return list(by_id.values())


def arxiv_id_to_month(arxiv_id):
    """Convert arXiv id to YYYY-MM. Handles both new-style (YYMM.NNNNN) and
    old-style (subj-class/YYMMNNN) ids."""
    if '/' in arxiv_id:
        # Old style: subj-class/YYMMNNN
        tail = arxiv_id.split('/')[-1]
        if len(tail) >= 4 and tail[:4].isdigit():
            yymm = tail[:4]
        else:
            return None
    else:
        # New style: YYMM.NNNNN
        if '.' not in arxiv_id:
            return None
        yymm = arxiv_id.split('.')[0]
        if len(yymm) != 4 or not yymm.isdigit():
            return None
    yy = int(yymm[:2])
    mm = int(yymm[2:])
    if not (1 <= mm <= 12):
        return None
    year = 2000 + yy if yy < 90 else 1900 + yy
    return f'{year:04d}-{mm:02d}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--from', dest='from_month', default='2016-01')
    parser.add_argument('--to', dest='to_month', default=None,
                        help='Default: current month')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    if not args.to_month:
        args.to_month = datetime.now().strftime('%Y-%m')

    pubs = load_all_publications()
    print(f'Loaded {len(pubs)} unique publications across all people', file=sys.stderr)

    by_month = defaultdict(list)
    for p in pubs:
        if args.from_month <= p['month'] <= args.to_month:
            by_month[p['month']].append(p)

    print(f'In window {args.from_month}..{args.to_month}: {sum(len(v) for v in by_month.values())} pubs across {len(by_month)} months',
          file=sys.stderr)

    if args.dry_run:
        for m in sorted(by_month):
            print(f'  {m}: {len(by_month[m])} pubs')
        return

    os.makedirs(NEWS_DIR, exist_ok=True)
    written = 0
    for month, entries in sorted(by_month.items()):
        # Skip months that already have a daily file (existing 2026 data)
        # but always (re)write the YYYY-MM aggregate so it's idempotent
        # Sort: published first (richer metadata), then by date
        entries.sort(key=lambda e: ((not e.get('doi')), e.get('id') or ''))
        out = {
            'fetch_date': datetime.now().strftime('%Y-%m-%d'),
            'kind': 'monthly_backfill',
            'month': month,
            'source': 'aggregated from person YAMLs (enrich-publications output)',
            'total_count': len(entries),
            'entries': [
                {
                    'id': e['id'],
                    'title': e['title'],
                    'matched_people': sorted(e['matched_people']),
                    'primary_category': e.get('primary_category'),
                    **({'doi': e['doi']} if e.get('doi') else {}),
                    **({'journal': e['journal']} if e.get('journal') else {}),
                }
                for e in entries
            ],
        }
        path = os.path.join(NEWS_DIR, f'{month}.yaml')
        with open(path, 'w') as f:
            yaml.dump(out, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        written += 1
    print(f'Wrote {written} monthly files to {NEWS_DIR}/', file=sys.stderr)


if __name__ == '__main__':
    main()
