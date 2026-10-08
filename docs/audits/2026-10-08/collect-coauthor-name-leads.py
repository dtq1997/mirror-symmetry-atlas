"""[Codex] Read-only name compatibility leads, never identity verdicts."""
import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import yaml
sys.path.insert(0, str(Path('scripts').resolve()))
from name_match import names_compatible
from paper_identity import canonical_arxiv_id

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', required=True, help='New JSON report path; existing files are never overwritten')
args = parser.parse_args()
output = Path(args.output)
if output.exists():
    parser.error('Output already exists; preserve prior review records')

cache = json.loads(Path('docs/audits/2026-10-08/arxiv-metadata-audit.json').read_text())
sources = {}
for row in cache['rows']:
    source = row.get('source') or {}
    key = canonical_arxiv_id(source.get('id'))
    if key:
        assert not sources.get(key) or sources[key] == source, key
        sources[key] = source
people = {p.stem: yaml.safe_load(p.read_text()) for p in sorted(Path('data/people').glob('*.yaml')) if not p.name.startswith('_')}
counts = Counter()
leads = []
uncovered = []
for slug, person in people.items():
    for index, pub in enumerate(person.get('publications') or []):
        counts['publication_rows'] += 1
        key = canonical_arxiv_id(pub.get('id'))
        source = sources.get(key)
        if not source:
            counts['rows_without_cached_arxiv_source'] += 1
            uncovered.append({'person': slug, 'id': pub.get('id'), 'reason': 'no complete arxiv source in the chosen snapshot'})
            continue
        counts['rows_with_cached_arxiv_source'] += 1
        authors = source['authors_raw']
        for value in pub.get('coauthors') or []:
            counts['coauthor_fields_compared'] += 1
            target = people.get(value)
            name = (target.get('name') or {}).get('en', '') if target else value
            if any(names_compatible(name, a) for a in authors):
                counts['name_compatible_fields_not_identity_verified'] += 1
                continue
            counts['incompatible_name_leads'] += 1
            leads.append({'person':slug,'locator':f'publications[{index}].coauthors',
                          'id':pub.get('id'),'recorded_title':pub.get('title'),
                          'recorded_coauthor':value,'resolved_name':name,
                          'bound_to_person':bool(target),'source':source,
                          'status':'name-incompatibility-lead; requires source and spelling review'})
report = {'provider':'Codex','checked_at':datetime.now(timezone.utc).isoformat(),
          'scope':'Read-only comparison of currently recorded coauthor fields with a dated arXiv source snapshot. Names compatible is not identity verified; accents, transliteration, initials and incomplete lists can produce review leads. No publication or person was modified.',
          'source_snapshot':'arxiv-metadata-audit.json','source_checked_at':cache['checked_at'],
          'counts':dict(counts),'leads':leads,'uncovered':uncovered}
output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report['counts'],ensure_ascii=False))
for item in leads:
    print(item['person'],item['id'],repr(item['recorded_coauthor']),'=>',repr(item['resolved_name']),'|',item['source']['authors_raw'])
