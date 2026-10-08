"""[Codex] Guard visible arXiv labels against unrelated external targets."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('site_audit', Path(__file__).with_name('audit-site.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def errors(html):
    document = module.Document()
    document.feed(html)
    return document.arxiv_label_errors


class IdentifierTargetTests(unittest.TestCase):
    def test_doi_wrong_paper_and_lookalike_host_do_not_satisfy_arxiv_label(self):
        for href in ('https://doi.org/10.4310/pamq.260122023941',
                     'https://arxiv.org/abs/2010.14338',
                     'https://arxiv.org.example.com/abs/2010.14339'):
            with self.subTest(href=href):
                self.assertEqual(len(errors(f'<a href="{href}"><span>2010.14339</span> ↗</a>')), 1)

    def test_same_paper_versions_pdf_and_legacy_archives_are_accepted(self):
        for label, href in [
            ('2010.14339v2', 'https://arxiv.org/abs/2010.14339'),
            ('arXiv:2010.14339', 'https://export.arxiv.org/pdf/2010.14339v1.pdf'),
            ('arXiv:2502.13558', 'https://arxiv.org/html/2502.13558v1'),
            ('math.AG/0301001', 'https://arxiv.org/abs/math.AG/0301001'),
        ]:
            self.assertEqual(errors(f'<a href="{href}">{label} ↗</a>'), [])
        self.assertEqual(len(errors('<a href="https://arxiv.org/abs/hep-th/0301001">math/0301001</a>')), 1)

    def test_titles_doi_labels_and_ambiguous_old_ids_are_out_of_scope(self):
        for label in ('A paper about 2010.14339', 'DOI ↗', 'doi:10.1234/example', '0301001'):
            self.assertEqual(errors(f'<a href="https://doi.org/10.1234/example">{label}</a>'), [])
        self.assertEqual(errors('<a href="https://arxiv.org/abs/2010.14339">2010.14339</a> outside'), [])


if __name__ == '__main__':
    unittest.main()
