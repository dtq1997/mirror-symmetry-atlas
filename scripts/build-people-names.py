#!/usr/bin/env python3
"""Generate src/lib/people-names.json — single source of truth for slug → display name.

All UI components (server + client) import from this JSON so there's one place
to look up a person's display name. Chinese name preferred when available
and not a [待验证] placeholder; English fallback.

Also includes "ghost" slugs (referenced from connections/advisor-student.yaml,
career_timeline advisor fields, key_collaborators etc. but no own yaml file)
with English-style names derived from slug for legibility.

Run before `pnpm build` (or as a build step).
"""

import json
import os
import re
import yaml

PEOPLE_DIR = 'data/people'
CONN_DIR = 'data/connections'
OUT = 'src/lib/people-names.json'


def slug_to_english(slug):
    """Best-effort English Title Case from slug. e.g. 'croke' → 'Croke',
    'tian-jun-li' → 'Tian-Jun Li' (last token is the surname)."""
    parts = slug.split('-')
    if not parts:
        return slug
    # Single token: just title-case
    if len(parts) == 1:
        return parts[0].title()
    # Heuristic: surname is the longer / more distinctive token, often listed first
    # in pinyin slugs (e.g. 'liu-xiaobo' = surname Liu first). For ghost slugs of
    # foreign names (e.g. 'croke' alone), it's usually surname only. For multi-token
    # we don't know order, so just title-case all and join with space.
    return ' '.join(p.title() for p in parts)


def main():
    table = {}
    # 1. Real yaml people
    yaml_slugs = set()
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        yaml_slugs.add(slug)
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            p = yaml.safe_load(fh) or {}
        name = p.get('name') or {}
        en = name.get('en') or slug
        zh = name.get('zh') or ''
        use_zh = bool(zh) and not zh.startswith('[') and not zh.startswith('待')
        table[slug] = {
            'displayName': zh if use_zh else en,
            'en': en,
            'zh': zh if use_zh else None,
        }

    # 2. Ghost slugs: collect all slugs referenced anywhere
    ghost_slugs = set()

    def maybe_add(s):
        if isinstance(s, str) and s and re.fullmatch(r'[a-z][a-z0-9-]*', s):
            ghost_slugs.add(s)

    # Connections
    if os.path.isdir(CONN_DIR):
        for f in os.listdir(CONN_DIR):
            if not f.endswith('.yaml'):
                continue
            with open(os.path.join(CONN_DIR, f)) as fh:
                d = yaml.safe_load(fh) or {}
            for e in (d.get('edges') or []):
                maybe_add(e.get('source'))
                maybe_add(e.get('target'))
                for p in (e.get('papers') or []):
                    pass  # paper ids, not slugs

    # Per-yaml refs
    for f in os.listdir(PEOPLE_DIR):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            p = yaml.safe_load(fh) or {}
        maybe_add(p.get('advisor'))
        for s in (p.get('students') or []):
            maybe_add(s)
        for s in (p.get('mentors') or []):
            maybe_add(s)
        for kc in (p.get('key_collaborators') or []):
            maybe_add(kc.get('person'))
        for ev in (p.get('career_timeline') or []):
            maybe_add(ev.get('advisor'))
        for pub in (p.get('publications') or []):
            for c in (pub.get('coauthors') or []):
                maybe_add(c)

    ghost_slugs -= yaml_slugs
    for slug in ghost_slugs:
        en = slug_to_english(slug)
        table[slug] = {
            'displayName': en,
            'en': en,
            'zh': None,
        }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        json.dump(table, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print(f'wrote {OUT}: {len(yaml_slugs)} yaml + {len(ghost_slugs)} ghost = {len(table)}')


if __name__ == '__main__':
    main()
