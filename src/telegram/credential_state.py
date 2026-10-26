"""Saved Telegram credentials and the startup credential check.

Credentials written by ``telegram auth`` live in hull's encrypted
``PerPluginStore("telegram")`` (machine key ``~/.telegram/.secret``):

- namespace ``default`` (stdio, ``no-auth`` and ``token`` HTTP modes):
  ``~/.telegram/config.json``, the same blob the ``telegram config`` /
  ``status`` / ``doctor`` built-ins read.
- any other namespace (hull ``multi`` mode, ``telegram auth --user <ns>``):
  ``~/.telegram/subs/<ns>/config.json``.

Before the hull migration the config lived in mcp-core's shared
``config.enc`` under :data:`~telegram.sessions.SERVER_NAME`. The first read
that finds nothing in the store migrates that entry: it is saved into the store
and then only that entry is deleted from ``config.enc``.
"""

from __future__ import annotations

import os
from enum import Enum
from typing import Any

from hull_core.storage import (
    PerPluginStore,
    delete_legacy_config,
    read_legacy_config,
    validate_sub,
)
from loguru import logger

from .config import quarantine_foreign_machine_key
from .sessions import SERVER_NAME, check_saved_sessions

# Storage slug, shared with the CLI built-ins (``build_cli(plugin_name=...)``),
# the Telethon StringSession store and the api-identity marker.
PLUGIN_NAME = "telegram"
DEFAULT_NAMESPACE = "default"


def namespace_leaf(namespace: str, leaf: str) -> str:
    """PerPluginStore ``sub_key`` for ``leaf`` in ``namespace``.

    ``default`` keeps the flat single-user layout (``config``, ``session``,
    ``tokens/<name>``); any other namespace is nested under ``subs/<ns>/``.
    Both use the machine key, so no ``CREDENTIAL_SECRET`` is needed.
    """
    if namespace == DEFAULT_NAMESPACE:
        return leaf
    return f"subs/{validate_sub(namespace)}/{leaf}"


def plugin_store(leaf: str, namespace: str = DEFAULT_NAMESPACE) -> PerPluginStore:
    """The telegram PerPluginStore for ``leaf`` in ``namespace``.

    Moves a pre-hull ``.secret`` aside first, so hull never trips over it.
    """
    quarantine_foreign_machine_key()
    return PerPluginStore(PLUGIN_NAME, sub_key=namespace_leaf(namespace, leaf))


def _migrate_legacy_config() -> dict[str, Any] | None:
    legacy = read_legacy_config(SERVER_NAME)
    if not legacy:
        return None
    plugin_store("config").save(legacy)
    delete_legacy_config(SERVER_NAME)
    logger.info("Migrated saved credentials from the legacy config.enc entry")
    return legacy


def _write_single_user_config(
    config: dict[str, Any], namespace: str = DEFAULT_NAMESPACE
) -> None:
    plugin_store("config", namespace).save(config)


def _read_single_user_config(
    namespace: str = DEFAULT_NAMESPACE,
) -> dict[str, Any] | None:
    saved = plugin_store("config", namespace).load()
    if saved is not None or namespace != DEFAULT_NAMESPACE:
        return saved
    return _migrate_legacy_config()


def _delete_single_user_config(namespace: str = DEFAULT_NAMESPACE) -> None:
    plugin_store("config", namespace).clear()
    if namespace == DEFAULT_NAMESPACE:
        # A legacy entry that was never migrated would otherwise resurrect
        # the credentials on the next read.
        delete_legacy_config(SERVER_NAME)


class CredentialState(Enum):
    AWAITING_SETUP = "awaiting_setup"
    CONFIGURED = "configured"


_state = CredentialState.AWAITING_SETUP


def get_state() -> CredentialState:
    return _state


def resolve_credential_state() -> CredentialState:
    """Fast, synchronous credential check for the ``default`` namespace.

    Checks (in order):
    1. ENV VARS -- TELEGRAM_BOT_TOKEN or TELEGRAM_PHONE present -> CONFIGURED
    2. SAVED CONFIG -- the store (or the migrated legacy entry) has a bot
       token or phone -> CONFIGURED
    3. SAVED SESSIONS -- Telethon session files exist -> AWAITING_SETUP
       (a session exists but the phone is still needed)
    4. NOTHING -- AWAITING_SETUP
    """
    global _state

    if os.environ.get("TELEGRAM_BOT_TOKEN"):
        logger.info("Bot token found in environment")
        _state = CredentialState.CONFIGURED
        return _state

    if os.environ.get("TELEGRAM_PHONE"):
        logger.info("User mode credentials found in environment")
        _state = CredentialState.CONFIGURED
        return _state

    try:
        saved = _read_single_user_config()
    except Exception as e:  # MachineKeyError, unreadable store
        logger.warning("Could not read saved credentials: {}", type(e).__name__)
        saved = None
    if saved and (saved.get("TELEGRAM_BOT_TOKEN") or saved.get("TELEGRAM_PHONE")):
        logger.info("Config loaded from the encrypted store")
        _state = CredentialState.CONFIGURED
        return _state

    if check_saved_sessions():
        logger.info(
            "Found saved Telethon session files. "
            "Run `telegram auth --phone <+number>` or set TELEGRAM_PHONE to reuse them."
        )
        _state = CredentialState.AWAITING_SETUP
        return _state

    logger.info("No credentials found -- server starting unconfigured")
    _state = CredentialState.AWAITING_SETUP
    return _state
