"""Read-only primary-source collection for the publication review queue."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, importlib.util, json, sys, time, urllib.parse
import yaml
ROOT=Path.cwd()
sys.path.insert(0,str(ROOT/'scripts'))
from paper_identity import canonical_arxiv_id, canonical_title
spec=importlib.util.spec_from_file_location('news',ROOT/'scripts/fetch-arxiv-news.py')
news=importlib.util.module_from_spec(spec);spec.loader.exec_module(news)
cache=ROOT/'.cache/msa/arxiv-metadata/2026-10-08';cache.mkdir(parents=True,exist_ok=True)
rows=[]
for file in sorted((ROOT/'data/people').glob('*.yaml')):
 if file.name.startswith('_'):continue
 person=yaml.safe_load(file.read_text()) or {}
 for i,pub in enumerate(person.get('publications') or []):
  aid=canonical_arxiv_id(pub.get('id'))
  if aid and ('/' in aid or '.' in aid):
   rows.append({'file':str(file.relative_to(ROOT)), 'locator':f'publications[{i}]','person_name':person.get('name',{}).get('en'), 'id':aid,'recorded_title':pub.get('title','')})
ids=sorted(set(row['id'] for row in rows));sources={};failures=[];batches=[]
for i in range(0,len(ids),100):
 batch=ids[i:i+100]
 url='https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'id_list':','.join(batch),'start':0,'max_results':100})
 file=cache/(hashlib.sha256(url.encode()).hexdigest()+'.xml')
 try:
  body=file.read_bytes() if file.exists() else news.request_feed(url)
  total,papers=news.parse_feed(body,0)
  # Missing identifiers remain explicit, never converted to success.
  if len(papers)!=total:raise news.FetchError('Incomplete ID batch')
  if any(p['id'] not in batch for p in papers):raise news.FetchError('Unexpected ID')
  if len(set(p['id'] for p in papers))!=len(papers):raise news.FetchError('Duplicate ID')
  file.write_bytes(body)
  for paper in papers:
   sources[paper['id']]={k:paper[k] for k in ['id','title','authors_raw','category','date','updated','source_url','source_version']}
  batches.append({'requested':batch,'returned':len(papers),'url':url,'sha256':hashlib.sha256(body).hexdigest()})
  print(f'{i+len(batch)}/{len(ids)} requested; {len(sources)} source records',flush=True)
 except Exception as exc:
  failures.append({'ids':batch,'error':str(exc)})
  print(f'Batch {i}: FAILED {exc}',flush=True)
 if i+100<len(ids):time.sleep(4)
for row in rows:
 source=sources.get(row['id'])
 row['metadata_retrieval']='retrieved' if source else 'unresolved'
 if source:
  row['source']=source
  row['title_comparison']='normalized-equal' if canonical_title(row['recorded_title'])==canonical_title(source['title']) else 'requires-review'
 row['identity_review']='not-reviewed; matching author strings would not prove identity'
report={'provider':'Codex','checked_at':datetime.now(timezone.utc).isoformat(),'scope':'Primary metadata collection and literal normalized-title comparison only. Title differences may be version changes, not necessarily errors. No author identity or publication status verdict. No source data modified.','requested_unique_ids':len(ids),'retrieved_unique_ids':len(sources),'rows':rows,'failures':failures,'batches':batches}
output=ROOT/'docs/audits/2026-10-08/arxiv-metadata-audit.json';output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'requested':len(ids),'retrieved':len(sources),'rows':len(rows),'title_review_rows':sum(r.get('title_comparison')=='requires-review' for r in rows),'failed_batches':len(failures)}),flush=True)
