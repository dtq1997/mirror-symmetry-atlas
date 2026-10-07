#!/usr/bin/env python3
"""[Codex] Fetch complete bounded arXiv windows; names are leads, not identities.

Any HTTP, XML or pagination failure exits nonzero BEFORE changing news files.
Successful reruns merge today's entries. No researcher profile is auto-modified.
"""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET

import yaml
from name_match import names_match
from paper_identity import canonical_arxiv_id

ROOT = Path(__file__).resolve().parents[1]
NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom',
      'o': 'http://a9.com/-/spec/opensearch/1.1/'}
CATEGORIES = ['math-ph', 'math.AG', 'math.QA', 'hep-th', 'math.DG', 'math.SG', 'nlin.SI']


class FetchError(RuntimeError):
    pass


def load_people():
    people = {}
    for file in sorted((ROOT / 'data/people').glob('*.yaml')):
        if file.name.startswith('_'):
            continue
        person = yaml.safe_load(file.read_text()) or {}
        people[file.stem] = {'name_en': (person.get('name') or {}).get('en', '')}
    return people


def load_concepts():
    return {f.stem for f in (ROOT / 'data/concepts').glob('*.yaml')
            if not f.name.startswith('_')}


def author_candidates(author_name, people):
    # Shared name matching is only a search aid. Never choose the first homonym.
    # Initial-only/surname-only names do not supply an adequate search lead.
    if len(re.findall(r'[A-Za-z]{2,}', author_name)) < 2:
        return []
    return sorted(slug for slug, person in people.items()
                  if names_match(person['name_en'], author_name))


def match_concepts(title, abstract, concepts):
    text = title + ' ' + abstract
    # Whole ordered phrases: "RNA" must not match inside "external", etc.
    return sorted(c for c in concepts if re.search(
        r'(?<!\w)' + r'[\s\-–]+'.join(re.escape(t) for t in c.split('-')) + r'(?!\w)',
        text, re.I))


def parse_feed(body, expected_start):
    try:
        root = ET.fromstring(body)
        if root.tag != f"{{{NS['a']}}}feed":
            raise ValueError('not an Atom feed')
        total = int(root.findtext('o:totalResults', default='', namespaces=NS))
        start = int(root.findtext('o:startIndex', default='', namespaces=NS))
        if total < 0 or start != expected_start:
            raise ValueError('invalid total or wrong page offset')
        papers = []
        for entry in root.findall('a:entry', NS):
            def required(key):
                value = entry.findtext(key, default='', namespaces=NS).strip()
                if not value:
                    raise ValueError(f'missing {key}')
                return value
            url = required('a:id')
            if not re.fullmatch(r'https?://(?:export\.)?arxiv\.org/abs/.+', url):
                raise ValueError('arXiv error entry or invalid article URL')
            aid = canonical_arxiv_id(url)
            if not aid or re.fullmatch(r'\d{7}', aid):
                raise ValueError('ambiguous or invalid arXiv ID')
            published, updated = required('a:published'), required('a:updated')
            for timestamp in (published, updated):
                if datetime.fromisoformat(timestamp.replace('Z', '+00:00')).tzinfo is None:
                    raise ValueError('timestamp without timezone')
            authors = [a.findtext('a:name', default='', namespaces=NS).strip()
                       for a in entry.findall('a:author', NS)]
            category = entry.find('arxiv:primary_category', NS)
            if not authors or not all(authors) or category is None or not category.get('term'):
                raise ValueError('missing authors or primary category')
            papers.append({
                'id': aid, 'title': ' '.join(required('a:title').split()),
                'abstract': ' '.join(required('a:summary').split()),
                'authors_raw': authors, 'date': published[:10], 'published': published,
                'updated': updated, 'category': category.get('term'),
                'source_url': f'https://arxiv.org/abs/{aid}',
                'source_version': url.split('/abs/', 1)[1],
            })
        if start + len(papers) > total or (not papers and start < total):
            raise ValueError('incomplete or inconsistent page')
        return total, papers
    except (ET.ParseError, ValueError, TypeError) as exc:
        raise FetchError(f'Invalid arXiv response: {exc}') from exc


def request_feed(url):
    result = subprocess.run(
        ['curl', '--fail', '--silent', '--show-error', '--location',
         '--max-time', '30', '--retry', '2', '--retry-delay', '4',
         '--user-agent', 'MirrorSymmetryAtlas/1.0 (+https://dtq1997.github.io/mirror-symmetry-atlas/)', url],
        capture_output=True, timeout=110)
    if result.returncode or not result.stdout:
        raise FetchError(f'arXiv HTTP request failed (curl {result.returncode})')
    return result.stdout


def fetch_recent_papers(days=7, page_size=200, max_pages=50, now=None, request=request_feed,
                        sleep=time.sleep, cache_dir=None):
    now = now or datetime.now(timezone.utc)
    # Bound both ends so a changing feed cannot extend the window while paging.
    cutoff = now - timedelta(days=days)
    date_range = f'submittedDate:[{cutoff:%Y%m%d%H%M} TO {now:%Y%m%d%H%M}]'
    query = '(' + ' OR '.join(f'cat:{c}' for c in CATEGORIES) + ') AND ' + date_range
    papers, evidence, expected_total, start = {}, [], None, 0
    for page in range(max_pages):
        if page:
            sleep(4)
        url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode({
            'search_query': query, 'start': start, 'max_results': page_size,
            'sortBy': 'submittedDate', 'sortOrder': 'descending'})
        body = request(url)
        total, rows = parse_feed(body, start)
        if expected_total is not None and total != expected_total:
            raise FetchError('arXiv result count changed while paging; retry later')
        expected_total = total
        if len(rows) > page_size:
            raise FetchError('arXiv page exceeds requested size')
        digest = hashlib.sha256(body).hexdigest()
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
            (cache_dir / f'{digest}.xml').write_bytes(body)
        evidence.append({'url': url, 'sha256': digest, 'start': start, 'count': len(rows)})
        for paper in rows:
            if paper['id'] in papers:
                raise FetchError('duplicate ID across pages; incomplete coverage')
            published = datetime.fromisoformat(paper['published'].replace('Z', '+00:00'))
            # API uses minute-resolution boundaries; allow the entire first minute.
            if not cutoff.replace(second=0, microsecond=0) <= published <= now:
                raise FetchError('arXiv returned an article outside the requested window')
            papers[paper['id']] = paper
        start += len(rows)
        print(f'arXiv: {start}/{total} records', file=sys.stderr)
        if start == total:
            return list(papers.values()), {'query': query, 'categories': CATEGORIES,
                    'window_start': cutoff.isoformat(), 'window_end': now.isoformat(),
                    'total_fetched': total, 'pages': evidence}
    raise FetchError(f'Exceeded {max_pages} pages; refusing an incomplete update')


def news_entry(paper, people, concepts, retrieved_at, min_score):
    candidates = sorted({slug for name in paper['authors_raw']
                         for slug in author_candidates(name, people)})
    matched = match_concepts(paper['title'], paper['abstract'], concepts)
    score = 10 * bool(candidates) + 3 * len(matched)
    if score < min_score:
        return None
    # Keep the complete abstract in the response cache for selection/review.
    # The public feed contains bibliographic facts and a link to the original.
    metadata = {key: value for key, value in paper.items() if key != 'abstract'}
    return {**metadata, 'matched_people': [], 'candidate_people': candidates,
            'matched_concepts': matched, 'relevance_score': score,
            'review_status': 'metadata-only', 'retrieved_at': retrieved_at,
            'summary_zh': ''}


def read_news(file):
    data = yaml.safe_load(file.read_text()) or {}
    if not isinstance(data, dict) or not isinstance(data.get('entries', []), list):
        raise FetchError(f'Malformed existing news file: {file.name}')
    return data


def canonical_news_id(value):
    return canonical_arxiv_id(value) or str(value)


def merge_entries(existing, incoming):
    # Preserve manually edited rows. Refresh only metadata-only rows on same-day reruns.
    by_id = {canonical_news_id(e['id']): e for e in existing}
    for entry in incoming:
        key = canonical_news_id(entry['id'])
        old = by_id.get(key)
        if old is None or old.get('review_status') == 'metadata-only':
            by_id[key] = entry
    return sorted(by_id.values(), key=lambda e: (e['date'], e['id']), reverse=True)


def write_update(output, entries, evidence, now, days, dedup_window):
    # Validate all existing input before any write. Same-day files are excluded from dedup.
    previous = read_news(output) if output.exists() else {}
    cutoff = now.date() - timedelta(days=dedup_window)
    seen = set()
    for file in output.parent.glob('*.yaml'):
        if file.resolve() == output.resolve() or file.name.startswith('_'):
            continue
        try:
            day = datetime.strptime(file.stem, '%Y-%m-%d').date()
        except ValueError:
            continue
        if dedup_window > 0 and day >= cutoff:
            seen.update(canonical_news_id(e['id']) for e in read_news(file).get('entries', []))
    incoming = [e for e in entries if canonical_news_id(e['id']) not in seen]
    merged = merge_entries(previous.get('entries', []), incoming)
    data = {**previous, 'fetch_date': now.date().isoformat(), 'period_days': days,
            'last_success_at': now.isoformat(), 'total_fetched': evidence['total_fetched'],
            'relevant_count': len(merged), 'fetch_evidence': evidence, 'entries': merged}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix('.yaml.new')
    temporary.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding='utf-8')
    temporary.replace(output)
    print(f'Wrote {len(merged)} entries to {output}', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--min-score', type=int, default=3)
    parser.add_argument('--dedup-window', type=int, default=14)
    parser.add_argument('--max-pages', type=int, default=50)
    args = parser.parse_args()
    if args.days < 1 or args.max_pages < 1 or args.min_score < 1 or args.dedup_window < 0:
        parser.error('days, max-pages and min-score must be positive; dedup-window nonnegative')
    now = datetime.now(timezone.utc)
    output = args.output or ROOT / 'data/news' / f'{now:%Y-%m-%d}.yaml'
    try:
        papers, evidence = fetch_recent_papers(args.days, max_pages=args.max_pages, now=now,
                cache_dir=ROOT / '.cache/msa/arxiv-news' / f'{now:%Y-%m-%d}')
        people, concepts = load_people(), load_concepts()
        entries = [entry for paper in papers if (entry := news_entry(
            paper, people, concepts, now.isoformat(), args.min_score))]
        write_update(output, entries, evidence, now, args.days, args.dedup_window)
    except (FetchError, OSError, subprocess.TimeoutExpired, yaml.YAMLError, KeyError) as exc:
        print(f'FAILED: {exc}. Existing news preserved.', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
