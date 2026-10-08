"""[Codex] Regression and negative controls for raw bibliography markup."""
import unittest

from publication_text import publication_text_errors, text_residue


class PublicationTextTests(unittest.TestCase):
    def test_named_numeric_and_double_encoding_are_blocked(self):
        for text in ('K&amp;auml;hler', 'Fay&#x000E7;al', '&#231;', '&lt;i&gt;', '&amp;'):
            with self.subTest(text=text):
                self.assertTrue(text_residue(text))

    def test_paired_and_self_closing_markup_are_blocked(self):
        for text in ('<i>W</i>', '<mml:math><mml:mi>x</mml:mi></mml:math>',
                     '<jats:italic>x</jats:italic>', '<span class="x">text</span>', '<br/>'):
            with self.subTest(text=text):
                self.assertTrue(text_residue(text))

    def test_unicode_tex_and_literal_inequalities_are_not_markup(self):
        for text in ('Kähler', 'Fayçal', 'Computers & Mathematics', '$W$-constraints',
                     r'$a<b$ and $b>c$', '$a<b>c$', r'$x \& y$', '&unknownentity;'):
            with self.subTest(text=text):
                self.assertEqual(text_residue(text), [])

    def test_only_public_bibliographic_text_fields_are_checked(self):
        pub = {'title': '<i>D</i>-modules', 'journal': 'A &amp; B',
               'coauthors': ['Fay&#231;al'], 'doi': '10.1234/a&amp;b'}
        errors = publication_text_errors(pub)
        self.assertEqual(len(errors), 3)
        self.assertTrue(errors[0].startswith('title:'))
        self.assertTrue(errors[1].startswith('journal:'))
        self.assertTrue(errors[2].startswith('coauthors[0]:'))
        self.assertEqual(publication_text_errors({'sources': ['<i>source</i>']}), [])


if __name__ == '__main__':
    unittest.main()
