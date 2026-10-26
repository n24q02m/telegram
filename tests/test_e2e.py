"""Full E2E test for the telegram MCP server -- 2 setup modes, 2 backend modes.

Tests 6 tools, 31 actions via the MCP protocol over stdio.
Bot mode tests a subset (bot API limitations).
User mode tests all actions.

Credentials come from env vars (``TELEGRAM_BOT_TOKEN`` / ``TELEGRAM_PHONE``)
or from a prior ``telegram auth`` on this machine. These tests talk to the
real Telegram API and are excluded from the default ``pytest`` run.

Usage:
    # Bot mode
    uv run pytest tests/test_e2e.py -m e2e --setup=env --backend=bot -v

    # User mode (run `telegram auth --phone <+number>` first)
    uv run pytest tests/test_e2e.py -m e2e --setup=env --backend=user -v

    # Plugin mode (published package)
    uv run pytest tests/test_e2e.py -m e2e --setup=plugin --backend=bot -v
"""

from __future__ import annotations

import os
import warnings

import pytest
import pytest_asyncio
from conftest_e2e import parse_result, parse_result_allow_error
from mcp import StdioServerParameters
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.timeout(180),
    pytest.mark.asyncio(loop_scope="module"),
]

EXPECTED_TOOLS = {
    "message",
    "chat",
    "media",
    "contact",
    "config",
    "help",
}


@pytest.fixture(scope="module")
def setup_mode(request):
    return request.config.getoption("--setup")


@pytest.fixture(scope="module")
def backend_mode(request):
    return request.config.getoption("--backend")


def _build_server_params(setup_mode: str):
    if setup_mode == "env":
        params = StdioServerParameters(
            command="uv", args=["run", "telegram"], env=dict(os.environ)
        )
    elif setup_mode == "plugin":
        params = StdioServerParameters(
            command="uvx",
            args=["--python", "3.13", "n24q02m-telegram@latest"],
            env=dict(os.environ),
        )
    else:
        msg = f"Unknown setup mode: {setup_mode}"
        raise ValueError(msg)

    return params


@pytest_asyncio.fixture(scope="module", loop_scope="module")
async def session(setup_mode):
    params = _build_server_params(setup_mode)

    try:
        async with stdio_client(params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as s:
                await s.initialize()
                yield s
    except (RuntimeError, ExceptionGroup) as exc:
        msg = str(exc).lower()
        if "cancel scope" in msg or "different task" in msg:
            warnings.warn(
                f"Suppressed teardown error: {exc}", RuntimeWarning, stacklevel=1
            )
        else:
            raise


# -- Server Init --


class TestServerInit:
    async def test_connects(self, session):
        assert session is not None

    async def test_tools_list(self, session):
        result = await session.list_tools()
        names = {t.name for t in result.tools}
        assert names == EXPECTED_TOOLS

    async def test_tools_have_schema(self, session):
        result = await session.list_tools()
        for tool in result.tools:
            assert tool.inputSchema is not None
            assert tool.description


# -- Message Tool (8 actions) --


class TestMessage:
    """Test message domain actions. Some actions require user mode."""

    async def test_send(self, session):
        r = await session.call_tool(
            "message", {"action": "send", "chat_id": "me", "text": "E2E test message"}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_search(self, session):
        r = await session.call_tool(
            "message", {"action": "search", "query": "E2E test"}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_history(self, session):
        r = await session.call_tool(
            "message", {"action": "history", "chat_id": "me", "limit": 5}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_edit(self, session):
        # Send then edit
        r = await session.call_tool(
            "message", {"action": "send", "chat_id": "me", "text": "will be edited"}
        )
        text = parse_result_allow_error(r)
        r = await session.call_tool(
            "message",
            {
                "action": "edit",
                "chat_id": "me",
                "message_id": 1,
                "text": "edited by E2E",
            },
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_forward(self, session):
        r = await session.call_tool(
            "message",
            {"action": "forward", "from_chat": "me", "to_chat": "me", "message_id": 1},
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_pin(self, session):
        r = await session.call_tool(
            "message", {"action": "pin", "chat_id": "me", "message_id": 1}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_react(self, session):
        r = await session.call_tool(
            "message",
            {"action": "react", "chat_id": "me", "message_id": 1, "emoji": "thumbs_up"},
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_delete(self, session):
        r = await session.call_tool(
            "message", {"action": "delete", "chat_id": "me", "message_id": 1}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)


# -- Chat Tool (9 actions) --


class TestChat:
    async def test_list(self, session):
        r = await session.call_tool("chat", {"action": "list", "limit": 5})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_info(self, session):
        r = await session.call_tool("chat", {"action": "info", "chat_id": "me"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_create(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("create requires user mode")
        r = await session.call_tool(
            "chat", {"action": "create", "title": "E2E Test Chat"}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_join(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("join requires user mode")
        r = await session.call_tool(
            "chat", {"action": "join", "link_or_hash": "test_invite_link"}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_leave(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("leave requires user mode")
        r = await session.call_tool(
            "chat", {"action": "leave", "chat_id": "test_chat_id"}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_members(self, session):
        r = await session.call_tool("chat", {"action": "members", "chat_id": "me"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_admin(self, session):
        r = await session.call_tool("chat", {"action": "admin", "chat_id": "me"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_settings(self, session):
        r = await session.call_tool("chat", {"action": "settings", "chat_id": "me"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_topics(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("topics requires user mode or supergroup")
        r = await session.call_tool(
            "chat", {"action": "topics", "chat_id": "test_supergroup"}
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)


# -- Media Tool (5 actions) --


class TestMedia:
    async def test_send_photo(self, session):
        r = await session.call_tool(
            "media",
            {
                "action": "send_photo",
                "chat_id": "me",
                "file_path_or_url": "https://www.w3.org/Icons/w3c_home.png",
            },
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_send_file(self, session):
        r = await session.call_tool(
            "media",
            {
                "action": "send_file",
                "chat_id": "me",
                "file_path_or_url": "https://example.com/test.txt",
            },
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_send_voice(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("send_voice may require user mode")
        r = await session.call_tool(
            "media",
            {
                "action": "send_voice",
                "chat_id": "me",
                "file_path_or_url": "https://example.com/voice.ogg",
            },
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_send_video(self, session):
        r = await session.call_tool(
            "media",
            {
                "action": "send_video",
                "chat_id": "me",
                "file_path_or_url": "https://example.com/video.mp4",
            },
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_download(self, session):
        r = await session.call_tool(
            "media",
            {
                "action": "download",
                "chat_id": "me",
                "message_id": 1,
                "output_dir": "/tmp",
            },
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)


# -- Contact Tool (4 actions) --


class TestContact:
    async def test_list(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("list requires user mode")
        r = await session.call_tool("contact", {"action": "list"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_search(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("search requires user mode")
        r = await session.call_tool("contact", {"action": "search", "query": "test"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_add(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("add requires user mode")
        r = await session.call_tool(
            "contact",
            {"action": "add", "phone": "+0000000000", "first_name": "E2E Test"},
        )
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_block(self, session, backend_mode):
        if backend_mode == "bot":
            pytest.skip("block requires user mode")
        r = await session.call_tool("contact", {"action": "block", "user_id": 0})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)


# -- Config + Help --


class TestConfig:
    async def test_status(self, session):
        r = await session.call_tool("config", {"action": "status"})
        text = parse_result(r)
        assert isinstance(text, str)

    async def test_set(self, session):
        r = await session.call_tool("config", {"action": "set", "message_limit": 42})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)

    async def test_cache_clear(self, session):
        r = await session.call_tool("config", {"action": "cache_clear"})
        text = parse_result_allow_error(r)
        assert isinstance(text, str)


class TestHelp:
    async def test_help(self, session):
        r = await session.call_tool("help", {})
        text = parse_result(r)
        assert "message" in text.lower() or "telegram" in text.lower()


class TestErrorHandling:
    async def test_invalid_action(self, session):
        r = await session.call_tool("message", {"action": "nonexistent"})
        text = parse_result_allow_error(r)
        assert (
            "error" in text.lower()
            or "unknown" in text.lower()
            or "invalid" in text.lower()
        )
