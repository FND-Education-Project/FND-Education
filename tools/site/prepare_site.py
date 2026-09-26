#!/usr/bin/env python3
"""
Prepare repository Markdown for the Jekyll website.

The canonical Markdown files remain untouched. This script creates a generated
website copy under web/, adding Jekyll front matter and removing content that is
already supplied by the website layout.

This first version intentionally prepares only Course Module 1, Page 1. Once the
rendered result is approved, the same rules will be generalized across the
course and then the reference section.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"

SOURCE_PAGE = (
    ROOT
    / "course"
    / "part-1-understanding-fnd"
    / "module-01-what-fnd-is"
    / "01-what-functional-means-and-how-fnd-can-appear.md"
)

DEST_PAGE = WEB / "course" / "m1" / "1" / "index.md"

PUBLIC_URL = "/course/m1/1/"

NAV_BLOCKS = (
    "BREADCRUMB",
    "CONTEXT",
)


def yaml_string(value: str) -> str:
    """Return a double-quoted YAML-safe scalar using JSON escaping."""
    return json.dumps(value, ensure_ascii=False)


def remove_nav_blocks(text: str) -> str:
    """Remove repository-only navigation blocks from the website copy."""
    for name in NAV_BLOCKS:
        pattern = re.compile(
            rf"\\?<!--\s*NAV-{name}:START\s*-->.*?"
            rf"<!--\s*NAV-{name}:END\s*-->\s*",
            re.IGNORECASE | re.DOTALL,
        )
        text = pattern.sub("", text)
    return text


def extract_title(text: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"No level-1 title found in {SOURCE_PAGE}")
    return match.group(1).strip()


def extract_status_and_authorship(text: str) -> tuple[str, str]:
    match = re.search(
        r"^>\s*\*\*Working draft:\*\*\s*(.+?)\s*$",
        text,
        re.MULTILINE,
    )
    if not match:
        raise ValueError(f"No Working draft line found in {SOURCE_PAGE}")

    wording = match.group(1).lower()

    if "automatically generated" in wording:
        authorship = "automatically-generated"
    elif "human authored" in wording:
        authorship = "human"
    else:
        authorship = "unspecified"

    return "working-draft", authorship


def extract_last_reviewed(text: str) -> str | None:
    match = re.search(
        r"^\*Last reviewed:\s*(.+?)\*\s*$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def normalize_audience_separators(text: str) -> str:
    """
    Replace only the horizontal-rule marker immediately following the
    Research and Sources audience link.

    This deliberately does not replace arbitrary *** sequences because those
    can legitimately represent emphasis elsewhere in Markdown.
    """
    return re.sub(
        r"(\[Research and Sources\]\(#research-and-sources\)[ \t]*\n)"
        r"[ \t]*\*\*\*[ \t]*(?=\n|$)",
        r"\1\n---\n",
        text,
    )


def strip_website_header_material(text: str) -> tuple[str, str]:
    """
    Remove material already represented by the Jekyll page heading.

    Returns:
        cleaned Markdown body
        opening description
    """
    text = remove_nav_blocks(text)
    text = normalize_audience_separators(text)

    # The Jekyll course layout supplies the H1.
    text, count = re.subn(
        r"^#\s+.+?\s*$",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError("Expected exactly one opening H1 to remove")

    # The Jekyll status bar replaces the original repository blockquote.
    text, count = re.subn(
        r"^>\s*\*\*Working draft:\*\*.*?\s*$",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError("Expected exactly one Working draft block to remove")

    # The first paragraph remaining at the top is the page description.
    text = text.lstrip()
    parts = re.split(r"\n\s*\n", text, maxsplit=1)

    if len(parts) != 2:
        raise ValueError("Could not identify the opening description")

    description = " ".join(line.strip() for line in parts[0].splitlines()).strip()
    body = parts[1].lstrip()

    # The top status bar already carries this information on the website.
    body = re.sub(
        r"^\*Last reviewed:\s*.+?\*\s*$",
        "",
        body,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    return body.strip() + "\n", description


def copy_public_assets() -> None:
    """
    Copy non-Markdown assets that are allowed to appear on the website.

    Site-only CSS, JavaScript, and icons already live under web/assets and are
    not touched here.
    """
    for dirname in ("illustrations", "images", "puzzles"):
        src = ROOT / "assets" / dirname
        dst = WEB / "assets" / dirname

        if dst.exists():
            shutil.rmtree(dst)

        if src.exists():
            shutil.copytree(src, dst)


def rewrite_relative_links(markdown: str, source_file: Path) -> str:
    """
    Rewrite relative links to published static files.

    Markdown-page-to-public-page rewriting will be expanded after the complete
    page URL map is generated. Fragment links and external URLs are unchanged.
    """
    pattern = re.compile(
        r"(?P<prefix>!?\[[^\]]*\]\()"
        r"(?P<target>[^)\s]+)"
        r"(?P<suffix>\))"
    )

    def replace(match: re.Match[str]) -> str:
        target = match.group("target")

        if (
            target.startswith("#")
            or target.startswith("/")
            or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)
            or target.startswith("{{")
        ):
            return match.group(0)

        path_part, separator, fragment = target.partition("#")

        resolved = (source_file.parent / path_part).resolve()

        # A few older course links use crosswords/<file>, while the PDFs now
        # live in assets/puzzles/crosswords/. Preserve those links on the site.
        if not resolved.exists() and path_part.startswith("crosswords/"):
            fallback = ROOT / "assets" / "puzzles" / "crosswords" / Path(path_part).name
            if fallback.exists():
                resolved = fallback.resolve()

        try:
            relative = resolved.relative_to(ROOT.resolve())
        except ValueError:
            return match.group(0)

        if not resolved.exists():
            return match.group(0)

        # Markdown-to-Markdown links will be handled by the complete URL map.
        if resolved.suffix.lower() == ".md":
            return match.group(0)

        public_path = "/" + relative.as_posix()
        if separator:
            public_path += "#" + fragment

        liquid_target = "{{ " + yaml_string(public_path) + " | relative_url }}"
        return f"{match.group('prefix')}{liquid_target}{match.group('suffix')}"

    return pattern.sub(replace, markdown)


def write_generated_page_data() -> None:
    """Create the small generated data file used by the course layout."""
    generated_dir = WEB / "_data" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    pages = generated_dir / "pages.yml"
    pages.write_text(
        "course/m1/1/index.md:\n"
        "  part_number: 1\n"
        "  module_number: 1\n"
        "  lesson_number: 1\n",
        encoding="utf-8",
    )

    navigation = generated_dir / "navigation.yml"
    navigation.write_text("{}\n", encoding="utf-8")


def prepare_course_page() -> None:
    source = SOURCE_PAGE.read_text(encoding="utf-8")

    title = extract_title(source)
    status, authorship = extract_status_and_authorship(source)
    last_reviewed = extract_last_reviewed(source)

    body, description = strip_website_header_material(source)
    body = rewrite_relative_links(body, SOURCE_PAGE)

    front_matter = [
        "---",
        "layout: course",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description)}",
        f"status: {status}",
        f"authorship: {authorship}",
    ]

    if last_reviewed:
        front_matter.append(f"last_reviewed: {yaml_string(last_reviewed)}")

    front_matter.extend(
        [
            f"permalink: {PUBLIC_URL}",
            "---",
            "",
        ]
    )

    DEST_PAGE.parent.mkdir(parents=True, exist_ok=True)
    DEST_PAGE.write_text(
        "\n".join(front_matter) + body,
        encoding="utf-8",
    )


def main() -> None:
    copy_public_assets()
    prepare_course_page()
    write_generated_page_data()

    print("Prepared Jekyll website source.")
    print(f"  Source:      {SOURCE_PAGE.relative_to(ROOT)}")
    print(f"  Generated:   {DEST_PAGE.relative_to(ROOT)}")
    print(f"  Public URL:  {PUBLIC_URL}")


if __name__ == "__main__":
    main()
