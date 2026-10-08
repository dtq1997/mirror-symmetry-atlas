#!/usr/bin/env python3
"""[Codex] Preview reviewed recipient links; --write explicitly materializes them."""
import argparse
import json
from pathlib import Path

import yaml

from grant_review import reviewed_grant_edges

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    directory = ROOT / 'data/derived'
    raw = [json.loads(line) for line in (directory / 'raw-acks.jsonl').read_text().splitlines() if line.strip()]
    reviews = yaml.safe_load((directory / 'grant-reviews.yaml').read_text())['reviews']
    people = {p.stem: yaml.safe_load(p.read_text()) for p in (ROOT / 'data/people').glob('*.yaml')}
    data = reviewed_grant_edges(raw, reviews, people)
    if args.write:
        target = directory / 'grant-edges.yaml'
        temporary = target.with_suffix('.yaml.pending')
        try:
            temporary.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
    print(json.dumps({'mode': 'write' if args.write else 'read-only', 'edges': data['edges']}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
