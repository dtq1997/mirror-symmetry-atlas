"""Source author lists for publication review (not personal identity proof).

Only a validated, exact source identifier may supply an author list. Same-name
membership still needs independent affiliation/CV evidence. Missing responses
are unresolved, never evidence that a person did not author a paper.

Old unversioned caches and permanent .miss files are retained for provenance
but are not trusted. Successful, source-bound records expire after one day.
"""
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import warnings
import xml.etree.ElementTree as ET
from urllib.parse import quote

from cache_paths import cache_path
from paper_identity import canonical_arxiv_id, canonical_doi

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARXIV_CACHE = cache_path('_arxiv_authors_cache')
CROSSREF_CACHE = cache_path('_crossref_authors_cache')
OPENALEX_CACHE = cache_path('_openalex_authors_cache')
NS = {'a': 'http://www.w3.org/2005/Atom'}
CACHE_VERSION = 2
CACHE_TTL = 24 * 60 * 60
USER_AGENT = 'mirror-symmetry-atlas/1.0 (+https://dtq1997.github.io/mirror-symmetry-atlas)'


def _curl(url, max_time=30, expected_type=None):
    """HTTP failure/timeout is unresolved; respect the user's proxy settings."""
    try:
        result = subprocess.run(
            ['curl', '--fail', '--silent', '--show-error', '--location',
             '--max-time', str(max_time), '-A', USER_AGENT,
             '--write-out', '\n%{http_code}\t%{content_type}', url],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=max_time + 5,
        )
    except subprocess.TimeoutExpired:
        warnings.warn('Source lookup timed out; unresolved, not cached', RuntimeWarning)
        return None
    except OSError:
        warnings.warn('Source lookup could not start curl; unresolved, not cached', RuntimeWarning)
        return None
    body, _, metadata = result.stdout.rpartition('\n')
    status, _, content_type = metadata.partition('\t')
    status = status if re.fullmatch(r'\d{3}', status) else 'unknown'
    if result.returncode or not status.startswith('2'):
        reason = 'HTTP error' if result.returncode == 22 else 'transport error'
        if result.returncode == 28:
            reason = 'timeout'
        warnings.warn(f'Source lookup {reason} (HTTP {status}); unresolved, not cached', RuntimeWarning)
        return None
    mime = content_type.partition(';')[0].strip().lower()
    allowed = {'xml': {'application/atom+xml', 'application/xml', 'text/xml'},
               'json': {'application/json'}}
    if expected_type and mime not in allowed[expected_type]:
        warnings.warn('Source lookup returned unexpected content type; unresolved, not cached', RuntimeWarning)
        return None
    return body if body.strip() else None


def _valid_authors(authors):
    return (isinstance(authors, list) and bool(authors)
            and all(isinstance(name, str) and bool(name.strip()) for name in authors))


def _cache_file(folder, key):
    return os.path.join(folder, 'v2', hashlib.sha256(key.encode()).hexdigest() + '.json')


def _read_cache(folder, key, source):
    try:
        with open(_cache_file(folder, key), encoding='utf-8') as handle:
            record = json.load(handle)
        age = time.time() - record['retrieved_at']
        if (record.get('schema_version') == CACHE_VERSION and record.get('source') == source
                and record.get('key') == key and 0 <= age < CACHE_TTL
                and _valid_authors(record.get('authors'))):
            return record['authors']
    except (OSError, ValueError, KeyError, TypeError):
        pass
    return None


def _save_authors(folder, key, source, url, body, authors):
    """Atomic success-only cache; errors never poison future lookups."""
    if not _valid_authors(authors):
        return None
    authors = [name.strip() for name in authors]
    record = {'schema_version': CACHE_VERSION, 'source': source, 'key': key,
              'source_url': url, 'retrieved_at': time.time(), 'authors': authors,
              'response_sha256': hashlib.sha256(body.encode()).hexdigest()}
    destination = _cache_file(folder, key)
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8',
                                         dir=os.path.dirname(destination), delete=False) as handle:
            temp_path = handle.name
            json.dump(record, handle, ensure_ascii=False, indent=2)
        os.replace(temp_path, destination)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
    return authors


def _arxiv_parse_authors(xml_text, expected_id):
    if not xml_text:
        return None
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return None
    if root.tag != f"{{{NS['a']}}}feed":
        return None
    entries = root.findall('a:entry', NS)
    if len(entries) != 1:
        return None
    entry = entries[0]
    source_id = entry.findtext('a:id', default='', namespaces=NS).strip()
    if not re.match(r'^https?://arxiv\.org/abs/', source_id):
        return None
    if canonical_arxiv_id(source_id) != expected_id:
        return None
    if not entry.findtext('a:title', default='', namespaces=NS).strip():
        return None
    authors = [author.findtext('a:name', default='', namespaces=NS)
               for author in entry.findall('a:author', NS)]
    return [name.strip() for name in authors] if _valid_authors(authors) else None


def fetch_arxiv_authors(arxiv_id, primary_category=None, delay=3, owner_hint=None):
    """Return exact-ID source authors, or None (unresolved).

    Bare seven-digit IDs are ambiguous and never resolved from category/name
    hints. The retained optional arguments keep older callers compatible; they
    do not authorize guessing an archive or binding an author to a person.
    """
    aid = canonical_arxiv_id(arxiv_id)
    if not aid or re.fullmatch(r'\d{7}', aid):
        return None
    cached = _read_cache(ARXIV_CACHE, aid, 'arxiv')
    if cached:
        return cached
    time.sleep(delay)
    url = f'https://export.arxiv.org/api/query?id_list={quote(aid, safe="/")}&max_results=1'
    body = _curl(url, expected_type='xml')
    authors = _arxiv_parse_authors(body, aid)
    if authors:
        return _save_authors(ARXIV_CACHE, aid, 'arxiv', url, body, authors)
    return None


def _doi(value):
    value = canonical_doi(value)
    return value if value and re.fullmatch(r'10\.\d{4,9}/\S+', value) else None


def fetch_crossref_authors(doi, delay=0.3):
    doi = _doi(doi)
    if not doi:
        return None
    cached = _read_cache(CROSSREF_CACHE, doi, 'crossref')
    if cached:
        return cached
    time.sleep(delay)
    url = f'https://api.crossref.org/works/{quote(doi, safe="/")}'
    body = _curl(url, expected_type='json')
    try:
        data = json.loads(body or '')
        message = data.get('message') or {}
        if data.get('status') != 'ok' or _doi(message.get('DOI')) != doi:
            return None
        authors = [(' '.join(str(a.get(part) or '').strip() for part in ('given', 'family'))).strip()
                   or a.get('name') or '' for a in message.get('author', [])]
    except (ValueError, AttributeError, TypeError):
        return None
    return _save_authors(CROSSREF_CACHE, doi, 'crossref', url, body, authors)


def _openalex_key(value):
    key = str(value or '').strip()
    key = re.sub(r'^https?://(?:api\.)?openalex\.org/(?:works/)?', '', key, flags=re.I)
    key = re.sub(r'^openalex:', '', key, flags=re.I)
    if re.fullmatch(r'W\d+', key, re.I):
        return key.upper()
    return _doi(key)


def fetch_openalex_authors(work_id_or_doi, delay=0.3):
    key = _openalex_key(work_id_or_doi)
    if not key:
        return None
    cached = _read_cache(OPENALEX_CACHE, key, 'openalex')
    if cached:
        return cached
    lookup = key if key.startswith('W') else 'doi:' + key
    url = f'https://api.openalex.org/works/{quote(lookup, safe="/:")}'
    time.sleep(delay)
    body = _curl(url, expected_type='json')
    try:
        data = json.loads(body or '')
        returned = _openalex_key(data.get('id')) if key.startswith('W') else _doi(data.get('doi'))
        if returned != key:
            return None
        authors = [(a.get('author') or {}).get('display_name') or ''
                   for a in data.get('authorships', [])]
    except (ValueError, AttributeError, TypeError):
        return None
    return _save_authors(OPENALEX_CACHE, key, 'openalex', url, body, authors)


def get_actual_authors(pub, owner_hint=None):
    """Return (source author names, source label), or (None, None).

    This lookup does not verify the record's title, DOI/arXiv equivalence or
    personal identity. Callers must not turn unresolved lookups into a verdict.
    """
    pid = str(pub.get('id') or '').strip()
    doi = _doi(pub.get('doi') or (pid[4:] if pid.startswith('doi:') else None))
    oa = pub.get('openalex_id') or (pid[9:] if pid.startswith('openalex:') else None)
    aid = canonical_arxiv_id(pid)
    if aid:
        authors = fetch_arxiv_authors(aid, primary_category=pub.get('primary_category'), owner_hint=owner_hint)
        if authors:
            return authors, 'arxiv'
    if doi:
        authors = fetch_crossref_authors(doi)
        if authors:
            return authors, 'crossref'
    for key in dict.fromkeys(key for key in (oa, doi) if key):
        authors = fetch_openalex_authors(key)
        if authors:
            return authors, 'openalex'
    return None, None
