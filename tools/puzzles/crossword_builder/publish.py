"""Accessible one-page crossword PDF editions and an offline review gallery.

The page geometry is *measured* before anything is written. The layout
selects the most readable combination that fits: 14–12 pt clues, 16–14 pt
squares, and 36–24 pt margins. No missing clues, split puzzle pages, or
unannounced below-minimum font sizes are allowed.
"""
from __future__ import annotations

from dataclasses import dataclass
import html
import json
from pathlib import Path

import pymupdf as fitz

from .core import Entry, Layout, _points, verify_layout

WIDTH, HEIGHT = 612.0, 792.0  # US Letter, PDF points
SQUARE_SIZES = (16.0, 15.0, 14.0)
CLUE_FONTS = (14.0, 13.0, 12.0)
MARGINS = (36.0, 30.0, 24.0)
TITLE_FONT = 15.0  # Keep the same title size in preview and final editions.


@dataclass
class PrintPlan:
    """Precisely measured page geometry shared by Normal, Easy, and Key."""
    grid_x: float
    grid_y: float
    square: float
    margin: float
    font_size: float
    regions: list[tuple[float, float, float, float]]
    clues: list[tuple[float, float, str, float, bool]]
    bank_top: float
    bank_lines: list[str]
    divider_end: float


def _width(text: str, size: float, bold: bool = False) -> float:
    return fitz.get_text_length(
        text, fontname="hebo" if bold else "helv", fontsize=size
    )


def _wrap(text: str, width: float, size: float) -> list[str]:
    """Wrap without losing words, including unusually long single words."""
    lines: list[str] = []
    for paragraph in text.splitlines() or [""]:
        current = ""
        for word in paragraph.split():
            trial = f"{current} {word}".strip()
            if _width(trial, size) <= width:
                current = trial
                continue
            if current:
                lines.append(current)
                current = ""
            if _width(word, size) <= width:
                current = word
            else:
                fragment = ""
                for char in word:
                    if fragment and _width(fragment + char, size) > width:
                        lines.append(fragment)
                        fragment = char
                    else:
                        fragment += char
                current = fragment
        if current:
            lines.append(current)
        elif not paragraph.strip():
            lines.append("")
    return lines


def _try_plan(
    layout: Layout, font_size: float, square: float, margin: float
) -> PrintPlan | None:
    """Try an entire Easy edition; other editions then fit by construction."""
    rows, cols = layout.size()
    grid_width, grid_height = cols * square, rows * square
    grid_y = margin + 32
    if grid_width > WIDTH - margin * 2 or grid_y + grid_height > HEIGHT - margin - 110:
        return None

    # Reserve exactly the space needed for the full word bank in Easy.
    bank_font = 9.5
    original_answers = sorted(p.entry.original_answer.upper() for p in layout.placed)
    bank_lines = _wrap("  |  ".join(original_answers), WIDTH - 2 * margin - 8, bank_font)
    bank_height = 19 + len(bank_lines) * 12.0
    bank_top = HEIGHT - margin - bank_height
    if bank_top < grid_y + 32:
        return None
    clue_end = bank_top - 14
    if clue_end <= grid_y + 18:
        return None

    # Distribute content over the space alongside the grid and the two
    # ruled columns below. Wide grids are centred above two columns.
    spare_width = WIDTH - 2 * margin - grid_width - 14
    has_side = spare_width >= max(155, font_size * 11) and grid_height >= 120
    grid_x = margin if has_side else (WIDTH - grid_width) / 2
    below_top = grid_y + grid_height + 15
    if below_top >= clue_end:
        return None
    middle = WIDTH / 2
    regions: list[tuple[float, float, float, float]] = []
    if has_side:
        regions.append((
            margin + grid_width + 14, grid_y,
            WIDTH - margin, min(grid_y + grid_height, clue_end)
        ))
    regions.extend([
        (margin, below_top, middle - 12, clue_end),
        (middle + 12, below_top, WIDTH - margin, clue_end),
    ])
    numbering = layout.numbered()
    sections: list[tuple[bool, str]] = [(True, "Across")]
    sections.extend(
        (False, f"{n}. {p.entry.clue}") for n, p in numbering
        if p.direction == "across"
    )
    sections.append((True, "Down"))
    sections.extend(
        (False, f"{n}. {p.entry.clue}") for n, p in numbering
        if p.direction == "down"
    )

    output: list[tuple[float, float, str, float, bool]] = []
    region = 0
    cursor = regions[region][1]
    line_height = font_size * 1.22
    baseline_by_region: dict[int, float] = {}
    for is_heading, content in sections:
        size = font_size + 1.0 if is_heading else font_size
        while True:
            if region >= len(regions):
                return None
            x0, top, x1, bottom = regions[region]
            lines = [content] if is_heading else _wrap(content, x1 - x0 - 6, font_size)
            padding = 5.0 if is_heading else 3.0
            needed = len(lines) * line_height + padding
            if cursor + needed <= bottom:
                cursor += padding
                for line in lines:
                    baseline = cursor + size
                    output.append((x0 + 3, baseline, line, size, is_heading))
                    baseline_by_region[region] = baseline
                    cursor += line_height
                break
            region += 1
            if region < len(regions):
                cursor = regions[region][1]

    # The divider should end after actual text, not extend through blank paper.
    below_start = len(regions) - 2
    divider_end = max(
        regions[below_start][1],
        baseline_by_region.get(below_start, regions[below_start][1]),
        baseline_by_region.get(below_start + 1, regions[below_start + 1][1]),
    ) + 4
    return PrintPlan(
        grid_x, grid_y, square, margin, font_size, regions,
        output, bank_top, bank_lines, divider_end
    )


def plan_page(layout: Layout) -> PrintPlan:
    """Prefer clear 14 pt clues/16 pt cells; relax only within approved floors."""
    # Work inward from readability: try each font, then cell size,
    # then 0.5" → 0.42" → 0.33" margins.
    for font in CLUE_FONTS:
        for square in SQUARE_SIZES:
            for margin in MARGINS:
                plan = _try_plan(layout, font, square, margin)
                if plan:
                    return plan
    raise ValueError(
        "The complete puzzle cannot fit one US Letter page with at least "
        "12 pt clues and 14 pt squares. Try fewer answers or shorter clues."
    )


def title_measure(title: str, layout: Layout) -> tuple[float, float]:
    """Return title width and available width at the fixed 15 pt title font."""
    plan = plan_page(layout)
    return _width(title.strip(), TITLE_FONT, bold=True), WIDTH - 2 * plan.margin


def validate_title(title: str, layout: Layout) -> str:
    """Never shrink, truncate or wrap a user-selected crossword title."""
    title = title.strip()
    if not title or any(char in title for char in "\n\r\t"):
        raise ValueError("Enter a single-line title.")
    if len(title) > 120:
        raise ValueError("Title is too long. Use at most 120 characters.")
    used, available = title_measure(title, layout)
    if used > available + .01:
        raise ValueError(
            f"Title is {used:.0f} points wide but this layout permits "
            f"{available:.0f} points at {TITLE_FONT:g} pt. Shorten the title."
        )
    return title


def blocked_cells(layout: Layout) -> set[tuple[int, int]]:
    """All unoccupied squares inside the rectangular crossword border."""
    rows, cols = layout.size()
    return {
        (row, col)
        for row in range(rows) for col in range(cols)
        if (row, col) not in layout.cells
    }


def restore_layout(candidate: dict) -> Layout:
    """Re-create one candidate exactly from the traceable layout report.

    The user may rename the selected puzzle without regenerating or
    renumbering its grid.
    """
    from .core import _place
    layout = Layout()
    for item in candidate["included"]:
        entry = Entry(
            clue=item["clue"],
            original_answer=item.get("original_answer", item["answer"]),
            answer=item["answer"],
            priority=int(item["priority"]),
            lesson=int(item["lesson"]), module=int(item["module"]),
            source_row=int(item["row"]),
        )
        _place(layout, entry, int(item["grid_row"]),
               int(item["grid_col"]), item["direction"])
    layout = layout.normalized()
    verify_layout(layout)
    layout.score = float(candidate.get("score", 0))
    layout.metrics = dict(candidate.get("metrics", {}))
    return layout


def is_printable(layout: Layout) -> bool:
    try:
        plan_page(layout)
        return True
    except ValueError:
        return False


def _tab_sequence(layout: Layout) -> list[tuple[int, int]]:
    """Across-first field order, with every square appearing exactly once."""
    order: list[tuple[int, int]] = []
    seen = set()
    for orientation in ("across", "down"):
        for _, placed in layout.numbered():
            if placed.direction != orientation:
                continue
            for coord in _points(placed):
                if coord not in seen:
                    order.append(coord)
                    seen.add(coord)
    if seen != set(layout.cells):
        raise ValueError("Some writable crossword squares were not numbered.")
    return order


def _draw_page(
    page: fitz.Page, layout: Layout, plan: PrintPlan,
    edition: str, title: str
) -> list[tuple[int, int]]:
    """Draw the same grid and clues across all editions."""
    x, y, side, margin = plan.grid_x, plan.grid_y, plan.square, plan.margin
    page.insert_text((margin, margin + TITLE_FONT), title,
                     fontsize=TITLE_FONT, fontname="hebo")
    numbering = {(p.row, p.col): n for n, p in layout.numbered()}
    # A complete, conventional crossword rectangle: every square without
    # an answer letter is black. The small outer border is intentional.
    rows, cols = layout.size()
    board = fitz.Rect(x, y, x + cols * side, y + rows * side)
    page.draw_rect(board, fill=(.08, .08, .08), color=(.1, .1, .1), width=.9)
    for (r, c), ch in sorted(layout.cells.items()):
        rect = fitz.Rect(
            x + c * side, y + r * side, x + (c + 1) * side, y + (r + 1) * side
        )
        page.draw_rect(rect, color=(.15, .15, .15),
                       fill=(1, 1, 1), width=.65)
        if (r, c) in numbering:
            page.insert_text((rect.x0 + 1.5, rect.y0 + 6.0),
                             str(numbering[r, c]), fontsize=5.6, fontname="helv")
        if edition == "key":
            page.insert_text((rect.x0 + side * .24, rect.y1 - 3.6),
                             ch, fontsize=min(12.0, side * .7), fontname="hebo")
    start_below = plan.regions[-2][1]
    if plan.divider_end > start_below + 6:
        page.draw_line(
            (WIDTH / 2, start_below),
            (WIDTH / 2, min(plan.divider_end, plan.bank_top - 12)),
            color=(.7, .7, .7), width=.5
        )
    for tx, baseline, sentence, size, heading in plan.clues:
        page.insert_text((tx, baseline), sentence, fontsize=size,
                         fontname="hebo" if heading else "helv")
    if edition == "easy":
        page.draw_line((margin, plan.bank_top - 4),
                       (WIDTH - margin, plan.bank_top - 4),
                       color=(.6, .6, .6), width=.6)
        page.insert_text((margin, plan.bank_top + 11),
                         "Word bank", fontsize=11, fontname="hebo")
        for i, sentence in enumerate(plan.bank_lines):
            page.insert_text((margin, plan.bank_top + 24 + i * 12),
                             sentence, fontsize=9.5, fontname="helv")
    return _tab_sequence(layout)


def _save_pdf(layout: Layout, edition: str, destination: Path, title: str) -> None:
    verify_layout(layout)
    title = validate_title(title, layout)
    plan = plan_page(layout)
    doc = fitz.open()
    page = doc.new_page(width=WIDTH, height=HEIGHT)
    sequence = _draw_page(page, layout, plan, edition, title)
    if edition != "key":
        for r, c in sequence:
            x = plan.grid_x + c * plan.square
            y = plan.grid_y + r * plan.square
            field = fitz.Widget()
            field.field_name = f"cell_{r}_{c}"
            field.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            field.field_value = ""
            field.text_maxlen = 1
            field.text_align = 1
            field.text_font = "Helv"
            field.text_fontsize = min(11, plan.square * .7)
            field.text_color = (0, 0, 0)
            field.border_width = 0
            field.fill_color = None
            # Leave clue number visible in the upper-left of each square.
            field.rect = fitz.Rect(
                x + .8, y + 4.5, x + plan.square - .8, y + plan.square - 2.0
            )
            page.add_widget(field)
        doc.xref_set_key(page.xref, "Tabs", "/A")
    doc.set_metadata({"title": title, "subject": f"Crossword: {edition}"})
    doc.save(str(destination), deflate=True, garbage=4)
    doc.close()
    check = fitz.open(str(destination))
    try:
        if len(check) != 1 or check[0].rect != fitz.Rect(0, 0, WIDTH, HEIGHT):
            raise ValueError("PDF is not a single letter-size page.")
        fields = list(check[0].widgets() or [])
        expected = 0 if edition == "key" else len(sequence)
        if len(fields) != expected:
            raise ValueError("PDF form field count differs from the crossword grid.")
        if edition != "key":
            if any(w.text_maxlen != 1 for w in fields):
                raise ValueError("A PDF field accepts more than one letter.")
            if [w.field_name for w in fields] != [
                f"cell_{r}_{c}" for r, c in sequence
            ]:
                raise ValueError("PDF lost its Across-first tab order.")
            if check.xref_get_key(check[0].xref, "Tabs") != ("name", "/A"):
                raise ValueError("PDF missing /Tabs /A.")
    finally:
        check.close()


def export_pdfs(layout: Layout, folder: Path, title: str) -> dict[str, str]:
    """Write and individually validate three matching crossword editions."""
    folder.mkdir(parents=True, exist_ok=True)
    editions = {"normal": "normal.pdf", "easy": "easy.pdf",
                "key": "answer-key.pdf"}
    try:
        for edition, filename in editions.items():
            _save_pdf(layout, edition, folder / filename, title)
    except Exception:
        for filename in editions.values():
            (folder / filename).unlink(missing_ok=True)
        raise
    return editions


def _preview_svg(layout: Layout) -> str:
    """Scalable grid preview; only numbers/coordinates are interpolated."""
    rows, cols = layout.size()
    pitch = 19
    numbers = {(p.row, p.col): n for n, p in layout.numbered()}
    out = [
        f'<svg role="img" aria-label="Crossword grid: {rows} rows, {cols} columns" '
        f'viewBox="0 0 {cols * pitch} {rows * pitch}" '
        'xmlns="http://www.w3.org/2000/svg">'
    ]
    out.append(f'<rect x="0" y="0" width="{cols * pitch}" '
               f'height="{rows * pitch}" fill="#171717" stroke="#333"/>')
    for (r, c) in layout.cells:
        out.append(f'<rect x="{c * pitch}" y="{r * pitch}" '
                   f'width="{pitch}" height="{pitch}" '
                   'fill="white" stroke="#333" stroke-width=".8"/>')
        if (r, c) in numbers:
            out.append(f'<text x="{c * pitch + 2}" y="{r * pitch + 7}" '
                       f'font-size="7" fill="#111">{numbers[r, c]}</text>')
    return "".join(out) + "</svg>"


def export_gallery(
    layouts: list[Layout], out_dir: Path, title: str, primary: list[Entry],
    warnings: list[str], selection: dict[str, object],
    progress=None,
) -> None:
    """Publish up to five ranked options to a standalone offline review page."""
    out_dir.mkdir(parents=True, exist_ok=True)
    source_rows = {e.source_row for e in primary}
    report: dict[str, object] = {
        "title": title, "selection": selection,
        "warnings": warnings, "candidates": []
    }
    cards: list[str] = []
    for rank, layout in enumerate(layouts, 1):
        folder = out_dir / f"option-{rank:02d}"
        pdfs = export_pdfs(layout, folder, title)
        if progress is not None:
            progress(rank, len(layouts))
        plan = plan_page(layout)
        present = {p.entry.source_row for p in layout.placed}
        included = [
            {
                "row": p.entry.source_row, "answer": p.entry.answer,
                "original_answer": p.entry.original_answer,
                "grid_row": p.row, "grid_col": p.col,
                "clue": p.entry.clue, "priority": p.entry.priority,
                "module": p.entry.module, "lesson": p.entry.lesson,
                "borrowed": p.entry.source_row not in source_rows,
                "direction": p.direction,
            }
            for p in layout.placed
        ]
        omitted = [
            {"row": e.source_row, "answer": e.answer, "clue": e.clue}
            for e in primary if e.source_row not in present
        ]
        report["candidates"].append({
            "rank": rank, "score": layout.score, "metrics": layout.metrics,
            "print": {"clue_font_pt": plan.font_size, "square_pt": plan.square,
                      "margin_pt": plan.margin},
            "included": included,
            "unused_selected_questions": omitted,
            "pdfs": {k: f"option-{rank:02d}/{v}" for k, v in pdfs.items()}
        })
        links = " ".join(
            f'<a href="option-{rank:02d}/{filename}">{label}</a>'
            for label, filename in (
                ("Normal PDF", pdfs["normal"]),
                ("Easy PDF", pdfs["easy"]),
                ("Answer key", pdfs["key"]),
            )
        )
        borrowed = [p for p in layout.placed if p.entry.source_row not in source_rows]
        borrowed_names = ", ".join(
            f"{p.entry.answer} (M{p.entry.module} L{p.entry.lesson})"
            for p in borrowed
        ) or "None"
        omitted_names = ", ".join(e["answer"] for e in omitted) or "None"
        cards.append(
            f'<article class="option"><h2>Option {rank} — {layout.score:.2f}/100</h2>'
            f'<p class="stats">{layout.metrics["words"]} answers · '
            f'{layout.metrics["words_with_2plus_crossings"]} with 2+ crossings · '
            f'{plan.square:g} pt cells · {plan.font_size:g} pt clues</p>'
            f'<div class="diagram">{_preview_svg(layout)}</div>'
            f'<nav>{links}</nav>'
            f'<p><b>Borrowed:</b> {html.escape(borrowed_names)}</p>'
            f'<p><b>Unused selected answers:</b> {html.escape(omitted_names)}</p>'
            '</article>'
        )
    (out_dir / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    notes = "".join(f"<li>{html.escape(w)}</li>" for w in warnings)
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
.stats{{font-size:.92rem;color:#334255}}
.diagram{{max-width:100%;overflow:auto;margin:16px 0}}
svg{{display:block;width:100%;max-height:320px}}
nav{{display:flex;gap:8px;flex-wrap:wrap}}
a{{color:#123e83;text-decoration:underline}}
p{{font-size:.91rem;overflow-wrap:anywhere}}
</style></head><body>
<h1>{html.escape(title)} — top {len(layouts)} layouts</h1>
<p>Each puzzle is one US Letter page. Clues use 12–14 pt type and squares
use 14–16 pt sides; no material is clipped or dropped to fit.
Normal and Easy have fillable one-character squares.
See <a href="report.json">report.json</a> for source references.</p>
{"<details><summary>Source notes (" + str(len(warnings)) + ")</summary><ul>" +
notes + "</ul></details>" if warnings else ""}
<main>{"".join(cards)}</main></body></html>"""
    (out_dir / "index.html").write_text(markup, encoding="utf-8")
