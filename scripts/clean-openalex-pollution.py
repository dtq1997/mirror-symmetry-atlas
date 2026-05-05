#!/usr/bin/env python3
"""Aggressive cleanup of OpenAlex-source publications that are clearly NOT
mathematics, that slipped through the per-profile filter.

Reasons we now know about:
- Some math researchers' OpenAlex profile gets merged with same-name CS / engineering
  authors. The profile-level math ratio can be > 40% even with significant
  pollution if the math person is prolific.
- Per-paper math classification needs to be applied INSIDE the profile too,
  not just at profile-level gating.

Removal rules (all sources=openalex papers; arXiv-sourced papers untouched):
1. DOI prefix in {10.1109/, 10.1145/, 10.1007/978-, 10.1016/} AND venue/title
   contains CS/AI/engineering/translation keywords -> remove
2. Title contains any of: 'krill', 'mapreduce', 'random forest', 'gan ',
   'adversarial network', 'transfer learning', 'particle swarm',
   'crawl', 'recommend system', 'deep learning', 'neural network',
   'big data', 'cloud computing', 'image classific', 'face recogniti',
   'object detect', 'cnn', 'lstm', 'rnn', 'training algorithm',
   'web service', 'iot ', 'wireless sensor', 'cyber', 'malware',
   '【JST', '京大機械翻訳', 'アレロパシー', 'カラマツ' (Japanese translations
   from JST = Japan Science and Technology Agency mass-translated junk)
3. Venue contains: 'IEEE', 'ICDE', 'KDD', 'AAAI', 'NeurIPS', 'CVPR',
   'database', 'data engineering', 'pattern recognition', 'expert systems',
   'softcomputing', 'plant', 'agric', 'biolog', 'medic'
4. Already-known DOI publishers: 'IEEE', 'ACM' for non-math venues

Usage:
  python3 scripts/clean-openalex-pollution.py [--dry-run]
"""

import argparse
import os
import re
import sys
from copy import deepcopy
import yaml

PEOPLE_DIR = 'data/people'

CS_AI_TITLE_PATTERNS = [
    # Specific CS/AI/ML methods (rarely used in pure math)
    'krill', 'mapreduce', 'random forest', 'gan ', 'adversarial net',
    'particle swarm', 'crawl', 'recommend system', 'recommender system',
    'deep learn', 'neural net', 'big data', 'cloud comput',
    'image classific', 'face recogniti', 'object detect',
    ' cnn ', ' lstm ', ' rnn ', 'web service', 'iot ',
    'wireless sensor', 'cyber', 'malware',
    'spatial-spectral', 'hyperspectral',
    'multi-label', 'krill herd', 'data engineering', 'data mining',
    'feature extract', 'feature select', 'sentiment analysis',
    'text classific', 'speech recog', 'natural language process',
    'support vector mach',
    'blackboard network', 'hybrid learning mode',
    'multi-objective evolution', 'genetic algorithm',
    'ultrasonic', 'audio jamming',
    'cable load', 'fault localiz', 'power line',
    # Bio/medical/agriculture
    'enzyme', 'carbonic anhydrase', 'flavonoid', 'sinopodophyl',
    'cephalo', 'audio jamming',
    'dft', 'quantum chemistry dataset',
    'evolutionary algorithm based graph',
    # Japanese mass-translated junk (JST = Japan Sci & Tech Agency)
    '【JST', '京大機械翻訳',
    'アレロパシー', '薬用植物', 'カラマツ',
    'PINUS TABULAEFORMIS', 'LARIX',
    # Heart / clinical
    'electrical activity of heart', 'cardiac',
]

CS_AI_VENUE_PATTERNS = [
    # Big conferences/journals known non-math
    'icde', 'kdd ', 'aaai conference', 'neural information processing systems',
    'cvpr', 'iccv', 'eccv',
    'data engineering', 'pattern recognition letters', 'expert systems',
    'soft computing', 'plant ', 'agriculture', 'biology',
    'medicine', 'cancer', 'crop science', 'forestry',
    'industrial engineering', 'operations management',
    'computer applications', 'information sciences',
    'optics express', 'applied optics',
    'photonics', 'semiconductor', 'materials science',
    'computational intelligence', 'fuzzy', 'evolutionary computation',
    'sustainable', 'agroforestry',
]

# Math venue whitelist — when matched, KEEP regardless of other heuristics.
MATH_VENUE_WHITELIST = [
    'invent', 'annal', 'compositio', 'duke math', 'asterisque',
    'memoir', 'symplect', 'topology', 'geometry & topology',
    'algebraic & geometric topology', 'algebra & number theory',
    'crelle', 'manuscripta math', 'forum math',
    'communications in math', 'commun. math.', 'lett. math.',
    'mathematische ', 'journal of geometry', 'journal of differential',
    'journal of pure and applied alg', 'journal of algebra',
    'journal of number theory',
    'transformation groups', 'compositio math',
    'arxiv', 'preprint', 'progress in math',
    'lecture notes in math', 'memoirs of the ams',
    'pacific journal of math', 'transactions of the amer. math.',
    'proceedings of the amer. math.', 'proceedings of the london math',
    'proceedings of the royal society. a',
    'differential geometry', 'symplectic',
    'mathematische annalen', 'mathematische zeitschrift',
    'frobenius', 'integrable', 'mirror symmetry',
    'communications in mathematical physics',
    'commun. theor. phys', 'theoretical and mathematical physics',
    'reviews in mathematical physics', 'jhep',
    'nuclear physics b', 'springer', 'kluwer',
    'world scientific',
    # Common DOI publishers' math books
    'lecture notes', 'springer briefs',
]


# DOI prefix → publisher hints. We use these together with venue checks
# to avoid mass-deleting Springer/Wiley math books just because
# their DOI starts with 10.1007.
SPRINGER_OR_WILEY_DOI_PREFIXES = ('10.1007/', '10.1002/', '10.1016/')


def is_cs_ai_paper(pub):
    """Return True if this paper looks like CS/AI/agriculture/etc, NOT math."""
    title = (pub.get('title') or '').lower()
    journal = (pub.get('journal') or '').lower()
    doi = (pub.get('doi') or '').lower()

    # Strong whitelist: math venue trumps everything
    for m in MATH_VENUE_WHITELIST:
        if m in journal:
            return False

    # Title-based reject
    for kw in CS_AI_TITLE_PATTERNS:
        if kw.lower() in title:
            return True

    # Venue-based reject
    for kw in CS_AI_VENUE_PATTERNS:
        if kw in journal:
            return True

    # DOI-prefix patterns. 10.1109 = IEEE; 10.1145 = ACM; both used by
    # math too (rarely), so we ALSO require a non-math hint somewhere.
    if doi.startswith(('10.1109/', '10.1145/')):
        # Math at IEEE/ACM exists (e.g. proceedings of FOCS/STOC math papers)
        # but it's rare. If venue is empty + IEEE prefix = almost surely CS.
        if not journal or 'comput' in journal or 'engineer' in journal:
            return True

    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--slug', help='Test on one slug')
    args = parser.parse_args()

    targets = ([args.slug + '.yaml'] if args.slug
                else sorted(f for f in os.listdir(PEOPLE_DIR) if f.endswith('.yaml')))

    total_removed = 0
    total_files = 0
    sample_removed = []

    for fname in targets:
        path = os.path.join(PEOPLE_DIR, fname)
        slug = fname.replace('.yaml', '')
        try:
            with open(path) as f:
                person = yaml.safe_load(f)
        except Exception:
            continue
        pubs = person.get('publications') or []
        if not pubs:
            continue

        kept = []
        removed = []
        for pub in pubs:
            sources = pub.get('sources') or []
            # Only consider papers that came from OpenAlex (preserve all arXiv-sourced)
            if 'arxiv' in sources:
                kept.append(pub)
                continue
            if 'openalex' in sources and is_cs_ai_paper(pub):
                removed.append(pub)
            else:
                kept.append(pub)

        if removed:
            total_files += 1
            total_removed += len(removed)
            for r in removed[:2]:
                sample_removed.append((slug, r.get('year'), r.get('title', '')[:50]))
            if not args.dry_run:
                # Rewrite the publications/activity blocks in YAML text
                with open(path) as f:
                    text = f.read()
                text = rewrite_publications(text, kept, slug)
                with open(path, 'w') as f:
                    f.write(text)

    print(f'{total_files} files, {total_removed} OpenAlex pollution papers '
          f'{"would be removed (dry-run)" if args.dry_run else "removed"}')
    print('\nSample removed:')
    for s, y, t in sample_removed[:30]:
        print(f'  [{s}] [{y}] {t}')


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def coauthor_inline(c):
    s = str(c)
    if s and re.fullmatch(r'[a-z][a-z0-9_-]*', s):
        return s
    return squote(s)


def render_publications(pubs):
    lines = ['publications:']
    for p in pubs:
        pid = p.get('id')
        if not pid:
            continue
        lines.append(f'  - id: {squote(pid)}')
        lines.append(f'    title: {squote(p.get("title") or "")}')
        if p.get('year') is not None:
            lines.append(f'    year: {p["year"]}')
        cas = p.get('coauthors') or []
        if cas:
            lines.append(f'    coauthors: [{", ".join(coauthor_inline(c) for c in cas)}]')
        else:
            lines.append('    coauthors: []')
        if p.get('doi'):
            lines.append(f'    doi: {squote(p["doi"])}')
        if p.get('journal'):
            lines.append(f'    journal: {squote(p["journal"])}')
        if p.get('primary_category'):
            lines.append(f'    primary_category: {p["primary_category"]}')
        if p.get('openalex_id'):
            lines.append(f'    openalex_id: {p["openalex_id"]}')
        if p.get('sources'):
            lines.append(f'    sources: [{", ".join(p["sources"])}]')
        if p.get('no_arxiv'):
            lines.append('    no_arxiv: true')
    return '\n'.join(lines)


def render_activity(activity):
    order = ['total_papers', 'published_count', 'preprint_only_count', 'h_index',
             'mathscinet_citations', 'google_scholar_citations',
             'active_period', 'peak_period', 'phd_students',
             'academic_descendants', 'last_arxiv_paper']
    lines = ['activity:']
    keys = order + [k for k in activity if k not in order]
    for k in keys:
        v = activity.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            lines.append(f'  {k}: {squote(v)}')
        elif isinstance(v, list):
            lines.append(f'  {k}: {v}')
        else:
            lines.append(f'  {k}: {v}')
    return '\n'.join(lines)


def rewrite_publications(text, kept_pubs, slug):
    pub_block = render_publications(kept_pubs)
    pat = re.compile(r'^publications:.*?(?=^[A-Za-z_][\w]*:|\Z)',
                     re.MULTILINE | re.DOTALL)
    if pat.search(text):
        text = pat.sub(lambda _m: pub_block + '\n', text, count=1)
    # Recompute activity counts
    person = yaml.safe_load(text)
    pubs = person.get('publications') or []
    pub_count = sum(1 for p in pubs if p.get('journal') or p.get('doi'))
    pre_count = len(pubs) - pub_count
    activity = dict(person.get('activity') or {})
    activity['total_papers'] = len(pubs)
    activity['published_count'] = pub_count
    activity['preprint_only_count'] = pre_count
    act_block = render_activity(activity)
    pat2 = re.compile(r'^activity:.*?(?=^[A-Za-z_][\w]*:|\Z)',
                      re.MULTILINE | re.DOTALL)
    if pat2.search(text):
        text = pat2.sub(lambda _m: act_block + '\n', text, count=1)
    return text


if __name__ == '__main__':
    main()
