"""Regressions for the canonical 19-module / 59-lesson curriculum.

The superseded 34 lessons were intentionally removed. This test deliberately
does not require old URLs or their identities to remain in the site.
"""
import importlib.util
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location(
    'course_prepare', ROOT / 'tools/site/prepare_site.py')
PREPARE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PREPARE
SPEC.loader.exec_module(PREPARE)


class CurriculumRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = PREPARE.discover_course_pages()
        cls.modules = [p for p in cls.pages if p.kind == 'module']
        cls.lessons = [p for p in cls.pages if p.kind == 'lesson']
        cls.by_url = {p.public_url: p for p in cls.pages}
        cls.navigation = PREPARE.build_global_navigation(
            cls.pages, PREPARE.discover_reference_pages())

    def test_one_uniform_source_structure(self):
        self.assertEqual(len(self.modules), 19)
        self.assertEqual(len(self.lessons), 59)
        self.assertEqual([p.module_number for p in self.modules], list(range(1, 20)))
        self.assertEqual(len({p.public_url for p in self.pages}), 79)
        self.assertTrue(all(p.is_core and p.progress_eligible for p in self.lessons))
        self.assertTrue(all(
            re.fullmatch(r'module-\d{2}-.+', p.source.parent.name)
            and p.source.parent.parent == ROOT / 'course'
            for p in self.lessons
        ))
        self.assertTrue(all(
            re.fullmatch(r'/course/m\d+/\d+/', p.public_url)
            for p in self.lessons
        ))
        self.assertFalse((ROOT / 'course/concepts-first').exists())
        self.assertFalse(list((ROOT / 'course').glob('part-*')))

    def test_new_lessons_use_current_names_and_addresses(self):
        self.assertIn('/course/m6/1/', self.by_url)
        self.assertIn('/course/m7/4/', self.by_url)
        self.assertIn('/course/m7/5/', self.by_url)
        self.assertIn('/course/m7/6/', self.by_url)
        self.assertIn('cognitive-difficulties-in-fnd.md',
                      self.by_url['/course/m7/4/'].source.name)
        self.assertIn('emotional-regulation-and-involuntary-symptoms.md',
                      self.by_url['/course/m7/5/'].source.name)
        self.assertIn('agency-learning-and-your-own-adaptations.md',
                      self.by_url['/course/m7/6/'].source.name)
        self.assertFalse((ROOT / 'course/module-07-prediction-interoception-and-agency/04-emotional-regulation-and-involuntary-symptoms.md').exists())
        self.assertFalse((ROOT / 'course/module-07-prediction-interoception-and-agency/05-agency-learning-and-your-own-adaptations.md').exists())
        self.assertIn('/course/m10/3/', self.by_url)
        self.assertIn('/course/m11/1/', self.by_url)
        self.assertNotIn('/course/v2/m6/1/', self.by_url)
        self.assertNotIn('/course/m20/', self.by_url)
        for page in self.lessons:
            source = page.source.read_text(encoding='utf-8')
            self.assertIn('## For the Person With FND', source)
            self.assertIn('## For Family, Friends, and Other Supporters', source)
            self.assertIn('## For Clinicians and the Care Team', source)
            self.assertIn('## Research and Sources', source)

    def test_sequential_navigation(self):
        self.assertEqual(self.navigation['/course/m5/3/'].next_url,
                         '/course/m6/')
        self.assertEqual(self.navigation['/course/m8/3/'].next_url,
                         '/course/m9/')
        self.assertEqual(self.navigation['/course/m9/3/'].next_url,
                         '/course/m10/')
        self.assertEqual(self.navigation['/course/m10/3/'].next_url,
                         '/course/m11/')
        self.assertEqual(self.navigation['/course/m19/2/'].next_url,
                         '/reference/')

    def test_schema_has_current_actual_parent(self):
        children = PREPARE.build_collection_children(
            self.pages, PREPARE.discover_reference_pages())
        self.assertIn('/course/m6/1/', children['/course/m6/'])
        self.assertNotIn('/course/m6/1/', children['/course/m7/'])

    def test_new_chapters_keep_evidence_and_audience_sections(self):
        for page in self.lessons:
            if not (6 <= page.module_number <= 10):
                continue
            content = page.source.read_text(encoding='utf-8')
            self.assertTrue(
                'automatically generated' in content
                or 'human-edited' in content
                or 'human-authored' in content,
                f'Missing editorial status for {page.source}'
            )
            self.assertEqual(len(re.findall(r'^## For ', content, re.M)), 3)
            ids = re.findall(r'<a id="citation-(\d+)">', content)
            self.assertEqual(ids, [str(n) for n in range(1, len(ids) + 1)])
            for n in re.findall(r'\]\(#citation-(\d+)\)', content):
                self.assertIn(n, ids)


if __name__ == '__main__':
    unittest.main()
