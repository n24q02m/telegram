from __future__ import annotations

import os
from contextlib import contextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastmcp import Client
from hull_core.auth import AuthContext, reset_current_user, set_current_user
from structured import payload, text

from telegram.server import get_backend, get_settings, main, mcp

EXPECTED_TOOLS = {"message", "chat", "media", "contact", "config", "help"}


@contextmanager
def as_namespace(namespace: str):
    """Run tool code as a hull caller of ``namespace`` (multi mode)."""
    token = set_current_user(
        AuthContext(uid=namespace, namespace=namespace, mode="multi")
    )
    try:
        yield
    finally:
        reset_current_user(token)


@pytest.fixture
def default_backend(mock_backend):
    """Install ``mock_backend`` as the configured default-namespace backend."""
    import telegram.server as srv

    old = (srv._backend, srv._pending_auth, srv._unconfigured)
    srv._backend = mock_backend
    srv._pending_auth = False
    srv._unconfigured = False
    try:
        yield mock_backend
    finally:
        srv._backend, srv._pending_auth, srv._unconfigured = old


@pytest.fixture
def server_state():
    """Save and restore the module-level server state around a test."""
    import telegram.server as srv

    old = (srv._backend, srv._settings, srv._pending_auth, srv._unconfigured)
    try:
        yield srv
    finally:
        srv._backend, srv._settings, srv._pending_auth, srv._unconfigured = old


async def test_mcp_has_6_tools():
    tools = await mcp.list_tools()
    assert {t.name for t in tools} == EXPECTED_TOOLS


async def test_serverinfo_version_matches_package():
    """serverInfo.version reports the package version, not the framework's."""
    from telegram import __version__

    async with Client(mcp) as client:
        info = client.server_info
    assert info.name == "telegram"
    assert info.version == __version__


def test_main_exists():
    assert callable(main)


def test_get_backend_not_initialized(server_state):
    server_state._backend = None
    with pytest.raises(RuntimeError, match="Backend not initialized"):
        get_backend()


def test_get_settings_not_initialized(server_state):
    server_state._settings = None
    with pytest.raises(RuntimeError, match="Settings not initialized"):
        get_settings()


def test_get_settings_success(server_state):
    from telegram.config import Settings

    mock_settings = Settings(api_id=123, api_hash="abc", mode="bot")
    server_state._settings = mock_settings
    assert get_settings() == mock_settings


# --- tools on the default namespace ---


async def test_message_send(default_backend):
    from telegram.server import message

    result = payload(await message(action="send", chat_id=123, text="hi"))
    assert "message_id" in result


async def test_message_result_has_text_and_structured_channels(default_backend):
    """_wrap_tool keeps both channels: XPIA-tagged text + structuredContent."""
    from telegram.server import message

    result = await message(action="send", chat_id=123, text="hi")
    assert "<untrusted_message_content>" in text(result)
    assert "message_id" in payload(result)


async def test_message_backend_exception(default_backend):
    """message tool returns an error dict when the backend raises."""
    from telegram.server import message

    default_backend.send_message.side_effect = RuntimeError("Backend failure")
    result = payload(await message(action="send", chat_id=123, text="hi"))
    assert "RuntimeError" in result["error"]
    assert "Operation failed" in result["error"]


async def test_message_unknown_action(default_backend):
    from telegram.server import message

    result = payload(await message(action="nonexistent"))
    assert "Unknown action" in result["error"]


async def test_chat_list(default_backend):
    from telegram.server import chat

    result = payload(await chat(action="list"))
    assert "chats" in result


async def test_media_send_photo(default_backend):
    from telegram.server import media

    result = payload(
        await media(
            action="send_photo",
            chat_id=123,
            file_path_or_url="https://example.com/photo.jpg",
        )
    )
    assert "message_id" in result


async def test_contact_list(default_backend):
    from telegram.server import contact

    result = payload(await contact(action="list"))
    assert "contacts" in result
    default_backend.list_contacts.assert_awaited_once()


async def test_contact_search(default_backend):
    from telegram.server import contact

    result = payload(await contact(action="search", query="John"))
    assert "contacts" in result
    default_backend.search_contacts.assert_awaited_once_with("John")


async def test_contact_add(default_backend):
    from telegram.server import contact

    result = payload(
        await contact(
            action="add", phone="+1234567890", first_name="John", last_name="Doe"
        )
    )
    assert "added" in result
    default_backend.add_contact.assert_awaited_once_with(
        "+1234567890", "John", last_name="Doe"
    )


async def test_contact_block(default_backend):
    from telegram.server import contact

    result = payload(await contact(action="block", user_id=123))
    assert "blocked" in result
    default_backend.block_user.assert_awaited_once_with(123, unblock=False)


async def test_contact_unblock(default_backend):
    from telegram.server import contact

    result = payload(await contact(action="block", user_id=123, unblock=True))
    assert "unblocked" in result
    default_backend.block_user.assert_awaited_once_with(123, unblock=True)


async def test_contact_error(default_backend):
    from telegram.server import contact

    default_backend.list_contacts.side_effect = Exception("test error")
    result = payload(await contact(action="list"))
    assert "Operation failed" in result["error"]


async def test_contact_unknown_action(default_backend):
    from telegram.server import contact

    result = payload(await contact(action="invalid_action"))
    assert "Unknown action" in result["error"]


async def test_config_tool(default_backend):
    from telegram.server import config

    result = await config(action="status")
    assert "mode" in result

    result = await config(action="set", message_limit=42)
    assert "updated" in result


async def test_help_tool():
    from telegram.server import help

    result = await help(topic="messages")
    assert "Telegram Messages" in result


# --- lifespan ---


def _fake_module(name: str, obj: object) -> object:
    return type("module", (), {name: obj})()


async def test_lifespan_bot_mode(server_state):
    from telegram.server import _lifespan

    mock_bot = AsyncMock()
    mock_bot.is_authorized = AsyncMock(return_value=True)
    with (
        patch.object(server_state, "Settings") as mock_settings_cls,
        patch.dict(
            "sys.modules",
            {
                "telegram.backends.bot_backend": _fake_module(
                    "BotBackend", MagicMock(return_value=mock_bot)
                )
            },
        ),
    ):
        mock_settings = mock_settings_cls.return_value
        mock_settings.is_configured = True
        mock_settings.mode = "bot"
        mock_settings.bot_token = "fake:token"

        async with _lifespan(mcp):
            assert server_state._backend is mock_bot
            mock_bot.connect.assert_awaited_once()

        mock_bot.disconnect.assert_awaited_once()


async def test_lifespan_user_mode(server_state):
    from telegram.server import _lifespan

    mock_settings = MagicMock()
    mock_settings.is_configured = True
    mock_settings.mode = "user"
    mock_settings.api_id = 12345
    mock_settings.api_hash = "testhash"
    mock_settings.phone = "+84912345678"

    mock_user_backend = AsyncMock()
    mock_user_backend.is_authorized = AsyncMock(return_value=True)

    with (
        patch.object(server_state, "Settings", return_value=mock_settings),
        patch.dict(
            "sys.modules",
            {
                "telegram.backends.user_backend": _fake_module(
                    "UserBackend", MagicMock(return_value=mock_user_backend)
                )
            },
        ),
    ):
        async with _lifespan(mcp):
            assert server_state._backend is mock_user_backend
            assert server_state._pending_auth is False
            mock_user_backend.connect.assert_awaited_once()

        mock_user_backend.disconnect.assert_awaited_once()


async def test_lifespan_user_mode_unauthorized(server_state):
    """An unauthorized user session sets pending_auth (no in-process auth flow)."""
    from telegram.server import _lifespan

    mock_settings = MagicMock()
    mock_settings.is_configured = True
    mock_settings.mode = "user"
    mock_settings.api_id = 12345
    mock_settings.api_hash = "testhash"
    mock_settings.phone = None

    mock_user_backend = AsyncMock()
    mock_user_backend.is_authorized = AsyncMock(return_value=False)

    with (
        patch.object(server_state, "Settings", return_value=mock_settings),
        patch.dict(
            "sys.modules",
            {
                "telegram.backends.user_backend": _fake_module(
                    "UserBackend", MagicMock(return_value=mock_user_backend)
                )
            },
        ),
    ):
        async with _lifespan(mcp):
            assert server_state._pending_auth is True

        mock_user_backend.disconnect.assert_awaited_once()


async def test_lifespan_unconfigured_mode(server_state):
    """Lifespan starts without credentials and resets the flag on exit."""
    from telegram.credential_state import CredentialState
    from telegram.server import _lifespan

    with (
        patch.object(server_state, "Settings") as mock_settings_cls,
        patch(
            "telegram.credential_state.resolve_credential_state",
            return_value=CredentialState.AWAITING_SETUP,
        ),
    ):
        mock_settings_cls.return_value.is_configured = False

        async with _lifespan(mcp):
            assert server_state._unconfigured is True

        assert server_state._unconfigured is False


async def test_lifespan_shuts_down_namespace_backends(server_state):
    """Leaving the lifespan disconnects every per-namespace backend."""
    from telegram.auth.telegram_auth_provider import (
        TelegramAuthProvider,
        set_global_provider,
    )
    from telegram.credential_state import CredentialState
    from telegram.server import _lifespan

    provider = TelegramAuthProvider()
    ns_backend = AsyncMock()
    provider.active_clients["a"] = ns_backend
    set_global_provider(provider)

    with (
        patch.object(server_state, "Settings") as mock_settings_cls,
        patch(
            "telegram.credential_state.resolve_credential_state",
            return_value=CredentialState.AWAITING_SETUP,
        ),
    ):
        mock_settings_cls.return_value.is_configured = False
        async with _lifespan(mcp):
            pass

    ns_backend.disconnect.assert_awaited_once()
    assert provider.active_clients == {}


async def test_lifespan_resolves_saved_credentials(server_state):
    """Lifespan loads the saved config via Settings.from_saved_config."""
    from telegram.credential_state import CredentialState
    from telegram.server import _lifespan

    initial = MagicMock()
    initial.is_configured = False
    reconfigured = MagicMock()
    reconfigured.is_configured = True
    reconfigured.mode = "bot"
    reconfigured.bot_token = "resolved:token"

    mock_bot = AsyncMock()
    mock_bot.is_authorized = AsyncMock(return_value=True)

    with (
        patch.object(server_state, "Settings") as mock_settings_cls,
        patch(
            "telegram.credential_state.resolve_credential_state",
            return_value=CredentialState.CONFIGURED,
        ),
        patch(
            "telegram.credential_state._read_single_user_config",
            return_value={"TELEGRAM_BOT_TOKEN": "resolved:token"},
        ),
        patch.dict(
            "sys.modules",
            {
                "telegram.backends.bot_backend": _fake_module(
                    "BotBackend", MagicMock(return_value=mock_bot)
                )
            },
        ),
    ):
        mock_settings_cls.return_value = initial
        mock_settings_cls.from_saved_config.return_value = reconfigured

        async with _lifespan(mcp):
            assert server_state._settings is reconfigured
            mock_settings_cls.from_saved_config.assert_called_once_with(
                {"TELEGRAM_BOT_TOKEN": "resolved:token"}
            )
            mock_bot.connect.assert_awaited_once()

        mock_bot.disconnect.assert_awaited_once()


def test_ensure_settings_loads_config_without_env_injection():
    """_ensure_settings reads the saved config explicitly; os.environ untouched.

    Exporting credentials into the process environment leaks them to every
    subprocess and third-party dependency.
    """
    import telegram.server as srv

    token = "123456:ABCdefGHIjklMNOpqrsTUVwxyz0123456789"
    isolated_home = {k: os.environ[k] for k in ("HOME", "USERPROFILE")}
    with (
        patch.dict(os.environ, isolated_home, clear=True),
        patch(
            "telegram.credential_state._read_single_user_config",
            return_value={"TELEGRAM_BOT_TOKEN": token},
        ),
    ):
        settings = srv._ensure_settings()

        assert settings.is_configured
        assert settings.bot_token == token
        assert "TELEGRAM_BOT_TOKEN" not in os.environ


def test_create_backend_instance_user_mode():
    from telegram.config import Settings
    from telegram.server import _create_backend_instance

    settings = Settings(phone="+10000000000")
    with patch("telegram.backends.user_backend.UserBackend") as mock_user:
        backend = _create_backend_instance(settings)
    assert backend is mock_user.return_value
    mock_user.assert_called_once_with(settings)


# --- pending_auth ---


@pytest.fixture
def pending_auth(default_backend):
    import telegram.server as srv

    srv._pending_auth = True
    return default_backend


async def test_message_blocked_during_pending_auth(pending_auth):
    from telegram.server import message

    result = payload(await message(action="send", chat_id=123, text="hi"))
    assert "not authenticated" in result["error"].lower()
    assert "telegram auth --phone" in result["error"]


async def test_chat_blocked_during_pending_auth(pending_auth):
    from telegram.server import chat

    result = payload(await chat(action="list"))
    assert "not authenticated" in result["error"].lower()


async def test_media_blocked_during_pending_auth(pending_auth):
    from telegram.server import media

    result = payload(
        await media(
            action="send_photo",
            chat_id=123,
            file_path_or_url="https://example.com/photo.jpg",
        )
    )
    assert "not authenticated" in result["error"].lower()


async def test_contact_blocked_during_pending_auth(pending_auth):
    from telegram.server import contact

    result = payload(await contact(action="list"))
    assert "not authenticated" in result["error"].lower()


async def test_config_works_during_pending_auth(pending_auth):
    """Config status always works, even during pending auth."""
    from telegram.server import config

    result = await config(action="status")
    assert "mode" in result
    assert result["pending_auth"] is True


async def test_help_works_during_pending_auth(pending_auth):
    from telegram.server import help

    result = await help(topic="messages")
    assert "Telegram Messages" in result


# --- unconfigured ---


@pytest.fixture
def unconfigured(server_state):
    server_state._unconfigured = True
    server_state._pending_auth = False
    return server_state


async def test_help_works_without_credentials():
    from telegram.server import help

    assert "Telegram Messages" in await help(topic="messages")
    assert "Telegram" in await help(topic=None)


async def test_message_returns_setup_hint_when_unconfigured(unconfigured):
    from telegram.server import message

    result = payload(await message(action="send", chat_id=123, text="hi"))
    assert result["error"] == "Not configured"
    setup = result["setup"]
    assert setup["bot_mode"]["env_var"] == "TELEGRAM_BOT_TOKEN"
    assert setup["bot_mode"]["command"] == "telegram auth --bot-token <token>"
    assert setup["user_mode"]["command"] == "telegram auth --phone <+number>"
    assert setup["user_mode"]["env_vars"] == ["TELEGRAM_PHONE"]


async def test_chat_returns_setup_hint_when_unconfigured(unconfigured):
    from telegram.server import chat

    result = payload(await chat(action="list"))
    assert result["error"] == "Not configured"
    assert "setup" in result


async def test_media_returns_setup_hint_when_unconfigured(unconfigured):
    from telegram.server import media

    result = payload(
        await media(
            action="send_photo",
            chat_id=123,
            file_path_or_url="https://example.com/photo.jpg",
        )
    )
    assert result["error"] == "Not configured"


async def test_contact_returns_setup_hint_when_unconfigured(unconfigured):
    from telegram.server import contact

    result = payload(await contact(action="list"))
    assert result["error"] == "Not configured"


def test_not_ready_response_unconfigured(unconfigured):
    data = unconfigured._not_ready_response()
    assert data["error"] == "Not configured"
    assert "bot_mode" in data["setup"]
    assert "user_mode" in data["setup"]


def test_not_ready_response_pending_auth(server_state):
    server_state._unconfigured = False
    server_state._pending_auth = True
    data = server_state._not_ready_response()
    assert "not authenticated" in data["error"].lower()


async def test_config_status_works_when_unconfigured(unconfigured):
    from telegram.server import config

    result = await config(action="status")
    assert result["configured"] is False
    assert result["connected"] is False
    assert "telegram auth --bot-token" in result["setup"]["bot_mode"]
    assert "relay" not in str(result).lower()


async def test_config_set_blocked_when_unconfigured(unconfigured):
    from telegram.server import config

    result = await config(action="set", message_limit=42)
    assert result["error"] == "Not configured"


async def test_config_unknown_setup_action_is_not_special(default_backend):
    """The relay-era setup_* actions are gone; they are plain unknown actions."""
    from telegram.server import config

    result = await config(action="setup_start")
    assert "error" in result


# --- non-default namespaces (hull multi mode) ---


def test_get_backend_namespace_without_backend():
    with (
        as_namespace("a"),
        pytest.raises(RuntimeError, match="No connected Telegram backend"),
    ):
        get_backend()


def test_get_backend_namespace_uses_provider():
    from telegram.auth.telegram_auth_provider import get_provider

    backend = MagicMock()
    get_provider().active_clients["a"] = backend
    with as_namespace("a"):
        assert get_backend() is backend


async def test_tool_in_unconfigured_namespace_returns_namespaced_hint():
    from telegram.server import message

    with as_namespace("a"):
        result = payload(await message(action="send", chat_id=1, text="hi"))
    assert result["error"] == "Not configured"
    assert result["setup"]["bot_mode"]["command"] == (
        "telegram auth --bot-token <token> --user a"
    )
    # Env vars only configure the default namespace.
    assert "env_var" not in result["setup"]["bot_mode"]


async def test_tool_in_unauthorized_namespace_returns_auth_hint():
    """Saved phone but no authorized session: point at `auth --user`."""
    from telegram.server import chat

    with (
        patch(
            "telegram.auth.telegram_auth_provider.settings_for_namespace",
            return_value=MagicMock(),
        ),
        patch(
            "telegram.auth.telegram_auth_provider.TelegramAuthProvider.get",
            new=AsyncMock(return_value=None),
        ),
        as_namespace("b"),
    ):
        result = payload(await chat(action="list"))
    assert "--user b" in result["error"]


async def test_config_status_in_unconfigured_namespace():
    from telegram.server import config

    with as_namespace("a"):
        result = await config(action="status")
    assert result["configured"] is False
    assert "--user a" in result["setup"]["bot_mode"]


async def test_config_in_ready_namespace_uses_namespace_backend(mock_backend):
    from telegram.server import config

    with (
        patch(
            "telegram.auth.telegram_auth_provider.TelegramAuthProvider.get",
            new=AsyncMock(return_value=mock_backend),
        ),
        as_namespace("a"),
    ):
        result = await config(action="status")
    assert "mode" in result


# --- main() ---


def test_main_stdio_runs_when_configured():
    import telegram.server as srv

    with (
        patch.object(srv.mcp, "run") as mock_run,
        patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "fake:token"}),
    ):
        assert main([]) == 0
    mock_run.assert_called_once_with(transport="stdio", show_banner=False)


def test_main_reads_sys_argv_when_argv_is_none():
    import telegram.server as srv

    with (
        patch.object(srv.mcp, "run") as mock_run,
        patch.object(srv, "_parse_serve_args", wraps=srv._parse_serve_args) as parse,
        patch("sys.argv", ["telegram"]),
        patch.dict(os.environ, {"TELEGRAM_BOT_TOKEN": "fake:token"}),
    ):
        assert main() == 0
    parse.assert_called_once_with([])
    mock_run.assert_called_once()


def test_main_stdio_missing_credentials_exits_1(capsys):
    """Stdio with no credentials returns 1 with a CLI login hint."""
    with (
        patch(
            "telegram.credential_state._read_single_user_config",
            return_value=None,
        ),
        patch(
            "telegram.credential_state.check_saved_sessions",
            return_value=False,
        ),
    ):
        assert main([]) == 1
    err_out = capsys.readouterr().err
    assert "stdio mode" in err_out
    assert "telegram auth --bot-token" in err_out
    assert "TELEGRAM_BOT_TOKEN" in err_out
    assert "https://github.com/n24q02m/telegram#setup" in err_out
    # No local setup endpoint: the hint never points at a browser form.
    for needle in ("localhost", "127.0.0.1", "--http", "/authorize"):
        assert needle not in err_out


def test_main_stdio_config_bot_token_no_env_runs():
    """A bot token in the saved config (not env) resolves CONFIGURED."""
    import telegram.server as srv

    with (
        patch(
            "telegram.credential_state._read_single_user_config",
            return_value={"TELEGRAM_BOT_TOKEN": "123:ABC"},
        ),
        patch.object(srv.mcp, "run") as mock_run,
    ):
        assert main([]) == 0
    mock_run.assert_called_once_with(transport="stdio", show_banner=False)


def test_main_stdio_phone_session_runs():
    import telegram.server as srv

    with (
        patch(
            "telegram.credential_state._read_single_user_config",
            return_value={"TELEGRAM_PHONE": "+84900000000"},
        ),
        patch.object(srv.mcp, "run") as mock_run,
    ):
        assert main([]) == 0
    mock_run.assert_called_once_with(transport="stdio", show_banner=False)


@pytest.mark.parametrize(
    ("argv", "env"),
    [
        (["--http"], {}),
        ([], {"MCP_TRANSPORT": "http"}),
        ([], {"TRANSPORT_MODE": "http"}),
    ],
)
def test_main_http_dispatches_to_start_http(argv, env):
    with (
        patch("telegram.transports.http.start_http", return_value=0) as start,
        patch.dict(os.environ, env),
    ):
        assert main(argv) == 0
    start.assert_called_once_with(host=None, port=None)


def test_main_http_passes_host_and_port():
    with patch("telegram.transports.http.start_http", return_value=2) as start:
        assert main(["--http", "--host", "127.0.0.1", "--port", "9123"]) == 2
    start.assert_called_once_with(host="127.0.0.1", port=9123)
