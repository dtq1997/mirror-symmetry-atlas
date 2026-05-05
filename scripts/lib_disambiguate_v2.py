#!/usr/bin/env python3
"""Evidence-driven disambiguator: score a candidate paper against an
identity_profile and accept/reject/queue-for-review.

This replaces the keyword-blacklist approach. Decisions are made by matching
verifiable evidence (ORCID, affiliation, year window, coauthor circle, email
domain) against the person's identity profile.

Score scheme (per candidate paper):
  HARD ACCEPT (no scoring needed):
    - ORCID in paper authorships matches identity_profile.orcid

  HARD REJECT (immediate):
    - Target author's name not present in author list at all
    - Year well outside any affiliation period (e.g. born 1990 with paper year 1985)

  SOFT SCORING:
    +20  any author affiliation string matches one of profile.affiliations.institution
         (when the candidate paper is authored by name-match alone, this is the
          single strongest non-ORCID signal)
    +15  any author email domain matches profile.email_domains
    +10  per coauthor in circle_core_names (cap 30)
    +5   per coauthor in circle_extended_names (cap 15)
    +5   year falls within ANY affiliation period
    +3   per research_keyword found in title
    +5   primary_category / venue is a math venue (only when no contamination signals)
    -10  paper venue clearly outside math (chemistry/CS/medicine — using a small
          curated denylist of HARD non-math venues)

  Threshold:
    >= 20  ACCEPT
    < 10   REJECT
    10-19  REVIEW (write to data/papers/_review_queue/<slug>.yaml)

Output:
  - All accepted papers added to publications
  - Review queue file per person listing the borderline cases
  - Rejected logs to /tmp for inspection
"""

import os
import re

# Hard-non-math venues (used only as -10 penalty, not as kill switch).
# Conservative: only listed venues where math content is essentially impossible.
HARD_NONMATH_VENUE_HINTS = [
    'plant ', 'agronomy', 'crop ', 'forestry',
    'cancer', 'tumor', 'oncolog', 'cardiol', 'pathol',
    'biochem', 'enzyme', 'molecular biology',
    'agricultural', 'food chemistry', 'nutrition',
    'ieee transactions on knowledge', 'icde ', 'sigmod',
    'pattern recognition letters', 'expert systems with',
    'soft computing', 'information sciences',
    'photonics', 'semiconductor', 'optoelec',
    'industrial engineering', 'operations management',
]


def score_candidate(paper, profile, target_name, all_people=None):
    """Return (decision, score, evidence) where decision in
    {'accept', 'reject', 'review'}."""
    evidence = {}

    # --- HARD ACCEPT: ORCID match ---
    profile_orcid = profile.get('orcid', '').strip().lower() if profile.get('orcid') else ''
    if profile_orcid:
        for a in (paper.get('authorships') or []):
            cand_orcid = ((a.get('author') or {}).get('orcid') or '').lower()
            if cand_orcid and profile_orcid in cand_orcid:
                return 'accept', 100, {'reason': 'orcid_match', 'orcid': profile_orcid}

    # --- HARD REJECT: target name not in author list ---
    target_low = re.sub(r'[^a-z ]', ' ', (target_name or '').lower()).split()
    target_parts = [p for p in target_low if len(p) > 1]
    name_in_authors = False
    candidate_authors = []
    for a in (paper.get('authorships') or []):
        n = (a.get('author') or {}).get('display_name') or ''
        candidate_authors.append(n)
        nl = re.sub(r'[^a-z ]', ' ', n.lower())
        if target_parts and all(p in nl for p in target_parts):
            name_in_authors = True
    if not name_in_authors:
        return 'reject', 0, {'reason': 'name_not_in_authors'}
    evidence['authors'] = candidate_authors

    # --- HARD REJECT: year impossible relative to affiliations ---
    py = paper.get('publication_year')
    if py:
        # Earliest year across all affiliation periods (parse "YYYY" or "~YYYY")
        affiliations = profile.get('affiliations') or []
        all_years = []
        for aff in affiliations:
            period = aff.get('period') or ''
            for m in re.findall(r'(\d{4})', period):
                all_years.append(int(m))
        if all_years:
            earliest = min(all_years)
            # Allow some grace: PhD students often publish 2-3 years before
            # earliest recorded period if their first arXiv predates official
            # education record.
            if py < earliest - 5:
                return 'reject', 0, {'reason': 'year_before_career', 'paper_year': py,
                                      'earliest_career': earliest}

    score = 0

    # --- AFFILIATION match ---
    affiliations = profile.get('affiliations') or []
    profile_inst_keys = []
    for aff in affiliations:
        inst = aff.get('institution', '')
        if not inst:
            continue
        # institution slug may be "pku-bicmr" — break into searchable tokens
        tokens = re.split(r'[-_/]', inst)
        profile_inst_keys.extend([t for t in tokens if len(t) >= 3])
    profile_inst_keys = list(set(profile_inst_keys))
    aff_matched = []
    for a in (paper.get('authorships') or []):
        if (a.get('author') or {}).get('display_name', '').lower() != '':
            # Check this author's institution strings
            for inst_obj in (a.get('institutions') or []):
                inst_name = (inst_obj.get('display_name') or '').lower()
                for tok in profile_inst_keys:
                    if tok.lower() in inst_name:
                        aff_matched.append(inst_name)
                        break
                if aff_matched and aff_matched[-1] == inst_name:
                    break
    if aff_matched:
        score += 20
        evidence['affiliation_match'] = aff_matched[:3]

    # --- EMAIL domain match (when authorship has email; OpenAlex rarely gives it) ---
    profile_domains = profile.get('email_domains') or []
    for a in (paper.get('authorships') or []):
        # OpenAlex generally strips emails, but corresponding-author email is
        # sometimes present in 'corresponding_author_ids' / extra fields.
        author_obj = a.get('author') or {}
        cand_email = (author_obj.get('email') or '').lower()
        if not cand_email:
            continue
        for d in profile_domains:
            if d.lower() in cand_email:
                score += 15
                evidence['email_match'] = cand_email
                break

    # --- COAUTHOR circle ---
    core_names = set((profile.get('coauthor_circle_core_names') or []))
    ext_names = set((profile.get('coauthor_circle_extended_names') or []))

    def author_name_matches(author_n, ref_n):
        """Strict name equivalence: same set of (>=2-char) tokens, in same order
        partially. This avoids 'Xinxin Wang' falsely matching 'Xin Wang'."""
        an = re.sub(r'[^a-z ]', ' ', author_n.lower()).split()
        rn = re.sub(r'[^a-z ]', ' ', ref_n.lower()).split()
        an = [t for t in an if len(t) > 1]
        rn = [t for t in rn if len(t) > 1]
        if len(an) < 2 or len(rn) < 2:
            return False
        # Each token in ref must appear as a STANDALONE token in author
        # (not as substring). Order: ref's last token (surname) must appear
        # somewhere; ref's first must appear somewhere too.
        for tok in rn:
            if tok not in an:
                return False
        return True

    core_hits, ext_hits = [], []
    for n in candidate_authors:
        nl = re.sub(r'[^a-z ]', ' ', n.lower())
        if target_parts and all(p in nl for p in target_parts):
            continue
        for cn in core_names:
            if author_name_matches(n, cn):
                core_hits.append(n)
                break
        else:
            for en in ext_names:
                if author_name_matches(n, en):
                    ext_hits.append(n)
                    break
    if core_hits:
        delta = min(30, 10 * len(core_hits))
        score += delta
        evidence['coauthor_core'] = core_hits[:5]
    if ext_hits:
        delta = min(15, 5 * len(ext_hits))
        score += delta
        evidence['coauthor_extended'] = ext_hits[:5]

    # --- YEAR within an affiliation period ---
    if py and affiliations:
        for aff in affiliations:
            period = aff.get('period') or ''
            years = re.findall(r'(\d{4})', period)
            if not years:
                continue
            ys = [int(y) for y in years]
            lo = min(ys)
            hi = max(ys) if 'present' not in period else 2100
            if lo - 2 <= py <= hi + 2:
                score += 5
                evidence['year_in_period'] = period
                break

    # --- KEYWORD match in title ---
    title = (paper.get('title') or paper.get('display_name') or '').lower()
    keywords = profile.get('research_keywords') or []
    kw_hits = []
    for kw in keywords:
        if len(kw) < 4:
            continue
        # Match prefix (cohomology -> cohomol, integrable -> integrabl)
        root = kw[:7] if len(kw) >= 7 else kw[:5]
        if root in title:
            kw_hits.append(kw)
    if kw_hits:
        score += min(15, 3 * len(kw_hits))
        evidence['keywords'] = kw_hits[:5]

    # --- VENUE math/non-math ---
    src = (paper.get('primary_location') or {}).get('source') or {}
    venue = (src.get('display_name') or '').lower() if isinstance(src, dict) else ''
    pcat = paper.get('primary_category') or ''
    if pcat.startswith(('math.', 'math-ph', 'nlin.', 'hep-th')):
        score += 5
        evidence['math_category'] = pcat
    elif venue:
        for hint in HARD_NONMATH_VENUE_HINTS:
            if hint in venue:
                score -= 10
                evidence['nonmath_venue'] = venue[:60]
                break
        else:
            # Soft positive for math-looking venues
            if any(w in venue for w in (
                'math', 'invent', 'duke', 'compositio', 'annal',
                'topology', 'symplect', 'commun', 'arxiv',
                'journal of geometry', 'differential', 'algebra',
            )):
                score += 3
                evidence['math_venue'] = venue[:60]

    # --- DECISION ---
    # affiliation alone is unreliable: many universities have multiple same-name
    # researchers (e.g. PKU has both math Liu and CS Liu). Require at least one
    # independent corroborating signal (coauthor, keyword, math venue) for
    # acceptance. Without that the affiliation match is at best a "review".
    independent_signals = sum(1 for k in [
        'coauthor_core', 'coauthor_extended', 'keywords',
        'math_category', 'math_venue', 'email_match',
    ] if k in evidence)

    # Core-coauthor hit is itself decisive when accompanied by another signal,
    # even if total score < 20: a known advisor/student/key-collaborator
    # appearing in the author list almost always identifies the right person.
    if 'coauthor_core' in evidence and (
        'math_category' in evidence or 'math_venue' in evidence
        or 'affiliation_match' in evidence or 'year_in_period' in evidence
    ):
        return 'accept', score, evidence

    if score >= 20 and independent_signals >= 1:
        return 'accept', score, evidence
    if score >= 30 and independent_signals == 0:
        # Extreme score from many same-affiliation hits: reluctantly review,
        # never auto-accept without an independent topic signal.
        return 'review', score, evidence
    if score < 10:
        return 'reject', score, evidence
    return 'review', score, evidence
