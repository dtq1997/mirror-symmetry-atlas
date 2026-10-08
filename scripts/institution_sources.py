"""[Codex] Structural gate for dated appointment citations, not a truth oracle."""
from datetime import date
import re
from urllib.parse import urlsplit


def appointment_errors(institution, people, today=None):
    today = today or date.today()
    records = institution.get('appointment_checks', [])
    if not isinstance(records, list):
        return ['appointment_checks must be a list']
    errors = []
    seen = set()
    for index, record in enumerate(records):
        prefix = f'appointment_checks[{index}]'
        if not isinstance(record, dict):
            errors.append(f'{prefix} must be an object')
            continue
        person = record.get('person')
        if not isinstance(person, str) or person not in people:
            errors.append(f'{prefix}.person must identify an existing person')
        role = record.get('role')
        if not isinstance(role, str) or not role.strip() or '待核' in role or '待验证' in role:
            errors.append(f'{prefix}.role must state the source-backed role')
        day = record.get('checked_on')
        try:
            if not isinstance(day, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', day):
                raise ValueError
            if date.fromisoformat(day) > today:
                raise ValueError
        except ValueError:
            errors.append(f'{prefix}.checked_on must be a real, nonfuture YYYY-MM-DD date string')
        source = record.get('source')
        if not isinstance(source, dict) or not isinstance(source.get('label'), str) or not source['label'].strip():
            errors.append(f'{prefix}.source needs a nonempty label')
        url = source.get('url') if isinstance(source, dict) else None
        try:
            parsed = urlsplit(url) if isinstance(url, str) else None
            if not parsed or parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
                raise ValueError
        except ValueError:
            errors.append(f'{prefix}.source.url must be a public HTTP(S) URL')
        if isinstance(person, str) and isinstance(day, str):
            key = (person, day)
            if key in seen:
                errors.append(f'{prefix} duplicates a person/date check')
            seen.add(key)
    return errors
