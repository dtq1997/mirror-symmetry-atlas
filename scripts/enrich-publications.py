#!/usr/bin/env python3
"""Enrich a person YAML's publications field with disambiguated arXiv candidates.

Adds new high-score papers, fills journal/doi from arXiv journal_ref, and
computes activity.published_count / activity.preprint_only_count.

Usage:
  python3 scripts/enrich-publications.py <slug> [--threshold 10] [--write]
  python3 scripts/enrich-publications.py --all [--threshold 10] [--write]

Without --write, prints a dry-run summary of what would change.
"""

import argparse
import os
import sys
import yaml
from copy import deepcopy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_disambiguate import (
    load_all_people, fetch_candidates_for_person, disambiguate, normalize_name,
    keyword_signal,
)

PEOPLE_DIR = 'data/people'


def _name_token_variants(s):
    """Return two token sets for `s`:
      a: hyphen-as-space    'Si-Qi Liu' → {'si','qi','liu'}
      b: hyphen-concatenated 'Si-Qi Liu' → {'siqi','liu'}
    Used for symmetric strict matching that handles both 'Si-Qi Liu' and
    'Siqi Liu' romanization styles WITHOUT falling back to substring (which
    is what mis-bound 'Chien-Hao Liu' to slug `li-ao` because 'ao' and 'li'
    happen to be substrings of 'chien-hao liu')."""
    s = re.sub(r'\([^)]*\)', '', s or '')
    s = re.sub(r'[^a-zA-Z\- ]', ' ', s).lower()
    a = set(t for t in re.sub(r'-', ' ', s).split() if len(t) > 1)
    b = set(t for t in re.sub(r'([a-z])-([a-z])', r'\1\2', s).split() if len(t) > 1)
    return a, b


def _names_match_strict(a_name, b_name):
    """True iff token-set OR concatenated-token-set are equal between the
    two names. NEVER substring."""
    a1, a2 = _name_token_variants(a_name)
    b1, b2 = _name_token_variants(b_name)
    if a1 and b1 and a1 == b1:
        return True
    if a2 and b2 and a2 == b2:
        return True
    return False


def slugify_coauthor(author_name, all_people):
    """Map an arXiv author name to a known slug ONLY when the names match
    strictly (token set equality). Otherwise return the cleaned raw name.

    History: a previous substring-based match catastrophically bound
    'Chien-Hao Liu' to slug `li-ao` because 'ao' and 'li' both appear as
    substrings of 'chien-hao liu'. Substring matching is forbidden here."""
    for slug, p in all_people.items():
        en = (p.get('name') or {}).get('en', '')
        if en and _names_match_strict(en, author_name):
            return slug
    return normalize_name(author_name)


def enrich_person(slug, person, all_people, threshold=10, fetch_delay=4, target_self=None):
    target_name = target_self or (person.get('name') or {}).get('en', '')
    if not target_name:
        return None, 'no name'

    candidates = fetch_candidates_for_person(target_name, max_results=300,
                                              math_only=True, delay=fetch_delay)
    if not candidates:
        return None, 'no candidates'

    # Auto-detect unique name: when name is rare (low candidate count and
    # every candidate trivially contains the target name in author list),
    # known coauthor signal isn't necessary - drop threshold.
    effective_threshold = threshold
    # Relax threshold ONLY when (a) candidate pool is small enough that name
    # is likely unique, (b) person has metadata, AND (c) topic coherence:
    # at least 25% of candidates' titles match this person's research areas.
    # Without (c), we'd hoover up papers from a different homonym in a
    # different field — e.g. yang-yi (Julia sets) accidentally absorbing
    # 70 hep-th papers from a different "Yi Yang".
    research_areas = person.get('research_areas') or []
    has_metadata = bool(research_areas) or bool(person.get('key_collaborators'))
    topic_matches = (
        sum(1 for c in candidates if keyword_signal(c.get('title', ''), research_areas))
        if research_areas else 0
    )
    topic_coherent = (research_areas and topic_matches / max(1, len(candidates)) >= 0.25)
    if len(candidates) < 100 and has_metadata and topic_coherent:
        effective_threshold = max(5, threshold - 5)

    existing = {(p.get('id') or '').split('v')[0]: p
                for p in (person.get('publications') or [])}

    # Score & accept
    accepted = []
    for c in candidates:
        score, signals = disambiguate(person, c, all_people, target_name=target_name)
        if score < effective_threshold:
            continue
        # Per-paper safety in relaxed mode: even though the overall person
        # is topic-coherent, each individual paper must have at least one
        # non-trivial signal beyond bare math-cat (a known coauthor or a
        # keyword hit). Otherwise homonym contamination at the paper level
        # slips through. E.g. liu-siqi accidentally inherited STOC paper
        # 2111.11316 ("Testing thresholds..." by a different Siqi Liu in CS).
        if effective_threshold < threshold:
            if not (signals.get('known_coauthors') or signals.get('keywords')):
                continue
        # Drop self from coauthors
        coauthors = []
        for a in c['authors']:
            if normalize_name(a).lower() == normalize_name(target_name).lower():
                continue
            coauthors.append(slugify_coauthor(a, all_people))
        entry = {
            'id': c['id'],
            'title': c['title'],
            'year': c['year'],
            'coauthors': coauthors,
        }
        if c.get('doi'):
            entry['doi'] = c['doi']
        if c.get('journal_ref'):
            entry['journal'] = c['journal_ref']
        if c.get('primary_category'):
            entry['primary_category'] = c['primary_category']
        accepted.append((c['id'], entry, score, signals))

    accepted_ids = {aid for aid, *_ in accepted}

    # Merge: keep existing manual fields where present, add new
    merged = []
    seen = set()
    for aid, entry, _, _ in accepted:
        prev = existing.get(aid)
        if prev:
            # Preserve any human-edited fields not in entry
            merged_entry = {**entry, **{k: v for k, v in prev.items() if v not in (None, '', [])}}
            # But always overwrite journal/doi from arxiv fresh data if newly available
            if entry.get('journal'):
                merged_entry['journal'] = entry['journal']
            if entry.get('doi'):
                merged_entry['doi'] = entry['doi']
            if entry.get('primary_category'):
                merged_entry['primary_category'] = entry['primary_category']
            merged.append(merged_entry)
        else:
            merged.append(entry)
        seen.add(aid)

    # Keep existing publications that didn't show up in math query (could be old / cross-cat)
    kept_extra = []
    for aid, prev in existing.items():
        if aid not in accepted_ids:
            kept_extra.append(prev)

    merged.sort(key=lambda x: -(x.get('year') or 0))

    published_count = sum(1 for p in merged + kept_extra
                          if p.get('journal') or p.get('doi'))
    preprint_count = (len(merged) + len(kept_extra)) - published_count

    return {
        'merged_publications': merged,
        'kept_extra': kept_extra,
        'new_count': len([1 for aid, *_ in accepted if aid not in existing]),
        'existing_count': len(existing),
        'final_count': len(merged) + len(kept_extra),
        'published_count': published_count,
        'preprint_count': preprint_count,
    }, None


def _yaml_squote(s):
    """Wrap string in YAML single quotes (no escape interpretation)."""
    return "'" + str(s).replace("'", "''") + "'"


def _format_publications_block(pubs):
    """Render a publications list using the project's existing 2-space-indent dash style.
    Uses single quotes throughout so backslash-laden LaTeX titles round-trip safely."""
    lines = ['publications:']
    for p in pubs:
        pid = p.get('id')
        if not pid:
            continue
        lines.append(f'  - id: {_yaml_squote(pid)}')
        lines.append(f'    title: {_yaml_squote(p.get("title") or "")}')
        lines.append(f'    year: {p.get("year")}')
        coauthors = p.get('coauthors') or []
        if coauthors:
            inner = ', '.join(_coauthor_inline(c) for c in coauthors)
            lines.append(f'    coauthors: [{inner}]')
        else:
            lines.append('    coauthors: []')
        if p.get('doi'):
            lines.append(f'    doi: {_yaml_squote(p["doi"])}')
        if p.get('journal'):
            lines.append(f'    journal: {_yaml_squote(p["journal"])}')
        if p.get('primary_category'):
            lines.append(f'    primary_category: {p["primary_category"]}')
    return '\n'.join(lines)


def _coauthor_inline(c):
    """Render a coauthor for an inline flow-style list. Slugs (lowercase + dash) bare,
    raw names quoted."""
    s = str(c)
    if s and s.replace('-', '').replace('_', '').isalnum() and s.islower():
        return s
    return _yaml_squote(s)


def _format_activity_block(activity):
    lines = ['activity:']
    order = ['total_papers', 'published_count', 'preprint_only_count', 'h_index',
             'mathscinet_citations', 'google_scholar_citations',
             'active_period', 'peak_period', 'phd_students',
             'academic_descendants', 'last_arxiv_paper']
    keys = order + [k for k in activity if k not in order]
    for k in keys:
        v = activity.get(k)
        if v is None:
            continue
        if isinstance(v, str):
            lines.append(f'  {k}: {_yaml_squote(v)}')
        else:
            lines.append(f'  {k}: {v}')
    return '\n'.join(lines)


def _replace_block(text, block_name, new_block):
    """Replace a top-level YAML block (lines starting with `block_name:` until
    the next top-level key) with `new_block`. If absent, append before the next
    sensible top-level key."""
    import re
    pattern = re.compile(rf'(^{block_name}:.*?)(?=^[A-Za-z_][\w]*:|\Z)',
                         re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        # Use a lambda to avoid backreference interpretation in new_block
        return pattern.sub(lambda _m: new_block + '\n', text, count=1)
    # Append before sources: or external_ids: or end of file
    for anchor in ['sources:', 'external_ids:', 'links:', 'personal_notes:']:
        m = re.search(rf'^{anchor}', text, re.MULTILINE)
        if m:
            return text[:m.start()] + new_block + '\n' + text[m.start():]
    return text.rstrip() + '\n' + new_block + '\n'


def write_back(slug, person, result):
    new_publications = result['merged_publications'] + result['kept_extra']
    activity = dict(person.get('activity') or {})
    activity['total_papers'] = result['final_count']
    activity['published_count'] = result['published_count']
    activity['preprint_only_count'] = result['preprint_count']

    path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
    with open(path, 'r') as f:
        text = f.read()

    text = _replace_block(text, 'publications', _format_publications_block(new_publications))
    text = _replace_block(text, 'activity', _format_activity_block(activity))

    with open(path, 'w') as f:
        f.write(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('slug', nargs='*')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--threshold', type=int, default=10)
    parser.add_argument('--delay', type=int, default=4)
    parser.add_argument('--write', action='store_true', help='Write changes back to YAML')
    args = parser.parse_args()

    all_people = load_all_people()
    targets = list(all_people.keys()) if args.all else (args.slug or [])
    if not targets:
        print('Specify slug or --all', file=sys.stderr)
        sys.exit(1)

    summary = []
    for i, slug in enumerate(targets):
        person = all_people.get(slug)
        if not person:
            print(f'[{i+1}/{len(targets)}] {slug} NOT FOUND', file=sys.stderr)
            continue
        print(f'[{i+1}/{len(targets)}] {slug} ...', file=sys.stderr)
        result, err = enrich_person(slug, person, all_people,
                                     threshold=args.threshold, fetch_delay=args.delay)
        if err:
            print(f'  skipped: {err}', file=sys.stderr)
            continue
        summary.append({
            'slug': slug,
            'before': result['existing_count'],
            'after': result['final_count'],
            'new': result['new_count'],
            'published': result['published_count'],
            'preprint': result['preprint_count'],
        })
        print(f"  {result['existing_count']} -> {result['final_count']} ({result['new_count']} new); "
              f"{result['published_count']} published / {result['preprint_count']} preprint",
              file=sys.stderr)
        if args.write:
            write_back(slug, person, result)

    print('\n=== SUMMARY ===')
    print(f"{'slug':<25} {'before':>7} {'after':>7} {'+new':>5} {'pub':>5} {'arxiv':>5}")
    for s in summary:
        print(f"{s['slug']:<25} {s['before']:>7} {s['after']:>7} {s['new']:>5} {s['published']:>5} {s['preprint']:>5}")


if __name__ == '__main__':
    main()
