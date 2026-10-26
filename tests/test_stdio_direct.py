"""Stdio subprocess tests over the real MCP wire protocol.

Each test spawns the CLI through ``tests/stdio_bootstrap.py`` so the child
process runs with an isolated home and an isolated pre-hull legacy config path
(see that module for why HOME alone is not enough on Windows).

- Unconfigured: the credential gate exits nonzero before any MCP output and
  prints the local auth guidance.
- Configured with a fake bot token (Bot API connect stubbed, no network):
  ``initialize``, ``tools/list`` (6 tools) and a ``help`` call succeed.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client
from stdio_bootstrap import BOOTSTRAP, EXIT_UNSAFE, isolated_env

from telegram.server import SETUP_DOCS_URL

pytestmark = pytest.mark.timeout(60)

FAKE_TOKEN = "123456:" + "A" * 35
EXPECTED_TOOLS = {"message", "chat", "media", "contact", "config", "help"}


def _run(
    env: dict[str, str], *args: str, stdin: str = ""
) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BOOTSTRAP), *args],
        env=env,
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
        check=False,
    )


def test_bootstrap_refuses_without_isolated_legacy_path(tmp_path: Path) -> None:
    env = isolated_env(tmp_path)
    del env["TELEGRAM_TEST_LEGACY_CONFIG"]
    result = _run(env, "--version")
    assert result.returncode == EXIT_UNSAFE
    assert "TELEGRAM_TEST_LEGACY_CONFIG is required" in result.stderr


def test_stdio_credential_gate_exits_before_mcp_handshake(tmp_path: Path) -> None:
    """Missing stdio credentials stop startup before MCP can respond."""
    result = _run(
        isolated_env(tmp_path, MCP_TRANSPORT="stdio"),
        stdin='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}\n',
    )
    assert result.returncode == 1
    assert result.stdout.strip() == ""

    stderr = result.stderr
    assert "[telegram] No Telegram credentials configured for stdio mode." in stderr
    assert "  telegram auth --bot-token <token>" in stderr
    assert "  telegram auth --phone <+number>" in stderr
    assert "login is a deprecated alias of auth" in stderr
    assert f"Documentation: {SETUP_DOCS_URL}" in stderr


async def test_stdio_initialize_list_tools_and_call_help(tmp_path: Path) -> None:
    env = isolated_env(
        tmp_path, TELEGRAM_BOT_TOKEN=FAKE_TOKEN, TELEGRAM_TEST_STUB_BOT="1"
    )
    params = StdioServerParameters(
        command=sys.executable, args=[str(BOOTSTRAP)], env=env
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            assert init.serverInfo.name == "telegram"

            tools = await session.list_tools()
            assert {t.name for t in tools.tools} == EXPECTED_TOOLS

            result = await session.call_tool("help", {"topic": "messages"})
            assert not result.isError
            text = result.content[0].text
            assert "message" in text.lower()
            assert FAKE_TOKEN not in text
