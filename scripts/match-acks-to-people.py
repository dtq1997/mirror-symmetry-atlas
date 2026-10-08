#!/usr/bin/env python3
"""[Codex] Generate acknowledgement leads; publish only explicit reviews.

Default is a read-only preview. --write updates derived views. Full names can
suggest a target for review; initials/surnames and registered paper owners never
establish identity or the grammatical subject of a thank-you statement.
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

from acknowledgement_review import checked_reviews, reviewed_edges
from name_match import names_match

ROOT = Path(__file__).resolve().parent.parent


def clean_latex(text):
    text = re.sub(r"(?<!\\)%[^\n]*", " ", text)
    text = re.sub(r"\\(?:cite[a-zA-Z]*|ref|label|eqref|pageref)\*?(?:\[[^]]*\])*\s*\{[^}]*\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?\s*(?:\[[^]]*\])?\s*\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    return re.sub(r"\s+", " ", text.replace("{", " ").replace("}", " ").replace("~", " ")).strip()


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




def full_name_leads(text, people):
    """Exact complete-name leads only; still needs identity/context review."""
    hits = defaultdict(set)
    for match in EXTERNAL_NAME_RE.finditer(clean_latex(text)):
        first, last = match.group(1), match.group(2)
        if first in NAME_STOPWORDS or last in NAME_LAST_STOPWORDS:
            continue
        name = match.group(0)
        slugs = [slug for slug, person in people.items()
                 if names_match(name, (person.get('name') or {}).get('en', ''))]
        if len(slugs) == 1:
            hits[slugs[0]].add(name)
    for slug, person in people.items():
        zh = (person.get('name') or {}).get('zh')
        if zh and zh in text:
            hits[slug].add(zh)
    return {slug: sorted(names) for slug, names in sorted(hits.items())}


def pending_legacy(legacy, decisions):
    rows = []
    for edge in legacy:
        for paper in sorted(set(edge['papers'])):
            key = (edge['source'], edge['target'], paper)
            if key not in decisions or decisions[key]['status'] == 'needs-review':
                rows.append(dict(source=key[0], target=key[1], paper=paper, status='needs-review'))
    return rows


def generate(records, reviews, people, legacy):
    decisions = checked_reviews(records, reviews, people)
    edges = reviewed_edges(records, reviews, people)
    pending = pending_legacy(legacy, decisions)
    mentions = []
    for row in records:
        leads = full_name_leads(row['ack_text'], people)
        if leads:
            mentions.append({'paper': row['arxiv_id'], 'full_name_leads': leads,
                             'recorded_owners_not_ack_subjects': row['paper_authors'],
                             'status': 'needs-review'})
    candidates = {'meta': {'note': '候选姓名与旧自动连线均待逐篇核对；不作为确定关系展示。',
                           'pending_legacy_paper_claims': len(pending)},
                  'pending_legacy_claims': pending, 'name_mentions': mentions}
    stats = {'papers_processed': len(records),
             'total_edges': len(edges['edges']) + len(edges['single_mentions']),
             'strong_edges': len(edges['edges']), 'single_edges': len(edges['single_mentions']),
             'accepted_paper_claims': sum(r['status'] == 'accepted' for r in reviews),
             'rejected_paper_claims': sum(r['status'] == 'rejected' for r in reviews),
             'pending_legacy_paper_claims': len(pending),
             'papers_with_full_name_leads': len(mentions)}
    return edges, candidates, stats


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='write reviewed outputs after validation')
    args = parser.parse_args()
    directory = ROOT / 'data/derived'
    people = {p.stem: yaml.safe_load(p.read_text()) for p in sorted((ROOT / 'data/people').glob('*.yaml'))}
    records = [json.loads(line) for line in (directory / 'raw-acks.jsonl').read_text().splitlines() if line.strip()]
    reviews = yaml.safe_load((directory / 'ack-reviews.yaml').read_text())['reviews']
    legacy = yaml.safe_load((directory / 'ack-legacy-review.yaml').read_text())['unreviewed_original_edges']
    edges, candidates, stats = generate(records, reviews, people, legacy)
    if args.write:
        for filename, data in [('acknowledgements.yaml', edges), ('ack-candidates.yaml', candidates)]:
            (directory / filename).write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        (directory / 'ack-stats.json').write_text(json.dumps(stats, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'mode': 'write' if args.write else 'preview', **stats}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
