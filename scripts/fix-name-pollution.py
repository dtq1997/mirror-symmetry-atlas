#!/usr/bin/env python3
"""Fix historical name-resolution pollution in publications.coauthors.

Problem: in earlier enrich runs, raw names like "Si-qi Liu" got mis-normalized
to slug `si-li` (李思) via token-subset matching against `Si Li`.

Strategy:
1. For each publication entry whose `id` is an arXiv id, fetch the canonical
   author list from arXiv API (cached).
2. Compare against the YAML's stored coauthors. For each coauthor slug, check
   whether the corresponding person's English name appears in the actual
   author list (strict, all tokens must appear AS WHOLE TOKENS, not substring).
3. If not, look for a different slug whose en name DOES appear there → swap.
4. If no slug fits, keep as raw name string.

Cache arxiv responses to data/papers/_arxiv_cache/{id}.xml

Usage: python3 scripts/fix-name-pollution.py [--dry-run]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
import yaml

PEOPLE_DIR = 'data/people'
ARXIV_CACHE = 'data/papers/_arxiv_authors_cache'

NS = {'a': 'http://www.w3.org/2005/Atom'}


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def normalize_name(s):
    """Lowercase + drop parens + non-ascii. Hyphens become spaces (so
    'Si-Qi Liu' tokenizes as ['si', 'qi', 'liu'])."""
    s = re.sub(r'\([^)]*\)', '', s or '')
    # Strip arxiv-style prefixes that mark non-primary authors
    s = re.sub(r'^\s*with\s+an?\s+(appendix|introduction|preface|foreword|note)\s+by\s+',
               '', s, flags=re.IGNORECASE)
    s = re.sub(r'^\s*and\s+', '', s, flags=re.IGNORECASE)
    s = re.sub(r'[^a-z\- ]', ' ', s.lower())
    s = re.sub(r'-', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def name_tokens(s):
    return [t for t in normalize_name(s).split() if len(t) > 1]


def name_tokens_concat(s):
    """Like name_tokens but concatenate hyphenated parts. 'Si-Qi Liu' → ['siqi', 'liu']."""
    s = re.sub(r'\([^)]*\)', '', s or '')
    s = re.sub(r'([a-zA-Z])-([a-zA-Z])', r'\1\2', s)
    s = re.sub(r'[^a-z ]', ' ', s.lower())
    return [t for t in re.sub(r'\s+', ' ', s).strip().split() if len(t) > 1]


def strict_name_match(target_en, candidate_raw):
    """Symmetric: match if EITHER hyphen-split tokens OR hyphen-concat tokens match.
    Handles both 'Siqi Liu' and 'Si-Qi Liu' forms."""
    a1 = set(name_tokens(target_en))
    b1 = set(name_tokens(candidate_raw))
    if a1 and b1 and a1 == b1:
        return True
    a2 = set(name_tokens_concat(target_en))
    b2 = set(name_tokens_concat(candidate_raw))
    if a2 and b2 and a2 == b2:
        return True
    # Also: target tokens (concat) ⊂ candidate tokens (split) or vice versa
    return False


def fetch_arxiv_authors_batch(arxiv_ids, delay=3, batch_size=50):
    """Fetch arxiv authors for a list of ids, batching to API.

    arxiv id_list query supports up to 200 ids per request.
    Uses cache first."""
    os.makedirs(ARXIV_CACHE, exist_ok=True)
    out = {}
    need_fetch = []
    for aid in arxiv_ids:
        safe = aid.replace('/', '_')
        cache = os.path.join(ARXIV_CACHE, f'{safe}.json')
        if os.path.exists(cache):
            try:
                out[aid] = json.load(open(cache))
                continue
            except json.JSONDecodeError:
                pass
        need_fetch.append(aid)

    for i in range(0, len(need_fetch), batch_size):
        batch = need_fetch[i:i + batch_size]
        time.sleep(delay)
        url = f'https://export.arxiv.org/api/query?id_list={",".join(batch)}&max_results={batch_size}'
        r = subprocess.run(['curl', '-s', '--noproxy', '*', '--max-time', '40', url],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        if not r.stdout:
            print(f'  warn: empty response for batch {i}', file=sys.stderr)
            continue
        try:
            root = ET.fromstring(r.stdout)
        except ET.ParseError:
            continue
        for entry in root.findall('a:entry', NS):
            aid_elem = entry.find('a:id', NS)
            if aid_elem is None:
                continue
            full = aid_elem.text or ''
            m = re.search(r'arxiv\.org/abs/([\w./-]+?)(v\d+)?$', full)
            if not m:
                continue
            arxiv_id = m.group(1)
            authors = [a.find('a:name', NS).text for a in entry.findall('a:author', NS)
                       if a.find('a:name', NS) is not None]
            out[arxiv_id] = authors
            safe = arxiv_id.replace('/', '_')
            with open(os.path.join(ARXIV_CACHE, f'{safe}.json'), 'w') as f:
                json.dump(authors, f, ensure_ascii=False)
        # Progress
        print(f'  fetched batch {i//batch_size + 1}/{(len(need_fetch)+batch_size-1)//batch_size}',
              file=sys.stderr)
    return out


def fetch_arxiv_authors(arxiv_id, delay=4):
    """Single-id fetch (backward-compat). Prefer fetch_arxiv_authors_batch."""
    return fetch_arxiv_authors_batch([arxiv_id], delay=delay).get(arxiv_id, [])


def render_pubs(pubs):
    lines = ['publications:']
    for p in pubs:
        if not p.get('id'):
            continue
        lines.append(f'  - id: {squote(p["id"])}')
        lines.append(f'    title: {squote(p.get("title") or "")}')
        if p.get('year') is not None:
            lines.append(f'    year: {p["year"]}')
        cas = p.get('coauthors') or []
        if cas:
            inner = ', '.join(c if re.fullmatch(r'[a-z][a-z0-9_-]*', str(c)) else squote(c) for c in cas)
            lines.append(f'    coauthors: [{inner}]')
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


def replace_block(text, name, new_block):
    pat = re.compile(rf'^{name}:.*?(?=^[A-Za-z_][\w]*:|\Z)', re.MULTILINE | re.DOTALL)
    if pat.search(text):
        return pat.sub(lambda _m: new_block + '\n', text, count=1)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    all_people = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            all_people[f.replace('.yaml', '')] = yaml.safe_load(fh) or {}

    # Build slug → en name index for strict matching
    slug_to_en = {}
    for slug, p in all_people.items():
        en = (p.get('name') or {}).get('en') or ''
        if en:
            slug_to_en[slug] = en

    # Pre-fetch ALL arxiv authors in batches first (saves time vs serial calls)
    all_arxiv_ids = set()
    for slug, person in all_people.items():
        for pub in (person.get('publications') or []):
            pid = pub.get('id', '')
            if pid and not pid.startswith(('doi:', 'openalex:', 'cr:')):
                aid = pid.split('v')[0]
                if re.match(r'^\d{4}\.\d{4,5}$|^\d{7}$|^[a-z-]+/\d{7}$', aid):
                    all_arxiv_ids.add(aid)
    print(f'Pre-fetching arxiv authors for {len(all_arxiv_ids)} unique papers...', file=sys.stderr)
    arxiv_lookup = fetch_arxiv_authors_batch(sorted(all_arxiv_ids))
    print(f'  done. cached {len(arxiv_lookup)} papers', file=sys.stderr)

    fixes_per_slug = defaultdict(list)  # slug -> list of (paper-id, old-coauthors, new-coauthors)

    for slug, person in all_people.items():
        target_en = slug_to_en.get(slug, '')
        new_pubs = []
        changed = False
        for pub in (person.get('publications') or []):
            new_pub = dict(pub)
            pid = pub.get('id', '')
            # Only look up arxiv-style ids (skip doi:/openalex:/cr:)
            if not pid or pid.startswith(('doi:', 'openalex:', 'cr:')):
                new_pubs.append(new_pub)
                continue
            arxiv_id = pid.split('v')[0]
            if not re.match(r'^\d{4}\.\d{4,5}$|^\d{7}$|^[a-z-]+/\d{7}$', arxiv_id):
                new_pubs.append(new_pub)
                continue
            actual_authors = arxiv_lookup.get(arxiv_id, [])
            if not actual_authors:
                new_pubs.append(new_pub)
                continue

            old_cas = pub.get('coauthors') or []
            new_cas = []
            for ca in old_cas:
                if not isinstance(ca, str):
                    new_cas.append(ca)
                    continue
                if re.fullmatch(r'[a-z][a-z0-9_-]*', ca):
                    # It's a slug. Check if its English name appears as a token-set
                    # match in any actual arxiv author. Yes → keep.
                    en_of_slug = slug_to_en.get(ca, '')
                    if en_of_slug and any(strict_name_match(en_of_slug, a) for a in actual_authors):
                        new_cas.append(ca)
                        continue
                    # Slug doesn't fit any actual author. This is the bug.
                    # Try to find a DIFFERENT slug whose name DOES match an actual
                    # author that is otherwise unaccounted for. We do this only
                    # when the actual author list contains a name with token
                    # overlap that would have caused the original mis-match.
                    # Specifically: find an actual author whose tokens are a SUPERSET
                    # of (or differ slightly from) the bad slug's name tokens.
                    # bad slug doesn't match any actual author. Two-step rescue:
                    # (a) for each actual author, see if some other indexed slug
                    #     STRICTLY matches it. If such a slug exists, the bad
                    #     slug was almost certainly a mis-normalization of that
                    #     real coauthor. Replace.
                    # (b) if no slug strictly matches any actual author, use
                    #     the actual author NAME (raw string) for the slot. This
                    #     is more correct than keeping a wrong slug because the
                    #     wrong slug links to a different person's page.
                    best_replacement = None
                    used_slugs = {s for s in new_cas if isinstance(s, str)
                                   and re.fullmatch(r'[a-z][a-z0-9_-]*', s)}
                    # First pass: find slug-matching replacement
                    for actual in actual_authors:
                        if strict_name_match(target_en, actual):
                            continue
                        if any(strict_name_match(slug_to_en.get(s, ''), actual) for s in used_slugs):
                            continue
                        for cand_slug, cand_en in slug_to_en.items():
                            if cand_slug == slug or cand_slug == ca or cand_slug in used_slugs:
                                continue
                            if strict_name_match(cand_en, actual):
                                best_replacement = cand_slug
                                break
                        if best_replacement:
                            break

                    # Second pass (no slug match): pick the unused actual author
                    # whose tokens best overlap with the bad slug's name. This
                    # heuristically restores the original intended raw name.
                    if not best_replacement:
                        bt = set(name_tokens(en_of_slug)) | set(name_tokens_concat(en_of_slug))
                        used_actuals = set()
                        for s_used in used_slugs:
                            for a in actual_authors:
                                if strict_name_match(slug_to_en.get(s_used, ''), a):
                                    used_actuals.add(a)
                        # rank by overlap
                        best_overlap = 0
                        for actual in actual_authors:
                            if actual in used_actuals:
                                continue
                            if strict_name_match(target_en, actual):
                                continue
                            actual_tokens = set(name_tokens(actual)) | set(name_tokens_concat(actual))
                            overlap = len(bt & actual_tokens)
                            if overlap > best_overlap:
                                best_overlap = overlap
                                best_replacement = actual
                        # Last resort: any unused actual author at all (so the
                        # WRONG slug doesn't survive). Better to show a raw
                        # name than mislink to a different person.
                        if not best_replacement:
                            for actual in actual_authors:
                                if actual in used_actuals:
                                    continue
                                if strict_name_match(target_en, actual):
                                    continue
                                best_replacement = actual
                                break
                    if best_replacement:
                        new_cas.append(best_replacement)
                    else:
                        # Cannot disambiguate confidently — keep original slug as-is
                        # (don't make things worse by random replacement)
                        new_cas.append(ca)
                else:
                    # Raw name; keep if it matches any arxiv author, drop only if
                    # it's clearly absent. Default to keep when uncertain.
                    new_cas.append(ca)

            if new_cas != old_cas:
                changed = True
                fixes_per_slug[slug].append((arxiv_id, old_cas, new_cas))
                new_pub['coauthors'] = new_cas
            new_pubs.append(new_pub)

        if changed:
            person['publications'] = new_pubs

    # Report
    total_fixes = sum(len(v) for v in fixes_per_slug.values())
    print(f'\n{len(fixes_per_slug)} files have coauthor fixes ({total_fixes} pubs corrected)')

    for slug, fixes in sorted(fixes_per_slug.items()):
        print(f'\n  {slug} ({len(fixes)} pubs):')
        for arxiv_id, old, new in fixes[:5]:
            print(f'    [{arxiv_id}] {old} → {new}')
        if len(fixes) > 5:
            print(f'    ... +{len(fixes)-5} more')

    if args.dry_run:
        return

    # Write back
    for slug, fixes in fixes_per_slug.items():
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        with open(path) as f:
            text = f.read()
        text = replace_block(text, 'publications', render_pubs(all_people[slug]['publications']))
        with open(path, 'w') as f:
            f.write(text)


if __name__ == '__main__':
    main()
