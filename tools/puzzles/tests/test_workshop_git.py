"""Recovery tests use real Git repositories and a deterministic GitHub stub."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("handoff", ROOT / "tools/puzzles/workshop_git.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        self.real_run = subprocess.run
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.org")
        self.book = self.root / "tools/puzzles/bank.xlsx"
        self.book.parent.mkdir(parents=True)
        self.book.write_bytes(b"original")
        self.git("add", ".")
        self.git("commit", "-m", "initial")
        self.remote = self.root.parent / "remote.git"
        self.git("init", "--bare", str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        self.git("push", "-u", "origin", "main")
        self.pr = None
        self.creates = 0
        self.views = 0
        self.merge_on_view = True
        self.branch = "crossword/session-test"

    def git(self, *args):
        r = self.real_run(["git", *args], cwd=self.root, text=True,
                          capture_output=True, check=True)
        return r.stdout.strip()

    def dispatch(self, args, **kwargs):
        """Simulate GitHub state, including a real squash commit on remote main."""
        if args[0] != "gh":
            return self.real_run(args, **kwargs)
        action = args[2]
        if action == "list":
            records = [self.pr] if self.pr else []
            if args[args.index("--state") + 1] == "open":
                records = [p for p in records if p["state"] == "OPEN"]
            output = json.dumps(records)
        elif action == "create":
            self.creates += 1
            self.pr = dict(state="OPEN", headRefName=self.branch,
                           headRefOid=self.git("rev-parse", "HEAD"),
                           baseRefName="main", url="https://example.test/pr/1")
            output = self.pr["url"]
        elif action == "view":
            self.views += 1
            if self.merge_on_view:
                # A squash merge deliberately has a different commit ID.
                commit = self.git("commit-tree", self.git("rev-parse", "HEAD^{tree}"),
                                  "-p", self.git("rev-parse", "origin/main"),
                                  "-m", "Squash workbook PR")
                self.git("push", "origin", commit + ":refs/heads/main")
                self.pr["state"] = "MERGED"
            output = json.dumps(self.pr)
        else:
            raise AssertionError(args)
        return subprocess.CompletedProcess(args, 0, output, "")

    def invoke(self, finish=False, answers=("",), interactive=True):
        with patch.object(module.shutil, "which", return_value="/usr/bin/tool"), \
             patch.object(module.subprocess, "run", side_effect=self.dispatch), \
             patch.object(module.sys.stdin, "isatty", return_value=interactive), \
             patch("builtins.input", side_effect=answers):
            if finish:
                return module.finish_session(self.root, self.branch)
            return module.prepare_startup(self.root)

    def session(self, commit=False):
        self.git("switch", "-c", self.branch)
        self.book.write_bytes(b"recovered clues")
        if commit:
            self.git("commit", "-am", "saved")

    def test_dirty_interrupted_session_recovers_and_updates_main(self):
        self.session()
        self.assertTrue(self.invoke())
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertEqual(self.book.read_bytes(), b"recovered clues")
        self.assertEqual(self.creates, 1)

    def test_committed_but_unpushed_session_recovers(self):
        self.session(commit=True)
        self.invoke()
        self.assertEqual(self.creates, 1)
        self.assertEqual(self.git("branch", "--show-current"), "main")

    def test_normal_exit_uses_same_verified_handoff(self):
        self.session()
        self.invoke(finish=True)
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.views, 1)

    def test_noninteractive_preserves_pushed_session_and_retry_reuses_pr(self):
        self.session()
        with self.assertRaisesRegex(RuntimeError, "run python"):
            self.invoke(interactive=False)
        self.assertEqual(self.git("branch", "--show-current"), self.branch)
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.invoke()
        self.assertEqual(self.creates, 1)

    def test_enter_does_not_prove_merge(self):
        self.session()
        self.merge_on_view = False
        with self.assertRaisesRegex(RuntimeError, "preserved"):
            self.invoke(answers=("", "q"))
        self.assertEqual(self.views, 1)
        self.assertEqual(self.git("branch", "--show-current"), self.branch)

    def test_unrelated_staged_changes_block_before_commit(self):
        self.session()
        (self.root / "other.txt").write_text("keep")
        self.git("add", "other.txt")
        before = self.git("rev-parse", "HEAD")
        with self.assertRaisesRegex(RuntimeError, "Unrelated"):
            self.invoke()
        self.assertEqual(self.git("rev-parse", "HEAD"), before)
        self.assertEqual(self.book.read_bytes(), b"recovered clues")

    def test_dirty_main_is_not_committed(self):
        self.book.write_bytes(b"main edit")
        with self.assertRaisesRegex(RuntimeError, "Uncommitted"):
            self.invoke()

    def test_unrelated_session_commits_are_not_pushed(self):
        self.session(commit=True)
        (self.root / "other.txt").write_text("keep")
        self.git("add", ".")
        self.git("commit", "-m", "unrelated")
        with self.assertRaisesRegex(RuntimeError, "unrelated commits"):
            self.invoke()
        self.assertEqual(self.creates, 0)

    def test_empty_session_returns_to_main_without_pr(self):
        self.git("switch", "-c", self.branch)
        self.invoke()
        self.assertEqual(self.git("branch", "--show-current"), "main")
        self.assertEqual(self.creates, 0)

    def test_already_squashed_session_recognized_after_remote_branch_deleted(self):
        self.session()
        self.invoke()
        self.git("push", "origin", "--delete", self.branch)
        self.git("switch", self.branch)
        self.invoke()
        self.assertEqual(self.creates, 1)
        self.assertEqual(self.git("branch", "--show-current"), "main")

    def test_post_merge_edits_are_preserved_for_review(self):
        self.session()
        self.invoke()
        self.git("switch", self.branch)
        self.book.write_bytes(b"later edits")
        with self.assertRaisesRegex(RuntimeError, "additional work"):
            self.invoke()
        self.assertEqual(self.book.read_bytes(), b"later edits")

    def test_unreachable_remote_preserves_work(self):
        self.session()
        self.git("remote", "set-url", "origin", str(self.root / "missing"))
        with self.assertRaisesRegex(RuntimeError, "failed"):
            self.invoke()
        self.assertEqual(self.book.read_bytes(), b"recovered clues")

    def test_stale_main_updates(self):
        self.book.write_bytes(b"new main")
        self.git("commit", "-am", "update")
        self.git("push", "origin", "main")
        self.git("reset", "--hard", "HEAD~1")
        self.invoke()
        self.assertEqual(self.book.read_bytes(), b"new main")

    def test_closed_unmerged_pr_preserves_session(self):
        self.session(commit=True)
        self.pr = dict(state="CLOSED", headRefOid=self.git("rev-parse", "HEAD"))
        with self.assertRaisesRegex(RuntimeError, "closed"):
            self.invoke()


if __name__ == "__main__":
    unittest.main()
