"""[Codex] Validate timeline dates, citations and references, not historical truth."""
import re
from datetime import date
from concept_references import source_errors
from paper_identity import paper_identity_keys


def valid_date(value, precision):
    patterns = {'year': r'\d{4}', 'month': r'\d{4}-\d{2}', 'day': r'\d{4}-\d{2}-\d{2}'}
    pattern = patterns.get(precision) if isinstance(precision, str) else None
    try:
        if not isinstance(value, str) or not pattern or not re.fullmatch(pattern, value):
            return False
        date.fromisoformat(value + {'year': '-01-01', 'month': '-01', 'day': ''}[precision])
        return True
    except (TypeError, ValueError):
        return False


def reference_errors(event, people, concepts):
    errors = []
    for field, records in [('people', people), ('concepts', concepts)]:
        refs = event.get(field, [])
        if not isinstance(refs, list) or any(not isinstance(ref, str) or ref not in records for ref in refs):
            errors.append(f'{field} must identify existing entries')
    papers = event.get('papers', [])
    if not isinstance(papers, list):
        return errors + ['papers must be a list']
    for paper in papers:
        doi, arxiv, _ = paper_identity_keys({'id': paper}) if isinstance(paper, str) else (None, None, None)
        if not ((arxiv and not re.fullmatch(r'\d{7}', arxiv)) or (doi and re.fullmatch(r'10\.\d{4,9}/\S+', doi))):
            errors.append('papers contains an unsupported identifier')
    return errors


def review_errors(event):
    errors = source_errors(event)
    if not any(field in event for field in ('reviewed_on', 'review_note', 'date_note')):
        return errors
    for field in ('review_note', 'date_note'):
        if not isinstance(event.get(field), str) or not event[field].strip():
            errors.append(f'{field} requires text')
    if not valid_date(event.get('reviewed_on'), 'day'):
        errors.append('reviewed_on requires an ISO date')
    if not event.get('sources'):
        errors.append('recorded review requires sources')
    return errors


def timeline_errors(events, people, concepts):
    if not isinstance(events, list):
        return ['events must be a list']
    errors, seen = [], set()
    for index, event in enumerate(events):
        label = f'events[{index}]'
        if not isinstance(event, dict):
            errors.append(f'{label} must be an object')
            continue
        slug = event.get('slug')
        if not isinstance(slug, str) or not re.fullmatch(r'[a-z][a-z0-9-]*', slug):
            errors.append(f'{label} requires a slug')
        elif slug in seen:
            errors.append(f'{label} duplicates {slug}')
        else:
            seen.add(slug)
        if not valid_date(event.get('date'), event.get('precision')):
            errors.append(f'{label} requires a real date matching its precision')
        title = event.get('title')
        if not isinstance(title, dict) or not isinstance(title.get('en'), str) or not title['en'].strip():
            errors.append(f'{label} requires title.en')
        if event.get('era') not in ('prehistory', 'classical', 'modern', 'contemporary'):
            errors.append(f'{label} has unknown era')
        if event.get('importance') not in ('milestone', 'major', 'notable'):
            errors.append(f'{label} has unknown importance')
        messages = reference_errors(event, people, concepts) + review_errors(event)
        errors.extend(f'{label}: {message}' for message in messages)
    return errors
