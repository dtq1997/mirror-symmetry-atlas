// [Codex] Search is a view over existing records, never identity evidence.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import yaml from 'js-yaml';
import { indexCatalog, filterCatalog, catalogWindow, emptyCatalogFilters } from '../.cache/msa/site-tests/catalog-search.js';
import { collectPublications } from '../.cache/msa/site-tests/publications.js';
import { publicationMetadata } from '../.cache/msa/site-tests/publication-metadata.js';
import { canonicalArxivId, publicationUrl } from '../.cache/msa/site-tests/paper-identity.js';
import { entityRoute } from '../.cache/msa/site-tests/entity-route.js';
import { renderMathText } from '../.cache/msa/site-tests/math-text.js';

const paper = (id, fields = {}) => ({ id, title: `Paper ${id}`, year: 2025, coauthors: [], ...fields });
const people = [
  { slug: 'liu-xiaobo', publications: [paper('2501.00001', {
    title: 'Frobenius structures on $\\mathbb{P}^1$', doi: '10.1234/ABC.7', journal: 'Geometry Journal', coauthors: ['Anna Müller'],
  }), paper('math/0301001', { title: '复几何与变形', year: 2003, journal: 'arXiv' })] },
  { slug: 'liu-siqi', publications: [paper('2501.00002', { title: 'A different subject', coauthors: ['Xiaobo Liu'], doi: '10.48550/arXiv.2501.00002' }),
    paper('hep-th/0301001', { title: 'Another legacy record', year: 2003 })] },
];
const catalog = collectPublications(people);
const index = indexCatalog(catalog);
const search = (patch) => filterCatalog(index, { ...emptyCatalogFilters, ...patch }).map((p) => p.id);

test('catalog searches bilingual names, raw authors, accents, math titles and Chinese without binding names', () => {
  assert.deepEqual(search({ query: '刘小博 frobenius' }), ['2501.00001']);
  assert.deepEqual(search({ query: 'XIAOBO LIU' }).sort(), ['2501.00001', '2501.00002', 'math/0301001'].sort());
  assert.deepEqual(search({ query: 'Xiaobo Liu', owner: 'liu-xiaobo', year: '2025' }), ['2501.00001']);
  assert.deepEqual(search({ query: 'muller P 1' }), ['2501.00001']);
  assert.deepEqual(search({ query: '复几何' }), ['math/0301001']);
  assert.deepEqual(search({ query: 'Geometry Journal' }), ['2501.00001']);
  assert.deepEqual(search({ query: 'another', owner: 'liu-xiaobo' }), []);
});

test('complete arXiv and DOI queries match exact keys, normalize prefixes/versions and retain archive distinctions', () => {
  for (const query of ['2501.00001', 'arXiv:2501.00001v3', 'https://arxiv.org/abs/2501.00001v2',
    '10.1234/abc.7', 'DOI:10.1234/ABC.7', 'https://doi.org/10.1234/ABC.7']) {
    assert.deepEqual(search({ query }), ['2501.00001'], query);
  }
  assert.deepEqual(search({ query: '10.48550/arxiv.2501.00002' }), ['2501.00002']);
  assert.deepEqual(search({ query: 'math/0301001v4' }), ['math/0301001']);
  assert.deepEqual(search({ query: 'hep-th/0301001' }), ['hep-th/0301001']);
  assert.deepEqual(search({ query: '0301001' }), []);
  assert.deepEqual(search({ query: '10.1234/abc' }), []);
  assert.deepEqual(search({ query: '2501.00003' }), []);
});

test('merged records remain findable by identifiers absent from the chosen display row', () => {
  const records = [{ slug: 'a', publications: [paper('2501.00005', { doi: '10.5555/bridge' })] },
    { slug: 'b', publications: [paper('doi:10.5555/bridge', { journal: 'Journal', title: 'Retained title' })] }];
  const before = structuredClone(records);
  const groups = collectPublications(records);
  assert.equal(groups.length, 1);
  assert.equal(groups[0].id, 'doi:10.5555/bridge');
  assert.deepEqual(filterCatalog(indexCatalog(groups), { ...emptyCatalogFilters, query: '2501.00005v4' }), groups);
  assert.deepEqual(groups[0].ownerSlugs, ['a', 'b']);
  assert.deepEqual(records, before);
});

test('English name search cannot match Qian inside Weiqiang or Tang inside Tangent', () => {
  const rows = collectPublications([{ slug: 'unlisted', publications: [
    paper('2501.00011', { coauthors: ['Weiqiang He', 'Xinxing Tang'] }),
    paper('2501.00012', { coauthors: ['Qian Tangent'] }),
    paper('2501.00013', { coauthors: ['Qian Tang'] }),
  ] }]);
  assert.deepEqual(filterCatalog(indexCatalog(rows), { ...emptyCatalogFilters, query: 'Qian Tang' }).map(p => p.id), ['2501.00013']);
});

test('combined filters use recorded ownership, exact years and the shared publication-clue classifier', () => {
  assert.deepEqual(search({ year: '2003', owner: 'liu-xiaobo', publication: 'needs-clues' }), ['math/0301001']);
  assert.deepEqual(search({ publication: 'with-clues' }), ['2501.00001']);
  assert.equal(search({ publication: 'needs-clues' }).length, 3);
  assert.deepEqual(search({ query: '2501.00002', publication: 'with-clues' }), []);
  assert.deepEqual(search({ year: '2024' }), []);
  assert.deepEqual(search({ owner: 'unknown' }), []);
});

test('empty/punctuation searches, reset, display increments and final partial group preserve order and input', () => {
  const before = structuredClone(catalog);
  assert.equal(search({ query: '  \t ' }).length, catalog.length);
  assert.deepEqual(search({ query: '+++$' }), []);
  assert.deepEqual(search({ query: 'impossible no matches' }), []);
  assert.deepEqual(filterCatalog(index, emptyCatalogFilters), catalog);
  const many = Array.from({ length: 122 }, (_, i) => ({ ...catalog[0], catalogKey: String(i) }));
  for (const [limit, count, next] of [[50, 50, 50], [100, 100, 22], [150, 122, 0]]) {
    const view = catalogWindow(many, limit);
    assert.equal(view.visible.length, count);
    assert.equal(view.total, 122);
    assert.equal(view.nextCount, next);
    assert.deepEqual(view.visible.map((p) => p.catalogKey), many.slice(0, count).map((p) => p.catalogKey));
  }
  assert.deepEqual(catalogWindow([], 50), { visible: [], total: 0, nextCount: 0 });
  assert.deepEqual(catalog, before);
});

test('all catalog records remain searchable and all hidden titles and person destinations are checked', () => {
  const sourcePeople = readdirSync('data/people').filter((f) => /\.yaml$/.test(f) && !f.startsWith('_'))
    .map((f) => yaml.load(readFileSync(`data/people/${f}`, 'utf8')));
  const before = structuredClone(sourcePeople);
  const papers = collectPublications(sourcePeople);
  const indexed = indexCatalog(papers);
  assert.equal(indexed.length, papers.length);
  assert.equal(new Set(papers.map((p) => p.catalogKey)).size, papers.length);
  assert.deepEqual(filterCatalog(indexed, emptyCatalogFilters), papers);
  for (const p of papers) {
    assert.doesNotMatch(renderMathText(p.title, { inline: true }), /katex-error/, p.title);
    assert.ok(filterCatalog(indexed, { ...emptyCatalogFilters, query: p.title }).includes(p), p.title);
    for (const owner of p.ownerSlugs) assert.equal(entityRoute(`/people/${owner}`)?.exists, true, owner);
    const url = publicationUrl(p);
    if (url) assert.match(url, /^https:\/\/(?:arxiv\.org\/abs\/|doi\.org\/|openalex\.org\/W)/);
    for (const identifier of p.identifiers) {
      if (!canonicalArxivId(identifier) && !publicationMetadata({ doi: identifier }).doi) continue;
      assert.ok(filterCatalog(indexed, { ...emptyCatalogFilters, query: identifier }).includes(p), identifier);
    }
  }
  assert.deepEqual(sourcePeople, before);
});
