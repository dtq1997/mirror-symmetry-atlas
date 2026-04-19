#!/usr/bin/env python3
"""Match acknowledgement text to registered people slugs.

Input : data/derived/raw-acks.jsonl
Output:
  data/derived/acknowledgements.yaml    # all matches (source, target, count, papers)
  data/derived/ack-candidates.yaml      # high-freq external names (≥3 occurrences)
  data/derived/ack-stats.json           # summary stats

Strategy (conservative, prefers precision over recall):
  1. Full-name match ("Si Li", "Boris Dubrovin")  — high confidence
  2. Initial + surname ("B. Dubrovin")            — only if surname is UNIQUE among registered people
  3. Chinese names in zh field                    — exact substring in ack text

The ack text is cleaned of LaTeX commands before matching to avoid false
positives from things like `\cite{Li}`.
"""

import os, re, json, yaml, glob, collections, unicodedata
from collections import defaultdict, Counter

PEOPLE_DIR = "data/people"
RAW_FILE = "data/derived/raw-acks.jsonl"
OUT_EDGES = "data/derived/acknowledgements.yaml"
OUT_CANDIDATES = "data/derived/ack-candidates.yaml"
OUT_STATS = "data/derived/ack-stats.json"


# ---------- LaTeX cleaning ----------

def clean_latex(s: str) -> str:
    """Strip LaTeX commands & braces, keep letters/punctuation/spaces."""
    # Remove \cite{...}, \ref{...}, \label{...}
    s = re.sub(r"\\(?:cite|ref|label|eqref|pageref)\s*\*?\s*\{[^}]*\}", " ", s)
    # Remove \command[opt]{arg} keeping arg
    s = re.sub(r"\\[a-zA-Z]+\s*\*?\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", r"\1", s)
    # Remove remaining \command
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)
    # Remove remaining braces
    s = s.replace("{", " ").replace("}", " ")
    # Collapse whitespace
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ---------- Name variants ----------

def _norm_hyphen(s: str) -> str:
    """Normalize a name chunk: 'Si-Qi' / 'SiQi' / 'Si Qi' all map to 'siqi'."""
    return re.sub(r"[\s\-'\.]+", "", s).lower()


def _first_variants(first: str):
    """Given 'Siqi', produce regex alternatives for 'Si-Qi', 'Si Qi', 'Siqi', 'S.-Q.', 'S. Q.', 'S.Q.'."""
    alts = {re.escape(first)}
    # Try to split Pinyin syllables (rough heuristic: consecutive lowercase blocks after a capital)
    # For 'Siqi' → split into 'Si' 'qi' → variants: 'Si-qi', 'Si qi', 'Si-Qi', 'SiQi'
    m = re.match(r"^([A-Z][a-z]+)([a-z]+)$", first)
    if m:
        a, b = m.group(1), m.group(2)
        # Si, qi  → also Qi
        B = b[0].upper() + b[1:]
        alts.add(re.escape(a) + r"[\-\s]" + re.escape(B))
        alts.add(re.escape(a) + r"[\-\s]" + re.escape(b))
        alts.add(re.escape(a) + re.escape(B))  # SiQi
        alts.add(re.escape(a[0]) + r"\.?\s*[\-]?\s*" + re.escape(B[0]) + r"\.?")  # S.-Q. / S.Q. / S Q
    # Hyphenated already? e.g. 'Si-Qi' → also 'Siqi' 'SiQi'
    if "-" in first:
        parts = first.split("-")
        if all(re.match(r"^[A-Z][a-z]+$", p) or re.match(r"^[a-z]+$", p) for p in parts):
            concat = "".join(parts)
            alts.add(re.escape(concat))
            alts.add(re.escape(concat.lower()))
            alts.add(re.escape(" ".join(parts)))
    return alts


def _last_variants(last: str):
    """Last names: handle 'Zhang-Ju' ↔ 'Zhangju' etc."""
    alts = {re.escape(last)}
    if "-" in last:
        concat = "".join(last.split("-"))
        alts.add(re.escape(concat))
    # Also 'Zhangju' → 'Zhang-Ju'
    m = re.match(r"^([A-Z][a-z]+)([a-z]+)$", last)
    if m:
        a, b = m.group(1), m.group(2)
        B = b[0].upper() + b[1:]
        alts.add(re.escape(a) + r"[\-\s]" + re.escape(B))
    return alts


def name_variants_en(en_name: str):
    """Generate English-name match variants.

    Handles 'FirstName LastName' and 'LastName FirstName' (Chinese style).
    Handles 'Si-Qi' / 'SiQi' / 'Siqi' / 'Si Qi' equivalences.
    """
    en_name = en_name.strip()
    en_name = re.sub(r"\([^)]*\)", "", en_name).strip()
    parts = en_name.split()
    parts = [p for p in parts if p and not (len(p) <= 2 and p.endswith("."))]
    if len(parts) < 2:
        return None
    first = parts[0]
    last = parts[-1]

    fvs = _first_variants(first)
    lvs = _last_variants(last)

    first_alt = "(?:" + "|".join(fvs) + ")"
    last_alt = "(?:" + "|".join(lvs) + ")"

    # Full name: FirstName [middle] LastName
    full_re = re.compile(
        r"\b" + first_alt + r"(?:\s+[A-Z]\.?)*\s+" + last_alt + r"\b"
    )
    # Chinese order: LastName FirstName (e.g., "Liu Siqi")
    reversed_re = re.compile(
        r"\b" + last_alt + r"\s+" + first_alt + r"\b"
    )
    # "LastName, FirstName" format
    comma_re = re.compile(
        r"\b" + last_alt + r",\s+" + first_alt + r"\b"
    )
    # Initial + surname: "S. Liu", "S.Q. Liu", "S.-Q. Liu"
    first_initial = re.escape(first[0])
    initial_re = re.compile(
        r"\b" + first_initial + r"\.?(?:\s*[\-]?\s*[A-Z]\.?)*\s+" + last_alt + r"\b"
    )
    surname_re = re.compile(r"\b" + last_alt + r"\b")
    return {
        "full": full_re,
        "reversed": reversed_re,
        "comma": comma_re,
        "initial": initial_re,
        "surname": surname_re,
        "surname_str": last,
        "surname_norm": _norm_hyphen(last),
        "first": first,
        "first_norm": _norm_hyphen(first),
    }


def name_variants_zh(zh_name: str):
    """Chinese name — exact substring."""
    if not zh_name:
        return None
    # strip whitespace
    return zh_name.strip()


# ---------- Build registry ----------

def load_people():
    people = {}
    for f in sorted(os.listdir(PEOPLE_DIR)):
        if not f.endswith(".yaml"):
            continue
        slug = f[:-5]
        with open(os.path.join(PEOPLE_DIR, f)) as fh:
            try:
                p = yaml.safe_load(fh) or {}
            except Exception:
                continue
        en = (p.get("name") or {}).get("en", "")
        zh = (p.get("name") or {}).get("zh", "")
        people[slug] = {"en": en, "zh": zh}
    return people


def build_matchers(people):
    """For each slug build a match spec; also build a surname→slugs map to
    disambiguate initial-matches."""
    matchers = {}
    surname_to_slugs = defaultdict(list)
    for slug, names in people.items():
        v = name_variants_en(names["en"]) if names["en"] else None
        zh = name_variants_zh(names["zh"]) if names["zh"] else None
        matchers[slug] = {"en": v, "zh": zh}
        if v:
            surname_to_slugs[v["surname_norm"]].append(slug)
    return matchers, surname_to_slugs


# ---------- External name harvest ----------

# Pattern to harvest candidate full-name mentions in ack text.
# Matches "FirstName [M.] LastName" with capitalized words.
EXTERNAL_NAME_RE = re.compile(
    r"\b([A-Z][a-z]+(?:[-'][A-Z][a-z]+)?)"  # First
    r"(?:\s+[A-Z]\.?)*"                      # middle initials
    r"\s+([A-Z][a-z]+(?:[-'][A-Z][a-z]+)?)"  # Last
    r"\b"
)
# Words that commonly appear but are not names
NAME_STOPWORDS = {
    # Pronouns / grammatical
    "The", "This", "We", "Our", "Their", "His", "Her", "Its", "They", "Them", "These", "Those", "All",
    "During", "Part", "Much", "When", "While", "Where", "If", "After", "Before", "Also",
    # Doc structure
    "Acknowledgments", "Acknowledgements", "Thanks", "Thank",
    "Professor", "Prof", "Dr", "Sir", "Mr", "Ms", "Mrs",
    # Institution words (any of these as first word → skip)
    "University", "Universities", "Institute", "Institutes", "Center", "Centre", "Centers",
    "Department", "School", "College", "Research", "Science", "Sciences", "Foundation",
    "Grant", "Grants", "Program", "Programme", "Project", "Projects",
    "Fellowship", "Fellowships", "Laboratory", "Labs",
    "Natural", "National", "Chinese", "China", "American", "European", "British",
    "Italian", "German", "French", "Russian", "Japanese", "Korean",
    "Academy", "Society", "Ministry", "Union", "Commission", "Council",
    "Max", "Marie", "Van", "De", "La", "Le", "El", "Saint", "St",
    "Royal", "Imperial", "Federal", "State", "Central", "Eastern", "Western",
    "Mathematical", "Physical", "Theoretical", "Applied", "Pure", "Fundamental",
    "Integrable", "Young", "Advanced", "Open", "New", "Old",
    "Quantum", "Non", "Stochastic", "Complex", "Real",
    "Simons", "Leverhulme",
    # City/country name words (first-word starter; 2-word city names like "Hong Kong")
    "Hong", "New", "San", "Los", "Santa", "Tel", "Abu", "South", "North",
    "United", "People's", "Peoples", "Republic",
    # Award/institute names that look like "First Last"
    "Penn", "Brown", "Stony", "Johns", "George", "Jean",  # ambiguous given names often appearing in "XX State" etc.
}

# Second-word stopwords (skip if last word is one of these)
NAME_LAST_STOPWORDS = {
    "Kong", "York", "Francisco", "Angeles", "Diego", "Barbara", "Clara",  # city halves
    "Science", "Sciences", "Mathematics", "Physics", "Engineering",
    "Technology", "University", "Institute", "Centre", "Center", "Foundation",
    "Society", "Union", "Ministry", "Republic", "Fellowship", "Grant", "Program",
    "State", "Kingdom", "Nations", "Studies", "Research", "Systems",
    "Academy", "College", "School", "Department", "Committee", "Commission",
    "Planck", "Curie",  # "Max Planck", "Marie Curie"
    "Scientists", "Award", "Prize", "Medal",
    "Field", "Fields", "Theory", "Theories", "Dynamics", "Equations", "Linear",
}


# ---------- Main matching ----------

def main():
    people = load_people()
    matchers, surname_to_slugs = build_matchers(people)

    # Load raw acks
    records = []
    with open(RAW_FILE) as fh:
        for line in fh:
            records.append(json.loads(line))

    # edges[(source_slug, target_slug)] = {count, papers: [arxiv_ids]}
    edges = defaultdict(lambda: {"count": 0, "papers": []})
    # Candidates: external_name -> [arxiv_ids]
    candidates = defaultdict(list)

    for r in records:
        ack_raw = r["ack_text"]
        ack = clean_latex(ack_raw)
        authors = r["paper_authors"]  # who wrote the paper = WHO is acknowledging
        if not authors:
            continue  # Can't assign direction without knowing author
        arxiv_id = r["arxiv_id"]

        matched_slugs = set()

        for slug, m in matchers.items():
            if slug in authors:
                continue  # skip self
            hit = False
            # EN full name match (forward, reversed, comma — all high-confidence)
            if m["en"]:
                if (m["en"]["full"].search(ack)
                        or m["en"]["reversed"].search(ack)
                        or m["en"]["comma"].search(ack)):
                    hit = True
                # Initial+surname: accept only if surname unique
                elif surname_to_slugs.get(m["en"]["surname_norm"], []) == [slug]:
                    if m["en"]["initial"].search(ack):
                        hit = True
                    # surname-only also acceptable when unique AND surname is distinctive (>=4 chars)
                    elif len(m["en"]["surname_str"]) >= 4 and m["en"]["surname"].search(ack):
                        hit = True
            # ZH name match
            if not hit and m["zh"] and m["zh"] in ack_raw:
                hit = True

            if hit:
                matched_slugs.add(slug)

        # Build edges: each author ack's each matched person
        for a in authors:
            for target in matched_slugs:
                if a == target:
                    continue
                key = (a, target)
                edges[key]["count"] += 1
                edges[key]["papers"].append(arxiv_id)

        # Harvest external name candidates
        for m in EXTERNAL_NAME_RE.finditer(ack):
            first, last = m.group(1), m.group(2)
            if first in NAME_STOPWORDS or last in NAME_STOPWORDS:
                continue
            if last in NAME_LAST_STOPWORDS:
                continue
            full = f"{first} {last}"
            # skip if already matched to a registered slug
            skip = False
            for slug in matched_slugs:
                mm = matchers[slug]["en"]
                if mm and (_norm_hyphen(mm["surname_str"]) == _norm_hyphen(last) or _norm_hyphen(mm["first"]) == _norm_hyphen(first)):
                    skip = True
                    break
            # Also skip if the candidate name itself matches a registered slug
            # (e.g., registered person not picked up as author but mentioned)
            if not skip:
                for slug, mm_outer in matchers.items():
                    mm2 = mm_outer["en"]
                    if not mm2:
                        continue
                    if (_norm_hyphen(mm2["surname_str"]) == _norm_hyphen(last) and
                        _norm_hyphen(mm2["first"]) == _norm_hyphen(first)):
                        skip = True
                        break
            if skip:
                continue
            candidates[full].append(arxiv_id)

    # Convert edges to YAML structure
    edges_list = []
    for (source, target), info in sorted(edges.items()):
        edges_list.append({
            "source": source,
            "target": target,
            "type": "acknowledgement",
            "weight": info["count"],
            "papers": sorted(set(info["papers"])),
        })

    # Split: strong (≥2) vs single (1)
    strong = [e for e in edges_list if e["weight"] >= 2]
    single = [e for e in edges_list if e["weight"] == 1]

    # Write edges file (only ≥2)
    with open(OUT_EDGES, "w") as fh:
        yaml.safe_dump(
            {
                "meta": {
                    "note": "Auto-generated from arXiv LaTeX acknowledgements. weight = count of papers where source acknowledges target. Threshold ≥2.",
                    "single_count": len(single),
                    "strong_count": len(strong),
                },
                "edges": strong,
                "single_mentions": single,  # kept for detail-page display
            },
            fh,
            allow_unicode=True,
            sort_keys=False,
        )

    # Write candidates (≥3)
    cand_sorted = sorted(
        [(n, len(ids), sorted(set(ids))) for n, ids in candidates.items() if len(ids) >= 3],
        key=lambda x: -x[1],
    )
    with open(OUT_CANDIDATES, "w") as fh:
        yaml.safe_dump(
            {
                "meta": {
                    "note": "External full-name mentions in ack sections, frequency ≥3. Candidates for future slug registration.",
                    "total": len(cand_sorted),
                },
                "candidates": [
                    {"name": n, "count": c, "papers": p} for n, c, p in cand_sorted
                ],
            },
            fh,
            allow_unicode=True,
            sort_keys=False,
        )

    stats = {
        "papers_processed": len(records),
        "total_edges": len(edges_list),
        "strong_edges": len(strong),
        "single_edges": len(single),
        "candidates": len(cand_sorted),
    }
    with open(OUT_STATS, "w") as fh:
        json.dump(stats, fh, indent=2, ensure_ascii=False)

    print("Stats:", json.dumps(stats, indent=2))
    print("Wrote", OUT_EDGES, OUT_CANDIDATES, OUT_STATS)


if __name__ == "__main__":
    main()
