"""[Codex] Publish only explicitly reviewed, text-bound acknowledgement claims.

Name matches and a paper's registered owners are review leads, never a verdict
about who thanked whom. This gate checks evidence consistency, not its truth.
"""
import hashlib
import json
import re
from collections import defaultdict
from datetime import date
from pathlib import Path

import yaml

from paper_identity import canonical_arxiv_id


def ack_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def normalized_text(text):
    return ' '.join(text.split())


def raw_index(records):
    result = {}
    for row in records:
        paper = canonical_arxiv_id(row.get('arxiv_id'))
        if not paper or paper in result or not isinstance(row.get('ack_text'), str):
            raise ValueError('invalid or duplicate raw acknowledgement paper')
        result[paper] = row
    return result


def checked_reviews(records, reviews, people):
    raw, result = raw_index(records), {}
    if not isinstance(reviews, list):
        raise ValueError('acknowledgement reviews must be a list')
    for row in reviews:
        key = (row.get('source'), row.get('target'), row.get('paper'))
        source, target, paper = key
        if source not in people or target not in people or source == target:
            raise ValueError(f'{key}: invalid source or target')
        if paper not in raw or canonical_arxiv_id(paper) != paper or key in result:
            raise ValueError(f'{key}: missing paper or duplicate/conflicting review')
        if row.get('status') not in {'accepted', 'rejected', 'needs-review'}:
            raise ValueError(f'{key}: invalid review status')
        if row.get('ack_sha256') != ack_hash(raw[paper]['ack_text']):
            raise ValueError(f'{key}: acknowledgement changed; review again')
        date.fromisoformat(row.get('reviewed_on', ''))
        for field in ('reviewed_by', 'reason'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                raise ValueError(f'{key}: missing {field}')
        if row['status'] in {'accepted', 'rejected'}:
            quote = row.get('quote', '')
            if not quote or normalized_text(quote) not in normalized_text(raw[paper]['ack_text']):
                raise ValueError(f'{key}: quote absent from saved acknowledgement')
            if not re.fullmatch(r'https://arxiv\.org/(?:abs|html)/' + re.escape(paper) + r'(?:v\d+)?', row.get('source_url', '')):
                raise ValueError(f'{key}: source URL must identify the reviewed paper')
        if row['status'] == 'accepted':
            for field in ('identity_note', 'subject_note'):
                if not isinstance(row.get(field), str) or not row[field].strip():
                    raise ValueError(f'{key}: missing {field}')
            owned = {canonical_arxiv_id(p.get('id')) for p in people[source].get('publications', [])}
            if paper not in owned:
                raise ValueError(f'{key}: reviewed author is absent from current bibliography')
        result[key] = row
    return result


def reviewed_edges(records, reviews, people):
    decisions = checked_reviews(records, reviews, people)
    grouped = defaultdict(set)
    for (source, target, paper), review in decisions.items():
        if review['status'] == 'accepted':
            grouped[source, target].add(paper)
    rows = [dict(source=s, target=t, type='acknowledgement',
                 review_status='accepted', weight=len(papers), papers=sorted(papers))
            for (s, t), papers in sorted(grouped.items())]
    return {'meta': {'note': '仅包含逐篇核对身份和致谢主体的记录；次数是不同论文数，不表示学术影响力。',
                     'single_count': sum(e['weight'] == 1 for e in rows),
                     'strong_count': sum(e['weight'] >= 2 for e in rows)},
            'edges': [e for e in rows if e['weight'] >= 2],
            'single_mentions': [e for e in rows if e['weight'] == 1]}


def acknowledgement_errors(root, people):
    """Prebuild gate: no unreviewed insertion or stale materialized output."""
    try:
        directory = Path(root) / 'data/derived'
        records = [json.loads(line) for line in (directory / 'raw-acks.jsonl').read_text().splitlines() if line.strip()]
        reviews = yaml.safe_load((directory / 'ack-reviews.yaml').read_text())['reviews']
        expected = reviewed_edges(records, reviews, people)
        actual = yaml.safe_load((directory / 'acknowledgements.yaml').read_text())
        if actual != expected:
            return ['acknowledgements.yaml differs from reviewed evidence; regenerate with match-acks-to-people.py --write']
        return []
    except (OSError, KeyError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        return [f'invalid acknowledgement evidence: {exc}']
