"""Audit MISSING publications: each yaml owner's expected papers vs current.

For each yaml, fetch the arxiv author search results (constrained to math /
math-ph categories). For each candidate paper:
  - canonical id form arxiv id
  - if NOT in this yaml's publications: this is a candidate "missing" paper

Output a markdown report listing per-slug:
  - papers in arxiv that we don't have
  - papers we have but arxiv doesn't (these are likely DOI-only / Crossref)

Conservative: low recall is the user's biggest worry. We want to surface
EVERY paper that might belong to this person, even at the cost of false
positives that the user can scan past.

Categories used (broad, not narrow):
  math.* (all subdomains), math-ph, nlin.SI, hep-th, cs.LG (rare math overlap),
  q-alg, dg-ga, alg-geom (legacy)
"""
import argparse
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'
CACHE_DIR = ROOT / 'data/papers/_arxiv_author_search_cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUT = ROOT / 'data/papers/_missing_paper_review.md'

NS = {'a': 'http://www.w3.org/2005/Atom',
      'arxiv': 'http://arxiv.org/schemas/atom'}

MATH_CATS = (
    'math.AG', 'math.AT', 'math.AP', 'math.CT', 'math.CA', 'math.CO',
    'math.DG', 'math.DS', 'math.FA', 'math.GT', 'math.MP', 'math.OA',
    'math.PR', 'math.QA', 'math.RA', 'math.RT', 'math.SG', 'math.SP',
    'math.ST', 'math.NT', 'math.GR', 'math.HO',
    'math-ph', 'nlin.SI', 'nlin.CD', 'hep-th', 'q-alg', 'dg-ga',
    'alg-geom', 'cond-mat.stat-mech',
)


def fetch_arxiv_author(name, max_results=200, delay=3):
    """Search arxiv API for author, return list of (arxiv_id, title, year, primary_cat)."""
    safe = re.sub(r'[^a-zA-Z]', '_', name)
    cache = CACHE_DIR / f'{safe}.xml'
    if cache.exists():
        try:
            text = cache.read_text()
        except Exception:
            text = None
    else:
        text = None
    if not text:
        time.sleep(delay)
        # quote name; restrict to math primary categories. Use %22 (URL-
        # encoded quote) so subprocess invocations don't get tripped by the
        # raw " character.
        cat_query = '+OR+'.join(f'cat:{c}' for c in MATH_CATS)
        encoded_name = name.replace(' ', '+')
        url = (f'https://export.arxiv.org/api/query?'
               f'search_query=au:%22{encoded_name}%22+AND+({cat_query})'
               f'&max_results={max_results}')
        r = subprocess.run(['curl', '-sLk', '--noproxy', '*', '--max-time', '40',
                             url],
                            capture_output=True, text=True, encoding='utf-8',
                            errors='replace')
        text = r.stdout or ''
        if text and len(text) > 500:
            cache.write_text(text)
    if not text:
        return []
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return []
    out = []
    for entry in root.findall('a:entry', NS):
        aid = entry.find('a:id', NS)
        if aid is None:
            continue
        m = re.search(r'/abs/([\w./-]+?)(v\d+)?$', aid.text or '')
        if not m:
            continue
        arxiv_id = m.group(1)
        title = (entry.find('a:title', NS).text or '').strip().replace('\n', ' ')
        title = re.sub(r'\s+', ' ', title)
        published = entry.find('a:published', NS)
        year = int(published.text[:4]) if published is not None else None
        primary = entry.find('arxiv:primary_category', NS)
        primary_cat = primary.get('term') if primary is not None else None
        # Keep names of authors so we can do downstream verification
        authors = [a.find('a:name', NS).text
                   for a in entry.findall('a:author', NS)
                   if a.find('a:name', NS) is not None]
        out.append({
            'id': arxiv_id, 'title': title, 'year': year,
            'primary_category': primary_cat, 'authors': authors,
        })
    return out


def normalize_id(s):
    if not s:
        return s
    return s.split('v')[0]


def main(slugs=None):
    sys.path.insert(0, str(Path(__file__).parent))
    from name_match import names_compatible

    all_people = {}
    for f in sorted(PEOPLE_DIR.glob('*.yaml')):
        if f.name.startswith('_'):
            continue
        all_people[f.stem] = yaml.safe_load(f.read_text()) or {}

    if slugs:
        targets = {s: all_people[s] for s in slugs if s in all_people}
    else:
        targets = all_people

    report_lines = ['# Missing-paper audit',
                    '',
                    '生成方式: 用 arxiv author search 拉每位 owner 的论文,',
                    '与 yaml.publications 对比.',
                    '',
                    '**Action**: 每个候选论文需人工判断:',
                    '  - 是这个人的 → 应该添加到 yaml',
                    '  - 是同名作者的 → 忽略 (但可能要加进 review_queue)',
                    '',
                    '已知陷阱:',
                    '  - arxiv 拉取仍会含同名作者污染 (尤其 "Wang Zhiyuan" 等常见名)',
                    '  - 但**漏掉真正的论文比加进同名污染更严重** — 用户能看到多的不能看到漏的',
                    '',
                    f'扫描了 {len(targets)} 位学者.',
                    '']

    total_missing = 0
    for slug, person in targets.items():
        en = ((person.get('name') or {}).get('en') or '').strip()
        if not en:
            continue
        existing_ids = set()
        for p in (person.get('publications') or []):
            if not isinstance(p, dict):
                continue
            pid = normalize_id(p.get('id') or '')
            if pid and not pid.startswith(('doi:', 'openalex:', 'cr:')):
                existing_ids.add(pid)

        candidates = fetch_arxiv_author(en)
        if not candidates:
            continue

        missing = []
        for c in candidates:
            cid = normalize_id(c['id'])
            if cid in existing_ids:
                continue
            # Owner must appear in author list (compatible match) so we don't
            # surface the obvious different-person hits as "missing" — those
            # are NOT missing, they were correctly never assigned.
            if not any(names_compatible(en, a) for a in c.get('authors') or []):
                continue
            missing.append(c)

        if not missing:
            continue
        report_lines.append(f'\n## {slug} (en={en}) — {len(missing)} candidates not in yaml\n')
        for c in sorted(missing, key=lambda x: -(x['year'] or 0)):
            authors_str = ', '.join((c.get('authors') or [])[:5])
            report_lines.append(
                f"- [{c['year']}] {c['title'][:90]}\n"
                f"  - arxiv: `{c['id']}` ({c.get('primary_category')})\n"
                f"  - authors: {authors_str}\n"
            )
            total_missing += 1

    report_lines.insert(8, f'**Total missing-candidate count: {total_missing}**.')
    report_lines.insert(9, '')
    OUT.write_text('\n'.join(report_lines))
    print(f'Wrote {OUT} — {total_missing} missing candidates across '
          f'{len(targets)} slugs scanned')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--slug', action='append', help='Only scan this slug (can pass multiple)')
    args = parser.parse_args()
    main(slugs=args.slug)
