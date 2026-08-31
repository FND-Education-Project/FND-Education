from __future__ import annotations

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


def clean_legacy_navigation(text: str) -> str:
    for pattern in LEGACY_LINE_PATTERNS:
        text = pattern.sub("", text)
    # Remove an isolated horizontal rule left behind by deleted previous/next links
    text = re.sub(r"\n\*\*\*\n(?=<details>|<!-- NAV-CONTEXT:START -->)", "\n", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def fix_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    match = CTX_BLOCK.search(text)
    if not match:
        return

    context = match.group(0).strip()
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
