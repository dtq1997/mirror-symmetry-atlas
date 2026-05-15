#!/usr/bin/env python3
"""Audit person notes for SSOT drift risks.

`personal_notes` should add context, not re-state a second mini-CV that can
drift away from structured fields. This audit flags common duplicated labels
such as 现职/学历/研究/奖项/趣闻 so maintainers can move facts back into
career_timeline, links, external_ids, online_traces, known_emails, and
known_affiliations.

Output: data/people/_ssot_notes_report.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / "data/people"
OUT = PEOPLE_DIR / "_ssot_notes_report.md"

LABEL_RE = re.compile(
    r"(?m)^\s*(现职|学历|教育|研究|奖项|重要奖项|趣闻|邮箱|办公室|媒体/社交|代表作)[：:]"
)


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


def note_labels(note: str) -> list[str]:
    return [m.group(1) for m in LABEL_RE.finditer(note)]


def structured_status(person: dict[str, Any]) -> list[str]:
    status: list[str] = []
    links = person.get("links") or {}
    if person.get("career_timeline"):
        status.append("career_timeline")
    if has_value(person.get("advisor")):
        status.append("advisor")
    if has_value(person.get("known_emails")) or has_value(links.get("email")):
        status.append("email")
    if has_value(person.get("known_affiliations")):
        status.append("known_affiliations")
    if has_value(person.get("online_traces")):
        status.append("online_traces")
    if any(has_value(v) for v in (person.get("external_ids") or {}).values()):
        status.append("external_ids")
    if person.get("publications"):
        status.append("publications")
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default=str(OUT))
    args = parser.parse_args()

    rows = []
    for slug, person in load_people().items():
        note = str(person.get("personal_notes") or "")
        labels = note_labels(note)
        if not labels:
            continue
        rows.append(
            {
                "slug": slug,
                "name": (person.get("name") or {}).get("zh")
                or (person.get("name") or {}).get("en")
                or slug,
                "labels": labels,
                "structured": structured_status(person),
            }
        )

    rows.sort(key=lambda r: (-len(r["labels"]), r["slug"]))

    lines = [
        "# personal_notes SSOT 风险审计",
        "",
        "这是本地静态审计，只报告 `personal_notes` 中疑似第二份简历的标签行。",
        "这些内容不一定错误，但应优先迁移到结构字段；备注保留解释性背景和消歧说明。",
        "",
        f"- 扫描人物：{len(load_people())}",
        f"- 命中人物：{len(rows)}",
        "",
        "| slug | name | labels | structured fields already present |",
        "|---|---|---|---|",
    ]
    for row in rows:
        labels = ", ".join(row["labels"])
        structured = ", ".join(row["structured"]) or "-"
        lines.append(f"| `{row['slug']}` | {row['name']} | {labels} | {structured} |")

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines))
    print(f"Wrote {out}: {len(rows)} people with note SSOT labels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
