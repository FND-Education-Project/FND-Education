from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CTX_START = "<!-- NAV-CONTEXT:START -->"
CTX_END = "<!-- NAV-CONTEXT:END -->"

SOURCE_HEADINGS = re.compile(
    r"(?im)^##\s+(?:Research and Sources|Research and evidence|Sources|Evidence and Sources|Research Sources)\s*$"
)
CTX_BLOCK = re.compile(
    rf"\n?{re.escape(CTX_START)}.*?{re.escape(CTX_END)}\n?",
    re.S,
)

LEGACY_LINE_PATTERNS = [
    re.compile(r"(?m)^⬅️\s+\*\*(?:Previous page|Previous article):\*\*.*\n?"),
    re.compile(r"(?m)^➡️\s+\*\*(?:Next page|Next article):\*\*.*\n?"),
    re.compile(r"(?m)^\[Back to technique index\]\(technique-index\.md\)\s*·\s*\[Diagnostic-sign page\]\([^\n]+\)\s*\n?"),
    re.compile(r"(?m)^\*\*Related course page:\*\*\s*\[[^\]]+\]\([^\n]+\)\s*\n?"),
]


def rel(path: Path, target: str | Path) -> str:
    return Path(os.path.relpath(ROOT / Path(target), start=path.parent)).as_posix()


def link(path: Path, label: str, target: str | Path) -> str:
    return f"[{label}]({rel(path, target)})"


def cbt_context(path: Path) -> str:
    nav: list[str] = []
    if path.name != "README.md":
        is_guide = "content-creator-guide" in path.name
        peers = sorted(
            p for p in path.parent.glob("*.md")
            if p.name != "README.md" and (("content-creator-guide" in p.name) == is_guide)
        )
        if path in peers:
            idx = peers.index(path)
            if idx > 0:
                nav.append(link(path, "← Previous", peers[idx - 1].relative_to(ROOT)))
            if idx < len(peers) - 1:
                next_link = link(path, "Next →", peers[idx + 1].relative_to(ROOT))
            else:
                next_link = None
        else:
            next_link = None
    else:
        next_link = None

    nav.extend(
        [
            link(path, "Booklet collection", "reference/recovery-techniques/functional_seizures/unified_cbt_booklets/README.md"),
            link(path, "Functional-seizure recovery materials", "reference/recovery-techniques/functional_seizures/README.md"),
            link(path, "Functional-seizure recovery page", "reference/recovery-techniques/06-functional-seizures.md"),
        ]
    )
    if next_link:
        nav.append(next_link)

    global_nav = " · ".join(
        [
            link(path, "Home", "README.md"),
            link(path, "Course", "course/README.md"),
            link(path, "Reference Library", "reference/README.md"),
            link(path, "Site Map", "SITEMAP.md"),
        ]
    )
    return (
        f"{CTX_START}\n"
        f"**CBT materials:** {' · '.join(nav)}\n\n"
        f"**Navigate:** {global_nav}\n"
        f"{CTX_END}"
    )


def clean_legacy_navigation(text: str) -> str:
    for pattern in LEGACY_LINE_PATTERNS:
        text = pattern.sub("", text)
    text = re.sub(r"\n\*\*\*\n(?=<details>|<!-- NAV-CONTEXT:START -->)", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def fix_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = CTX_BLOCK.search(text)
    if not match:
        return

    context = match.group(0).strip()
    if "unified_cbt_booklets" in path.parts:
        context = cbt_context(path)

    text = CTX_BLOCK.sub("\n", text)
    text = clean_legacy_navigation(text).strip() + "\n"

    source_matches = list(SOURCE_HEADINGS.finditer(text))
    if source_matches:
        pos = source_matches[-1].start()
        before = text[:pos].rstrip()
        after = text[pos:].lstrip()
        text = before + "\n\n" + context + "\n\n" + after
    else:
        text = text.rstrip() + "\n\n" + context + "\n"

    path.write_text(text, encoding="utf-8")


def main() -> None:
    files = sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and ".github" not in p.parts
    )
    for path in files:
        fix_file(path)
    print(f"Checked contextual navigation placement in {len(files)} Markdown files.")


if __name__ == "__main__":
    main()
