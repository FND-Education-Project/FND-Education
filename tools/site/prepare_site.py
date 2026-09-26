#!/usr/bin/env python3
"""
Prepare canonical repository content for the Jekyll website.

The repository Markdown remains untouched. This script creates generated
website copies under web/, adding Jekyll front matter, removing repository-only
navigation/header material, and translating links for the public site.

Generated output is safe to erase and rebuild on every run.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
COURSE_ROOT = ROOT / "course"

GITHUB_BLOB_BASE = (
    "https://github.com/FND-Education-Project/FND-Education/blob/main/"
)

NAV_BLOCKS = ("BREADCRUMB", "CONTEXT")

PART_RE = re.compile(r"^part-(\d+)-", re.IGNORECASE)
MODULE_RE = re.compile(r"^module-(\d+)-", re.IGNORECASE)
LESSON_RE = re.compile(r"^(\d+)-.+\.md$", re.IGNORECASE)


@dataclass(frozen=True)
class CoursePage:
    source: Path
    part_number: int
    module_number: int
    lesson_number: int

    @property
    def public_url(self) -> str:
        return f"/course/m{self.module_number}/{self.lesson_number}/"

    @property
    def destination(self) -> Path:
        return (
            WEB
            / "course"
            / f"m{self.module_number}"
            / str(self.lesson_number)
            / "index.md"
        )

    @property
    def jekyll_path(self) -> str:
        return self.destination.relative_to(WEB).as_posix()


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


def normalize_audience_separators(text: str) -> str:
    """
    Replace only the horizontal-rule marker immediately following the
    Research and Sources audience link.

    Arbitrary *** sequences are left alone because they can legitimately mean
    strong+italic emphasis in Markdown.
    """
    return re.sub(
        r"(\[Research and Sources\]\(#research-and-sources\)[ \t]*\n)"
        r"[ \t]*\*\*\*[ \t]*(?=\n|$)",
        r"\1\n---\n",
        text,
    )


def discover_course_pages() -> list[CoursePage]:
    """Find numbered lesson pages and derive their structural numbers."""
    pages: list[CoursePage] = []

    for source in COURSE_ROOT.rglob("*.md"):
        lesson_match = LESSON_RE.match(source.name)
        module_match = MODULE_RE.match(source.parent.name)

        if not lesson_match or not module_match:
            continue

        part_dir = source.parent.parent.name
        part_match = PART_RE.match(part_dir)

        if not part_match:
            raise ValueError(
                f"Could not determine course part from {source.relative_to(ROOT)}"
            )

        pages.append(
            CoursePage(
                source=source,
                part_number=int(part_match.group(1)),
                module_number=int(module_match.group(1)),
                lesson_number=int(lesson_match.group(1)),
            )
        )

    pages.sort(
        key=lambda page: (
            page.module_number,
            page.lesson_number,
            page.source.as_posix(),
        )
    )

    # A short URL must identify exactly one source page.
    seen: dict[str, Path] = {}
    for page in pages:
        if page.public_url in seen:
            raise ValueError(
                "Duplicate public course URL "
                f"{page.public_url}: {seen[page.public_url]} and {page.source}"
            )
        seen[page.public_url] = page.source

    return pages


def extract_title(text: str, source: Path) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"No level-1 title found in {source.relative_to(ROOT)}")
    return match.group(1).strip()


def extract_status_and_authorship(text: str, source: Path) -> tuple[str, str]:
    match = re.search(
        r"^>\s*\*\*Working draft:\*\*\s*(.+?)\s*$",
        text,
        re.MULTILINE,
    )
    if not match:
        raise ValueError(
            f"No Working draft line found in {source.relative_to(ROOT)}"
        )

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


def strip_website_header_material(text: str, source: Path) -> tuple[str, str]:
    """
    Remove source-only material already represented by the website layout.

    Returns:
        cleaned Markdown body
        opening description
    """
    text = remove_nav_blocks(text)
    text = normalize_audience_separators(text)

    text, count = re.subn(
        r"^#\s+.+?\s*$",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(
            f"Expected one opening H1 in {source.relative_to(ROOT)}"
        )

    text, count = re.subn(
        r"^>\s*\*\*Working draft:\*\*.*?\s*$",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(
            f"Expected one Working draft block in {source.relative_to(ROOT)}"
        )

    # After the repository breadcrumb, H1 and Working draft box are removed,
    # the first ordinary paragraph is the website description.
    text = text.lstrip()
    parts = re.split(r"\n\s*\n", text, maxsplit=1)

    if len(parts) != 2:
        raise ValueError(
            f"Could not identify opening description in "
            f"{source.relative_to(ROOT)}"
        )

    description = " ".join(line.strip() for line in parts[0].splitlines()).strip()
    body = parts[1].lstrip()

    # If a page has this editorial line in its body, the website status area
    # already carries the same information.
    body = re.sub(
        r"^\*Last reviewed:\s*.+?\*\s*$",
        "",
        body,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    return body.strip() + "\n", description


def clean_generated_course() -> None:
    """Erase only the generated course tree, preserving its placeholder."""
    course_web = WEB / "course"
    course_web.mkdir(parents=True, exist_ok=True)

    for child in course_web.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def copy_public_asset_trees() -> None:
    """
    Copy the explicitly approved shared asset trees into the Jekyll source.

    Site-owned CSS, JavaScript and icons already live directly under web/assets
    and are not touched.
    """
    for dirname in ("illustrations", "images", "puzzles"):
        src = ROOT / "assets" / dirname
        dst = WEB / "assets" / dirname

        if dst.exists():
            shutil.rmtree(dst)

        if src.exists():
            shutil.copytree(src, dst)


def copy_referenced_asset(resolved: Path) -> None:
    """Copy a referenced non-Markdown repository file to the same public path."""
    resolved = resolved.resolve()

    try:
        relative = resolved.relative_to(ROOT.resolve())
    except ValueError:
        return

    # Shared assets are copied as complete approved trees above.
    if relative.parts and relative.parts[0] == "assets":
        return

    destination = WEB / relative
    destination.parent.mkdir(parents=True, exist_ok=True)

    if resolved.is_file():
        shutil.copy2(resolved, destination)


def relative_url_liquid(public_path: str) -> str:
    return "{{ " + yaml_string(public_path) + " | relative_url }}"


def rewrite_relative_links(
    markdown: str,
    source_file: Path,
    page_url_map: dict[Path, str],
) -> str:
    """
    Translate links in the generated website copy.

    - Course lesson Markdown -> its short website URL.
    - Published non-Markdown assets -> corresponding public asset path.
    - Other repository Markdown -> canonical GitHub source for now.
    - External URLs and same-page fragments -> unchanged.

    As landing/reference layouts are generated, their Markdown paths will be
    added to the website URL map and will automatically stop falling back to
    GitHub.
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

        # Older course links sometimes used a local crosswords/ folder. The
        # canonical puzzle PDFs now live in assets/puzzles/crosswords/.
        if not resolved.exists() and path_part.startswith("crosswords/"):
            fallback = (
                ROOT
                / "assets"
                / "puzzles"
                / "crosswords"
                / Path(path_part).name
            )
            if fallback.exists():
                resolved = fallback.resolve()

        if not resolved.exists():
            return match.group(0)

        mapped_url = page_url_map.get(resolved)

        if mapped_url:
            public_path = mapped_url
            if separator:
                public_path += "#" + fragment

            return (
                f"{match.group('prefix')}"
                f"{relative_url_liquid(public_path)}"
                f"{match.group('suffix')}"
            )

        try:
            relative = resolved.relative_to(ROOT.resolve())
        except ValueError:
            return match.group(0)

        if resolved.suffix.lower() == ".md":
            github_url = GITHUB_BLOB_BASE + relative.as_posix()
            if separator:
                github_url += "#" + fragment
            return (
                f"{match.group('prefix')}"
                f"{github_url}"
                f"{match.group('suffix')}"
            )

        copy_referenced_asset(resolved)

        public_path = "/" + relative.as_posix()
        if separator:
            public_path += "#" + fragment

        return (
            f"{match.group('prefix')}"
            f"{relative_url_liquid(public_path)}"
            f"{match.group('suffix')}"
        )

    return pattern.sub(replace, markdown)


def render_front_matter(
    page: CoursePage,
    title: str,
    description: str,
    status: str,
    authorship: str,
    last_reviewed: str | None,
) -> str:
    lines = [
        "---",
        "layout: course",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description)}",
        f"status: {status}",
        f"authorship: {authorship}",
    ]

    if last_reviewed:
        lines.append(f"last_reviewed: {yaml_string(last_reviewed)}")

    lines.extend(
        [
            f"permalink: {page.public_url}",
            "---",
            "",
        ]
    )

    return "\n".join(lines)


def write_generated_page_data(pages: list[CoursePage]) -> None:
    """Write structural data used by layouts, regenerated from scratch."""
    generated_dir = WEB / "_data" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []

    for page in pages:
        lines.extend(
            [
                f"{yaml_string(page.jekyll_path)}:",
                f"  part_number: {page.part_number}",
                f"  module_number: {page.module_number}",
                f"  lesson_number: {page.lesson_number}",
            ]
        )

    (generated_dir / "pages.yml").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    # Detailed previous/next/parent navigation comes in the next site pass.
    (generated_dir / "navigation.yml").write_text("{}\n", encoding="utf-8")


def prepare_course(pages: list[CoursePage]) -> None:
    page_url_map = {
        page.source.resolve(): page.public_url
        for page in pages
    }

    errors: list[str] = []

    for page in pages:
        try:
            source_text = page.source.read_text(encoding="utf-8")

            title = extract_title(source_text, page.source)
            status, authorship = extract_status_and_authorship(
                source_text,
                page.source,
            )
            last_reviewed = extract_last_reviewed(source_text)

            body, description = strip_website_header_material(
                source_text,
                page.source,
            )

            body = rewrite_relative_links(
                body,
                page.source,
                page_url_map,
            )

            page.destination.parent.mkdir(parents=True, exist_ok=True)
            page.destination.write_text(
                render_front_matter(
                    page=page,
                    title=title,
                    description=description,
                    status=status,
                    authorship=authorship,
                    last_reviewed=last_reviewed,
                )
                + body,
                encoding="utf-8",
            )

        except Exception as exc:  # collect all page problems in one run
            errors.append(f"{page.source.relative_to(ROOT)}: {exc}")

    if errors:
        joined = "\n  - ".join(errors)
        raise RuntimeError(
            "Course preparation stopped because some pages did not match "
            f"the expected source pattern:\n  - {joined}"
        )


def main() -> None:
    pages = discover_course_pages()

    clean_generated_course()
    copy_public_asset_trees()
    prepare_course(pages)
    write_generated_page_data(pages)

    print("Prepared Jekyll website source.")
    print(f"  Course lessons generated: {len(pages)}")
    print("  Public course pattern:     /course/m{module}/{lesson}/")
    print("  Canonical Markdown files:  unchanged")


if __name__ == "__main__":
    main()
