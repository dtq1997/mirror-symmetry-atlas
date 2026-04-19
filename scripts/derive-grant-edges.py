#!/usr/bin/env python3
"""从 raw-acks.jsonl 按 (agency, number) 聚合,生成多人共享基金的边,写入 data/derived/grant-edges.yaml"""
import json
from pathlib import Path
from collections import defaultdict
from itertools import combinations

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data/derived/raw-acks.jsonl"
OUT = ROOT / "data/derived/grant-edges.yaml"
EXISTING = ROOT / "data/connections/grant.yaml"

def main():
    # (agency, number) -> {author_slugs}, [arxiv_ids]
    grant_authors = defaultdict(lambda: {"authors": set(), "papers": set()})
    with open(RAW) as f:
        for line in f:
            rec = json.loads(line)
            authors = [a for a in rec["paper_authors"] if a]
            for g in rec.get("grants", []):
                key = (g["agency"], g["number"])
                grant_authors[key]["authors"].update(authors)
                grant_authors[key]["papers"].add(rec["arxiv_id"])

    # 已有边去重键
    existing_pairs = set()
    if EXISTING.exists():
        import yaml
        with open(EXISTING) as f:
            data = yaml.safe_load(f) or {}
        for e in data.get("edges", []):
            s, t = e.get("source"), e.get("target")
            if s and t:
                existing_pairs.add(frozenset([s, t]))

    # 聚合每对学者共享的基金
    pair_grants = defaultdict(list)  # frozenset({a,b}) -> [(agency, number, [papers])]
    for (agency, number), info in grant_authors.items():
        authors = sorted(info["authors"])
        if len(authors) < 2:
            continue
        for a, b in combinations(authors, 2):
            pair_grants[frozenset([a, b])].append({
                "agency": agency,
                "number": number,
                "papers": sorted(info["papers"]),
            })

    edges = []
    for pair, grants in sorted(pair_grants.items(), key=lambda x: -len(x[1])):
        if pair in existing_pairs:
            continue
        a, b = sorted(pair)
        grant_strs = [f"{g['agency']} {g['number']}" for g in grants]
        edges.append({
            "source": a,
            "target": b,
            "type": "grant",
            "notes": "共享基金: " + "; ".join(grant_strs),
            "grants": [{"agency": g["agency"], "number": g["number"]} for g in grants],
            "derived": True,
        })

    OUT.write_text(
        "# 自动推导的共享基金边 (从致谢段基金号聚合)\n"
        "# 仅包含已建档学者之间的配对,且不与 data/connections/grant.yaml 重复\n"
        "edges:\n" +
        "\n".join(
            f"  - source: {e['source']}\n"
            f"    target: {e['target']}\n"
            f"    type: grant\n"
            f"    derived: true\n"
            f"    notes: \"{e['notes']}\"\n"
            for e in edges
        )
    )
    print(f"写入 {len(edges)} 条共享基金边 → {OUT}")
    for e in edges[:10]:
        print(f"  {e['source']} ↔ {e['target']}: {e['notes'][:80]}")

if __name__ == "__main__":
    main()
