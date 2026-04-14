#!/usr/bin/env python3
"""Fetch arXiv papers for a specific author and output YAML-ready publications list.

Usage:
  python3 scripts/fetch-arxiv-by-author.py "Firstname Lastname" [--cats math-ph,math.AG] [--filter-coauthors "Name1,Name2"]

The --filter-coauthors flag is for common names: only papers with at least one known
collaborator OR math-relevant title keywords will be included.
"""

import sys
import time
import subprocess
import xml.etree.ElementTree as ET
import argparse
import urllib.parse

MATH_KEYWORDS = [
    'tau', 'bkp', 'kp ', 'hurwitz', 'gromov', 'witten', 'frobenius',
    'stokes', 'painlev', 'virasoro', 'cohomol', 'moduli', 'calabi',
    'mirror', 'integrab', 'hierarch', 'intersection', 'hodge', 'spectral',
    'vertex', 'topological', 'nekrasov', 'quantum', 'dessin', 'partition',
    'orbifold', 'holomorphic', 'anomaly', 'isomonodrom', 'monodromy',
    'euler', 'affine', 'schur', 'yang-baxter', 'poisson', 'symplect',
    'fukaya', 'remodel', 'crepant', 'enumerativ', 'categorical',
]

NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

def fetch_papers(author_name, cats=None, filter_coauthors=None, max_results=100):
    query = f'au:"{author_name}"'
    if cats:
        cat_query = ' OR '.join(f'cat:{c}' for c in cats)
        query = f'{query} AND ({cat_query})'

    url = f'https://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending'

    time.sleep(4)  # respect rate limit (arXiv requires 3s minimum between requests)
    result = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', '30', url], capture_output=True, text=True)
    if not result.stdout or 'Rate exceeded' in result.stdout:
        print(f'ERROR: arXiv rate limited or empty response. Wait 30s and retry.', file=sys.stderr)
        sys.exit(1)
    tree = ET.ElementTree(ET.fromstring(result.stdout))

    papers = []
    for entry in tree.findall('a:entry', NS):
        title = entry.find('a:title', NS).text.strip().replace('\n', ' ').replace('  ', ' ')
        full_id = entry.find('a:id', NS).text
        arxiv_id = full_id.split('/')[-1].split('v')[0]
        year = int(entry.find('a:published', NS).text[:4])
        authors = [a.find('a:name', NS).text for a in entry.findall('a:author', NS)]
        cats_found = [c.get('term') for c in entry.findall('arxiv:primary_category', NS)]

        # Verify author is actually in the list
        name_parts = author_name.lower().split()
        if not any(all(p in a.lower() for p in name_parts) for a in authors):
            continue

        # If filter mode, check collaborators or keywords
        if filter_coauthors:
            has_collab = any(c.lower() in ' '.join(authors).lower() for c in filter_coauthors)
            has_keyword = any(k in title.lower() for k in MATH_KEYWORDS)
            if not (has_collab or has_keyword):
                continue

        papers.append({
            'id': arxiv_id,
            'title': title,
            'year': year,
            'authors': authors,
            'category': cats_found[0] if cats_found else '',
        })

    return papers

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('author', help='Author name, e.g. "Chenglang Yang"')
    parser.add_argument('--cats', help='Comma-separated arXiv categories', default=None)
    parser.add_argument('--filter-coauthors', help='Comma-separated known collaborator names for filtering', default=None)
    parser.add_argument('--max', type=int, default=100)
    args = parser.parse_args()

    cats = args.cats.split(',') if args.cats else None
    coauthors = args.filter_coauthors.split(',') if args.filter_coauthors else None

    papers = fetch_papers(args.author, cats=cats, filter_coauthors=coauthors, max_results=args.max)

    print(f'# {args.author}: {len(papers)} papers found')
    print('publications:')
    for p in papers:
        coauth = [a for a in p['authors'] if not all(part in a.lower() for part in args.author.lower().split())]
        coauth_str = ', '.join(coauth[:4])
        if len(coauth) > 4:
            coauth_str += f' +{len(coauth)-4}'
        print(f'  - id: "{p["id"]}"')
        print(f'    title: "{p["title"]}"')
        print(f'    year: {p["year"]}')
        print(f'    coauthors_raw: [{coauth_str}]')

if __name__ == '__main__':
    main()
