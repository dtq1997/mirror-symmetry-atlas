#!/usr/bin/env python3
"""Generate src/lib/institution-names.json — SSOT for institution slug → display name.

Same SSOT philosophy as build-people-names.py. Every UI place that renders an
institution slug MUST go through institutionName(slug).
"""
import json
import os
import yaml

INST_DIR = 'data/institutions'
OUT = 'src/lib/institution-names.json'


def main():
    table = {}
    if not os.path.isdir(INST_DIR):
        print(f'No institutions dir at {INST_DIR}')
        return
    for f in sorted(os.listdir(INST_DIR)):
        if not f.endswith('.yaml') or f.startswith('_'):
            continue
        slug = f.replace('.yaml', '')
        with open(os.path.join(INST_DIR, f)) as fh:
            d = yaml.safe_load(fh) or {}
        name = d.get('name') or {}
        if isinstance(name, str):
            zh = name; en = name
        else:
            en = name.get('en') or slug
            zh = name.get('zh') or ''
        use_zh = bool(zh) and not str(zh).startswith('[') and not str(zh).startswith('待')
        table[slug] = {
            'displayName': zh if use_zh else en,
            'en': en,
            'zh': zh if use_zh else None,
        }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w') as fh:
        json.dump(table, fh, ensure_ascii=False, indent=2, sort_keys=True)
    print(f'wrote {OUT}: {len(table)} institutions')


if __name__ == '__main__':
    main()
