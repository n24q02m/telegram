"""Tests for error sanitisation, saved-session detection and saved-config settings."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from telegram.config import Settings
from telegram.errors import (
    _needs_2fa_password,
    _sanitize_error,
    redact_bot_token,
)

# Token-shaped value (bot id + 35-char secret) assembled from parts so no
# scanner-matchable literal exists in source. Not a real credential.
_FAKE_SECRET = "AAE" + ("x" * 32)
_FAKE_TOKEN = "123456789:" + _FAKE_SECRET


def test_redact_bot_token_in_url():
    text = f"error posting https://api.telegram.org/bot{_FAKE_TOKEN}/getMe"
    redacted = redact_bot_token(text)
    assert _FAKE_SECRET not in redacted
    assert "123456789:<redacted>" in redacted


def test_redact_bot_token_standalone():
    redacted = redact_bot_token(f"token {_FAKE_TOKEN} leaked into logs")
    assert _FAKE_SECRET not in redacted


def test_redact_bot_token_noop_when_absent():
    text = "Bad Request: chat not found"
    assert redact_bot_token(text) == text


def test_sanitize_error_redacts_bot_token():
    # _sanitize_error feeds logs/return values, so it must also strip tokens.
    redacted = _sanitize_error(f"Connection failed using {_FAKE_TOKEN}")
    assert _FAKE_SECRET not in redacted


# --- Settings.from_saved_config ---


def test_from_saved_config_bot_mode():
    """Create Settings from saved config with bot token."""
    config = {"TELEGRAM_BOT_TOKEN": "123456:ABC-DEF"}
    s = Settings.from_saved_config(config)
    assert s.bot_token == "123456:ABC-DEF"
    assert s.mode == "bot"
    assert s.is_configured is True


def test_from_saved_config_user_mode():
    """Create Settings from saved config with user credentials."""
    config = {
        "TELEGRAM_API_ID": "12345",
        "TELEGRAM_API_HASH": "abcdef123456",
        "TELEGRAM_PHONE": "+84912345678",
    }
    s = Settings.from_saved_config(config)
    assert s.api_id == 12345
    assert s.api_hash == "abcdef123456"
    assert s.phone == "+84912345678"
    assert s.mode == "user"
    assert s.is_configured is True


def test_from_saved_config_empty_values():
    """Empty values in saved config should result in unconfigured state."""
    config = {"TELEGRAM_BOT_TOKEN": ""}
    s = Settings.from_saved_config(config)
    assert s.bot_token is None  # _empty_to_none normalizes it
    assert s.is_configured is False


def test_from_saved_config_missing_keys():
    """Missing keys should use built-in defaults for api_id/api_hash."""
    config = {}
    s = Settings.from_saved_config(config)
    assert s.bot_token is None
    assert s.api_id == 37984984  # built-in default
    assert s.api_hash == "2f5f4c76c4de7c07302380c788390100"  # built-in default
    assert s.is_configured is False  # no phone, no bot_token


# --- check_saved_sessions ---


def test_check_saved_sessions_no_dir(tmp_path):
    """Returns False when data directory does not exist."""
    from telegram.sessions import check_saved_sessions

    with patch(
        "pathlib.Path.home",
        return_value=tmp_path / "nonexistent",
    ):
        assert check_saved_sessions() is False


def test_check_saved_sessions_empty_dir(tmp_path):
    """Returns False when data directory exists but has no session files."""
    from telegram.sessions import check_saved_sessions

    data_dir = tmp_path / ".telegram"
    data_dir.mkdir()

    with patch(
        "pathlib.Path.home",
        return_value=tmp_path,
    ):
        assert check_saved_sessions() is False


def test_check_saved_sessions_with_sessions(tmp_path):
    """Returns True when session files exist."""
    from telegram.sessions import check_saved_sessions

    data_dir = tmp_path / ".telegram"
    data_dir.mkdir()
    (data_dir / "user.session").write_text("session_data")

    with patch(
        "pathlib.Path.home",
        return_value=tmp_path,
    ):
        assert check_saved_sessions() is True


# --- Lifespan integration ---


@pytest.mark.asyncio
async def test_lifespan_tries_credential_state_when_unconfigured():
    """Lifespan should use resolve_credential_state when no env vars are set."""
    import telegram.server as srv
    from telegram.credential_state import CredentialState
    from telegram.server import _lifespan, mcp

    mock_bot = AsyncMock()
    mock_bot.is_authorized = AsyncMock(return_value=True)

    # Bare Settings() -> unconfigured; explicit from_saved_config -> configured.
    unconfigured_settings = MagicMock(is_configured=False)
    configured_settings = MagicMock(
        is_configured=True,
        mode="bot",
        bot_token="saved:TOKEN",
    )

    def mock_resolve():
        return CredentialState.CONFIGURED

    with (
        patch.object(srv, "Settings") as mock_settings_cls,
        patch(
            "telegram.credential_state.resolve_credential_state",
            side_effect=mock_resolve,
        ),
        patch(
            "telegram.credential_state._read_single_user_config",
            return_value={"TELEGRAM_BOT_TOKEN": "saved:TOKEN"},
        ),
        patch.dict(
            "sys.modules",
            {
                "telegram.backends.bot_backend": type(
                    "module", (), {"BotBackend": MagicMock(return_value=mock_bot)}
                )()
            },
        ),
    ):
        mock_settings_cls.return_value = unconfigured_settings
        mock_settings_cls.from_saved_config.return_value = configured_settings

        async with _lifespan(mcp):
            assert srv._backend is mock_bot
            mock_bot.connect.assert_awaited_once()

        mock_bot.disconnect.assert_awaited_once()


@pytest.mark.asyncio
async def test_lifespan_falls_back_to_unconfigured_when_no_credentials():
    """Lifespan should fall back to unconfigured state when no credentials found."""
    import telegram.server as srv
    from telegram.credential_state import CredentialState
    from telegram.server import _lifespan, mcp

    def mock_resolve():
        return CredentialState.AWAITING_SETUP

    with (
        patch.object(srv, "Settings", return_value=MagicMock(is_configured=False)),
        patch(
            "telegram.credential_state.resolve_credential_state",
            side_effect=mock_resolve,
        ),
    ):
        async with _lifespan(mcp):
            assert srv._unconfigured is True

        assert srv._unconfigured is False


# --- _sanitize_error ---


class TestSanitizeError:
    def test_password_required(self):
        assert _sanitize_error("Password is required for this account") == (
            "Two-factor authentication password is required."
        )

    def test_password_invalid(self):
        assert _sanitize_error("The password is invalid") == (
            "Incorrect 2FA password. Please try again."
        )

    def test_invalid_password(self):
        assert _sanitize_error("Invalid password provided") == (
            "Incorrect 2FA password. Please try again."
        )

    def test_phone_code_invalid(self):
        assert _sanitize_error("Phone code is invalid") == (
            "Invalid OTP code. Please check and try again."
        )

    def test_code_expired(self):
        assert _sanitize_error("Phone code has expired") == (
            "OTP code has expired. Please request a new one."
        )

    def test_flood_wait(self):
        assert _sanitize_error("Flood wait of 300 seconds") == (
            "Too many attempts. Please wait a moment and try again."
        )

    def test_too_many(self):
        assert _sanitize_error("Too many requests") == (
            "Too many attempts. Please wait a moment and try again."
        )

    def test_strips_caused_by_suffix(self):
        result = _sanitize_error("Something happened (caused by SomeError)")
        assert result == "Something happened"

    def test_passthrough_unknown_error(self):
        assert _sanitize_error("Some unknown error") == "Some unknown error"

    def test_sanitize_error_empty(self):
        assert _sanitize_error("") == ""

    def test_sanitize_error_whitespace(self):
        assert _sanitize_error("   ") == ""

    def test_sanitize_error_long_string(self):
        long_msg = "A" * 1000
        assert _sanitize_error(long_msg) == long_msg

    def test_sanitize_error_special_chars(self):
        msg = "Error! @#$%^&*()_+"
        assert _sanitize_error(msg) == msg

    def test_sanitize_error_caused_by_variations(self):
        assert _sanitize_error("Fail (CAUSED BY Error)") == "Fail"
        assert _sanitize_error("Fail(caused by Error) ") == "Fail"
        assert _sanitize_error("Fail (caused by 123)") == "Fail"


# --- _needs_2fa_password ---


class TestNeeds2faPassword:
    @pytest.mark.parametrize(
        "error_msg,expected",
        [
            ("SESSION_PASSWORD_NEEDED", True),
            ("SessionPasswordNeeded", True),
            ("password required", True),
            ("2fa authentication required", True),
            ("Two-factor auth needed", True),
            ("SRP protocol required", True),
            ("Needs TWO-FACTOR", True),
            ("Invalid phone number", False),
            ("CODE_INVALID", False),
            ("", False),
        ],
    )
    def test_needs_2fa_password(self, error_msg: str, expected: bool):
        assert _needs_2fa_password(error_msg) is expected
