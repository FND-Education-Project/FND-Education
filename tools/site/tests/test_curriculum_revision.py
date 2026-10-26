"""Regression checks for new routes, original identity and course sequencing.

These tests exercise the publication model; they do not access learner records
or replace live acceptance tests for a later account-service change.
"""
import importlib.util
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('course_prepare', ROOT / 'tools/site/prepare_site.py')
PREPARE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PREPARE
SPEC.loader.exec_module(PREPARE)


class CurriculumRevisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Discover exactly the same content as the production generator."""
        cls.pages = PREPARE.discover_course_pages()
        cls.by_source = {str(p.source.relative_to(ROOT)): p for p in cls.pages}
        cls.by_url = {p.public_url: p for p in cls.pages}
        cls.navigation = PREPARE.build_global_navigation(
            cls.pages, PREPARE.discover_reference_pages()
        )

    def test_every_original_lesson_keeps_url_and_identity(self):
        """Saved keys and old bookmarks must still identify their old topic."""
        inventory = json.loads((ROOT / 'reference/_internal/course/syllabus-redesign-identity-map-2026-10-26.json').read_text())
        for old in inventory['legacy_lessons']:
            page = self.by_source[old['source_path']]
            self.assertEqual(page.public_url, old['legacy_url'])
            self.assertEqual(f'm{page.module_number}-{page.lesson_number}', old['legacy_key'])
            self.assertTrue(page.progress_eligible)

    def test_new_topics_do_not_reuse_original_slots(self):
        """Unsupported new progress is preferable to completing a wrong topic."""
        old = {f'm{p.module_number}-{p.lesson_number}' for p in self.pages if p.kind == 'lesson' and p.module_number < 24}
        new = [p for p in self.pages if p.kind == 'lesson' and p.module_number >= 24]
        self.assertEqual(len(new), 16)
        for page in new:
            self.assertNotIn(f'm{page.module_number}-{page.lesson_number}', old)
            self.assertFalse(page.progress_eligible)
            self.assertTrue(page.public_url.startswith('/course/v2/'))
        self.assertEqual(self.by_url['/course/m6/1/'].module_number, 6)
        self.assertEqual(self.by_url['/course/v2/m6/1/'].module_number, 24)

    def test_core_sequence_and_earlier_reading_are_separate(self):
        """Next must follow concepts, symptom description, rehab, then pacing."""
        modules = [p for p in self.pages if p.kind == 'module' and p.is_core]
        self.assertEqual([p.display_module_number for p in modules], list(range(1, 20)))
        self.assertEqual(sum(p.kind == 'lesson' and p.is_core for p in self.pages), 57)
        self.assertEqual(self.navigation['/course/m5/3/'].next_url, '/course/v2/m6/')
        self.assertEqual(self.navigation['/course/v2/m8/3/'].next_url, '/course/v2/m9/')
        self.assertEqual(self.navigation['/course/v2/m9/3/'].next_url, '/course/v2/m10/')
        self.assertEqual(self.navigation['/course/v2/m10/3/'].next_url, '/course/m13/')
        self.assertNotEqual(self.navigation['/course/m6/1/'].next_url, '/course/v2/m6/2/')

    def test_schema_uses_actual_parent_and_no_route_collisions(self):
        """Schema membership must not attach new lessons to legacy modules."""
        children = PREPARE.build_collection_children(self.pages, PREPARE.discover_reference_pages())
        self.assertIn('/course/v2/m6/1/', children['/course/v2/m6/'])
        self.assertNotIn('/course/v2/m6/1/', children['/course/m6/'])
        self.assertEqual(len(self.by_url), len(self.pages))

    def test_new_lessons_are_complete_working_drafts(self):
        """Catch draft-only references, incomplete audiences and source tables."""
        for page in self.pages:
            if page.kind != 'lesson' or page.module_number < 24:
                continue
            text = page.source.read_text()
            self.assertIn('automatically generated', text)
            self.assertEqual(len(re.findall(r'^## For ', text, re.M)), 3)
            self.assertIn('## Research and Sources', text)
            self.assertNotIn('new-lessons-research-2026-10-26/sources.md', text)
            ids = re.findall(r'<a id="citation-(\d+)">', text)
            self.assertEqual(ids, [str(i) for i in range(1, len(ids) + 1)])
            for number in re.findall(r'\]\(#citation-(\d+)\)', text):
                self.assertIn(number, ids)


if __name__ == '__main__':
    unittest.main()
