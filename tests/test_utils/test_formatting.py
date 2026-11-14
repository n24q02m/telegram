from __future__ import annotations

from telegram.backends.base import ModeError
from telegram.backends.security import SecurityError
from telegram.utils.formatting import err, ok, safe_error


def test_ok_basic_passthrough():
    data = {"key": "value", "number": 42}
    assert ok(data) == data


def test_ok_unicode_passthrough():
    data = {"emoji": "😊", "cyrillic": "Привет", "chinese": "你好"}
    result = ok(data)
    assert result["emoji"] == "😊"
    assert result["cyrillic"] == "Привет"
    assert result["chinese"] == "你好"


def test_ok_empty_dict():
    assert ok({}) == {}


def test_ok_nested_mixed_types():
    data = {
        "str": "text",
        "nested": {"val": 1},
        "list": [1, {"a": 1}],
    }
    result = ok(data)
    assert result is data
    assert result["nested"]["val"] == 1
    assert result["list"][1] == {"a": 1}


def test_err_basic():
    message = "Something went wrong"
    result = err(message)
    assert result == {"error": message}


def test_err_unicode():
    message = "Ошибка: ❌"
    result = err(message)
    assert result == {"error": message}


def test_safe_error_allowed_exceptions():
    # Exceptions that should expose their actual message
    allowed_exceptions = [
        (
            ModeError("user"),
            "This action requires user mode. Set TELEGRAM_API_ID + TELEGRAM_API_HASH + TELEGRAM_PHONE.",
        ),
        (ModeError("bot"), "This action requires bot mode."),
        (SecurityError("Security error message"), "Security error message"),
        (ValueError("Value error message"), "Value error message"),
        (FileNotFoundError("File not found message"), "File not found message"),
    ]

    for exc, expected_msg in allowed_exceptions:
        result = safe_error(exc)
        assert result == {"error": expected_msg}


def test_safe_error_generic_exceptions():
    # Exceptions that should be sanitized to avoid leaking internals
    generic_exceptions = [
        KeyError("internal_key"),
        TypeError("bad type"),
        RuntimeError("system crash"),
        Exception("generic fail"),
    ]

    for exc in generic_exceptions:
        result = safe_error(exc)

        # Format should be: "{ExceptionName}: Operation failed. Check server logs for details."
        expected_msg = (
            f"{type(exc).__name__}: Operation failed. Check server logs for details."
        )
        assert result == {"error": expected_msg}

        # Ensure internal details are NOT leaked
        assert str(exc) not in result["error"]


def test_safe_error_empty_message():
    # Allowed exception with empty message
    exc = ValueError("")
    result = safe_error(exc)
    assert result == {"error": ""}

    # Generic exception with empty message
    exc = Exception("")
    result = safe_error(exc)
    assert result == {
        "error": "Exception: Operation failed. Check server logs for details."
    }


def test_safe_error_subclasses_allowed():
    class CustomValueError(ValueError):
        pass

    exc = CustomValueError("custom message")
    result = safe_error(exc)
    assert result == {"error": "custom message"}


def test_safe_error_disallowed_oserror():
    # PermissionError is an OSError but not FileNotFoundError
    exc = PermissionError("access denied")
    result = safe_error(exc)
    assert (
        result["error"]
        == "PermissionError: Operation failed. Check server logs for details."
    )
    assert "access denied" not in result["error"]


def test_safe_error_base_exception():
    # Although the type hint says Exception, in practice someone might pass BaseException
    # safe_error should still handle it if it makes it through
    exc = KeyboardInterrupt("stop")
    # KeyboardInterrupt is NOT a subclass of Exception, it's a sibling.
    # The code uses isinstance(e, (...)) and it doesn't match, so it falls through.
    result = safe_error(exc)
    assert (
        result["error"]
        == "KeyboardInterrupt: Operation failed. Check server logs for details."
    )
    assert "stop" not in result["error"]


def test_safe_error_surfaces_bot_api_refusal():
    # The Bot API description is what the caller can act on ("chat not found",
    # "bot was blocked by the user"); the server log is out of reach over HTTP.
    from telegram.backends.bot_backend import TelegramAPIError

    result = safe_error(TelegramAPIError("Bad Request: chat not found", 400))
    assert result == {"error": "Telegram API: Bad Request: chat not found"}


def test_safe_error_bot_api_refusal_keeps_the_token_redacted():
    from telegram.backends.bot_backend import TelegramAPIError

    token = "123456789:" + "A" * 35
    result = safe_error(
        TelegramAPIError(f"request to https://api.telegram.org/bot{token}/getMe failed")
    )
    assert "A" * 35 not in result["error"]
    assert "123456789:<redacted>" in result["error"]
