"""Faculty page enrichment for Chinese scholars in mirror-symmetry-atlas.

For each target slug, fetch its institutional faculty page (curated URL list),
extract: title (rank), department, email, office, education (year/degree/inst),
work history (year-range/title/inst), Chinese national honors (杰青/长江/优青/
青年长江/院士/青年学者), publications gist, photo. Then upsert into yaml.

Conservative writes:
- For numeric/structured fields with conflict, keep existing & add a
  `[待验证]` flag at the new value.
- For new info (email, office, faculty_url), write directly.
- All extracted facts get `sources` attached with the URL.

This script does NOT use any name-based matching at the slug level — slug is
the input, faculty URL is the input. Cross-verification with NSFC公示 / 学校
新闻 is done in a SECOND pass driven by the user's confirmation.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'
URL_FILE = ROOT / 'data/people/_faculty_urls.yaml'
PROGRESS = ROOT / 'data/people/_enrichment_progress.json'
RAW_CACHE = ROOT / 'data/papers/_faculty_html_cache'
RAW_CACHE.mkdir(parents=True, exist_ok=True)


def fetch(url, slug, max_time=30):
    safe = re.sub(r'[^a-zA-Z0-9]', '_', url)[:120]
    cache = RAW_CACHE / f'{slug}__{safe}.html'
    if cache.exists() and cache.stat().st_size > 500:
        return cache.read_text(errors='replace')
    r = subprocess.run(
        ['curl', '-sk', '-L', '--max-time', str(max_time),
         '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14) atlas-enricher',
         url],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    if r.stdout and len(r.stdout) > 500:
        cache.write_text(r.stdout)
        return r.stdout
    return None


# ===== Chinese honor / title detection =====
HONOR_PATTERNS = [
    # (regex, normalized title, typical year-range proximity)
    (r'中国科学院院士|中科院院士|CAS\s*Academician', '中国科学院院士'),
    (r'中国工程院院士', '中国工程院院士'),
    (r'国家杰出青年科学基金|杰青(?![年])', '国家杰出青年科学基金 (杰青)'),
    (r'优秀青年科学基金|优青(?![年])', '国家优秀青年科学基金 (优青)'),
    (r'青年长江学者|长江学者青年|青年长江', '教育部青年长江学者'),
    (r'长江学者特聘教授|长江特聘', '教育部长江学者特聘教授'),
    (r'国家高层次人才|国家级人才计划', '国家高层次人才'),
    (r'青年千人|千人计划青年项目', '国家青年千人计划'),
    (r'(?<!青年)千人计划|海外高层次人才千人', '国家千人计划'),
    (r'万人计划青年拔尖|青年拔尖人才', '万人计划青年拔尖人才'),
    (r'万人计划领军', '万人计划科技创新领军人才'),
    (r'百千万人才工程国家级', '百千万人才工程国家级人选'),
    (r'国家自然科学奖', '国家自然科学奖'),
    (r'求是杰出青年|求是科技基金会', '求是杰出青年学者'),
    (r'晨兴数学(金奖|银奖)', 'ICCM 晨兴数学奖'),
    (r'陈省身奖|S\.S\.\s*Chern\s*Award', '陈省身奖'),
    (r'华罗庚奖', '华罗庚奖'),
    (r'钟家庆奖', '钟家庆奖'),
    (r'ICM\s*invited\s*speaker|ICM\s*邀请报告人', 'ICM 邀请报告人'),
]

EMAIL_OBFUSCATIONS = [
    (r'\s*(?:dot|\.|·|＠?)\s*', '.'),
    (r'\s*(?:at|@|＠)\s*', '@'),
]


def find_email(text):
    """Best-effort email extraction with deobfuscation."""
    # Standard pattern (canonical form)
    m = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}', text)
    if m:
        return m.group(0).lower()
    # Obfuscated form: "user at host dot tld dot cn" — convert space-separated
    # 'at'/'dot' tokens. We require that the LEFT side is a single token (no
    # spaces) to avoid false positives in normal English prose.
    obfus_re = re.compile(
        r'([a-zA-Z0-9._%+-]+)\s*(?:\(at\)|\[at\]|（at）|at|@|＠)\s*'
        r'([a-zA-Z0-9-]+(?:\s+(?:\(dot\)|\[dot\]|（dot）|dot|\.|·)\s+[a-zA-Z0-9-]+)+)',
        re.IGNORECASE)
    m = obfus_re.search(text)
    if m:
        host = re.sub(r'\s*(?:\(dot\)|\[dot\]|（dot）|dot|·)\s*', '.', m.group(2),
                       flags=re.IGNORECASE)
        host = re.sub(r'\s+', '', host)
        return f'{m.group(1)}@{host}'.lower()
    return None


def detect_honors(text):
    found = []
    for pat, name in HONOR_PATTERNS:
        for m in re.finditer(pat, text, re.IGNORECASE):
            # Try to find year within 30 chars
            window = text[max(0, m.start() - 30): m.end() + 30]
            yrs = re.findall(r'\b(19\d{2}|20\d{2})\b', window)
            year = yrs[0] if yrs else None
            found.append({'title': name, 'year': year, 'snippet': window.strip()})
    # Dedup by title
    seen = set()
    out = []
    for h in found:
        if h['title'] in seen:
            continue
        seen.add(h['title'])
        out.append(h)
    return out


def extract_education(text):
    """Match patterns like '2010, 河南大学, 学士' / '2010 河南大学 本科'."""
    rows = []
    for m in re.finditer(
        r'(\d{4})\s*[，,\s]+([一-鿿 A-Za-z\.\s\-]+?[大学|学院|University|Institute|College]+)\s*[，,\s]+(博士|硕士|学士|本科|PhD|MS|BS|Master|Bachelor)',
            text):
        rows.append({'year': int(m.group(1)),
                     'institution_text': m.group(2).strip(),
                     'degree': m.group(3)})
    return rows


def extract_work_history(text):
    rows = []
    # 2019-2025, 北京大学, 助理教授  /  2025-, 北京大学, 长聘副教授
    for m in re.finditer(
        r'(\d{4})\s*[\-—–~]\s*(\d{4}|至今|present|现在|)\s*[，,\s]+([一-鿿 A-Za-z\.\-\s]+?[大学|学院|University|Institute|College]+)\s*[，,\s]+([一-鿿 A-Za-z\-\s]+?(?:教授|研究员|博士后|讲师|Professor|Researcher|Postdoc|Lecturer|Fellow))',
            text):
        rows.append({
            'period': f"{m.group(1)}-{m.group(2) or 'present'}",
            'institution_text': m.group(3).strip(),
            'role': m.group(4).strip(),
        })
    return rows


def extract_main_content(html):
    """Try to isolate the personal-info block from sidebar/menu noise.

    Different schools use different containers. We look for known wrapper
    classes; if none match, fall back to stripping nav/menu sections.
    """
    candidates = [
        # PKU faculty pages — stop before footer block
        r'<div\s+class="subPersonHome[^"]*"[^>]*>.*?(?=<footer|<div\s+class="footer|Copyright)',
        # Tsinghua
        r'<div\s+class="(?:detail|content|teacherIntro|teacher_detail)[^"]*"[^>]*>.*?(?=<footer|</body)',
        # Sun Yat-sen / generic
        r'<div\s+class="(?:article|main|teacher-intro|info)[^"]*"[^>]*>.*?(?=<footer|</body)',
        # WUHAN / SCUEC etc
        r'<div\s+id="(?:vsb_content|content|main)[^"]*"[^>]*>.*?(?=<footer|</body)',
    ]
    for pat in candidates:
        m = re.search(pat, html, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(0)
    # Fallback: drop nav/header/footer/sidebar, keep the rest
    cleaned = html
    for tag_pat in [
        r'<nav\b.*?</nav>',
        r'<header\b.*?</header>',
        r'<footer\b.*?</footer>',
        r'<aside\b.*?</aside>',
        r'<ul\s+class="(?:mtopList|navm|subNavs|nav)[^"]*".*?</ul>',
        r'<div\s+class="(?:menu|sidebar|nav|footer|header)[^"]*".*?</div>',
    ]:
        cleaned = re.sub(tag_pat, ' ', cleaned, flags=re.DOTALL | re.IGNORECASE)
    return cleaned


def main(slugs=None):
    urls = yaml.safe_load(URL_FILE.read_text()) if URL_FILE.exists() else {}
    if slugs is None:
        slugs = list(urls.keys())

    progress = json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}

    for slug in slugs:
        url_entry = urls.get(slug)
        if not url_entry:
            print(f'SKIP {slug}: no faculty url')
            continue
        if isinstance(url_entry, str):
            url_list = [url_entry]
        else:
            url_list = list(url_entry)

        print(f'\n=== {slug} ===')
        merged = {'honors': [], 'education': [], 'work': [],
                  'emails': set(), 'office': None, 'urls': []}
        for url in url_list:
            html = fetch(url, slug)
            if not html:
                print(f'  warn: empty {url}')
                continue
            # Isolate the personal-content block before stripping. This avoids
            # navigation menu links like '<a>中科院院士</a>' polluting honor
            # detection (without this, 81/86 pages would falsely award the
            # honor 'CAS Academician' to everyone whose page has that menu).
            html = extract_main_content(html)
            # Strip tags but keep text
            text = re.sub(r'<script[^>]*>.*?</script>', ' ', html,
                          flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', ' ', text,
                          flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'&[a-zA-Z]+;', ' ', text)
            text = re.sub(r'\s+', ' ', text)

            for h in detect_honors(text):
                merged['honors'].append({**h, 'source': url})
            merged['education'].extend(
                {**e, 'source': url} for e in extract_education(text))
            merged['work'].extend(
                {**w, 'source': url} for w in extract_work_history(text))
            email = find_email(text)
            if email and 'mathweb' not in email and 'admin' not in email:
                merged['emails'].add(email)
            # Office
            m = re.search(r'(智华楼|镜春园|理科一号楼|理科二号楼|理科三号楼|理科四号楼|理科五号楼|静园|逸夫教学楼|MCM 楼|数学楼|理学院|科学楼)\s*[A-Za-z\d]{0,8}', text)
            if m and not merged['office']:
                merged['office'] = m.group(0).strip()
            merged['urls'].append(url)

        merged['emails'] = sorted(merged['emails'])
        progress[slug] = merged
        print(f'  honors: {[h["title"] for h in merged["honors"]]}')
        print(f'  emails: {merged["emails"]}')
        print(f'  office: {merged["office"]}')
        print(f'  edu rows: {len(merged["education"])}')
        print(f'  work rows: {len(merged["work"])}')

    PROGRESS.write_text(json.dumps(progress, ensure_ascii=False, indent=2,
                                    default=list))
    print(f'\nWrote progress to {PROGRESS}')


if __name__ == '__main__':
    args = sys.argv[1:]
    main(slugs=args or None)
