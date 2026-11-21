#!/usr/bin/env python3
"""Rebuild the internal Thought–Heart–Activity inventory from course lessons.

The public Person sections are authoritative. The inventory copies their actual
reflection/activity wording; it does not invent missing prompts, infer clinical
approval, or turn older "Questions" into modern Heart prompts.

Run from any working directory:
    python tools/course/build_thought_heart_activity_inventory.py
    python tools/course/build_thought_heart_activity_inventory.py --check

For PRs based on an older commit, generate from the merged/current checkout so
the inventory reflects approved lessons already merged into the base branch.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITEMAP = ROOT / "SITEMAP.md"
INVENTORY = ROOT / "reference/_internal/course/thought-heart-activity-inventory.md"
START_MARKER = "<!-- AUTO-INVENTORY:START -->"
END_MARKER = "<!-- AUTO-INVENTORY:END -->"

# Find numbered, focused lesson files in the same order as the course site map.
LESSON_LINK = re.compile(
    r"\]\((course/module-(\d{2})-[^/)]+/\d{2}-[^)]+\.md)\)"
)
SECTION_HEADING = re.compile(r"^### ([^\n]+)\s*$", re.MULTILINE)
PAGE_TITLE = re.compile(r"^# (.+)$", re.MULTILINE)


def lesson_paths() -> list[tuple[int, str]]:
    """Return each numbered lesson once, preserving reader-facing order."""
    sitemap = SITEMAP.read_text(encoding="utf-8")
    paths: list[tuple[int, str]] = []
    seen: set[str] = set()

    for match in LESSON_LINK.finditer(sitemap):
        path, module_number = match.group(1), int(match.group(2))
        if path not in seen:
            seen.add(path)
            paths.append((module_number, path))

    if not paths:
        raise ValueError("No numbered lesson paths were found in SITEMAP.md.")
    return paths


def person_section(page: str) -> str:
    """Keep only the Person audience, not later audiences or source lists."""
    start = page.find("## For the Person With FND")
    if start < 0:
        return ""

    end = page.find("## For Family, Friends, and Other Supporters", start)
    if end < 0:
        end = page.find("## For Clinicians and the Care Team", start)
    return page[start:end] if end >= 0 else page[start:]


def prompt_kind(title: str) -> str | None:
    """Preserve old question labels instead of assigning them a Heart meaning."""
    if title.startswith("Something to think about"):
        return "Thought"
    if title.startswith("How might that feel"):
        return "Heart"
    if title.startswith(("One small step", "One small thing you can do")):
        return "Activity"
    if title in {"Questions to reflect on", "Questions"}:
        return "Earlier questions"
    return None


def prompts_from_person(person: str) -> list[tuple[str, str, str]]:
    """Extract verbatim paragraphs below recognized third-level headings."""
    headings = list(SECTION_HEADING.finditer(person))
    prompts: list[tuple[str, str, str]] = []

    for index, heading in enumerate(headings):
        title = heading.group(1).strip()
        kind = prompt_kind(title)
        if kind is None:
            continue

        end = headings[index + 1].start() if index + 1 < len(headings) else len(person)
        value = person[heading.end():end].strip()

        # Remove navigation and section separators from the final prompt.
        value = re.sub(r"\n\*\*\*\s*[\s\S]*$", "", value)
        value = re.sub(r"\n---\s*[\s\S]*$", "", value)
        prompts.append((kind, title, value.strip()))
    return prompts


def render_inventory() -> str:
    """Render a complete, ordered snapshot from the checked-out course source."""
    pieces: list[str] = []
    previous_module: int | None = None

    for lesson_number, (module_number, path) in enumerate(lesson_paths(), start=1):
        file = ROOT / path
        if not file.is_file():
            raise FileNotFoundError(f"Missing lesson referenced by SITEMAP: {path}")

        source = file.read_text(encoding="utf-8")
        title_match = PAGE_TITLE.search(source)
        title = title_match.group(1) if title_match else file.name
        prompts = prompts_from_person(person_section(source))

        if module_number != previous_module:
            pieces.append(f"\n## Module {module_number}\n\n")
            previous_module = module_number

        source_label = f"[Source lesson](../../../{path}) · Module {module_number}"
        pieces.append(f"### Lesson {lesson_number} — {title}\n\n{source_label}\n\n")
        if not prompts:
            pieces.append("**No matching reflection/activity headings in this Person section.**\n\n")

        for kind, heading, value in prompts:
            pieces.append(
                f"**{kind}** (source heading: *{heading}*)\n\n"
                f"{value or '*Empty in source*'}\n\n"
            )

    return "".join(pieces)


def replace_generated_section(document: str, new_section: str) -> str:
    """Replace only the generated inventory; retain human-authored guidance."""
    if document.count(START_MARKER) != 1 or document.count(END_MARKER) != 1:
        raise ValueError("Expected one start and one end marker in the inventory.")

    start = document.index(START_MARKER) + len(START_MARKER)
    end = document.index(END_MARKER)
    if start > end:
        raise ValueError("Inventory markers are out of order.")
    return document[:start] + new_section + document[end:]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="Exit nonzero if the inventory differs from the course pages."
    )
    args = parser.parse_args()

    current = INVENTORY.read_text(encoding="utf-8")
    expected = replace_generated_section(current, render_inventory())
    if expected == current:
        print("Thought–Heart–Activity inventory is up to date.")
        return 0

    if args.check:
        diff = difflib.unified_diff(
            current.splitlines(), expected.splitlines(),
            fromfile="committed inventory", tofile="generated from lessons", lineterm=""
        )
        for index, line in enumerate(diff):
            if index >= 100:
                print("... additional differences omitted")
                break
            print(line)
        return 1

    INVENTORY.write_text(expected, encoding="utf-8")
    print(f"Updated {INVENTORY.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Inventory generation failed: {error}", file=sys.stderr)
        sys.exit(2)
