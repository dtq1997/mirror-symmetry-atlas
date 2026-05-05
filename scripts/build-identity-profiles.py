#!/usr/bin/env python3
"""Build identity_profile for each person YAML.

The identity profile is the **single source of truth** for who this person is,
used by the disambiguator to score candidate papers.

Construction (zero manual input — all from existing YAML data):
- arxiv_author_id: from existing links.arxiv_author or extracted from arXiv abs HTML
- orcid: from existing external_ids.orcid
- openalex_id: from existing external_ids.openalex
- mathgenealogy_id: from existing external_ids.mathgenealogy
- affiliations: from career_timeline (period + institution + role + advisor)
- coauthor_circle: union of {advisor, students, mentors, key_collaborators[].person,
                              all coauthor slugs from existing publications}
- email_domains: derived from career institution (pku.edu.cn for pku etc.)
                 + any explicit emails in the YAML
- research_keywords: from research_areas slugs (kebab-case → keywords)
- coauthor_circle_names: union of (slug → name.en) for all in circle, used
  when a candidate paper's authors are raw names not slugs
- known_paper_ids: arXiv ids of confirmed publications, used as bootstrap

Output: writes identity_profile block back into each YAML, before sources/links.

Usage:
  python3 scripts/build-identity-profiles.py [--dry-run]
"""

import argparse
import os
import re
import sys
import yaml

PEOPLE_DIR = 'data/people'

# institution slug -> email domain hint (best-effort; extend as needed)
INSTITUTION_TO_DOMAIN = {
    'pku': 'pku.edu.cn',
    'pku-bicmr': 'bicmr.pku.edu.cn',
    'tsinghua': 'tsinghua.edu.cn',
    'tsinghua-yau': 'yau.center.tsinghua.edu.cn',
    'sysu': 'mail.sysu.edu.cn',
    'sun-yat-sen': 'mail.sysu.edu.cn',
    'fudan': 'fudan.edu.cn',
    'sjtu': 'sjtu.edu.cn',
    'zju': 'zju.edu.cn',
    'ustc': 'ustc.edu.cn',
    'amss': 'amss.ac.cn',
    'sustech': 'sustech.edu.cn',
    'whu': 'whu.edu.cn',
    'wuhan': 'whu.edu.cn',
    'hust': 'hust.edu.cn',
    'cqu': 'cqu.edu.cn',
    'scu': 'scu.edu.cn',
    'ccnu': 'ccnu.edu.cn',
    'bnu': 'bnu.edu.cn',
    'cas': 'cas.cn',
    'sjtu-cqsc': 'sjtu.edu.cn',
    'westlake': 'westlake.edu.cn',
    'shanghaitech': 'shanghaitech.edu.cn',
    'gbu': 'gbu.edu.cn',
    'bimsa': 'bimsa.cn',
    'pku-bjtu': 'bjtu.edu.cn',
    'cnu': 'cnu.edu.cn',
    'cumtb': 'cumtb.edu.cn',
    'columbia': 'columbia.edu',
    'northwestern': 'northwestern.edu',
    'princeton': 'princeton.edu',
    'mit': 'mit.edu',
    'harvard': 'harvard.edu',
    'stanford': 'stanford.edu',
    'berkeley': 'berkeley.edu',
    'ucla': 'ucla.edu',
    'mich': 'umich.edu',
    'michigan': 'umich.edu',
    'oxford': 'maths.ox.ac.uk',
    'cambridge': 'dpmms.cam.ac.uk',
    'imperial': 'imperial.ac.uk',
    'ucl': 'ucl.ac.uk',
    'ihes': 'ihes.fr',
    'ihp': 'ihp.fr',
    'ens': 'ens.fr',
    'ens-paris': 'ens.fr',
    'sorbonne': 'sorbonne-universite.fr',
    'sissa': 'sissa.it',
    'utokyo': 'ms.u-tokyo.ac.jp',
    'kyoto': 'kurims.kyoto-u.ac.jp',
    'rims': 'kurims.kyoto-u.ac.jp',
    'mpi-bonn': 'mpim-bonn.mpg.de',
    'mpim': 'mpim-bonn.mpg.de',
    'eth': 'math.ethz.ch',
    'epfl': 'epfl.ch',
    'kcl': 'kcl.ac.uk',
    'cnrs': 'math.cnrs.fr',
    'upenn': 'upenn.edu',
    'cmu': 'cmu.edu',
    'cuhk': 'math.cuhk.edu.hk',
    'hkust': 'ust.hk',
    'hku': 'hku.hk',
    'cu-boulder': 'colorado.edu',
}


def load_all():
    out = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            out[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}
    return out


def name_en(person):
    return ((person.get('name') or {}).get('en') or '').strip()


def build_profile(slug, person, all_people):
    profile = {}

    # External ids
    ext = person.get('external_ids') or {}
    if ext.get('orcid'):
        profile['orcid'] = ext['orcid']
    if ext.get('openalex'):
        profile['openalex_id'] = ext['openalex']
    if ext.get('mathgenealogy'):
        profile['mathgenealogy_id'] = ext['mathgenealogy']

    # arxiv author link
    links = person.get('links') or {}
    if links.get('arxiv_author'):
        profile['arxiv_author_url'] = links['arxiv_author']

    # Affiliations from career_timeline
    affs = []
    domains = set()
    for ev in (person.get('career_timeline') or []):
        if ev.get('type') in ('education', 'position', 'visit'):
            inst = ev.get('institution')
            period = ev.get('period')
            if inst:
                aff = {'institution': inst}
                if period:
                    aff['period'] = period
                if ev.get('role'):
                    aff['role'] = ev['role']
                affs.append(aff)
                if inst in INSTITUTION_TO_DOMAIN:
                    domains.add(INSTITUTION_TO_DOMAIN[inst])
    if affs:
        profile['affiliations'] = affs
    if domains:
        profile['email_domains'] = sorted(domains)

    # Coauthor circle. Two layers:
    # - "core" (high signal): advisor + students + mentors + key_collaborators.
    #   These are vetted relationships. Used for the strongest +10 boost.
    # - "extended" (medium signal): coauthors observed in known publications
    #   that themselves have arXiv ids (i.e. confirmed papers in this person's
    #   list). Limited to slugs we can resolve - raw names are dropped because
    #   they may be from the very contamination we're trying to detect.
    core_slugs = set()
    if isinstance(person.get('advisor'), str):
        core_slugs.add(person['advisor'])
    for s in (person.get('students') or []):
        if isinstance(s, str):
            core_slugs.add(s)
    for s in (person.get('mentors') or []):
        if isinstance(s, str):
            core_slugs.add(s)
    for kc in (person.get('key_collaborators') or []):
        v = kc.get('person')
        if isinstance(v, str):
            core_slugs.add(v)
    core_slugs.discard(slug)

    extended_slugs = set()
    for pub in (person.get('publications') or []):
        # Only count coauthors from arXiv-sourced (confirmed) papers
        srcs = pub.get('sources') or ['arxiv']
        if 'arxiv' not in srcs:
            continue
        for ca in (pub.get('coauthors') or []):
            if isinstance(ca, str) and ca in all_people:
                extended_slugs.add(ca)
    extended_slugs.discard(slug)
    extended_slugs -= core_slugs

    # Resolve to names. Only include slugs that are in the people index.
    core_names = set()
    for s in core_slugs:
        if s in all_people:
            en = name_en(all_people[s])
            if en:
                core_names.add(en)
    ext_names = set()
    for s in extended_slugs:
        en = name_en(all_people[s])
        if en:
            ext_names.add(en)

    if core_slugs & set(all_people.keys()):
        profile['coauthor_circle_core_slugs'] = sorted(s for s in core_slugs if s in all_people)
    if core_names:
        profile['coauthor_circle_core_names'] = sorted(core_names)
    if extended_slugs:
        profile['coauthor_circle_extended_slugs'] = sorted(extended_slugs)
    if ext_names:
        profile['coauthor_circle_extended_names'] = sorted(ext_names)

    # Research keywords: from research_areas (slug -> word)
    ras = person.get('research_areas') or []
    if ras:
        keywords = set()
        for r in ras:
            for w in str(r).replace('-', ' ').split():
                if len(w) > 3:
                    keywords.add(w.lower())
        if keywords:
            profile['research_keywords'] = sorted(keywords)

    # Known arxiv paper ids (bootstrap)
    known_ids = []
    for pub in (person.get('publications') or []):
        pid = pub.get('id', '')
        if pid and not pid.startswith(('doi:', 'openalex:')):
            known_ids.append(pid)
    if known_ids:
        profile['known_arxiv_ids'] = known_ids

    return profile


def render_profile_yaml(profile):
    """Render compactly. Avoid pyyaml's default-flow-style overhaul."""
    if not profile:
        return None
    lines = ['identity_profile:']
    for key, value in profile.items():
        if isinstance(value, str):
            lines.append(f'  {key}: {squote(value)}')
        elif isinstance(value, list):
            if not value:
                lines.append(f'  {key}: []')
            elif all(isinstance(x, str) for x in value):
                items = ', '.join(squote(x) if (' ' in x or '/' in x or "'" in x) else x for x in value)
                # If the list is short, inline; else multi-line
                inline = f'[{items}]'
                if len(inline) < 100:
                    lines.append(f'  {key}: {inline}')
                else:
                    lines.append(f'  {key}:')
                    for x in value:
                        lines.append(f'    - {squote(x)}')
            else:
                # list of dicts (affiliations)
                lines.append(f'  {key}:')
                for d in value:
                    first = True
                    for kk, vv in d.items():
                        if first:
                            lines.append(f'    - {kk}: {squote(vv) if isinstance(vv, str) else vv}')
                            first = False
                        else:
                            lines.append(f'      {kk}: {squote(vv) if isinstance(vv, str) else vv}')
    return '\n'.join(lines)


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def insert_profile(text, block):
    """Insert/replace identity_profile block. Place it right after research_areas
    (before advisor) for visibility, or at the top after research_areas."""
    pat = re.compile(r'^identity_profile:.*?(?=^[A-Za-z_][\w]*:|\Z)',
                     re.MULTILINE | re.DOTALL)
    if pat.search(text):
        return pat.sub(lambda _m: block + '\n', text, count=1)
    # Insert before `advisor:` if found, else before `external_ids:`
    for anchor in ['advisor:', 'mentors:', 'students:', 'key_collaborators:',
                   'publications:', 'external_ids:', 'sources:']:
        m = re.search(rf'^{anchor}', text, re.MULTILINE)
        if m:
            return text[:m.start()] + block + '\n' + text[m.start():]
    return text.rstrip() + '\n' + block + '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    all_people = load_all()
    written = 0
    for slug, person in all_people.items():
        profile = build_profile(slug, person, all_people)
        if not profile:
            continue
        block = render_profile_yaml(profile)
        if not block:
            continue
        if args.dry_run:
            print(f'=== {slug} ===')
            print(block)
            print()
            continue
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        new_text = insert_profile(text, block)
        with open(path, 'w') as f:
            f.write(new_text)
        written += 1
    print(f'wrote identity_profile for {written} people')


if __name__ == '__main__':
    main()
