"""Print and preview outputs for the FND Education Project crossword standard.

Uses PyMuPDF (also used by the repository's legacy crossword upgrader).
No PDF is written unless the SAME fourteen-point grid and clue placement
fit all three letter-size, single-page editions.
"""
from __future__ import annotations

from collections import defaultdict
import html
import json
from pathlib import Path

import fitz

from .core import Entry, Layout, _points, verify_layout


WIDTH, HEIGHT = 612.0, 792.0     # US Letter, points
MARGIN, GRID_TOP, SIDE = 24.0, 52.0, 14.0
BANK_TOP, BANK_END = 727.0, 772.0
FONT_SIZE, LINE = 8.7, 11.4


def _text_width(text: str, font_size: float = FONT_SIZE, bold: bool = False) -> float:
    return fitz.get_text_length(
        text, fontname="hebo" if bold else "helv", fontsize=font_size)


def _wrap(text: str, width: float, size: float = FONT_SIZE) -> list[str]:
    """Fit whole words to a fixed physical width without clipping."""
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        parts = paragraph.split()
        if not parts:
            lines.append("")
            continue
        current = ""
        for word in parts:
            trial = (current + " " + word).strip()
            if _text_width(trial, size) <= width:
                current = trial
            else:
                if current:
                    lines.append(current)
                    current = ""
                if _text_width(word, size) > width:
                    # A single oversized word must be split, not truncated.
                    fragment = ""
                    for letter in word:
                        if fragment and _text_width(fragment + letter, size) > width:
                            lines.append(fragment)
                            fragment = letter
                        else:
                            fragment += letter
                    current = fragment
                else:
                    current = word
        if current:
            lines.append(current)
    return lines


def _clue_regions(layout: Layout) -> tuple[float, float, list[tuple[float, float, float, float]]]:
    """Use a side column beside a tall/narrow grid and two below it."""
    rows, cols = layout.size()
    grid_width, grid_height = cols * SIDE, rows * SIDE
    if grid_width > WIDTH - 2 * MARGIN or GRID_TOP + grid_height > BANK_TOP - 28:
        raise ValueError("Grid exceeds the one-page printable area at 14 pt/square.")
    has_side = WIDTH - (MARGIN + grid_width + 12) - MARGIN >= 164 \
        and grid_height >= 115
    grid_x = MARGIN if has_side else (WIDTH - grid_width) / 2
    grid_bottom = GRID_TOP + grid_height
    below_top = grid_bottom + 13
    regions: list[tuple[float, float, float, float]] = []
    if has_side:
        regions.append((MARGIN + grid_width + 12, GRID_TOP,
                        WIDTH - MARGIN, grid_bottom))
    # Clue text flows through ruled columns without reserving separate
    # Across and Down regions.
    column_mid = WIDTH / 2
    regions.extend([
        (MARGIN, below_top, column_mid - 11, BANK_TOP - 10),
        (column_mid + 11, below_top, WIDTH - MARGIN, BANK_TOP - 10),
    ])
    return grid_x, GRID_TOP, regions


def _clue_plan(layout: Layout) -> tuple[
    float, float, list[tuple[float, float, str, float, bool]],
    list[tuple[float, float, float, float]]
]:
    """Preflight every line on the hardest (Easy) edition before drawing."""
    x, y, regions = _clue_regions(layout)
    numbered = layout.numbered()
    across = [(num, p) for num, p in numbered if p.direction == "across"]
    down = [(num, p) for num, p in numbered if p.direction == "down"]
    sections: list[tuple[str, str, bool]] = [("Across", "", True)]
    sections.extend(("", f"{num}. {p.entry.clue}", False) for num, p in across)
    sections.append(("Down", "", True))
    sections.extend(("", f"{num}. {p.entry.clue}", False) for num, p in down)

    output: list[tuple[float, float, str, float, bool]] = []
    region_index = 0
    cursor = regions[0][1]
    for heading, sentence, is_heading in sections:
        while True:
            if region_index >= len(regions):
                raise ValueError("Clues do not fit one letter-size page at readable type.")
            x0, y0, x1, y1 = regions[region_index]
            width = x1 - x0 - 4
            size = 10.0 if is_heading else FONT_SIZE
            lines = [heading] if is_heading else _wrap(sentence, width, size)
            used_height = len(lines) * LINE + (3 if is_heading else 0)
            if cursor + used_height <= y1:
                if is_heading:
                    cursor += 3
                for line in lines:
                    output.append((x0 + 2, cursor + size, line, size, is_heading))
                    cursor += LINE
                break
            region_index += 1
            if region_index < len(regions):
                cursor = regions[region_index][1]

    # Bank must fit all answers, including when two words share an answer.
    answers = sorted(p.entry.original_answer.upper() for p in layout.placed)
    bank_lines = _wrap("  |  ".join(answers), WIDTH - 2 * MARGIN - 8, 7.8)
    if len(bank_lines) * 10.3 > BANK_END - BANK_TOP - 14:
        raise ValueError("Easy word bank cannot fit at legible size on page one.")
    return x, y, output, regions


def is_printable(layout: Layout) -> bool:
    """Use exactly the same preflight for preview ranking and actual PDFs."""
    try:
        _clue_plan(layout)
        return True
    except ValueError:
        return False


def _tab_sequence(layout: Layout) -> list[tuple[int, int]]:
    """Across-first order, then remaining Down-only writable squares."""
    sequence: list[tuple[int, int]] = []
    visited = set()
    for direction in ("across", "down"):
        for _, p in layout.numbered():
            if p.direction != direction:
                continue
            for coord in _points(p):
                if coord not in visited:
                    sequence.append(coord)
                    visited.add(coord)
    if set(sequence) != set(layout.cells):
        raise ValueError("Field ordering missed a grid square.")
    return sequence


def _draw_page(page: fitz.Page, layout: Layout, edition: str,
               title: str) -> list[tuple[int, int]]:
    """Draw all non-editable artwork once, with consistent edition geometry."""
    x, y, clues, regions = _clue_plan(layout)
    page.insert_text(
        (MARGIN, 29), title[:90], fontsize=14.0, fontname="hebo",
        color=(0, 0, 0),
    )
    numbers = {(p.row, p.col): num for num, p in layout.numbered()}
    for (r, c), letter in sorted(layout.cells.items()):
        rect = fitz.Rect(x + c * SIDE, y + r * SIDE,
                         x + (c + 1) * SIDE, y + (r + 1) * SIDE)
        page.draw_rect(rect, color=(0.08, 0.08, 0.08),
                       fill=(1, 1, 1), width=.65)
        if (r, c) in numbers:
            page.insert_text((rect.x0 + 1.4, rect.y0 + 5),
                             str(numbers[(r, c)]), fontsize=5.0,
                             fontname="helv", color=(0, 0, 0))
        if edition == "key":
            page.insert_text(
                (rect.x0 + 3.3, rect.y0 + 12.3), letter,
                fontsize=10.0, fontname="hebo", color=(0, 0, 0),
            )
    # A thin rule distinguishes the two lower clue columns.
    if regions[1][1] < BANK_TOP - 22:
        page.draw_line((WIDTH / 2, regions[1][1]),
                       (WIDTH / 2, BANK_TOP - 10),
                       color=(.7, .7, .7), width=.4)
    for tx, baseline, line, size, bold in clues:
        page.insert_text(
            (tx, baseline), line, fontsize=size,
            fontname="hebo" if bold else "helv", color=(0, 0, 0))
    if edition == "easy":
        page.draw_line((MARGIN, BANK_TOP - 3), (WIDTH - MARGIN, BANK_TOP - 3),
                       color=(.65, .65, .65), width=.5)
        page.insert_text((MARGIN, BANK_TOP + 9), "Word bank",
                         fontsize=9.0, fontname="hebo")
        answers = sorted(p.entry.original_answer.upper() for p in layout.placed)
        for i, line in enumerate(
            _wrap("  |  ".join(answers), WIDTH - 2 * MARGIN - 8, 7.8)
        ):
            page.insert_text((MARGIN, BANK_TOP + 21 + 10.3 * i),
                             line, fontsize=7.8, fontname="helv")
    return _tab_sequence(layout)


def _save_pdf(layout: Layout, edition: str, destination: Path,
              title: str) -> None:
    """Write a PDF, then independently re-open and inspect form invariants."""
    verify_layout(layout)
    doc = fitz.open()
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    sequence = _draw_page(page, layout, edition, title)
    if edition != "key":
        x, y, _, _ = _clue_plan(layout)
        for row, col in sequence:
            rect = fitz.Rect(x + col * SIDE + .6, y + row * SIDE + 5.4,
                             x + (col + 1) * SIDE - .6,
                             y + (row + 1) * SIDE - .5)
            widget = fitz.Widget()
            widget.field_name = f"cell_{row}_{col}"
            widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            widget.field_value = ""
            widget.text_maxlen = 1
            widget.text_align = 1
            widget.text_font = "Helv"
            widget.text_fontsize = 9.0
            widget.text_color = (0, 0, 0)
            widget.border_width = 0
            widget.fill_color = None
            widget.rect = rect
            page.add_widget(widget)
        doc.xref_set_key(page.xref, "Tabs", "/A")
    doc.set_metadata({"title": title, "subject": f"Crossword: {edition}"})
    doc.save(str(destination), deflate=True, garbage=4)
    doc.close()
    verified = fitz.open(str(destination))
    try:
        if len(verified) != 1 or verified[0].rect != fitz.Rect(0, 0, WIDTH, HEIGHT):
            raise ValueError(f"{destination.name} is not one US Letter page.")
        widgets = list(verified[0].widgets() or [])
        expected = 0 if edition == "key" else len(sequence)
        if len(widgets) != expected:
            raise ValueError(f"{destination.name} has the wrong number of text fields.")
        if edition != "key":
            if any(widget.text_maxlen != 1 for widget in widgets):
                raise ValueError("A text field allows more than one character.")
            if [w.field_name for w in widgets] != [
                f"cell_{r}_{c}" for r, c in sequence
            ]:
                raise ValueError("Across-first tab order was not retained.")
            if verified.xref_get_key(verified[0].xref, "Tabs") != ("name", "/A"):
                raise ValueError("Missing Acrobat annotation tab-order declaration.")
    finally:
        verified.close()


def export_pdfs(layout: Layout, folder: Path, title: str) -> dict[str, str]:
    """Export the required Normal, Easy, and Answer Key, or fail explicitly."""
    folder.mkdir(parents=True, exist_ok=True)
    names = {"normal": "normal.pdf", "easy": "easy.pdf",
             "key": "answer-key.pdf"}
    paths = {}
    try:
        for edition, filename in names.items():
            _save_pdf(layout, edition, folder / filename, title)
            paths[edition] = filename
    except Exception:
        for filename in names.values():
            (folder / filename).unlink(missing_ok=True)
        raise
    return paths


def _preview_svg(layout: Layout) -> str:
    """A static, accessible-preview-friendly inline SVG of an empty grid."""
    rows, cols = layout.size()
    cell = 17
    numbers = {(p.row, p.col): n for n, p in layout.numbered()}
    items = [f'<svg role="img" aria-label="Crossword grid, {rows} rows by {cols} columns" '
             f'viewBox="0 0 {cols * cell} {rows * cell}" '
             f'xmlns="http://www.w3.org/2000/svg">']
    for (r, c) in layout.cells:
        items.append(f'<rect x="{c * cell}" y="{r * cell}" width="{cell}" '
                     f'height="{cell}" fill="white" stroke="#333" stroke-width=".8"/>')
        if (r, c) in numbers:
            items.append(f'<text x="{c * cell + 2}" y="{r * cell + 6}" '
                         f'font-size="6" fill="#111">{numbers[(r, c)]}</text>')
    items.append("</svg>")
    return "".join(items)


def export_gallery(
    layouts: list[Layout], out_dir: Path, title: str, primary: list[Entry],
    warnings: list[str], selection: dict[str, object],
) -> None:
    """Self-contained offline gallery with source traceability and PDF links."""
    out_dir.mkdir(parents=True, exist_ok=True)
    primary_rows = {e.source_row for e in primary}
    report: dict[str, object] = {
        "title": title, "selection": selection, "warnings": warnings,
        "candidates": [],
    }
    cards = []
    for rank, layout in enumerate(layouts, 1):
        folder = out_dir / f"option-{rank:02d}"
        pdfs = export_pdfs(layout, folder, title)
        present = {p.entry.source_row for p in layout.placed}
        included = [{
            "row": p.entry.source_row, "answer": p.entry.answer,
            "clue": p.entry.clue, "priority": p.entry.priority,
            "module": p.entry.module, "lesson": p.entry.lesson,
            "borrowed": p.entry.source_row not in primary_rows,
            "direction": p.direction,
        } for p in layout.placed]
        omitted = [{
            "row": e.source_row, "answer": e.answer, "clue": e.clue,
        } for e in primary if e.source_row not in present]
        report["candidates"].append({
            "rank": rank, "score": layout.score, "metrics": layout.metrics,
            "included": included, "unused_selected_questions": omitted,
            "pdfs": {k: f"option-{rank:02d}/{v}" for k, v in pdfs.items()},
        })
        links = " ".join(
            f'<a href="option-{rank:02d}/{filename}">{label}</a>'
            for label, filename in
            (("Normal PDF", pdfs["normal"]), ("Easy PDF", pdfs["easy"]),
             ("Answer key", pdfs["key"]))
        )
        borrowed = [p for p in layout.placed if p.entry.source_row not in primary_rows]
        borrowed_text = ", ".join(
            f"{p.entry.answer} (M{p.entry.module} L{p.entry.lesson})"
            for p in borrowed) or "None"
        omitted_text = ", ".join(e["answer"] for e in omitted) or "None"
        cards.append(
            f'<article class="option"><h2>Option {rank} — {layout.score:.2f}/100</h2>'
            f'<div class="stats">{layout.metrics["words"]} answers | '
            f'{layout.metrics["words_with_2plus_crossings"]} with 2+ crossings | '
            f'{layout.metrics["rows"]} x {layout.metrics["columns"]} grid</div>'
            f'<div class="diagram">{_preview_svg(layout)}</div><nav>{links}</nav>'
            f'<p><b>Borrowed:</b> {html.escape(borrowed_text)}</p>'
            f'<p><b>Unused selected answers:</b> {html.escape(omitted_text)}</p>'
            f'</article>'
        )
    (out_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    warning_text = "".join(f"<li>{html.escape(w)}</li>" for w in warnings)
    markup = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — crossword choices</title>
<style>
body{{margin:0 auto;max-width:1150px;padding:24px;background:#f6f7f9;
color:#17212b;font:16px/1.5 system-ui,Arial,sans-serif}}
main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px}}
.option{{padding:17px;background:white;border:1px solid #d4d9df;border-radius:10px}}
.option h2{{margin:0 0 4px;font-size:1.2rem}}
.stats{{font-size:.88rem;color:#334255}}
.diagram{{max-width:100%;overflow:auto;margin:16px 0}}
svg{{display:block;width:100%;max-height:320px}}
nav{{display:flex;gap:8px;flex-wrap:wrap}}
a{{color:#123e83;text-decoration:underline}}
p{{font-size:.86rem;overflow-wrap:anywhere}}
</style></head><body>
<h1>{html.escape(title)} — top {len(layouts)} layouts</h1>
<p>Ranked by word coverage and crossing quality. All PDFs are single-page US Letter,
with 14-point squares. Normal and Easy include fillable one-character squares.
No clues or answers are invented. Details are in <a href="report.json">report.json</a>.</p>
{"<details><summary>Source notes (" + str(len(warnings)) + ")</summary><ul>" +
warning_text + "</ul></details>" if warnings else ""}
<main>{"".join(cards)}</main></body></html>"""
    (out_dir / "index.html").write_text(markup, encoding="utf-8")
