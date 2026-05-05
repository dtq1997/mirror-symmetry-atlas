"""Remove a slug from coauthor lists in OTHER yamls when the corresponding
paper has just been ejected from that slug's own yaml.

Why: canonicalize-publications.py used to auto-bind raw English names to slugs
on both sides. After we eject a paper from slug S's yaml, other yamls may
still list S as a coauthor on that same paper. Those references are the
mirror of the same false attribution and must be replaced with the raw English
name to avoid runtime intersection re-creating bogus edges.

Strategy: for each slug S whose yaml we just cleaned, collect the canonical
ids of papers that are NO LONGER in S.publications. Then walk every other
yaml and, for any pub matching one of those canonical ids that lists S in
coauthors, replace S with the English name (or drop if no English name).
"""
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paper_identity import canonical_doi, canonical_arxiv_id, canonical_title

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'


def keys_for(pub):
    return (
        canonical_doi(pub.get('doi')),
        canonical_arxiv_id(pub.get('id', '')),
        canonical_title(pub.get('title') or ''),
    )


def keys_match(a, b):
    return any(x and y and x == y for x, y in zip(a, b))


def main(target_slugs, apply=False):
    all_people = {}
    for f in sorted(PEOPLE_DIR.glob('*.yaml')):
        all_people[f.stem] = (f, yaml.safe_load(f.read_text()) or {})

    for target in target_slugs:
        if target not in all_people:
            print(f'SKIP unknown slug: {target}')
            continue
        f, d = all_people[target]
        en = ((d.get('name') or {}).get('en') or '').strip()
        own_keys = [keys_for(p) for p in (d.get('publications') or []) if isinstance(p, dict)]

        replacements = 0
        for slug, (g, e) in all_people.items():
            if slug == target:
                continue
            pubs = e.get('publications') or []
            if not pubs:
                continue
            modified = False
            for p in pubs:
                if not isinstance(p, dict):
                    continue
                cas = p.get('coauthors') or []
                if target not in cas:
                    continue
                # Is this paper ALSO in target's yaml? If yes, leave the slug.
                # If not, the coauthor reference is orphaned — replace with raw.
                pk = keys_for(p)
                still_owned = any(keys_match(pk, ok) for ok in own_keys)
                if still_owned:
                    continue
                new_cas = [c if c != target else (en or target) for c in cas]
                if en:
                    p['coauthors'] = new_cas
                    modified = True
                    replacements += 1
                else:
                    p['coauthors'] = [c for c in cas if c != target]
                    modified = True
                    replacements += 1
            if modified and apply:
                g.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=200))
        print(f'{target}: scrubbed {replacements} orphan refs across other yamls')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    apply = '--apply' in sys.argv
    if not args:
        print('usage: scrub-orphan-slug-coauthors.py SLUG [SLUG...] [--apply]')
        sys.exit(1)
    main(args, apply=apply)
