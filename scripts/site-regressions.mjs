// [Codex] Regression checks for broken public links and incorrect paper grouping.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import identity from '../.cache/msa/site-tests/paper-identity.js';
import { entityRoute } from '../.cache/msa/site-tests/entity-route.js';
import { publicSourceUrl } from '../.cache/msa/site-tests/source-url.js';
import { collectPublications } from '../.cache/msa/site-tests/publications.js';

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
