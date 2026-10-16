# FND Education Project — one-page crossword standard

**Status:** Project editorial standard approved October 14, 2026; adaptive-layout preferences updated October 16, 2026. Applies to all new crossword variants and updates to older puzzles.

## Print requirement

Every crossword must be supplied as **three versions**, and **each version must fit entirely on one letter-size (8.5 × 11 in) page**:

- Normal — empty numbered grid and Across/Down clues, no answers or word bank.
- Easy — the *same* empty grid and clues, with the exact answer word bank on the same page; preserve duplicate words where answers are repeated.
- Answer key — the *same* numbered grid completed with the verified answers and the same clues.

Never silently change, drop, renumber, or regenerate clues/answers to satisfy a layout constraint. Preserve the CrosswordLabs grid and numbering **when upgrading an existing crossword**. For a **newly generated crossword**, new valid layouts and numbering are expected: keep the supplied wording intact and explicitly report which source questions were not selected or borrowed from earlier lessons. Confirm an answer key matches the puzzle before publishing.

**Accessible digital option:** Put a PDF text field inside each writable grid square in the Normal and Easy editions, with **maximum length exactly one character**. Leave number labels visible and black/blocked squares non-editable. These PDFs should be usable on screen without printing. The completed answer-key PDF need not be interactive. Verify that a test entry can be typed, saved and reopened; PDF viewer support varies.

**Keyboard movement:** Arrange form widgets in an **Across-first tab order**: every Across word follows left to right, then remaining Down-only cells. Set the page's PDF tab order to annotation order (`/Tabs /A`) and order the document's form-field references to match. A crossing square has only one form field, so a single linear sequence cannot also follow every Down answer. Readers may use the mouse/touch to navigate Down clues. Do not require PDF JavaScript for automatic focus changes: many browser PDF viewers do not support JavaScript-based auto-advance. Optional auto-advance may be considered only after compatibility testing.

## Preferred layout

Start with comfortable print margins (**0.5 in**) and narrow them to **0.42 in** or **0.33 in** only if needed. **Prefer 16-point crossword squares**, falling back to **15 or 14 PDF points** (never smaller). **Prefer 14-point clue text**, falling back to **13 or 12 points** (never smaller). Layout selection must preflight the whole Easy edition, including the word bank, before generating the three PDFs. Fit more educational answers when page space permits, rather than capping every crossword at 24 answers. Use a thin divider and flowing Across/Down clues; do not add a second page or silently clip material.

In shorter/wider crosswords, place the grid above the Across/Down columns. In taller crosswords, use the page efficiently: the grid may appear at upper left, some clues beside it, and remaining clues in **two ruled columns below it**. **Across and Down form a single flowing sequence**: start the Down heading directly after the last Across clue in the available space, not in a separately reserved region. Let subsequent clues flow into the next column as needed. Text should wrap near the grid instead of leaving substantial dead space.

Word-bank typography may be slightly smaller than the clues, but must be complete and legible. Format as a compact block at the foot of the same page whenever possible. If genuinely impossible without reducing the grid below 14 points or making the clues unreadable, ask the project lead before using a second page. For new generated puzzles, if the Easy word bank cannot fit on page one without breaking minimum sizes, reject that layout and try another. For legacy conversions only, seek explicit approval before an announced second page. The answer key remains a separate, one-page PDF.

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
