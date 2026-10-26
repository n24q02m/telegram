"""Saved credentials (hull PerPluginStore) and the startup credential check.

Everything runs against the real encrypted store under the fake home of the
autouse ``_isolate_per_plugin_home`` fixture; nothing is mocked at the
storage layer, so these tests exercise the same files the CLI writes.
"""

from __future__ import annotations

import pytest
from hull_core.storage import MachineKeyError, PerPluginStore, data_dir
from legacy_store import legacy_path, read_legacy_entry, write_legacy_store

import telegram.credential_state as cs
from telegram.config import QUARANTINED_SECRET_NAME
from telegram.credential_state import (
    DEFAULT_NAMESPACE,
    PLUGIN_NAME,
    CredentialState,
    _delete_single_user_config,
    _read_single_user_config,
    _write_single_user_config,
    get_state,
    namespace_leaf,
    plugin_store,
    resolve_credential_state,
)
from telegram.sessions import SERVER_NAME

FAKE_TOKEN = "123456:" + "T" * 35
OTHER_SERVER = "better-notion-mcp"


@pytest.fixture(autouse=True)
def _reset_state():
    cs._state = CredentialState.AWAITING_SETUP
    yield
    cs._state = CredentialState.AWAITING_SETUP


def _config_file():
    return data_dir(PLUGIN_NAME) / "config.json"


# --- layout ---


def test_state_values():
    assert {s.value for s in CredentialState} == {"awaiting_setup", "configured"}
    assert get_state() is CredentialState.AWAITING_SETUP


def test_namespace_leaf_default_is_flat():
    assert namespace_leaf(DEFAULT_NAMESPACE, "config") == "config"
    assert namespace_leaf("alice", "config") == "subs/alice/config"


@pytest.mark.parametrize("bad", ["../x", "a/b", ""])
def test_namespace_leaf_rejects_unsafe(bad):
    with pytest.raises(ValueError):
        namespace_leaf(bad, "config")


def test_default_config_is_the_builtin_cli_blob():
    """The default namespace writes the blob hull's config/status read."""
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
    assert _config_file().exists()
    assert PerPluginStore(PLUGIN_NAME).load() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    # Encrypted at rest.
    assert FAKE_TOKEN.encode() not in _config_file().read_bytes()


def test_namespaces_are_isolated():
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}, "a")
    assert _read_single_user_config("a") == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    assert _read_single_user_config("b") is None
    assert _read_single_user_config() is None
    assert not _config_file().exists()


def test_delete_clears_only_that_namespace():
    _write_single_user_config({"TELEGRAM_PHONE": "+10000000000"})
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}, "a")
    _delete_single_user_config()
    assert _read_single_user_config() is None
    assert _read_single_user_config("a") == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    _delete_single_user_config("a")
    assert _read_single_user_config("a") is None


# --- legacy mcp-core config.enc migration ---


def test_legacy_entry_is_migrated_once_and_only_that_entry_deleted():
    write_legacy_store(
        {
            SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN},
            OTHER_SERVER: {"NOTION_TOKEN": "keep-me"},
        }
    )

    assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}

    assert PerPluginStore(PLUGIN_NAME).load() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    assert read_legacy_entry(SERVER_NAME) is None
    assert read_legacy_entry(OTHER_SERVER) == {"NOTION_TOKEN": "keep-me"}
    # Second read comes from the store, not the (now absent) legacy entry.
    assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}


def test_legacy_file_removed_when_telegram_was_the_only_entry():
    write_legacy_store({SERVER_NAME: {"TELEGRAM_PHONE": "+10000000000"}})
    assert _read_single_user_config() == {"TELEGRAM_PHONE": "+10000000000"}
    assert not legacy_path().exists()


def test_store_wins_over_legacy_entry():
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})
    write_legacy_store({SERVER_NAME: {"TELEGRAM_PHONE": "+19999999999"}})
    assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    # Not migrated, not deleted: the store already had credentials.
    assert read_legacy_entry(SERVER_NAME) == {"TELEGRAM_PHONE": "+19999999999"}


def test_legacy_entry_is_not_migrated_into_other_namespaces():
    write_legacy_store({SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}})
    assert _read_single_user_config("a") is None
    assert read_legacy_entry(SERVER_NAME) == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}


def test_delete_default_also_drops_unmigrated_legacy_entry():
    write_legacy_store(
        {
            SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN},
            OTHER_SERVER: {"NOTION_TOKEN": "keep-me"},
        }
    )
    _delete_single_user_config()
    assert read_legacy_entry(SERVER_NAME) is None
    assert read_legacy_entry(OTHER_SERVER) == {"NOTION_TOKEN": "keep-me"}
    assert _read_single_user_config() is None


def test_ensure_settings_first_call_migrates_legacy_entry():
    """Server startup loads the legacy entry, persists it, drops only it."""
    from telegram.server import _ensure_settings

    write_legacy_store(
        {
            SERVER_NAME: {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN},
            OTHER_SERVER: {"NOTION_TOKEN": "keep-me"},
        }
    )

    settings = _ensure_settings()

    assert settings.mode == "bot"
    assert settings.bot_token == FAKE_TOKEN
    assert PerPluginStore(PLUGIN_NAME).load() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}
    assert read_legacy_entry(SERVER_NAME) is None
    assert read_legacy_entry(OTHER_SERVER) == {"NOTION_TOKEN": "keep-me"}


# --- pre-hull .secret quarantine ---


def test_plugin_store_quarantines_foreign_secret():
    home = data_dir(PLUGIN_NAME)
    home.mkdir(parents=True, exist_ok=True)
    old = b"ab" * 32  # 64 hex chars: the pre-hull HTTP master secret
    (home / ".secret").write_bytes(old)

    _write_single_user_config({"TELEGRAM_BOT_TOKEN": FAKE_TOKEN})

    assert (home / QUARANTINED_SECRET_NAME).read_bytes() == old
    assert (home / ".secret").stat().st_size == 32
    assert _read_single_user_config() == {"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}


def test_foreign_secret_without_quarantine_breaks_hull():
    """Why the quarantine exists: hull refuses a non-32-byte machine key."""
    home = data_dir(PLUGIN_NAME)
    home.mkdir(parents=True, exist_ok=True)
    (home / ".secret").write_bytes(b"ab" * 32)
    with pytest.raises(MachineKeyError):
        PerPluginStore(PLUGIN_NAME).save({"x": "y"})


def test_plugin_store_returns_namespaced_store():
    store = plugin_store("config", "a")
    store.save({"TELEGRAM_PHONE": "+10000000000"})
    assert store.cred_path.parts[-3:-1] == ("subs", "a")


# --- resolve_credential_state ---


def test_resolve_bot_token_from_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", FAKE_TOKEN)
    assert resolve_credential_state() is CredentialState.CONFIGURED
    assert get_state() is CredentialState.CONFIGURED


def test_resolve_phone_from_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_PHONE", "+10000000000")
    assert resolve_credential_state() is CredentialState.CONFIGURED


@pytest.mark.parametrize(
    "saved", [{"TELEGRAM_BOT_TOKEN": FAKE_TOKEN}, {"TELEGRAM_PHONE": "+10000000000"}]
)
def test_resolve_from_saved_config_without_env_injection(saved):
    import os

    _write_single_user_config(saved)
    assert resolve_credential_state() is CredentialState.CONFIGURED
    assert os.environ.get("TELEGRAM_BOT_TOKEN") is None
    assert os.environ.get("TELEGRAM_PHONE") is None


def test_resolve_saved_config_without_credential_keys():
    _write_single_user_config({"TELEGRAM_SESSION_NAME": "x"})
    assert resolve_credential_state() is CredentialState.AWAITING_SETUP


def test_resolve_unreadable_store_falls_through(monkeypatch):
    def _boom(namespace=DEFAULT_NAMESPACE):
        raise MachineKeyError("unreadable")

    monkeypatch.setattr(cs, "_read_single_user_config", _boom)
    assert resolve_credential_state() is CredentialState.AWAITING_SETUP


def test_resolve_saved_sessions_only(monkeypatch):
    monkeypatch.setattr(cs, "check_saved_sessions", lambda: True)
    assert resolve_credential_state() is CredentialState.AWAITING_SETUP


def test_resolve_nothing():
    assert resolve_credential_state() is CredentialState.AWAITING_SETUP
