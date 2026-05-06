"""Full-coverage publication validator.

For every (yaml-owner-slug, pub) pair:
  1. Look up authoritative author list via arxiv/Crossref/OpenAlex (lib_truth).
  2. If yaml owner not strictly among real authors → eject paper from yaml.
  3. For each slug-form coauthor: if it doesn't strictly match any real
     author → try to find correct slug, else replace with a raw real-author
     name from the unaccounted-for set.
  4. Dedup raw-name coauthors that already correspond to a slug already
     present.

Strict matching only — see scripts/name_match.py.

Output: a unified diff log and (with --apply) writes corrected yamls in
place using the existing render_pubs from canonicalize-publications.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from name_match import names_match, names_compatible, is_slug
from lib_truth import get_actual_authors

ROOT = os.path.dirname(HERE)
PEOPLE_DIR = os.path.join(ROOT, 'data/people')

# Reuse existing yaml-friendly renderers from canonicalize-publications
import importlib.util
_spec = importlib.util.spec_from_file_location(
    'canon', os.path.join(HERE, 'canonicalize-publications.py'))
_canon = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_canon)
render_pubs = _canon.render_pubs
render_activity = _canon.render_activity
replace_block = _canon.replace_block
is_published = _canon.is_published


def find_correct_slug(actual_author, all_people, used_slugs):
    """Return the slug whose name strictly matches `actual_author`,
    excluding `used_slugs`. Only returns a unique match (no ambiguity)."""
    matches = []
    for slug, p in all_people.items():
        if slug in used_slugs:
            continue
        en = ((p.get('name') or {}).get('en') or '')
        if en and names_match(en, actual_author):
            matches.append(slug)
    return matches[0] if len(matches) == 1 else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--only', help='Only process this slug (for debugging)')
    args = parser.parse_args()

    all_people = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            all_people[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}

    slug_to_en = {s: ((p.get('name') or {}).get('en') or '')
                  for s, p in all_people.items()}

    stats = {'ejected': 0, 'fixed_coauthor': 0, 'no_truth': 0,
             'kept': 0, 'files_changed': 0}
    log = defaultdict(list)  # slug -> list of (action, paper, detail)

    items = list(all_people.items())
    if args.only:
        items = [(args.only, all_people[args.only])]

    for idx, (slug, person) in enumerate(items):
        target_en = slug_to_en.get(slug, '')
        if not target_en:
            continue
        old_pubs = person.get('publications') or []
        if not old_pubs:
            continue
        new_pubs = []
        changed = False
        print(f'  [{idx+1}/{len(items)}] {slug} ({len(old_pubs)} pubs)',
              file=sys.stderr, flush=True)
        for pub in old_pubs:
            if not isinstance(pub, dict):
                new_pubs.append(pub)
                continue
            authors, source = get_actual_authors(pub, owner_hint=target_en)
            if not authors:
                # Cannot validate — keep as is, count
                stats['no_truth'] += 1
                new_pubs.append(pub)
                continue

            # 1) ownership check — use compatible (initials-tolerant) match.
            # Why looser here: ground-truth APIs (Crossref, arxiv, OpenAlex)
            # often return 'A. Alekseev' style initials; we don't want to
            # eject genuine papers just because the API rendering uses
            # initials. Surname must still equal exactly. For slug binding
            # below we keep the strict matcher to avoid mis-routing.
            if not any(names_compatible(target_en, a) for a in authors):
                stats['ejected'] += 1
                log[slug].append(('EJECT', pub.get('id') or pub.get('title','')[:60],
                                  f'owner={target_en!r} not in {authors}'))
                changed = True
                continue

            # 2) coauthor cleanup
            old_cas = list(pub.get('coauthors') or [])
            new_cas = []
            used_slugs = set()  # slugs already placed
            used_actuals = set()  # actual-author names already accounted for
            # Pre-account for the owner (compatible match, since the API may
            # use initials for the owner too).
            for a in authors:
                if names_compatible(target_en, a):
                    used_actuals.add(a)
                    break

            # First pass: keep slug coauthors that strictly match a real author
            kept_indices = set()
            for i, ca in enumerate(old_cas):
                if not isinstance(ca, str):
                    new_cas.append(ca); kept_indices.add(i); continue
                if is_slug(ca):
                    en = slug_to_en.get(ca, '')
                    matched_actual = None
                    if en:
                        for a in authors:
                            if a in used_actuals:
                                continue
                            if names_match(en, a):
                                matched_actual = a
                                break
                    if matched_actual:
                        new_cas.append(ca)
                        used_slugs.add(ca)
                        used_actuals.add(matched_actual)
                        kept_indices.add(i)

            # Second pass: handle un-kept entries (raw names + bad slugs)
            # Strategy: for each remaining unaccounted real author, try to bind
            # to a known slug; otherwise emit raw name.
            unaccounted = [a for a in authors if a not in used_actuals]
            for a in unaccounted:
                cand_slug = find_correct_slug(a, all_people, used_slugs | {slug})
                if cand_slug:
                    new_cas.append(cand_slug)
                    used_slugs.add(cand_slug)
                else:
                    new_cas.append(a)
                used_actuals.add(a)

            if new_cas != old_cas:
                stats['fixed_coauthor'] += 1
                log[slug].append(('FIX', pub.get('id') or pub.get('title','')[:60],
                                  f'{old_cas} -> {new_cas}'))
                new_pub = dict(pub)
                new_pub['coauthors'] = new_cas
                new_pubs.append(new_pub)
                changed = True
            else:
                stats['kept'] += 1
                new_pubs.append(pub)

        if changed:
            stats['files_changed'] += 1
            person['publications'] = new_pubs

    # Report
    print(f'\nResult: {stats}')
    for slug in sorted(log.keys()):
        actions = log[slug]
        ej = sum(1 for a, _, _ in actions if a == 'EJECT')
        fx = sum(1 for a, _, _ in actions if a == 'FIX')
        print(f'\n  {slug}: eject={ej} fix={fx}')
        for action, paper, detail in actions[:8]:
            print(f'    {action} {paper}  // {detail[:120]}')
        if len(actions) > 8:
            print(f'    ... +{len(actions)-8} more')

    if not args.apply:
        return

    # Write back
    for slug, person in all_people.items():
        if slug not in log:
            continue
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        pubs = person['publications']
        text = replace_block(text, 'publications', render_pubs(pubs))
        published = sum(1 for p in pubs if isinstance(p, dict) and is_published(p))
        preprint = len(pubs) - published
        # Update activity counts
        try:
            p2 = yaml.safe_load(text)
            activity = dict(p2.get('activity') or {})
            activity['total_papers'] = len(pubs)
            activity['published_count'] = published
            activity['preprint_only_count'] = preprint
            text = replace_block(text, 'activity', render_activity(activity))
        except Exception as e:
            print(f'  warn: {slug} activity recompute failed: {e}', file=sys.stderr)
        with open(path, 'w') as f:
            f.write(text)
    print(f'\nApplied changes to {stats["files_changed"]} files.')


if __name__ == '__main__':
    main()
