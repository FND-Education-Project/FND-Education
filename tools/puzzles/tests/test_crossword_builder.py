"""Regression tests for educational crossword source selection and print rules."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

import fitz
from openpyxl import Workbook

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from crossword_builder.core import (
    Entry, read_workbook, select_entries, top_layouts, verify_layout,
)
from crossword_builder.publish import export_gallery, export_pdfs, is_printable


WORDS = (
    "BRAIN", "NERVE", "REST", "FLARE", "CALM", "FEEL", "BODY",
    "MOOD", "PANIC", "PAST", "SUPPORT", "RECOVERY", "ENERGY",
    "LISTEN", "FAMILY", "TRIGGER", "SLEEP", "LEARN", "ATTENTION",
    "COPING",
)


def entry(word: str, number: int, lesson: int = 1,
          module: int = 1, priority: int = 2) -> Entry:
    return Entry(f"A learning clue for {word.lower()}.", word, word,
                 priority, lesson, module, number)


class WorkbookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.file = Path(self.temp.name) / "questions.xlsx"

    def _book(self, rows):
        book = Workbook()
        sheet = book.active
        sheet.append(["Clue", "Answer", "Priority", "Lesson", "Module"])
        for row in rows:
            sheet.append(row)
        book.save(self.file)
        book.close()

    def test_read_validated_five_columns(self):
        self._book([
            ("A clue", "BRAIN FOG", "High", "Lesson 3", "Module 2"),
            ("Another clue", "NERVE", None, 2, 2),
        ])
        rows, notes = read_workbook(self.file)
        self.assertEqual([r.answer for r in rows], ["BRAINFOG", "NERVE"])
        self.assertEqual(rows[0].priority, 1)
        self.assertEqual(rows[1].priority, 2)
        self.assertEqual((rows[0].module, rows[0].lesson), (2, 3))
        self.assertTrue(any("BRAIN FOG" in note for note in notes))

    def test_invalid_data_does_not_silently_change_question(self):
        self._book([("Clue", "HELLO?", 1, 1, 1)])
        with self.assertRaisesRegex(ValueError, "Row 2"):
            read_workbook(self.file)

    def test_lesson_borrows_only_from_earlier_lessons(self):
        rows = [
            entry("BRAIN", 2, 1, 1),
            entry("NERVE", 3, 2, 1),
            entry("CALM", 4, 1, 2),
            entry("REST", 5, 2, 2),
            entry("PANIC", 6, 3, 2),
        ]
        primary, loans, _ = select_entries(rows, "lesson", module=2, lesson=2)
        self.assertEqual([e.answer for e in primary], ["REST"])
        self.assertEqual({e.answer for e in loans}, {"BRAIN", "NERVE", "CALM"})
        self.assertNotIn("PANIC", {e.answer for e in primary + loans})

    def test_module_and_all_are_strictly_scoped(self):
        rows = [entry("BRAIN", 1, 1, 1), entry("REST", 2, 2, 1),
                entry("PANIC", 3, 1, 2)]
        module_rows, loans, _ = select_entries(rows, "module", module=1)
        self.assertEqual({e.answer for e in module_rows}, {"BRAIN", "REST"})
        self.assertFalse(loans)
        all_rows, loans, _ = select_entries(rows, "all")
        self.assertEqual(len(all_rows), 3)
        self.assertFalse(loans)

    def test_duplicate_answer_is_disclosed_and_prioritized(self):
        rows = [entry("BRAIN", 2, priority=3),
                entry("BRAIN", 3, priority=1),
                entry("NERVE", 4)]
        chosen, _, notes = select_entries(rows, "all")
        self.assertEqual({e.answer for e in chosen}, {"BRAIN", "NERVE"})
        self.assertEqual(next(e for e in chosen if e.answer == "BRAIN").source_row, 3)
        self.assertTrue(any("row 2" in note for note in notes))


class LayoutAndPdfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pool = [entry(w, i + 2, priority=1 if i % 4 == 0 else 2)
                    for i, w in enumerate(WORDS)]
        cls.candidates = top_layouts(cls.pool, [], attempts=100, top=5,
                                     max_words=14, max_side=25, seed=13)
        cls.printable = [c for c in cls.candidates if is_printable(c)]

    def test_legality_and_separate_variants(self):
        self.assertGreaterEqual(len(self.candidates), 3)
        keys = [candidate.signature() for candidate in self.candidates]
        self.assertEqual(len(keys), len(set(keys)))
        for candidate in self.candidates:
            verify_layout(candidate)
            self.assertGreaterEqual(candidate.metrics["words"], 3)
            self.assertGreater(candidate.metrics["intersection_letters"], 0)

    def test_one_page_three_edition_pdf_forms(self):
        self.assertTrue(self.printable)
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            layout = self.printable[0]
            pdfs = export_pdfs(layout, folder, "Educational crossword test")
            self.assertEqual(set(pdfs), {"normal", "easy", "key"})
            expected_cells = len(layout.cells)
            expected_text = None
            for mode, name in pdfs.items():
                doc = fitz.open(folder / name)
                self.assertEqual(len(doc), 1)
                self.assertEqual((doc[0].rect.width, doc[0].rect.height),
                                 (612, 792))
                widgets = list(doc[0].widgets() or [])
                self.assertEqual(len(widgets), 0 if mode == "key" else expected_cells)
                self.assertTrue(all(w.text_maxlen == 1 for w in widgets))
                current = doc[0].get_text()
                self.assertIn("Across", current)
                self.assertIn("Down", current)
                if mode == "easy":
                    self.assertIn("Word bank", current)
                if mode == "normal":
                    expected_text = current
                if mode == "key":
                    self.assertNotIn("Word bank", current)
                doc.close()
            self.assertIsNotNone(expected_text)

    def test_pdf_field_can_be_saved_and_reopened(self):
        self.assertTrue(self.printable)
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            pdfs = export_pdfs(self.printable[0], folder, "Fillable PDF test")
            doc = fitz.open(folder / pdfs["normal"])
            page = doc[0]  # Retain the page while editing its widget.
            first = next(iter(page.widgets()))
            original_name = first.field_name
            first.field_value = "A"
            first.update()
            destination = folder / "filled.pdf"
            doc.save(destination, garbage=4, deflate=True)
            doc.close()
            reopened = fitz.open(destination)
            filled = next(w for w in reopened[0].widgets()
                          if w.field_name == original_name)
            self.assertEqual(filled.field_value, "A")
            self.assertEqual(filled.text_maxlen, 1)
            reopened.close()

    def test_gallery_contains_five_options_and_origin_report(self):
        self.assertTrue(self.printable)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            export_gallery(self.printable[:5], root, "FND course review",
                           self.pool, [], {"mode": "all"})
            report = json.loads((root / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(len(report["candidates"]), min(5, len(self.printable)))
            self.assertIn("Option 1", (root / "index.html").read_text())
            first = report["candidates"][0]
            self.assertIn("unused_selected_questions", first)
            self.assertIn("included", first)
            for mode in ("normal", "easy", "key"):
                self.assertTrue((root / first["pdfs"][mode]).is_file())


if __name__ == "__main__":
    unittest.main()
