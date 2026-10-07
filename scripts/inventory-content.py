#!/usr/bin/env python3
"""[Codex] Enumerate content review units without claiming factual correctness."""
import argparse
import hashlib
import json
from pathlib import Path
import yaml

COLLECTIONS = ('papers', 'publications', 'events', 'edges', 'single_mentions', 'entries', 'series', 'seminars')


def public_urls(value):
    if isinstance(value, dict):
        return sorted(set(url for child in value.values() for url in public_urls(child)))
    if isinstance(value, list):
        return sorted(set(url for child in value for url in public_urls(child)))
    return [value] if isinstance(value, str) and value.startswith(('https://', 'http://')) else []


def unit(path, locator, value):
    serialized = json.dumps(value, sort_keys=True, ensure_ascii=False, default=str)
    return {
        'file': str(path), 'locator': locator,
        'sha256': hashlib.sha256(serialized.encode()).hexdigest(),
        'review_status': 'not-reviewed-in-this-campaign',
        'source_candidates': public_urls(value),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    units = []
    auxiliary = []
    for path in sorted(Path('data').rglob('*.yaml')):
        if any(part.startswith('_') for part in path.parts):
            auxiliary.append(str(path))
            continue
        value = yaml.safe_load(path.read_text())
        units.append(unit(path, '$', value))
        if isinstance(value, dict):
            for key in COLLECTIONS:
                for index, row in enumerate(value.get(key) or []):
                    units.append(unit(path, f'{key}[{index}]', row))
    report = {
        'scope': 'Review units and candidate URLs. A URL or a previous verification date is not a new verification.',
        'files': len({row['file'] for row in units}), 'review_units': len(units),
        'auxiliary_files': auxiliary, 'units': units,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'{report["files"]} content files; {len(units)} review units; {len(auxiliary)} auxiliary/review files; no factual verdicts assigned')


if __name__ == '__main__':
    main()
