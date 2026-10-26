"""Credential field names and saved-session discovery."""

from __future__ import annotations

# Kept at the pre-rename value on purpose: it is the key of this server's
# entry in the legacy shared ``config.enc`` (written by releases before the
# hull migration). ``credential_state`` reads and then deletes exactly this
# entry once; renaming it would orphan existing saved configs.
SERVER_NAME = "better-telegram-mcp"
REQUIRED_FIELDS_BOT = ["TELEGRAM_BOT_TOKEN"]
REQUIRED_FIELDS_USER = ["TELEGRAM_PHONE"]
ALL_POSSIBLE_FIELDS = [
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_PHONE",
]


def check_saved_sessions() -> bool:
    """Check for a saved Telethon session from a previous authentication.

    Looks for ``*.session`` files in the data dir the server itself uses:
    ``TELEGRAM_DATA_DIR`` when set, else the default ``~/.telegram/`` (moved
    from the legacy ``~/.better-telegram-mcp/`` on first use).

    Returns:
        True if at least one saved session exists, False otherwise.
    """
    from .config import Settings

    data_dir = Settings().data_dir
    if not data_dir.exists():
        return False
    sessions = list(data_dir.glob("*.session"))
    return len(sessions) > 0
