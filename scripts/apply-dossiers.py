#!/usr/bin/env python3
"""Apply dossier markdown findings into person YAML personal_notes / sources / links.

Parses data/papers/dossiers/batch-*.md (markdown bullet style) and merges
extracted info into each person's yaml:
- 主页/homepage URL → links.homepage (only if missing)
- 信息源 URLs → sources (deduplicated)
- 履历/趣闻/研究/媒体 paragraphs → appended to personal_notes (only if not already there)

Won't overwrite existing data; merge mode only.

Usage:
  python3 scripts/apply-dossiers.py [--dry-run]
"""

import argparse
import os
import re
import sys
import yaml

PEOPLE_DIR = 'data/people'
DOSSIER_DIR = 'data/papers/dossiers'


def squote(s):
    return "'" + str(s).replace("'", "''") + "'"


def parse_dossier(path):
    """Parse a single dossier markdown file. Returns dict slug -> dict of fields."""
    with open(path) as f:
        text = f.read()
    # Sections start with ## slug-name (... ...) OR ### slug-name
    entries = {}
    # Matches "## slug-something (...)" or "### slug-something (...)"
    section_re = re.compile(r'^(#{2,3})\s+([a-z][a-z0-9-]+)\s*\(([^)]*)\)?\s*$', re.MULTILINE)
    matches = list(section_re.finditer(text))
    for i, m in enumerate(matches):
        slug = m.group(2)
        # Skip if not actually a slug-shaped heading
        if not re.match(r'^[a-z][a-z0-9-]+$', slug):
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        entry = parse_section_body(body)
        entry['_raw_body'] = body
        if slug in entries:
            # Already seen in another batch — append rather than overwrite
            existing = entries[slug]
            for k, v in entry.items():
                if k == '_raw_body':
                    existing[k] = (existing.get(k, '') + '\n\n' + v).strip()
                elif isinstance(v, list):
                    existing.setdefault(k, []).extend(x for x in v if x not in existing.get(k, []))
                elif v and not existing.get(k):
                    existing[k] = v
        else:
            entries[slug] = entry
    return entries


def parse_section_body(body):
    """Extract structured fields from a markdown bullet body.
    Recognized labels: 现职, 主页, 学历, 履历, 研究, 趣闻, 奖项, 重要奖项, 媒体, 媒体/社交,
                       邮箱, 联系方式, 信息源, 代表作, 教学, 个人.
    Returns: dict with keys homepage_urls, sources, narrative_lines (other bullets).
    """
    out = {
        'homepage_urls': [],
        'sources': [],  # list of {label, url}
        'narrative_lines': [],  # plain bullet lines (履历/趣闻/...)
    }
    cur_section = None
    for line in body.splitlines():
        line = line.rstrip()
        # Collect URL refs
        urls_in_line = re.findall(r'https?://[^\s\)\]\(\[【】　-〿＀-￯]+', line)
        # Trim trailing punctuation that often follows URLs in markdown
        urls_in_line = [u.rstrip('.,;:、，。：；') for u in urls_in_line]
        # Bullet line "- **label**: ..." or "- label: ..."
        m = re.match(r'^\s*-\s+\**([^:*]+?)\**\s*[:：]\s*(.+)$', line)
        if m:
            label = m.group(1).strip()
            content = m.group(2).strip()
            if label in ('主页', 'homepage', '主页/邮箱'):
                # extract URL
                for u in urls_in_line:
                    if u not in out['homepage_urls']:
                        out['homepage_urls'].append(u)
            elif label in ('信息源', 'sources', 'sources:'):
                cur_section = 'sources'
                # Sometimes inline url
                for u in urls_in_line:
                    out['sources'].append({'label': label, 'url': u})
            elif label in ('媒体', '媒体/社交', '媒体/社交:'):
                # Add as narrative AND extract URLs
                out['narrative_lines'].append(f'媒体/社交：{content}')
                for u in urls_in_line:
                    if u not in [s['url'] for s in out['sources']]:
                        out['sources'].append({'label': '媒体', 'url': u})
            elif label in ('履历', '学历', '研究', '趣闻', '奖项', '重要奖项',
                           '代表作', '教学', '个人', '现职'):
                if content:
                    out['narrative_lines'].append(f'{label}：{content}')
            cur_section = label
            continue
        # Continuation of `信息源:` — sub-bullet "  - https://..."
        sub = re.match(r'^\s+-\s+(.+)$', line)
        if sub:
            sub_content = sub.group(1).strip()
            # Markdown link [label](url)
            link_m = re.match(r'^\[([^\]]+)\]\(([^)]+)\)$', sub_content)
            if cur_section in ('信息源', 'sources') or '信息源' in (cur_section or ''):
                if link_m:
                    out['sources'].append({'label': link_m.group(1), 'url': link_m.group(2)})
                else:
                    for u in urls_in_line:
                        if u not in [s['url'] for s in out['sources']]:
                            out['sources'].append({'label': '', 'url': u})
            continue
    # Dedup sources
    seen = set()
    deduped_sources = []
    for s in out['sources']:
        u = s.get('url', '')
        if u and u not in seen:
            seen.add(u)
            deduped_sources.append(s)
    out['sources'] = deduped_sources
    return out


def render_links(existing_links, new_homepage):
    """Return updated links yaml block string."""
    links = dict(existing_links or {})
    if new_homepage and not links.get('homepage'):
        links['homepage'] = new_homepage
    return links


def render_sources_yaml(existing_sources, new_sources):
    """Merge sources, dedup by url. Returns rendered yaml block lines."""
    seen = set()
    out = []
    for s in (existing_sources or []) + new_sources:
        if not isinstance(s, dict):
            continue
        u = s.get('url', '')
        if not u or u in seen:
            continue
        seen.add(u)
        out.append(s)
    return out


def render_personal_notes(existing, new_lines):
    """Append new_lines to existing notes, deduplicated by content (case-insensitive
    substring match)."""
    existing = (existing or '').strip()
    appended = list(new_lines)
    if existing:
        # Don't duplicate lines that are already substring-contained
        appended = [l for l in new_lines if l.split('：', 1)[-1][:30].lower() not in existing.lower()]
    if not appended:
        return existing
    # Build new notes
    new = existing
    if existing and not existing.endswith('\n'):
        new += '\n\n'
    new += '\n'.join(appended)
    return new.strip()


def replace_or_insert(text, key, new_content):
    """Replace a top-level yaml key block with new_content (string), or insert if absent."""
    pat = re.compile(rf'^{key}:.*?(?=^[A-Za-z_][\w]*:|\Z)', re.MULTILINE | re.DOTALL)
    if pat.search(text):
        return pat.sub(lambda _m: new_content + '\n', text, count=1)
    # Insert before tags: if present
    for anchor in ['tags:', '$']:
        if anchor == '$':
            return text.rstrip() + '\n' + new_content + '\n'
        m = re.search(rf'^{anchor}', text, re.MULTILINE)
        if m:
            return text[:m.start()] + new_content + '\n' + text[m.start():]
    return text + new_content + '\n'


def block_links(links):
    if not links:
        return 'links: {}'
    lines = ['links:']
    for k, v in links.items():
        lines.append(f'  {k}: {squote(v)}')
    return '\n'.join(lines)


def block_sources(sources):
    if not sources:
        return 'sources: []'
    lines = ['sources:']
    for s in sources:
        lines.append(f'  - label: {squote(s.get("label", "") or "")}')
        lines.append(f'    url: {squote(s.get("url", ""))}')
    return '\n'.join(lines)


def block_personal_notes(notes):
    if not notes:
        return 'personal_notes: ""'
    if '\n' in notes:
        # Use literal block scalar
        lines = ['personal_notes: |']
        for line in notes.splitlines():
            lines.append('  ' + line)
        return '\n'.join(lines)
    return f'personal_notes: {squote(notes)}'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    # 1. Parse all dossier files
    all_entries = {}
    for f in sorted(os.listdir(DOSSIER_DIR)):
        if not f.endswith('.md'):
            continue
        if f == 'README.md':
            continue
        entries = parse_dossier(os.path.join(DOSSIER_DIR, f))
        for slug, ent in entries.items():
            if slug in all_entries:
                # merge
                existing = all_entries[slug]
                for k in ('homepage_urls', 'sources', 'narrative_lines'):
                    for v in ent.get(k, []):
                        if v not in existing.get(k, []):
                            existing.setdefault(k, []).append(v)
            else:
                all_entries[slug] = ent

    # 2. Apply each
    affected = 0
    for slug, ent in sorted(all_entries.items()):
        path = os.path.join(PEOPLE_DIR, f'{slug}.yaml')
        if not os.path.exists(path):
            continue
        with open(path) as f:
            person = yaml.safe_load(f)
        if not person:
            continue

        # Build merged values
        existing_links = person.get('links') or {}
        new_homepage = (ent.get('homepage_urls') or [None])[0]
        merged_links = render_links(existing_links, new_homepage)
        existing_sources = person.get('sources') or []
        merged_sources = render_sources_yaml(existing_sources, ent.get('sources', []))
        existing_notes = person.get('personal_notes') or ''
        merged_notes = render_personal_notes(existing_notes, ent.get('narrative_lines', []))

        # Did anything change?
        changes = []
        if new_homepage and merged_links.get('homepage') != existing_links.get('homepage'):
            changes.append(f'links.homepage += {new_homepage}')
        if len(merged_sources) > len(existing_sources):
            changes.append(f'sources +{len(merged_sources) - len(existing_sources)}')
        if merged_notes.strip() != existing_notes.strip():
            new_chars = len(merged_notes) - len(existing_notes)
            changes.append(f'personal_notes +{new_chars} chars')
        if not changes:
            continue
        affected += 1
        print(f'  {slug}: {", ".join(changes)}')
        if args.dry_run:
            continue

        # Apply
        with open(path) as f:
            text = f.read()
        text = replace_or_insert(text, 'links', block_links(merged_links))
        text = replace_or_insert(text, 'sources', block_sources(merged_sources))
        text = replace_or_insert(text, 'personal_notes', block_personal_notes(merged_notes))
        with open(path, 'w') as f:
            f.write(text)

    print(f'\n{affected} files {"would be" if args.dry_run else ""} updated')


if __name__ == '__main__':
    main()
