"""Regression tests for educational crossword source selection and print rules."""
from __future__ import annotations

import json
from io import BytesIO
from zipfile import ZipFile
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
from crossword_builder.publish import (
    blocked_cells, export_gallery, export_pdfs, is_printable,
    plan_page, restore_layout, title_measure, validate_title,
)
from crossword_builder.deliver import package_names, prepare_downloads


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

    def test_cli_excel_to_gallery_end_to_end(self):
        # Exercise the user-facing command with a real Excel workbook.
        from generate_crosswords import main
        words = ["BRAIN", "NERVE", "REST", "FLARE", "CALM", "FEEL",
                 "BODY", "MOOD", "PANIC", "PAST", "SUPPORT", "RECOVERY"]
        self._book([
            (f"A clue for {word.lower()}.", word, 2, 1, 1)
            for word in words
        ])
        output = Path(self.temp.name) / "out"
        stages = []
        status = main([str(self.file), "--module", "1", "--lesson", "1",
                       "--attempts", "45", "--max-words", "9", "--top", "2",
                       "--out", str(output)],
                      progress=lambda percent, label: stages.append((percent, label)))
        self.assertEqual(status, 0)
        self.assertEqual(stages[-1][0], 100)
        self.assertTrue(any("Searching" in label for _, label in stages))
        self.assertTrue(any("Rendering" in label for _, label in stages))
        self.assertTrue(all(
            earlier <= later
            for (earlier, _), (later, _) in zip(stages, stages[1:])
        ))
        self.assertTrue((output / "index.html").is_file())
        report = json.loads((output / "report.json").read_text())
        self.assertEqual(report["selection"]["mode"], "lesson")
        self.assertEqual(report["selection"]["module"], 1)
        self.assertGreaterEqual(len(report["candidates"]), 1)

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

    def test_crossword_has_black_block_squares_and_outer_border(self):
        self.assertTrue(self.printable)
        layout = self.printable[0]
        empty = blocked_cells(layout)
        self.assertGreater(len(empty), 0)
        self.assertTrue(empty.isdisjoint(layout.cells))
        rows, cols = layout.size()
        self.assertEqual(len(layout.cells) + len(empty), rows * cols)
        plan = plan_page(layout)
        with tempfile.TemporaryDirectory() as tmp:
            pdfs = export_pdfs(layout, Path(tmp), "FND learning review")
            doc = fitz.open(Path(tmp) / pdfs["normal"])
            r, c = sorted(empty)[0]
            x = plan.grid_x + (c + .5) * plan.square
            y = plan.grid_y + (r + .5) * plan.square
            # The inactive cell is a genuine halftone: mostly white with
            # visible dark dots, not a heavy solid black ink rectangle.
            pix = doc[0].get_pixmap(
                matrix=fitz.Matrix(4, 4),
                clip=fitz.Rect(
                    x - plan.square * .30, y - plan.square * .30,
                    x + plan.square * .30, y + plan.square * .30,
                ),
                alpha=False,
            )
            tones = pix.samples[0::3]
            self.assertGreater(max(tones), 235)
            self.assertLess(min(tones), 100)
            self.assertGreater(sum(tones) / len(tones), 175)
            self.assertEqual(len(list(doc[0].widgets() or [])), len(layout.cells))
            doc.close()

    def test_title_width_is_measured_and_not_truncated(self):
        layout = self.printable[0]
        self.assertEqual(validate_title("FND Learning Review", layout),
                         "FND Learning Review")
        used, available = title_measure("FND Learning Review", layout)
        self.assertLess(used, available)
        with self.assertRaisesRegex(ValueError, "Shorten"):
            validate_title("W" * 110, layout)
        with self.assertRaisesRegex(ValueError, "single-line"):
            validate_title("One\nTwo", layout)

    def test_selected_puzzle_retitle_and_download_naming(self):
        self.assertTrue(self.printable)
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            export_gallery(self.printable[:1], directory, "FND Module 2 Lesson 5",
                           self.pool, [], {"mode": "lesson", "module": 2,
                                           "lesson": 5})
            report = json.loads((directory / "report.json").read_text())
            candidate = report["candidates"][0]
            restored = restore_layout(candidate)
            self.assertEqual(restored.signature(), self.printable[0].signature())
            self.assertTrue(all(
                "grid_row" in item and "grid_col" in item
                for item in candidate["included"]
            ))
            name, files, zip_bytes = prepare_downloads(
                candidate, report["selection"], "Signs and Capacity",
                directory / "final",
            )
            self.assertEqual(name, "Module-2-Lesson-5.zip")
            self.assertEqual(
                files["normal"][0], "signs-and-capacity-m2-5-normal.pdf"
            )
            self.assertEqual(
                files["easy"][0], "signs-and-capacity-m2-5-easy.pdf"
            )
            self.assertEqual(
                files["key"][0], "signs-and-capacity-m2-5-answer-key.pdf"
            )
            with ZipFile(BytesIO(zip_bytes)) as zipped:
                self.assertEqual(len(zipped.namelist()), 4)
                for _kind, (filename, pdf_bytes) in files.items():
                    self.assertEqual(zipped.read(filename), pdf_bytes)
                    pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
                    self.assertIn("Signs and Capacity", pdf[0].get_text())
                    self.assertEqual(len(pdf), 1)
                    pdf.close()
            self.assertEqual(package_names("Course recap", {
                "mode": "module", "module": 2
            }), ("course-recap-m2", "Module-2.zip"))
            self.assertEqual(package_names("Course recap", {
                "mode": "all"
            }), ("course-recap-all", "Whole-Course.zip"))

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
