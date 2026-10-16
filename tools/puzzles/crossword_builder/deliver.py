"""Export exactly one chosen crossword under human-readable publication names.

Filename rules:
- ZIP: Module-2-Lesson-5.zip / Module-2.zip / Whole-Course.zip
- PDFs: title-m2-5-normal.pdf, title-m2-5-easy.pdf,
        title-m2-5-answer-key.pdf (analogous module/all labels).
The answer grid is restored from the selected layout, not re-generated.
"""
from __future__ import annotations

from io import BytesIO
import json
from pathlib import Path
import re
import unicodedata
from zipfile import ZipFile, ZIP_DEFLATED

from .publish import export_pdfs, restore_layout, validate_title


def title_slug(title: str) -> str:
    """Remove unsafe filesystem characters without altering the printed title."""
    normalized = unicodedata.normalize("NFKD", title)
    ascii_name = normalized.encode("ascii", errors="ignore").decode("ascii")
    stem = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return (stem or "crossword")[:76].strip("-")


def package_names(title: str, selection: dict) -> tuple[str, str]:
    """Return the PDF file prefix and the downloaded ZIP filename."""
    mode = selection.get("mode")
    if mode == "lesson":
        module, lesson = int(selection["module"]), int(selection["lesson"])
        if module < 1 or lesson < 1:
            raise ValueError("Module and lesson identifiers must be positive.")
        return (
            f"{title_slug(title)}-m{module}-{lesson}",
            f"Module-{module}-Lesson-{lesson}.zip",
        )
    if mode == "module":
        module = int(selection["module"])
        if module < 1:
            raise ValueError("Module identifier must be positive.")
        return f"{title_slug(title)}-m{module}", f"Module-{module}.zip"
    if mode == "all":
        return f"{title_slug(title)}-all", "Whole-Course.zip"
    raise ValueError(f"Unknown selection mode {mode!r}.")


def prepare_downloads(
    candidate: dict, selection: dict, title: str, destination: Path
) -> tuple[str, dict[str, tuple[str, bytes]], bytes]:
    """Render a re-titled chosen layout; return only its three PDFs and ZIP.

    Preparing a final title does not affect the preview PDFs, workbook or
    question bank. The same checked layout numbers, coordinates and clues
    are preserved, as is the complete word bank on Easy.
    """
    layout = restore_layout(candidate)
    title = validate_title(title, layout)
    prefix, zip_filename = package_names(title, selection)
    paths = export_pdfs(layout, destination, title)
    filenames: dict[str, tuple[str, bytes]] = {}
    for variant in ("normal", "easy", "key"):
        kind = "answer-key" if variant == "key" else variant
        name = f"{prefix}-{kind}.pdf"
        filenames[variant] = (name, (destination / paths[variant]).read_bytes())

    manifest = {
        "title": title, "selection": selection,
        "score": candidate.get("score"),
        "included": candidate["included"],
        "unused_selected_questions": candidate.get("unused_selected_questions", []),
    }
    zip_data = BytesIO()
    with ZipFile(zip_data, mode="w", compression=ZIP_DEFLATED) as archive:
        for name, data in filenames.values():
            archive.writestr(name, data)
        archive.writestr(
            f"{prefix}-sources.json",
            json.dumps(manifest, indent=2, ensure_ascii=False),
        )
    return zip_filename, filenames, zip_data.getvalue()
