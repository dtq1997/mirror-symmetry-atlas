#!/usr/bin/env python3
"""Strict data linter — prebuild gate.

Run on every `pnpm build` and as a CI check. Fails (non-zero exit) when ANY
yaml under data/ violates schema or SSOT invariants. The point: it should be
IMPOSSIBLE to add a new person / institution / paper / connection without
catching the historical pitfalls upfront.

Catches:
  1. key_collaborators[].person not a slug AND name strict-matches an
     existing slug → must use the slug
  2. career_timeline[].advisor: same
  3. top-level advisor / students / mentors fields: must be slug or in
     ghost set. Slug values must reference an existing yaml (no typos).
  4. career_timeline[].institution: must be a slug in data/institutions/
     OR explicitly listed in known-but-no-yaml. (Use [待补充] placeholder if
     truly unknown.)
  5. period strings must parse to a usable year (or be explicit placeholder
     '[?]', '[待验证]', etc.)
  6. nationality: required for any person.
  7. publications[].coauthors raw names: warn (not block) when they
     unambiguously match a slug.
  8. --strict-pubs compares names with exact-ID source author lists.
     Unresolved lookups block this check; name compatibility is not identity proof.
     Skipped by default (slow) — pass --strict-pubs to enable.

Exit code 0 = clean, 1 = violations.

USAGE:
  python3 scripts/lint-data.py              # default fast lint
  python3 scripts/lint-data.py --strict-pubs # also re-validate publications
  python3 scripts/lint-data.py --slug X     # only this slug
"""
import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

import yaml

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from name_match import names_match, slug_for_author, is_slug
from publication_review import load_review, blocked_review
from institution_sources import appointment_errors
from concept_references import concept_reference_errors, concept_content_errors

ROOT = HERE.parent
PEOPLE_DIR = ROOT / 'data/people'
INST_DIR = ROOT / 'data/institutions'
CONN_DIR = ROOT / 'data/connections'
REVIEW_DIR = ROOT / 'data/papers/_review_queue'

PLACEHOLDER_RE = re.compile(r'^\s*\[(?:\?|待[^\]]*|todo|tbd)\]?\s*$', re.IGNORECASE)
SLUG_RE = re.compile(r'^[a-z][a-z0-9-]*$')

ALLOWED_PERSON_LINK_KEYS = {
    'homepage',
    'faculty_page',
    'cv',
    'google_scholar',
    'mathscinet',
    'arxiv_author',
    'zbmath',
    'researchgate',
    'github',
    'youtube',
    'email',
}

ALLOWED_ONLINE_TRACE_TYPES = {
    'homepage',
    'faculty',
    'cv',
    'google_scholar',
    'orcid',
    'mathgenealogy',
    'zbmath',
    'mathscinet',
    'arxiv',
    'openalex',
    'video',
    'interview',
    'lecture_notes',
    'slides',
    'news',
    'blog',
    'github',
    'wayback',
    'other',
}

from non_math_keywords import is_non_math


def load_yaml_dir(d):
    out = {}
    for f in sorted(d.glob('*.yaml')):
        if f.name.startswith('_'):
            continue
        with open(f) as fh:
            out[f.stem] = yaml.safe_load(fh) or {}
    return out


def is_placeholder(s):
    return isinstance(s, str) and bool(PLACEHOLDER_RE.match(s))


def parse_year(period):
    """Return (start_year, ok). ok=False means we couldn't parse."""
    if not period:
        return None, False
    s = str(period).strip()
    if not s or is_placeholder(s):
        return None, True  # explicit placeholder is OK
    # Allow forms like "2010-2014", "2014-present", "2014.9-present",
    # "[?]-2010", "~2010-2014", "2010-08 — 2014-07", single year, etc.
    yrs = re.findall(r'\b(1[6-9]\d{2}|20\d{2}|21\d{2})\b', s)
    if yrs:
        return int(yrs[0]), True
    if re.search(r'present|至今|现在|\[\?\]', s.lower()):
        return None, True  # only "present" with no year — odd but allowed
    return None, False


def lint(strict_pubs=False, only_slug=None):
    people = load_yaml_dir(PEOPLE_DIR)
    institutions = load_yaml_dir(INST_DIR)
    inst_slugs = set(institutions.keys()) | {'_unknown'}

    # All slugs that may appear as a person reference: yaml people + ghost
    # slugs that get rendered (collected from yaml content). For lint purposes
    # we ALLOW ghost slugs but warn so user can decide whether to build them.
    ghost_slugs = set()
    for p in people.values():
        for kc in (p.get('key_collaborators') or []):
            v = kc.get('person')
            if isinstance(v, str) and SLUG_RE.match(v):
                ghost_slugs.add(v)
        for s in (p.get('students') or []):
            if isinstance(s, str) and SLUG_RE.match(s):
                ghost_slugs.add(s)
        for s in (p.get('mentors') or []):
            if isinstance(s, str) and SLUG_RE.match(s):
                ghost_slugs.add(s)
        v = p.get('advisor')
        if isinstance(v, str) and SLUG_RE.match(v):
            ghost_slugs.add(v)
        for e in (p.get('career_timeline') or []):
            v = e.get('advisor')
            if isinstance(v, str) and SLUG_RE.match(v):
                ghost_slugs.add(v)
    ghost_slugs -= set(people.keys())

    errors = []   # blocking (build fails)
    warnings = []  # non-blocking

    def err(slug, msg):
        errors.append((slug, msg))

    def warn(slug, msg):
        warnings.append((slug, msg))

    targets = {only_slug: people[only_slug]} if only_slug else people

    # === per-person checks ===
    for slug, p in targets.items():
        try:
            reviews = load_review(REVIEW_DIR / f'{slug}.yaml').get('candidates', [])
            for pub in p.get('publications') or []:
                if isinstance(pub, dict) and (review := blocked_review(pub, reviews)):
                    err(slug, f"publications {pub.get('id')!r}: blocked by explicit review {review.get('review_status')}; re-review sources before restoring")
        except (ValueError, yaml.YAMLError, OSError) as exc:
            err(slug, str(exc))
        if p.get('slug') != slug:
            err(slug, f"slug field {p.get('slug')!r} doesn't match filename")

        name = p.get('name') or {}
        if not (name.get('en') or name.get('zh')):
            err(slug, "name.en or name.zh required")

        # nationality
        if not p.get('nationality') and 'tags' not in p:
            warn(slug, "nationality missing")

        links = p.get('links') or {}
        if not isinstance(links, dict):
            err(slug, "links must be a mapping")
            links = {}
        for key, value in links.items():
            if key not in ALLOWED_PERSON_LINK_KEYS:
                warn(slug, f"links.{key!r} is not rendered by the person page; "
                     f"move public traces to online_traces or a standard links key")
            if isinstance(value, str) and value.strip().lower() in {'none', 'null'}:
                warn(slug, f"links.{key!r} has placeholder string {value!r}; "
                     f"remove it or replace with a real URL")

        for i, trace in enumerate(p.get('online_traces') or []):
            tag = f"online_traces[{i}]"
            if not isinstance(trace, dict):
                err(slug, f"{tag} must be a mapping")
                continue
            trace_type = trace.get('type')
            if trace_type not in ALLOWED_ONLINE_TRACE_TYPES:
                err(slug, f"{tag}.type {trace_type!r} is not in allowed set")
            if not trace.get('url'):
                err(slug, f"{tag}.url required")

        # advisor field (top-level)
        a = p.get('advisor')
        if a is not None:
            if not isinstance(a, str):
                err(slug, f"advisor must be string, got {type(a).__name__}")
            elif not is_slug(a) and not is_placeholder(a):
                # raw name — try to resolve
                cand = slug_for_author(a, people)
                if cand:
                    err(slug, f"advisor={a!r} should be slug {cand!r}")
                else:
                    warn(slug, f"advisor={a!r} is a raw name with no matching slug; "
                         f"either build a yaml or accept as ghost")
            elif is_slug(a) and a not in people and a not in ghost_slugs:
                warn(slug, f"advisor slug {a!r} has no yaml (ghost)")

        # students & mentors
        for field in ('students', 'mentors'):
            for s in (p.get(field) or []):
                if not isinstance(s, str):
                    err(slug, f"{field} entry must be string, got {type(s).__name__}")
                    continue
                if is_placeholder(s):
                    continue
                if not is_slug(s):
                    cand = slug_for_author(s, people)
                    if cand:
                        err(slug, f"{field} entry {s!r} should be slug {cand!r}")
                    else:
                        warn(slug, f"{field} entry {s!r} is raw name; "
                             f"build yaml or accept ghost")
                elif s not in people:
                    warn(slug, f"{field} slug {s!r} has no yaml")

        # key_collaborators
        for kc in (p.get('key_collaborators') or []):
            v = kc.get('person')
            raw_name = kc.get('name')
            if v is None and not raw_name:
                err(slug, f"key_collaborators entry needs `person` (slug) "
                    f"or `name` (raw)")
                continue
            if v is None:
                # raw-name only collaborator (foreign / unbuilt) — try to
                # nudge: if their name strict-matches an existing slug, the
                # entry SHOULD be migrated. Warn (not block) to avoid blocking
                # legitimate cases.
                cand = slug_for_author(raw_name, people)
                if cand:
                    err(slug, f"key_collaborators name={raw_name!r} maps to "
                        f"existing slug {cand!r}; use person: {cand} instead")
                continue
            if not isinstance(v, str):
                err(slug, f"key_collaborators.person must be string")
                continue
            if is_placeholder(v):
                continue
            if not is_slug(v):
                cand = slug_for_author(v, people)
                if cand:
                    err(slug, f"key_collaborators.person {v!r} should be slug {cand!r}")
                # else: foreign collaborator with no slug — OK
            elif v not in people and v not in ghost_slugs:
                warn(slug, f"key_collaborators.person {v!r} has no yaml")

        # career_timeline
        for i, e in enumerate(p.get('career_timeline') or []):
            tag = f"career_timeline[{i}] (period={e.get('period')!r})"
            # advisor
            v = e.get('advisor')
            if v and isinstance(v, str) and not is_placeholder(v):
                if not is_slug(v):
                    cand = slug_for_author(v, people)
                    if cand:
                        err(slug, f"{tag}.advisor {v!r} should be slug {cand!r}")
                    else:
                        warn(slug, f"{tag}.advisor {v!r} is raw name (foreign?)")
                elif v not in people and v not in ghost_slugs:
                    warn(slug, f"{tag}.advisor slug {v!r} has no yaml")
            # institution
            inst = e.get('institution')
            if inst:
                if not isinstance(inst, str):
                    err(slug, f"{tag}.institution must be string")
                elif is_placeholder(inst):
                    pass
                elif not is_slug(inst):
                    err(slug, f"{tag}.institution {inst!r} should be a slug "
                        f"under data/institutions/ (got raw text)")
                elif inst not in inst_slugs:
                    err(slug, f"{tag}.institution slug {inst!r} has no yaml "
                        f"under data/institutions/")
            # period
            year, ok = parse_year(e.get('period'))
            if not ok:
                # Awards may legitimately omit the year. Position/education
                # without a year is suspicious and blocks.
                if e.get('type') == 'award':
                    warn(slug, f"{tag}.period {e.get('period')!r} unparsed; "
                         f"award entries should still record the year")
                else:
                    err(slug, f"{tag}.period {e.get('period')!r} can't parse "
                        f"a year; use a known format or [待验证] placeholder")
            # type required
            if not e.get('type'):
                err(slug, f"{tag} missing 'type' field")
            elif e['type'] not in {'education', 'position', 'visit', 'award', 'event', 'teaching'}:
                err(slug, f"{tag}.type {e['type']!r} not in allowed set")

        # publications
        for i, pub in enumerate(p.get('publications') or []):
            if not isinstance(pub, dict):
                err(slug, f"publications[{i}] not a dict")
                continue
            tag = f"publications[{i}] (id={pub.get('id')!r})"
            # Non-math topic OR venue check (hard block — 99% homonym pollution)
            kw = is_non_math(title=pub.get('title'), journal=pub.get('journal'))
            if kw:
                kind, evidence = kw
                err(slug, f"{tag}: non-math {kind} ({evidence!r}); paper "
                    f"likely attributed via homonym. Run "
                    f"`python3 scripts/eject-non-math-publications.py "
                    f"--apply` or remove manually")
            for c in (pub.get('coauthors') or []):
                if not isinstance(c, str):
                    err(slug, f"{tag}.coauthors entry must be string")
                    continue
                if is_slug(c):
                    if c not in people and c not in ghost_slugs:
                        warn(slug, f"{tag}.coauthors slug {c!r} has no yaml")
                else:
                    cand = slug_for_author(c, people)
                    if cand:
                        warn(slug, f"{tag}.coauthors {c!r} could be slug "
                             f"{cand!r} (use scripts/normalize-slug-references.py)")

        # publication-count vs activity sanity:
        # if activity.total_papers is set but diverges from len(publications)
        # by more than 5 papers AND >25%, the yaml has stale stats — was the
        # case for zhao-qiulan (activity.total_papers=80 but only 11 listed).
        act = p.get('activity') or {}
        total = act.get('total_papers')
        listed = len(p.get('publications') or [])
        if isinstance(total, int) and total > 0 and listed > 0:
            diff = abs(total - listed)
            if diff >= 5 and diff / max(total, listed) > 0.25:
                warn(slug, f"activity.total_papers={total} but "
                     f"len(publications)={listed} (diff {diff}); list is "
                     f"likely incomplete — run scripts/enrich-from-openalex.py "
                     f"or update activity.total_papers to match")

    # === optional: re-validate publication ownership ===
    if strict_pubs:
        try:
            from lib_truth import get_actual_authors
            print("\n--- source-name compatibility check (not personal identity proof) ---")
            for slug, p in targets.items():
                target_en = ((p.get('name') or {}).get('en') or '').strip()
                if not target_en:
                    continue
                from name_match import names_compatible
                for pub in (p.get('publications') or []):
                    if not isinstance(pub, dict):
                        continue
                    authors, src = get_actual_authors(pub, owner_hint=target_en)
                    if not authors:
                        err(slug, f"publications {pub.get('id')!r}: unresolved source lookup; not checked")
                        continue
                    if not any(names_compatible(target_en, a) for a in authors):
                        err(slug, f"publications {pub.get('id')!r}: owner "
                            f"{target_en!r} not among real authors {authors!r} "
                            f"(source: {src})")
        except ImportError:
            err('-', 'lib_truth not importable; strict source-name check incomplete')

    # === institution checks ===
    if only_slug is None:
        concepts = load_yaml_dir(ROOT / 'data/concepts')
        for slug, concept in concepts.items():
            for message in concept_content_errors(concept, concepts):
                err(f'concept:{slug}', message)
            for message in concept_reference_errors(concept, concepts, people, institutions):
                err(f'concept:{slug}', message)
        for slug, inst in institutions.items():
            for message in appointment_errors(inst, people):
                err(f'inst:{slug}', message)
            name = inst.get('name')
            if not name or not (
                (isinstance(name, dict) and (name.get('en') or name.get('zh'))) or
                isinstance(name, str)
            ):
                err(f'inst:{slug}', "institution name required (en or zh)")

    # === report ===
    print(f"\n=== Lint report ===")
    print(f"  errors   : {len(errors)}")
    print(f"  warnings : {len(warnings)}")
    if errors:
        print("\nErrors (blocking):")
        for slug, msg in errors[:200]:
            print(f"  ✗ {slug}: {msg}")
        if len(errors) > 200:
            print(f"  ... +{len(errors) - 200} more")
    if warnings:
        print(f"\nWarnings (non-blocking; first 50):")
        for slug, msg in warnings[:50]:
            print(f"  ⚠ {slug}: {msg}")
        if len(warnings) > 50:
            print(f"  ... +{len(warnings) - 50} more")
    return 1 if errors else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict-pubs', action='store_true',
                        help='Also re-validate publication ownership against arxiv/Crossref')
    parser.add_argument('--slug', help='Only check this slug')
    args = parser.parse_args()
    sys.exit(lint(strict_pubs=args.strict_pubs, only_slug=args.slug))
