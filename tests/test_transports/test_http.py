"""HTTP transport: the telegram FastMCP server behind hull auth.

``start_http`` error paths are unit-tested; the auth behaviour is exercised
against a real uvicorn listener on 127.0.0.1 serving hull's
``build_http_app(telegram.server.mcp, settings)``, driven by raw httpx requests
and by a FastMCP client over Streamable HTTP. The server runs in-process (a
thread) so the autouse fake-home isolation from conftest.py applies to it.
No credentials are configured, so nothing contacts Telegram.
"""

from __future__ import annotations

import socket
import threading
import time
from collections.abc import Iterator
from unittest.mock import patch

import httpx
import pytest
import uvicorn
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from hull_core.auth.tokens import hash_token
from hull_core.server.http import build_http_app

from telegram.server import main as server_main
from telegram.transports import http as http_transport
from telegram.transports.http import config_dir, load_http_settings, start_http

GOOD_TOKEN = "good-token-for-tests"
WRONG_TOKEN = "wrong-token-for-tests"
ALICE_TOKEN = "alice-token-for-tests"
BOB_TOKEN = "bob-token-for-tests"

INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "0"},
    },
}
MCP_HEADERS = {
    "Accept": "application/json, text/event-stream",
    "Content-Type": "application/json",
}


def _write_config(body: str) -> None:
    config_dir().mkdir(parents=True, exist_ok=True)
    (config_dir() / "config.toml").write_text(body, encoding="utf-8")


# --- settings + start_http ---


def test_config_dir_is_dot_telegram_under_home(tmp_path):
    from pathlib import Path

    assert config_dir() == Path.home() / ".telegram"


def test_default_settings_bind_loopback_without_config_file():
    settings = load_http_settings()
    assert settings.server.host == "127.0.0.1"
    assert settings.server.port == 8000
    assert settings.server.auth == "no-auth"


def test_settings_read_from_config_toml():
    _write_config('[server]\nport = 9123\nauth = "token"\ntoken_hash = "scrypt$x"\n')
    settings = load_http_settings()
    assert settings.server.port == 9123
    assert settings.server.auth == "token"


@pytest.mark.parametrize(
    ("body", "fragment"),
    [
        ("[server\n", "not valid TOML"),
        ('[server]\nauth = "token"\n', "requires a non-empty token_hash"),
        ('[server]\nauth = "bogus"\n', "auth must be one of"),
    ],
)
def test_invalid_config_returns_2_with_one_line(capsys, body, fragment):
    _write_config(body)
    assert start_http() == 2
    stderr = capsys.readouterr().err
    assert stderr.startswith("[telegram] ")
    assert fragment in stderr
    assert "Traceback" not in stderr


def test_multi_mode_without_users_file_returns_2(capsys):
    _write_config('[server]\nauth = "multi"\n')
    assert start_http() == 2
    assert "users file not found" in capsys.readouterr().err


def test_no_auth_on_all_interfaces_is_refused(capsys):
    assert start_http(host="0.0.0.0") == 2
    stderr = capsys.readouterr().err
    assert "no-auth" in stderr
    assert "refusing host '0.0.0.0'" in stderr


def test_cli_no_auth_on_all_interfaces_is_refused(capsys):
    """Same refusal through the server entry (``--http --host 0.0.0.0``)."""
    assert server_main(["--http", "--host", "0.0.0.0"]) == 2
    assert "only permits loopback binds" in capsys.readouterr().err


def test_mcp_transport_env_selects_http(monkeypatch):
    monkeypatch.setenv("MCP_TRANSPORT", "http")
    with patch.object(http_transport, "run_http_server") as run:
        assert server_main([]) == 0
    run.assert_called_once()


def test_host_and_port_overrides_reach_hull():
    calls = {}

    async def _fake(mcp, settings, *, host=None, port=None):
        calls.update(host=host, port=port, auth=settings.server.auth)

    with patch.object(http_transport, "run_http_server", _fake):
        assert start_http(host="127.0.0.2", port=9001) == 0
    assert calls == {"host": "127.0.0.2", "port": 9001, "auth": "no-auth"}


def test_keyboard_interrupt_exits_cleanly():
    async def _interrupt(*args, **kwargs):
        raise KeyboardInterrupt

    with patch.object(http_transport, "run_http_server", _interrupt):
        assert start_http() == 0


# --- real loopback listener ---


class _LoopbackServer:
    """uvicorn on an ephemeral 127.0.0.1 port, in a daemon thread."""

    def __init__(self, app) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.bind(("127.0.0.1", 0))
        self.port = self._sock.getsockname()[1]
        self.server = uvicorn.Server(
            uvicorn.Config(app, host="127.0.0.1", port=self.port, log_level="warning")
        )
        self._thread = threading.Thread(
            target=self.server.run, kwargs={"sockets": [self._sock]}, daemon=True
        )

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"

    def __enter__(self) -> _LoopbackServer:
        self._thread.start()
        deadline = time.monotonic() + 15
        while not self.server.started:
            if time.monotonic() > deadline or not self._thread.is_alive():
                raise RuntimeError("loopback server did not start")
            time.sleep(0.05)
        return self

    def __exit__(self, *exc) -> None:
        self.server.should_exit = True
        self._thread.join(timeout=15)
        self._sock.close()


@pytest.fixture
def token_server() -> Iterator[_LoopbackServer]:
    _write_config(
        f'[server]\nauth = "token"\ntoken_hash = "{hash_token(GOOD_TOKEN)}"\n'
    )
    from telegram.server import mcp

    with _LoopbackServer(build_http_app(mcp, load_http_settings())) as server:
        yield server


def _bearer(token: str) -> dict[str, str]:
    return {**MCP_HEADERS, "Authorization": f"Bearer {token}"}


def test_health_is_public(token_server):
    response = httpx.get(f"{token_server.url}/health", timeout=10)
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_missing_token_is_401(token_server):
    response = httpx.post(
        f"{token_server.url}/mcp", json=INITIALIZE, headers=MCP_HEADERS, timeout=10
    )
    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_wrong_token_is_401(token_server):
    response = httpx.post(
        f"{token_server.url}/mcp",
        json=INITIALIZE,
        headers=_bearer(WRONG_TOKEN),
        timeout=10,
    )
    assert response.status_code == 401
    assert response.json()["error"] == "unauthorized"


def test_right_token_initializes(token_server):
    response = httpx.post(
        f"{token_server.url}/mcp",
        json=INITIALIZE,
        headers=_bearer(GOOD_TOKEN),
        timeout=10,
    )
    assert response.status_code == 200
    assert '"serverInfo"' in response.text
    assert '"telegram"' in response.text


async def test_client_over_http_lists_tools_and_reads_status(token_server):
    transport = StreamableHttpTransport(
        f"{token_server.url}/mcp", headers={"Authorization": f"Bearer {GOOD_TOKEN}"}
    )
    async with Client(transport) as client:
        tools = await client.list_tools()
        assert sorted(t.name for t in tools) == [
            "chat",
            "config",
            "contact",
            "help",
            "media",
            "message",
        ]
        status = await client.call_tool("config", {"action": "status"})
        assert status.structured_content["configured"] is False
        # Token mode is the shared ``default`` namespace: no --user hint.
        assert "--user" not in status.structured_content["setup"]["bot_mode"]


async def test_multi_mode_routes_each_token_to_its_namespace():
    users = config_dir() / "users.toml"
    config_dir().mkdir(parents=True, exist_ok=True)
    users.write_text(
        f'[users.alice]\ntoken_hash = "{hash_token(ALICE_TOKEN)}"\nnamespace = "a"\n'
        f'[users.bob]\ntoken_hash = "{hash_token(BOB_TOKEN)}"\nnamespace = "b"\n',
        encoding="utf-8",
    )
    _write_config('[server]\nauth = "multi"\n')
    from hull_core.server.app import load_users_for

    from telegram.server import mcp

    settings = load_http_settings()
    app = build_http_app(mcp, settings, users=load_users_for(settings))
    with _LoopbackServer(app) as server:
        for token, namespace in ((ALICE_TOKEN, "a"), (BOB_TOKEN, "b")):
            transport = StreamableHttpTransport(
                f"{server.url}/mcp", headers={"Authorization": f"Bearer {token}"}
            )
            async with Client(transport) as client:
                status = await client.call_tool("config", {"action": "status"})
                hint = status.structured_content["setup"]["bot_mode"]
                assert hint.endswith(f"--user {namespace}` (get from @BotFather)")
