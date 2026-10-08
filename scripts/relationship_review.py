"""[Codex] Structural gates for explicitly reviewed relationship records.

This detects duplicate episodes and prevents restoration of withheld claims.
It does not establish historical truth for other relationships.
"""
from pathlib import Path
import yaml

MENTOR_TYPES = {'advisor-student', 'postdoc-mentor'}
UNDIRECTED_TYPES = {'co-student', 'institutional'}
REVIEW_STATES = {'needs-review', 'rejected', 'accepted'}


def relationship_key(edge):
    source, target = edge.get('source'), edge.get('target')
    kind = edge.get('type')
    if not all(isinstance(x, str) and x.strip() for x in (source, target, kind)):
        raise ValueError('relationship requires nonempty string source, target and type')
    if kind in UNDIRECTED_TYPES:
        source, target = sorted((source, target))
    return source, target, kind


def relationship_errors(named_edges, review_dir):
    errors, seen, blocked = [], {}, {}
    for path in sorted(Path(review_dir).glob('*.yaml')):
        try:
            review = yaml.safe_load(path.read_text()) or {}
            candidates = review.get('candidates', [])
            if not isinstance(candidates, list):
                raise ValueError('candidates must be a list')
            for item in candidates:
                if not isinstance(item, dict) or item.get('review_status') not in REVIEW_STATES:
                    raise ValueError('invalid relationship review status')
                key = relationship_key(item.get('record') or {})
                if item['review_status'] != 'accepted':
                    blocked[key] = path.name
        except (ValueError, TypeError, AttributeError, OSError, yaml.YAMLError) as exc:
            errors.append(f'{path.name}: invalid relationship review: {exc}')
    for label, edge in named_edges:
        try:
            key = relationship_key(edge)
            if key in blocked:
                errors.append(f'{label}: relationship is withheld by {blocked[key]}; review sources before restoring')
            if edge.get('type') in MENTOR_TYPES:
                # Separate degrees / institutions / dated episodes remain distinct.
                episode = key + tuple(str(edge.get(k) or '') for k in ('institution', 'year', 'period'))
                if episode in seen:
                    errors.append(f'{label}: duplicate mentor episode of {seen[episode]}')
                seen[episode] = label
        except (ValueError, TypeError, AttributeError) as exc:
            errors.append(f'{label}: invalid relationship: {exc}')
    return errors
