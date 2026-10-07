"""Canonical paper identity functions. All comparisons go through here.

Why a separate module: every script (canonicalize, dedup, fix-name-pollution,
data.ts logic) needs to compare titles/dois consistently. Drift between local
normalize_title implementations is the recurring SSOT-violation bug.
"""

import re
import unicodedata


def fold_accents(s):
    """é → e, ü → u, etc."""
    return ''.join(c for c in unicodedata.normalize('NFKD', s)
                    if not unicodedata.combining(c))


def canonical_title(t):
    """Lowercase, accent-folded, LaTeX-stripped, alnum-tokenized title key.

    Used for matching same paper across data sources where authors may have
    formatted the same title differently (e.g. "Brézin" vs "Brezin", "Q-Schur"
    vs "Q-schur", with vs without LaTeX).

    Steps:
    1. NFKD + drop combining marks (é → e)
    2. Lowercase
    3. Strip LaTeX math delimiters $...$ AND keep their content as plain words
       (so "$W$-type" → "w type")
    4. Drop common LaTeX commands (\mathbb, \mathbf, etc.) keeping their args
    5. Drop XML/HTML tags
    6. Replace any non-alnum non-space with space
    7. Collapse whitespace
    """
    if not t:
        return ''
    s = fold_accents(t).lower()
    # Strip LaTeX commands like \mathbb{P} → P
    s = re.sub(r'\\[a-z]+\{([^}]*)\}', r'\1', s)
    s = re.sub(r'\\[a-z]+', ' ', s)
    # Strip math delimiters but keep content
    s = re.sub(r'\$([^$]*)\$', r'\1', s)
    # Drop XML/HTML
    s = re.sub(r'<[^>]+>', ' ', s)
    # Alphanumeric tokens only
    s = re.sub(r'[^a-z0-9 ]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def canonical_doi(d):
    """Lowercase, strip URL prefix. None for empty / arxiv self-DOI."""
    if not d:
        return None
    s = str(d).lower().strip()
    s = re.sub(r'^https?://(dx\.)?doi\.org/', '', s)
    s = re.sub(r'^doi:\s*', '', s)
    if not s or s.startswith('10.48550/arxiv.'):
        return None
    return s


def canonical_arxiv_id(pid):
    """If pid is an arxiv id (not doi:/openalex:/cr:), return it without v-suffix."""
    if not pid:
        return None
    pid = re.sub(r'^https?://(?:export\.)?arxiv\.org/abs/', '', str(pid).strip(), flags=re.I)
    pid = re.sub(r'^arxiv:\s*', '', pid, flags=re.I)
    pid = re.sub(r'v\d+$', '', pid)
    if pid.startswith(('doi:', 'openalex:', 'cr:')):
        return None
    if re.fullmatch(r'\d{4}\.\d{4,5}|\d{7}|[a-z][a-z.-]*/\d{7}', pid, flags=re.I):
        return pid
    return None


def paper_identity_keys(pub):
    """Return tuple of (real_doi, arxiv_id, title_canonical) for matching.
    Each component can be None. Two pubs are 'same paper' iff ANY non-None
    pair of corresponding components is equal."""
    return (
        canonical_doi(pub.get('doi') or (pub.get('id', '')[4:] if pub.get('id', '').startswith('doi:') else None)),
        canonical_arxiv_id(pub.get('id', '')),
        canonical_title(pub.get('title') or ''),
    )


def papers_match(a_keys, b_keys):
    for i in range(3):
        if a_keys[i] and b_keys[i] and a_keys[i] == b_keys[i]:
            return True
    return False
