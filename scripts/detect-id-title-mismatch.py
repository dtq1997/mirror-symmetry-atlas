#!/usr/bin/env python3
"""Detect papers whose arXiv id doesn't match their title in our yaml.

This catches data-pollution where someone wrote the wrong arxiv id next to a
title (e.g. zong-zhengyu has 2211.09203 labeled "All genus open-closed mirror
symmetry..." but that arxiv id is actually an EE paper "Multidimensional
Eigenwave Multiplexing").

For each pub with arxiv id where we have cached real authors, fetch the title
from cache (re-fetched by build-paper-titles-cache.py if needed). If yaml
title's canonical form doesn't substring-match arxiv title's canonical form,
flag it.

Output: data/papers/_id-title-mismatches.md (review list)
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paper_identity import canonical_title

PEOPLE_DIR = 'data/people'
TITLE_CACHE = 'data/papers/_arxiv_titles_cache'
OUT = 'data/papers/_id-title-mismatches.md'


def fetch_title(aid, delay=4):
    os.makedirs(TITLE_CACHE, exist_ok=True)
    safe = aid.replace('/', '_')
    cache = os.path.join(TITLE_CACHE, f'{safe}.json')
    if os.path.exists(cache):
        try:
            return json.load(open(cache)).get('title', '')
        except json.JSONDecodeError:
            pass
    time.sleep(delay)
    url = f'https://arxiv.org/abs/{aid}'
    r = subprocess.run(['curl', '-s', '--max-time', '20', '--noproxy', '*',
                        '-A', 'Mozilla/5.0', url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    m = re.search(r'citation_title"\s+content="([^"]+)"', r.stdout or '')
    title = m.group(1) if m else ''
    with open(cache, 'w') as f:
        json.dump({'title': title}, f, ensure_ascii=False)
    return title


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true', help='Remove mismatching pubs from yaml')
    args = parser.parse_args()

    mismatches = []  # list of (slug, pub, real_title)
    all_arxiv_ids = []
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            person = yaml.safe_load(fh) or {}
        for pub in (person.get('publications') or []):
            pid = pub.get('id', '').split('v')[0]
            if not pid or pid.startswith(('doi:', 'openalex:', 'cr:')):
                continue
            if not re.match(r'^\d{4}\.\d{4,5}$|^\d{7}$|^[a-z-]+/\d{7}$', pid):
                continue
            all_arxiv_ids.append((slug, pub))

    print(f'Checking {len(all_arxiv_ids)} arxiv-ided pubs...', file=sys.stderr)
    for i, (slug, pub) in enumerate(all_arxiv_ids):
        if i % 100 == 0:
            print(f'  {i}/{len(all_arxiv_ids)}', file=sys.stderr)
        pid = pub['id'].split('v')[0]
        real_title = fetch_title(pid)
        if not real_title:
            continue
        ours = canonical_title(pub.get('title') or '')
        theirs = canonical_title(real_title)
        if not ours or not theirs:
            continue
        # Match if shared token coverage >= 60%
        ot = set(ours.split())
        tt = set(theirs.split())
        if not ot or not tt:
            continue
        overlap = len(ot & tt) / min(len(ot), len(tt))
        if overlap < 0.5:
            mismatches.append((slug, pub, real_title))

    # Write report
    lines = ['# arXiv id ↔ title mismatch 报告\n']
    lines.append(f'扫描 {len(all_arxiv_ids)} 篇带 arxiv id 的 pub, '
                 f'发现 {len(mismatches)} 个不匹配。\n')
    by_slug = {}
    for slug, pub, real in mismatches:
        by_slug.setdefault(slug, []).append((pub, real))
    for slug, items in sorted(by_slug.items()):
        lines.append(f'## {slug} ({len(items)})\n')
        for pub, real in items:
            lines.append(f'- id: `{pub.get("id")}`')
            lines.append(f'  - YAML 中标的 title: {pub.get("title")}')
            lines.append(f'  - arXiv 实际 title: {real}')
            lines.append('')
    with open(OUT, 'w') as f:
        f.write('\n'.join(lines))
    print(f'\nWrote {OUT}: {len(mismatches)} mismatches across {len(by_slug)} people')

    if args.write and mismatches:
        # Remove mismatching pubs from each yaml
        for slug, items in by_slug.items():
            path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
            with open(path) as f:
                person = yaml.safe_load(f)
            bad_ids = {pub['id'].split('v')[0] for pub, _ in items}
            new_pubs = [p for p in (person.get('publications') or [])
                        if p.get('id', '').split('v')[0] not in bad_ids]
            if len(new_pubs) == len(person.get('publications') or []):
                continue
            person['publications'] = new_pubs
            with open(path) as f:
                text = f.read()
            from canonicalize_publications_helper import render_pubs
            # Inline the YAML-block writer to avoid import drama
            text = _replace_block(text, 'publications', _render_pubs(new_pubs))
            text = _recompute_activity(text, new_pubs)
            with open(path, 'w') as f:
                f.write(text)
            print(f'  removed {len(items)} bad-id pubs from {slug}')


def _squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def _render_pubs(pubs):
    lines = ['publications:']
    for p in pubs:
        if not p.get('id'):
            continue
        lines.append(f'  - id: {_squote(p["id"])}')
        lines.append(f'    title: {_squote(p.get("title") or "")}')
        if p.get('year') is not None:
            lines.append(f'    year: {p["year"]}')
        cas = p.get('coauthors') or []
        if cas:
            inner = ', '.join(c if re.fullmatch(r'[a-z][a-z0-9_-]*', str(c)) else _squote(c) for c in cas)
            lines.append(f'    coauthors: [{inner}]')
        else:
            lines.append('    coauthors: []')
        if p.get('doi'):
            lines.append(f'    doi: {_squote(p["doi"])}')
        if p.get('journal'):
            lines.append(f'    journal: {_squote(p["journal"])}')
        if p.get('primary_category'):
            lines.append(f'    primary_category: {p["primary_category"]}')
        if p.get('openalex_id'):
            lines.append(f'    openalex_id: {p["openalex_id"]}')
        if p.get('sources'):
            lines.append(f'    sources: [{", ".join(p["sources"])}]')
        if p.get('no_arxiv'):
            lines.append('    no_arxiv: true')
    return '\n'.join(lines)


def _replace_block(text, name, new_block):
    pat = re.compile(rf'^{name}:.*?(?=^[A-Za-z_][\w]*:|\Z)', re.MULTILINE | re.DOTALL)
    if pat.search(text):
        return pat.sub(lambda _m: new_block + '\n', text, count=1)
    return text


def _recompute_activity(text, pubs):
    pc = sum(1 for p in pubs if p.get('journal') or (
        p.get('doi') and not str(p['doi']).lower().startswith('10.48550/arxiv.')))
    prc = len(pubs) - pc
    text = re.sub(r"^(\s*total_papers:)\s*\d+",
                  lambda _m: f"  total_papers: {len(pubs)}", text, flags=re.MULTILINE)
    text = re.sub(r"^(\s*published_count:)\s*\d+",
                  lambda _m: f"  published_count: {pc}", text, flags=re.MULTILINE)
    text = re.sub(r"^(\s*preprint_only_count:)\s*\d+",
                  lambda _m: f"  preprint_only_count: {prc}", text, flags=re.MULTILINE)
    return text


if __name__ == '__main__':
    main()
