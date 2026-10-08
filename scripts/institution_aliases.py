"""[Codex] Explicit one-hop aliases; never infer identity from similar names."""


def alias_errors(records):
    errors = []
    for slug, record in records.items():
        if 'alias_of' not in record:
            continue
        target_slug = record['alias_of']
        target = records.get(target_slug) if isinstance(target_slug, str) else None
        if not target or target_slug == slug or 'alias_of' in target:
            errors.append(f'{slug}: alias_of must point directly to an existing primary institution')
        # A redirect cannot silently discard independently maintained content.
        for field in ('research_groups', 'appointment_checks', 'events', 'notes'):
            if record.get(field):
                errors.append(f'{slug}: move {field} to the primary institution before declaring an alias')
    return errors
