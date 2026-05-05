#!/usr/bin/env python3
"""Roll back: remove all publications whose sources contain 'openalex'.
Keep arXiv-sourced ones. Recompute activity counts.

Usage:
  python3 scripts/rollback-openalex.py [--dry-run]
"""

import argparse
import os
import re
import sys
import yaml

PEOPLE_DIR = 'data/people'


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def coauthor_inline(c):
    s = str(c)
    if s and re.fullmatch(r'[a-z][a-z0-9_-]*', s):
        return s
    return squote(s)


def render_pubs(pubs):
    lines = ['publications:']
    for p in pubs:
        pid = p.get('id')
        if not pid:
            continue
        lines.append(f'  - id: {squote(pid)}')
        lines.append(f'    title: {squote(p.get("title") or "")}')
        if p.get('year') is not None:
            lines.append(f'    year: {p["year"]}')
        cas = p.get('coauthors') or []
        if cas:
            lines.append(f'    coauthors: [{", ".join(coauthor_inline(c) for c in cas)}]')
        else:
            lines.append('    coauthors: []')
        if p.get('doi'):
            lines.append(f'    doi: {squote(p["doi"])}')
        if p.get('journal'):
            lines.append(f'    journal: {squote(p["journal"])}')
        if p.get('primary_category'):
            lines.append(f'    primary_category: {p["primary_category"]}')
        if p.get('sources'):
            lines.append(f'    sources: [{", ".join(p["sources"])}]')
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

    total_removed = 0
    affected = 0
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        path = os.path.join(PEOPLE_DIR, f)
        with open(path) as fh:
            person = yaml.safe_load(fh)
        pubs = person.get('publications') or []
        kept = []
        removed = 0
        for p in pubs:
            srcs = p.get('sources') or []
            # Remove if openalex is the only source. Keep if arxiv is also a source.
            if 'openalex' in srcs and 'arxiv' not in srcs:
                removed += 1
            else:
                # If both arxiv and openalex, strip openalex from sources
                if 'openalex' in srcs:
                    srcs = [s for s in srcs if s != 'openalex']
                    p['sources'] = srcs or ['arxiv']
                # Strip openalex_id and no_arxiv to keep yaml clean of stale OA refs
                p.pop('openalex_id', None)
                p.pop('no_arxiv', None)
                kept.append(p)
        if removed == 0 and not any('openalex' in (p.get('sources') or []) for p in pubs):
            continue
        affected += 1
        total_removed += removed
        if args.dry_run:
            print(f'  {f}: would remove {removed}, keep {len(kept)}')
            continue
        with open(path) as fh:
            text = fh.read()
        text = replace_block(text, 'publications', render_pubs(kept))
        # Recompute activity
        person2 = yaml.safe_load(text)
        pubs2 = person2.get('publications') or []
        pub_c = sum(1 for p in pubs2 if p.get('journal') or p.get('doi'))
        pre_c = len(pubs2) - pub_c
        activity = dict(person2.get('activity') or {})
        activity['total_papers'] = len(pubs2)
        activity['published_count'] = pub_c
        activity['preprint_only_count'] = pre_c
        text = replace_block(text, 'activity', render_activity(activity))
        with open(path, 'w') as fh:
            fh.write(text)
        print(f'  {f}: removed {removed}, kept {len(kept)}')

    print(f'\n{affected} files affected, {total_removed} OpenAlex-only papers removed')


if __name__ == '__main__':
    main()
