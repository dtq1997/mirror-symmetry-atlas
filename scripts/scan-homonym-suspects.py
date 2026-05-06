"""Heuristic full-database scan for likely-homonym publications.

ONLY high-confidence flags (~95% true positive when matched):
  - title contains hard-non-math keyword (lint already blocks; included for visibility)
  - non-math venue (substring match against curated list; lint blocks)
  - openalex-only AND zero coauthor circle overlap AND year far before
    career start  (combined rule, single-flag is too noisy)

Outputs a sorted markdown report at data/papers/_homonym_review.md.

This is for HUMAN review. Conservative on purpose — single-author early
papers are legit but show no circle overlap, so we DO NOT flag those alone.
"""
import re
import sys
import yaml
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'
OUT = ROOT / 'data/papers/_homonym_review.md'

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from name_match import names_match
from non_math_keywords import is_non_math_title, is_non_math_venue


def earliest_career_year(person):
    yrs = []
    for e in (person.get('career_timeline') or []):
        for m in re.findall(r'\b(19\d{2}|20\d{2})\b', str(e.get('period', ''))):
            yrs.append(int(m))
    return min(yrs) if yrs else None


def main():
    suspects_by_slug = defaultdict(list)
    for f in sorted(PEOPLE_DIR.glob('*.yaml')):
        if f.name.startswith('_'):
            continue
        d = yaml.safe_load(f.read_text()) or {}
        slug = f.stem
        target_en = ((d.get('name') or {}).get('en') or '').strip()
        profile = d.get('identity_profile') or {}
        circle_slugs = set(
            (profile.get('coauthor_circle_core_slugs') or []) +
            (profile.get('coauthor_circle_extended_slugs') or []))
        if d.get('advisor'):
            circle_slugs.add(d['advisor'])
        for s in (d.get('students') or []):
            circle_slugs.add(s)
        circle_names = set(
            (profile.get('coauthor_circle_core_names') or []) +
            (profile.get('coauthor_circle_extended_names') or []))
        career_start = earliest_career_year(d)

        for p in d.get('publications') or []:
            if not isinstance(p, dict):
                continue
            flags = []
            srcs = p.get('sources') or []
            cas = p.get('coauthors') or []
            slug_cas = set(c for c in cas if isinstance(c, str)
                          and re.fullmatch(r'[a-z][a-z0-9-]*', c))

            # Flag 1: title hard-non-math (lint already blocks)
            t = is_non_math_title(p.get('title'))
            if t:
                flags.append(f'title:{t}')

            # Flag 2: non-math venue (lint already blocks)
            v = is_non_math_venue(p.get('journal'))
            if v:
                flags.append(f'venue:{v}')

            # Flag 3 (combined high-confidence): openalex-only + no circle
            #         overlap + year >5y before career start.
            # Single-flag versions of these are too noisy. Combined rule
            # catches mazzocco-1990s-nuclear-physics and similar without
            # falsely flagging early career math papers of legit owners.
            is_oa_only = ('openalex' in srcs and 'arxiv' not in srcs)
            no_slug_overlap = bool(circle_slugs) and not (circle_slugs & slug_cas)
            if circle_names:
                shared_name = any(any(names_match(c, cn) for cn in circle_names)
                                  for c in cas if isinstance(c, str))
            else:
                shared_name = False
            no_circle_overlap = no_slug_overlap and not shared_name
            year_predates = (
                career_start
                and isinstance(p.get('year'), int)
                and p['year'] < career_start - 5
            )
            if is_oa_only and no_circle_overlap and year_predates:
                flags.append(f'oa-only+no-circle+year-predates'
                              f'({p["year"]}<{career_start}-5)')

            if flags:
                suspects_by_slug[slug].append({
                    'flags': flags,
                    'id': p.get('id'),
                    'year': p.get('year'),
                    'title': (p.get('title') or '')[:100],
                    'journal': (p.get('journal') or '')[:60],
                    'sources': srcs,
                })

    # Render report
    lines = ['# Homonym review queue', '',
             'Each row = one publication flagged by automated heuristics.',
             '',
             '**Action**: For each entry, decide:',
             '  - DELETE — if it belongs to a homonym (different person)',
             '  - KEEP — if it really is this person (the heuristic was wrong)',
             '  - VERIFY — if uncertain (open arxiv/journal page to check)',
             '',
             'Once decided, edit the yaml directly or add the title to',
             '`scripts/non_math_keywords.py` (if a new keyword class).',
             '']
    total = 0
    for slug, items in sorted(suspects_by_slug.items(),
                                key=lambda x: -len(x[1])):
        if not items:
            continue
        lines.append(f'\n## {slug} ({len(items)} flagged)\n')
        for item in items:
            total += 1
            flags_str = ', '.join(item['flags'])
            lines.append(f"- [{item['year']}] {item['title']}")
            lines.append(f"  - id: `{item['id']}`")
            if item['journal']:
                lines.append(f"  - journal: {item['journal']}")
            lines.append(f"  - flags: {flags_str}")
            lines.append('')
    lines.insert(2, f'Total flagged: **{total}** across {len(suspects_by_slug)} people.')
    lines.insert(3, '')

    OUT.write_text('\n'.join(lines))
    print(f'Wrote {OUT} — {total} flagged across {len(suspects_by_slug)} slugs')


if __name__ == '__main__':
    main()
