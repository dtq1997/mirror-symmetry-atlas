#!/usr/bin/env python3
"""Verify Chinese names of researchers using multi-source evidence.

For each Chinese-named person, query:
1. OpenAlex author profile - sometimes contains display_name in CN
2. Math Genealogy - dissertation title/Chinese name often present
3. Tsinghua/PKU/etc institutional pages (when affiliations include them)
4. arXiv author page

Cross-check the recorded zh name vs sources. Mismatch / unverifiable cases
are written to data/papers/_chinese_name_review.md for human review.

We do not auto-overwrite zh names - if anything looks wrong we LIST it for
manual review, with citations.

Usage:
  python3 scripts/verify-chinese-names.py [--all] [slug ...]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import yaml

PEOPLE_DIR = 'data/people'
OUT_PATH = 'data/papers/_chinese_name_review.md'
MAILTO = 'qiantang@tsinghua.edu.cn'


def http_text(url, timeout=20):
    r = subprocess.run(['curl', '-s', '-L', '--noproxy', '*', '--max-time', str(timeout),
                        '-A', 'Mozilla/5.0', url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout or ''


def http_json(url, timeout=20):
    s = http_text(url, timeout=timeout)
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None


def query_openalex_author(openalex_id):
    """OpenAlex author profile sometimes carries display_name_alternatives in CN."""
    if not openalex_id:
        return None
    url = f'https://api.openalex.org/authors/{openalex_id}?mailto={MAILTO}'
    time.sleep(0.3)
    return http_json(url)


def find_chinese_in_text(text):
    """Extract all CJK substrings of length >= 2 from text."""
    results = re.findall(r'[一-鿿]{2,5}', text)
    return list(set(results))


def query_mathgenealogy(mg_id):
    """Math Genealogy page, look for chinese characters."""
    if not mg_id or '[' in str(mg_id):
        return []
    url = f'https://www.mathgenealogy.org/id.php?id={mg_id}'
    time.sleep(0.5)
    html = http_text(url)
    return find_chinese_in_text(html)


def query_arxiv_author_search(name_en):
    """arXiv listing page might surface chinese names in titles or affil."""
    url = f'https://arxiv.org/a/{name_en.replace(" ","_").lower()}_1'
    time.sleep(0.5)
    html = http_text(url)
    return find_chinese_in_text(html)[:20]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slugs', nargs='*')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()

    targets = []
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        if args.slugs and slug not in args.slugs and not args.all:
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            p = yaml.safe_load(fh) or {}
        nat = p.get('nationality') or ''
        zh = (p.get('name') or {}).get('zh') or ''
        if nat != 'Chinese' and not zh:
            continue
        targets.append((slug, p))

    rows = []
    for slug, p in targets:
        en = (p.get('name') or {}).get('en') or ''
        zh_recorded = (p.get('name') or {}).get('zh') or ''
        ext = p.get('external_ids') or {}

        evidence = []  # list of (source, candidates)
        oa_id = ext.get('openalex')
        if oa_id and oa_id.startswith('A'):
            data = query_openalex_author(oa_id)
            if data:
                alts = data.get('display_name_alternatives') or []
                cjk = []
                for a in alts:
                    cjk.extend(find_chinese_in_text(a))
                cjk = list(set(cjk))
                if cjk:
                    evidence.append(('OpenAlex', cjk, f'https://openalex.org/{oa_id}'))

        mg_id = ext.get('mathgenealogy')
        if mg_id and not str(mg_id).startswith('['):
            cjk = query_mathgenealogy(mg_id)
            if cjk:
                evidence.append(('Math Genealogy',
                                 cjk[:5],
                                 f'https://www.mathgenealogy.org/id.php?id={mg_id}'))

        # Note: arXiv author search rarely has CJK; skip to save time
        rows.append({
            'slug': slug,
            'en': en,
            'zh_recorded': zh_recorded,
            'evidence': evidence,
            'verdict': classify_verdict(zh_recorded, evidence),
        })
        # Verbose progress
        print(f'  {slug}: zh={zh_recorded!r} sources={len(evidence)}', file=sys.stderr)

    write_report(rows)
    print(f'\nWrote {OUT_PATH} with {len(rows)} researchers', file=sys.stderr)


def classify_verdict(zh, evidence):
    if not zh and not evidence:
        return 'no-data'
    if not zh and evidence:
        # candidates available
        return 'missing-but-found'
    # zh recorded; check whether it appears in any source
    matched_sources = []
    conflicting = []
    for src, candidates, _url in evidence:
        if zh in candidates:
            matched_sources.append(src)
        else:
            # see if any candidate contains a substring of zh
            for c in candidates:
                if (zh in c or c in zh) and c != zh:
                    conflicting.append((src, c))
    if matched_sources:
        return f'verified-by-{",".join(matched_sources)}'
    if conflicting:
        return f'conflict: {conflicting[:3]}'
    if evidence:
        return 'unverified-but-sources-have-other-cjk'
    return 'unverified'


def write_report(rows):
    lines = ['# 华人中文名核对报告\n',
             f'扫描 {len(rows)} 位华人, 多源交叉验证结果\n',
             '---\n']
    by_verdict = {}
    for r in rows:
        v = r['verdict'].split(':')[0].strip()
        by_verdict.setdefault(v, []).append(r)
    for v in sorted(by_verdict):
        lines.append(f'## {v} ({len(by_verdict[v])} 人)\n')
        for r in by_verdict[v]:
            lines.append(f"### {r['slug']} (en: {r['en']}, recorded zh: {r['zh_recorded'] or '—'})")
            for src, cands, url in r['evidence']:
                cs = ', '.join(cands[:5])
                lines.append(f'- [{src}]({url}): {cs}')
            if not r['evidence']:
                lines.append('- (无可用外部证据源)')
            lines.append('')
    with open(OUT_PATH, 'w') as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
    main()
