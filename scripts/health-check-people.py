#!/usr/bin/env python3
"""Comprehensive data-integrity health check for all person YAML files.

Flags suspicious patterns that no-single-API audit can catch:
- publications count = 0 for someone who clearly publishes (declared total_papers > 0
  in personal_notes / activity, or is a known senior figure)
- advisor = null for non-founding-figure (born after ~1950)
- students = [] for senior PI (career has tenured position 10+ years old)
- career_timeline has only education / only one event for active researcher
- research_areas empty
- key_collaborators contains string-typed person (not slug)
- ghost slug references (advisor / student / coauthor slug not in the YAML index)

Output: data/papers/_health-check.md
"""

import os
import re
from collections import defaultdict
from datetime import datetime
import yaml

PEOPLE_DIR = 'data/people'
OUT = 'data/papers/_health-check.md'

NOW_YEAR = datetime.now().year


def load_all():
    out = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        slug = f.replace('.yaml', '')
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            out[slug] = yaml.safe_load(fh) or {}
    return out


def is_likely_active_researcher(p):
    """Born after 1950 OR has a position event in career_timeline."""
    born = p.get('born')
    if isinstance(born, int) and born >= 1950:
        return True
    for ev in (p.get('career_timeline') or []):
        if ev.get('type') == 'position':
            return True
    return False


def has_position_for_at_least(p, years):
    for ev in (p.get('career_timeline') or []):
        if ev.get('type') != 'position':
            continue
        period = ev.get('period') or ''
        m = re.search(r'(\d{4})', period)
        if m and (NOW_YEAR - int(m.group(1))) >= years:
            return True
    return False


def main():
    people = load_all()
    slug_set = set(people.keys())

    issues = defaultdict(list)  # slug -> list of issue strings

    for slug, p in people.items():
        pubs = p.get('publications') or []
        career = p.get('career_timeline') or []
        ras = p.get('research_areas') or []
        kcs = p.get('key_collaborators') or []
        advisor = p.get('advisor')
        students = p.get('students') or []

        # 1. Publications zero for active researcher
        if not pubs and is_likely_active_researcher(p):
            issues[slug].append('publications=0 但看起来是活跃研究者')

        # 2. advisor missing for non-founder
        born = p.get('born')
        if advisor in (None, '', 'null') and isinstance(born, int) and born >= 1955:
            issues[slug].append(f'advisor=null 但 born={born} (1955 后出生应有导师记录)')

        # 3. students=[] for senior PI (10+ years tenured)
        if not students and has_position_for_at_least(p, 15):
            issues[slug].append('students=[] 但已任职 15+ 年，应该有过博士生')

        # 4. career_timeline empty or only one event for active researcher
        if is_likely_active_researcher(p) and len(career) <= 1:
            issues[slug].append(f'career_timeline 仅 {len(career)} 项 (活跃研究者通常有多段经历)')

        # 5. research_areas empty for someone with publications
        if not ras and pubs:
            issues[slug].append(f'research_areas=[] 但有 {len(pubs)} 篇论文')

        # 6. key_collaborators contains non-slug string
        bad_kc = []
        for kc in kcs:
            v = kc.get('person')
            if isinstance(v, str) and v not in slug_set:
                if ' ' in v or '(' in v or any(ord(c) > 127 for c in v):
                    bad_kc.append(v)
        if bad_kc:
            issues[slug].append(f'key_collaborators 含字符串型 person: {bad_kc[:3]}{"..." if len(bad_kc)>3 else ""}')

        # 7. ghost slug references (slug-shaped, not in index)
        ghosts = set()
        if isinstance(advisor, str) and advisor and advisor not in slug_set and '-' in advisor and advisor.islower():
            ghosts.add(f'advisor={advisor}')
        for s in students:
            if isinstance(s, str) and s not in slug_set and '-' in s and s.islower():
                ghosts.add(f'student={s}')
        for kc in kcs:
            v = kc.get('person')
            if isinstance(v, str) and v not in slug_set and '-' in v and v.islower():
                ghosts.add(f'kc={v}')
        if ghosts:
            issues[slug].append(f'ghost slug 引用: {sorted(ghosts)}')

        # 8. Publications coauthors with slug-shaped string not in index
        ghost_co = set()
        for pub in pubs:
            for v in (pub.get('coauthors') or []):
                if isinstance(v, str) and '-' in v and v.islower() and v not in slug_set:
                    ghost_co.add(v)
        if ghost_co:
            issues[slug].append(f'publications.coauthors 含未建档 slug: {sorted(ghost_co)[:5]}{"..." if len(ghost_co)>5 else ""}')

        # 9. published_count = 0 but pubs > 10 (likely arxiv journal_ref under-report)
        activity = p.get('activity') or {}
        pub_c = activity.get('published_count')
        if pub_c == 0 and len(pubs) > 10:
            issues[slug].append(f'published_count=0 但有 {len(pubs)} 篇 → arxiv journal_ref 漏报，待 Crossref 校验')

    # Write report
    lines = ['# 人物 YAML 数据完整性体检\n']
    lines.append(f'扫描 {len(people)} 个人物，发现问题 {sum(len(v) for v in issues.values())} 条 (覆盖 {len(issues)} 人)\n')
    by_kind = defaultdict(list)
    for slug, problems in issues.items():
        for prob in problems:
            kind = prob.split(' ')[0].split('=')[0].split(':')[0]
            by_kind[kind].append((slug, prob))
    lines.append('## 按问题类型分组\n')
    for kind, items in sorted(by_kind.items(), key=lambda x: -len(x[1])):
        lines.append(f'### {kind} ({len(items)} 条)\n')
        for slug, prob in sorted(items):
            lines.append(f'- **{slug}**: {prob}')
        lines.append('')
    lines.append('## 按人物分组\n')
    for slug in sorted(issues):
        lines.append(f'### {slug}\n')
        for prob in issues[slug]:
            lines.append(f'- {prob}')
        lines.append('')

    with open(OUT, 'w') as f:
        f.write('\n'.join(lines))
    print(f'Wrote {OUT}: {len(issues)} people flagged')


if __name__ == '__main__':
    main()
