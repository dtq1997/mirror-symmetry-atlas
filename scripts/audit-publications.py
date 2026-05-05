#!/usr/bin/env python3
"""Audit existing publications across all people YAML files.

For every person, fetches arXiv candidates (math-only) and re-scores their
recorded publications + flags missing ones.

Output: data/papers/_audit-report.yaml with structure:
  generated_at: ISO datetime
  per_person:
    <slug>:
      recorded_count: int
      math_candidate_count: int
      recorded_low_score: [{id, title, score, signals}]   # recorded but suspicious
      missing_high_score: [{id, title, score, signals}]   # not recorded but math-matched
      total_papers_declared: int

Usage:
  python3 scripts/audit-publications.py [slug1 slug2 ...] [--all]
  python3 scripts/audit-publications.py --slug-list zhangwei,si-li
"""

import argparse
import os
import sys
import time
from datetime import datetime, timezone
import yaml

# Allow running from repo root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_disambiguate import (
    load_all_people, fetch_candidates_for_person, disambiguate,
)


def audit_person(slug, person, all_people, threshold=10, fetch_delay=4):
    target_name = (person.get('name') or {}).get('en', '')
    if not target_name:
        return None
    candidates = fetch_candidates_for_person(target_name, max_results=200,
                                              math_only=True, delay=fetch_delay)
    recorded_ids = {(p.get('id') or '').split('v')[0] for p in (person.get('publications') or [])}

    scored = []
    for c in candidates:
        score, signals = disambiguate(person, c, all_people, use_submitter=False,
                                       target_name=target_name)
        scored.append({**c, 'score': score, 'signals': signals})

    recorded_low = []
    found_match_ids = set()
    for c in scored:
        if c['id'] in recorded_ids:
            found_match_ids.add(c['id'])
            if c['score'] < threshold:
                recorded_low.append({
                    'id': c['id'], 'title': c['title'], 'year': c['year'],
                    'score': c['score'], 'signals': c['signals'],
                })

    missing_recorded = recorded_ids - found_match_ids
    missing_high = []
    for c in scored:
        if c['id'] not in recorded_ids and c['score'] >= threshold:
            missing_high.append({
                'id': c['id'], 'title': c['title'], 'year': c['year'],
                'score': c['score'], 'signals': c['signals'],
            })

    return {
        'recorded_count': len(recorded_ids),
        'math_candidate_count': len(candidates),
        'total_papers_declared': (person.get('activity') or {}).get('total_papers'),
        'recorded_low_score': recorded_low,
        'missing_recorded_in_math_query': sorted(missing_recorded),
        'missing_high_score': missing_high[:50],  # cap
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slugs', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--threshold', type=int, default=10)
    parser.add_argument('--delay', type=int, default=4)
    parser.add_argument('--output', default='data/papers/_audit-report.yaml')
    args = parser.parse_args()

    all_people = load_all_people()
    if args.all:
        targets = list(all_people.keys())
    elif args.slugs:
        targets = args.slugs
    else:
        print('Specify slugs or --all', file=sys.stderr)
        sys.exit(1)

    report = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'threshold': args.threshold,
        'per_person': {},
    }

    for i, slug in enumerate(targets):
        person = all_people.get(slug)
        if not person:
            print(f'  [{i+1}/{len(targets)}] {slug} NOT FOUND', file=sys.stderr)
            continue
        print(f'  [{i+1}/{len(targets)}] {slug} ...', file=sys.stderr)
        try:
            entry = audit_person(slug, person, all_people,
                                  threshold=args.threshold, fetch_delay=args.delay)
        except Exception as e:
            print(f'    error: {e}', file=sys.stderr)
            continue
        if entry:
            report['per_person'][slug] = entry

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w') as f:
        yaml.dump(report, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    print(f'Wrote audit report to {args.output}', file=sys.stderr)


if __name__ == '__main__':
    main()
