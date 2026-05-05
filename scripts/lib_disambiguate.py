"""Author disambiguation utilities.

Multi-signal scoring for arXiv candidate papers against a person YAML profile.
Used by fetch-arxiv-by-author.py and audit-publications.py.

Signals (cumulative score):
  +5  primary_category in math.* / math-ph / nlin.SI / hep-th
  +10 per matched known coauthor (cap 3)
  +3  per matched research_area keyword in title
  +5  submitter name (arxiv "From:" field) matches person name
  +5  affiliation extracted from tex matches institution in career_timeline
  +5  email domain extracted from tex matches recorded email domain

Hard reject (score=0):
  primary_category starts with cs./q-bio/q-fin/stat (non-math sibling fields)
  no name part overlap with the actual author list

Threshold guidance:
  >= 15  : confident match
  10-14  : likely match (review queue)
  5-9    : weak (needs manual review)
  < 5    : reject
"""

import os
import re
import time
import subprocess
import urllib.parse
import xml.etree.ElementTree as ET
import yaml

NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

MATH_PRIMARY_PREFIXES = ('math.', 'math-ph', 'nlin.SI', 'hep-th')
NON_MATH_PRIMARY_PREFIXES = ('cs.', 'q-bio', 'q-fin', 'stat.', 'eess.', 'econ.')

PEOPLE_DIR = 'data/people'


def load_person(slug, people_dir=PEOPLE_DIR):
    path = os.path.join(people_dir, f'{slug}.yaml')
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return yaml.safe_load(f) or {}


def load_all_people(people_dir=PEOPLE_DIR):
    people = {}
    for f in sorted(os.listdir(people_dir)):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        with open(os.path.join(people_dir, f)) as fh:
            people[slug] = yaml.safe_load(fh) or {}
    return people


def collect_known_collaborator_names(person_data, all_people=None):
    """Resolve a person's known collaborator slugs to English name strings.
    Falls back to advisor / students slugs and raw names in key_collaborators
    when slug isn't in the people index.
    """
    names = set()
    if all_people is None:
        all_people = load_all_people()

    def resolve(slug_or_name):
        if not isinstance(slug_or_name, str) or not slug_or_name:
            return
        if slug_or_name in all_people:
            en = (all_people[slug_or_name].get('name') or {}).get('en', '')
            if en:
                names.add(en)
        else:
            cleaned = normalize_name(slug_or_name)
            if cleaned and ' ' in cleaned:
                names.add(cleaned)

    for kc in (person_data.get('key_collaborators') or []):
        resolve(kc.get('person'))
    if person_data.get('advisor'):
        resolve(person_data['advisor'])
    for s in (person_data.get('students') or []):
        resolve(s)
    for m in (person_data.get('mentors') or []):
        resolve(m)
    # Pull from existing publications coauthors
    for pub in (person_data.get('publications') or []):
        for ca in (pub.get('coauthors') or []):
            resolve(ca)
    return names


def collect_known_institutions(person_data, all_institutions=None):
    """Get institution name aliases for matching against tex affiliations."""
    insts = set()
    for ev in (person_data.get('career_timeline') or []):
        i = ev.get('institution')
        if i:
            insts.add(i)
    return insts


def fix_mojibake(s):
    """Reverse the common arXiv double-encoding: bytes that were UTF-8 got
    decoded as Latin-1 then re-encoded as UTF-8. We detect by looking for
    typical artifacts (Ã©, Ã¨, Ã, etc.) and try a round-trip.
    Falls back to the original string if the round-trip fails."""
    if not s or 'Ã' not in s:
        return s
    try:
        return s.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return s


def normalize_name(s):
    """Strip parenthesized content and non-ascii (e.g. Chinese annotation) to leave the latin name."""
    if not s:
        return ''
    s = re.sub(r'\([^)]*\)', '', s)
    s = re.sub(r'[^\x20-\x7e]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def name_parts_match(target_name, candidate_name):
    """Return True if every word in target_name (lowercased, normalized) appears as substring in candidate."""
    target_name = normalize_name(target_name)
    candidate_name = normalize_name(candidate_name)
    parts = target_name.lower().split()
    if not parts:
        return False
    cl = candidate_name.lower()
    return all(p in cl for p in parts if len(p) > 1)


def primary_category_signal(primary_cat):
    if not primary_cat:
        return 0, None
    if any(primary_cat.startswith(p) for p in NON_MATH_PRIMARY_PREFIXES):
        return -1, 'non-math-rejected'
    if any(primary_cat.startswith(p) for p in MATH_PRIMARY_PREFIXES):
        return 5, 'math-cat'
    return 0, 'other-cat'


def coauthor_signal(authors, known_collaborator_names):
    matched = []
    for name in known_collaborator_names:
        for a in authors:
            if name_parts_match(name, a):
                matched.append(name)
                break
    return matched


def keyword_signal(title, research_areas):
    """Match research-area slugs (kebab-case) against title."""
    title_l = title.lower()
    matched = []
    for slug in (research_areas or []):
        kw = slug.replace('-', ' ').lower()
        roots = [w[:6] for w in kw.split() if len(w) > 3]
        if roots and all(r in title_l for r in roots):
            matched.append(slug)
    return matched


def fetch_arxiv_submitter(arxiv_id, cache_dir='data/papers/_arxiv_cache', delay=4):
    """Fetch the abstract HTML page and extract the 'From: <name>' submitter.
    Returns the submitter name string or None.
    Caches HTML on disk to avoid re-hitting arxiv.
    """
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f'{arxiv_id}.html')
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 1000:
        with open(cache_path, 'r', errors='ignore') as f:
            html = f.read()
    else:
        time.sleep(delay)
        url = f'https://arxiv.org/abs/{arxiv_id}'
        result = subprocess.run(
            ['curl', '-s', '--noproxy', '*', '--max-time', '30', url],
            capture_output=True, text=True, encoding='utf-8', errors='replace'
        )
        html = result.stdout or ''
        if len(html) > 1000:
            with open(cache_path, 'w') as f:
                f.write(html)
    m = re.search(r'From:\s*([^<\[\n]+?)\s*\[', html)
    if m:
        return m.group(1).strip()
    return None


def submitter_signal(submitter, target_name):
    if not submitter:
        return False
    return name_parts_match(target_name, submitter) or name_parts_match(submitter, target_name)


def disambiguate(person_data, candidate_paper, all_people=None,
                 use_submitter=False, target_name=None):
    """Score a candidate paper against a person profile.

    candidate_paper: dict with keys: id, title, authors (list of str), primary_category
    Returns (score, signals_dict)
    """
    if all_people is None:
        all_people = load_all_people()
    if target_name is None:
        target_name = (person_data.get('name') or {}).get('en', '')

    signals = {}
    score = 0

    # Hard sanity: target name must appear as one of the listed authors
    if target_name and not any(name_parts_match(target_name, a)
                                for a in candidate_paper.get('authors', [])):
        return 0, {'rejected': 'target-not-in-authors'}

    cat_score, cat_label = primary_category_signal(candidate_paper.get('primary_category', ''))
    if cat_score < 0:
        return 0, {'rejected': cat_label}
    if cat_score > 0:
        score += cat_score
        signals['math_category'] = cat_label

    known_names = collect_known_collaborator_names(person_data, all_people)
    matched_co = coauthor_signal(candidate_paper.get('authors', []), known_names)
    if matched_co:
        delta = 10 * min(3, len(matched_co))
        score += delta
        signals['known_coauthors'] = matched_co

    matched_kw = keyword_signal(candidate_paper.get('title', ''),
                                 person_data.get('research_areas') or [])
    if matched_kw:
        score += 3 * len(matched_kw)
        signals['keywords'] = matched_kw

    if use_submitter:
        sub = fetch_arxiv_submitter(candidate_paper['id'])
        if sub and submitter_signal(sub, target_name):
            score += 5
            signals['submitter_match'] = sub
        elif sub:
            signals['submitter_other'] = sub

    return score, signals


def fetch_candidates_for_person(target_name, max_results=200, math_only=True, delay=4):
    """Query arxiv for an author, optionally restricted to math/math-ph categories."""
    query = f'au:"{target_name}"'
    if math_only:
        cats = ['math.AG', 'math.QA', 'math.DG', 'math.SG', 'math.RT', 'math.GT',
                'math.AT', 'math.AC', 'math.CO', 'math.RA', 'math.NT', 'math.CA',
                'math.DS', 'math.AP', 'math.PR', 'math.OA', 'math.GM', 'math.GN',
                'math-ph', 'nlin.SI', 'nlin.CD', 'hep-th']
        cat_q = ' OR '.join(f'cat:{c}' for c in cats)
        query = f'{query} AND ({cat_q})'
    url = (f'https://export.arxiv.org/api/query?'
           f'search_query={urllib.parse.quote(query)}&max_results={max_results}'
           f'&sortBy=submittedDate&sortOrder=descending')
    time.sleep(delay)
    res = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', '40', url],
                         capture_output=True, text=True, encoding='utf-8', errors='replace')
    if not res.stdout or 'Rate exceeded' in res.stdout:
        return []
    try:
        tree = ET.fromstring(res.stdout)
    except ET.ParseError:
        return []
    out = []
    for entry in tree.findall('a:entry', NS):
        aid = entry.find('a:id', NS).text.split('/')[-1].split('v')[0]
        title = entry.find('a:title', NS).text.strip().replace('\n', ' ').replace('  ', ' ')
        year = int(entry.find('a:published', NS).text[:4])
        authors = [a.find('a:name', NS).text for a in entry.findall('a:author', NS)]
        primary = entry.find('arxiv:primary_category', NS)
        primary_cat = primary.get('term') if primary is not None else ''
        # arXiv-specific fields: journal_ref, doi (only when author filled them in)
        jref = entry.find('arxiv:journal_ref', NS)
        doi = entry.find('arxiv:doi', NS)
        out.append({
            'id': aid,
            'title': fix_mojibake(title),
            'year': year,
            'authors': [fix_mojibake(a) for a in authors],
            'primary_category': primary_cat,
            'journal_ref': fix_mojibake(jref.text.strip()) if jref is not None and jref.text else None,
            'doi': doi.text.strip() if doi is not None and doi.text else None,
        })
    return out
