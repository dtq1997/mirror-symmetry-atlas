"""[Codex] Problem-page input validation; no mathematical status inference."""
from datetime import date
from concept_references import source_errors


def problem_errors(problem, problems):
    errors = source_errors(problem)
    if problem.get('status') not in ('open', 'partially-solved', 'solved', 'abandoned', 'needs-review'):
        errors.append('unknown problem status')
    review_fields = ('status_note', 'review_note', 'reviewed_on')
    if any(field in problem for field in review_fields):
        for field in review_fields:
            if not isinstance(problem.get(field), str) or not problem[field].strip():
                errors.append(f'{field} must be nonempty text')
        try:
            date.fromisoformat(problem.get('reviewed_on', ''))
        except (TypeError, ValueError):
            errors.append('reviewed_on must be an ISO date')
        if not problem.get('sources'):
            errors.append('recorded review requires sources')
    related = problem.get('related_problems', [])
    if not isinstance(related, list) or any(not isinstance(ref, str) or ref not in problems for ref in related):
        errors.append('related_problems must identify existing problem entries')
    progress = problem.get('progress', [])
    if not isinstance(progress, list):
        return errors + ['progress must be a list']
    for index, entry in enumerate(progress):
        if not isinstance(entry, dict):
            errors.append(f'progress[{index}] must be an object')
            continue
        for field in ('date', 'description'):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(f'progress[{index}].{field} requires text')
        papers = entry.get('papers', [])
        if not isinstance(papers, list) or any(not isinstance(p, str) or not p.strip() for p in papers):
            errors.append(f'progress[{index}].papers must be a list of identifiers')
    return errors
