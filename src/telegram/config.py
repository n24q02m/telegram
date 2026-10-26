from __future__ import annotations

import functools
import os
from pathlib import Path
from typing import Literal

from hull_core.auth import BundledClientSpec, resolve_bundled_client
from loguru import logger
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


def _empty_to_none(v: str | None) -> str | None:
    """Treat empty or whitespace-only string as None (plugin.json sets env vars to '' by default)."""
    if not v or not v.strip():
        return None
    return v


# Default data dir (Telethon ``*.session`` files). Renamed with the project;
# the pre-rename directory is moved over once on first use.
# ``TELEGRAM_DATA_DIR`` bypasses all of this. The same ``~/.telegram/`` is also
# hull's ``PerPluginStore("telegram")`` data dir (``config.json``,
# ``tokens/``, ``subs/<ns>/`` and the 32-byte machine key ``.secret``); hull
# reads the older ``~/.telegram-mcp/`` layout itself as a legacy location.
DATA_DIR_NAME = ".telegram"
LEGACY_DATA_DIR_NAME = ".better-telegram-mcp"

# Releases before the hull migration kept a 64-hex-character HTTP-mode master
# secret at ``<data dir>/.secret``. hull uses that exact path for its 32-byte
# machine key and refuses (``MachineKeyError``) to touch a foreign one, so the
# old file is renamed aside once. Nothing reads the renamed file: it only
# protected the removed relay-era ``user_sessions/`` store.
_MACHINE_KEY_FILE = ".secret"
_MACHINE_KEY_LEN = 32
QUARANTINED_SECRET_NAME = ".secret.legacy-credential-store"


def quarantine_foreign_machine_key() -> Path | None:
    """Move a pre-hull ``.secret`` out of hull's machine-key path.

    Only a ``.secret`` that is not exactly 32 bytes is moved; a 32-byte file
    is (or could be) hull's own key and is left alone. The file is renamed,
    never read, logged or deleted. Returns the new path when a file was moved,
    else ``None``.
    """
    from hull_core.storage import data_dir

    secret = data_dir("telegram") / _MACHINE_KEY_FILE
    try:
        size = secret.stat().st_size
    except FileNotFoundError:
        return None
    if size == _MACHINE_KEY_LEN:
        return None
    target = secret.with_name(QUARANTINED_SECRET_NAME)
    n = 0
    while target.exists():
        n += 1
        target = secret.with_name(f"{QUARANTINED_SECRET_NAME}.{n}")
    os.replace(secret, target)
    logger.warning(
        "Moved pre-hull {} ({} bytes, not a hull machine key) to {}.",
        secret,
        size,
        target,
    )
    return target


def _holds_server_state(directory: Path) -> bool:
    """True if ``directory`` contains files this server writes."""
    return (
        (directory / ".secret").exists()
        or (directory / "user_sessions").exists()
        or any(directory.glob("*.session"))
    )


def resolve_default_data_dir() -> Path:
    """Return the default data dir, moving the legacy one over once.

    - ``~/.telegram`` exists and holds server state (or no legacy dir
      exists): use it.
    - Only ``~/.better-telegram-mcp`` exists: rename it to ``~/.telegram``,
      read back that the move landed, and use the new path. If the rename
      fails (for example a file is still open by an old process on Windows)
      or the readback does not match, keep reading the legacy dir.
    - Both exist but ``~/.telegram`` holds none of this server's files (an
      unrelated directory): keep the legacy dir rather than strand its
      sessions.

    Whenever ``~/.telegram`` is the result, a pre-hull ``.secret`` in it is
    moved aside (:func:`quarantine_foreign_machine_key`).
    """
    home = Path.home()
    target = home / DATA_DIR_NAME
    legacy = home / LEGACY_DATA_DIR_NAME

    if not legacy.exists():
        quarantine_foreign_machine_key()
        return target
    if target.exists():
        if _holds_server_state(target):
            logger.warning(
                "Both {} and legacy {} exist; using {}. The legacy dir was left "
                "untouched -- remove it once nothing reads it.",
                target,
                legacy,
                target,
            )
            quarantine_foreign_machine_key()
            return target
        logger.warning(
            "{} exists but holds no telegram server state; still reading legacy "
            "{}. Set TELEGRAM_DATA_DIR to choose explicitly.",
            target,
            legacy,
        )
        return legacy

    try:
        os.rename(legacy, target)
    except OSError as exc:
        logger.warning(
            "Could not move legacy data dir {} to {} ({}); reading the legacy "
            "dir for now.",
            legacy,
            target,
            exc,
        )
        return legacy

    if target.is_dir() and not legacy.exists():
        logger.info("Moved data dir {} -> {}", legacy, target)
        quarantine_foreign_machine_key()
        return target
    logger.warning(
        "Data dir move {} -> {} did not read back as expected; reading the legacy dir.",
        legacy,
        target,
    )
    return legacy if legacy.exists() else target


# Telegram api_id/api_hash identity (BYO resolver chain: CLI (unused here) >
# env pair > bundled default, unless USE_BUNDLED_TELEGRAM_CLIENT explicitly
# disables it). This is Telegram's own public desktop app pair
# (https://core.telegram.org/api/obtaining_api_id) -- hardcoding it here is
# safe and gives users zero-config user mode.
_BUNDLED_TELEGRAM_API_ID = "37984984"
_BUNDLED_TELEGRAM_API_HASH = "2f5f4c76c4de7c07302380c788390100"  # gitleaks:allow
_TELEGRAM_CLIENT_SPEC = BundledClientSpec(
    provider="telegram",
    env_id="TELEGRAM_API_ID",
    env_secret="TELEGRAM_API_HASH",
    bundled_id=_BUNDLED_TELEGRAM_API_ID,
    bundled_secret=_BUNDLED_TELEGRAM_API_HASH,
    use_bundled_env="USE_BUNDLED_TELEGRAM_CLIENT",
)


class Settings(BaseSettings):
    model_config = {"env_prefix": "TELEGRAM_", "extra": "ignore"}

    # Bot mode
    bot_token: str | None = None

    # User mode (app-level credentials with built-in defaults, like Google Drive client_id/secret)
    api_id: int | None = Field(
        default_factory=lambda: int(
            resolve_bundled_client(_TELEGRAM_CLIENT_SPEC).client_id
        )
    )
    api_hash: str | None = Field(
        default_factory=lambda: (
            resolve_bundled_client(_TELEGRAM_CLIENT_SPEC).client_secret
        )
    )
    phone: str | None = None
    session_name: str = "default"

    # Data
    data_dir: Path = Field(default_factory=resolve_default_data_dir)

    # Security
    trusted_proxies: str | None = None

    # Runtime (derived)
    mode: Literal["bot", "user"] = "bot"

    @functools.cached_property
    def trusted_proxy_list(self) -> frozenset[str]:
        """⚡ Bolt: Memoize proxy parsing and convert to frozenset for O(1) lookups."""
        if not self.trusted_proxies:
            return frozenset()
        return frozenset(
            p.strip() for p in self.trusted_proxies.split(",") if p.strip()
        )

    @model_validator(mode="after")
    def _detect_mode(self) -> Settings:
        # Normalize empty strings to None (plugin.json sets env vars to "" by default)
        self.bot_token = _empty_to_none(self.bot_token)
        self.api_hash = _empty_to_none(self.api_hash)
        self.phone = _empty_to_none(self.phone)

        has_bot = self.bot_token is not None
        # User mode requires phone (api_id/api_hash have built-in defaults)
        has_user = (
            self.api_id is not None
            and self.api_hash is not None
            and self.phone is not None
        )

        if has_bot:
            self.mode = "bot"
        elif has_user:
            self.mode = "user"
        # No credentials: keep default mode="bot", server starts in unconfigured state
        return self

    @property
    def is_configured(self) -> bool:
        """Check if any Telegram credentials are provided."""
        return self.bot_token is not None or (
            self.api_id is not None
            and self.api_hash is not None
            and self.phone is not None
        )

    @classmethod
    def from_saved_config(cls, config: dict[str, str], **overrides: object) -> Settings:
        """Create Settings from a saved credential dict (written by ``telegram auth``).

        Args:
            config: Dict with keys like TELEGRAM_BOT_TOKEN, TELEGRAM_PHONE,
                TELEGRAM_API_ID. API_ID and API_HASH use the bundled defaults
                unless the dict sets them.
            overrides: Extra Settings fields (e.g. ``data_dir`` for a
                per-namespace session directory).

        Returns:
            A configured Settings instance.
        """
        kwargs: dict[str, object] = {
            "bot_token": config.get("TELEGRAM_BOT_TOKEN"),
            "phone": config.get("TELEGRAM_PHONE"),
        }
        # Only override the bundled defaults when the saved config sets them
        if config.get("TELEGRAM_API_ID"):
            kwargs["api_id"] = int(config["TELEGRAM_API_ID"])
        if config.get("TELEGRAM_API_HASH"):
            kwargs["api_hash"] = config["TELEGRAM_API_HASH"]
        kwargs.update(overrides)
        return cls(**kwargs)

    @property
    def session_path(self) -> Path:
        return self.data_dir / f"{self.session_name}.session"
