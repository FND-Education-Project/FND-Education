"""Diagnostic-only audit of existing crossword PDF grids. Does not modify files."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import fitz

ROOT = Path("assets/puzzles/crosswords")
STEMS = ("What-is-FND-crossword", "Biopsychosocial-What-crossword", "Recovery-crossword")
for stem in STEMS:
    for variant in ("", "-easy", "-answer-key"):
        path = ROOT / f"{stem}{variant}-09-2026.pdf"
        if not path.exists():
            print("NOT FOUND", path)
            continue
        doc = fitz.open(path)
        page = doc[0]
        squares = []
        for draw in page.get_drawings():
            r = draw["rect"]
            if 6 <= r.width <= 28 and 6 <= r.height <= 28 and abs(r.width - r.height) < 0.9:
                squares.append(r)
        common = Counter(round(r.width * 2) / 2 for r in squares).most_common(1)
        width = common[0][0] if common else None
        group = [r for r in squares if width is not None and abs(r.width - width) <= 0.6]
        bbox = fitz.Rect(min(r.x0 for r in group), min(r.y0 for r in group), max(r.x1 for r in group), max(r.y1 for r in group)) if group else None
        print(f"{path.name}: pages={len(doc)} page_points={page.rect.width:.0f}x{page.rect.height:.0f} widgets={len(list(page.widgets() or []))} images={len(page.get_images())} drawings={len(page.get_drawings())} squares={len(group)} side={width} bbox={bbox} extracted_chars={len(page.get_text())}")
        if group:
            xs = sorted(set(round(r.x0, 1) for r in group))
            ys = sorted(set(round(r.y0, 1) for r in group))
            print(f"  grid columns={len(xs)} rows={len(ys)} first-x={xs[:8]} first-y={ys[:8]}")
        doc.close()
