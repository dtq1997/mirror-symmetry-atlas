"""[Codex] Reference namespace checks, not mathematical relationship validation."""

from urllib.parse import urlsplit


def concept_content_errors(concept, concepts):
    """Check alias/citation structure only; a well-formed source is not a verdict."""
    errors = []
    if 'alias_of' in concept:
        alias = concept['alias_of']
        target = concepts.get(alias) if isinstance(alias, str) else None
        if not target or target.get('alias_of') or alias == concept.get('slug'):
            errors.append('alias_of must identify a different canonical concept')
        for field in ('definition', 'history_note', 'review_note', 'sources', 'year_introduced',
                      'introduced_by', 'prerequisites', 'leads_to', 'related', 'key_people',
                      'key_papers', 'contributions', 'dual_to'):
            if concept.get(field):
                errors.append(f'alias entry must keep {field} on its canonical concept')
    sources = concept.get('sources', [])
    if not isinstance(sources, list):
        return errors + ['sources must be a list']
    for index, source in enumerate(sources):
        if not isinstance(source, dict) or not isinstance(source.get('label'), str) or not source['label'].strip():
            errors.append(f'sources[{index}] requires a nonempty label')
            continue
        try:
            url = source.get('url')
            parsed = urlsplit(url) if isinstance(url, str) else None
            if not parsed or parsed.scheme not in ('http', 'https') or not parsed.netloc:
                errors.append(f'sources[{index}] requires an HTTP(S) URL')
        except ValueError:
            errors.append(f'sources[{index}] contains an invalid URL')
    return errors


def concept_reference_errors(concept, concepts, people, institutions):
    errors = []
    for field in ('prerequisites', 'leads_to', 'related'):
        refs = concept.get(field)
        if refs is None:
            refs = []
        if not isinstance(refs, list):
            errors.append(f'{field} must be a list of concept slugs')
            continue
        for index, ref in enumerate(refs):
            if not isinstance(ref, str) or not ref.strip():
                errors.append(f'{field}[{index}] must be a nonempty concept slug')
            elif ref not in concepts and (ref in people or ref in institutions):
                errors.append(f'{field}[{index}] {ref!r} identifies a person/institution, not a concept')
    return errors
