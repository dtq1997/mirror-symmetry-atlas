#!/usr/bin/env python3
"""Crossref-based supplementary enrichment.

Runs AFTER OpenAlex enrich. Two purposes:

1. **Catch recent papers OpenAlex hasn't indexed yet.**
   Query Crossref by author name + identity_profile signals; for each hit,
   if the paper is not already in publications and the disambiguator scores
   it as accept, add it (sources=['crossref']).

2. **Fill missing journal/DOI on existing publications.**
   For each pub that is "preprint" (no journal/no doi) but has a clear
   arXiv id, query Crossref by title; if a confident journal hit exists,
   write the journal+doi back.

Crossref API:
  /works?query.author=...&rows=20&select=DOI,title,container-title,...
  /works?query.bibliographic=<title>

Usage:
  python3 scripts/crossref-supplementary-enrich.py [slug ...] [--all] [--write]
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_disambiguate_v2 import score_candidate

PEOPLE_DIR = 'data/people'
CACHE_DIR = 'data/papers/_crossref_cache'
MAILTO = 'qiantang@tsinghua.edu.cn'


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def http(url, timeout=20):
    r = subprocess.run(['curl', '-s', '--max-time', str(timeout), '--noproxy', '*', url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if not r.stdout:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def normalize_doi(d):
    if not d:
        return None
    s = str(d).lower().strip()
    return re.sub(r'^https?://(dx\.)?doi\.org/', '', s) or None


def normalize_title(s):
    s = (s or '').lower()
    s = re.sub(r'\$[^$]*\$', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def title_match(a, b):
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    sa, sb = set(na.split()), set(nb.split())
    return sa and sb and len(sa & sb) / max(len(sa), len(sb)) >= 0.85


def crossref_by_author(name, rows=30):
    url = (f'https://api.crossref.org/works?query.author={urllib.parse.quote(name)}'
           f'&rows={rows}&mailto={MAILTO}'
           f'&filter=from-pub-date:2014')
    time.sleep(0.5)
    d = http(url)
    if not d:
        return []
    return (d.get('message') or {}).get('items') or []


def crossref_by_title(title, rows=3):
    if not title:
        return []
    url = (f'https://api.crossref.org/works?query.bibliographic={urllib.parse.quote(title[:200])}'
           f'&rows={rows}&mailto={MAILTO}')
    time.sleep(0.3)
    d = http(url)
    if not d:
        return []
    return (d.get('message') or {}).get('items') or []


def cr_to_paper(item, target_name):
    """Convert Crossref item to our internal paper representation matching
    the structure that lib_disambiguate_v2.score_candidate expects."""
    title = ' '.join(item.get('title') or [])
    if not title:
        return None
    year_parts = ((item.get('published') or item.get('published-online')
                    or item.get('issued') or {}).get('date-parts') or [[None]])
    year = year_parts[0][0] if year_parts and year_parts[0] else None
    venue = ' '.join(item.get('container-title') or [])
    doi = normalize_doi(item.get('DOI'))
    cr_authors = []
    for a in (item.get('author') or []):
        n = (a.get('given', '') + ' ' + a.get('family', '')).strip()
        if not n:
            continue
        cr_authors.append({
            'author': {
                'display_name': n,
                'orcid': a.get('ORCID'),
            },
            'institutions': [
                {'display_name': aff.get('name', '')} for aff in (a.get('affiliation') or [])
            ],
        })
    paper = {
        'title': title,
        'publication_year': year,
        'authorships': cr_authors,
        'primary_location': {'source': {'display_name': venue}} if venue else {},
        'primary_category': None,
    }
    return paper, {
        'title': title, 'year': year, 'doi': doi, 'venue': venue,
    }


def discover_new_papers(slug, person, write):
    """Crossref by-author search. Add accepted hits to publications."""
    name_en = (person.get('name') or {}).get('en') or ''
    if not name_en:
        return 0
    profile = dict(person.get('identity_profile') or {})
    # Pull ORCID from external_ids if profile missing it
    if not profile.get('orcid'):
        ext = person.get('external_ids') or {}
        if ext.get('orcid'):
            profile['orcid'] = ext['orcid']
    existing_dois = set()
    existing_titles_norm = set()
    for pub in (person.get('publications') or []):
        if pub.get('doi'):
            existing_dois.add(normalize_doi(pub['doi']))
        existing_titles_norm.add(normalize_title(pub.get('title') or ''))

    items = crossref_by_author(name_en, rows=40)
    added = []
    for it in items:
        paper, meta = cr_to_paper(it, name_en) or (None, None)
        if not paper:
            continue
        if meta['doi'] and meta['doi'] in existing_dois:
            continue
        if normalize_title(meta['title']) in existing_titles_norm:
            continue
        decision, score, evidence = score_candidate(paper, profile, name_en)
        if decision != 'accept':
            continue
        added.append({**meta, 'evidence': evidence, 'score': score})

    if added and write:
        # Build new pub entries
        new_pubs = []
        for a in added:
            entry = {
                'id': f"doi:{a['doi']}" if a['doi'] else f"cr:{normalize_title(a['title'])[:40]}",
                'title': a['title'],
                'year': a['year'],
                'coauthors': [],  # we don't have slug-resolved coauthors from CR easily; leave empty
                'sources': ['crossref'],
                'no_arxiv': True,
            }
            if a['doi']:
                entry['doi'] = a['doi']
            if a['venue']:
                entry['journal'] = a['venue']
            new_pubs.append(entry)
        # Append to publications block in YAML text
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        # Find publications: block end (next top-level key)
        m = re.search(r'^publications:.*?(?=^[A-Za-z_][\w]*:|\Z)', text, re.MULTILINE | re.DOTALL)
        if m:
            block = m.group(0).rstrip() + '\n'
            for entry in new_pubs:
                block += f'  - id: {squote(entry["id"])}\n'
                block += f'    title: {squote(entry["title"])}\n'
                if entry['year']:
                    block += f'    year: {entry["year"]}\n'
                block += '    coauthors: []\n'
                if entry.get('doi'):
                    block += f'    doi: {squote(entry["doi"])}\n'
                if entry.get('journal'):
                    block += f'    journal: {squote(entry["journal"])}\n'
                block += f'    sources: [crossref]\n'
                block += f'    no_arxiv: true\n'
            text = text[:m.start()] + block + text[m.end():]
            # Recompute activity counts
            try:
                p2 = yaml.safe_load(text)
                pubs = p2.get('publications') or []
                pc = sum(1 for p in pubs if p.get('journal') or p.get('doi'))
                prc = len(pubs) - pc
                act_pat = re.compile(r'^activity:.*?(?=^[A-Za-z_][\w]*:|\Z)', re.MULTILINE | re.DOTALL)
                am = act_pat.search(text)
                if am:
                    activity = p2.get('activity') or {}
                    activity['total_papers'] = len(pubs)
                    activity['published_count'] = pc
                    activity['preprint_only_count'] = prc
                    new_lines = ['activity:']
                    order = ['total_papers', 'published_count', 'preprint_only_count', 'h_index',
                             'mathscinet_citations', 'google_scholar_citations',
                             'active_period', 'peak_period', 'phd_students',
                             'academic_descendants', 'last_arxiv_paper', 'confidence']
                    keys = order + [k for k in activity if k not in order]
                    for k in keys:
                        v = activity.get(k)
                        if v is None:
                            continue
                        if isinstance(v, str):
                            new_lines.append(f'  {k}: {squote(v)}')
                        elif isinstance(v, list):
                            new_lines.append(f'  {k}: {v}')
                        else:
                            new_lines.append(f'  {k}: {v}')
                    text = text[:am.start()] + '\n'.join(new_lines) + '\n' + text[am.end():]
            except Exception:
                pass
            with open(path, 'w') as f:
                f.write(text)
    return len(added), [a['title'][:60] for a in added]


def fill_missing_journal(slug, person, write):
    """For each preprint-only pub, query Crossref by title; if we get a
    confident match with a journal venue, write back doi+journal."""
    pubs = person.get('publications') or []
    upgraded = []
    for pub in pubs:
        if pub.get('journal') or pub.get('doi'):
            continue
        # arXiv id only (skip cr:/doi:/openalex:)
        pid = pub.get('id', '')
        if pid.startswith(('cr:', 'doi:', 'openalex:')):
            continue
        items = crossref_by_title(pub.get('title') or '', rows=3)
        for it in items:
            cr_title = ' '.join(it.get('title') or [])
            if not title_match(cr_title, pub.get('title')):
                continue
            cr_year = ((it.get('published') or it.get('published-online')
                         or it.get('issued') or {}).get('date-parts') or [[None]])[0][0]
            if pub.get('year') and cr_year and abs(int(cr_year) - int(pub['year'])) > 2:
                continue
            ctype = it.get('type', '')
            container = ' '.join(it.get('container-title') or [])
            if ctype != 'journal-article' and not container:
                continue
            doi = normalize_doi(it.get('DOI'))
            upgraded.append({
                'id': pid, 'doi': doi, 'venue': container,
                'title': pub.get('title'),
            })
            break

    if upgraded and write:
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        for u in upgraded:
            # Find the entry by id
            pat = re.compile(
                rf"(  - id: {re.escape(squote(u['id']))}.*?coauthors:[^\n]*\n)",
                re.DOTALL
            )
            m = pat.search(text)
            if not m:
                continue
            extras = []
            if u.get('doi'):
                extras.append(f"    doi: {squote(u['doi'])}")
            if u.get('venue'):
                extras.append(f"    journal: {squote(u['venue'])}")
            inj = m.group(1) + '\n'.join(extras) + '\n'
            text = text[:m.start()] + inj + text[m.end():]
        # Recompute
        try:
            p2 = yaml.safe_load(text)
            pubs = p2.get('publications') or []
            pc = sum(1 for p in pubs if p.get('journal') or p.get('doi'))
            prc = len(pubs) - pc
            text = re.sub(r"^(\s*published_count:)\s*\d+",
                          lambda _m: f"  published_count: {pc}", text, flags=re.MULTILINE)
            text = re.sub(r"^(\s*preprint_only_count:)\s*\d+",
                          lambda _m: f"  preprint_only_count: {prc}", text, flags=re.MULTILINE)
        except Exception:
            pass
        with open(path, 'w') as f:
            f.write(text)
    return len(upgraded)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slugs', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--mode', choices=['discover', 'journal', 'both'], default='both')
    args = parser.parse_args()

    targets = ([f.replace('.yaml', '') for f in sorted(os.listdir(PEOPLE_DIR)) if f.endswith('.yaml')]
                if args.all else args.slugs)
    if not targets:
        print('Specify slugs or --all', file=sys.stderr)
        sys.exit(1)

    discovered = 0
    upgraded = 0
    for i, slug in enumerate(targets):
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            person = yaml.safe_load(f)
        if not person:
            continue
        msg = f'[{i+1}/{len(targets)}] {slug}'
        if args.mode in ('discover', 'both'):
            n, samples = discover_new_papers(slug, person, args.write)
            discovered += n
            if n:
                msg += f' +{n} new'
                for s in samples[:2]:
                    msg += f'\n    + {s}'
        if args.mode in ('journal', 'both'):
            # reload after possible writes
            with open(path) as f:
                person = yaml.safe_load(f)
            n2 = fill_missing_journal(slug, person, args.write)
            upgraded += n2
            if n2:
                msg += f' / journal-upgrade {n2}'
        print(msg, file=sys.stderr)
    print(f'\nTotal: {discovered} new papers discovered, {upgraded} preprint→published upgrades')


if __name__ == '__main__':
    main()
