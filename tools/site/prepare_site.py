#!/usr/bin/env python3
"""
Prepare canonical repository content for the Jekyll website.

Canonical Markdown remains optimized for GitHub and is never edited here.
This script creates a generated website copy under web/, adds Jekyll front
matter, removes repository-only navigation, translates public links, and copies
approved public assets.

Publication is allowlist-based. In particular, reference/_internal/ is a
permanent repository-only area and is never published.
"""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape


ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"

COURSE_ROOT = ROOT / "course"
REFERENCE_ROOT = ROOT / "reference"
INTERNAL_REFERENCE_ROOT = REFERENCE_ROOT / "_internal"
GLOSSARY_SOURCE = ROOT / "glossary" / "README.md"
HUMAN_SITEMAP_SOURCE = ROOT / "SITEMAP.md"

GITHUB_BLOB_BASE = (
    "https://github.com/FND-Education-Project/FND-Education/blob/main/"
)

NAV_BLOCKS = ("BREADCRUMB",)

PART_RE = re.compile(r"^part-(\d+)-", re.IGNORECASE)
MODULE_RE = re.compile(r"^module-(\d+)-", re.IGNORECASE)
LESSON_RE = re.compile(r"^(\d+)-.+\.md$", re.IGNORECASE)
NUMBERED_MD_RE = re.compile(r"^(\d+)-(.+)\.md$", re.IGNORECASE)


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


@dataclass(frozen=True)
class ReferencePage:
    source: Path
    kind: str
    public_url: str
    section: str | None = None
    symptom_slug: str | None = None
    number: int | None = None

    @property
    def destination(self) -> Path:
        relative = self.public_url.strip("/")
        if not relative:
            raise ValueError("Reference public URL cannot be the site root")
        return WEB / relative / "index.md"

    @property
    def jekyll_path(self) -> str:
        return self.destination.relative_to(WEB).as_posix()

    @property
    def layout(self) -> str:
        if self.kind in {"diagnostic-technique", "recovery-technique"}:
            return "technique"
        return "reference"


def yaml_string(value: str) -> str:
    """Return a double-quoted YAML-safe scalar using JSON escaping."""
    return json.dumps(value, ensure_ascii=False)


def humanize_slug(slug: str) -> str:
    """Create a readable breadcrumb label from a stable URL slug."""
    special = {
        "fnd": "FND",
        "fcd": "FCD",
        "pppd": "PPPD",
    }
    return " ".join(
        special.get(word.lower(), word.capitalize())
        for word in slug.split("-")
    )


def remove_nav_blocks(text: str) -> str:
    """Remove repository-only breadcrumb blocks from the website copy."""
    for name in NAV_BLOCKS:
        pattern = re.compile(
            rf"\\?<!--\s*NAV-{name}:START\s*-->.*?"
            rf"<!--\s*NAV-{name}:END\s*-->\s*",
            re.IGNORECASE | re.DOTALL,
        )
        text = pattern.sub("", text)
    return text


def remove_plain_reference_breadcrumb(text: str) -> str:
    """
    Remove the older one-line breadcrumb form used on some Reference pages.

    It is intentionally limited to a line beginning with [Home] near the top
    and containing the Reference Library link.
    """
    top = text[:2500]
    match = re.search(
        r"^\[Home\]\([^)]+\).*?\[Reference Library\]\([^)]+\).*?$",
        top,
        re.MULTILINE,
    )
    if not match:
        return text
    return text[: match.start()] + text[match.end() :].lstrip("\n")


def remove_context_navigation(text: str) -> str:
    """Remove repository-only NAV-CONTEXT blocks from the website copy."""
    pattern = re.compile(
        r"\\?<!--\s*NAV-CONTEXT:START\s*-->.*?"
        r"<!--\s*NAV-CONTEXT:END\s*-->\s*",
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub("", text)


def normalize_generated_horizontal_rules(text: str) -> str:
    """
    Normalize standalone thematic breaks in the generated website copy.

    A line containing only *** is Markdown's horizontal-rule syntax, not
    strong/italic text. Converting that exact standalone form to --- avoids
    Kramdown edge cases after <br>-based navigation menus. Adjacent thematic
    rules are then collapsed so audience menus never render double rules.
    Inline *** emphasis is untouched.
    """
    text = re.sub(
        r"^[ \t]*\*\*\*[ \t]*$",
        "---",
        text,
        flags=re.MULTILINE,
    )

    return re.sub(
        r"^[ \t]*---[ \t]*\n(?:[ \t]*\n)*^[ \t]*---[ \t]*$",
        "---",
        text,
        flags=re.MULTILINE,
    )


def format_inline_citations(text: str) -> str:
    """
    Turn compact (*citations* [1]...) markers into accessible citation chips.

    The numbered links keep their original anchors while CSS makes them smaller
    than body text, visually distinct, and easy to click or tap.
    """
    cluster = re.compile(
        r"\(\*citations?\*\s*"
        r"(?P<links>"
        r"(?:\[\d+\]\(#[^)]+\)(?:,\s*)?)+"
        r")\)",
        re.IGNORECASE,
    )
    link = re.compile(r"\[(?P<number>\d+)\]\((?P<href>#[^)]+)\)")

    def replace(match: re.Match[str]) -> str:
        links = []
        for item in link.finditer(match.group("links")):
            number = item.group("number")
            href = item.group("href")
            links.append(
                f'<a href="{href}" aria-label="Citation {number}">'
                f'[{number}]</a>'
            )

        if not links:
            return match.group(0)

        return (
            '<span class="inline-citations" aria-label="Citations">'
            + "".join(links)
            + "</span>"
        )

    return cluster.sub(replace, text)


def insert_recovery_diagnosis_link(
    text: str,
    page: "ReferencePage",
) -> str:
    """
    Add a non-bulleted diagnosis cross-link at the top of Refers to on each
    symptom recovery landing page. Canonical Markdown remains unchanged.
    """
    if page.kind != "recovery-overview" or not page.symptom_slug:
        return text

    diagnosis_url = (
        f"/reference/{page.symptom_slug}/diagnosis/"
    )
    sentence = (
        "For a fuller description of this symptom and the diagnostic "
        "techniques used to assess it, see "
        f"[Understanding & Diagnosis]({relative_url_liquid(diagnosis_url)})."
    )

    standalone = re.compile(
        r"(?P<label>^\*\*Refers to:\*\*[ \t]*$)",
        re.MULTILINE,
    )

    updated, count = standalone.subn(
        lambda match: match.group("label") + "\n\n" + sentence,
        text,
        count=1,
    )

    if count == 1:
        return updated

    inline = re.compile(
        r"^\*\*Refers to:\*\*[ \t]+(?P<description>.+?)\s*$",
        re.MULTILINE,
    )

    updated, count = inline.subn(
        lambda match: (
            "**Refers to:**\n\n"
            + sentence
            + "\n\n"
            + match.group("description").strip()
        ),
        text,
        count=1,
    )

    if count != 1:
        raise ValueError(
            "Recovery overview is missing the expected **Refers to:** label: "
            f"{page.source.relative_to(ROOT)}"
        )

    return updated


def insert_navigation_after_audience_sections(text: str) -> tuple[str, int]:
    """
    Insert previous/next controls after Person, Supporter and Clinician sections.

    The complete four-link audience block is the insertion marker. A block
    before the Person section is introductory navigation and is skipped. A
    block after Research and Sources is also skipped because the layout supplies
    the final previous/next control after the article.
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

    person_pos = text.find("## For the Person With FND")
    research_pos = text.find("## Research and Sources")

    matches = list(pattern.finditer(text))
    eligible = [
        match
        for match in matches
        if person_pos >= 0
        and match.start() > person_pos
        and (research_pos < 0 or match.start() < research_pos)
    ]

    for match in reversed(eligible):
        replacement = (
            match.group("block")
            + "\n\n{% include page-navigation.html %}\n"
        )
        text = text[: match.start()] + replacement + text[match.end() :]

    return text, len(eligible)


def extract_title(text: str, source: Path) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"No level-1 title found in {source.relative_to(ROOT)}")
    return match.group(1).strip()


def extract_course_status_and_authorship(
    text: str,
    source: Path,
) -> tuple[str, str]:
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


def extract_reference_editorial_status(
    text: str,
) -> tuple[str | None, str | None, str]:
    """
    Extract only obvious editorial draft/status blockquotes near the page top.

    Clinical explanatory blockquotes elsewhere are preserved.
    """
    for match in re.finditer(r"^>\s*(.+?)\s*$", text, re.MULTILINE):
        if match.start() > 3500:
            break

        wording = match.group(1).lower()
        editorial = any(
            phrase in wording
            for phrase in (
                "working draft",
                "draft in progress",
                "working inventory",
                "automatically generated expansion",
            )
        )
        if not editorial:
            continue

        if "human draft" in wording or "human authored" in wording:
            authorship = "human"
        elif "automatically generated" in wording:
            authorship = "automatically-generated"
        else:
            authorship = None

        cleaned = text[: match.start()] + text[match.end() :]
        return "working-draft", authorship, cleaned

    return None, None, text


def extract_last_reviewed(text: str) -> str | None:
    match = re.search(
        r"^\*Last reviewed:\s*(.+?)\*\s*$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def extract_reference_description(text: str) -> tuple[str, str | None]:
    """
    Move one suitable introductory prose paragraph into page.description.

    Structured labels, lists, navigation blocks and headings stay in the body.
    """
    h2_pos = text.find("\n## ")
    search_area = text if h2_pos < 0 else text[:h2_pos]

    offset = 0
    for block in re.split(r"(\n\s*\n)", search_area):
        block_start = offset
        offset += len(block)

        stripped = block.strip()
        if not stripped or re.fullmatch(r"\n\s*\n", block):
            continue

        first = stripped[0]
        if (
            first in "#>*-|<"
            or first.isdigit()
            or stripped.startswith("[")
            or stripped.startswith("**")
            or "<br>" in stripped
            or "{%" in stripped
        ):
            continue

        description = " ".join(
            line.strip()
            for line in stripped.splitlines()
        ).strip()

        if not description:
            continue

        before = text[:block_start]
        after = text[block_start + len(block):]
        cleaned = (before + after).lstrip("\n")
        return cleaned, description

    return text, None


def discover_course_pages() -> list[CoursePage]:
    """Find the course landing page, module intros and numbered lessons."""
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


def numbered_slug(source: Path) -> tuple[int, str]:
    match = NUMBERED_MD_RE.match(source.name)
    if not match:
        raise ValueError(
            f"Expected numbered Markdown filename: {source.relative_to(ROOT)}"
        )
    return int(match.group(1)), match.group(2)


def discover_reference_pages() -> list[ReferencePage]:
    """
    Discover only explicitly supported reader-facing Reference page patterns.

    reference/_internal/ is never traversed. Any unexpected Markdown elsewhere
    under reference/ fails the build so new publication types are deliberate.
    """
    pages: list[ReferencePage] = []
    unknown: list[Path] = []

    for source in sorted(REFERENCE_ROOT.rglob("*.md")):
        if INTERNAL_REFERENCE_ROOT in source.parents:
            continue

        rel = source.relative_to(REFERENCE_ROOT)
        parts = rel.parts

        page: ReferencePage | None = None

        if rel.as_posix() == "README.md":
            page = ReferencePage(
                source=source,
                kind="reference-home",
                public_url="/reference/",
                section="reference",
            )

        elif rel.as_posix() == "reference-index.md":
            page = ReferencePage(
                source=source,
                kind="reference-index",
                public_url="/reference/index/",
                section="reference",
            )

        elif rel.as_posix() == "functional-cognitive-disorder.md":
            page = ReferencePage(
                source=source,
                kind="reference-topic",
                public_url="/reference/functional-cognitive-disorder/",
                section="reference",
                symptom_slug="functional-cognitive-disorder",
            )

        elif parts[0] == "co-occurring-conditions":
            if len(parts) == 2 and parts[1] == "README.md":
                page = ReferencePage(
                    source=source,
                    kind="co-occurring-home",
                    public_url="/reference/co-occurring/",
                    section="co-occurring",
                )
            elif len(parts) == 2:
                number, slug = numbered_slug(source)
                page = ReferencePage(
                    source=source,
                    kind="co-occurring-condition",
                    public_url=f"/reference/co-occurring/{slug}/",
                    section="co-occurring",
                    symptom_slug=slug,
                    number=number,
                )

        elif parts[0] == "diagnostic-concepts":
            if len(parts) == 2 and parts[1] == "README.md":
                page = ReferencePage(
                    source=source,
                    kind="diagnostic-concepts-home",
                    public_url="/reference/diagnosis/concepts/",
                    section="diagnosis",
                )
            elif len(parts) == 2:
                number, _slug = numbered_slug(source)
                page = ReferencePage(
                    source=source,
                    kind="diagnostic-concept",
                    public_url=f"/reference/diagnosis/concepts/{number}/",
                    section="diagnosis",
                    number=number,
                )

        elif parts[0] == "diagnostic-signs":
            if len(parts) == 2 and parts[1] == "README.md":
                page = ReferencePage(
                    source=source,
                    kind="diagnostic-home",
                    public_url="/reference/diagnosis/",
                    section="diagnosis",
                )
            elif len(parts) == 2 and parts[1] == "diagnostic-index.md":
                page = ReferencePage(
                    source=source,
                    kind="diagnostic-index",
                    public_url="/reference/diagnosis/index/",
                    section="diagnosis",
                )
            elif len(parts) == 2:
                number, slug = numbered_slug(source)
                page = ReferencePage(
                    source=source,
                    kind="diagnostic-overview",
                    public_url=f"/reference/{slug}/diagnosis/",
                    section="diagnosis",
                    symptom_slug=slug,
                    number=number,
                )
            elif len(parts) == 3:
                slug = parts[1].replace("_", "-")
                if parts[2] == "README.md":
                    page = ReferencePage(
                        source=source,
                        kind="diagnostic-techniques-home",
                        public_url=(
                            f"/reference/{slug}/diagnosis/techniques/"
                        ),
                        section="diagnosis",
                        symptom_slug=slug,
                    )
                elif parts[2] == "technique-inventory.md":
                    page = ReferencePage(
                        source=source,
                        kind="diagnostic-inventory",
                        public_url=(
                            f"/reference/{slug}/diagnosis/inventory/"
                        ),
                        section="diagnosis",
                        symptom_slug=slug,
                    )
                else:
                    number, _technique_slug = numbered_slug(source)
                    page = ReferencePage(
                        source=source,
                        kind="diagnostic-technique",
                        public_url=(
                            f"/reference/{slug}/diagnosis/{number}/"
                        ),
                        section="diagnosis",
                        symptom_slug=slug,
                        number=number,
                    )

        elif parts[0] == "recovery-techniques":
            if len(parts) == 2 and parts[1] == "README.md":
                page = ReferencePage(
                    source=source,
                    kind="recovery-home",
                    public_url="/reference/recovery/",
                    section="recovery",
                )
            elif len(parts) == 2 and parts[1] == "collection-guide.md":
                page = ReferencePage(
                    source=source,
                    kind="recovery-guide",
                    public_url="/reference/recovery/guide/",
                    section="recovery",
                )
            elif len(parts) == 2 and parts[1] == "technique-index.md":
                page = ReferencePage(
                    source=source,
                    kind="recovery-index",
                    public_url="/reference/recovery/index/",
                    section="recovery",
                )
            elif len(parts) == 2:
                number, slug = numbered_slug(source)
                page = ReferencePage(
                    source=source,
                    kind="recovery-overview",
                    public_url=f"/reference/{slug}/recovery/",
                    section="recovery",
                    symptom_slug=slug,
                    number=number,
                )
            elif len(parts) == 3:
                slug = parts[1].replace("_", "-")
                if parts[2] == "README.md":
                    page = ReferencePage(
                        source=source,
                        kind="recovery-techniques-home",
                        public_url=(
                            f"/reference/{slug}/recovery/techniques/"
                        ),
                        section="recovery",
                        symptom_slug=slug,
                    )
                else:
                    number, _technique_slug = numbered_slug(source)
                    page = ReferencePage(
                        source=source,
                        kind="recovery-technique",
                        public_url=(
                            f"/reference/{slug}/recovery/{number}/"
                        ),
                        section="recovery",
                        symptom_slug=slug,
                        number=number,
                    )

        if page is None:
            unknown.append(source)
        else:
            pages.append(page)

    if unknown:
        formatted = "\n  - ".join(
            str(path.relative_to(ROOT))
            for path in unknown
        )
        raise ValueError(
            "Unclassified public Reference Markdown. Either add an explicit "
            "public route or move repository-only material under "
            f"reference/_internal/:\n  - {formatted}"
        )

    seen: dict[str, Path] = {}
    for page in pages:
        if page.public_url in seen:
            raise ValueError(
                "Duplicate public Reference URL "
                f"{page.public_url}: {seen[page.public_url]} and {page.source}"
            )
        seen[page.public_url] = page.source

    return pages


def clean_generated_area(name: str) -> None:
    """Erase one known generated web tree, preserving its .gitkeep."""
    area = WEB / name
    area.mkdir(parents=True, exist_ok=True)

    for child in area.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def copy_public_asset_trees() -> None:
    """
    Copy explicitly approved shared assets.

    Site-owned CSS, JavaScript and icons already live under web/assets and are
    not touched.
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


def is_internal_reference_path(path: Path) -> bool:
    """Return True when a repository path is under reference/_internal/."""
    try:
        path.resolve().relative_to(INTERNAL_REFERENCE_ROOT.resolve())
        return True
    except ValueError:
        return False


def rewrite_relative_links(
    markdown: str,
    source_file: Path,
    page_url_map: dict[Path, str],
) -> str:
    """
    Translate links in the generated website copy.

    - Published Markdown -> its website URL.
    - Internal Reference working material -> plain link text, never published.
    - Approved non-Markdown assets -> corresponding public asset path.
    - Other repository Markdown -> canonical GitHub source for now.
    - External URLs and same-page fragments -> unchanged.
    """
    pattern = re.compile(
        r"(?P<image>!)?"
        r"\[(?P<label>[^\]]*)\]"
        r"\((?P<target>[^)\s]+)\)"
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

        if is_internal_reference_path(resolved):
            if match.group("image"):
                return ""
            return match.group("label")

        mapped_url = page_url_map.get(resolved)

        if mapped_url:
            public_path = mapped_url
            if separator:
                public_path += "#" + fragment
            return (
                f"{'!' if match.group('image') else ''}"
                f"[{match.group('label')}]"
                f"({relative_url_liquid(public_path)})"
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
                f"{'!' if match.group('image') else ''}"
                f"[{match.group('label')}]"
                f"({github_url})"
            )

        copy_referenced_asset(resolved)

        public_path = "/" + relative.as_posix()
        if separator:
            public_path += "#" + fragment

        return (
            f"{'!' if match.group('image') else ''}"
            f"[{match.group('label')}]"
            f"({relative_url_liquid(public_path)})"
        )

    return pattern.sub(replace, markdown)


def strip_course_header_material(
    text: str,
    source: Path,
) -> tuple[str, str]:
    """Transform one course source page into its generated website body."""
    text = remove_context_navigation(text)
    text = remove_nav_blocks(text)
    text = normalize_generated_horizontal_rules(text)
    text, _ = insert_navigation_after_audience_sections(text)

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

    description = " ".join(
        line.strip()
        for line in parts[0].splitlines()
    ).strip()
    body = parts[1].lstrip()

    body = re.sub(
        r"^\*Last reviewed:\s*.+?\*\s*$",
        "",
        body,
        flags=re.MULTILINE | re.IGNORECASE,
    )

    return body.strip() + "\n", description


def strip_reference_header_material(
    text: str,
    source: Path,
) -> tuple[
    str,
    str | None,
    str | None,
    str | None,
]:
    """Transform one reader-facing Reference source page."""
    text = remove_context_navigation(text)
    text = remove_nav_blocks(text)
    text = remove_plain_reference_breadcrumb(text)
    text = normalize_generated_horizontal_rules(text)
    text, _ = insert_navigation_after_audience_sections(text)

    text, count = re.subn(
        r"^#\s+.+?\s*$",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(
            f"Expected one H1 in {source.relative_to(ROOT)}"
        )

    status, authorship, text = extract_reference_editorial_status(text)
    text = text.lstrip()

    text, description = extract_reference_description(text)

    return (
        text.strip() + "\n",
        description,
        status,
        authorship,
    )


def render_course_front_matter(
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
    """Build Jekyll-only front matter for a generated course page."""
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


def reference_context_label(page: ReferencePage) -> str:
    labels = {
        "reference-home": "REFERENCE LIBRARY",
        "reference-index": "REFERENCE LIBRARY",
        "reference-topic": "REFERENCE LIBRARY",
        "diagnostic-home": "REFERENCE · DIAGNOSIS",
        "diagnostic-index": "REFERENCE · DIAGNOSIS",
        "diagnostic-overview": "REFERENCE · DIAGNOSIS",
        "diagnostic-concepts-home": "REFERENCE · UNDERSTANDING DIAGNOSIS",
        "diagnostic-concept": "REFERENCE · UNDERSTANDING DIAGNOSIS",
        "diagnostic-techniques-home": "REFERENCE · DIAGNOSTIC TECHNIQUES",
        "diagnostic-inventory": "REFERENCE · DIAGNOSTIC TECHNIQUES",
        "diagnostic-technique": "REFERENCE · DIAGNOSTIC TECHNIQUE",
        "recovery-home": "REFERENCE · RECOVERY",
        "recovery-guide": "REFERENCE · RECOVERY",
        "recovery-index": "REFERENCE · RECOVERY",
        "recovery-overview": "REFERENCE · RECOVERY",
        "recovery-techniques-home": "REFERENCE · RECOVERY TECHNIQUES",
        "recovery-technique": "REFERENCE · RECOVERY TECHNIQUE",
        "co-occurring-home": "REFERENCE · CO-OCCURRING CONDITIONS",
        "co-occurring-condition": "REFERENCE · CO-OCCURRING CONDITION",
    }
    return labels.get(page.kind, "REFERENCE LIBRARY")


def render_reference_front_matter(
    page: ReferencePage,
    title: str,
    description: str | None,
    status: str | None,
    authorship: str | None,
    previous_page: ReferencePage | None,
    previous_title: str | None,
    next_page: ReferencePage | None,
    next_title: str | None,
) -> str:
    """Build Jekyll-only front matter for a generated Reference page."""
    lines = [
        "---",
        f"layout: {page.layout}",
        f"title: {yaml_string(title)}",
        f"page_kind: {page.kind}",
        f"page_context_label: {yaml_string(reference_context_label(page))}",
        f"permalink: {page.public_url}",
    ]

    if description:
        lines.append(f"description: {yaml_string(description)}")

    if status:
        lines.append(f"status: {status}")

    if authorship:
        lines.append(f"authorship: {authorship}")

    if page.section:
        lines.append(f"reference_section: {page.section}")

    if page.symptom_slug:
        lines.extend(
            [
                f"symptom_slug: {yaml_string(page.symptom_slug)}",
                f"symptom_label: "
                f"{yaml_string(humanize_slug(page.symptom_slug))}",
            ]
        )

    if page.number is not None:
        lines.append(f"reference_number: {page.number}")

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

    lines.extend(["---", ""])
    return "\n".join(lines)


def extract_continue_target(source_text: str, source: Path) -> Path | None:
    """Resolve the authored NAV-CONTEXT Continue link, when it is public."""
    block = re.search(
        r"\\?<!--\s*NAV-CONTEXT:START\s*-->(.*?)"
        r"<!--\s*NAV-CONTEXT:END\s*-->",
        source_text,
        re.IGNORECASE | re.DOTALL,
    )
    if not block:
        return None

    match = re.search(
        r"\*\*Continue:\*\*\s*\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)",
        block.group(1),
        re.IGNORECASE,
    )
    if not match:
        return None

    target = match.group(1).strip()
    if (
        target.startswith("/")
        or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target)
    ):
        return None

    resolved = (source.parent / target).resolve()
    return resolved if resolved.exists() else None


def prepare_course(
    pages: list[CoursePage],
    page_url_map: dict[Path, str],
) -> None:
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

            status, authorship = extract_course_status_and_authorship(
                source_text,
                page.source,
            )
            last_reviewed = extract_last_reviewed(source_text)

            body, description = strip_course_header_material(
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
            body = format_inline_citations(body)

            previous_page = pages[index - 1] if index > 0 else None
            next_page = pages[index + 1] if index < len(pages) - 1 else None

            page.destination.parent.mkdir(parents=True, exist_ok=True)
            page.destination.write_text(
                render_course_front_matter(
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


def build_reference_navigation(
    pages: list[ReferencePage],
    source_text_by_page: dict[ReferencePage, str],
) -> tuple[
    dict[ReferencePage, ReferencePage | None],
    dict[ReferencePage, ReferencePage | None],
]:
    """
    Use authored NAV-CONTEXT Continue links as the Reference reading sequence.

    Previous links are inferred only when exactly one public page points to the
    current page, avoiding invented navigation when several paths converge.
    """
    by_source = {
        page.source.resolve(): page
        for page in pages
    }

    next_by_page: dict[ReferencePage, ReferencePage | None] = {}
    incoming: dict[ReferencePage, list[ReferencePage]] = {
        page: []
        for page in pages
    }

    for page in pages:
        target = extract_continue_target(
            source_text_by_page[page],
            page.source,
        )
        next_page = by_source.get(target) if target else None
        next_by_page[page] = next_page
        if next_page is not None:
            incoming[next_page].append(page)

    previous_by_page: dict[ReferencePage, ReferencePage | None] = {}
    for page in pages:
        candidates = incoming[page]
        previous_by_page[page] = (
            candidates[0]
            if len(candidates) == 1
            else None
        )

    return previous_by_page, next_by_page


def prepare_reference(
    pages: list[ReferencePage],
    page_url_map: dict[Path, str],
) -> None:
    source_text_by_page = {
        page: page.source.read_text(encoding="utf-8")
        for page in pages
    }

    title_by_page = {
        page: extract_title(source_text_by_page[page], page.source)
        for page in pages
    }

    previous_by_page, next_by_page = build_reference_navigation(
        pages,
        source_text_by_page,
    )

    errors: list[str] = []

    for page in pages:
        try:
            source_text = source_text_by_page[page]
            title = title_by_page[page]

            (
                body,
                description,
                status,
                authorship,
            ) = strip_reference_header_material(
                source_text,
                page.source,
            )

            body = insert_recovery_diagnosis_link(
                body,
                page,
            )
            body = rewrite_relative_links(
                body,
                page.source,
                page_url_map,
            )
            body = format_inline_citations(body)

            previous_page = previous_by_page[page]
            next_page = next_by_page[page]

            page.destination.parent.mkdir(parents=True, exist_ok=True)
            page.destination.write_text(
                render_reference_front_matter(
                    page=page,
                    title=title,
                    description=description,
                    status=status,
                    authorship=authorship,
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
            "Reference preparation stopped because some pages did not match "
            f"the expected source pattern:\n  - {joined}"
        )


def strip_resource_header(text: str, source: Path) -> str:
    """Remove repository-only header/navigation from a simple public resource."""
    text = remove_context_navigation(text)
    text = remove_nav_blocks(text)
    text = normalize_generated_horizontal_rules(text)

    text, count = re.subn(
        r"^#\s+.+?\s*$",
        "",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError(
            f"Expected one H1 in {source.relative_to(ROOT)}"
        )

    return text.lstrip()


def render_resource_front_matter(
    title: str,
    description: str,
    context_label: str,
    public_url: str,
) -> str:
    """Build front matter for glossary and human-readable sitemap pages."""
    lines = [
        "---",
        "layout: resource",
        f"title: {yaml_string(title)}",
        f"description: {yaml_string(description)}",
        f"page_context_label: {yaml_string(context_label)}",
        f"permalink: {public_url}",
        "---",
        "",
    ]
    return "\n".join(lines)


def prepare_resource_page(
    source: Path,
    destination: Path,
    public_url: str,
    title: str,
    description: str,
    context_label: str,
    page_url_map: dict[Path, str],
) -> None:
    """Generate one simple reader-facing resource from canonical Markdown."""
    if not source.exists():
        raise ValueError(f"Missing resource source: {source.relative_to(ROOT)}")

    text = source.read_text(encoding="utf-8")
    body = strip_resource_header(text, source)
    body = rewrite_relative_links(body, source, page_url_map)
    body = format_inline_citations(body)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        render_resource_front_matter(
            title=title,
            description=description,
            context_label=context_label,
            public_url=public_url,
        )
        + body.strip()
        + "\n",
        encoding="utf-8",
    )


def read_config_scalar(name: str) -> str:
    """Read one simple scalar from web/_config.yml without adding YAML deps."""
    config = (WEB / "_config.yml").read_text(encoding="utf-8")
    match = re.search(
        rf"^{re.escape(name)}:\s*(.*?)\s*$",
        config,
        re.MULTILINE,
    )
    if not match:
        raise ValueError(f"Missing {name} in web/_config.yml")

    value = match.group(1).strip()
    if (
        len(value) >= 2
        and value[0] == value[-1]
        and value[0] in {"'", '"'}
    ):
        value = value[1:-1]

    return value


def public_origin_with_base() -> str:
    """Return configured public origin including the current Pages base path."""
    origin = read_config_scalar("url").rstrip("/")
    baseurl = read_config_scalar("baseurl").strip()

    if baseurl and not baseurl.startswith("/"):
        baseurl = "/" + baseurl

    return origin + baseurl.rstrip("/")


def write_machine_sitemap(public_urls: list[str]) -> None:
    """Generate the search-engine sitemap from the final public route map."""
    origin = public_origin_with_base()
    routes = sorted(set(public_urls))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for route in routes:
        if not route.startswith("/"):
            raise ValueError(f"Public URL must start with '/': {route}")

        if route == "/":
            absolute = origin + "/"
        else:
            absolute = origin + route

        lines.extend(
            [
                "  <url>",
                f"    <loc>{xml_escape(absolute)}</loc>",
                "  </url>",
            ]
        )

    lines.append("</urlset>")
    (WEB / "sitemap.xml").write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )

    (WEB / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {origin}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_generated_page_data(pages: list[CoursePage]) -> None:
    """
    Keep the small generated course data files for compatibility.

    Current layouts read structural navigation directly from generated page
    front matter; these files remain rebuildable and may support future indexes.
    """
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

    (generated_dir / "navigation.yml").write_text(
        "{}\n",
        encoding="utf-8",
    )


def main() -> None:
    course_pages = discover_course_pages()
    reference_pages = discover_reference_pages()

    clean_generated_area("course")
    clean_generated_area("reference")
    clean_generated_area("glossary")
    clean_generated_area("sitemap")
    copy_public_asset_trees()

    page_url_map = {
        page.source.resolve(): page.public_url
        for page in course_pages
    }
    page_url_map.update(
        {
            page.source.resolve(): page.public_url
            for page in reference_pages
        }
    )
    page_url_map[(ROOT / "README.md").resolve()] = "/"
    page_url_map[GLOSSARY_SOURCE.resolve()] = "/glossary/"
    page_url_map[HUMAN_SITEMAP_SOURCE.resolve()] = "/sitemap/"

    prepare_course(course_pages, page_url_map)
    prepare_reference(reference_pages, page_url_map)

    prepare_resource_page(
        source=GLOSSARY_SOURCE,
        destination=WEB / "glossary" / "index.md",
        public_url="/glossary/",
        title="FND Terminology Glossary",
        description=(
            "Plain-language explanations of terms used in FND research, "
            "clinical care, rehabilitation, and this project."
        ),
        context_label="GLOSSARY",
        page_url_map=page_url_map,
    )

    prepare_resource_page(
        source=HUMAN_SITEMAP_SOURCE,
        destination=WEB / "sitemap" / "index.md",
        public_url="/sitemap/",
        title="FND Education Site Map",
        description=(
            "Browse the current course, Reference Library, glossary, "
            "research links, and project documentation."
        ),
        context_label="SITE MAP",
        page_url_map=page_url_map,
    )

    public_urls = [
        "/",
        "/contact/",
        "/glossary/",
        "/sitemap/",
        *[page.public_url for page in course_pages],
        *[page.public_url for page in reference_pages],
    ]
    write_machine_sitemap(public_urls)
    write_generated_page_data(course_pages)

    module_count = sum(
        page.kind == "module"
        for page in course_pages
    )
    lesson_count = sum(
        page.kind == "lesson"
        for page in course_pages
    )
    internal_count = (
        len(list(INTERNAL_REFERENCE_ROOT.rglob("*.md")))
        if INTERNAL_REFERENCE_ROOT.exists()
        else 0
    )

    print("Prepared Jekyll website source.")
    print("  Course landing pages:       1")
    print(f"  Module landing pages:       {module_count}")
    print(f"  Course lessons:             {lesson_count}")
    print(f"  Total generated course:     {len(course_pages)}")
    print(f"  Public Reference pages:     {len(reference_pages)}")
    print("  Glossary pages:             1")
    print("  Human sitemap pages:        1")
    print(f"  Internal Reference ignored: {internal_count}")
    print(f"  Total public routes:        {len(set(public_urls))}")
    print("  Module pattern:             /course/m{module}/")
    print("  Lesson pattern:             /course/m{module}/{lesson}/")
    print("  Reference root:             /reference/")
    print("  Canonical Markdown files:   unchanged")


if __name__ == "__main__":
    main()
