"""Tests for the opt-in-by-clean-main crossword draft-PR handoff."""
from __future__ import annotations

import importlib.util
import os
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "crossword_workshop_git", ROOT / "tools/puzzles/workshop_git.py"
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class WorkshopGitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        self._run("init", "-b", "main")
        self._run("config", "user.name", "Test author")
        self._run("config", "user.email", "testing@example.org")
        path = self.root / "tools/puzzles/FND_Crossword_Question_Bank_Template.xlsx"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"initial-workbook")
        self._run("add", ".")
        self._run("commit", "-m", "Initial test workbook")
        self.workbook = path

    def _run(self, *args):
        result = subprocess.run(
            ["git", *args], cwd=self.root, text=True, capture_output=True, check=False
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def _start(self):
        with patch.object(module.shutil, "which", return_value="/usr/bin/tool"):
            return module.start_session(self.root)

    def _gh_stub(self):
        bindir = self.root.parent / "bin"
        bindir.mkdir(exist_ok=True)
        gh = bindir / "gh"
        gh.write_text("#!/bin/sh\nprintf 'https://github.com/example/repo/pull/9\\n'\n")
        gh.chmod(0o755)
        return patch.dict(os.environ, {"PATH": str(bindir) + os.pathsep + os.environ["PATH"]})

    def test_clean_main_without_edits_returns_to_main(self):
        name = self._start()
        self.assertTrue(name.startswith("crossword/session-"))
        self.assertEqual(self._run("branch", "--show-current"), name)
        module.finish_session(self.root, name)
        self.assertEqual(self._run("branch", "--show-current"), "main")
        self.assertNotIn(name, self._run("branch", "--list", name))

    def test_dirty_main_keeps_existing_work_untouched(self):
        self.workbook.write_bytes(b"earlier-unsaved-edit")
        self.assertIsNone(self._start())
        self.assertEqual(self._run("branch", "--show-current"), "main")
        self.assertEqual(self.workbook.read_bytes(), b"earlier-unsaved-edit")

    def test_only_workbook_committed_pushed_and_pr_prepared(self):
        remote = self.root.parent / "upstream.git"
        bare = subprocess.run(
            ["git", "init", "--bare", "-b", "main", str(remote)],
            capture_output=True, text=True
        )
        self.assertEqual(bare.returncode, 0, bare.stderr)
        self._run("remote", "add", "origin", str(remote))
        self._run("push", "-u", "origin", "main")
        name = self._start()
        self.workbook.write_bytes(b"session-workbook-update")
        with self._gh_stub():
            module.finish_session(self.root, name)
        self.assertEqual(self._run("branch", "--show-current"), "main")
        self.assertEqual(self._run("status", "--porcelain"), "")
        self.assertIn(name, self._run("ls-remote", "--heads", "origin", name))

    def test_other_untracked_files_are_not_committed_or_removed(self):
        remote = self.root.parent / "upstream.git"
        subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)],
                       check=True, capture_output=True)
        self._run("remote", "add", "origin", str(remote))
        self._run("push", "-u", "origin", "main")
        name = self._start()
        self.workbook.write_bytes(b"session-edit")
        other = self.root / "unrelated.txt"
        other.write_text("keep me")
        with self._gh_stub():
            module.finish_session(self.root, name)
        self.assertEqual(self._run("branch", "--show-current"), name)
        self.assertTrue(other.is_file())
        self.assertEqual(self._run("show", "--format=", "--name-only", "HEAD"),
                         "tools/puzzles/FND_Crossword_Question_Bank_Template.xlsx")


class StartupTests(unittest.TestCase):
    _run = WorkshopGitTests._run
    """Exercise startup against real local Git repositories, with GitHub stubbed."""

    def setUp(self):
        WorkshopGitTests.setUp(self)
        remote = self.root.parent / "origin.git"
        subprocess.run(["git", "init", "--bare", "-b", "main", str(remote)],
                       check=True, capture_output=True)
        self._run("remote", "add", "origin", str(remote))
        self._run("push", "-u", "origin", "main")

    def prepare(self, records=()):
        real_run = subprocess.run

        def dispatch(args, **kwargs):
            if args[0] == "gh":
                selected = list(records)
                if args[args.index("--state") + 1] == "open":
                    selected = [p for p in selected if p["state"] == "OPEN"]
                return subprocess.CompletedProcess(args, 0, json.dumps(selected), "")
            return real_run(args, **kwargs)

        with patch.object(module.shutil, "which", return_value="/usr/bin/tool"), \
             patch.object(module.subprocess, "run", side_effect=dispatch):
            return module.prepare_startup(self.root)

    def test_updates_stale_main_from_remote(self):
        self.workbook.write_bytes(b"new merged clues")
        self._run("commit", "-am", "New clues")
        self._run("push", "origin", "main")
        self._run("reset", "--hard", "HEAD~1")
        self.assertTrue(self.prepare())
        self.assertEqual(self.workbook.read_bytes(), b"new merged clues")

    def test_unsaved_work_is_preserved(self):
        self.workbook.write_bytes(b"unsaved")
        with self.assertRaisesRegex(RuntimeError, "Uncommitted"):
            self.prepare()
        self.assertEqual(self.workbook.read_bytes(), b"unsaved")

    def test_open_session_blocks_even_on_main(self):
        with self.assertRaisesRegex(RuntimeError, "still open"):
            self.prepare([dict(state="OPEN", headRefName="crossword/session-test",
                               headRefOid="unused", url="https://example.test/pr/1")])
        self.assertEqual(self._run("branch", "--show-current"), "main")

    def test_unpushed_session_blocks(self):
        self._run("switch", "-c", "crossword/session-test")
        self.workbook.write_bytes(b"local only")
        self._run("commit", "-am", "Local work")
        with self.assertRaisesRegex(RuntimeError, "needs review"):
            self.prepare()
        self.assertEqual(self.workbook.read_bytes(), b"local only")

    def test_squashed_session_can_return_to_main(self):
        branch = "crossword/session-test"
        self._run("switch", "-c", branch)
        self.workbook.write_bytes(b"saved clues")
        self._run("commit", "-am", "Session")
        head = self._run("rev-parse", "HEAD")
        self._run("switch", "main")
        self._run("merge", "--squash", branch)
        self._run("commit", "-m", "Squashed PR")
        self._run("push", "origin", "main")
        self._run("switch", branch)
        records = [dict(state="MERGED", headRefName=branch, headRefOid=head,
                        url="https://example.test/pr/1")]
        self.assertTrue(self.prepare(records))
        self.assertEqual(self._run("branch", "--show-current"), "main")
        self.assertEqual(self.workbook.read_bytes(), b"saved clues")
        # Edits after the merged PR must never be mistaken for merged work.
        self._run("switch", branch)
        self.workbook.write_bytes(b"later clues")
        self._run("commit", "-am", "Later work")
        with self.assertRaisesRegex(RuntimeError, "needs review"):
            self.prepare(records)

    def test_unreachable_remote_stops(self):
        self._run("remote", "set-url", "origin", str(self.root / "missing.git"))
        with self.assertRaisesRegex(RuntimeError, "failed"):
            self.prepare()
        self.assertEqual(self._run("branch", "--show-current"), "main")

    def test_local_main_commits_stop(self):
        self.workbook.write_bytes(b"local main work")
        self._run("commit", "-am", "Local main")
        with self.assertRaisesRegex(RuntimeError, "failed"):
            self.prepare()
        self.assertEqual(self.workbook.read_bytes(), b"local main work")



if __name__ == "__main__":
    unittest.main()
