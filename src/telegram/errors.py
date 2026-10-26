"""Error sanitization shared by the CLI, the backends and the tool layer.

Telegram bot tokens have the shape ``<bot_id>:<35+ char secret>`` and appear in
httpx request URLs (``https://api.telegram.org/bot<token>/<method>``), so they
can surface in transport-level exception messages. Every error string that is
logged or returned to a caller goes through :func:`redact_bot_token` (directly
or via :func:`_sanitize_error`) first.
"""

from __future__ import annotations

import re

_BOT_TOKEN_RE = re.compile(r"\d+:[A-Za-z0-9_-]{35,}")

_CAUSED_BY_RE = re.compile(r"\s*\(caused by \w+\)\s*$", re.IGNORECASE)
_ERROR_SIMPLIFICATIONS: list[tuple[re.Pattern[str], str]] = [
    (
        re.compile(r".*password.*required.*", re.IGNORECASE),
        "Two-factor authentication password is required.",
    ),
    (
        re.compile(r".*password.*invalid.*|.*invalid.*password.*", re.IGNORECASE),
        "Incorrect 2FA password. Please try again.",
    ),
    (
        re.compile(r".*phone.*code.*invalid.*|.*invalid.*code.*", re.IGNORECASE),
        "Invalid OTP code. Please check and try again.",
    ),
    (
        re.compile(r".*phone.*code.*expired.*|.*code.*expired.*", re.IGNORECASE),
        "OTP code has expired. Please request a new one.",
    ),
    (
        re.compile(r".*flood.*wait.*|.*too many.*", re.IGNORECASE),
        "Too many attempts. Please wait a moment and try again.",
    ),
]


def redact_bot_token(text: str) -> str:
    """Mask any Telegram bot token embedded in ``text``.

    The bot id is preserved for debuggability while the secret is replaced.
    """
    return _BOT_TOKEN_RE.sub(
        lambda m: m.group(0).split(":", 1)[0] + ":<redacted>", text
    )


def _sanitize_error(msg: str) -> str:
    """Simplify internal error messages to user-friendly text."""
    cleaned = redact_bot_token(_CAUSED_BY_RE.sub("", msg).strip())
    for pattern, friendly in _ERROR_SIMPLIFICATIONS:
        if pattern.match(cleaned):
            return friendly
    return cleaned


def _needs_2fa_password(error_msg: str) -> bool:
    """Check if the error indicates a 2FA password is required."""
    return any(
        kw in error_msg.lower() for kw in {"password", "2fa", "two-factor", "srp"}
    )
