"""Eject obviously-non-math publications wrongly attributed via name match.

Keywords come from scripts/non_math_keywords.py — single source of truth
shared with lint-data.py so the two never drift.
"""
import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from non_math_keywords import is_non_math_title
import importlib.util
_spec = importlib.util.spec_from_file_location(
    'canon', str(HERE / 'canonicalize-publications.py'))
_canon = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_canon)
render_pubs = _canon.render_pubs
render_activity = _canon.render_activity
replace_block = _canon.replace_block
is_published = _canon.is_published


def is_non_math(title):
    return is_non_math_title(title)


def main(apply=False):
    files_changed = 0
    total_ejected = 0
    log = []
    for f in sorted(PEOPLE_DIR.glob('*.yaml')):
        if f.name.startswith('_'):
            continue
        d = yaml.safe_load(f.read_text()) or {}
        slug = f.stem
        pubs = d.get('publications') or []
        keep, eject = [], []
        for p in pubs:
            if not isinstance(p, dict):
                keep.append(p); continue
            kw = is_non_math(p.get('title') or '')
            if kw:
                eject.append((p, kw))
            else:
                keep.append(p)
        if not eject:
            continue
        log.append((slug, eject))
        files_changed += 1
        total_ejected += len(eject)
        d['publications'] = keep
        if apply:
            text = f.read_text()
            text = replace_block(text, 'publications', render_pubs(keep))
            published = sum(1 for p in keep if isinstance(p, dict) and is_published(p))
            preprint = len(keep) - published
            try:
                p2 = yaml.safe_load(text)
                activity = dict(p2.get('activity') or {})
                activity['total_papers'] = len(keep)
                activity['published_count'] = published
                activity['preprint_only_count'] = preprint
                text = replace_block(text, 'activity', render_activity(activity))
            except Exception as e:
                print(f'  warn: {slug} activity recompute failed: {e}')
            f.write_text(text)

    print(f'\n{"APPLIED" if apply else "DRY-RUN"}: '
          f'{total_ejected} pubs across {files_changed} files\n')
    for slug, items in log:
        print(f'  {slug} ({len(items)}):')
        for p, kw in items:
            print(f'    - [{p.get("year")}] {p.get("title","")[:90]}  // matched {kw}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    main(apply=args.apply)
