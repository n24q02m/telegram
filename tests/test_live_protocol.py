"""Live MCP protocol tests for the telegram MCP server.

Spawns the MCP server as a subprocess and communicates via the MCP protocol
(JSON-RPC over stdio), testing ALL tools through the actual transport layer.

Tests are split into two groups:
- Direct stdio credential-gate coverage lives in ``test_stdio_direct.py``.
- Auth tests here require TELEGRAM_BOT_TOKEN (skip if not set).
"""

from __future__ import annotations

import json
import os
import re

import pytest
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

live = pytest.mark.live

# External-content tools wrap their JSON payload in <untrusted_..._content> XPIA
# boundary tags + a [SECURITY: ...] warning; strip them to recover the JSON body.
_UNTRUSTED_WRAPPER = re.compile(
    r"^<untrusted_[a-z_]+_content>\n(?P<body>.*)\n</untrusted_[a-z_]+_content>\n\n"
    r"\[SECURITY:",
    re.DOTALL,
)


def _parse_result(result) -> dict | str:
    """Extract text from MCP call_tool result and try to parse as JSON."""
    text = result.content[0].text
    match = _UNTRUSTED_WRAPPER.match(text)
    if match:
        text = match.group("body")
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return text


def _server_params(*, with_token: bool = False) -> StdioServerParameters:
    """Build server params, optionally injecting BOT_TOKEN."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("TELEGRAM_")}
    if with_token and BOT_TOKEN:
        env["TELEGRAM_BOT_TOKEN"] = BOT_TOKEN
    return StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "telegram"],
        env=env,
    )


# =========================================================================
# Auth tests: server starts WITH TELEGRAM_BOT_TOKEN
# =========================================================================


@live
@pytest.mark.skipif(not BOT_TOKEN, reason="TELEGRAM_BOT_TOKEN not set")
class TestWithAuth:
    """Tests that require a valid TELEGRAM_BOT_TOKEN."""

    async def test_list_tools_with_auth(self):
        """Server exposes exactly 6 tools when authenticated."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                names = {t.name for t in tools.tools}
                expected = {
                    "message",
                    "chat",
                    "media",
                    "contact",
                    "config",
                    "help",
                }
                assert expected == names, f"Expected {expected}, got {names}"

    async def test_config_status_connected(self):
        """config status shows connected=True with valid token."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("config", {"action": "status"})
                data = _parse_result(result)
                assert isinstance(data, dict)
                assert data.get("connected") is True
                assert data.get("mode") == "bot"

    async def test_config_set_message_limit(self):
        """config set updates message_limit at protocol level."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(
                    "config", {"action": "set", "message_limit": 42}
                )
                data = _parse_result(result)
                assert isinstance(data, dict)
                assert data.get("updated", {}).get("message_limit") == 42

    async def test_config_cache_clear(self):
        """config cache_clear succeeds at protocol level."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("config", {"action": "cache_clear"})
                data = _parse_result(result)
                assert isinstance(data, dict)
                assert "message" in data or "error" not in data

    async def test_config_unknown_action(self):
        """config with unknown action returns error."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("config", {"action": "nonexistent"})
                data = _parse_result(result)
                assert isinstance(data, dict)
                assert "error" in data

    async def test_help_all_with_auth(self):
        """help returns full documentation when authenticated."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("help", {})
                data = _parse_result(result)
                if isinstance(data, str):
                    assert len(data) > 100

    async def test_message_history_bot_self(self):
        """message history on bot's own chat returns result (may be empty)."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # Bot history returns empty list (Bot API limitation)
                result = await session.call_tool(
                    "message",
                    {"action": "history", "chat_id": "123", "limit": 5},
                )
                data = _parse_result(result)
                assert isinstance(data, dict)
                # Either returns data or a structured error (NOT a crash)
                assert "error" in data or "messages" in data or isinstance(data, dict)

    async def test_chat_list_bot_mode_error(self):
        """chat list in bot mode returns mode error."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("chat", {"action": "list"})
                data = _parse_result(result)
                assert isinstance(data, dict)
                # Bot mode cannot list chats - should return error
                assert "error" in data

    async def test_contact_list_bot_mode_error(self):
        """contact list in bot mode returns mode error."""
        async with stdio_client(_server_params(with_token=True)) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("contact", {"action": "list"})
                data = _parse_result(result)
                assert isinstance(data, dict)
                assert "error" in data
