#!/usr/bin/env python3
"""Audit person-profile depth, not publication correctness.

This is a local, non-network queue builder. It does not decide facts. It only
answers: which person files are missing biographical depth, public online
traces, sources, and narrative context?

Output: data/people/_profile_depth_report.md
"""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / "data/people"
OUT = PEOPLE_DIR / "_profile_depth_report.md"


def load_people() -> dict[str, dict[str, Any]]:
    people: dict[str, dict[str, Any]] = {}
    for path in sorted(PEOPLE_DIR.glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        people[path.stem] = yaml.safe_load(path.read_text()) or {}
    return people


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip() not in {"null", "[待补充]", "[待验证]"}
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def has_life_date(person: dict[str, Any], precise_key: str, legacy_key: str) -> bool:
    fact = person.get(precise_key)
    if isinstance(fact, dict) and has_value(fact.get("date")):
        return True
    return has_value(person.get(legacy_key))


def current_position(person: dict[str, Any]) -> bool:
    for entry in person.get("career_timeline") or []:
        if entry.get("type") != "position":
            continue
        period = str(entry.get("period") or "").lower()
        if any(token in period for token in ("present", "至今", "现在")):
            return True
    return False


def online_trace_count(person: dict[str, Any]) -> int:
    count = 0
    links = person.get("links") or {}
    count += sum(1 for value in links.values() if has_value(value))
    external_ids = person.get("external_ids") or {}
    count += sum(1 for value in external_ids.values() if has_value(value))
    count += len(person.get("online_traces") or [])
    return count


def has_official_trace(person: dict[str, Any]) -> bool:
    links = person.get("links") or {}
    if has_value(links.get("homepage")) or has_value(links.get("faculty_page")) or has_value(links.get("cv")):
        return True
    for trace in person.get("online_traces") or []:
        if trace.get("type") in {"homepage", "faculty", "cv"} and has_value(trace.get("url")):
            return True
    for source in person.get("sources") or []:
        label = str(source.get("label") or "").lower()
        if any(token in label for token in ("faculty", "homepage", "cv", "profile", "主页", "教师")):
            return True
    return False


def has_identity_trace(person: dict[str, Any]) -> bool:
    links = person.get("links") or {}
    profile = person.get("identity_profile") or {}
    return any(
        [
            has_value(links.get("email")),
            has_value(person.get("known_emails")),
            has_value(person.get("known_affiliations")),
            has_value(profile.get("email_domains")),
            has_value(profile.get("affiliations")),
        ]
    )


def source_count(person: dict[str, Any]) -> int:
    return len(person.get("sources") or [])


def note_len(person: dict[str, Any]) -> int:
    return len(str(person.get("personal_notes") or "").strip())


def is_deceased(person: dict[str, Any]) -> bool:
    return has_life_date(person, "death", "died")


def missing_fields(person: dict[str, Any], min_traces: int, include_photo: bool) -> list[str]:
    missing: list[str] = []
    if not has_life_date(person, "birth", "born"):
        missing.append("出生年份/生日")
    if not has_official_trace(person):
        missing.append("官方主页/CV")
    if online_trace_count(person) < min_traces:
        missing.append(f"网上痕迹<{min_traces}")
    if not has_identity_trace(person):
        missing.append("邮箱/署名单位线索")
    if source_count(person) < 2:
        missing.append("sources<2")
    if note_len(person) < 80:
        missing.append("personal_notes<80字")
    if not is_deceased(person) and not current_position(person):
        missing.append("当前职位")
    if not person.get("career_timeline"):
        missing.append("career_timeline")
    elif not any(e.get("type") == "education" for e in person.get("career_timeline") or []):
        missing.append("教育经历")
    if not has_value(person.get("advisor")):
        missing.append("导师")
    if not person.get("publications"):
        missing.append("publications")
    if not any(has_value(v) for v in (person.get("external_ids") or {}).values()):
        missing.append("external_ids")
    if include_photo and not has_value(person.get("photo_url")):
        missing.append("照片")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    parser.add_argument("--min-traces", type=int, default=3)
    parser.add_argument("--include-photo", action="store_true")
    args = parser.parse_args()

    people = load_people()
    rows = []
    counter: Counter[str] = Counter()

    for slug, person in people.items():
        missing = missing_fields(person, args.min_traces, args.include_photo)
        for item in missing:
            counter[item] += 1
        rows.append(
            {
                "slug": slug,
                "name": (person.get("name") or {}).get("zh")
                or (person.get("name") or {}).get("en")
                or slug,
                "missing": missing,
                "trace_count": online_trace_count(person),
                "sources": source_count(person),
                "notes_len": note_len(person),
            }
        )

    rows.sort(key=lambda r: (-len(r["missing"]), r["slug"]))

    lines = [
        "# 人物档案深度审计",
        "",
        "这是本地静态审计，只列缺口，不推断事实。生日、出生地、履历和网上痕迹必须有公开来源后再写入 YAML。",
        "",
        f"- 扫描人物：{len(people)}",
        f"- 网上痕迹目标：每人至少 {args.min_traces} 条",
        f"- 照片缺口：{'计入' if args.include_photo else '默认不计入'}",
        "",
        "## 缺口统计",
        "",
    ]
    for name, count in counter.most_common():
        lines.append(f"- {name}: {count}")

    lines.extend(["", "## 优先队列", ""])
    lines.append("| slug | name | missing | traces | sources | notes |")
    lines.append("|---|---|---:|---:|---:|---:|")
    for row in rows:
        lines.append(
            f"| `{row['slug']}` | {row['name']} | {len(row['missing'])} | "
            f"{row['trace_count']} | {row['sources']} | {row['notes_len']} |"
        )

    lines.extend(["", "## 逐人缺口", ""])
    for row in rows:
        if not row["missing"]:
            continue
        lines.append(f"### {row['slug']} — {row['name']}")
        for item in row["missing"]:
            lines.append(f"- {item}")
        lines.append("")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print(f"Wrote {out}: {len(rows)} people, {sum(counter.values())} missing markers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
