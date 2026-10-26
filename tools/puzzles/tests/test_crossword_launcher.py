"""Tests for the stdlib-only, one-command Codespaces crossword launcher."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from io import BytesIO

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("fnd_crossword_launcher", ROOT / "crossword.py")
launcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(launcher)


class CrosswordLauncherTests(unittest.TestCase):
    def test_codespaces_url_is_constructed_from_environment(self):
        url = launcher.workshop_url({
            "CODESPACE_NAME": "friendly-place-ab12",
            "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN": "app.github.dev",
        })
        self.assertEqual(url, "https://friendly-place-ab12-8502.app.github.dev/")

    def test_local_fallback_and_invalid_codespace_name(self):
        self.assertEqual(launcher.workshop_url({}), "http://localhost:8502/")
        self.assertEqual(
            launcher.workshop_url({
                "CODESPACE_NAME": "has.unexpected.dots",
                "GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN": "app.github.dev",
            }),
            "http://localhost:8502/",
        )

    def test_original_python_workshop_is_selected(self):
        self.assertEqual(launcher.WORKSHOP, ROOT / "tools/puzzles/crossword_app.py")
        self.assertTrue(launcher.WORKSHOP.is_file())
        self.assertTrue(launcher.REQUIREMENTS.is_file())
        self.assertEqual(launcher.PORT, 8502)

    def test_codespaces_requests_browser_open_on_private_port(self):
        config = json.loads((ROOT / ".vscode/settings.json").read_text())
        self.assertTrue(config["remote.autoForwardPorts"])
        self.assertEqual(
            config["remote.portsAttributes"]["8502"]["onAutoForward"],
            "openBrowser",
        )

    def test_health_probe_recognizes_streamlit(self):
        class Health:
            status = 200

            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def read(self, _max):
                return b"ok"

        with patch.object(launcher, "urlopen", return_value=Health()):
            self.assertTrue(launcher.ready())


if __name__ == "__main__":
    unittest.main()
