#!/usr/bin/env python3
"""Fetch recent arXiv papers relevant to mirror symmetry and generate news entries.

Usage:
  python3 scripts/fetch-arxiv-news.py [--days 7] [--output data/news/YYYY-MM-DD.yaml]

Queries arXiv for recent papers in relevant categories, matches against
known people and concepts, and generates a YAML news file with Chinese summaries.
"""

import subprocess
import xml.etree.ElementTree as ET
import time
import urllib.parse
import yaml
import os
import sys
import argparse
from datetime import datetime, timedelta

NS = {'a': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}

# Categories to monitor
CATEGORIES = ['math-ph', 'math.AG', 'math.QA', 'hep-th', 'math.DG', 'math.SG', 'nlin.SI']

# Load known people slugs and names
def load_people():
    people_dir = 'data/people'
    people = {}
    if not os.path.exists(people_dir):
        return people
    for f in os.listdir(people_dir):
        if not f.endswith('.yaml'):
            continue
        with open(os.path.join(people_dir, f)) as fh:
            p = yaml.safe_load(fh) or {}
        slug = f.replace('.yaml', '')
        name_en = (p.get('name') or {}).get('en', '')
        name_zh = (p.get('name') or {}).get('zh', '')
        institution = ''
        career = p.get('career_timeline') or []
        for entry in reversed(career):
            if entry.get('type') == 'position':
                institution = entry.get('institution', '')
                break
        people[slug] = {
            'name_en': name_en,
            'name_zh': name_zh,
            'institution': institution,
            'research_areas': p.get('research_areas') or [],
            'activity': p.get('activity') or {},
        }
    return people

# Load known concept slugs
def load_concepts():
    concepts_dir = 'data/concepts'
    concepts = set()
    if not os.path.exists(concepts_dir):
        return concepts
    for f in os.listdir(concepts_dir):
        if f.endswith('.yaml'):
            concepts.add(f.replace('.yaml', ''))
    return concepts

def match_author(author_name, people):
    """Match an arXiv author name to a known person slug."""
    name_lower = author_name.lower()
    for slug, info in people.items():
        en = info['name_en'].lower()
        if not en:
            continue
        # Check if all parts of the known name appear in the author name
        parts = en.split()
        if len(parts) >= 2 and all(p in name_lower for p in parts):
            return slug, info
    return None, None

def match_concepts(title, abstract, concepts):
    """Find matching concept slugs in title/abstract."""
    text = (title + ' ' + (abstract or '')).lower()
    matched = []
    for c in concepts:
        # Convert slug to searchable terms
        terms = c.replace('-', ' ').split()
        if all(t in text for t in terms):
            matched.append(c)
    return matched

def generate_author_context(slug, info):
    """Generate Chinese context string for a known author."""
    parts = []
    name = info.get('name_zh') or info.get('name_en', slug)
    parts.append(name)

    inst = info.get('institution', '')
    if inst:
        parts.append(f"（{inst}）")

    activity = info.get('activity') or {}
    papers = activity.get('total_papers')
    if papers:
        parts.append(f"，{papers} 篇论文")

    return ''.join(parts)

def fetch_recent_papers(days=7, max_per_cat=30):
    """Fetch recent papers from arXiv."""
    all_papers = []
    seen_ids = set()

    for cat in CATEGORIES:
        query = f'cat:{cat}'
        url = (
            f'https://export.arxiv.org/api/query?'
            f'search_query={urllib.parse.quote(query)}'
            f'&max_results={max_per_cat}'
            f'&sortBy=submittedDate&sortOrder=descending'
        )

        time.sleep(4)
        result = subprocess.run(
            ['curl', '-s', '--noproxy', '*', '--max-time', '20', url],
            capture_output=True, text=True
        )
        if not result.stdout or 'Rate exceeded' in result.stdout:
            print(f'  Rate limited on {cat}, skipping', file=sys.stderr)
            continue

        try:
            tree = ET.ElementTree(ET.fromstring(result.stdout))
        except:
            continue

        cutoff = datetime.utcnow() - timedelta(days=days)

        for entry in tree.findall('a:entry', NS):
            arxiv_id = entry.find('a:id', NS).text.split('/')[-1].split('v')[0]
            if arxiv_id in seen_ids:
                continue
            seen_ids.add(arxiv_id)

            published = entry.find('a:published', NS).text
            pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
            if pub_date.replace(tzinfo=None) < cutoff:
                continue

            title = entry.find('a:title', NS).text.strip().replace('\n', ' ').replace('  ', ' ')
            abstract_el = entry.find('a:summary', NS)
            abstract = abstract_el.text.strip().replace('\n', ' ') if abstract_el is not None else ''
            authors = [a.find('a:name', NS).text for a in entry.findall('a:author', NS)]
            cats = [c.get('term') for c in entry.findall('a:category', NS)]
            primary_cat = entry.find('arxiv:primary_category', NS)
            primary = primary_cat.get('term') if primary_cat is not None else cat

            all_papers.append({
                'id': arxiv_id,
                'title': title,
                'abstract': abstract[:500],
                'authors': authors,
                'date': published[:10],
                'primary_category': primary,
                'categories': cats,
            })

    return all_papers

def score_paper(paper, people, concepts):
    """Score a paper's relevance to our atlas."""
    score = 0
    matched_people = []
    matched_concepts = []

    # Match authors
    for author in paper['authors']:
        slug, info = match_author(author, people)
        if slug:
            score += 10
            matched_people.append({
                'slug': slug,
                'name': author,
                'context': generate_author_context(slug, info),
            })

    # Match concepts
    mc = match_concepts(paper['title'], paper.get('abstract', ''), concepts)
    for c in mc:
        score += 3
        matched_concepts.append(c)

    # Keyword boost
    title_lower = paper['title'].lower()
    high_value_keywords = [
        'frobenius', 'stokes', 'isomonodrom', 'painlev', 'dubrovin',
        'mirror symmetry', 'gromov-witten', 'quantum cohomol',
        'virasoro', 'gamma conjecture', 'calabi-yau',
    ]
    for kw in high_value_keywords:
        if kw in title_lower:
            score += 2

    return score, matched_people, matched_concepts

def generate_summary(paper, matched_people, matched_concepts):
    """Generate a Chinese summary for a paper."""
    parts = []

    # Author line
    if matched_people:
        author_strs = [p['context'] for p in matched_people]
        other_count = len(paper['authors']) - len(matched_people)
        if other_count > 0:
            author_strs.append(f"等 {other_count} 人")
        parts.append('、'.join(author_strs) + ' 的新工作。')
    else:
        authors_str = ', '.join(paper['authors'][:3])
        if len(paper['authors']) > 3:
            authors_str += f' 等 {len(paper["authors"])} 人'
        parts.append(f'{authors_str} 的新论文。')

    # Concept tags
    if matched_concepts:
        parts.append(f'涉及：{", ".join(matched_concepts)}。')

    return ''.join(parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=7)
    parser.add_argument('--output', default=None)
    parser.add_argument('--min-score', type=int, default=3)
    args = parser.parse_args()

    today = datetime.utcnow().strftime('%Y-%m-%d')
    output = args.output or f'data/news/{today}.yaml'

    print(f'Fetching papers from last {args.days} days...', file=sys.stderr)
    people = load_people()
    concepts = load_concepts()
    print(f'Loaded {len(people)} people, {len(concepts)} concepts', file=sys.stderr)

    papers = fetch_recent_papers(days=args.days)
    print(f'Found {len(papers)} recent papers', file=sys.stderr)

    # Score and filter
    scored = []
    for paper in papers:
        score, mp, mc = score_paper(paper, people, concepts)
        if score >= args.min_score:
            summary = generate_summary(paper, mp, mc)
            scored.append({
                'id': paper['id'],
                'title': paper['title'],
                'date': paper['date'],
                'authors_raw': paper['authors'],
                'matched_people': [p['slug'] for p in mp],
                'matched_concepts': mc,
                'category': paper['primary_category'],
                'relevance_score': score,
                'summary_zh': summary,
            })

    scored.sort(key=lambda x: -x['relevance_score'])

    # Write output
    news_data = {
        'fetch_date': today,
        'period_days': args.days,
        'total_fetched': len(papers),
        'relevant_count': len(scored),
        'entries': scored,
    }

    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, 'w') as f:
        yaml.dump(news_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f'Wrote {len(scored)} relevant papers to {output}', file=sys.stderr)

if __name__ == '__main__':
    main()
