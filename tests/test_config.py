from __future__ import annotations

import pytest

from telegram.config import Settings


def test_bot_mode_detection(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC-DEF")
    s = Settings()
    assert s.mode == "bot"
    assert s.bot_token == "123456:ABC-DEF"


def test_user_mode_detection(monkeypatch):
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abcdef123456")
    monkeypatch.setenv("TELEGRAM_PHONE", "+84912345678")
    s = Settings()
    assert s.mode == "user"


def test_user_mode_priority_over_bot(monkeypatch):
    """When both bot_token and user credentials are set, bot_token takes priority."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abcdef123456")
    monkeypatch.setenv("TELEGRAM_PHONE", "+84912345678")
    s = Settings()
    assert s.mode == "bot"


def test_no_credentials_starts_unconfigured(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_API_ID", raising=False)
    monkeypatch.delenv("TELEGRAM_API_HASH", raising=False)
    s = Settings()
    assert s.is_configured is False
    assert s.mode == "bot"  # default mode


def test_is_configured_bot(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    s = Settings()
    assert s.is_configured is True


def test_is_configured_user(monkeypatch):
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abcdef123456")
    monkeypatch.setenv("TELEGRAM_PHONE", "+84912345678")
    s = Settings()
    assert s.is_configured is True


def test_api_id_api_hash_without_phone_not_configured(monkeypatch):
    """api_id + api_hash without phone should NOT be configured (defaults exist)."""
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abcdef123456")
    s = Settings()
    assert s.is_configured is False
    assert s.mode == "bot"


def test_default_api_credentials():
    """api_id and api_hash have built-in defaults."""
    s = Settings()
    assert s.api_id == 37984984
    assert s.api_hash == "2f5f4c76c4de7c07302380c788390100"


# -----------------------------------------------------------------------
# Telegram api_id/api_hash BYO client resolver (bundled default + env pair +
# kill-switch)
# -----------------------------------------------------------------------

_TELEGRAM_CLIENT_ENV_VARS = (
    "TELEGRAM_API_ID",
    "TELEGRAM_API_HASH",
    "USE_BUNDLED_TELEGRAM_CLIENT",
)


def test_telegram_api_env_pair_beats_bundled(monkeypatch):
    """A full BYO env pair overrides the bundled default."""
    for v in _TELEGRAM_CLIENT_ENV_VARS:
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "my-hash")
    s = Settings()
    assert (s.api_id, s.api_hash) == (12345, "my-hash")


@pytest.mark.parametrize("set_id, set_hash", [(True, False), (False, True)])
def test_telegram_api_env_half_pair_fails_loud(monkeypatch, set_id, set_hash):
    """Setting only one half of the BYO pair raises instead of silently falling back."""
    for v in _TELEGRAM_CLIENT_ENV_VARS:
        monkeypatch.delenv(v, raising=False)
    if set_id:
        monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    if set_hash:
        monkeypatch.setenv("TELEGRAM_API_HASH", "my-hash")
    with pytest.raises(Exception, match="together"):
        Settings()


def test_telegram_api_kill_switch_fails_loud_without_override(monkeypatch):
    """USE_BUNDLED_TELEGRAM_CLIENT=false with no BYO pair raises instead of using bundled."""
    for v in _TELEGRAM_CLIENT_ENV_VARS:
        monkeypatch.delenv(v, raising=False)
    monkeypatch.setenv("USE_BUNDLED_TELEGRAM_CLIENT", "false")
    with pytest.raises(Exception, match="disables the bundled client"):
        Settings()


def test_default_data_dir(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    s = Settings()
    assert s.data_dir.name == ".telegram"


def test_custom_data_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    monkeypatch.setenv("TELEGRAM_DATA_DIR", str(tmp_path))
    s = Settings()
    assert s.data_dir == tmp_path


def test_session_path(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    s = Settings()
    assert str(s.session_path).endswith("default.session")


@pytest.mark.parametrize(
    "input_val, expected",
    [
        (None, None),
        ("\t", None),
        ("\n", None),
        ("\r\n", None),
        ("", None),
        ("   ", None),
        ("valid", "valid"),
        ("  valid  ", "  valid  "),
    ],
)
def test_empty_to_none(input_val, expected):
    from telegram.config import _empty_to_none

    assert _empty_to_none(input_val) == expected


def test_settings_hold_no_http_master_secret(tmp_path):
    """The pre-hull HTTP master secret is gone: hull owns all key material.

    Settings must not grow a ``secret`` field again, and building Settings
    must not create a ``.secret`` file in the data dir (hull's machine key
    lives there and a foreign one breaks the store).
    """
    s = Settings(data_dir=tmp_path)
    assert not hasattr(s, "secret")
    assert not (tmp_path / ".secret").exists()


def test_trusted_proxy_list():
    # Empty
    s = Settings(trusted_proxies=None)
    assert s.trusted_proxy_list == frozenset()

    s = Settings(trusted_proxies="")
    assert s.trusted_proxy_list == frozenset()

    # Populated
    s = Settings(trusted_proxies="127.0.0.1, 10.0.0.1 , , 192.168.1.1")
    assert s.trusted_proxy_list == frozenset({"127.0.0.1", "10.0.0.1", "192.168.1.1"})


def test_from_saved_config(tmp_path):
    config = {
        "TELEGRAM_BOT_TOKEN": "123:ABC",
        "TELEGRAM_PHONE": "+123456789",
        "TELEGRAM_API_ID": "98765",
        "TELEGRAM_API_HASH": "hash123",
    }
    s = Settings.from_saved_config(config)
    assert s.bot_token == "123:ABC"
    assert s.phone == "+123456789"
    assert s.api_id == 98765
    assert s.api_hash == "hash123"

    # Defaults
    s2 = Settings.from_saved_config({})
    assert s2.api_id == 37984984
    assert s2.api_hash == "2f5f4c76c4de7c07302380c788390100"

    # Field overrides (per-namespace session dir).
    s3 = Settings.from_saved_config({"TELEGRAM_PHONE": "+1"}, data_dir=tmp_path)
    assert s3.session_path == tmp_path / "default.session"
