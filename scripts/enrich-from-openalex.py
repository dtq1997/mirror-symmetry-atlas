#!/usr/bin/env python3
"""Enrich publications using OpenAlex as the authoritative publications source.

OpenAlex aggregates Crossref, MAG, DataCite etc. and gives us papers that
never appeared on arXiv (pure-journal submissions, conference proceedings, books).

Strategy:
1. Resolve each person to their OpenAlex author id.
   - Use existing external_ids.openalex if present.
   - Otherwise search by name + verify by works_count + last_known_institution.
   - Stash the resolved id back to YAML.
2. Pull all works for that author (paginated, 200/page).
3. Filter to research papers (skip "other", "report" without doi).
4. Merge with existing arXiv-derived publications:
   - Match by DOI first; then by normalized-title fuzzy match.
   - If matched: enrich existing entry with OpenAlex venue/doi/openalex_id;
     mark sources += ["openalex"]. arXiv id stays as primary id.
   - If unmatched: new entry. id = "doi:..." or "openalex:W...". Mark
     sources = ["openalex"], no_arxiv = true.
5. Recompute activity.total_papers / published_count / preprint_only_count.

Usage:
  python3 scripts/enrich-from-openalex.py <slug> [--write]
  python3 scripts/enrich-from-openalex.py --all --write
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

PEOPLE_DIR = 'data/people'
CACHE_DIR = 'data/papers/_openalex_cache'
MAILTO = 'qiantang@tsinghua.edu.cn'


def load_all():
    out = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            out[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}
    return out


def http_get_json(url, timeout=25):
    r = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', str(timeout), url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    if not r.stdout:
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


def search_author(name, hint_institution=None):
    """Search OpenAlex authors by name, return best match dict or None."""
    url = (f'https://api.openalex.org/authors?search={urllib.parse.quote(name)}'
           f'&per-page=10&mailto={MAILTO}')
    time.sleep(0.3)
    data = http_get_json(url)
    if not data:
        return None
    results = data.get('results') or []
    if not results:
        return None
    # Score: works_count + institution match boost
    def score(a):
        s = a.get('works_count') or 0
        if hint_institution:
            inst = (a.get('last_known_institution') or {}).get('display_name') or ''
            if hint_institution.lower() in inst.lower():
                s += 100
        return s
    return max(results, key=score)


def resolve_openalex_id(slug, person):
    """Return (openalex_id, source) where source ∈ {'yaml','search','fail'}."""
    ext = (person.get('external_ids') or {})
    existing = ext.get('openalex')
    if isinstance(existing, str) and existing.startswith('A'):
        return existing, 'yaml'
    name_en = (person.get('name') or {}).get('en') or ''
    if not name_en:
        return None, 'fail'
    # institution hint: latest position
    hint = None
    for ev in (person.get('career_timeline') or []):
        if ev.get('type') == 'position':
            hint = ev.get('institution')
    found = search_author(name_en, hint_institution=hint)
    if not found:
        return None, 'fail'
    aid = (found.get('id') or '').rsplit('/', 1)[-1]
    return aid if aid.startswith('A') else None, 'search'


def fetch_all_works(openalex_id, cache=True):
    """Paginate through all OpenAlex works for an author. Includes the
    `concepts` field so downstream filters can detect homonym contamination."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f'{openalex_id}.json')
    if cache and os.path.exists(cache_path):
        try:
            return json.load(open(cache_path))
        except json.JSONDecodeError:
            pass

    all_works = []
    cursor = '*'
    while cursor:
        url = (f'https://api.openalex.org/works?filter=author.id:{openalex_id}'
               f'&per-page=200&cursor={urllib.parse.quote(cursor)}'
               f'&select=id,doi,title,display_name,publication_year,type,'
               f'primary_location,authorships,locations,ids,concepts'
               f'&mailto={MAILTO}')
        time.sleep(0.3)
        d = http_get_json(url)
        if not d:
            break
        results = d.get('results') or []
        all_works.extend(results)
        cursor = (d.get('meta') or {}).get('next_cursor')
        if not results or not cursor:
            break

    with open(cache_path, 'w') as f:
        json.dump(all_works, f, ensure_ascii=False)
    return all_works


def fix_mojibake(s):
    if not s or not isinstance(s, str) or 'Ã' not in s:
        return s
    try:
        return s.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def normalize_title(s):
    s = fix_mojibake(s or '').lower()
    s = re.sub(r'\$[^$]*\$', ' ', s)
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def title_matches(a, b):
    na, nb = normalize_title(a), normalize_title(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    sa, sb = set(na.split()), set(nb.split())
    if not sa or not sb:
        return False
    return len(sa & sb) / max(len(sa), len(sb)) >= 0.85


def normalize_doi(d):
    if not d:
        return None
    s = str(d).lower().strip()
    s = re.sub(r'^https?://(dx\.)?doi\.org/', '', s)
    return s or None


def get_arxiv_id_from_work(w):
    """OpenAlex sometimes lists an arXiv id under ids or as a 'preprint' locator."""
    ids = w.get('ids') or {}
    pmid = ids.get('arxiv') or ''
    if pmid:
        # form: https://arxiv.org/abs/XXXX.YYYYY
        m = re.search(r'arxiv\.org/abs/([\w./-]+)', pmid)
        if m:
            return m.group(1).split('v')[0]
    # Look in primary_location source / locations
    for loc in (w.get('locations') or []):
        url = (loc.get('landing_page_url') or '') + ' ' + (loc.get('pdf_url') or '')
        m = re.search(r'arxiv\.org/(?:abs|pdf)/([\d.]+)', url)
        if m:
            return m.group(1).split('v')[0]
    return None


RESEARCH_TYPES = {
    'journal-article', 'article', 'proceedings-article', 'book-chapter',
    'book', 'monograph', 'reference-entry', 'preprint', 'posted-content',
    'dissertation', 'edited-book',
}

# When a Yes/No is unclear, what fields tell us the work is actually math?
MATH_VENUE_HINTS = (
    'math', 'invent', 'annal', 'topology', 'geometry', 'algebra', 'compositio',
    'asterisque', 'memoir', 'arxiv', 'duke math', 'ann. of math', 'ann sci',
    'commun', 'theor', 'jhep', 'nuclear phys b', 'symplectic', 'differential',
    'european math', 'forum math', 'transactions of the amer', 'crelle',
    'journal de math', 'nagoya math', 'bulletin of the amer', 'manuscripta',
    'asymptotic', 'selecta', 'progress in math', 'lecture notes in math',
    'compositio math', 'inventiones', 'duke', 'algebraic & geometric topology',
)
NON_MATH_VENUE_HINTS = (
    'chem', 'biology', 'medical', 'medicine', 'engineering', 'biomed',
    'cancer', 'clinical', 'cell', 'plant', 'molecul', 'cardiol', 'tissue',
    'oncolog', 'pathol', 'food', 'agric',
    # CS / data
    'sigmod', 'icde', 'sigir', 'kdd', 'aaai', 'neurips', 'cvpr', 'iccv', 'eccv',
    'acl', 'emnlp', 'naacl', 'database', 'data engineering', 'transactions on knowledge',
    'computational complexity', 'soft computing', 'neural network', 'pattern recogn',
    'information sciences', 'expert systems', 'knowledge based',
    # Condensed matter / device physics (Si Li type)
    'condensed matter', 'phys. rev. b', 'physical review b', 'applied physics',
    'solid state', 'nanotechnology', 'nano letters', 'photonics',
    'semiconductor', 'metallurg', 'optical materials',
    # Statistics applied not pure
    'biometrics', 'biostatistics',
)


def is_math_work(w):
    """Heuristic: tell whether a work is in mathematics.
    Conservative: when in doubt, REJECT. We'd rather miss a few real math
    papers than absorb hundreds of homonym contamination."""
    src = (w.get('primary_location') or {}).get('source') or {}
    venue = (src.get('display_name') or '').lower()
    if any(h in venue for h in NON_MATH_VENUE_HINTS):
        return False
    venue_is_math = any(h in venue for h in MATH_VENUE_HINTS)

    # Check OpenAlex concepts
    concepts = w.get('concepts') or []
    has_math_concept = False
    has_nonmath_concept = False
    for c in concepts[:5]:
        name = (c.get('display_name') or '').lower()
        score = c.get('score') or 0
        if score < 0.3:
            continue
        if name in ('mathematics', 'pure mathematics', 'algebra', 'topology',
                    'geometry', 'algebraic geometry', 'differential geometry',
                    'mathematical physics', 'symplectic geometry',
                    'mathematical analysis', 'theoretical physics',
                    'particle physics', 'quantum mechanics',
                    'number theory', 'representation theory'):
            has_math_concept = True
        if name in ('chemistry', 'biology', 'medicine', 'biochemistry',
                    'cancer research', 'genetics', 'engineering',
                    'materials science', 'computer science', 'artificial intelligence',
                    'machine learning', 'data mining', 'database',
                    'condensed matter physics', 'astronomy', 'food science',
                    'agriculture', 'economics', 'finance', 'psychology'):
            has_nonmath_concept = True

    if has_nonmath_concept and not has_math_concept:
        return False
    if venue_is_math:
        return True
    if has_math_concept:
        return True
    # arXiv preprints with no other signal: only accept if title contains
    # math keywords. Otherwise reject (default safe).
    if (w.get('type') or '') in ('preprint', 'posted-content'):
        title = (w.get('title') or w.get('display_name') or '').lower()
        if any(kw in title for kw in [
            'frobenius', 'stokes', 'painlev', 'mirror', 'gromov', 'dubrovin',
            'isomonodrom', 'hierarchy', 'cohomol', 'moduli', 'calabi', 'yau',
            'orbifold', 'hodge', 'symplect', 'lagrang', 'fukaya',
            'integrabl', 'virasoro', 'tau function', 'kdv', 'kp ', 'bkp',
            'hurwitz', 'representation', 'lie algebra', 'lie group',
            'manifold', 'geometric', 'algebraic', 'number theor',
            'differential equ', 'variational', 'topological',
        ]):
            return True
        return False
    return False


def work_to_publication(w, target_name, strict_math=False):
    """Convert OpenAlex work to our Publication shape, or None if not research.

    If strict_math=True (used when total works > 200, suggesting profile
    contamination by homonyms), additionally require is_math_work(w)."""
    wtype = w.get('type') or ''
    if wtype not in RESEARCH_TYPES:
        return None
    if strict_math and not is_math_work(w):
        return None
    title = fix_mojibake(w.get('title') or w.get('display_name') or '')
    if not title:
        return None
    year = w.get('publication_year')
    doi = normalize_doi(w.get('doi'))
    openalex_id = (w.get('id') or '').rsplit('/', 1)[-1]
    src = (w.get('primary_location') or {}).get('source') or {}
    venue = fix_mojibake(src.get('display_name')) if isinstance(src, dict) else None
    is_published_venue = bool(doi) and venue and wtype in {
        'journal-article', 'article', 'proceedings-article', 'book-chapter', 'book',
    }
    arxiv_id = get_arxiv_id_from_work(w)

    coauthors = []
    target_norm = re.sub(r'[^a-z ]', ' ', (target_name or '').lower())
    target_parts = [p for p in target_norm.split() if len(p) > 1]
    for a in (w.get('authorships') or []):
        n = fix_mojibake((a.get('author') or {}).get('display_name') or '')
        nn = re.sub(r'[^a-z ]', ' ', n.lower())
        if target_parts and all(p in nn for p in target_parts):
            continue
        coauthors.append(n)

    pub = {
        'id': arxiv_id or (f'doi:{doi}' if doi else f'openalex:{openalex_id}'),
        'title': title,
        'year': year,
        'coauthors': coauthors,
        'sources': ['openalex'],
        'openalex_id': openalex_id,
    }
    if doi:
        pub['doi'] = doi
    if venue and is_published_venue:
        pub['journal'] = venue
    if not arxiv_id:
        pub['no_arxiv'] = True
    return pub


def merge_publications(arxiv_pubs, openalex_pubs):
    """Merge by DOI first, then title fuzzy."""
    by_doi = {}
    by_arxiv = {}
    out = []
    for p in arxiv_pubs:
        p = deepcopy(p)
        p.setdefault('sources', ['arxiv'])
        if 'arxiv' not in p['sources']:
            p['sources'].append('arxiv')
        out.append(p)
        if p.get('doi'):
            by_doi[normalize_doi(p['doi'])] = p
        by_arxiv[(p.get('id') or '').split('v')[0]] = p

    for op in openalex_pubs:
        merged = None
        # 1. DOI match
        if op.get('doi') and normalize_doi(op['doi']) in by_doi:
            merged = by_doi[normalize_doi(op['doi'])]
        # 2. arXiv id match
        elif op.get('id', '').split(':')[0] not in ('doi', 'openalex'):
            if op['id'] in by_arxiv:
                merged = by_arxiv[op['id']]
        # 3. Title fuzzy match
        if not merged:
            for ap in out:
                if title_matches(ap.get('title'), op.get('title')):
                    merged = ap
                    break
        if merged:
            # Enrich
            for k in ('doi', 'journal', 'openalex_id'):
                if op.get(k) and not merged.get(k):
                    merged[k] = op[k]
            srcs = set(merged.get('sources') or [])
            srcs.update(op.get('sources') or [])
            merged['sources'] = sorted(srcs)
            # Better coauthors? prefer the longer list as it's more complete
            if op.get('coauthors') and len(op['coauthors']) > len(merged.get('coauthors') or []):
                # Keep slug-resolved coauthors from arXiv side; only fill in if empty
                if not merged.get('coauthors'):
                    merged['coauthors'] = op['coauthors']
        else:
            out.append(deepcopy(op))
    return out


def slugify_coauthor(name, all_people):
    """Best-effort: map name to slug, otherwise return cleaned name."""
    cleaned = re.sub(r'[^a-zA-Z ]', ' ', name).lower()
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    parts = cleaned.split()
    for slug, p in all_people.items():
        en = ((p.get('name') or {}).get('en') or '').lower()
        en_parts = re.sub(r'[^a-z ]', ' ', en).split()
        if en_parts and all(part in cleaned for part in en_parts if len(part) > 1):
            return slug
    return name


def render_yaml_publications(pubs, all_people):
    """Render pubs to a YAML block. Same style as enrich-publications.py."""
    def squote(s):
        return "'" + str(s).replace("'", "''") + "'"

    def coauthor_inline(c):
        s = str(c)
        if s and re.fullmatch(r'[a-z][a-z0-9_-]*', s):
            return s
        return squote(s)

    lines = ['publications:']
    for p in pubs:
        pid = p.get('id')
        if not pid:
            continue
        lines.append(f'  - id: {squote(pid)}')
        lines.append(f'    title: {squote(p.get("title") or "")}')
        if p.get('year') is not None:
            lines.append(f'    year: {p["year"]}')
        coauthors = []
        for ca in (p.get('coauthors') or []):
            slug = slugify_coauthor(ca, all_people) if isinstance(ca, str) else ca
            coauthors.append(slug)
        if coauthors:
            lines.append(f'    coauthors: [{", ".join(coauthor_inline(c) for c in coauthors)}]')
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
            lines.append(f'    no_arxiv: true')
    return '\n'.join(lines)


def render_activity(activity):
    order = ['total_papers', 'published_count', 'preprint_only_count', 'h_index',
             'mathscinet_citations', 'google_scholar_citations',
             'active_period', 'peak_period', 'phd_students',
             'academic_descendants', 'last_arxiv_paper']
    lines = ['activity:']
    keys = order + [k for k in activity if k not in order]
    for k in keys:
        v = activity.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            lines.append(f"  {k}: '{v.replace(chr(39), chr(39)*2)}'")
        else:
            lines.append(f'  {k}: {v}')
    return '\n'.join(lines)


def replace_block(text, block_name, new_block):
    pattern = re.compile(rf'(^{block_name}:.*?)(?=^[A-Za-z_][\w]*:|\Z)',
                         re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda _m: new_block + '\n', text, count=1)
    for anchor in ['sources:', 'external_ids:', 'links:', 'personal_notes:']:
        m = re.search(rf'^{anchor}', text, re.MULTILINE)
        if m:
            return text[:m.start()] + new_block + '\n' + text[m.start():]
    return text.rstrip() + '\n' + new_block + '\n'


def update_external_ids(text, openalex_id):
    """Ensure external_ids.openalex is set."""
    if not openalex_id:
        return text
    m = re.search(r'^external_ids:.*?(?=^[A-Za-z_][\w]*:|\Z)', text, re.MULTILINE | re.DOTALL)
    if not m:
        return text  # not present, skip
    block = m.group(0)
    if re.search(r'openalex:\s*\S', block):
        return text  # already set
    if block.strip() == 'external_ids: {}':
        new_block = f'external_ids:\n  openalex: {openalex_id}\n'
    else:
        new_block = block.rstrip() + f'\n  openalex: {openalex_id}\n'
    return text[:m.start()] + new_block + text[m.end():]


def process(slug, person, all_people, write=False):
    name_en = (person.get('name') or {}).get('en') or ''
    if not name_en:
        return {'slug': slug, 'skipped': 'no name'}

    aid, src = resolve_openalex_id(slug, person)
    if not aid:
        return {'slug': slug, 'skipped': 'no openalex id'}

    works = fetch_all_works(aid)
    math_works = [w for w in works if is_math_work(w)]
    if len(works) > 50 and len(math_works) / len(works) < 0.4:
        return {
            'slug': slug,
            'skipped': f'openalex profile contaminated ({len(math_works)}/{len(works)} math); needs manual external_ids.openalex'
        }
    # Sanity cap: OpenAlex math works should not exceed 5× arXiv-known publications
    # (with floor 30 for people with very few arXiv records). Otherwise the OpenAlex
    # profile likely merges multiple homonyms even though the math ratio passed.
    arxiv_count = len(person.get('publications') or [])
    cap = max(30, arxiv_count * 5)
    if len(math_works) > cap:
        return {
            'slug': slug,
            'skipped': f'openalex math-works {len(math_works)} > 5× arxiv ({arxiv_count}); profile likely homonym-merged. needs manual external_ids.openalex'
        }

    strict = len(works) > 100
    openalex_pubs = []
    for w in works:
        p = work_to_publication(w, name_en, strict_math=strict)
        if p:
            openalex_pubs.append(p)

    arxiv_pubs = person.get('publications') or []
    merged = merge_publications(arxiv_pubs, openalex_pubs)
    merged.sort(key=lambda p: -(p.get('year') or 0))

    published = sum(1 for p in merged if (p.get('journal') or p.get('doi')))
    preprint = len(merged) - published

    result = {
        'slug': slug,
        'openalex_id': aid,
        'openalex_works': len(works),
        'openalex_research_pubs': len(openalex_pubs),
        'arxiv_pubs_before': len(arxiv_pubs),
        'final_pubs': len(merged),
        'published': published,
        'preprint': preprint,
        'new_via_openalex': len(merged) - len(arxiv_pubs),
    }

    if write:
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        text = replace_block(text, 'publications', render_yaml_publications(merged, all_people))
        activity = dict(person.get('activity') or {})
        activity['total_papers'] = len(merged)
        activity['published_count'] = published
        activity['preprint_only_count'] = preprint
        text = replace_block(text, 'activity', render_activity(activity))
        if src == 'search':
            text = update_external_ids(text, aid)
        with open(path, 'w') as f:
            f.write(text)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slug', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()

    all_people = load_all()
    targets = list(all_people.keys()) if args.all else args.slug
    if not targets:
        print('Specify slug(s) or --all', file=sys.stderr)
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
        print(f"  arxiv {r['arxiv_pubs_before']} + openalex {r['openalex_research_pubs']}"
              f" -> {r['final_pubs']} (+{r['new_via_openalex']} via OA);"
              f" {r['published']} pub / {r['preprint']} preprint", file=sys.stderr)
        summary.append(r)

    print('\n=== SUMMARY ===')
    print(f"{'slug':<25} {'arxiv':>6} {'+OA':>5} {'final':>6} {'pub':>5} {'pre':>5}")
    for s in summary:
        print(f"{s['slug']:<25} {s['arxiv_pubs_before']:>6} "
              f"{s['new_via_openalex']:>5} {s['final_pubs']:>6} "
              f"{s['published']:>5} {s['preprint']:>5}")


if __name__ == '__main__':
    main()
