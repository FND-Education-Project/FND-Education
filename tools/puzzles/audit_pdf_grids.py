"""Diagnostic-only audit of existing crossword PDF grids. Does not modify files."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import fitz
from io import BytesIO
from PIL import Image
import numpy as np
import cv2

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
        for img in page.get_images(full=True):
            xref = img[0]
            loc = page.get_image_rects(xref)
            raw = doc.extract_image(xref)
            print(f"  embedded image xref={xref} width={raw['width']} height={raw['height']} ext={raw['ext']} bytes={len(raw['image'])} placements={loc}")
            array = np.asarray(Image.open(BytesIO(raw['image'])).convert("L"))
            mask = (array < 150).astype("uint8") * 255
            contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            boxes = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if 8 <= w <= 80 and 8 <= h <= 80 and abs(w - h) <= 3:
                    boxes.append((x, y, w, h))
            common = Counter((w, h) for _, _, w, h in boxes).most_common(5)
            if common:
                side = common[0][0][0]
                grouped = [b for b in boxes if abs(b[2] - side) <= 1 and abs(b[3] - side) <= 1]
                bounds = (min(b[0] for b in grouped), max(b[0] for b in grouped), min(b[1] for b in grouped), max(b[1] for b in grouped))
            else:
                grouped, bounds = [], None
            print(f"  CV squares: contours={len(contours)} candidates={len(boxes)} modes={common} grouped={len(grouped)} bounds={bounds} samples={grouped[:8]}")

        doc.close()
