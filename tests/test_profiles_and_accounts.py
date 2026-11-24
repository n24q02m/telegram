"""Tests for Tier-2 profiles (--profile / TELEGRAM_PROFILE) and Tier-3 named accounts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

from hull_core.storage import data_dir

from telegram import cli as cli_mod
from telegram.auth.telegram_auth_provider import settings_for_namespace
from telegram.config import Settings
from telegram.credential_state import (
    _read_single_user_config,
    _write_single_user_config,
    list_accounts,
    remove_account,
    use_account,
)
from telegram.tool_session import load_settings


def test_profile_routes_data_dir_and_config_dir(monkeypatch):
    from hull_core.storage import PerPluginStore

    from telegram.transports.http import config_dir

    monkeypatch.setenv("TELEGRAM_PROFILE", "work")
    expected = data_dir("telegram")
    assert expected == Path.home() / ".n24q02m" / "telegram"
    assert Settings().data_dir == expected
    assert config_dir() == expected
    store = PerPluginStore("telegram")
    assert store.profile == "work"
    assert (
        store.cred_path
        == Path.home() / ".n24q02m" / "telegram" / "profiles" / "work" / "config.json"
    )


def test_cli_profile_flag_sets_and_restores_env(monkeypatch, capsys):
    monkeypatch.delenv("TELEGRAM_PROFILE", raising=False)
    monkeypatch.setattr(
        sys, "argv", ["telegram", "--profile", "work", "accounts", "list"]
    )
    assert cli_mod.main() == 0
    assert "TELEGRAM_PROFILE" not in __import__("os").environ

    monkeypatch.setenv("TELEGRAM_PROFILE", "orig")
    rc = cli_mod.main(["--profile=staging", "accounts", "list"])
    assert rc == 0
    assert __import__("os").environ["TELEGRAM_PROFILE"] == "orig"
    assert "No saved accounts." in capsys.readouterr().out


def test_cli_profile_errors(capsys):
    assert cli_mod.main(["--profile"]) == 2
    assert "--profile requires a value" in capsys.readouterr().err

    assert cli_mod.main(["--profile", "../escape"]) == 2
    assert capsys.readouterr().err


def test_named_accounts_crud_and_switching(monkeypatch):
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": "111:AAA"}, account="bot_a")
    _write_single_user_config(
        {"TELEGRAM_PHONE": "+84900000001", "session_name": "account-personal"},
        account="personal",
    )

    aliases, active = list_accounts()
    assert aliases == ["bot_a", "personal"]
    assert active == "personal"
    active_cfg = _read_single_user_config()
    assert active_cfg is not None
    assert active_cfg["TELEGRAM_PHONE"] == "+84900000001"
    bot_cfg = _read_single_user_config(account="bot_a")
    assert bot_cfg is not None
    assert bot_cfg["TELEGRAM_BOT_TOKEN"] == "111:AAA"

    use_account("bot_a")
    _, active = list_accounts()
    assert active == "bot_a"
    switched_cfg = _read_single_user_config()
    assert switched_cfg is not None
    assert switched_cfg["TELEGRAM_BOT_TOKEN"] == "111:AAA"

    # Explicit TELEGRAM_ACCOUNT overrides active account even if bot token env is set
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "999:ENV")
    monkeypatch.setenv("TELEGRAM_ACCOUNT", "personal")
    loaded = load_settings()
    assert loaded is not None
    assert loaded.mode == "user"
    assert loaded.phone == "+84900000001"
    assert loaded.session_name == "account-personal"
    assert loaded.session_path == loaded.data_dir / "account-personal.session"

    monkeypatch.delenv("TELEGRAM_ACCOUNT")
    assert remove_account("personal") is True
    assert remove_account("missing") is False
    aliases, active = list_accounts()
    assert aliases == ["bot_a"]
    assert active == "bot_a"


def test_namespace_scoped_named_account():
    _write_single_user_config(
        {"TELEGRAM_BOT_TOKEN": "222:NS"}, namespace="alice", account="team"
    )
    settings = settings_for_namespace("alice", account="team")
    assert settings is not None
    assert settings.bot_token == "222:NS"
    assert settings.data_dir.parts[-2:] == ("subs", "alice")


def test_cli_accounts_subcommands(capsys):
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": "111:AAA"}, account="alpha")
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": "222:BBB"}, account="beta")

    assert cli_mod.main(["accounts", "list"]) == 0
    out = capsys.readouterr().out
    assert "* beta" in out
    assert "  alpha" in out

    assert cli_mod.main(["accounts", "list", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"active": "beta", "accounts": ["alpha", "beta"]}

    assert cli_mod.main(["accounts", "use", "alpha"]) == 0
    assert "Active account set to 'alpha'" in capsys.readouterr().out

    assert cli_mod.main(["accounts", "use", "ghost"]) == 1
    assert "ghost" in capsys.readouterr().err

    assert cli_mod.main(["accounts", "remove", "beta"]) == 0
    assert "Removed account 'beta'" in capsys.readouterr().out

    assert cli_mod.main(["accounts", "remove", "ghost"]) == 1
    assert "unknown account 'ghost'" in capsys.readouterr().err


def test_auth_and_logout_with_account_flag(capsys, tmp_path):
    with patch("telegram.cli._verify_bot_token") as verify:
        verify.return_value = None
        assert (
            cli_mod.main(["auth", "--account", "work", "--bot-token", "123:WORKTOKEN"])
            == 0
        )

    aliases, active = list_accounts()
    assert aliases == ["work"]
    assert active == "work"

    # Session file isolated per account under Settings.data_dir
    sess = Settings().data_dir / "account-work.session"
    sess.parent.mkdir(parents=True, exist_ok=True)
    sess.write_bytes(b"fake")
    assert cli_mod.main(["logout", "--yes", "--account", "work"]) == 0
    aliases, _ = list_accounts()
    assert aliases == []


def test_account_flag_forwarded_to_tool_session():
    seen: list[tuple[str, str | None]] = []

    class FakeBackend:
        pass

    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def fake_conn(namespace="default", *, account=None):
        seen.append((namespace, account))
        yield FakeBackend()

    with (
        patch("telegram.tool_session.connected_backend", fake_conn),
        patch(
            "telegram.tools.dispatch.run_chat",
            new=AsyncMock(return_value={"chats": []}),
        ),
    ):
        rc = cli_mod.main(["chat", "list", "--account", "ops", "--json"])
    assert rc == 0
    assert seen == [("default", "ops")]
