"""[Codex] Reject publisher markup left in plain-text bibliography fields.

This is a review gate, not an HTML decoder or a mathematical-title normalizer.
Unicode and TeX stay literal; corrections must be checked against their source.
"""
import html.entities
import re

ENTITY = re.compile(r'&(#(?:[xX][0-9a-fA-F]+|[0-9]+)|[A-Za-z][A-Za-z0-9]+);')
PAIRED_TAG = re.compile(
    r'<((?:[a-z][\w.-]*:)?[a-z][\w.-]*)(?:\s+[^<>]*)?>[\s\S]*?</\1\s*>',
    re.IGNORECASE,
)
SELF_CLOSING_TAG = re.compile(r'<[a-z][\w.:-]*(?:\s+[^<>]*)?\s*/>', re.IGNORECASE)


def text_residue(value):
    if not isinstance(value, str):
        return []
    residues = [match.group() for match in ENTITY.finditer(value)
                if match[1].startswith('#') or match[1] + ';' in html.entities.html5]
    for pattern in (PAIRED_TAG, SELF_CLOSING_TAG):
        residues.extend(match.group() for match in pattern.finditer(value))
    return residues


def publication_text_errors(pub):
    fields = [('title', pub.get('title')), ('journal', pub.get('journal'))]
    fields += [(f'coauthors[{i}]', name)
               for i, name in enumerate(pub.get('coauthors') or [])]
    return [f'{field}: encoded entity or markup {residue!r}; review the source text'
            for field, value in fields for residue in text_residue(value)]
