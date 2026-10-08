"""[Codex] Adversarial checks for reviewed funding, not source truth tests."""
import copy
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from acknowledgement_review import ack_hash
from grant_review import grant_errors, reviewed_grant_edges, valid_grant_number

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('extract_acks', ROOT / 'scripts/extract-acknowledgements.py')
extract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract)


class FundingReviewTests(unittest.TestCase):
    def setUp(self):
        self.paper = '2501.00001'
        self.raw = [{'arxiv_id': self.paper, 'paper_authors': ['a', 'b', 'c'],
                     'ack_text': 'Alice is supported by NSFC 12345678. Bob is supported by NSFC 12345678. This work is supported by NSFC 87654321.'}]
        self.people = {p: {'publications': [{'id': self.paper}]} for p in ['a', 'b', 'c']}
        self.reviews = [dict(person=p, paper=self.paper, agency='NSFC', number='12345678', status='accepted',
            ack_sha256=ack_hash(self.raw[0]['ack_text']), reviewed_on='2026-10-08', reviewed_by='Reviewer',
            reason='Reviewed source', source_url=f'https://arxiv.org/html/{self.paper}v1',
            author_name=name, full_author_order=['Alice', 'Bob', 'Carol'], subject_scope='named-recipient',
            identity_note='Reviewed identity', subject_note='Named recipient',
            quote=f'{name} is supported by NSFC 12345678.') for p, name in [('a', 'Alice'), ('b', 'Bob')]]

    def edges(self, reviews=None):
        return reviewed_grant_edges(self.raw, self.reviews if reviews is None else reviews, self.people)['edges']

    def test_only_reviewed_recipients_not_all_owners(self):
        edges = self.edges()
        self.assertEqual([(e['source'], e['target']) for e in edges], [('a', 'b')])
        evidence = edges[0]['funding_evidence'][0]
        self.assertEqual({r['person'] for r in evidence['recipients']}, {'a', 'b'})
        self.assertEqual(len(evidence['recipients']), 2)

    def test_one_recipient_does_not_form_link(self):
        self.assertEqual(self.edges(self.reviews[:1]), [])

    def test_pending_rejected_do_not_publish(self):
        for status in ['needs-review', 'rejected']:
            rows = copy.deepcopy(self.reviews)
            rows[1]['status'] = status
            self.assertEqual(self.edges(rows), [])

    def test_work_support_does_not_identify_authors(self):
        self.reviews[0].update(subject_scope='work', quote='This work is supported by NSFC 87654321.', number='87654321')
        with self.assertRaisesRegex(ValueError, 'work-level'):
            self.edges()

    def test_changed_source_invalidates_review(self):
        self.raw[0]['ack_text'] += ' New version.'
        with self.assertRaisesRegex(ValueError, 'changed'):
            self.edges()

    def test_invented_quote_and_substring_number_fail(self):
        for mutation in [{'quote': 'Carol is supported by NSFC 12345678.'}, {'number': '2345678'}]:
            rows = copy.deepcopy(self.reviews)
            rows[0].update(mutation)
            with self.assertRaisesRegex(ValueError, 'quote'):
                self.edges(rows)

    def test_missing_identity_scope_order_and_wrong_paper_fail(self):
        for mutation in [{'identity_note': ''}, {'subject_note': ''}, {'subject_scope': 'paper-owners'},
                         {'full_author_order': ['Bob']}, {'source_url': 'https://arxiv.org/html/9999.99999v1'}]:
            rows = copy.deepcopy(self.reviews)
            rows[0].update(mutation)
            with self.assertRaises(ValueError):
                self.edges(rows)

    def test_conflicting_order_duplicate_and_removed_owner_fail(self):
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.edges(self.reviews + self.reviews[:1])
        self.reviews[1]['full_author_order'].reverse()
        with self.assertRaisesRegex(ValueError, 'order'):
            self.edges()
        self.reviews[1]['full_author_order'].reverse()
        self.people['a']['publications'] = []
        with self.assertRaisesRegex(ValueError, 'bibliography'):
            self.edges()

    def test_different_agencies_do_not_join(self):
        self.reviews[1]['agency'] = 'another-agency'
        self.assertEqual(self.edges(), [])

    def test_different_papers_keep_both_sources(self):
        second = '2501.00002'
        self.raw.append({**self.raw[0], 'arxiv_id': second})
        self.people['b']['publications'].append({'id': second})
        self.reviews[1].update(paper=second, source_url=f'https://arxiv.org/html/{second}v2')
        evidence = self.edges()[0]['funding_evidence'][0]['recipients']
        self.assertEqual({e['paper'] for e in evidence}, {self.paper, second})

    def test_dry_run_does_not_write_output(self):
        output = ROOT / 'data/derived/grant-edges.yaml'
        before = output.read_bytes()
        run = subprocess.run(['python3', 'scripts/derive-grant-edges.py'], cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(json.loads(run.stdout)['mode'], 'read-only')
        self.assertEqual(output.read_bytes(), before)

    def test_materialized_output_cannot_backfill_or_expand_claim(self):
        cache = ROOT / '.cache/msa/site-tests'
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as tmp:
            root = Path(tmp)
            directory = root / 'data/derived'
            directory.mkdir(parents=True)
            (directory / 'raw-acks.jsonl').write_text('\n'.join(map(json.dumps, self.raw)))
            (directory / 'grant-reviews.yaml').write_text(yaml.safe_dump({'reviews': self.reviews}))
            expected = reviewed_grant_edges(self.raw, self.reviews, self.people)
            output = directory / 'grant-edges.yaml'
            output.write_text(yaml.safe_dump(expected))
            self.assertEqual(grant_errors(root, self.people), [])
            expected['edges'][0]['period'] = '2014-2018'
            output.write_text(yaml.safe_dump(expected))
            self.assertTrue(grant_errors(root, self.people))
            output.unlink()
            self.assertTrue(grant_errors(root, self.people))

    def test_plain_words_never_become_identifiers(self):
        for word in ['Scientific', 'Grant', 'Funded', 'Shandong', 'Central', '-1309118', '', None]:
            self.assertFalse(valid_grant_number(word))
        text = 'JSPS Grant-in-Aid for Scientific Research Grant 23K03102. China Postdoctoral Science Foundation Funded Project 2023M743717.'
        self.assertEqual(extract.extract_grants(text), [{'agency': 'CPSF', 'number': '2023M743717'}, {'agency': 'JSPS', 'number': '23K03102'}])

    def test_nsf_dms_prefix_preserved_nsfc_separate(self):
        self.assertEqual(extract.extract_grants('NSF grant DMS-1309118.'), [{'agency': 'NSF', 'number': 'DMS-1309118'}])
        self.assertEqual(extract.extract_grants('NSFC Grant 11831017.'), [{'agency': 'NSFC', 'number': '11831017'}])

    def test_preamble_comments_and_following_sections_not_ack(self):
        text = r'\newcommand{\ack}{\section{Acknowledgements}} \author{Name} \begin{document} \section{Intro} Hi'
        self.assertIsNone(extract.extract_ack(text))
        for ending in [r'\subsection{Next}', r'\input{Body}', r'\paragraph{Proof}']:
            text = r'\section{Acknowledgements} Alice is supported. ' + ending + ' Unrelated body'
            self.assertEqual(extract.extract_ack(text), 'Alice is supported.')
        text = r'\begin{comment}\section{Acknowledgements} Invisible.\end{comment}\section{Acknowledgements} Actual.\section{Next}'
        self.assertEqual(extract.extract_ack(text), 'Actual.')


if __name__ == '__main__':
    unittest.main()
