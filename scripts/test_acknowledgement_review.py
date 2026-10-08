"""[Codex] Regression cases for false identity/subject binding and stale reviews."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from acknowledgement_review import ack_hash, acknowledgement_errors, reviewed_edges

SPEC = importlib.util.spec_from_file_location('ack_match', Path(__file__).with_name('match-acks-to-people.py'))
MATCHER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MATCHER)


class AcknowledgementReviewTests(unittest.TestCase):
    def setUp(self):
        self.people = {
            'a': {'name': {'en': 'First Author'}, 'publications': [{'id': '2301.00001'}]},
            'b': {'name': {'en': 'Second Author'}, 'publications': [{'id': '2301.00001'}]},
            'target': {'name': {'en': 'Boris Dubrovin'}},
            'ding': {'name': {'en': 'Yanqiao Ding'}},
            'chen': {'name': {'en': 'Zhuo Chen'}},
            'chang': {'name': {'en': 'Huai-Liang Chang'}},
        }
        text = 'The second author thanks Boris Dubrovin.'
        self.raw = [{'arxiv_id': '2301.00001', 'ack_text': text, 'paper_authors': ['a', 'b']}]
        self.review = dict(source='b', target='target', paper='2301.00001', status='accepted',
                           quote=text, ack_sha256=ack_hash(text), reviewed_on='2026-10-08',
                           reviewed_by='Test', reason='Explicitly attributed.',
                           source_url='https://arxiv.org/html/2301.00001v2',
                           subject_note='Second author is b.', identity_note='Full identity checked.')

    def edges(self, reviews):
        result = reviewed_edges(self.raw, reviews, self.people)
        return result['edges'] + result['single_mentions']

    def test_same_surname_and_initials_never_bind(self):
        for text in ['We thank Weiyue Ding, Bohui Chen and Alice Chang.',
                     'We thank K. C. Chang and B. Dubrovin.', 'Thanks to Dubrovin.']:
            self.assertEqual(MATCHER.full_name_leads(text, self.people), {})
        self.assertEqual(MATCHER.full_name_leads('Thanks to Boris Dubrovin.', self.people),
                         {'target': ['Boris Dubrovin']})

    def test_full_name_alone_never_publishes(self):
        self.assertEqual(self.edges([]), [])
        edge = self.edges([self.review])[0]
        self.assertEqual((edge['source'], edge['target']), ('b', 'target'))
        self.assertEqual(edge['papers'], ['2301.00001'])
        # The first author is not credited with the second author's statement.
        self.assertNotEqual(edge['source'], 'a')

    def test_pending_and_rejected_do_not_publish(self):
        for status in ['rejected', 'needs-review']:
            self.assertEqual(self.edges([{**self.review, 'status': status}]), [])

    def test_stale_or_unsupported_evidence_blocks(self):
        changes = [('ack_sha256', '0' * 64), ('quote', 'Invented sentence'),
                   ('subject_note', ''), ('identity_note', ''), ('source', 'missing'),
                   ('target', 'b'), ('source_url', 'https://example.org'),
                   ('source_url', 'https://arxiv.org/abs/2301.99999'),
                   ('reviewed_on', '2026-02-30'), ('status', 'probably')]
        for key, value in changes:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                self.edges([{**self.review, key: value}])

    def test_duplicate_and_conflicting_decisions_block(self):
        for row in [self.review, {**self.review, 'status': 'rejected'}]:
            with self.assertRaises(ValueError):
                self.edges([self.review, row])
        with self.assertRaises(ValueError):
            reviewed_edges(self.raw * 2, [], self.people)

    def test_author_removed_from_bibliography_requires_review(self):
        self.people['b']['publications'] = []
        with self.assertRaises(ValueError):
            self.edges([self.review])

    def test_count_is_distinct_papers_not_repeated_name_occurrences(self):
        self.raw[0]['ack_text'] += ' Thanks again to Boris Dubrovin.'
        self.review['ack_sha256'] = ack_hash(self.raw[0]['ack_text'])
        self.assertEqual(self.edges([self.review])[0]['weight'], 1)
        second = copy.deepcopy(self.raw[0]); second['arxiv_id'] = '2301.00002'
        self.raw.append(second)
        self.people['b']['publications'].append({'id': '2301.00002v3'})
        review = {**self.review, 'paper': '2301.00002', 'source_url': 'https://arxiv.org/abs/2301.00002'}
        result = reviewed_edges(self.raw, [self.review, review], self.people)
        self.assertEqual(result['edges'][0]['weight'], 2)
        self.assertEqual(result['single_mentions'], [])

    def test_reference_and_comment_names_do_not_become_leads(self):
        for text in [r'We thank the referee. \cite{Boris Dubrovin}',
                     'We thank the referee. % Boris Dubrovin',
                     r'We thank the referee. \citep[see][p. 3]{Boris Dubrovin}']:
            self.assertEqual(MATCHER.full_name_leads(text, self.people), {})

    def test_ambiguous_registry_names_do_not_choose_person(self):
        self.people['homonym'] = {'name': {'en': 'Boris Dubrovin'}}
        self.assertEqual(MATCHER.full_name_leads('Thanks to Boris Dubrovin.', self.people), {})

    def test_live_evidence_and_known_false_bindings(self):
        root = Path(__file__).resolve().parent.parent
        people = {p.stem: yaml.safe_load(p.read_text()) for p in (root / 'data/people').glob('*.yaml')}
        self.assertEqual(acknowledgement_errors(root, people), [])
        rows = [json.loads(s) for s in (root / 'data/derived/raw-acks.jsonl').read_text().splitlines()]
        paper = next(r for r in rows if r['arxiv_id'] == '0712.4021')
        leads = MATCHER.full_name_leads(paper['ack_text'], people)
        for slug in ['ding-yanqiao', 'chen-zhuo', 'zhang-huailiang']:
            self.assertNotIn(slug, leads)

    def test_materialized_backfill_and_stale_raw_text_are_rejected(self):
        scratch = Path(__file__).resolve().parent.parent / '.cache/msa/ack-tests'
        scratch.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=scratch) as work:
            directory = Path(work) / 'data/derived'
            directory.mkdir(parents=True)
            raw_file = directory / 'raw-acks.jsonl'
            raw_file.write_text(json.dumps(self.raw[0]) + '\n')
            (directory / 'ack-reviews.yaml').write_text(yaml.safe_dump({'reviews': [self.review]}))
            output = reviewed_edges(self.raw, [self.review], self.people)
            out_file = directory / 'acknowledgements.yaml'
            out_file.write_text(yaml.safe_dump(output))
            self.assertEqual(acknowledgement_errors(work, self.people), [])
            output['single_mentions'].append({**output['single_mentions'][0], 'source': 'a'})
            out_file.write_text(yaml.safe_dump(output))
            self.assertTrue(acknowledgement_errors(work, self.people))
            out_file.write_text(yaml.safe_dump(reviewed_edges(self.raw, [self.review], self.people)))
            raw_file.write_text(json.dumps({**self.raw[0], 'ack_text': 'Changed source.'}) + '\n')
            self.assertTrue(acknowledgement_errors(work, self.people))


if __name__ == '__main__':
    unittest.main()
