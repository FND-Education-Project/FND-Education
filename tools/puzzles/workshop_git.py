"""Conservative GitHub draft-PR handoff for the local crossword workshop.

Only XLSX question banks saved in tools/puzzles are staged. Generated PDFs
remain downloads requiring separate editorial approval and publication.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=False
    )


def _warn(message: str) -> None:
    print(f"[Crossword Git handoff] {message}", flush=True)


def start_session(root: Path) -> str | None:
    """Make a dedicated branch only when main is clean and gh is installed."""
    if shutil.which("gh") is None or shutil.which("git") is None:
        _warn("GitHub CLI or Git is unavailable. Save and commit changes manually.")
        return None

    current = _git(root, "branch", "--show-current")
    if current.returncode != 0 or current.stdout.strip() != "main":
        _warn("Automatic PR requires starting the workshop on main; manual Git remains available.")
        return None

    changes = _git(root, "status", "--porcelain", "--untracked-files=all")
    if changes.returncode != 0 or changes.stdout.strip():
        _warn("Working tree already has changes. Finish or set them aside before starting an automatic PR session.")
        return None

    name = "crossword/session-" + datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    created = _git(root, "switch", "-c", name)
    if created.returncode != 0:
        _warn("Could not create a session branch: " + created.stderr.strip())
        return None
    _warn(f"Started isolated question-bank session on {name}.")
    _warn("Use 'Save edits to workbook in Codespaces' before leaving the workshop.")
    return name


def _saved_workbooks(root: Path) -> list[str]:
    """Return only existing, modified/untracked XLSX files directly in tools/puzzles."""
    result = _git(root, "status", "--porcelain", "-z", "--untracked-files=all", "--", "tools/puzzles")
    if result.returncode != 0:
        raise RuntimeError("Cannot read Git status: " + result.stderr.strip())

    found: list[str] = []
    for record in result.stdout.split("\x00"):
        if len(record) < 4 or record[:2].strip().startswith("D"):
            continue
        path = record[3:]
        candidate = Path(path)
        if (candidate.parent.as_posix() == "tools/puzzles"
                and candidate.suffix.lower() == ".xlsx"
                and (root / candidate).is_file()):
            found.append(path)
    return sorted(set(found))


def _return_to_main(root: Path, branch: str, delete_empty: bool = False) -> None:
    status = _git(root, "status", "--porcelain", "--untracked-files=all")
    if status.returncode or status.stdout.strip():
        _warn("Other local changes remain; staying on this branch to protect them.")
        return
    switched = _git(root, "switch", "main")
    if switched.returncode:
        _warn("PR saved, but could not switch back to main: " + switched.stderr.strip())
        return
    if delete_empty:
        _git(root, "branch", "-d", branch)
    _warn("Returned to main with a clean working tree.")


def finish_session(root: Path, branch: str | None) -> None:
    """Commit saved workbooks, open draft PR, leave other files untouched."""
    if not branch:
        return
    current = _git(root, "branch", "--show-current")
    if current.returncode or current.stdout.strip() != branch:
        _warn("Branch changed while workshop ran. Skipping automatic commit.")
        return
    try:
        workbooks = _saved_workbooks(root)
    except RuntimeError as exc:
        _warn(str(exc))
        return

    if not workbooks:
        _warn("No saved workbook changes; no commit or PR needed.")
        _return_to_main(root, branch, delete_empty=True)
        return

    staged_before = _git(root, "diff", "--cached", "--name-only", "-z")
    if staged_before.returncode or staged_before.stdout.strip():
        _warn("Existing staged changes found. Skipping automatic commit to avoid including unrelated work.")
        return

    added = _git(root, "add", "--", *workbooks)
    if added.returncode:
        _warn("Could not stage question banks: " + added.stderr.strip())
        return

    committed = _git(root, "commit", "-m", "Save crossword workshop question bank edits")
    if committed.returncode:
        _warn("Commit failed: " + committed.stderr.strip())
        return
    _warn("Committed only these saved question banks: " + ", ".join(workbooks))

    pushed = _git(root, "push", "-u", "origin", branch)
    if pushed.returncode:
        _warn("Saved locally, but push failed: " + pushed.stderr.strip())
        _warn(f"On {branch}, run: git push -u origin HEAD")
        return

    title = "Crossword workshop question bank — " + datetime.now().strftime("%Y-%m-%d")
    opened = subprocess.run(
        ["gh", "pr", "create", "--draft", "--base", "main", "--head", branch,
         "--title", title, "--body",
         "Saved Excel question-bank edits from the Codespaces crossword workshop. "
         "Review and merge manually. Finished puzzle PDFs are published separately."],
        cwd=root, text=True, capture_output=True, check=False,
    )
    if opened.returncode:
        _warn("Changes pushed, but opening the draft PR failed: " + opened.stderr.strip())
        _warn(f"Run: gh pr create --draft --base main --head {branch} --fill")
        return
    _warn("Draft PR ready to review: " + opened.stdout.strip())
    _return_to_main(root, branch)
