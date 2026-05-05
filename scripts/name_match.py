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


def is_slug(s):
    return isinstance(s, str) and bool(re.fullmatch(r'[a-z][a-z0-9_-]*', s))


def slug_for_author(author_name, all_people):
    """Return slug iff EXACTLY one slug's English name strictly matches.
    Never use substring; never collapse on initials.
    Returns None when ambiguous or no match."""
    matches = [s for s, p in all_people.items()
               if names_match(((p.get('name') or {}).get('en') or ''), author_name)]
    return matches[0] if len(matches) == 1 else None
