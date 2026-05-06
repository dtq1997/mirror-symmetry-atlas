"""Single source of truth for "are these two name strings the same person?"

NEVER use substring matching. The pattern `all(part in candidate for part in
target.split())` catastrophically binds 'Ao Li' to 'Chien-Hao Liu' (because
'ao' and 'li' both occur as substrings) and 'Zhang Qing' to 'Zhang Qingsheng'
(because 'qing' is a prefix of 'qingsheng'). Every script that compares names
MUST go through `names_match` here.

Equivalence rule: token sets must be EQUAL after one of two normalizations:
  (a) hyphen → space:    'Si-Qi Liu' → {si, qi, liu}
  (b) hyphen → empty:    'Si-Qi Liu' → {siqi, liu}

Hits 'Si-Qi Liu' = 'Siqi Liu' (rule b) and rejects 'Zhang Qing' = 'Zhang
Qingsheng' (neither rule). Tokens of length <2 (initials) are dropped — we
never auto-bind on initials alone.
"""
import re


def _variants(s):
    s = re.sub(r'\([^)]*\)', '', s or '')
    s = re.sub(r'[^a-zA-Z\- ]', ' ', s).lower()
    a = set(t for t in re.sub(r'-', ' ', s).split() if len(t) > 1)
    b = set(t for t in re.sub(r'([a-z])-([a-z])', r'\1\2', s).split() if len(t) > 1)
    return a, b


def names_match(a_name, b_name):
    a1, a2 = _variants(a_name)
    b1, b2 = _variants(b_name)
    if a1 and b1 and a1 == b1:
        return True
    if a2 and b2 and a2 == b2:
        return True
    return False


def names_compatible(yaml_name, candidate_name):
    """Looser match for OWNERSHIP CHECK ONLY (never for slug binding).

    Accepts initials when surname is identical and given-name initials are a
    prefix-compatible match. Examples:
       'Anton Alekseev' ~ 'A. Alekseev'      → True
       'Si-Qi Liu'      ~ 'S.-Q. Liu'        → True
       'Ao Li'          ~ 'A. Liu'           → False (different surname)
       'Anton Alekseev' ~ 'Andrey Alekseev'  → False (full given names differ)

    Rule: STRICT match wins outright. Otherwise: same surname (last
    >=2-char token), and each given-name token in `yaml_name` must either
    EQUAL or be initials-compatible with the corresponding token in
    `candidate_name`. 'Initials-compatible' means a single letter (with or
    without trailing dot/hyphen) matching the first letter of the full word.
    """
    if names_match(yaml_name, candidate_name):
        return True

    def _toks(s):
        s = re.sub(r'\([^)]*\)', '', s or '')
        s = s.lower().replace('.', ' ')
        # Replace hyphens between letters with spaces too for token extraction.
        s = re.sub(r'([a-z])-([a-z])', r'\1 \2', s)
        s = re.sub(r'[^a-z ]', ' ', s)
        return [t for t in s.split() if t]

    a = _toks(yaml_name)
    b = _toks(candidate_name)
    if len(a) < 2 or len(b) < 2:
        return False
    # Surname = last >=2-char token (if all are 1-char, take last).
    def _surname(toks):
        for t in reversed(toks):
            if len(t) >= 2:
                return t
        return toks[-1] if toks else ''

    if _surname(a) != _surname(b):
        return False

    # Given-name compatibility: pair up the given tokens. If counts differ,
    # require the shorter side to be initials-only and prefix-compatible.
    a_given = a[:-1] if len(a[-1]) >= 2 else a
    b_given = b[:-1] if len(b[-1]) >= 2 else b
    if not a_given or not b_given:
        return False

    def _compat(x, y):
        if x == y:
            return True
        if len(x) == 1 and y.startswith(x):
            return True
        if len(y) == 1 and x.startswith(y):
            return True
        return False

    # Pair up by position. Allow length mismatch only when the shorter side is
    # entirely single-char initials.
    if len(a_given) != len(b_given):
        short, long = (a_given, b_given) if len(a_given) < len(b_given) else (b_given, a_given)
        if not all(len(t) == 1 for t in short):
            return False
        # match short[i] to long[i] (or long[i:i+...] for hyphenated initials)
        for i, t in enumerate(short):
            if i >= len(long):
                return False
            if not _compat(t, long[i]):
                return False
        return True

    return all(_compat(x, y) for x, y in zip(a_given, b_given))


def is_slug(s):
    return isinstance(s, str) and bool(re.fullmatch(r'[a-z][a-z0-9_-]*', s))


def slug_for_author(author_name, all_people):
    """Return slug iff EXACTLY one slug's English name strictly matches.
    Never use substring; never collapse on initials.
    Returns None when ambiguous or no match."""
    matches = [s for s, p in all_people.items()
               if names_match(((p.get('name') or {}).get('en') or ''), author_name)]
    return matches[0] if len(matches) == 1 else None
