"""Eject publications whose year predates the person's career start by >3 years.

Targets the false attributions from canonicalize-publications.py's old name-match
logic (a master's student with 1998-2021 papers cannot be the same Ao Li who
wrote them). Conservative: only ejects when year is clearly impossible.
"""
import os
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'

YEAR_RE = re.compile(r'\b(19\d{2}|20\d{2})\b')


def earliest_career_year(person):
    years = []
    for e in person.get('career_timeline') or []:
        ys = [int(m) for m in YEAR_RE.findall(str(e.get('period', '')))]
        years.extend(ys)
    return min(years) if years else None


def is_junior_stub(person):
    """Junior researchers (students/postdocs/stubs starting >= 2020) must show
    a clear link to their advisor's circle for any paper to be plausible."""
    tags = set(person.get('tags') or [])
    earliest = earliest_career_year(person)
    return ((tags & {'stub', 'student'}) and earliest and earliest >= 2020)


def core_circle_slugs(person):
    profile = person.get('identity_profile') or {}
    return set(profile.get('coauthor_circle_core_slugs') or [])


def main(apply=False):
    total_ejected = 0
    files_changed = 0
    for f in sorted(PEOPLE_DIR.glob('*.yaml')):
        text = f.read_text()
        d = yaml.safe_load(text) or {}
        slug = f.stem
        earliest = earliest_career_year(d)
        if earliest is None:
            continue
        cutoff = earliest - 3
        circle = core_circle_slugs(d) | {d.get('advisor')} - {None, ''}
        junior = is_junior_stub(d)
        pubs = d.get('publications') or []
        keep = []
        ejected = []
        for p in pubs:
            if not isinstance(p, dict):
                keep.append(p); continue
            y = p.get('year')
            reason = None
            if isinstance(y, int) and y < cutoff:
                reason = f'year {y} < cutoff {cutoff}'
            elif junior and circle:
                # require at least one core-circle slug among coauthors
                cas = set(p.get('coauthors') or [])
                if not (cas & circle):
                    reason = f'junior stub: no core circle ({sorted(circle)}) among coauthors'
            if reason:
                ejected.append((p, reason))
            else:
                keep.append(p)
        if not ejected:
            continue
        print(f'\n{slug} (career starts {earliest}, cutoff {cutoff}): '
              f'eject {len(ejected)}/{len(pubs)}')
        for p, reason in ejected:
            print(f"  - [{p.get('year')}] {p.get('title','')[:90]}  ({reason})")
        total_ejected += len(ejected)
        files_changed += 1
        if apply:
            d['publications'] = keep
            # Recompute activity counts
            published = sum(1 for p in keep if isinstance(p, dict) and (p.get('journal') or p.get('doi')))
            preprint = len(keep) - published
            act = d.setdefault('activity', {})
            act['total_papers'] = len(keep)
            act['published_count'] = published
            act['preprint_only_count'] = preprint
            f.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False, width=200))
    print(f'\n{"APPLIED" if apply else "DRY-RUN"}: {total_ejected} pubs across {files_changed} files')


if __name__ == '__main__':
    main(apply=('--apply' in sys.argv))
