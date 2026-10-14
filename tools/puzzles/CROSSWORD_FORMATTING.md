# FND Education Project — one-page crossword standard

**Status:** Project editorial standard approved by the project lead, October 14, 2026. Applies to all new crossword variants and to updates to older puzzles.

## Print requirement

Every crossword must be supplied as **three versions**, and **each version must fit entirely on one letter-size (8.5 × 11 in) page**:

- Normal — empty numbered grid and Across/Down clues, no answers or word bank.
- Easy — the *same* empty grid and clues, with the exact answer word bank on the same page; preserve duplicate words where answers are repeated.
- Answer key — the *same* numbered grid completed with the verified answers and the same clues.

Never silently change, drop, renumber, or regenerate clues/answers to satisfy a layout constraint. Preserve the CrosswordLabs grid, numbering and supplied wording. Confirm an answer key matches the puzzle before publishing.

**Accessible digital option:** Put a PDF text field inside each writable grid square in the Normal and Easy editions, with **maximum length exactly one character**. Leave number labels visible and black/blocked squares non-editable. These PDFs should be usable on screen without printing. The completed answer-key PDF need not be interactive. Verify that a test entry can be typed, saved and reopened; PDF viewer support varies.

## Preferred layout

Use an extra-narrow print margin (roughly 0.25–0.35 in), but keep every printable element comfortably inside the page. **Aim for squares that are 14 PDF points high and wide**, measured from border to border, irrespective of the number of clues. Do not silently shrink grid squares below that target to force the page to fit; flag the crossword to the project lead if the clues cannot be kept readable with that grid size. Use closely spaced clue text and a thin vertical column divider. Scale the grid to the 14-point target and place it where the remaining clue text flows effectively.

In shorter/wider crosswords, place the grid above the Across/Down columns. In taller crosswords, use the page efficiently: the grid may appear at upper left, some clues beside it, and remaining clues in **two ruled columns below it**. **Across and Down form a single flowing sequence**: start the Down heading directly after the last Across clue in the available space, not in a separately reserved region. Let subsequent clues flow into the next column as needed. Text should wrap near the grid instead of leaving substantial dead space.

Word-bank typography may be slightly smaller than the clues, but must be complete and legible. Format as a compact block at the foot of the same page whenever possible. If genuinely impossible without reducing the grid below 14 points or making the clues unreadable, ask the project lead before using a second page. The first page must state **“See the word bank on page 2.”** if the bank is moved. The answer key is normally a separate, one-page PDF.

## Quality control

Render **all three final PDFs** for visual inspection. Confirm:

1. Exactly one letter-size page per PDF (unless the project lead approves a clearly announced second-page word bank).
2. No clipped, overlapping or truncated grid cells, numbering, clues, word-bank entries or answer letters.
3. Readable, continuously flowing Across and Down clues, with a visible fine vertical divider and 14-point grid squares.
4. Identical grid and clues in all three editions; only the letters and word bank change.
5. The source crossword may be 1–2 pages: its pagination is *not* a template for the finished PDFs.
6. Normal/Easy PDFs have one-character fillable fields in all writable cells; the PDFs open, accept entry and print without depending on third-party services.

## Repository placement

Keep the three printable files under `assets/puzzles/crosswords/` with consistent names. Add three thumbnail cards (Normal, Easy, Answer key) to `assets/puzzles/README.md`; thumbnails belong in `assets/puzzles/thumbnails/`.

**Lesson-specific puzzles** are linked on their corresponding lessons and in the overall puzzle gallery. **Module-wide recap puzzles** should be linked from that module's landing page and the gallery, rather than repeated on every lesson page.

For future modules, the project lead can supply raw crossword PDF and answer-key PDF. Convert them to the standard automatically when possible; report legibility or input ambiguities instead of silently altering the material.

## Privacy: live crossword embeds

Print PDFs and thumbnails remain first-party files. An optional online crossword may be offered as an external `Play online` link; do not automatically embed third-party iframes in reader pages without a deliberate privacy/accessibility review. Embedded providers can receive visitor IP addresses and technical browser data and may set cookies or track activity, depending on their policies. Fixed iframe dimensions can also impair mobile reading and keyboard navigation.

All links to crosswords or colouring-page PDFs on the site's course and module pages must also include a visible **thumbnail preview**. Use the existing `.puzzle-grid` and `.puzzle-card` components from the central puzzle gallery; do not add text-only PDF links when a thumbnail is available.
