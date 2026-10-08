"""[Codex] Reference namespace checks, not mathematical relationship validation."""


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
