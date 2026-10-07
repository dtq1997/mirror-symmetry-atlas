"""[Codex] Preserve source-backed review decisions across enrichment runs.

These keys identify records, not people. Only an explicit per-person review
can block an attribution; titles and ambiguous legacy numbers never suffice.
"""
import os
from pathlib import Path
import re
import tempfile

import yaml
from paper_identity import canonical_arxiv_id, canonical_doi

BLOCKED_STATUSES = {'rejected-homonym', 'rejected', 'needs-review', 'quarantined'}


def record_keys(pub):
    keys = set()
    pid = str(pub.get('id') or '')
    doi = canonical_doi(pub.get('doi') or (pid if pid.startswith('doi:') else None))
    if doi and re.fullmatch(r'10\.\d{4,9}/\S+', doi):
        keys.add(('doi', doi))
    arxiv = canonical_arxiv_id(pid)
    if arxiv and not re.fullmatch(r'\d{7}', arxiv):
        keys.add(('arxiv', arxiv.lower()))
    for raw in [pub.get('openalex_id'), pid]:
        oa = re.sub(r'^(?:https?://openalex\.org/|openalex:)', '', str(raw or ''), flags=re.I)
        if re.fullmatch(r'W\d+', oa, re.I):
            keys.add(('openalex', oa.upper()))
    return keys


def load_review(path):
    path = Path(path)
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict) or not isinstance(data.get('candidates'), list):
        raise ValueError(f'Malformed publication review: {path}')
    if any(not isinstance(row, dict) for row in data['candidates']):
        raise ValueError(f'Malformed publication review candidate: {path}')
    return data


def blocked_review(pub, candidates):
    keys = record_keys(pub)
    return next((row for row in candidates
                 if row.get('review_status') in BLOCKED_STATUSES
                 and keys.intersection(record_keys(row))), None)


def save_candidates(path, slug, candidates):
    """Replace unreviewed suggestions, retaining every explicit review intact."""
    path = Path(path)
    previous = load_review(path)
    reviewed = [row for row in previous.get('candidates', []) if row.get('review_status')]
    reviewed_keys = set().union(*(record_keys(row) for row in reviewed))
    fresh = [row for row in candidates if not record_keys(row).intersection(reviewed_keys)]
    output = dict(previous, slug=slug, count=len(reviewed) + len(fresh), candidates=reviewed + fresh)
    output.setdefault('note', '[Codex] 自动候选待核实；已有具名审查保留，不能由自动评分覆盖。')
    if not output['candidates'] and not path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile('w', dir=path.parent, suffix='.yaml', delete=False) as f:
            temp_path = f.name
            yaml.safe_dump(output, f, allow_unicode=True, sort_keys=False)
        os.replace(temp_path, path)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
