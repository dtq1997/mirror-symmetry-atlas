#!/usr/bin/env python3
"""[Codex] Generate existing detail routes; never infer entities from names."""
import json
from pathlib import Path
import yaml


def main():
    routes = {}
    for kind in ('people', 'concepts', 'institutions', 'problems'):
        for path in sorted((Path('data') / kind).glob('*.yaml')):
            if path.name.startswith('_'):
                continue
            row = yaml.safe_load(path.read_text())
            slug = row['slug']
            if slug != path.stem:
                raise ValueError(f'{path}: slug does not match filename')
            name = row.get('name') or {}
            # Person/institution display names still use their existing SSOT.
            label = name.get('zh') or name.get('en') or slug
            routes[f'/{kind}/{slug}'] = label
    Path('src/lib/entity-routes.json').write_text(
        json.dumps(routes, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
    print(f'Generated {len(routes)} existing entity routes')


if __name__ == '__main__':
    main()
