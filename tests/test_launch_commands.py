"""Every documented uvx launch of n24q02m-telegram runs on Python 3.13.

n24q02m-telegram declares ``Requires-Python ==3.13.*``. Without ``--python 3.13``
uvx uses the default interpreter: below 3.13 the install fails, and on 3.14 or
newer uv ignores the upper bound and runs telegram on a Python it does not
support. Smithery and the plugin manifest also spell out the same launch, so a
change to one must reach the other.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# CHANGELOG records history, legacy/ holds the frozen better-telegram-mcp stub
# as published, and tests describe gates rather than give install steps.
SKIPPED = ("CHANGELOG.md:", "legacy/", "tests/")


def test_documented_uvx_launches_pin_python_3_13():
    result = subprocess.run(
        ["git", "grep", "-nE", "-e", r"uvx (--from )?n24q02m-telegram"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode in (0, 1), result.stderr
    hits = [
        line
        for line in result.stdout.splitlines()
        if line and not line.startswith(SKIPPED)
    ]
    assert not hits, "uvx launch without --python 3.13:\n" + "\n".join(hits)


def test_smithery_launch_matches_the_plugin():
    manifest = json.loads(
        (REPO_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    server = manifest["mcpServers"]["telegram"]
    expected = (
        f"command: '{server['command']}', args: ["
        + ", ".join(f"'{arg}'" for arg in server["args"])
        + "]"
    )
    smithery = (REPO_ROOT / "smithery.yaml").read_text(encoding="utf-8")
    assert expected in smithery
