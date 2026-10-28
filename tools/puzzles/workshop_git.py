"""Conservative GitHub draft-PR handoff for the local crossword workshop.

Only XLSX question banks saved in tools/puzzles are staged. Generated PDFs
remain downloads requiring separate editorial approval and publication.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
import shutil
import subprocess
import sys


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True, check=False
    )


def _warn(message: str) -> None:
    print(f"[Crossword Git handoff] {message}", flush=True)



def prepare_startup(root: Path) -> bool:
    """Refresh clean main only after proving saved sessions are incorporated.

    Fail closed: never stash, reset, delete branches, merge a PR, or launch an
    older workbook after a failed check. Return whether HEAD changed so the
    launcher can restart with any newly downloaded Python code.
    """
    def run(*args: str) -> str:
        """Bound network waits and keep commands out of the shell."""
        result = subprocess.run(
            list(args), cwd=root, text=True, capture_output=True, check=False,
            timeout=45,
        )
        if result.returncode:
            raise RuntimeError(
                f"{args[0]} {args[1]} failed. Check connectivity/authentication "
                "and retry; your local work has been preserved."
            )
        return result.stdout.strip()

    def prs(*args: str) -> list[dict]:
        """Ask GitHub directly; cached remote refs cannot establish PR state."""
        result = json.loads(run(
            "gh", "pr", "list", "--base", "main", *args, "--limit", "1000",
            "--json", "state,headRefName,headRefOid,url",
        ))
        if not isinstance(result, list) or len(result) >= 1000:
            raise RuntimeError("Could not fully verify workshop PRs. Review them on GitHub.")
        return result

    try:
        if not shutil.which("git") or not shutil.which("gh"):
            raise RuntimeError("Git and GitHub CLI (gh) are required for safe startup.")
        before = run("git", "rev-parse", "HEAD")
        current = run("git", "branch", "--show-current")
        if current.startswith("crossword/session-"):
            recover_session(root, current)
        if run("git", "status", "--porcelain", "--untracked-files=all"):
            raise RuntimeError(
                "Uncommitted files need attention. Save/commit them on their "
                "existing branch before retrying. No files were changed."
            )
        current = run("git", "branch", "--show-current")
        if current != "main" and not current.startswith("crossword/session-"):
            raise RuntimeError(
                "Start on main or a crossword/session branch. "
                "Your current branch has been left untouched."
            )
        _warn("Checking GitHub for the latest workbook and unfinished sessions…")
        run("git", "fetch", "origin")
        # Check remote open sessions even when this checkout is already on main.
        for pr in prs("--state", "open"):
            if pr["headRefName"].startswith("crossword/session-"):
                _wait_for_merge(root, pr["url"], pr["headRefOid"])
                run("git", "fetch", "origin")

        # Squash merges have different commit IDs. Accept a merged PR only
        # when its exact head matches the local branch, preserving later edits.
        branches = run(
            "git", "for-each-ref", "--format=%(refname:short)",
            "refs/heads/crossword/session-*",
        ).splitlines()
        for branch in branches:
            ancestor = subprocess.run(
                ["git", "merge-base", "--is-ancestor", branch, "origin/main"],
                cwd=root, capture_output=True, check=False, timeout=45,
            )
            if ancestor.returncode == 0:
                continue
            if ancestor.returncode != 1:
                raise RuntimeError("Could not verify saved session " + branch)
            head = run("git", "rev-parse", branch)
            if not any(p["state"] == "MERGED" and p["headRefOid"] == head
                       for p in prs("--state", "all", "--head", branch)):
                raise RuntimeError(
                    "Saved session needs review: " + branch
                    + ". Its latest commit is not verified as merged. "
                    "Open its PR or recover its workbook before continuing."
                )

        # Require local main to be an ancestor, not merely fast-forwardable:
        # local-only commits must also receive human review.
        run("git", "merge-base", "--is-ancestor", "main", "origin/main")
        run("git", "switch", "main")
        run("git", "merge", "--ff-only", "origin/main")
        _warn("Main is up to date. Starting from the latest merged workbook.")
        return before != run("git", "rev-parse", "HEAD")
    except (OSError, subprocess.TimeoutExpired, ValueError, KeyError, TypeError) as exc:
        raise RuntimeError(
            "Could not verify startup safely. Check GitHub access and retry. "
            "The workshop has not opened."
        ) from exc


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


def _run_checked(root: Path, *args: str) -> str:
    """Run bounded Git/GitHub operations without a shell or credential output."""
    try:
        result = subprocess.run(
            list(args), cwd=root, capture_output=True, text=True,
            check=False, timeout=45,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError("Git/GitHub could not respond. Your work is preserved; retry later.") from exc
    if result.returncode:
        raise RuntimeError(
            f"{args[0]} {args[1]} failed. Your work is preserved. "
            "Check GitHub access or resolve the Git problem before retrying."
        )
    return result.stdout.rstrip("\n")


def _branch_prs(root: Path, branch: str) -> list[dict]:
    """Read all PR states so retries reuse a PR and never revive a closed one."""
    try:
        records = json.loads(_run_checked(
            root, "gh", "pr", "list", "--base", "main", "--head", branch,
            "--state", "all", "--limit", "1000",
            "--json", "state,headRefOid,url",
        ))
        if not isinstance(records, list) or len(records) >= 1000:
            raise ValueError("Incomplete PR results")
        return records
    except (ValueError, TypeError) as exc:
        raise RuntimeError("Could not read PR status. Your session is preserved.") from exc


def _wait_for_merge(root: Path, url: str, expected_head: str) -> None:
    """Wait only in an interactive terminal; Enter triggers verification, not a merge."""
    _warn("Your workbook is saved. Review and merge this pull request: " + url)
    _warn("For a draft PR, click Ready for review first, then merge after checks pass.")
    if not sys.stdin.isatty():
        raise RuntimeError("Merge the PR on GitHub, then run python crossword.py again.")
    while True:
        try:
            answer = input("After merging, press Enter to check; type q to finish later: ")
        except (EOFError, KeyboardInterrupt) as exc:
            raise RuntimeError("Session preserved. Run python crossword.py when ready.") from exc
        if answer.strip().lower() == "q":
            raise RuntimeError("Session preserved. Run python crossword.py when ready.")
        try:
            pr = json.loads(_run_checked(
                root, "gh", "pr", "view", url,
                "--json", "state,headRefOid,baseRefName",
            ))
            if pr["headRefOid"] != expected_head or pr["baseRefName"] != "main":
                raise RuntimeError("The PR changed. Session preserved; review its latest work.")
            if pr["state"] == "MERGED":
                return
            if pr["state"] == "CLOSED":
                raise RuntimeError("The PR was closed without merging. Session preserved.")
            _warn("This PR is still open. Merge it on GitHub, or type q to finish later.")
        except (ValueError, KeyError, TypeError) as exc:
            raise RuntimeError("Could not verify the merge. Session preserved.") from exc


def recover_session(root: Path, branch: str) -> None:
    """Commit only workbook edits and recover interrupted push/PR/merge steps.

    Never switch away from uncommitted work or publish unrelated commits.
    Already merged exact heads are accepted, including squash merges.
    """
    if not branch.startswith("crossword/session-"):
        raise RuntimeError("Automatic recovery is limited to crossword session branches.")
    if _run_checked(root, "git", "branch", "--show-current") != branch:
        raise RuntimeError("The branch changed. Recovery stopped.")
    # Parse NUL-delimited status safely; renames/deletions/conflicts require review.
    status = _run_checked(root, "git", "status", "--porcelain=v1", "-z",
                          "--untracked-files=all")
    paths = []
    for record in status.split("\0"):
        if not record:
            continue
        code, path = record[:2], record[3:]
        candidate = Path(path)
        if (code not in (" M", "M ", "MM", "A ", "AM", "??")
                or candidate.parent.as_posix() != "tools/puzzles"
                or candidate.suffix.lower() != ".xlsx"
                or not (root / candidate).is_file()
                or (root / candidate).is_symlink()):
            raise RuntimeError("Unrelated, deleted, or conflicted files need attention. Session preserved.")
        paths.append(path)
    _run_checked(root, "git", "fetch", "origin")
    records = _branch_prs(root, branch)
    head = _run_checked(root, "git", "rev-parse", "HEAD")
    merged = any(p["state"] == "MERGED" and p["headRefOid"] == head for p in records)
    if records and not any(p["state"] == "OPEN" for p in records):
        if merged and not paths:
            return
        raise RuntimeError("This session PR is closed or merged but has additional work. Preserve it for manual review.")
    # Check the entire proposed PR, not only the files staged in this invocation.
    base = _run_checked(root, "git", "merge-base", "HEAD", "origin/main")
    changed = _run_checked(root, "git", "diff", "--name-only", "-z", base, "HEAD")
    for path in changed.split("\0"):
        if path and (Path(path).parent.as_posix() != "tools/puzzles"
                     or Path(path).suffix.lower() != ".xlsx"):
            raise RuntimeError("Session includes unrelated commits. Review them manually before publishing.")
    if paths:
        _run_checked(root, "git", "add", "--", *paths)
        _run_checked(root, "git", "commit", "-m", "Save crossword workshop question bank edits")
        head = _run_checked(root, "git", "rev-parse", "HEAD")
    if head == base and not records:
        return  # Empty interrupted session: startup can safely return to main.
    _run_checked(root, "git", "push", "-u", "origin", branch)
    open_pr = next((p for p in records if p["state"] == "OPEN"), None)
    if open_pr:
        url = open_pr["url"]
    else:
        url = _run_checked(
            root, "gh", "pr", "create", "--draft", "--base", "main", "--head", branch,
            "--title", "Crossword workshop question bank — " + datetime.now().strftime("%Y-%m-%d"),
            "--body", "Saved workbook edits, including recovery after an interrupted session. "
            "Review and merge manually. Puzzle PDFs are published separately.",
        )
    _wait_for_merge(root, url, head)


def finish_session(root: Path, branch: str | None) -> None:
    """Use the same recoverable handoff on exit, then refresh clean main."""
    if not branch:
        return
    try:
        if _run_checked(root, "git", "branch", "--show-current") != branch:
            raise RuntimeError("Branch changed while the workshop ran. Automatic handoff stopped.")
        prepare_startup(root)
    except (RuntimeError, KeyboardInterrupt) as exc:
        _warn(str(exc) or "Session preserved. Run python crossword.py to continue later.")
