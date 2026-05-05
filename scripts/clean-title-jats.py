#!/usr/bin/env python3
"""Clean JATS/MathML XML residue from publication titles.

OpenAlex sometimes returns titles with embedded JATS XML like:
  Genus-2 G-function for <mml:math ...><mml:msup>...</mml:msup></mml:math> orbifolds
We rewrite such titles to:
  Genus-2 G-function for $\\mathbb{P}^1$ orbifolds

Strategy: best-effort regex-based collapse of common JATS patterns.
- <mml:math ...>(content)</mml:math> -> $...$ (LaTeX fragment)
- <mml:msup><mml:mrow>X</mml:mrow><mml:mrow>Y</mml:mrow></mml:msup> -> X^{Y}
- <mml:mi mathvariant="double-struck">P</mml:mi> -> \\mathbb{P}
- Stray <mml:*> tags stripped
- Numeric entities decoded

Usage: python3 scripts/clean-title-jats.py [--dry-run]
"""

import argparse
import os
import re
import sys
import yaml

PEOPLE_DIR = 'data/people'


def clean_title(t):
    if not t or '<' not in t:
        return t
    s = t
    # mathvariant="double-struck">P  ->  \mathbb{P}
    s = re.sub(r'<mml:mi[^>]*mathvariant="double-struck"[^>]*>([^<]+)</mml:mi>',
               r'\\mathbb{\1}', s)
    s = re.sub(r'<mml:mi[^>]*mathvariant="bold"[^>]*>([^<]+)</mml:mi>',
               r'\\mathbf{\1}', s)
    # mml:msup with mrow children -> X^{Y}
    def msup_repl(m):
        inner = m.group(1)
        # Try to extract two mml:mrow blocks
        rows = re.findall(r'<mml:mrow>(.*?)</mml:mrow>', inner, re.DOTALL)
        if len(rows) >= 2:
            base = strip_tags(rows[0])
            sup = strip_tags(rows[1])
            return f'{base}^{{{sup}}}'
        return strip_tags(inner)
    s = re.sub(r'<mml:msup>(.*?)</mml:msup>', msup_repl, s, flags=re.DOTALL)
    # mml:msub -> X_{Y}
    def msub_repl(m):
        inner = m.group(1)
        rows = re.findall(r'<mml:mrow>(.*?)</mml:mrow>', inner, re.DOTALL)
        if len(rows) >= 2:
            return f'{strip_tags(rows[0])}_{{{strip_tags(rows[1])}}}'
        return strip_tags(inner)
    s = re.sub(r'<mml:msub>(.*?)</mml:msub>', msub_repl, s, flags=re.DOTALL)
    # mml:mfrac -> \frac{X}{Y}
    def mfrac_repl(m):
        inner = m.group(1)
        rows = re.findall(r'<mml:mrow>(.*?)</mml:mrow>', inner, re.DOTALL)
        if len(rows) >= 2:
            return f'\\frac{{{strip_tags(rows[0])}}}{{{strip_tags(rows[1])}}}'
        return strip_tags(inner)
    s = re.sub(r'<mml:mfrac>(.*?)</mml:mfrac>', mfrac_repl, s, flags=re.DOTALL)
    # Wrap remaining mml:math contents with $ ... $
    s = re.sub(
        r'<mml:math[^>]*>(.*?)</mml:math>',
        lambda m: f'${strip_tags(m.group(1))}$', s, flags=re.DOTALL
    )
    # Strip any remaining mml:* tags
    s = re.sub(r'</?mml:[^>]+>', '', s)
    # Strip altimg / overflow / xmlns junk that escaped
    s = re.sub(r'altimg="[^"]*"', '', s)
    s = re.sub(r'overflow="[^"]*"', '', s)
    s = re.sub(r'xmlns:mml="[^"]*"', '', s)
    # Generic xml/xhtml tags
    s = re.sub(r'</?[a-zA-Z]+[^>]*>', '', s)
    # Decode entities
    s = s.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    s = s.replace('&quot;', '"').replace('&#x2019;', "'")
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def strip_tags(s):
    return re.sub(r'</?[^>]+>', '', s).strip()


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    total = 0
    files = 0
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith('.yaml'):
            continue
        path = os.path.join(PEOPLE_DIR, f)
        with open(path) as fh:
            text = fh.read()
        if 'mml:' not in text and 'altimg' not in text:
            continue
        # Just regex-replace: title: '...mml...'  -> cleaned
        new_text, n = re.subn(
            r"^(    title:\s*)'((?:[^']|'')*?)'(\s*)$",
            lambda m: m.group(1) + squote(clean_title(m.group(2).replace("''", "'"))) + m.group(3),
            text, flags=re.MULTILINE
        )
        if n == 0:
            continue
        if new_text != text:
            files += 1
            total += n
            if args.dry_run:
                # show diff snippet
                for old, new in zip(re.findall(r"title:\s*'[^']*'", text),
                                     re.findall(r"title:\s*'[^']*'", new_text)):
                    if old != new and 'mml' in old:
                        print(f'  {f}:')
                        print(f'    OLD: {old[:120]}')
                        print(f'    NEW: {new[:120]}')
            else:
                with open(path, 'w') as fh:
                    fh.write(new_text)
    print(f'\n{files} files, {total} title cleanups '
          f'{"(dry-run)" if args.dry_run else "applied"}')


if __name__ == '__main__':
    main()
