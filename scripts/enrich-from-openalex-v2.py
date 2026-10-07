#!/usr/bin/env python3
"""Enrich publications with OpenAlex, using evidence-driven disambiguation v2.

For each person:
1. Use the OpenAlex id from external_ids if present.
   If not, search by name + use identity_profile.affiliations to disambiguate
   among same-name profiles. If still ambiguous, log to review queue.
2. Pull all works.
3. For each candidate work, score against identity_profile.
4. Accept (>=20) → merge; Reject (<10) → drop; Review (10-19) → write to
   data/papers/_review_queue/<slug>.yaml for human inspection.

Usage:
  python3 scripts/enrich-from-openalex-v2.py [--all] [--write] [slug]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from copy import deepcopy
import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cache_paths import cache_path
from lib_disambiguate_v2 import score_candidate
from publication_review import load_review, blocked_review, save_candidates

PEOPLE_DIR = 'data/people'
CACHE_DIR = cache_path('_openalex_cache')
REVIEW_DIR = 'data/papers/_review_queue'
MAILTO = 'qiantang@tsinghua.edu.cn'


def http_json(url):
    r = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', '30', url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if not r.stdout:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def load_all():
    out = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            out[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}
    return out


def search_openalex_author(name, profile):
    """Find best OpenAlex author id using identity_profile to disambiguate."""
    url = f'https://api.openalex.org/authors?search={urllib.parse.quote(name)}&per-page=15&mailto={MAILTO}'
    time.sleep(0.3)
    data = http_json(url)
    if not data:
        return None, 'http-failed'
    candidates = data.get('results') or []
    if not candidates:
        return None, 'no-candidates'

    affiliations = profile.get('affiliations') or []
    inst_keywords = []
    for aff in affiliations:
        inst = aff.get('institution', '').lower()
        for tok in re.split(r'[-_/]', inst):
            if len(tok) >= 3:
                inst_keywords.append(tok)

    scored = []
    for c in candidates:
        score = 0
        # institution match
        lk = (c.get('last_known_institution') or {})
        inst_name = (lk.get('display_name') or '').lower()
        if inst_name:
            for kw in inst_keywords:
                if kw in inst_name:
                    score += 50
                    break
        # works_count baseline
        score += min(20, (c.get('works_count') or 0) // 50)
        # ORCID match
        c_orcid = (c.get('orcid') or '').lower()
        p_orcid = (profile.get('orcid') or '').lower()
        if c_orcid and p_orcid and p_orcid in c_orcid:
            score += 1000  # ORCID = decisive
        scored.append((score, c))

    scored.sort(key=lambda x: -x[0])
    if not scored or scored[0][0] < 30:
        # No confident match. If there's only 1 candidate and works_count is
        # sane, accept; else log to review
        if len(scored) == 1 and (scored[0][1].get('works_count') or 0) < 100:
            return scored[0][1].get('id', '').rsplit('/', 1)[-1], 'single-candidate'
        return None, f'ambiguous-{len(scored)}-candidates-top-score-{scored[0][0]}'
    aid = (scored[0][1].get('id') or '').rsplit('/', 1)[-1]
    return aid, f'matched-score-{scored[0][0]}'


def fetch_works(openalex_id):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f'{openalex_id}.json')
    if os.path.exists(cache_path):
        try:
            return json.load(open(cache_path))
        except json.JSONDecodeError:
            pass
    works = []
    cursor = '*'
    while cursor:
        url = (f'https://api.openalex.org/works?filter=author.id:{openalex_id}'
               f'&per-page=200&cursor={urllib.parse.quote(cursor)}'
               f'&select=id,doi,title,display_name,publication_year,type,'
               f'primary_location,authorships,locations,ids,concepts'
               f'&mailto={MAILTO}')
        time.sleep(0.3)
        d = http_json(url)
        if not d:
            break
        results = d.get('results') or []
        works.extend(results)
        cursor = (d.get('meta') or {}).get('next_cursor')
        if not results or not cursor:
            break
    with open(cache_path, 'w') as f:
        json.dump(works, f, ensure_ascii=False)
    return works


def fix_mojibake(s):
    if not s or not isinstance(s, str) or 'Ã' not in s:
        return s
    try:
        return s.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def normalize_doi(d):
    if not d: return None
    s = str(d).lower().strip()
    return re.sub(r'^https?://(dx\.)?doi\.org/', '', s) or None


def normalize_title(s):
    s = fix_mojibake(s or '').lower()
    s = re.sub(r'\$[^$]*\$', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def title_match(a, b):
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb: return False
    if na == nb: return True
    sa, sb = set(na.split()), set(nb.split())
    return sa and sb and len(sa & sb) / max(len(sa), len(sb)) >= 0.85


def get_arxiv_id(w):
    ids = w.get('ids') or {}
    aid = ids.get('arxiv') or ''
    m = re.search(r'arxiv\.org/abs/([\w./-]+)', aid)
    if m:
        return m.group(1).split('v')[0]
    for loc in (w.get('locations') or []):
        url = (loc.get('landing_page_url') or '') + ' ' + (loc.get('pdf_url') or '')
        m = re.search(r'arxiv\.org/(?:abs|pdf)/([\d.]+)', url)
        if m:
            return m.group(1).split('v')[0]
    return None


def to_pub(w, target_name):
    title = fix_mojibake(w.get('title') or w.get('display_name') or '')
    if not title:
        return None
    year = w.get('publication_year')
    doi = normalize_doi(w.get('doi'))
    oa_id = (w.get('id') or '').rsplit('/', 1)[-1]
    src = (w.get('primary_location') or {}).get('source') or {}
    venue = fix_mojibake(src.get('display_name')) if isinstance(src, dict) else None
    arxiv_id = get_arxiv_id(w)
    # Strict match to skip the target author themselves; never substring.
    import sys as _sys, os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from name_match import names_match
    coauthors = []
    for a in (w.get('authorships') or []):
        n = fix_mojibake((a.get('author') or {}).get('display_name') or '')
        if names_match(target_name, n):
            continue
        coauthors.append(n)
    pub = {
        'id': arxiv_id or (f'doi:{doi}' if doi else f'openalex:{oa_id}'),
        'title': title,
        'year': year,
        'coauthors': coauthors,
        'sources': ['openalex'],
        'openalex_id': oa_id,
    }
    if doi:
        pub['doi'] = doi
    if venue and (w.get('type') or '') in {
        'journal-article', 'article', 'proceedings-article', 'book-chapter', 'book',
    }:
        pub['journal'] = venue
    if not arxiv_id:
        pub['no_arxiv'] = True
    return pub


def slugify_coauthor(name, all_people, profile):
    """Strict token-set match to a slug; otherwise return the raw name."""
    import sys as _sys, os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from name_match import slug_for_author
    s = slug_for_author(name, all_people)
    return s if s else name


def merge_pubs(arxiv_pubs, oa_accepted):
    by_doi, by_arxiv = {}, {}
    out = []
    for p in arxiv_pubs:
        p = deepcopy(p)
        srcs = p.get('sources') or ['arxiv']
        if 'arxiv' not in srcs:
            srcs.append('arxiv')
        p['sources'] = srcs
        out.append(p)
        if p.get('doi'):
            by_doi[normalize_doi(p['doi'])] = p
        by_arxiv[(p.get('id') or '').split('v')[0]] = p

    for op in oa_accepted:
        merged = None
        if op.get('doi') and normalize_doi(op['doi']) in by_doi:
            merged = by_doi[normalize_doi(op['doi'])]
        else:
            aid_part = op['id'].split(':', 1)
            if aid_part[0] not in ('doi', 'openalex') and op['id'] in by_arxiv:
                merged = by_arxiv[op['id']]
        if not merged:
            for ap in out:
                if title_match(ap.get('title'), op.get('title')):
                    merged = ap
                    break
        if merged:
            for k in ('doi', 'journal', 'openalex_id'):
                if op.get(k) and not merged.get(k):
                    merged[k] = op[k]
            srcs = set(merged.get('sources') or [])
            srcs.update(op.get('sources') or [])
            merged['sources'] = sorted(srcs)
        else:
            out.append(deepcopy(op))
    return out


def render_pubs(pubs, all_people, profile):
    def squote(s): return "'" + str(s).replace("'", "''") + "'"
    def coa(c):
        s = str(c)
        if re.fullmatch(r'[a-z][a-z0-9_-]*', s):
            return s
        slug = slugify_coauthor(s, all_people, profile)
        if re.fullmatch(r'[a-z][a-z0-9_-]*', slug):
            return slug
        return squote(s)
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
            lines.append(f'    coauthors: [{", ".join(coa(c) for c in cas)}]')
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
    def squote(s): return "'" + str(s).replace("'", "''") + "'"
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
    for anchor in ['external_ids:', 'links:', 'sources:']:
        m = re.search(rf'^{anchor}', text, re.MULTILINE)
        if m:
            return text[:m.start()] + new_block + '\n' + text[m.start():]
    return text.rstrip() + '\n' + new_block + '\n'


def write_review(slug, items):
    save_candidates(os.path.join(REVIEW_DIR, f'{slug}.yaml'), slug, items)


def process(slug, person, all_people, write=False):
    name_en = (person.get('name') or {}).get('en') or ''
    profile = person.get('identity_profile') or {}
    existing_reviews = load_review(os.path.join(REVIEW_DIR, f'{slug}.yaml')).get('candidates', [])

    # Resolve OpenAlex id
    aid = profile.get('openalex_id') or (person.get('external_ids') or {}).get('openalex')
    resolution_note = 'from-yaml' if aid else None
    if not aid:
        aid, resolution_note = search_openalex_author(name_en, profile)
    if not aid:
        return {'slug': slug, 'skipped': f'no openalex id ({resolution_note})'}

    works = fetch_works(aid)
    arxiv_pubs = person.get('publications') or []

    accepted = []
    rejected = []
    review = []
    for w in works:
        pub = to_pub(w, name_en)
        if not pub:
            continue
        if prior := blocked_review(pub, existing_reviews):
            rejected.append({'id': pub['id'], 'title': pub.get('title'),
                             'evidence': f"explicit review: {prior['review_status']}"})
            continue
        # Build a paper representation that disambiguator can score
        paper = {
            'authorships': w.get('authorships') or [],
            'publication_year': pub.get('year'),
            'title': pub.get('title'),
            'primary_location': w.get('primary_location'),
            'primary_category': pub.get('primary_category'),
        }
        decision, score, evidence = score_candidate(paper, profile, name_en, all_people)
        if decision == 'accept':
            accepted.append(pub)
        elif decision == 'review':
            review.append({
                'id': pub['id'], 'title': pub.get('title'),
                'year': pub.get('year'), 'score': score,
                'evidence': evidence, 'doi': pub.get('doi'),
                'venue': pub.get('journal'),
            })
        else:
            rejected.append({
                'id': pub['id'], 'title': pub.get('title'),
                'score': score, 'evidence': evidence,
            })

    if write:
        write_review(slug, review)
    merged = merge_pubs(arxiv_pubs, accepted)
    merged.sort(key=lambda p: -(p.get('year') or 0))
    pub_count = sum(1 for p in merged if p.get('journal') or p.get('doi'))
    pre_count = len(merged) - pub_count

    res = {
        'slug': slug,
        'openalex_id': aid,
        'oa_works': len(works),
        'arxiv_before': len(arxiv_pubs),
        'oa_accepted': len(accepted),
        'oa_review': len(review),
        'oa_rejected': len(rejected),
        'final': len(merged),
        'published': pub_count,
        'preprint': pre_count,
    }
    if write and (accepted or any(p.get('sources') == ['arxiv'] for p in merged) != any(p.get('sources') == ['arxiv'] for p in arxiv_pubs)):
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        text = replace_block(text, 'publications', render_pubs(merged, all_people, profile))
        activity = dict(person.get('activity') or {})
        activity['total_papers'] = len(merged)
        activity['published_count'] = pub_count
        activity['preprint_only_count'] = pre_count
        # confidence flag
        if review:
            activity['confidence'] = f'has-{len(review)}-review-pending'
        else:
            activity.pop('confidence', None)
        text = replace_block(text, 'activity', render_activity(activity))
        with open(path, 'w') as f:
            f.write(text)
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slug', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    all_people = load_all()
    targets = list(all_people.keys()) if args.all else args.slug
    if not targets:
        print('Specify slug or --all', file=sys.stderr)
        sys.exit(1)
    summary = []
    for i, slug in enumerate(targets):
        person = all_people.get(slug)
        if not person:
            continue
        print(f'[{i+1}/{len(targets)}] {slug} ...', file=sys.stderr)
        try:
            r = process(slug, person, all_people, write=args.write)
        except Exception as e:
            print(f'  error: {e}', file=sys.stderr)
            continue
        if 'skipped' in r:
            print(f'  skipped: {r["skipped"]}', file=sys.stderr)
            continue
        print(f"  oa works={r['oa_works']}: accept {r['oa_accepted']} / review "
              f"{r['oa_review']} / reject {r['oa_rejected']}; final {r['final']} "
              f"({r['published']} pub / {r['preprint']} pre)", file=sys.stderr)
        summary.append(r)
    print('\n=== SUMMARY ===')
    print(f"{'slug':<25} {'final':>6} {'pub':>5} {'pre':>5} {'review':>7}")
    for s in summary:
        print(f"{s['slug']:<25} {s['final']:>6} {s['published']:>5} {s['preprint']:>5} {s['oa_review']:>7}")


if __name__ == '__main__':
    main()
