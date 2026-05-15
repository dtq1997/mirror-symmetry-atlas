"""Unified ground-truth author list lookup.

Given a publication record (any combination of arxiv id, DOI, OpenAlex id),
return the authoritative list of author names from the most reliable source.
Cached on disk under .cache/msa/papers/_*_authors_cache/ by default.

This is the SSOT for "who actually wrote this paper". Every cleanup script
that decides whether a yaml's pub assignment is correct should consult this
module — never substring matching, never the yaml's own coauthor field.
"""
import json
import os
import re
import subprocess
import time
import xml.etree.ElementTree as ET

from cache_paths import cache_path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARXIV_CACHE = cache_path('_arxiv_authors_cache')
CROSSREF_CACHE = cache_path('_crossref_authors_cache')
OPENALEX_CACHE = cache_path('_openalex_authors_cache')
NS = {'a': 'http://www.w3.org/2005/Atom'}

POLITE_EMAIL = 'mirror-symmetry-atlas@local'

for d in (ARXIV_CACHE, CROSSREF_CACHE, OPENALEX_CACHE):
    os.makedirs(d, exist_ok=True)


def _curl(url, max_time=30):
    r = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', str(max_time),
                        '-A', f'mirror-symmetry-atlas (mailto:{POLITE_EMAIL})', url],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout


# =================== arxiv ===================

def _arxiv_archive_for_category(primary_category):
    """Map modern category like 'math.AG' to legacy archive prefix used in
    pre-2007 arXiv ids. Used to recover authors of 7-digit legacy ids."""
    if not primary_category:
        return None
    pc = primary_category.lower()
    if pc.startswith('math.ag') or pc.startswith('math-ag'):
        return ['alg-geom', 'math']
    if pc.startswith('math-ph') or pc.startswith('mathph'):
        return ['math-ph', 'math', 'hep-th']
    if pc.startswith('math.dg') or pc.startswith('math-dg'):
        return ['dg-ga', 'math']
    if pc.startswith('math.qa'):
        return ['q-alg', 'math']
    if pc.startswith('math.'):
        return ['math']
    if pc.startswith('hep-th') or pc.startswith('hept'):
        return ['hep-th']
    if pc.startswith('hep-ph'):
        return ['hep-ph']
    if pc.startswith('hep-lat'):
        return ['hep-lat']
    if pc.startswith('gr-qc'):
        return ['gr-qc']
    if pc.startswith('cond-mat'):
        return ['cond-mat']
    return None


def _arxiv_parse_authors(xml_text):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None
    entries = root.findall('a:entry', NS)
    if not entries:
        return None
    entry = entries[0]
    aid = entry.find('a:id', NS)
    if aid is not None and '/errors' in (aid.text or ''):
        return None
    return [a.find('a:name', NS).text for a in entry.findall('a:author', NS)
            if a.find('a:name', NS) is not None]


def fetch_arxiv_authors(arxiv_id, primary_category=None, delay=1,
                        owner_hint=None):
    """Returns list of author names or None.

    For 7-digit legacy ids, the same number can resolve to DIFFERENT papers
    under different archive prefixes (e.g. `hep-th/9602001` is by Jose Gaite,
    `dg-ga/9602001` is by Anton Alekseev). We try ALL plausible archives and,
    if `owner_hint` is given, return the variant whose author list contains
    a compatible match for the hint. Without a hint we take the first hit
    (legacy behavior, may be wrong for ambiguous ids).
    """
    arxiv_id = arxiv_id.split('v')[0]
    safe = arxiv_id.replace('/', '_')
    cache = os.path.join(ARXIV_CACHE, f'{safe}.json')
    miss_cache = cache + '.miss'
    if os.path.exists(cache):
        try:
            return json.load(open(cache))
        except json.JSONDecodeError:
            pass
    if os.path.exists(miss_cache):
        return None  # known-bad id, don't retry
    candidates = [arxiv_id]
    is_legacy = bool(re.match(r'^\d{7}$', arxiv_id))
    if is_legacy:
        prefixes = _arxiv_archive_for_category(primary_category) or []
        for arch in prefixes + ['hep-th', 'math', 'alg-geom', 'dg-ga',
                                'math-ph', 'q-alg', 'gr-qc']:
            qid = f'{arch}/{arxiv_id}'
            if qid not in candidates:
                candidates.append(qid)

    hits = []  # (qid, authors)
    for qid in candidates:
        time.sleep(delay)
        url = f'https://export.arxiv.org/api/query?id_list={qid}&max_results=1'
        out = _curl(url, max_time=20)
        authors = _arxiv_parse_authors(out)
        if authors:
            hits.append((qid, authors))
            # For non-legacy (modern arxiv id), one hit is enough — they're
            # globally unique.
            if not is_legacy:
                break

    if not hits:
        open(miss_cache, 'w').close()
        return None

    chosen = None
    if owner_hint and len(hits) > 1:
        # Import lazily to avoid circular at module load.
        try:
            from name_match import names_compatible
            for qid, auths in hits:
                if any(names_compatible(owner_hint, a) for a in auths):
                    chosen = auths
                    break
        except Exception:
            pass
    if chosen is None:
        chosen = hits[0][1]
    with open(cache, 'w') as f:
        json.dump(chosen, f, ensure_ascii=False)
    return chosen


# =================== crossref ===================

def fetch_crossref_authors(doi, delay=0.3):
    if not doi:
        return None
    doi = doi.lower().strip()
    if doi.startswith('10.48550/arxiv.'):
        return None
    safe = re.sub(r'[^a-z0-9]', '_', doi)
    cache = os.path.join(CROSSREF_CACHE, f'{safe}.json')
    miss_cache = cache + '.miss'
    if os.path.exists(cache):
        try:
            return json.load(open(cache))
        except json.JSONDecodeError:
            pass
    if os.path.exists(miss_cache):
        return None
    time.sleep(delay)
    url = f'https://api.crossref.org/works/{doi}?mailto={POLITE_EMAIL}'
    out = _curl(url, max_time=15)
    if not out:
        open(miss_cache, 'w').close()
        return None
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        open(miss_cache, 'w').close()
        return None
    if data.get('status') != 'ok':
        open(miss_cache, 'w').close()
        return None
    msg = data.get('message') or {}
    authors = []
    for a in (msg.get('author') or []):
        given = a.get('given') or ''
        family = a.get('family') or ''
        n = (given + ' ' + family).strip()
        if not n:
            n = a.get('name') or ''
        if n:
            authors.append(n)
    if authors:
        with open(cache, 'w') as f:
            json.dump(authors, f, ensure_ascii=False)
        return authors
    open(miss_cache, 'w').close()
    return None


# =================== openalex ===================

def fetch_openalex_authors(work_id_or_doi, delay=0.3):
    if not work_id_or_doi:
        return None
    key = str(work_id_or_doi).strip()
    safe = re.sub(r'[^a-zA-Z0-9]', '_', key)
    cache = os.path.join(OPENALEX_CACHE, f'{safe}.json')
    miss_cache = cache + '.miss'
    if os.path.exists(cache):
        try:
            return json.load(open(cache))
        except json.JSONDecodeError:
            pass
    if os.path.exists(miss_cache):
        return None
    if key.startswith('W'):
        url = f'https://api.openalex.org/works/{key}?mailto={POLITE_EMAIL}'
    elif '/' in key or key.startswith('10.'):
        url = f'https://api.openalex.org/works/doi:{key}?mailto={POLITE_EMAIL}'
    else:
        return None
    time.sleep(delay)
    out = _curl(url, max_time=15)
    if not out:
        open(miss_cache, 'w').close()
        return None
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        open(miss_cache, 'w').close()
        return None
    auths = []
    for a in (data.get('authorships') or []):
        n = (a.get('author') or {}).get('display_name')
        if n:
            auths.append(n)
    if auths:
        with open(cache, 'w') as f:
            json.dump(auths, f, ensure_ascii=False)
        return auths
    open(miss_cache, 'w').close()
    return None


# =================== unified ===================

def get_actual_authors(pub, owner_hint=None):
    """Return ground-truth author list for `pub` (yaml entry) or None.

    Tries arxiv > Crossref > OpenAlex. arxiv is most reliable for math papers.
    Returns None when no source can resolve.
    """
    pid = (pub.get('id') or '').strip()
    pcat = pub.get('primary_category')
    doi = (pub.get('doi') or '').strip()
    oa = (pub.get('openalex_id') or '').strip()

    # 1) arxiv id (modern or legacy)
    arxiv_id = None
    if pid and not pid.startswith(('doi:', 'openalex:', 'cr:')):
        aid = pid.split('v')[0]
        if re.match(r'^\d{4}\.\d{4,5}$|^\d{7}$|^[a-z-]+/\d{7}$', aid):
            arxiv_id = aid
    if arxiv_id:
        a = fetch_arxiv_authors(arxiv_id, primary_category=pcat,
                                owner_hint=owner_hint)
        if a:
            return a, 'arxiv'

    # 2) DOI via Crossref
    if doi:
        a = fetch_crossref_authors(doi)
        if a:
            return a, 'crossref'

    # 3) OpenAlex (work id or doi)
    if oa:
        a = fetch_openalex_authors(oa)
        if a:
            return a, 'openalex'
    if doi:
        a = fetch_openalex_authors(doi)
        if a:
            return a, 'openalex'

    return None, None
