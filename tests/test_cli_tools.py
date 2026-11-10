"""Tests for the ``telegram <tool> <action>`` commands and their sessions.

Every command must reach the handler the MCP server registers, so these tests
stub the transport (``create_backend``) rather than the handlers: a CLI call
runs the real ``telegram.tools.dispatch`` entry, the real tool handler and the
real argument model, and only Telegram itself is fake.

Output contract under test: ``--json`` prints the tool envelope on stdout,
human output is ``key: value`` lines, a tool error goes to stderr and exits 1.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest

from telegram import cli
from telegram.config import Settings
from telegram.credential_state import CredentialState
from telegram.tool_session import (
    ToolSessionError,
    connected_backend,
    load_settings,
    not_configured_hint,
)

FAKE_TOKEN = "123456:" + "B" * 35
PHONE = "+10000000000"


def _settings(mode: str = "bot") -> Settings:
    if mode == "user":
        return Settings(phone=PHONE)
    return Settings(bot_token=FAKE_TOKEN)


@contextmanager
def _stubbed(backend: Any, settings: Settings | None = None):
    """Stub the backend transport; keep handlers and dispatch real."""
    with (
        patch(
            "telegram.tool_session.load_settings",
            return_value=settings or _settings(),
        ) as load,
        patch(
            "telegram.auth.telegram_auth_provider.create_backend",
            return_value=backend,
        ) as create,
    ):
        yield backend, load, create


def _run(capsys, argv: list[str]) -> tuple[int, str, str]:
    rc = cli.main(argv)
    out, err = capsys.readouterr()
    return rc, out, err


# --- usage ---


class TestUsage:
    def test_help_lists_operator_commands_and_tool_groups_separately(self, capsys):
        rc, out, err = _run(capsys, ["--help"])
        assert (rc, err) == (0, "")
        operator_block = out.split("tool commands")[0]
        assert "operator commands" in operator_block
        assert "doctor" in operator_block
        assert "message   send | edit" in out.split("tool commands")[1]
        assert "settings  status | set | cache_clear" in out

    def test_short_help_flag(self, capsys):
        rc, out, _ = _run(capsys, ["-h"])
        assert rc == 0
        assert "usage: telegram" in out


# --- message group ---


class TestMessageGroup:
    def test_send_json_runs_handler(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, err = _run(
                capsys,
                ["message", "send", "--chat-id", "42", "--text", "hi", "--json"],
            )
        assert (rc, err) == (0, "")
        assert json.loads(out) == {"message_id": 1}
        mock_backend.send_message.assert_awaited_once_with(
            42, "hi", reply_to=None, parse_mode=None
        )

    def test_negative_chat_id_becomes_int(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, _ = _run(
                capsys,
                [
                    "message",
                    "history",
                    "--chat-id=-1001234567890",
                    "--limit",
                    "5",
                ],
            )
        assert rc == 0
        mock_backend.get_history.assert_awaited_once_with(
            -1001234567890, limit=5, offset_id=None
        )

    def test_username_chat_id_stays_a_string(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, _ = _run(capsys, ["message", "history", "--chat-id", "@mychannel"])
        assert rc == 0
        mock_backend.get_history.assert_awaited_once_with(
            "@mychannel", limit=20, offset_id=None
        )

    def test_human_output_summarizes_messages(self, capsys, mock_backend):
        mock_backend.search_messages = AsyncMock(
            return_value=[{"message_id": 5, "text": "hello"}]
        )
        with _stubbed(mock_backend):
            rc, out, err = _run(capsys, ["message", "search", "--query", "hello"])
        assert (rc, err) == (0, "")
        assert "messages: 1" in out
        assert "message_id=5" in out

    def test_missing_argument_is_a_tool_error(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, err = _run(capsys, ["message", "send", "--chat-id", "42"])
        assert rc == 1
        assert out == ""
        assert "requires chat_id and text" in err
        mock_backend.send_message.assert_not_awaited()

    def test_tool_error_as_json_goes_to_stderr(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, err = _run(capsys, ["message", "delete", "--json"])
        assert rc == 1
        assert out == ""
        assert "error" in json.loads(err)


# --- chat group ---


class TestChatGroup:
    def test_list_json_runs_handler(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(capsys, ["chat", "list", "--json"])
        assert rc == 0
        assert json.loads(out) == {"chats": [], "count": 0}
        mock_backend.list_chats.assert_awaited_once_with(limit=50)

    def test_create_without_title_fails(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, err = _run(capsys, ["chat", "create"])
        assert rc == 1
        assert "'create' requires title" in err

    def test_create_passes_title_and_channel_flag(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, _ = _run(
                capsys, ["chat", "create", "--title", "news", "--is-channel"]
            )
        assert rc == 0
        mock_backend.create_chat.assert_awaited_once_with("news", is_channel=True)


# --- media group ---


class TestMediaGroup:
    def test_download_json_runs_handler(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(
                capsys,
                ["media", "download", "--chat-id", "12", "--message-id", "7", "--json"],
            )
        assert rc == 0
        assert json.loads(out) == {"path": "/tmp/file.jpg"}
        mock_backend.download_media.assert_awaited_once_with(
            12, 7, file_id=None, output_dir=None
        )

    def test_send_photo_maps_action_to_media_type(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(
                capsys,
                [
                    "media",
                    "send_photo",
                    "--chat-id",
                    "12",
                    "--file-path-or-url",
                    "/tmp/a.jpg",
                    "--caption",
                    "look",
                    "--json",
                ],
            )
        assert rc == 0
        assert json.loads(out) == {"message_id": 3}
        mock_backend.send_media.assert_awaited_once_with(
            12, "photo", "/tmp/a.jpg", caption="look"
        )

    def test_missing_file_fails(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, err = _run(capsys, ["media", "send_file", "--chat-id", "12"])
        assert rc == 1
        assert "requires chat_id and file_path_or_url" in err


# --- contact group ---


class TestContactGroup:
    def test_list_json_runs_handler(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(capsys, ["contact", "list", "--json"])
        assert rc == 0
        assert json.loads(out) == {"contacts": [], "count": 0}
        mock_backend.list_contacts.assert_awaited_once_with()

    def test_add_without_phone_fails(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, err = _run(capsys, ["contact", "add", "--first-name", "An"])
        assert rc == 1
        assert "requires phone and first_name" in err

    def test_block_passes_unblock_flag(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, _ = _run(capsys, ["contact", "block", "--user-id", "9", "--unblock"])
        assert rc == 0
        mock_backend.block_user.assert_awaited_once_with(9, unblock=True)


# --- settings group (the MCP `config` tool) ---


class TestSettingsGroup:
    def test_status_json_reports_connection(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(capsys, ["settings", "status", "--json"])
        assert rc == 0
        payload = json.loads(out)
        assert payload["mode"] == "bot"
        assert payload["connected"] is True
        assert payload["authorized"] is True
        mock_backend.is_connected.assert_awaited_once_with()

    def test_status_human_output_nests_runtime_config(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(capsys, ["settings", "status"])
        assert rc == 0
        assert "mode: bot" in out
        assert "connected: True" in out
        assert "config:" in out
        assert "  message_limit: " in out
        assert "  timeout: " in out

    def test_set_typed_limit_updates_runtime_config(self, capsys, mock_backend):
        import telegram.server as srv

        before = dict(srv._runtime_config)
        try:
            with _stubbed(mock_backend):
                rc, out, _ = _run(
                    capsys, ["settings", "set", "--timeout", "45", "--json"]
                )
            assert rc == 0
            assert json.loads(out)["updated"] == {"timeout": 45}
            assert srv._runtime_config["timeout"] == 45
        finally:
            srv._runtime_config.clear()
            srv._runtime_config.update(before)

    def test_set_with_unknown_key_fails(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, _, err = _run(
                capsys, ["settings", "set", "--key", "nope", "--value", "1"]
            )
        assert rc == 1
        assert "Invalid key: nope" in err

    def test_cache_clear_runs_handler(self, capsys, mock_backend):
        with _stubbed(mock_backend):
            rc, out, _ = _run(capsys, ["settings", "cache_clear", "--json"])
        assert rc == 0
        assert json.loads(out) == {"message": "Cache cleared."}
        mock_backend.clear_cache.assert_awaited_once_with()


# --- help group ---


class TestHelpGroup:
    def test_topic_json_wraps_documentation(self, capsys):
        rc, out, _ = _run(capsys, ["help", "messages", "--json"])
        assert rc == 0
        payload = json.loads(out)
        assert payload["topic"] == "messages"
        assert "message" in payload["content"].lower()

    def test_default_topic_prints_all_docs(self, capsys):
        rc, out, err = _run(capsys, ["help"])
        assert (rc, err) == (0, "")
        assert "messages" in out

    def test_default_topic_json(self, capsys):
        rc, out, _ = _run(capsys, ["help", "--json"])
        assert rc == 0
        assert json.loads(out)["topic"] == "all"

    def test_unknown_topic_is_a_tool_error(self, capsys):
        rc, out, err = _run(capsys, ["help", "nope"])
        assert rc == 1
        assert out == ""
        assert "Unknown topic" in err

    def test_unknown_topic_as_json_goes_to_stderr(self, capsys):
        rc, out, err = _run(capsys, ["help", "nope", "--json"])
        assert rc == 1
        assert out == ""
        assert "Unknown topic" in json.loads(err)["error"]

    def test_help_needs_no_credentials(self, capsys):
        # No backend stub at all: help must not open a session.
        rc, out, _ = _run(capsys, ["help", "chats"])
        assert rc == 0
        assert out.strip()

    def test_help_failure_prints_one_line(self, capsys):
        with patch(
            "telegram.tools.dispatch.run_help",
            new=AsyncMock(side_effect=RuntimeError("boom")),
        ):
            rc, out, err = _run(capsys, ["help"])
        assert rc == 1
        assert out == ""
        assert err.strip() == "telegram: boom"


# --- rendering helpers ---


class TestHumanRendering:
    def test_summary_of_plain_list(self):
        assert cli._summary([1, 2]) == "2 items"

    def test_summary_of_empty_dict(self):
        assert cli._summary({}) == "{}"

    def test_help_error_accepts_documents_and_ignores_non_errors(self):
        assert cli._help_error("# Documentation") is None
        assert cli._help_error("{not json") is None
        assert cli._help_error('["a"]') is None
        assert cli._help_error('{"error": "nope"}') == "nope"


# --- shared entry point (server and CLI call the same function) ---


class TestSharedDispatch:
    def test_chat_command_calls_the_dispatch_entry(self, capsys, mock_backend):
        with (
            _stubbed(mock_backend),
            patch(
                "telegram.tools.dispatch.run_chat",
                new=AsyncMock(return_value={"chats": [], "count": 0}),
            ) as run_chat,
        ):
            rc, out, _ = _run(capsys, ["chat", "list", "--json"])
        assert rc == 0
        assert json.loads(out) == {"chats": [], "count": 0}
        called = run_chat.await_args
        assert called is not None
        assert called.args[0] is mock_backend
        assert called.kwargs["action"] == "list"

    def test_media_command_calls_the_dispatch_entry(self, capsys, mock_backend):
        with (
            _stubbed(mock_backend),
            patch(
                "telegram.tools.dispatch.run_media",
                new=AsyncMock(return_value={"path": "x"}),
            ) as run_media,
        ):
            rc, _, _ = _run(
                capsys, ["media", "download", "--chat-id", "1", "--message-id", "2"]
            )
        assert rc == 0
        called = run_media.await_args
        assert called is not None
        assert called.args[0] is mock_backend


# --- namespace plumbing and session failures ---


class TestNamespaceAndSessions:
    def test_user_flag_selects_namespace(self, capsys, mock_backend):
        with _stubbed(mock_backend) as (_, load, _):
            rc, _, _ = _run(capsys, ["chat", "list", "--user", "alice"])
        assert rc == 0
        load.assert_called_once_with("alice")

    def test_not_configured_exits_1_with_hint(self, capsys):
        with patch("telegram.tool_session.load_settings", return_value=None):
            rc, out, err = _run(capsys, ["chat", "list"])
        assert rc == 1
        assert out == ""
        assert "no Telegram credentials" in err
        assert "telegram auth --bot-token" in err

    def test_transport_failure_prints_one_sanitized_line(self, capsys, mock_backend):
        with (
            _stubbed(mock_backend),
            patch(
                "telegram.auth.telegram_auth_provider.create_backend",
                side_effect=RuntimeError(FAKE_TOKEN + " boom"),
            ),
        ):
            rc, out, err = _run(capsys, ["chat", "list"])
        assert rc == 1
        assert out == ""
        assert "Traceback" not in err
        assert "123456:<redacted>" in err

    def test_load_settings_uses_env(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", FAKE_TOKEN)
        settings = load_settings()
        assert settings is not None
        assert settings.bot_token == FAKE_TOKEN

    def test_load_settings_uses_saved_config(self):
        with (
            patch(
                "telegram.credential_state.resolve_credential_state",
                return_value=CredentialState.CONFIGURED,
            ),
            patch(
                "telegram.credential_state._read_single_user_config",
                return_value={"TELEGRAM_BOT_TOKEN": FAKE_TOKEN},
            ),
        ):
            settings = load_settings()
        assert settings is not None
        assert settings.bot_token == FAKE_TOKEN

    def test_load_settings_without_credentials(self):
        with patch(
            "telegram.credential_state.resolve_credential_state",
            return_value=CredentialState.AWAITING_SETUP,
        ):
            assert load_settings() is None

    def test_load_settings_without_saved_config(self):
        with (
            patch(
                "telegram.credential_state.resolve_credential_state",
                return_value=CredentialState.CONFIGURED,
            ),
            patch(
                "telegram.credential_state._read_single_user_config",
                return_value=None,
            ),
        ):
            assert load_settings() is None

    def test_load_settings_ignores_saved_config_without_credentials(self):
        with (
            patch(
                "telegram.credential_state.resolve_credential_state",
                return_value=CredentialState.CONFIGURED,
            ),
            patch(
                "telegram.credential_state._read_single_user_config",
                return_value={"TELEGRAM_PHONE": ""},
            ),
        ):
            assert load_settings() is None

    def test_load_settings_for_other_namespace(self):
        with patch(
            "telegram.auth.telegram_auth_provider.settings_for_namespace",
            return_value=_settings(),
        ) as for_namespace:
            settings = load_settings("alice")
        assert settings is not None
        for_namespace.assert_called_once_with("alice")

    async def test_connected_backend_connects_and_disconnects(
        self, monkeypatch, mock_backend
    ):
        monkeypatch.setenv("TELEGRAM_BOT_TOKEN", FAKE_TOKEN)
        with patch(
            "telegram.auth.telegram_auth_provider.create_backend",
            return_value=mock_backend,
        ) as create:
            async with connected_backend() as opened:
                assert opened is mock_backend
        create.assert_called_once()
        mock_backend.connect.assert_awaited_once_with()
        mock_backend.disconnect.assert_awaited_once_with()

    async def test_connected_backend_requires_credentials(self):
        with patch("telegram.tool_session.load_settings", return_value=None):
            with pytest.raises(ToolSessionError) as excinfo:
                async with connected_backend():
                    pass
        assert "telegram auth" in str(excinfo.value)

    async def test_connected_backend_rejects_unauthorized_session(
        self, mock_user_backend
    ):
        mock_user_backend.is_authorized = AsyncMock(return_value=False)
        with (
            patch(
                "telegram.tool_session.load_settings",
                return_value=_settings("user"),
            ),
            patch(
                "telegram.auth.telegram_auth_provider.create_backend",
                return_value=mock_user_backend,
            ),
        ):
            with pytest.raises(ToolSessionError) as excinfo:
                async with connected_backend():
                    pass
        assert "not authorized" in str(excinfo.value)
        mock_user_backend.disconnect.assert_awaited_once_with()

    def test_not_configured_hint_names_the_namespace(self):
        assert "--user alice" in not_configured_hint("alice")
        assert "--user" not in not_configured_hint()
