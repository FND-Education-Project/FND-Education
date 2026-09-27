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

NAV_BLOCKS = ("BREADCRUMB",)

PART_RE = re.compile(r"^part-(\d+)-", re.IGNORECASE)
MODULE_RE = re.compile(r"^module-(\d+)-", re.IGNORECASE)
LESSON_RE = re.compile(r"^(\d+)-.+\.md$", re.IGNORECASE)


@dataclass(frozen=True)
class CoursePage:
    source: Path
    kind: str
    part_number: int | None = None
    module_number: int | None = None
    lesson_number: int | None = None

    @property
    def public_url(self) -> str:
        if self.kind == "course":
            return "/course/"
        if self.kind == "module":
            return f"/course/m{self.module_number}/"
        return f"/course/m{self.module_number}/{self.lesson_number}/"

    @property
    def destination(self) -> Path:
        if self.kind == "course":
            return WEB / "course" / "index.md"
        if self.kind == "module":
            return WEB / "course" / f"m{self.module_number}" / "index.md"
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

    @property
    def layout(self) -> str:
        return "landing" if self.kind in {"course", "module"} else "course"


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


def remove_context_navigation(text: str) -> str:
    """
    Remove repository-only NAV-CONTEXT content from the website copy.

    Website previous/next controls are inserted separately after each audience
    section and again after Research and Sources by the layout.
    """
    pattern = re.compile(
        r"\\?<!--\s*NAV-CONTEXT:START\s*-->.*?"
        r"<!--\s*NAV-CONTEXT:END\s*-->\s*",
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub("", text)


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


def insert_navigation_after_audience_blocks(text: str) -> tuple[str, int]:
    """
    Insert website previous/next controls after each of the three audience
    sections.

    The match is intentionally the complete four-link audience navigation
    block, not a bare *** or --- marker, so ordinary Markdown emphasis and
    unrelated horizontal rules are untouched.
    """
    pattern = re.compile(
        r"(?P<block>"
        r"\[For the Person With FND\]\(#for-the-person-with-fnd\)<br>[ \t]*\n"
        r"\[For Family, Friends, and Other Supporters\]"
        r"\(#for-family-friends-and-other-supporters\)<br>[ \t]*\n"
        r"\[For Clinicians and the Care Team\]"
        r"\(#for-clinicians-and-the-care-team\)<br>[ \t]*\n"
        r"\[Research and Sources\]\(#research-and-sources\)[ \t]*\n"
        r"(?:[ \t]*\n)*"
        r"[ \t]*---[ \t]*"
        r")",
        re.MULTILINE,
    )

    replacement = (
        r"\g<block>\n\n"
        "{% include page-navigation.html %}\n"
    )

    return pattern.subn(replacement, text)


def discover_course_pages() -> list[CoursePage]:
    """
    Find the course landing page, 23 module landing pages, and numbered lessons.

    The module README remains part of the public course sequence:
        /course/m1/       -> module README
        /course/m1/1/     -> first lesson
    """
    pages: list[CoursePage] = []

    course_readme = COURSE_ROOT / "README.md"
    if not course_readme.exists():
        raise ValueError("course/README.md is missing")

    pages.append(CoursePage(source=course_readme, kind="course"))

    for part_dir in sorted(COURSE_ROOT.iterdir()):
        if not part_dir.is_dir():
            continue

        part_match = PART_RE.match(part_dir.name)
        if not part_match:
            continue

        part_number = int(part_match.group(1))

        for module_dir in sorted(part_dir.iterdir()):
            if not module_dir.is_dir():
                continue

            module_match = MODULE_RE.match(module_dir.name)
            if not module_match:
                continue

            module_number = int(module_match.group(1))
            module_readme = module_dir / "README.md"

            if not module_readme.exists():
                raise ValueError(
                    f"Module landing page missing: "
                    f"{module_dir.relative_to(ROOT)}/README.md"
                )

            pages.append(
                CoursePage(
                    source=module_readme,
                    kind="module",
                    part_number=part_number,
                    module_number=module_number,
                )
            )

            for source in sorted(module_dir.glob("*.md")):
                lesson_match = LESSON_RE.match(source.name)
                if not lesson_match:
                    continue

                pages.append(
                    CoursePage(
                        source=source,
                        kind="lesson",
                        part_number=part_number,
                        module_number=module_number,
                        lesson_number=int(lesson_match.group(1)),
                    )
                )

    def sequence_key(page: CoursePage) -> tuple[int, int, int]:
        if page.kind == "course":
            return (0, 0, 0)
        if page.kind == "module":
            return (page.module_number or 0, 0, 0)
        return (page.module_number or 0, 1, page.lesson_number or 0)

    pages.sort(key=sequence_key)

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
    text = remove_context_navigation(text)
    text = remove_nav_blocks(text)
    text = normalize_audience_separators(text)
    text, _ = insert_navigation_after_audience_blocks(text)

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

    text = text.lstrip()
    parts = re.split(r"\n\s*\n", text, maxsplit=1)

    if len(parts) != 2:
        raise ValueError(
            f"Could not identify opening description in "
            f"{source.relative_to(ROOT)}"
        )

    description = " ".join(line.strip() for line in parts[0].splitlines()).strip()
    body = parts[1].lstrip()

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

    - Course/module Markdown -> its short website URL.
    - Published non-Markdown assets -> corresponding public asset path.
    - Other repository Markdown -> canonical GitHub source for now.
    - External URLs and same-page fragments -> unchanged.
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
    previous_page: CoursePage | None,
    previous_title: str | None,
    next_page: CoursePage | None,
    next_title: str | None,
) -> str:
    """
    Build Jekyll-only front matter for the generated copy.

    Structural and previous/next information lives directly on each generated
    page so navigation does not depend on matching page.path against a data
    lookup at render time.
    """
    lines = [
        "---",
        f"layout: {page.layout}",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description)}",
        f"status: {status}",
        f"authorship: {authorship}",
        f"page_kind: {page.kind}",
    ]

    if page.part_number is not None:
        lines.append(f"part_number: {page.part_number}")

    if page.module_number is not None:
        lines.extend(
            [
                f"module_number: {page.module_number}",
                f"module_url: "
                f"{yaml_string(f'/course/m{page.module_number}/')}",
            ]
        )

    if page.lesson_number is not None:
        lines.append(f"lesson_number: {page.lesson_number}")

    if last_reviewed:
        lines.append(f"last_reviewed: {yaml_string(last_reviewed)}")

    if previous_page is not None and previous_title is not None:
        lines.extend(
            [
                f"previous_page_url: {yaml_string(previous_page.public_url)}",
                f"previous_page_title: {yaml_string(previous_title)}",
            ]
        )

    if next_page is not None and next_title is not None:
        lines.extend(
            [
                f"next_page_url: {yaml_string(next_page.public_url)}",
                f"next_page_title: {yaml_string(next_title)}",
            ]
        )

    lines.extend(
        [
            f"permalink: {page.public_url}",
            "---",
            "",
        ]
    )

    return "\n".join(lines)


def write_generated_page_data(pages: list[CoursePage]) -> None:
    """Write structure and sequence data used by Jekyll layouts."""
    generated_dir = WEB / "_data" / "generated"
    generated_dir.mkdir(parents=True, exist_ok=True)

    page_lines: list[str] = []

    for page in pages:
        page_lines.extend(
            [
                f"{yaml_string(page.jekyll_path)}:",
                f"  kind: {page.kind}",
                f"  course_url: {yaml_string('/course/')}",
            ]
        )

        if page.part_number is not None:
            page_lines.append(f"  part_number: {page.part_number}")

        if page.module_number is not None:
            page_lines.extend(
                [
                    f"  module_number: {page.module_number}",
                    f"  module_url: "
                    f"{yaml_string(f'/course/m{page.module_number}/')}",
                ]
            )

        if page.lesson_number is not None:
            page_lines.append(f"  lesson_number: {page.lesson_number}")

    (generated_dir / "pages.yml").write_text(
        "\n".join(page_lines) + "\n",
        encoding="utf-8",
    )

    title_by_source = {
        page.source: extract_title(
            page.source.read_text(encoding="utf-8"),
            page.source,
        )
        for page in pages
    }

    nav_lines: list[str] = []

    for index, page in enumerate(pages):
        nav_lines.append(f"{yaml_string(page.jekyll_path)}:")

        if index > 0:
            previous = pages[index - 1]
            nav_lines.extend(
                [
                    "  previous:",
                    f"    title: {yaml_string(title_by_source[previous.source])}",
                    f"    url: {yaml_string(previous.public_url)}",
                ]
            )

        if index < len(pages) - 1:
            following = pages[index + 1]
            nav_lines.extend(
                [
                    "  next:",
                    f"    title: {yaml_string(title_by_source[following.source])}",
                    f"    url: {yaml_string(following.public_url)}",
                ]
            )

    (generated_dir / "navigation.yml").write_text(
        "\n".join(nav_lines) + "\n",
        encoding="utf-8",
    )


def prepare_course(pages: list[CoursePage]) -> None:
    page_url_map = {
        page.source.resolve(): page.public_url
        for page in pages
    }

    source_text_by_page = {
        page: page.source.read_text(encoding="utf-8")
        for page in pages
    }

    title_by_page = {
        page: extract_title(source_text_by_page[page], page.source)
        for page in pages
    }

    errors: list[str] = []

    for index, page in enumerate(pages):
        try:
            source_text = source_text_by_page[page]
            title = title_by_page[page]

            status, authorship = extract_status_and_authorship(
                source_text,
                page.source,
            )
            last_reviewed = extract_last_reviewed(source_text)

            body, description = strip_website_header_material(
                source_text,
                page.source,
            )

            if page.kind == "lesson":
                section_nav_count = body.count(
                    "{% include page-navigation.html %}"
                )
                if section_nav_count != 3:
                    raise ValueError(
                        "Expected three audience-section navigation points; "
                        f"found {section_nav_count}"
                    )

            body = rewrite_relative_links(
                body,
                page.source,
                page_url_map,
            )

            previous_page = pages[index - 1] if index > 0 else None
            next_page = pages[index + 1] if index < len(pages) - 1 else None

            page.destination.parent.mkdir(parents=True, exist_ok=True)
            page.destination.write_text(
                render_front_matter(
                    page=page,
                    title=title,
                    description=description,
                    status=status,
                    authorship=authorship,
                    last_reviewed=last_reviewed,
                    previous_page=previous_page,
                    previous_title=(
                        title_by_page[previous_page]
                        if previous_page is not None
                        else None
                    ),
                    next_page=next_page,
                    next_title=(
                        title_by_page[next_page]
                        if next_page is not None
                        else None
                    ),
                )
                + body,
                encoding="utf-8",
            )

        except Exception as exc:
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

    module_count = sum(page.kind == "module" for page in pages)
    lesson_count = sum(page.kind == "lesson" for page in pages)

    print("Prepared Jekyll website source.")
    print("  Course landing pages:       1")
    print(f"  Module landing pages:       {module_count}")
    print(f"  Course lessons:             {lesson_count}")
    print(f"  Total generated course:     {len(pages)}")
    print("  Module pattern:             /course/m{module}/")
    print("  Lesson pattern:             /course/m{module}/{lesson}/")
    print("  Canonical Markdown files:   unchanged")


if __name__ == "__main__":
    main()
