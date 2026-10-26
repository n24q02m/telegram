"""Tests for telegram.cli -- the hull ``build_cli`` mount.

Bare invocation and any leading-dash argv start the server unchanged;
subcommands run one-shot operator actions. hull's ``build_cli`` returns the
argparse exit code (2 on bad args) instead of raising ``SystemExit``.

No network or Telegram calls: the Bot/User backends are mocked and OTP/2FA
prompts are driven via patched stdin/getpass. Credential storage is the real
hull ``PerPluginStore`` under the fake home of the autouse
``_isolate_per_plugin_home`` fixture, so the logout tests prove the files are
actually gone.
"""

from __future__ import annotations

import io
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from telegram import __version__, cli
from telegram.credential_state import (
    _read_single_user_config,
    _write_single_user_config,
    plugin_store,
)

FAKE_TOKEN = "123456:" + "A" * 35
PHONE = "+10000000000"
TWO_FA_INPUT = "fake-2fa"


def _bot_backend(connect_error: Exception | None = None) -> MagicMock:
    backend = MagicMock()
    backend.connect = AsyncMock(side_effect=connect_error)
    backend.disconnect = AsyncMock()
    return backend


def _tty_stdin(line: str = "") -> MagicMock:
    stdin = MagicMock()
    stdin.isatty.return_value = True
    stdin.readline.return_value = line
    return stdin


def _pipe_stdin(text: str) -> io.StringIO:
    stdin = io.StringIO(text)
    stdin.isatty = lambda: False  # type: ignore[method-assign]
    return stdin


# --- dispatch + rc contract ---


class TestServeDispatch:
    """Bare/flag argv route to the server unchanged."""

    def test_bare_invocation_starts_server(self):
        with patch("telegram.server.main", return_value=0) as server_main:
            assert cli.main([]) == 0
        server_main.assert_called_once_with([])

    def test_http_flag_passes_through(self):
        with patch("telegram.server.main", return_value=0) as server_main:
            assert cli.main(["--http", "--port", "9001"]) == 0
        server_main.assert_called_once_with(["--http", "--port", "9001"])

    def test_server_rc_is_propagated(self):
        with patch("telegram.server.main", return_value=1):
            assert cli.main([]) == 1


class TestRcContract:
    def test_help_rc_0(self, capsys):
        assert cli.main(["--help"]) == 0
        out = capsys.readouterr().out
        assert "usage: better-telegram-mcp" in out
        for name in ("auth", "login", "logout", "status", "token"):
            assert name in out

    def test_version_rc_0(self, capsys):
        assert cli.main(["--version"]) == 0
        assert capsys.readouterr().out.strip() == f"better-telegram-mcp {__version__}"

    def test_unknown_subcommand_rc_2(self, capsys):
        assert cli.main(["nope"]) == 2
        assert "unknown subcommand 'nope'" in capsys.readouterr().err

    def test_token_hash_refuses_argv_token(self, capsys):
        assert cli.main(["token", "hash", "on-the-command-line"]) == 2
        captured = capsys.readouterr()
        assert "refusing to read a token from the command line" in captured.err
        assert "on-the-command-line" not in captured.out + captured.err

    def test_token_hash_from_stdin(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", _pipe_stdin("piped-token-value\n"))
        assert cli.main(["token", "hash"]) == 0
        out = capsys.readouterr().out
        assert out.startswith("scrypt$")
        assert "piped-token-value" not in out

    def test_status_on_empty_home(self, capsys):
        assert cli.main(["status"]) == 0
        assert "better-telegram-mcp: not configured" in capsys.readouterr().out

    def test_status_after_auth_reports_configured(self, capsys):
        _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
        assert cli.main(["status"]) == 0
        out = capsys.readouterr().out
        assert "better-telegram-mcp: configured" in out
        assert FAKE_TOKEN not in out

    def test_invalid_user_namespace_rc_2(self, capsys):
        assert cli.main(["logout", "--yes", "--user", "../x"]) == 2


# --- auth / login ---


class TestAuthArgs:
    """auth/login require exactly one of --bot-token / --phone."""

    @pytest.mark.parametrize("sub", ["auth", "login"])
    def test_no_flags_rc_2(self, sub):
        assert cli.main([sub]) == 2

    @pytest.mark.parametrize("sub", ["auth", "login"])
    def test_both_flags_rc_2(self, sub):
        assert cli.main([sub, "--bot-token", "x", "--phone", "+1"]) == 2

    def test_rejects_unknown_provider(self):
        assert cli.main(["auth", "notion", "--bot-token", "x"]) == 2


class TestAuthBot:
    """`auth --bot-token` validates via BotBackend then persists config."""

    def test_happy_path_persists_to_default_namespace(self, capsys):
        backend = _bot_backend()
        with patch("telegram.backends.bot_backend.BotBackend", return_value=backend):
            assert cli.main(["auth", "--bot-token", FAKE_TOKEN]) == 0

        backend.connect.assert_awaited_once()
        backend.disconnect.assert_awaited_once()
        assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
        captured = capsys.readouterr()
        assert "bot mode, namespace default" in captured.out
        assert "deprecated" not in captured.err
        assert FAKE_TOKEN not in captured.out + captured.err

    def test_provider_positional_accepted(self):
        with patch(
            "telegram.backends.bot_backend.BotBackend", return_value=_bot_backend()
        ):
            assert cli.main(["auth", "telegram", "--bot-token", FAKE_TOKEN]) == 0

    def test_user_flag_targets_namespace(self):
        with patch(
            "telegram.backends.bot_backend.BotBackend", return_value=_bot_backend()
        ):
            assert cli.main(["auth", "--bot-token", FAKE_TOKEN, "--user", "a"]) == 0
        assert _read_single_user_config("a") == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
        assert _read_single_user_config() is None

    def test_invalid_token_rc_1_and_not_persisted(self, capsys):
        backend = _bot_backend(Exception(f"Unauthorized for {FAKE_TOKEN}"))
        with patch("telegram.backends.bot_backend.BotBackend", return_value=backend):
            assert cli.main(["auth", "--bot-token", FAKE_TOKEN]) == 1

        assert _read_single_user_config() is None
        err = capsys.readouterr().err
        assert "Login failed" in err
        # The failure message is sanitized: the bot token is redacted.
        assert FAKE_TOKEN not in err

    def test_login_alias_warns_and_persists(self, capsys):
        with patch(
            "telegram.backends.bot_backend.BotBackend", return_value=_bot_backend()
        ):
            assert cli.main(["login", "--bot-token", FAKE_TOKEN]) == 0
        assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
        err = capsys.readouterr().err
        assert "deprecated" in err
        assert "auth" in err


class TestAuthPhone:
    """`auth --phone` is interactive tty-only; OTP + optional 2FA."""

    def _user_backend(self, sign_in) -> MagicMock:
        backend = MagicMock()
        backend.connect = AsyncMock()
        backend.send_code = AsyncMock()
        backend.sign_in = sign_in
        backend.disconnect = AsyncMock()
        return backend

    def test_non_tty_rc_1(self, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", _pipe_stdin(""))
        assert cli.main(["auth", "--phone", PHONE]) == 1
        assert "interactive terminal" in capsys.readouterr().err

    def test_tty_happy_path_persists_config_and_marker(self, capsys, monkeypatch):
        backend = self._user_backend(AsyncMock(return_value={"authenticated_as": "A"}))
        monkeypatch.setattr("sys.stdin", _tty_stdin("12345\n"))
        with patch(
            "telegram.backends.user_backend.UserBackend", return_value=backend
        ) as user_backend:
            assert cli.main(["auth", "--phone", PHONE]) == 0

        assert user_backend.call_args.kwargs == {"namespace": "default"}
        backend.send_code.assert_awaited_once_with(PHONE)
        backend.sign_in.assert_awaited_once_with(PHONE, "12345")
        backend.disconnect.assert_awaited_once()
        assert _read_single_user_config() == {"TELEGRAM_PHONE": PHONE}
        marker = plugin_store("tokens/app-identity", "default").load()
        assert marker is not None
        assert "api_id" in marker
        assert "Logged in as A" in capsys.readouterr().out

    def test_tty_2fa_reissues_sign_in_with_password(self, capsys, monkeypatch):
        backend = self._user_backend(
            AsyncMock(
                side_effect=[
                    Exception("2FA password required"),
                    {"authenticated_as": "B"},
                ]
            )
        )
        monkeypatch.setattr("sys.stdin", _tty_stdin("54321\n"))
        with (
            patch("getpass.getpass", return_value=TWO_FA_INPUT),
            patch("telegram.backends.user_backend.UserBackend", return_value=backend),
        ):
            assert cli.main(["auth", "--phone", PHONE, "--user", "b"]) == 0

        assert backend.sign_in.await_count == 2
        second = backend.sign_in.await_args_list[1]
        assert second.args == (PHONE, "54321")
        assert second.kwargs == {"password": TWO_FA_INPUT}
        assert _read_single_user_config("b") == {"TELEGRAM_PHONE": PHONE}
        assert "Logged in as B" in capsys.readouterr().out

    def test_tty_sign_in_failure_rc_1(self, capsys, monkeypatch):
        backend = self._user_backend(AsyncMock(side_effect=Exception("Invalid code")))
        monkeypatch.setattr("sys.stdin", _tty_stdin("00000\n"))
        with patch("telegram.backends.user_backend.UserBackend", return_value=backend):
            assert cli.main(["auth", "--phone", PHONE]) == 1

        assert _read_single_user_config() is None
        backend.disconnect.assert_awaited_once()
        assert "Login failed" in capsys.readouterr().err


# --- logout ---


def _seed_phone_login(namespace: str = "default"):
    """Create the config, session blob, marker and session file of a login."""
    _write_single_user_config({"TELEGRAM_PHONE": PHONE}, namespace)
    plugin_store("session", namespace).save({"session": "fake"})
    plugin_store("tokens/app-identity", namespace).save({"api_id": "1"})
    session_file = cli._settings_for(namespace).session_path
    session_file.parent.mkdir(parents=True, exist_ok=True)
    session_file.write_text("x")
    return session_file


def _user_backend_for_logout(log_out: AsyncMock) -> MagicMock:
    backend = MagicMock()
    backend.connect = AsyncMock()
    backend.log_out = log_out
    backend.disconnect = AsyncMock()
    return backend


class TestLogout:
    """`logout` revokes + deletes the session, config, and marker; idempotent."""

    def test_yes_clears_config_session_and_marker(self, capsys):
        session_file = _seed_phone_login()
        backend = _user_backend_for_logout(AsyncMock(return_value=True))
        with patch("telegram.backends.user_backend.UserBackend", return_value=backend):
            assert cli.main(["logout", "--yes"]) == 0

        backend.log_out.assert_awaited_once()
        assert not session_file.exists()
        assert _read_single_user_config() is None
        assert not plugin_store("session", "default").has_stored_blob()
        assert not plugin_store("tokens/app-identity", "default").has_stored_blob()
        out = capsys.readouterr().out
        for action in (
            "revoked Telegram session server-side",
            "deleted local session file",
            "cleared saved credentials",
            "cleared stored session blob",
            "cleared api identity marker",
        ):
            assert action in out
        assert out.rstrip().endswith("Logged out.")
        # Idempotent.
        assert cli.main(["logout", "--yes"]) == 0
        assert "Nothing to log out." in capsys.readouterr().out

    def test_user_flag_only_clears_that_namespace(self):
        _seed_phone_login("a")
        _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
        backend = _user_backend_for_logout(AsyncMock(return_value=True))
        with patch("telegram.backends.user_backend.UserBackend", return_value=backend):
            assert cli.main(["logout", "--yes", "--user", "a"]) == 0
        assert _read_single_user_config("a") is None
        assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}

    def test_revoke_failure_is_best_effort(self, capsys):
        session_file = _seed_phone_login()
        backend = _user_backend_for_logout(AsyncMock(side_effect=Exception("down")))
        with patch("telegram.backends.user_backend.UserBackend", return_value=backend):
            assert cli.main(["logout", "--yes"]) == 0

        assert not session_file.exists()
        captured = capsys.readouterr()
        assert "could not revoke" in captured.err
        assert "Logged out." in captured.out

    def test_nothing_to_log_out(self, capsys):
        assert cli.main(["logout", "--yes"]) == 0
        assert "Nothing to log out." in capsys.readouterr().out

    def test_non_interactive_without_yes_refuses(self, capsys, monkeypatch):
        _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
        monkeypatch.setattr("sys.stdin", _pipe_stdin(""))
        assert cli.main(["logout"]) == 1
        assert "without --yes" in capsys.readouterr().err
        assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}

    def test_interactive_confirm_yes(self, capsys, monkeypatch):
        _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
        monkeypatch.setattr("sys.stdin", _tty_stdin("y\n"))
        assert cli.main(["logout"]) == 0
        assert _read_single_user_config() is None

    def test_interactive_confirm_no_aborts(self, capsys, monkeypatch):
        _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
        monkeypatch.setattr("sys.stdin", _tty_stdin("n\n"))
        assert cli.main(["logout"]) == 1
        assert "aborted" in capsys.readouterr().err
        assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
