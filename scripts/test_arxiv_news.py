"""[Codex] Failure, pagination, identity and rerun regression tests; no network."""
import importlib.util
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import yaml

spec = importlib.util.spec_from_file_location('news', Path(__file__).with_name('fetch-arxiv-news.py'))
news = importlib.util.module_from_spec(spec)
spec.loader.exec_module(news)
NOW = datetime(2026, 10, 8, 12, tzinfo=timezone.utc)


def feed(ids=(), total=None, start=0):
    root = ET.Element(f"{{{news.NS['a']}}}feed")
    ET.SubElement(root, f"{{{news.NS['o']}}}totalResults").text = str(len(ids) if total is None else total)
    ET.SubElement(root, f"{{{news.NS['o']}}}startIndex").text = str(start)
    for aid in ids:
        entry = ET.SubElement(root, f"{{{news.NS['a']}}}entry")
        for key, text in [('id', f'http://arxiv.org/abs/{aid}'), ('title', 'Mirror symmetry'),
                          ('summary', 'An external calculation in mirror symmetry.'),
                          ('published', '2026-10-07T12:00:00Z'), ('updated', '2026-10-07T12:00:00Z')]:
            ET.SubElement(entry, f"{{{news.NS['a']}}}{key}").text = text
        author = ET.SubElement(entry, f"{{{news.NS['a']}}}author")
        ET.SubElement(author, f"{{{news.NS['a']}}}name").text = 'Ao Li'
        ET.SubElement(entry, f"{{{news.NS['arxiv']}}}primary_category", term='math.AG')
    return ET.tostring(root)


class NewsTests(unittest.TestCase):
    def test_http_failure_is_not_empty_success(self):
        with patch.object(news.subprocess, 'run', return_value=subprocess.CompletedProcess([], 22, b'', b'503')):
            with self.assertRaises(news.FetchError):
                news.request_feed('https://export.arxiv.org/api/query')

    def test_invalid_xml_and_api_error_fail(self):
        for body in [b'Rate exceeded', b'<html/>', feed(['errors#invalid']), feed([], total=1)]:
            with self.subTest(body=body), self.assertRaises(news.FetchError):
                news.parse_feed(body, 0)

    def test_legacy_archive_and_version(self):
        _, rows = news.parse_feed(feed(['solv-int/9501001v2']), 0)
        self.assertEqual(rows[0]['id'], 'solv-int/9501001')
        self.assertEqual(rows[0]['source_version'], 'solv-int/9501001v2')

    def test_complete_pagination_and_category_window_query(self):
        urls, sleeps = [], []
        def request(url):
            urls.append(url)
            return feed(['2610.00001v1'], 2, 0) if len(urls) == 1 else feed(['2610.00002v1'], 2, 1)
        rows, evidence = news.fetch_recent_papers(2, page_size=1, now=NOW, request=request, sleep=sleeps.append)
        self.assertEqual(len(rows), 2)
        self.assertEqual(evidence['total_fetched'], 2)
        self.assertIn('start=1', urls[1])
        self.assertIn('submittedDate', evidence['query'])
        self.assertIn('cat:math.AG OR', evidence['query'])
        self.assertEqual(sleeps, [4])

    def test_partial_page_failure_and_limit_abort(self):
        calls = []
        def request(url):
            calls.append(url)
            if len(calls) == 2:
                raise news.FetchError('network down')
            return feed(['2610.00001'], 2, 0)
        with self.assertRaises(news.FetchError):
            news.fetch_recent_papers(2, page_size=1, now=NOW, request=request, sleep=lambda _: None)
        with self.assertRaises(news.FetchError):
            news.fetch_recent_papers(2, page_size=1, max_pages=1, now=NOW,
                                     request=lambda _: feed(['2610.00001'], 2, 0))

    def test_wrong_offset_duplicate_changed_total_and_outside_window_fail(self):
        for second in [feed(['2610.00002'], 2, 0), feed(['2610.00001'], 2, 1), feed(['2610.00002'], 3, 1)]:
            pages = iter([feed(['2610.00001'], 2, 0), second])
            with self.subTest(second=second), self.assertRaises(news.FetchError):
                news.fetch_recent_papers(2, page_size=1, now=NOW, request=lambda _: next(pages), sleep=lambda _: None)
        with self.assertRaises(news.FetchError):
            news.fetch_recent_papers(1, now=NOW.replace(day=9), request=lambda _: feed(['2610.00001']))

    def test_homonyms_remain_candidates_never_bound(self):
        people = {'first': {'name_en': 'Ao Li'}, 'second': {'name_en': 'Ao Li'},
                  'different': {'name_en': 'Chien-Hao Liu'}}
        self.assertEqual(news.author_candidates('Ao Li', people), ['first', 'second'])
        self.assertEqual(news.author_candidates('Li', people), [])
        self.assertEqual(news.author_candidates('A. Li', people), [])
        _, rows = news.parse_feed(feed(['2610.00001']), 0)
        entry = news.news_entry(rows[0], people, set(), NOW.isoformat(), 3)
        self.assertEqual(entry['matched_people'], [])
        self.assertEqual(entry['candidate_people'], ['first', 'second'])
        self.assertEqual(entry['authors_raw'], ['Ao Li'])
        self.assertEqual(entry['summary_zh'], '')

    def test_concept_substrings_and_unordered_words_do_not_match(self):
        self.assertEqual(news.match_concepts('External quantum effect', 'a cohomology course', {'rna', 'quantum-cohomology'}), [])
        self.assertEqual(news.match_concepts('Quantum cohomology and Gromov–Witten theory', '',
                                            {'quantum-cohomology', 'gromov-witten-theory'}),
                         ['gromov-witten-theory', 'quantum-cohomology'])

    def test_same_day_rerun_preserves_curated_content_and_adds_new(self):
        cache = news.ROOT / '.cache/msa/site-tests'
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as directory:
            output = Path(directory) / '2026-10-08.yaml'
            old = {'id': '2610.00001', 'date': '2026-10-07', 'summary_zh': '人工摘要', 'review_status': 'abstract-reviewed'}
            output.write_text(yaml.safe_dump({'entries': [old]}))
            new = {'id': '2610.00002', 'date': '2026-10-07', 'review_status': 'metadata-only'}
            evidence = {'total_fetched': 2}
            news.write_update(output, [{**old, 'id': '2610.00001v2', 'summary_zh': '覆盖'}, new], evidence, NOW, 7, 14)
            news.write_update(output, [], evidence, NOW, 7, 14)
            rows = news.read_news(output)['entries']
            self.assertEqual(len(rows), 2)
            self.assertEqual(next(e for e in rows if e['id'] == old['id'])['summary_zh'], '人工摘要')

    def test_malformed_existing_input_preserves_file(self):
        cache = news.ROOT / '.cache/msa/site-tests'
        cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as directory:
            output = Path(directory) / '2026-10-08.yaml'
            output.write_text('entries: []\n')
            (output.parent / '2026-10-07.yaml').write_text('entries: bad\n')
            before = output.read_bytes()
            with self.assertRaises(news.FetchError):
                news.write_update(output, [], {'total_fetched': 0}, NOW, 7, 14)
            self.assertEqual(before, output.read_bytes())

    def test_main_network_failure_does_not_create_output(self):
        output = news.ROOT / '.cache/msa/site-tests/should-not-exist.yaml'
        self.assertFalse(output.exists())
        with patch.object(news.sys, 'argv', ['fetch', '--output', str(output)]), \
             patch.object(news, 'fetch_recent_papers', side_effect=news.FetchError('network')):
            self.assertEqual(news.main(), 1)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
