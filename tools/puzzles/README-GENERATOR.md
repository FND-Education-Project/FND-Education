# Excel-to-crossword generator (Codespaces)

A local/offline authoring tool for FND Education Project crosswords. The site
does **not** execute Python; run this tool in GitHub Codespaces and review
the five generated options before adding approved PDFs/thumbnails to the site.

This tool is separate from the existing legacy PDF upgrade scripts. Its output
follows [CROSSWORD_FORMATTING.md](CROSSWORD_FORMATTING.md): **Normal, Easy,
Answer Key**, one **US Letter** page each, **14–16 pt squares and 12–14 pt clues**, same clues/grid,
with fillable one-character cells in Normal and Easy. The easy version has
the word bank on the same page. PDFs are not published automatically.

## Open the spreadsheet-style workshop in Codespaces

After opening the feature branch in GitHub Codespaces, install dependencies once:

    python -m pip install -r tools/puzzles/requirements-crosswords.txt

Then start the private, local browser app:

    python -m streamlit run tools/puzzles/crossword_app.py --server.address 0.0.0.0 --server.port 8501

Open port **8501** from the Codespaces **Ports** tab (or click the
notification offering to open the app in your browser). Keep port
visibility **Private**, not Public. Nothing needs to be deployed to the
website or any external server.

The workshop supports the full workflow without further terminal commands:

1. Open the question-bank workbook already in tools/puzzles, or upload
   another .xlsx file. Add or paste answers and clues directly into the
   editable spreadsheet-like table.
2. Choose Lesson, Module or All from simple dropdowns, then press
   **Generate five crossword choices**. The default aims for **36** answers
   rather than the previous arbitrary 24-word limit. If a full puzzle
   cannot fit legibly, the search tries fewer words automatically.
3. Compare **full-page PDF previews** of up to five layouts. Select one,
   then press **Download selected puzzle (ZIP)** to receive Normal, Easy,
   Answer Key and a source report. Individual PDF downloads are included.

**Important:** The in-browser editor has a **Save edits to workbook in
Codespaces** button. Saving locally does not commit your work to GitHub:
you can download the edited workbook for backup, or commit/push it when
ready. Generating a puzzle uses your *current edits*, even if you have
not saved them to the repository. No public site pages or PDFs are
published automatically.

## Workbook

Use **one .xlsx file** with these **five column headers**, in any order,
on the **first worksheet**:

| clue | answer | priority | lesson | module |
| --- | --- | --- | --- | --- |
| A part of the nervous system inside your head. | BRAIN | 1 | 1 | 1 |
| A time symptoms become worse for a while. | FLARE | 2 | 1 | 1 |
| A break from activity. | REST | 3 | 2 | 1 |

- Enter roughly 35–40 question/answer pairs **per lesson**, as desired.
  A puzzle can select a subset; it does not have to include all 40.
- **Priority:** 1 or High = most important; 2 or Medium = normal; 3 or
  Low = optional. An empty cell defaults to 2. High priority influences
  selection; it is not an absolute guarantee of inclusion.
- **Lesson and module** are *positive numeric identifiers*, or "Lesson 2"
  / "Module 1". Lesson numbers restart at 1 in each module.
- A crossword answer contains letters A–Z. Internal spaces and hyphens
  are removed **only for the grid** (e.g. "BRAIN FOG" → "BRAINFOG").
  The original source spelling remains in the Excel file, report, and
  word bank. The generator reports such normalizations.
- Blanks, invalid identifiers, unsupported punctuation, and invalid
  priorities trigger an explicit error with the Excel row number.
  Other than blank rows, source questions are never rewritten.
- If the same answer occurs in multiple rows, the current version selects
  one matching clue (highest priority, then earliest row) and reports the
  excluded duplicate rows. **It does not silently create duplicate clues.**
  If distinct clues need the same answer in one puzzle, that enhancement
  requires additional placement logic.

## One-time Codespaces setup

From the repository root:

    python -m pip install -r tools/puzzles/requirements-crosswords.txt

## Select questions and generate

List available lessons before selecting:

    python tools/puzzles/generate_crosswords.py my-questions.xlsx --list

Make a lesson-specific puzzle:

    python tools/puzzles/generate_crosswords.py my-questions.xlsx --module 1 --lesson 3

Make a module recap using every lesson in that module:

    python tools/puzzles/generate_crosswords.py my-questions.xlsx --module 1

Make a whole-course review from the complete workbook:

    python tools/puzzles/generate_crosswords.py my-questions.xlsx --all

Choose a larger pool, search harder, or change the reproducible starting seed:

    python tools/puzzles/generate_crosswords.py my-questions.xlsx --module 1 --lesson 3 --max-words 30 --attempts 600 --seed 42

Options include --top 5 (default), --max-words 36 (default),
--max-side 29 (default), --title "Your title", and
--out tools/puzzles/.crossword-output (default). The output directory
is ignored by Git; publishing is a separate, deliberate action.

**Question selection:**

1. **Lesson** — draw from that exact module and lesson. Try all of its
   questions first. If the crossword still has unused capacity because
   terms cannot be fitted, supplement it using *only prior lessons*,
   including lessons in earlier modules. Prefer recent prior lessons.
2. **Module** — draw from all lessons in that module, with no outside
   borrowing.
3. **All** — draw from all questions in the workbook, with no borrowing.

An earlier-lesson answer is shown as *borrowed* in the report. A question
from a later lesson is **never** used for a lesson-specific crossword.

## Review the five results

Open tools/puzzles/.crossword-output/index.html (or your chosen output
folder's index file) to inspect an empty grid for each option and
links to its three PDFs. report.json identifies:

- Score, number of placed answers, and two-plus/three-plus intersections.
- **Every included question**, including source row, module, lesson and
  borrowed status.
- All selected questions that were **not** placed.
- Duplicate-answer exclusions and answer spacing/hyphen normalization.

Each option is in option-01/, option-02/, etc., containing
normal.pdf, easy.pdf, and answer-key.pdf.

The quality score (out of 100) rewards question coverage, multiple and
spread-out crossings, compactness, Across/Down balance, priority, and
keeping questions in their selected lesson. Only **legally connected**
crosswords are scored. An algorithm cannot guarantee every source answer
will fit; there may be fewer than five distinct printable layouts.

**Print standard takes precedence over word count.** The program rejects
layouts if the complete clues or word bank cannot fit on a single Letter
page with at least 14-point squares and 12-point clues. Increase --attempts, reduce
--max-words, or add more crossing-friendly questions. It will
never silently shrink squares, truncate clues, or add a second page.

## Publishing

After reviewing the PDF pages and **testing a form field in your target PDF
viewer**, copy the chosen three PDFs into assets/puzzles/crosswords/
with approved, stable names. Create suitable thumbnail images and update
the puzzle gallery and relevant course/module page. Do not automatically
commit all five alternatives.

The generator re-opens each PDF and checks page dimensions, form counts,
one-character limits, and Across-first field order. Some PDF viewers do
not save or restore fillable fields reliably; manually test entry, save,
and reopen before publishing. PDF JavaScript is intentionally not used.

## Development / testing

    python -m unittest discover -s tools/puzzles/tests -p "test_crossword_builder.py" -v

Dependencies are restricted to the workbook reader (openpyxl) and
PyMuPDF, already used by the project for PDF crossword form fields. The
tool does not contact third-party sites or accept visitor submissions.
