// [Codex] Regression checks for broken public links and incorrect paper grouping.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import identity from '../.cache/msa/site-tests/paper-identity.js';
import { entityRoute } from '../.cache/msa/site-tests/entity-route.js';
import { buildPeopleGraph, buildConceptGraph, getPrerequisiteChain, highlightConceptPrerequisites, simulationGraph, filterByYear, recordedStartYear, recordedInstitutions } from '../.cache/msa/site-tests/graph.js';
import { publicSourceUrl } from '../.cache/msa/site-tests/source-url.js';
import { renderMathText } from '../.cache/msa/site-tests/math-text.js';
import { publicationMetadata } from '../.cache/msa/site-tests/publication-metadata.js';
import { collectPublications, collectCoauthorship, recordedPublicationStats } from '../.cache/msa/site-tests/publications.js';
import { recordedAffiliations } from '../.cache/msa/site-tests/institution-affiliations.js';
import { canonicalConcepts, conceptLookup } from '../.cache/msa/site-tests/concepts.js';

const conceptFixture = (slug, fields = {}) => ({ slug, name: { en: slug }, difficulty: 'advanced', ...fields });

test('explicit concept aliases share content and references without duplicate nodes or input mutation', () => {
  const input = [conceptFixture('a', { related: ['a-plural', 'b', 'b-plural', 'missing'], sources: [{ label: 'primary', url: 'https://example.org' }] }),
    conceptFixture('a-plural', { alias_of: 'a', name: { en: 'A plural' } }),
    conceptFixture('b', { prerequisites: ['a-plural'], leads_to: ['a-plural'], dual_to: 'a-plural' }),
    conceptFixture('b-plural', { alias_of: 'b' }), conceptFixture('similar-name')];
  const before = structuredClone(input);
  const canonical = canonicalConcepts(input), lookup = conceptLookup(input);
  assert.equal(canonical.length, 3);
  assert.deepEqual(canonical[0].related, ['b', 'missing']);
  assert.ok(canonical[0].aliases.includes('A plural'));
  assert.deepEqual(canonical[1].prerequisites, ['a']);
  assert.deepEqual(canonical[1].leads_to, ['a']);
  assert.equal(canonical[1].dual_to, 'a');
  assert.equal(lookup.get('a-plural'), lookup.get('a'));
  assert.notEqual(lookup.get('similar-name'), lookup.get('a'));
  assert.ok(!buildConceptGraph(canonical).nodes.some(n => n.id.endsWith('plural')));
  canonical[0].sources[0].label = 'changed';
  assert.deepEqual(input, before);
});

test('concept aliases fail on absent targets, chains, cycles and duplicate slugs', () => {
  const a = conceptFixture('a');
  for (const records of [[a, a], [conceptFixture('a', { alias_of: 'a' })],
    [conceptFixture('a', { alias_of: 'missing' })],
    [a, conceptFixture('b', { alias_of: 'a' }), conceptFixture('c', { alias_of: 'b' })],
    [conceptFixture('a', { alias_of: 'b' }), conceptFixture('b', { alias_of: 'a' })]]) {
    assert.throws(() => canonicalConcepts(records));
  }
  assert.deepEqual(canonicalConcepts([]), []);
});

test('concept citation and alias lint rejects conflicting content and invalid sources', () => {
  const code = `import sys,copy
sys.path.insert(0,'scripts')
from concept_references import concept_content_errors
canonical={'slug':'a'}
alias={'slug':'b','alias_of':'a'}
pool={'a':canonical,'b':alias}
check=lambda c: concept_content_errors(c,pool)
assert not check(alias)
assert not check({'sources':[{'label':'Definition 1','url':'https://example.org'}]})
for value in ['b','missing','',None,[],{}]:
 assert check({'slug':'b','alias_of':value})
for field in ['definition','sources','related','year_introduced','dual_to']:
 assert check({**alias,field:'conflicting'})
for value in [None,{},'bad',[None],[{}],[{'label':'','url':'https://example.org'}],[{'label':'x','url':'javascript:alert(1)'}],[{'label':'x','url':[]}],[{'label':'x','url':'https://['}]]:
 assert check({'sources':value}),value
print('schema-only')`;
  const result = spawnSync('python3', ['-c', code], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
});

test('concept reference gate catches a person or institution used as a concept without banning unknown concepts', () => {
  const code = `import sys
sys.path.insert(0,'scripts')
from concept_references import concept_reference_errors
check=lambda c: concept_reference_errors(c, {'real','shared'}, {'person','shared'}, {'university'})
assert not check({'related':['real','unknown','shared'], 'key_people':['person']})
for field in ['prerequisites','leads_to','related']:
 for value in [['person'],['university'],[None],[''],'wrong scalar','',0,{}]:
  assert check({field:value}),(field,value)
print('namespace-only')`;
  const result = spawnSync('python3', ['-c', code], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
});

test('concept graph retains one-sided reversed and missing related references without duplicate pairs', () => {
  const input = [conceptFixture('z', { related: ['a', 'a', 'missing', 'z'] }), conceptFixture('a')];
  const before = structuredClone(input);
  const graph = buildConceptGraph(input);
  assert.deepEqual(graph.links.map(l => [l.type, l.source, l.target]), [
    ['related', 'a', 'z'], ['related', 'missing', 'z'],
  ]);
  assert.equal(graph.nodes.find(n => n.id === 'missing').isGhost, true);
  const reciprocal = buildConceptGraph([input[0], conceptFixture('a', { related: ['z'] })]);
  assert.equal(reciprocal.links.length, 2);
  graph.links[0].dash[0] = 99;
  assert.deepEqual(input, before);
  assert.deepEqual(buildConceptGraph(input).links[0].dash, [3, 4]);
});

test('concept direction and relation types survive duplicate citations, reverse arrows and parallel paths', () => {
  const concepts = [conceptFixture('a', { prerequisites: ['b', 'b'], leads_to: ['b', 'b'], related: ['b'] }),
    conceptFixture('b', { prerequisites: ['a'], leads_to: ['a'] })];
  const graph = buildConceptGraph(concepts);
  assert.equal(graph.links.length, 5);
  assert.deepEqual(new Set(graph.links.map(l => `${l.type}:${l.source}>${l.target}`)), new Set([
    'prerequisite:b>a', 'prerequisite:a>b', 'leads-to:a>b', 'leads-to:b>a', 'related:a>b',
  ]));
  const physicalOffsets = graph.links.map(l => (l.source < l.target ? 1 : -1) * l.curve);
  assert.equal(new Set(physicalOffsets).size, 5);
  const curves = (g) => Object.fromEntries(g.links.map(l => [`${l.type}:${l.source}`, l.curve]));
  assert.deepEqual(curves(graph), curves(buildConceptGraph([...concepts].reverse())));
  assert.deepEqual(buildConceptGraph([]), { nodes: [], links: [] });
});

test('prerequisite tracing terminates on cycles and never promotes related or further-study records', () => {
  const concepts = [conceptFixture('a', { prerequisites: ['b'], leads_to: ['c'], related: ['d', 'b'] }),
    conceptFixture('b', { prerequisites: ['a', 'missing'], leads_to: ['a'] }), conceptFixture('c'), conceptFixture('d')];
  const chain = getPrerequisiteChain('a', concepts);
  assert.deepEqual([...chain].sort(), ['a', 'b', 'missing']);
  const graph = buildConceptGraph(concepts), before = structuredClone(graph);
  const highlighted = highlightConceptPrerequisites(graph, chain);
  assert.ok(highlighted.links.filter(l => l.opacity > 0.5).every(l => l.type === 'prerequisite'));
  assert.equal(highlighted.links.find(l => l.type === 'related' && l.target === 'b').opacity, 0.06);
  assert.equal(highlighted.nodes.find(n => n.id === 'c').opacity, 0.15);
  assert.deepEqual(graph, before);
  assert.deepEqual([...getPrerequisiteChain('unknown', concepts)], ['unknown']);
});

test('institution records retain historical study, work and visits without inventing current appointments', () => {
  const inst = { slug: 'a', research_groups: [] };
  const people = [{ slug: 'old', died: 2005, career_timeline: [
    { institution: 'a', type: 'position', period: '1980-present' },
    { institution: 'a', type: 'education', period: '1960-1964' },
    { institution: 'a', type: 'visit', period: '2000-' },
    { institution: 'b', type: 'position', period: '2001-present' },
    { institution: 'a', type: 'award', period: '1990' },
  ] }];
  const rows = recordedAffiliations(inst, people);
  assert.deepEqual(rows[0].career.map(e => e.type), ['position', 'education', 'visit']);
  assert.deepEqual(rows[0].appointmentChecks, []);
  assert.equal(rows.length, 1);
  assert.deepEqual(recordedAffiliations(inst, [{ ...people[0], career_timeline: [...people[0].career_timeline].reverse() }])[0].appointmentChecks, []);
});

test('institution counts deduplicate people but preserve contradictory group claims and independent dated citations', () => {
  const inst = { slug: 'a', research_groups: [{ name: 'Old list', current_members: ['x', 'x', 'ghost'], past_members: ['x'] }],
    appointment_checks: [{ person: 'y', role: 'Professor', checked_on: '2026-10-08', source: { label: 'Faculty', url: 'https://example.edu/faculty' } }] };
  const people = [{ slug: 'x', career_timeline: [{ institution: 'a', type: 'visit' }] }];
  const before = structuredClone({ inst, people });
  const rows = recordedAffiliations(inst, people);
  assert.deepEqual(rows.map(r => r.person), ['ghost', 'x', 'y']);
  assert.deepEqual(rows.find(r => r.person === 'x').groupClaims.map(g => g.recordedAs), ['current', 'past']);
  assert.equal(rows.find(r => r.person === 'ghost').appointmentChecks.length, 0);
  assert.equal(rows.find(r => r.person === 'y').appointmentChecks.length, 1);
  rows.find(r => r.person === 'x').career[0].period = 'mutated';
  rows.find(r => r.person === 'y').appointmentChecks[0].source.label = 'mutated';
  assert.deepEqual({ inst, people }, before);
  assert.deepEqual(recordedAffiliations({ slug: 'empty' }, []), []);
});

test('appointment citation gate rejects missing identity, role, date or source URL metadata', () => {
  const code = `import sys,copy,datetime
sys.path.insert(0,'scripts')
from institution_sources import appointment_errors
good={'person':'x','role':'Professor','checked_on':'2026-10-08','source':{'label':'Faculty','url':'https://example.edu/faculty'}}
check=lambda rows: appointment_errors({'appointment_checks':rows},{'x'},datetime.date(2026,10,8))
assert not check([good])
assert not appointment_errors({}, {'x'})
for field,value in [('person','ghost'),('person',[]),('role',''),('role','待核实'),('checked_on','2026-02-30'),('checked_on','2027-01-01'),('source',{'label':'Faculty','url':'javascript:alert(1)'}),('source',{'url':'https://example.edu'})]:
 row=copy.deepcopy(good);row[field]=value;assert check([row]),(field,value)
assert check([good,good])
assert check([None])
assert check({})
print('citation-schema-only')`;
  const result = spawnSync('python3', ['-c', code], { encoding: 'utf8' });
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /citation-schema-only/);
});

test('DOI and OpenAlex records never link to arXiv', () => {
  assert.equal(identity.publicationUrl({ id: 'doi:10.1000/example' }), 'https://doi.org/10.1000/example');
  assert.equal(identity.publicationUrl({ id: 'openalex:W1234' }), 'https://openalex.org/W1234');
  assert.equal(identity.publicationUrl({ id: '2401.12345v2' }), 'https://arxiv.org/abs/2401.12345');
});

test('archive names containing v and dotted categories survive version stripping', () => {
  assert.equal(identity.canonicalArxivId('solv-int/9501001v2'), 'solv-int/9501001');
  assert.equal(identity.canonicalArxivId('math.AG/0301001v1'), 'math.AG/0301001');
});

test('ambiguous legacy numbers and unknown IDs do not get invented URLs', () => {
  assert.equal(identity.publicationUrl({ id: '9602001' }), undefined);
  assert.equal(identity.publicationUrl({ id: 'cr:unknown' }), undefined);
  assert.equal(identity.publicationUrl({ id: 'doi:garbage' }), undefined);
});

test('Python and TypeScript canonical keys agree on historic failure cases', () => {
  const rows = [
    { id: 'solv-int/9501001v2', title: 'Brézin and $W$-type theory' },
    { id: 'math.AG/0301001v1', doi: 'https://doi.org/10.1000/ABC' },
    { id: 'doi:10.1000/Test', title: 'An introduction' },
    { id: '2401.12345v3', doi: '10.48550/arXiv.2401.12345' },
  ];
  const py = spawnSync('python3', ['-c', 'import sys,json; sys.path.insert(0,"scripts"); from paper_identity import paper_identity_keys; print(json.dumps([paper_identity_keys(p) for p in json.load(sys.stdin)]))'], { input: JSON.stringify(rows), encoding: 'utf8' });
  assert.equal(py.status, 0, py.stderr);
  assert.deepEqual(rows.map((p) => Object.values(identity.paperIdentityKeys(p))), JSON.parse(py.stdout));
});

test('DOI and arXiv versions join across a shared bridge record', () => {
  const rows = [
    { id: 'doi:10.1000/example', title: 'Published title' },
    { id: '2401.12345', doi: '10.1000/example', title: 'Revised title' },
    { id: '2401.12345v1', title: 'Original title' },
  ];
  assert.equal(identity.groupPaperRecords(rows).length, 1);
  assert.equal(identity.groupPaperRecords([...rows].reverse()).length, 1);
});

test('equal titles cannot merge conflicting DOI or arXiv identities', () => {
  for (const ids of [['doi:10.1000/a', 'doi:10.1000/b'], ['2401.12345', '2401.54321']]) {
    assert.equal(identity.groupPaperRecords(ids.map((id) => ({ id, title: 'Introduction' }))).length, 2);
  }
});

test('empty titles remain separate and cannot create a coauthor relationship', () => {
  assert.equal(identity.groupPaperRecords([{}, {}]).length, 2);
});

test('shared placeholder IDs do not collapse distinct papers', () => {
  const rows = ['First work', 'Second work', 'First work'].map((title) => ({ id: '[待补充]', title }));
  assert.equal(identity.groupPaperRecords(rows).length, 2);
});

test('catalog counts a shared work once and keeps all recorded owners', () => {
  const people = ['one', 'two'].map((slug) => ({ slug, publications: [{ id: '2401.12345', title: 'Shared paper', year: 2024, coauthors: [] }] }));
  const rows = collectPublications(people);
  assert.equal(rows.length, 1);
  assert.deepEqual(rows[0].ownerSlugs, ['one', 'two']);
});

test('existing routes resolve and ghosts do not masquerade as detail pages', () => {
  assert.equal(entityRoute('/people/tang-qian').exists, true);
  assert.equal(entityRoute('/people/does-not-exist').exists, false);
  assert.equal(entityRoute('/people/Yefeng Shen').exists, false);
  assert.equal(entityRoute('/concepts/frobenius-manifold').label, 'Frobenius 流形');
  assert.equal(entityRoute('/people'), null);
  assert.equal(entityRoute('/people/tang-qian/#publications').exists, true);
});

test('local evidence paths and placeholders cannot be public links', () => {
  for (const input of ['None', 'file:../private.pdf', 'javascript:alert(1)', '']) assert.equal(publicSourceUrl(input), undefined);
  assert.equal(publicSourceUrl('https://arxiv.org/abs/2401.12345'), 'https://arxiv.org/abs/2401.12345');
});

test('archive-less legacy numbers cannot merge different papers', () => {
  assert.equal(identity.groupPaperRecords([
    { id: '9602001', title: 'Work in one archive' }, { id: '9602001', title: 'Different work elsewhere' },
  ]).length, 2);
});

test('coauthor counts join DOI/arXiv bridges once and require two distinct owners', () => {
  const a = { slug: 'a', publications: [
    { id: 'doi:10.1000/shared', title: 'Published title', year: 2024 },
    { id: '2401.12345', doi: '10.1000/shared', title: 'Revised title', year: 2024 },
  ] };
  const b = { slug: 'b', publications: [{ id: '2401.12345v1', title: 'Original title', year: 2024 }] };
  assert.equal(collectCoauthorship([a]).length, 0);
  const edges = collectCoauthorship([a, b]);
  assert.equal(edges.length, 1);
  assert.equal(edges[0].weight, 1);
  assert.deepEqual([edges[0].source, edges[0].target], ['a', 'b']);
});

test('matching titles, raw names and ambiguous numbers cannot create coauthor edges', () => {
  for (const ids of [['9602001', '9602001'], ['unknown-a', 'unknown-b'], ['2401.12345', '2401.54321']]) {
    const people = ids.map((id, i) => ({ slug: String(i), publications: [
      { id, title: 'Same title', year: 2024, coauthors: ['Same Name', String(1 - i)] },
    ] }));
    assert.equal(collectCoauthorship(people).length, 0);
  }
});

test('live counts ignore stale manual totals and count duplicate records once', () => {
  const person = { slug: 'a', activity: { total_papers: 999, published_count: 999 }, publications: [
    { id: '2401.12345', title: 'Shared', year: 2024, doi: '10.1000/shared' },
    { id: 'doi:10.1000/shared', title: 'Shared', year: 2024 },
  ] };
  assert.deepEqual(recordedPublicationStats(person), { total_papers: 1, published_count: 1, preprint_only_count: 0 });
});

test('graph does not invent age, prestige or manual coauthor counts', () => {
  const person = (slug) => ({ slug, name: { en: slug }, publications: [], career_timeline: [] });
  const a = { ...person('a'), tags: ['fields-medal'], activity: { total_papers: 999 },
    career_timeline: [{ type: 'position', period: '1980', role: 'professor' }] };
  const graph = buildPeopleGraph([a, person('b')], [{ source: 'a', target: 'b', type: 'coauthor', weight: 999 }]);
  assert.equal(graph.links.length, 0);
  assert.equal(graph.nodes[0].radius, graph.nodes[1].radius);
  assert.equal(graph.nodes[0].color, graph.nodes[1].color);
});

test('simulation mutation cannot corrupt source data or filtered link endpoints', () => {
  const source = { nodes: [{ id: 'a' }, { id: 'b' }], links: [{ source: 'a', target: 'b' }] };
  const first = simulationGraph(source);
  first.nodes[0].x = 17;
  first.nodes[0].y = 23;
  first.links[0].source = first.nodes[0];
  first.links[0].target = first.nodes[1];
  assert.equal(source.nodes[0].x, undefined);
  assert.equal(source.links[0].source, 'a');
  const filtered = { nodes: source.nodes.map(n => ({ ...n, opacity: 0.5 })), links: first.links };
  const next = simulationGraph(filtered, first);
  assert.equal(next.links[0].source, 'a');
  assert.equal(next.links[0].target, 'b');
  assert.equal(next.nodes[0].x, 17);
  assert.equal(next.nodes[0].opacity, 0.5);
  assert.notEqual(next.nodes[0], first.nodes[0]);
  assert.equal(simulationGraph({ nodes: [source.nodes[0]], links: first.links }, first).links.length, 0);
});

test('multiline math renders without rewriting the generated MathML', () => {
  const html = renderMathText('**说明**\n$F(t)$\n$\\frac{a}{b}\n= c$\n$$x^2\n+y^2$$');
  assert.equal((html.match(/class="katex"/g) || []).length, 3);
  assert.match(html, /<strong>说明<\/strong>/);
  assert.match(html, /<annotation encoding="application\/x-tex">\\frac\{a\}\{b\}\n= c<\/annotation>/);
  assert.doesNotMatch(html, /katex-error/);
});

test('math prose is escaped and untrusted TeX cannot inject links or HTML', () => {
  const html = renderMathText('<img src=x onerror=alert(1)> \\$5 **safe** $\\href{javascript:alert(1)}{link}$');
  assert.match(html, /&lt;img/);
  assert.match(html, /\$5/);
  assert.doesNotMatch(html, /<img|<a\s|href="javascript:/);
  assert.match(renderMathText('$\\frac{$'), /katex-error/);
});


test('year cutoff excludes unknown/future dates but retains historical records after death or departure', () => {
  const person = (slug, extras = {}) => ({ slug, name: { en: slug }, publications: [], career_timeline: [], ...extras });
  const people = [person('unknown', { born: 1900 }),
    person('future', { career_timeline: [{ period: '2025-present' }] }),
    person('past', { died: 1990, career_timeline: [{ period: '1970-1980' }] }),
    person('paper-only', { publications: [{ id: 'math/9501001', title: 'Work', year: 1995 }] }),
    person('edge-only'), person('missing-start', { career_timeline: [{ period: '[?]-1980' }] })];
  const graph = buildPeopleGraph(people, [
    { source: 'past', target: 'edge-only', type: 'advisor-student', period: '1980-1985' },
    { source: 'unknown', target: 'past', type: 'grant' },
    { source: 'past', target: 'future', type: 'co-student', year: 2025 },
  ]);
  const before = JSON.stringify(graph);
  const cut = filterByYear(graph, 2000);
  assert.deepEqual(cut.nodes.map(n => n.id).sort(), ['edge-only', 'paper-only', 'past']);
  assert.equal(cut.links.length, 1);
  assert.equal(cut.links[0].type, 'advisor-student');
  assert.equal(JSON.stringify(graph), before);
  assert.equal(filterByYear(graph, null), graph);
  for (const value of [undefined, '[待核实]', '[?]-1980', 'nineteen eighty', 0, Infinity]) {
    assert.equal(recordedStartYear(value), null);
  }
  for (const value of ['~1980-1990', 'circa 1980', '1980-05-01', 1980]) assert.equal(recordedStartYear(value), 1980);
});

test('historical graph counts and node sizes cannot contain future coauthored papers', () => {
  const publications = [
    { id: 'math/9901001', title: 'Earlier', year: 1999 },
    { id: 'math/0001001', title: 'Cutoff', year: 2000, doi: '10.1000/cutoff' },
    { id: '2501.12345', title: 'Future', year: 2025 },
  ];
  const people = ['a', 'b'].map(slug => ({ slug, name: { en: slug }, publications }));
  const graph = buildPeopleGraph(people, collectCoauthorship(people));
  assert.equal(graph.links[0].weight, 3);
  const cut = filterByYear(graph, 2000);
  assert.equal(cut.links[0].weight, 2);
  assert.equal(cut.links[0].label, '2');
  assert.equal(cut.links[0].data.coauthored_papers.published.length, 1);
  assert.equal(cut.links[0].data.coauthored_papers.preprint.length, 1);
  assert.equal(cut.links[0].data.period, '1999-2000');
  assert.ok(cut.nodes[0].radius < graph.nodes[0].radius);
  assert.equal(graph.links[0].weight, 3);
  assert.equal(filterByYear(graph, 1998).nodes.length, 0);
  assert.equal(filterByYear(graph, 1998).links.length, 0);
});

test('affiliation filters retain recorded past visits and education without guessing a current employer', () => {
  const person = { career_timeline: [
    { institution: 'old', type: 'education', period: '1990-1995' },
    { institution: 'visit', type: 'visit', period: '1998' },
    { institution: 'old', type: 'position', period: '2000-2010' },
    { institution: 'future', type: 'position', period: '2025-present' },
    { institution: 'unknown', type: 'position', period: '[待核实]' },
  ] };
  assert.deepEqual(recordedInstitutions(person), ['old', 'visit', 'future', 'unknown']);
  assert.deepEqual(recordedInstitutions(person, 2000), ['old', 'visit']);
  assert.deepEqual(recordedInstitutions(person, 1980), []);
});


test('repository records and DOI deposits are not themselves publication clues', () => {
  for (const journal of ['arXiv (Cornell University)', 'ArXiv.org', 'SSRN Electronic Journal',
    'cIRcle (University of British Columbia)', 'Institutional Repositories DataBase (IRDB)',
    'Repository for Publications and Research Data (ETH Zurich)',
    'Kyoto University Research Information Repository (Kyoto University)']) {
    assert.equal(publicationMetadata({ journal }).hasPublicationClue, false, journal);
  }
  for (const doi of ['10.48550/arXiv.2601.12345', '10.2139/ssrn.4516041',
    '10.14288/1.0377037', '10.24546/81001100', '10.3929/ethz-b-000482826']) {
    const metadata = publicationMetadata({ doi });
    assert.equal(metadata.hasPublicationClue, false, doi);
    assert.equal(metadata.repositoryDoi, true);
    assert.ok(metadata.doiUrl.startsWith('https://doi.org/'));
  }
});

test('published citations mentioning arXiv and publisher DOIs with repository venues retain clues', () => {
  for (const journal of [
    'Duke Math. J. 139 (2007), no. 2, 369-405 (section 6 is not in this 2002 arxiv version)',
    'Lecture Notes in mathematics vol. 2060, Springer Verlag, 2012. (Numbering on the arXiv version changed)',
    'Rokko Lectures in Mathematics 7 (2000), 91-100',
  ]) assert.equal(publicationMetadata({ journal }).hasPublicationClue, true);
  for (const doi of ['10.1017/fmp.2021.3', '10.1093/oso/9780198802020.003.0017']) {
    assert.equal(publicationMetadata({ doi, journal: 'ArXiv.org' }).hasPublicationClue, true);
  }
  assert.equal(publicationMetadata({ journal: 'Rokko Lectures in Mathematics 7', doi: '10.24546/81001100' }).hasPublicationClue, true);
});

test('empty or malformed metadata cannot create publication clues or invalid DOI links', () => {
  for (const value of ['', 'None', 'null', 'N/A', '[待核实]']) {
    assert.equal(publicationMetadata({ doi: value, journal: value }).hasPublicationClue, false);
  }
  for (const doi of ['garbage', 'javascript:alert(1)', '10.1000/with space', '10.1000/<tag>']) {
    assert.equal(publicationMetadata({ doi }).doiUrl, undefined);
  }
  assert.equal(publicationMetadata({ doi: 'https://doi.org/10.1000/ABC' }).doiUrl, 'https://doi.org/10.1000/abc');
  assert.equal(publicationMetadata({ id: 'doi:10.1000/test?x#y' }).doiUrl, 'https://doi.org/10.1000/test%3Fx%23y');
});

test('catalog selection, person totals and coauthor buckets use the same publication clues', () => {
  const repository = { id: '2601.12345', title: 'Shared work', year: 2026, journal: 'ArXiv.org' };
  const citation = { ...repository, journal: 'A real journal 12 (2026)' };
  const a = { slug: 'a', publications: [repository, citation] };
  const b = { slug: 'b', publications: [repository] };
  for (const people of [[a, b], [b, a]]) {
    const papers = collectPublications(people);
    assert.equal(papers.length, 1);
    assert.equal(papers[0].journal, citation.journal);
    const edge = collectCoauthorship(people)[0];
    assert.equal(edge.coauthored_papers.published.length, 1);
    assert.equal(edge.coauthored_papers.preprint.length, 0);
  }
  assert.deepEqual(recordedPublicationStats(a), { total_papers: 1, published_count: 1, preprint_only_count: 0 });
  assert.deepEqual(recordedPublicationStats(b), { total_papers: 1, published_count: 0, preprint_only_count: 1 });
  const edge = collectCoauthorship([b, { ...b, slug: 'c' }])[0];
  assert.equal(edge.coauthored_papers.published.length, 0);
  assert.equal(edge.coauthored_papers.preprint.length, 1);
});


test('paper-title math remains inline inside links, including display delimiters', () => {
  const source = String.raw`DAHA of type $\check{C_1}C_1$ and $$\mathbb{P}^2$$`;
  const html = renderMathText(source, { inline: true });
  assert.equal((html.match(/class="katex"/g) || []).length, 2);
  assert.doesNotMatch(html, /<div|katex-display|katex-error/);
  assert.match(html, /DAHA of type/);
  assert.match(renderMathText('$$x^2$$'), /katex-display/);
});

test('inline title rendering keeps HTML and TeX links untrusted', () => {
  const html = renderMathText(String.raw`<script>alert(1)</script> $\href{javascript:alert(2)}{x}$`, { inline: true });
  assert.match(html, /&lt;script&gt;/);
  assert.doesNotMatch(html, /<script|<a\s|href="javascript:/);
});
