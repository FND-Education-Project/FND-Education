#!/usr/bin/env python3
"""One-command launcher for the PRIVATE FND crossword workshop in Codespaces.

From the repository root:
    python crossword.py

Create/reuse an isolated Python environment, install the existing
workshop dependencies only when needed, and start the original Streamlit
app. Codespaces automatically forwards port 8501 and opens a browser using
.vscode/settings.json. We print a clickable URL as a fallback.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent
REQUIREMENTS = ROOT / "tools" / "puzzles" / "requirements-crosswords.txt"
WORKSHOP = ROOT / "tools" / "puzzles" / "crossword_app.py"
VENV = ROOT / ".venv-crossword"
INSTALLED_HASH = VENV / ".fnd-requirements-sha256"
PORT = 8501
HEALTH = f"http://127.0.0.1:{PORT}/_stcore/health"


def workshop_url(environment: dict[str, str] | None = None) -> str:
    """Return the private forwarded Codespaces URL, or a localhost fallback."""
    values = os.environ if environment is None else environment
    name = values.get("CODESPACE_NAME", "").strip()
    domain = values.get("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN", "app.github.dev")
    if name and domain and all(c.isalnum() or c == "-" for c in name) and all(
        c.isalnum() or c in ".-" for c in domain
    ):
        return f"https://{name}-{PORT}.{domain}/"
    return f"http://localhost:{PORT}/"


def python_in_venv() -> Path:
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ready() -> bool:
    try:
        with urlopen(HEALTH, timeout=1.0) as answer:
            return answer.status == 200 and answer.read(20).strip() == b"ok"
    except (OSError, URLError, TimeoutError):
        return False


def install_if_needed() -> Path:
    if not REQUIREMENTS.is_file() or not WORKSHOP.is_file():
        raise RuntimeError("Run this from the FND Education repository containing tools/puzzles.")
    if not python_in_venv().is_file():
        print("Preparing the private crossword Python environment (first launch only)…", flush=True)
        subprocess.run([sys.executable, "-m", "venv", str(VENV)], check=True, cwd=ROOT)
    python = python_in_venv()
    fingerprint = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()
    previous = INSTALLED_HASH.read_text(encoding="utf-8").strip() if INSTALLED_HASH.is_file() else ""
    if previous == fingerprint:
        check = subprocess.run(
            [str(python), "-c", "import streamlit, pandas, openpyxl, fitz, PIL"],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            check=False,
        )
        if check.returncode == 0:
            return python
    print("Installing crossword workshop dependencies. Please wait…", flush=True)
    subprocess.run(
        [str(python), "-m", "pip", "install", "--disable-pip-version-check",
         "-r", str(REQUIREMENTS)],
        cwd=ROOT, check=True,
    )
    INSTALLED_HASH.write_text(fingerprint + "\n", encoding="utf-8")
    return python


def show_open_instructions() -> None:
    print("\n" + "=" * 58, flush=True)
    print("FND Crossword Workshop is ready.", flush=True)
    print("Codespaces should open your PRIVATE forwarded browser tab.", flush=True)
    print("If it doesn't, open the following link:", flush=True)
    print("  " + workshop_url(), flush=True)
    print("The Ports tab must show port 8501 as PRIVATE, not Public.", flush=True)
    print("Exit using the workshop's 'Exit workshop' button.", flush=True)
    print("Or press Ctrl+C here to stop the server.", flush=True)
    print("=" * 58 + "\n", flush=True)


def main() -> int:
    if sys.version_info < (3, 10):
        print("Python 3.10 or newer is required.", file=sys.stderr)
        return 1
    if ready():
        print("A Streamlit workshop is already running on port 8501.", flush=True)
        show_open_instructions()
        return 0
    try:
        python = install_if_needed()
    except (subprocess.CalledProcessError, OSError, RuntimeError) as error:
        print(f"Could not prepare the crossword workshop: {error}", file=sys.stderr)
        return 1

    # Codespaces recognizes this listener and .vscode/settings.json requests
    # that port 8501 open automatically in the user's browser. No changes to
    # port visibility are requested. Codespaces' default is PRIVATE.
    command = [
        str(python), "-m", "streamlit", "run", str(WORKSHOP),
        "--server.address", "0.0.0.0",
        "--server.port", str(PORT),
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false",
    ]
    print("Starting the private Python crossword workshop…", flush=True)
    try:
        process = subprocess.Popen(command, cwd=ROOT)
    except OSError as error:
        print(f"Could not start Streamlit: {error}", file=sys.stderr)
        return 1

    try:
        deadline = time.monotonic() + 90
        while time.monotonic() < deadline:
            if process.poll() is not None:
                print("The workshop stopped before it opened.", file=sys.stderr)
                return process.returncode or 1
            if ready():
                show_open_instructions()
                return process.wait()
            time.sleep(0.7)
        print("Workshop startup timed out. Check terminal errors.", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nStopping the private crossword workshop…", flush=True)
        return 0
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGTERM)
            try:
                process.wait(timeout=6)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    raise SystemExit(main())
