#!/usr/bin/env python3
"""Extract Acknowledgements section and grant numbers from arXiv LaTeX sources.

Reads data/papers/sources/{arxiv_id}/*.tex, writes
data/derived/raw-acks.jsonl with one JSON per paper:
{arxiv_id, ack_text, grants: [...], paper_authors: [...]}

paper_authors are slug(s) of YAML-registered authors (based on publications
index) — used later to know WHO is acknowledging.
"""

import os, re, json, yaml, glob, sys

SOURCES_DIR = "data/papers/sources"
PEOPLE_DIR = "data/people"
OUT_DIR = "data/derived"
OUT_FILE = os.path.join(OUT_DIR, "raw-acks.jsonl")

# Section headers that usually mark the ack block.
ACK_HEADER_RE = re.compile(
    r"""
    (?:
        \\section\*?\s*\{\s*Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \\subsection\*?\s*\{\s*Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \\paragraph\s*\{\s*Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \\chapter\*?\s*\{\s*Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \{\s*\\bf\s+Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \{\s*\\sc\s+Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \\noindent\s*\\textbf\s*\{\s*Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \\textbf\s*\{\s*Acknowledg(?:e?)ment(?:s)?[^}]*\}
      | \\begin\{acknowledg(?:e?)ments?\}
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Where the ack section ends
END_RE = re.compile(
    r"""
    (?:
        \\section\*?\s*\{
      | \\chapter\*?\s*\{
      | \\bibliographystyle\b
      | \\bibliography\b
      | \\begin\{thebibliography\}
      | \\end\{document\}
      | \\appendix\b
      | \\end\{acknowledg(?:e?)ments?\}
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Grant patterns
GRANT_PATTERNS = [
    # NSFC: 8-digit numbers (11931009, 12171254, etc.); historical 5-7 digit too
    (r"\b(?:NSFC|National\s+Natural\s+Science\s+Foundation(?:\s+of\s+China)?)[^\.;]{0,200}?\b(?:No\.?|Grant(?:s)?|#)?\s*([0-9]{5,13})", "NSFC"),
    # China Postdoctoral Science Foundation
    (r"\bChina\s+Postdoctoral\s+Science\s+Foundation[^\.;]{0,200}?\b(?:No\.?|Grant(?:s)?)?\s*([0-9A-Z]{6,15})", "CPSF"),
    # Tsinghua Postdoc
    (r"\bTsinghua\s+(?:University\s+)?(?:Initiative\s+Scientific\s+Research\s+Program|Dushi\s+Program|Postdoctoral?)[^\.;]{0,200}?([0-9]{5,15})", "Tsinghua"),
    # DFG
    (r"\bDFG[^\.;]{0,200}?\b(?:CRC|SFB|TRR|GRK)?\s*([A-Z]{0,4}[\-\s]?[0-9]{3,8})", "DFG"),
    # ERC
    (r"\bERC\s+(?:Advanced|Starting|Consolidator|Synergy)?\s*(?:Grant)?[^\.;]{0,100}?(?:No\.?|#)?\s*([0-9]{5,10})", "ERC"),
    # NSF (US)
    (r"\bNSF\s+(?:DMS|grant|Grant|No\.?|#)?[^\.;]{0,80}?([A-Z]{0,4}[\-\s]?[0-9]{5,10})", "NSF"),
    # Simons Foundation
    (r"\bSimons\s+(?:Foundation|Collaboration|Fellowship)[^\.;]{0,200}?(?:No\.?|#|Grant)?\s*([0-9]{5,10})", "Simons"),
    # JSPS
    (r"\bJSPS\s+(?:KAKENHI|Grant)[^\.;]{0,100}?([A-Z0-9]{5,15})", "JSPS"),
    # 973/863 计划
    (r"\b(?:973|863)\s+Program[^\.;]{0,100}?(?:No\.?)?\s*([A-Z0-9]{5,15})", "China973"),
    # Fundamental Research Funds (中央高校基本科研业务费)
    (r"\bFundamental\s+Research\s+Funds[^\.;]{0,200}?([A-Z0-9]{5,20})", "FundResFunds"),
]


def read_tex_files(paper_dir):
    """Concatenate all .tex files in a paper directory."""
    chunks = []
    for f in sorted(os.listdir(paper_dir)):
        if not f.endswith(".tex"):
            continue
        path = os.path.join(paper_dir, f)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
            # Skip HTML error pages
            if content.lstrip().startswith(("<!DOCTYPE", "<html")):
                continue
            chunks.append(content)
        except Exception:
            pass
    return "\n".join(chunks)


def strip_comments(text):
    """Remove LaTeX line comments (% not preceded by \\)."""
    return re.sub(r"(?<!\\)%.*", "", text)


def extract_ack(text):
    """Find the ack section; return string or None."""
    text = strip_comments(text)
    m = ACK_HEADER_RE.search(text)
    if not m:
        return None
    start = m.end()
    # Find the end
    end_match = END_RE.search(text, start)
    end = end_match.start() if end_match else min(len(text), start + 5000)
    ack = text[start:end].strip()
    # Cap at 3000 chars — long "acks" are likely false positives
    return ack[:3000] if ack else None


def extract_grants(ack_text):
    """Find grant references within the ack."""
    found = []
    if not ack_text:
        return found
    for pat, kind in GRANT_PATTERNS:
        for m in re.finditer(pat, ack_text, flags=re.IGNORECASE | re.DOTALL):
            num = m.group(1) if m.groups() else m.group(0)
            num = re.sub(r"\s+", "", num)
            if num:
                found.append({"agency": kind, "number": num})
    # Dedupe
    seen = set()
    uniq = []
    for g in found:
        k = (g["agency"], g["number"])
        if k not in seen:
            seen.add(k)
            uniq.append(g)
    return uniq


def build_paper_author_index():
    """arxiv_id → list of slugs (authors registered in YAML)."""
    idx = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith(".yaml"):
            continue
        slug = f[:-5]
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            try:
                p = yaml.safe_load(fh) or {}
            except Exception:
                continue
        for pub in p.get("publications") or []:
            aid = (pub.get("id") or "").strip()
            if aid and not aid.startswith("["):
                idx.setdefault(aid, []).append(slug)
    return idx


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    author_idx = build_paper_author_index()
    dirs = sorted(os.listdir(SOURCES_DIR))
    total = 0
    with_ack = 0
    with_grant = 0
    records = []
    for arxiv_id in dirs:
        paper_dir = os.path.join(SOURCES_DIR, arxiv_id)
        if not os.path.isdir(paper_dir):
            continue
        total += 1
        text = read_tex_files(paper_dir)
        if not text:
            continue
        ack = extract_ack(text)
        if not ack:
            continue
        with_ack += 1
        grants = extract_grants(ack)
        if grants:
            with_grant += 1
        records.append({
            "arxiv_id": arxiv_id,
            "paper_authors": author_idx.get(arxiv_id, []),
            "ack_text": ack,
            "grants": grants,
        })

    with open(OUT_FILE, "w") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Processed {total} papers")
    print(f"  with ack section: {with_ack}")
    print(f"  with grant info:  {with_grant}")
    print(f"Wrote {OUT_FILE}")


if __name__ == "__main__":
    main()
