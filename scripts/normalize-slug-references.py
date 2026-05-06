"""Replace raw-name strings in yaml fields with slugs when an unambiguous
slug exists.

Targets:
  - key_collaborators[].person  (when raw English name string)
  - career_timeline[].advisor    (raw name)
  - publications[].coauthors     (raw name — only when EXACTLY one slug
    matches strictly; never on initials)

Uses scripts/name_match.py:slug_for_author for unambiguous matching.
Conservative: if multiple slugs match, leaves the raw name intact.

Apply with --apply; otherwise dry-run.
"""
import argparse
import os
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from name_match import slug_for_author, is_slug

ROOT = HERE.parent
PEOPLE_DIR = ROOT / 'data/people'

import importlib.util
_spec = importlib.util.spec_from_file_location(
    'canon', str(HERE / 'canonicalize-publications.py'))
_canon = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_canon)
render_pubs = _canon.render_pubs
replace_block = _canon.replace_block


def main(apply=False):
    all_people = {}
    for f in sorted(PEOPLE_DIR.glob('*.yaml')):
        if f.name.startswith('_'):
            continue
        with open(f) as fh:
            all_people[f.stem] = yaml.safe_load(fh) or {}

    n_kc = n_advisor = n_pub = 0
    files_changed = set()

    for slug, person in all_people.items():
        # 1) key_collaborators[].person
        for kc in (person.get('key_collaborators') or []):
            p = kc.get('person')
            if not p or is_slug(p):
                continue
            cand = slug_for_author(str(p), all_people)
            if cand and cand != slug:
                print(f'  {slug}: kc.person {p!r} → {cand}')
                if apply:
                    kc['person'] = cand
                n_kc += 1
                files_changed.add(slug)

        # 2) career_timeline[].advisor (slug-able)
        for e in (person.get('career_timeline') or []):
            a = e.get('advisor')
            if not a or is_slug(a):
                continue
            if '[' in str(a):  # [待验证] etc — leave alone
                continue
            cand = slug_for_author(str(a), all_people)
            if cand and cand != slug:
                print(f'  {slug}: timeline.advisor {a!r} → {cand}')
                if apply:
                    e['advisor'] = cand
                n_advisor += 1
                files_changed.add(slug)

        # 3) publications[].coauthors (raw name — only when unambiguous)
        for pub in (person.get('publications') or []):
            if not isinstance(pub, dict):
                continue
            cas = pub.get('coauthors') or []
            new_cas = []
            changed = False
            for c in cas:
                if isinstance(c, str) and not is_slug(c):
                    cand = slug_for_author(c, all_people)
                    if cand and cand != slug:
                        new_cas.append(cand)
                        changed = True
                        n_pub += 1
                        continue
                new_cas.append(c)
            if changed:
                pub['coauthors'] = new_cas
                files_changed.add(slug)

    print(f'\nSummary: kc.person={n_kc}, timeline.advisor={n_advisor}, '
          f'publications.coauthors={n_pub}')
    print(f'Files changed: {len(files_changed)}')

    if not apply:
        return

    # Write back
    for slug in files_changed:
        path = PEOPLE_DIR / f'{slug}.yaml'
        text = path.read_text()
        person = all_people[slug]
        # Re-render publications (preserve formatting via canon helpers)
        if person.get('publications'):
            text = replace_block(text, 'publications',
                                  render_pubs(person['publications']))
        # For key_collaborators / career_timeline, in-place YAML rewrite is
        # risky (formatting). Use regex line edits.
        # k_collaborators: replace "person: '<raw>'" with "person: <slug>"
        for kc in (person.get('key_collaborators') or []):
            if not is_slug(kc.get('person', '')):
                continue
            # Already updated in-memory; we need to find original raw value.
            # Easier: re-parse and do a generic dump for THIS section. To
            # avoid wholesale yaml.dump (breaks formatting), we walk the file
            # text and patch only matched lines.
            pass  # see below

        # Strategy: load file as YAML, mutate, dump only the two top-level
        # sections we care about. Dumping full yaml will reformat — to
        # preserve manual style, we instead write a single-key replacement.
        for section in ('key_collaborators', 'career_timeline'):
            block = person.get(section)
            if block is None:
                continue
            new_block = yaml.safe_dump(
                {section: block}, allow_unicode=True, sort_keys=False,
                width=200, default_flow_style=False).rstrip() + '\n'
            text = replace_block(text, section, new_block.rstrip('\n'))
        path.write_text(text)
        print(f'  wrote {slug}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    main(apply=args.apply)
