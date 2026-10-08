"""[Codex] Regression checks: an automatic run must not undo source review."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import yaml
from publication_review import record_keys, blocked_review, load_review, save_candidates

ROOT = Path(__file__).resolve().parent.parent


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class ReviewTests(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.cache/msa/review-tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.path = self.folder / 'example.yaml'
        self.review = {'id': '2401.12345v1', 'doi': '10.1000/example',
                       'openalex_id': 'W123', 'title': 'Original title',
                       'review_status': 'rejected-homonym', 'reviewed_by': 'Codex',
                       'source_urls': ['https://example.org/primary-source']}
        self.path.write_text(yaml.safe_dump({'slug': 'example', 'candidates': [self.review]}))

    def test_identifier_variants_respect_review(self):
        for pub in [{'id': '2401.12345v3'}, {'doi': 'https://doi.org/10.1000/EXAMPLE'},
                    {'id': 'doi:10.1000/example'}, {'id': 'openalex:W123'},
                    {'openalex_id': 'https://openalex.org/W123'}]:
            with self.subTest(pub=pub):
                self.assertEqual(blocked_review(pub, [self.review]), self.review)

    def test_titles_and_ambiguous_ids_cannot_reject_other_works(self):
        self.assertIsNone(blocked_review({'id': '2401.54321', 'title': 'Original title'}, [self.review]))
        self.assertEqual(record_keys({'id': '9602001', 'title': 'Same'}), set())
        self.assertNotEqual(record_keys({'id': 'math/9602001'}), record_keys({'id': 'hep-th/9602001'}))

    def test_empty_or_new_automatic_results_preserve_explicit_review(self):
        for fresh in [[], [{'id': 'openalex:W123', 'title': 'A new title'}], [{'id': '2401.54321'}]]:
            save_candidates(self.path, 'example', fresh)
            data = load_review(self.path)
            self.assertEqual(data['candidates'][0], self.review)
            self.assertEqual(data['count'], 1 + int(bool(fresh) and fresh[0]['id'] == '2401.54321'))

    def test_pending_blocks_but_accepted_review_can_release(self):
        pending = dict(self.review, review_status='needs-review')
        self.assertIsNotNone(blocked_review({'id': '2401.12345'}, [pending]))
        accepted = dict(self.review, review_status='accepted')
        self.assertIsNone(blocked_review({'id': '2401.12345'}, [accepted]))

    def test_malformed_review_cannot_be_overwritten(self):
        self.path.write_text('candidates: broken')
        with self.assertRaises(ValueError):
            save_candidates(self.path, 'example', [])
        self.assertEqual(self.path.read_text(), 'candidates: broken')

    def test_atomic_write_failure_retains_original_and_cleans_temp(self):
        before = self.path.read_bytes()
        with patch('publication_review.os.replace', side_effect=OSError('disk error')):
            with self.assertRaises(OSError):
                save_candidates(self.path, 'example', [{'id': '2401.54321'}])
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.folder.iterdir()), [self.path])

    def test_default_lint_blocks_restoration_only_for_reviewed_owner(self):
        lint = module('review_lint', 'lint-data.py')
        person = lambda slug: {'slug': slug, 'name': {'en': 'Example'}, 'nationality': 'Unknown',
                               'publications': [{'id': '2401.12345', 'title': 'Title', 'year': 2024, 'coauthors': []}]}
        for slug, expected in [('example', 1), ('other', 0)]:
            output = io.StringIO()
            with patch.object(lint, 'REVIEW_DIR', self.folder), \
                 patch.object(lint, 'load_yaml_dir', side_effect=[{slug: person(slug)}, {}]), \
                 contextlib.redirect_stdout(output):
                self.assertEqual(lint.lint(only_slug=slug), expected)
            if expected:
                self.assertIn('blocked by explicit review', output.getvalue())

    def test_enrichment_dry_run_is_read_only_and_scores_cannot_override_review(self):
        enrich = module('review_enrich', 'enrich-from-openalex-v2.py')
        person = {'name': {'en': 'Example'}, 'external_ids': {'openalex': 'A123'}, 'publications': []}
        before = self.path.read_bytes()
        for write in [False, True]:
            with patch.object(enrich, 'REVIEW_DIR', str(self.folder)), \
                 patch.object(enrich, 'fetch_works', return_value=[{}]), \
                 patch.object(enrich, 'to_pub', return_value={'id': 'openalex:W123'}), \
                 patch.object(enrich, 'score_candidate', return_value=('accept', 999, [])) as score:
                result = enrich.process('example', person, {}, write=write)
                self.assertEqual(result['oa_accepted'], 0)
                self.assertEqual(result['oa_rejected'], 1)
                score.assert_not_called()
            if not write:
                self.assertEqual(self.path.read_bytes(), before)
            self.assertEqual(load_review(self.path)['candidates'], [self.review])
        before = self.path.read_bytes()
        with patch.object(enrich, 'REVIEW_DIR', str(self.folder)), \
             patch.object(enrich, 'fetch_works', return_value=[{}]), \
             patch.object(enrich, 'to_pub', return_value={'id': '2401.54321'}), \
             patch.object(enrich, 'score_candidate', return_value=('review', 15, [])):
            self.assertEqual(enrich.process('example', person, {}, write=False)['oa_review'], 1)
        self.assertEqual(self.path.read_bytes(), before)

    def test_identity_whitelist_cannot_restore_blocked_records(self):
        lint = module('identity_review_lint', 'lint-data.py')
        for slug, aid, status, expected in [
            ('example', '2401.12345v2', 'rejected-homonym', 1),
            ('example', '2401.12345', 'needs-review', 1),
            ('example', '2401.12345', 'accepted', 0),
            ('other', '2401.12345', 'rejected-homonym', 0),
            ('example', '2401.54321', 'rejected-homonym', 0),
        ]:
            self.path.write_text(yaml.safe_dump({'candidates': [dict(self.review, review_status=status)]}))
            person = {'slug': slug, 'name': {'en': 'Example'}, 'nationality': 'Unknown',
                      'publications': [], 'identity_profile': {'known_arxiv_ids': [aid]}}
            output = io.StringIO()
            with self.subTest(slug=slug, aid=aid, status=status), \
                 patch.object(lint, 'REVIEW_DIR', self.folder), \
                 patch.object(lint, 'load_yaml_dir', side_effect=[{slug: person}, {}]), \
                 contextlib.redirect_stdout(output):
                self.assertEqual(lint.lint(only_slug=slug), expected)
            if expected:
                self.assertIn('identity_profile.known_arxiv_ids', output.getvalue())


if __name__ == '__main__':
    unittest.main()
