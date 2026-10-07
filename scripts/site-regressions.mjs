// [Codex] Regression checks for broken public links and incorrect paper grouping.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import identity from '../.cache/msa/site-tests/paper-identity.js';
import { entityRoute } from '../.cache/msa/site-tests/entity-route.js';
import { buildPeopleGraph, simulationGraph } from '../.cache/msa/site-tests/graph.js';
import { publicSourceUrl } from '../.cache/msa/site-tests/source-url.js';
import { renderMathText } from '../.cache/msa/site-tests/math-text.js';
import { collectPublications, collectCoauthorship, recordedPublicationStats } from '../.cache/msa/site-tests/publications.js';

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
