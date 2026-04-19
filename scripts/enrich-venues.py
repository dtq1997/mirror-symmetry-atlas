#!/usr/bin/env python3
"""
Query OpenAlex for each person's publications with venue info, match to
新锐分区表 tiers, and write quality counters back to each person's YAML under
activity: { t1_papers, t2_papers, t3_papers, other_papers, venue_samples }.

Usage:
  python3 scripts/enrich-venues.py [slug1 slug2 ...]   # specific slugs
  python3 scripts/enrich-venues.py --all

Requires `external_ids.openalex` on the person record, OR falls back to name
search (lower quality for common Chinese names).
"""

import sys, json, time, re, urllib.request, urllib.parse
from pathlib import Path
import yaml

DATA = Path(__file__).resolve().parent.parent / "data"
JDIR = DATA / "journals"

# ----- Load tier tables -----
def load_tiers():
    issn_tier = {}  # issn (no dash) -> (tier, subject, rank, name)
    for f in JDIR.glob("ruirui-*.yaml"):
        subject = "math" if "math" in f.name else "physics"
        d = yaml.safe_load(f.read_text())
        tiers_def = d["tiers"]
        def rank_to_tier(r):
            for t, rng in tiers_def.items():
                lo, hi = rng["rank_range"]
                if lo <= r <= hi:
                    return t
            return "T5"
        for row in d["journals"]:
            rank, name, issn, eissn = row
            tier = rank_to_tier(rank)
            for x in (issn, eissn):
                if x:
                    issn_tier[x.replace("-", "").upper()] = (tier, subject, rank, name)
    return issn_tier

ISSN_TIER = load_tiers()
print(f"[tier-db] loaded {len(ISSN_TIER)} ISSN entries", file=sys.stderr)

# ----- OpenAlex -----
def fetch_openalex_author(aid, per_page=200):
    url = f"https://api.openalex.org/works?filter=author.id:{aid}&per-page={per_page}&select=id,display_name,publication_year,primary_location,doi,type,open_access"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "mirror-sym-atlas/1.0 (mailto:atlas@local)"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print(f"  openalex error {aid}: {e}", file=sys.stderr)
        return None

def classify_works(works):
    out = {"t1_papers": 0, "t2_papers": 0, "t3_papers": 0, "t4_papers": 0, "other_papers": 0, "total_papers": 0, "venue_samples": []}
    seen_venues = {}  # name -> (tier, count)
    for w in works or []:
        if w.get("type") not in (None, "article", "book-chapter", "posted-content", "preprint"):
            continue
        out["total_papers"] += 1
        loc = w.get("primary_location") or {}
        src = (loc.get("source") or {}) or {}
        issn_l = src.get("issn_l")
        issns = src.get("issn") or []
        name = src.get("display_name") or ""
        tier = None
        for cand in filter(None, [issn_l] + list(issns)):
            key = cand.replace("-", "").upper()
            if key in ISSN_TIER:
                tier = ISSN_TIER[key][0]
                break
        if tier == "T1": out["t1_papers"] += 1
        elif tier == "T2": out["t2_papers"] += 1
        elif tier == "T3": out["t3_papers"] += 1
        elif tier == "T4": out["t4_papers"] += 1
        else: out["other_papers"] += 1
        if name:
            prev = seen_venues.get(name, (tier or "-", 0))
            seen_venues[name] = (tier or prev[0] or "-", prev[1] + 1)
    # top venues for traceability (T1/T2 first, then by count)
    rank_tier = {"T1":0,"T2":1,"T3":2,"T4":3,"-":4}
    top = sorted(seen_venues.items(), key=lambda kv: (rank_tier.get(kv[1][0],4), -kv[1][1]))[:15]
    out["venue_samples"] = [{"name": n, "tier": t, "count": c} for n, (t, c) in top if t != "-" or c >= 2]
    return out

def enrich_person(slug):
    f = DATA / "people" / f"{slug}.yaml"
    if not f.exists():
        print(f"[skip] {slug}: no file", file=sys.stderr)
        return None
    d = yaml.safe_load(f.read_text()) or {}
    oa = ((d.get("external_ids") or {}).get("openalex") or "").strip()
    if not oa:
        print(f"[skip-no-oa] {slug}", file=sys.stderr)
        return None
    oa_full = oa if oa.startswith("http") or oa.startswith("A") else f"A{oa}"
    print(f"[enrich] {slug} <- {oa_full}")
    j = fetch_openalex_author(oa_full)
    if not j: return None
    cls = classify_works(j.get("results") or [])
    # merge into activity
    act = d.get("activity") or {}
    act.update({
        "quality_source": "openalex + ruirui-2026",
        "t1_papers": cls["t1_papers"],
        "t2_papers": cls["t2_papers"],
        "t3_papers": cls["t3_papers"],
        "t4_papers": cls["t4_papers"],
        "other_papers": cls["other_papers"],
    })
    if cls.get("venue_samples"):
        act["venue_samples"] = cls["venue_samples"]
    # store openalex total alongside curated total
    act["oa_total_papers"] = cls["total_papers"]
    if not act.get("total_papers"):
        act["total_papers"] = cls["total_papers"]
    d["activity"] = act
    # force publication ids to strings so js-yaml doesn't parse them as numbers
    for pub in (d.get("publications") or []):
        if "id" in pub and pub["id"] is not None:
            pub["id"] = str(pub["id"])
    # write back preserving key order roughly
    dumped = yaml.dump(d, allow_unicode=True, sort_keys=False, width=120, default_flow_style=False)
    # force quoting on pub `id:` lines that look numeric (e.g. 0510019) so js-yaml doesn't parse as number
    lines = []
    for ln in dumped.splitlines(keepends=True):
        m = re.match(r"^(\s*)id:\s*([0-9][\w.\-]*)\s*$", ln.rstrip("\n"))
        if m:
            indent, val = m.group(1), m.group(2)
            ln = f'{indent}id: "{val}"\n'
        lines.append(ln)
    with open(f, "w") as fp:
        fp.write("".join(lines))
    return cls

def main():
    args = sys.argv[1:]
    if args == ["--all"]:
        slugs = [p.stem for p in sorted((DATA/"people").glob("*.yaml"))]
    else:
        slugs = args
    for i, s in enumerate(slugs):
        enrich_person(s)
        time.sleep(0.25)  # polite to openalex
    print(f"done: {len(slugs)} slugs", file=sys.stderr)

if __name__ == "__main__":
    main()
