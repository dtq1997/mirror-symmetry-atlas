"""[Codex] Links require reviewed individual recipients, not paper ownership.

This gate checks evidence consistency, not the truth of a human decision.
"""
import json
import re
from collections import defaultdict
from datetime import date
from itertools import combinations
from pathlib import Path

import yaml

from acknowledgement_review import ack_hash, normalized_text, raw_index
from paper_identity import canonical_arxiv_id


def valid_grant_number(value):
    return isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9/-]*', value)) and bool(re.search(r'\d', value))


def check_recipient(row, raw, people):
    person, paper = row.get('person'), row.get('paper')
    if person not in people or paper not in raw or canonical_arxiv_id(paper) != paper:
        raise ValueError('unknown person or paper')
    if not valid_grant_number(row.get('number')) or not row.get('agency'):
        raise ValueError('invalid agency or grant number')
    if row.get('status') not in {'accepted', 'rejected', 'needs-review'}:
        raise ValueError('invalid review status')
    if row.get('ack_sha256') != ack_hash(raw[paper]['ack_text']):
        raise ValueError('funding text changed; review again')
    date.fromisoformat(row.get('reviewed_on', ''))
    for field in ('reviewed_by', 'reason'):
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ValueError(f'missing {field}')
    if row['status'] != 'accepted':
        return
    if row.get('subject_scope') not in {'named-recipient', 'all-authors'}:
        raise ValueError('work-level funding cannot identify an individual recipient')
    for field in ('identity_note', 'subject_note', 'quote', 'author_name'):
        if not isinstance(row.get(field), str) or not row[field].strip():
            raise ValueError(f'missing {field}')
    quote = normalized_text(row['quote'])
    if quote not in normalized_text(raw[paper]['ack_text']) or not re.search(r'(?<![A-Za-z0-9])' + re.escape(row['number']) + r'(?![A-Za-z0-9])', quote):
        raise ValueError('quote must contain the exact grant number and exist in saved text')
    if not re.fullmatch(r'https://arxiv\.org/html/' + re.escape(paper) + r'v\d+', row.get('source_url', '')):
        raise ValueError('source URL must identify the reviewed version')
    authors = row.get('full_author_order')
    if not isinstance(authors, list) or not authors or not all(isinstance(a, str) and a.strip() for a in authors):
        raise ValueError('complete source author order required')
    if len(set(authors)) != len(authors) or authors.count(row['author_name']) != 1:
        raise ValueError('recipient absent from source author order')
    owned = {canonical_arxiv_id(p.get('id')) for p in people[person].get('publications', [])}
    if paper not in owned:
        raise ValueError('recipient absent from current bibliography')


def reviewed_grant_edges(records, reviews, people):
    raw, seen, author_orders = raw_index(records), set(), {}
    recipients = defaultdict(lambda: defaultdict(list))
    if not isinstance(reviews, list):
        raise ValueError('grant reviews must be a list')
    for row in reviews:
        if not isinstance(row, dict):
            raise ValueError('invalid grant review')
        check_recipient(row, raw, people)
        person, paper = row['person'], row['paper']
        key = (person, paper, row['agency'], row['number'])
        if key in seen:
            raise ValueError('duplicate or conflicting recipient review')
        seen.add(key)
        if row['status'] != 'accepted':
            continue
        if paper in author_orders and author_orders[paper] != row['full_author_order']:
            raise ValueError('conflicting source author order')
        author_orders[paper] = row['full_author_order']
        recipients[row['agency'], row['number']][person].append({
            'person': person, 'paper': paper, 'source_url': row['source_url']})
    pairs = defaultdict(list)
    for (agency, number), authors in sorted(recipients.items()):
        for a, b in combinations(sorted(authors), 2):
            evidence = sorted(authors[a] + authors[b], key=lambda e: (e['person'], e['paper']))
            pairs[a, b].append({'agency': agency, 'number': number, 'recipients': evidence})
    return {'meta': {'note': '论文明确记载两人受同一编号资助；不推断项目负责人、成员名单、期限或两人直接合作。'},
            'edges': [{'source': a, 'target': b, 'type': 'grant', 'derived': True,
                       'review_status': 'accepted', 'funding_evidence': grants}
                      for (a, b), grants in sorted(pairs.items())]}


def grant_errors(root, people):
    try:
        directory = Path(root) / 'data/derived'
        records = [json.loads(line) for line in (directory / 'raw-acks.jsonl').read_text().splitlines() if line.strip()]
        reviews = yaml.safe_load((directory / 'grant-reviews.yaml').read_text())['reviews']
        expected = reviewed_grant_edges(records, reviews, people)
        actual = yaml.safe_load((directory / 'grant-edges.yaml').read_text())
        if actual != expected:
            return ['grant-edges.yaml differs from reviewed recipients; run derive-grant-edges.py --write']
        return []
    except (OSError, KeyError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        return [f'invalid grant evidence: {exc}']
