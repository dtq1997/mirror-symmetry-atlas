"""[Codex] Regression cases for wrong-paper and permanently poisoned lookups."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import lib_truth as truth


def atom(aid='2602.21532v1', names=('Si-Qi Liu', 'Youjin Zhang'), title='Example'):
    from xml.sax.saxutils import escape
    return ('<feed xmlns="http://www.w3.org/2005/Atom"><entry>'
            f'<id>https://arxiv.org/abs/{escape(aid)}</id><title>{escape(title)}</title>'
            + ''.join(f'<author><name>{escape(name)}</name></author>' for name in names)
            + '</entry></feed>')


def crossref(doi='10.1000/one', authors=None):
    return json.dumps({'status': 'ok', 'message': {'DOI': doi, 'author': authors if authors is not None else [
        {'given': 'Si-Qi', 'family': 'Liu'}, {'given': 'Youjin', 'family': 'Zhang'}]}})


class TruthTests(unittest.TestCase):
    def setUp(self):
        parent = Path(truth.ROOT) / '.cache/msa/site-tests'
        parent.mkdir(parents=True, exist_ok=True)
        self.directory = tempfile.TemporaryDirectory(dir=parent)
        self.addCleanup(self.directory.cleanup)
        for source in ('ARXIV', 'CROSSREF', 'OPENALEX'):
            folder = Path(self.directory.name) / source
            folder.mkdir()
            self.enterContext(patch.object(truth, f'{source}_CACHE', str(folder)))
        self.enterContext(patch.object(truth.time, 'sleep'))

    def test_http_error_body_and_timeout_are_unresolved(self):
        with patch.object(truth.subprocess, 'run', return_value=subprocess.CompletedProcess([], 22, '\n503\ttext/html', '503')):
            self.assertIsNone(truth._curl('https://example.org'))
        with patch.object(truth.subprocess, 'run', side_effect=subprocess.TimeoutExpired('curl', 30)):
            self.assertIsNone(truth._curl('https://example.org'))
        with patch.object(truth.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, 'ok\n200\tapplication/xml', '')) as run:
            self.assertEqual(truth._curl('https://example.org'), 'ok')
            self.assertNotIn('--noproxy', run.call_args.args[0])
            self.assertIn('--fail', run.call_args.args[0])
        with patch.object(truth.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '{}\n200\ttext/html', '')):
            with self.assertWarnsRegex(RuntimeWarning, 'content type'):
                self.assertIsNone(truth._curl('https://example.org', expected_type='json'))

    def test_api_error_wrong_id_partial_authors_and_empty_title_rejected(self):
        for body in ['<html/>', 'Rate exceeded', atom('errors#incorrect_id_format', ('arXiv api core',)),
                     atom('2602.99999v1'), atom(names=()), atom(names=('Si-Qi Liu', '')), atom(title='')]:
            with self.subTest(body=body), patch.object(truth, '_curl', return_value=body):
                self.assertIsNone(truth.fetch_arxiv_authors('2602.21532'))
        self.assertFalse(list(Path(truth.ARXIV_CACHE).rglob('v2/*.json')))

    def test_multiple_entries_rejected(self):
        body = atom().replace('</feed>', atom().split('<entry>')[1].replace('</feed>', '').join(['<entry>', '']) + '</feed>')
        with patch.object(truth, '_curl', return_value=body):
            self.assertIsNone(truth.fetch_arxiv_authors('2602.21532'))

    def test_legacy_number_never_guessed_from_owner_or_category(self):
        with patch.object(truth, '_curl') as request:
            self.assertIsNone(truth.fetch_arxiv_authors('9602001', 'math.DG', owner_hint='Anton Alekseev'))
            request.assert_not_called()

    def test_archive_name_and_version_survive(self):
        for aid in ['solv-int/9501001', 'math.AG/0301001']:
            with self.subTest(aid=aid), patch.object(truth, '_curl', return_value=atom(aid + 'v2')) as request:
                self.assertEqual(truth.fetch_arxiv_authors(aid + 'v1'), ['Si-Qi Liu', 'Youjin Zhang'])
                self.assertIn(aid, request.call_args.args[0])

    def test_old_positive_and_miss_cache_cannot_poison_new_source(self):
        old = Path(truth.ARXIV_CACHE) / '2602.21532.json'
        old.write_text(json.dumps(['Si Li']))
        miss = Path(str(old) + '.miss')
        miss.touch()
        with patch.object(truth, '_curl', return_value=atom()) as request:
            self.assertEqual(truth.fetch_arxiv_authors('2602.21532'), ['Si-Qi Liu', 'Youjin Zhang'])
            request.assert_called_once()
        self.assertTrue(miss.exists())
        self.assertEqual(json.loads(old.read_text()), ['Si Li'])

    def test_failure_is_retried_and_success_cached(self):
        with patch.object(truth, '_curl', side_effect=[None, atom()]) as request:
            self.assertIsNone(truth.fetch_arxiv_authors('2602.21532'))
            self.assertEqual(truth.fetch_arxiv_authors('2602.21532'), ['Si-Qi Liu', 'Youjin Zhang'])
            self.assertEqual(truth.fetch_arxiv_authors('2602.21532v3'), ['Si-Qi Liu', 'Youjin Zhang'])
            self.assertEqual(request.call_count, 2)
        record = json.loads(Path(truth._cache_file(truth.ARXIV_CACHE, '2602.21532')).read_text())
        self.assertEqual(record['key'], '2602.21532')
        self.assertEqual(len(record['response_sha256']), 64)

    def test_stale_wrong_source_wrong_key_future_and_corrupt_cache_refetched(self):
        path = Path(truth._cache_file(truth.ARXIV_CACHE, '2602.21532'))
        path.parent.mkdir()
        base = {'schema_version': 2, 'source': 'arxiv', 'key': '2602.21532',
                'retrieved_at': truth.time.time(), 'authors': ['Wrong']}
        variants = [{**base, 'retrieved_at': 0}, {**base, 'source': 'openalex'}, {**base, 'key': 'wrong'},
                    {**base, 'retrieved_at': truth.time.time() + 5000}, [], {'authors': ['Wrong']}]
        for record in variants:
            path.write_text(json.dumps(record))
            with self.subTest(record=record), patch.object(truth, '_curl', return_value=atom()) as request:
                self.assertEqual(truth.fetch_arxiv_authors('2602.21532'), ['Si-Qi Liu', 'Youjin Zhang'])
                request.assert_called_once()

    def test_archive_caches_cannot_collide(self):
        self.assertNotEqual(truth._cache_file(truth.ARXIV_CACHE, 'hep-th/9602001'),
                            truth._cache_file(truth.ARXIV_CACHE, 'dg-ga/9602001'))

    def test_crossref_requires_matching_doi_and_complete_authors(self):
        for body in [crossref('10.1000/other'), crossref(authors=[{'given': 'Si-Qi'}, {}]), '{}', '[]', None]:
            with self.subTest(body=body), patch.object(truth, '_curl', return_value=body):
                self.assertIsNone(truth.fetch_crossref_authors('10.1000/one'))
        with patch.object(truth, '_curl', return_value=crossref()):
            self.assertEqual(truth.fetch_crossref_authors('https://doi.org/10.1000/ONE'), ['Si-Qi Liu', 'Youjin Zhang'])

    def test_crossref_and_openalex_misses_are_not_permanent(self):
        for source, key, function, body in [
            ('CROSSREF', '10.1000/one', truth.fetch_crossref_authors, crossref()),
            ('OPENALEX', 'W123', truth.fetch_openalex_authors, json.dumps({'id': 'https://openalex.org/W123',
                 'authorships': [{'author': {'display_name': 'Si-Qi Liu'}}]})),
        ]:
            folder = Path(getattr(truth, source + '_CACHE'))
            (folder / ('10_1000_one.json.miss' if source == 'CROSSREF' else 'W123.json.miss')).touch()
            with patch.object(truth, '_curl', side_effect=[None, body]) as request:
                self.assertIsNone(function(key))
                self.assertTrue(function(key))
                self.assertEqual(request.call_count, 2)

    def test_openalex_requires_requested_identity(self):
        data = {'id': 'https://openalex.org/W123', 'doi': 'https://doi.org/10.1000/one',
                'authorships': [{'author': {'display_name': 'Si-Qi Liu'}}]}
        with patch.object(truth, '_curl', return_value=json.dumps(data)):
            self.assertIsNone(truth.fetch_openalex_authors('W999'))
            self.assertIsNone(truth.fetch_openalex_authors('10.1000/other'))
            self.assertEqual(truth.fetch_openalex_authors('W123'), ['Si-Qi Liu'])
            self.assertEqual(truth.fetch_openalex_authors('10.1000/one'), ['Si-Qi Liu'])

    def test_strict_lint_blocks_unresolved_instead_of_silent_success(self):
        import contextlib
        import importlib.util
        import io
        spec = importlib.util.spec_from_file_location('lint_data', Path(truth.ROOT) / 'scripts/lint-data.py')
        lint = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lint)
        person = {'slug': 'liu-siqi', 'name': {'en': 'Siqi Liu'}, 'nationality': 'Chinese',
                  'publications': [{'id': '2602.21532', 'title': 'Example', 'year': 2026, 'coauthors': []}]}
        output = io.StringIO()
        with patch.object(lint, 'load_yaml_dir', side_effect=[{'liu-siqi': person}, {}]), \
             patch.object(truth, 'get_actual_authors', return_value=(None, None)), contextlib.redirect_stdout(output):
            self.assertEqual(lint.lint(strict_pubs=True, only_slug='liu-siqi'), 1)
        self.assertIn('unresolved source lookup; not checked', output.getvalue())

    def test_prefixed_id_lookup_and_unknown_are_explicit(self):
        with patch.object(truth, 'fetch_crossref_authors', return_value=['Name']) as request:
            self.assertEqual(truth.get_actual_authors({'id': 'doi:10.1000/one'}), (['Name'], 'crossref'))
            request.assert_called_once_with('10.1000/one')
        with patch.object(truth, 'fetch_openalex_authors', return_value=['Name']) as request:
            self.assertEqual(truth.get_actual_authors({'id': 'openalex:W123'}), (['Name'], 'openalex'))
            request.assert_called_once_with('W123')
        self.assertEqual(truth.get_actual_authors({'id': 'unknown'}), (None, None))


if __name__ == '__main__':
    unittest.main()
