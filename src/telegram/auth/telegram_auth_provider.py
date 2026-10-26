"""Per-namespace Telegram backends for hull's ``multi`` HTTP mode.

hull resolves every HTTP request to an :class:`~hull_core.auth.AuthContext`
whose ``namespace`` scopes storage. ``no-auth`` and ``token`` mode always use
the ``default`` namespace, which ``server.py`` serves from its single global
backend (env vars or ``telegram auth``). In ``multi`` mode each
``users.toml`` user maps to its own namespace; this provider keeps one
connected backend per non-default namespace:

- credentials: ``PerPluginStore("telegram")`` leaf ``subs/<ns>/config``
  (written by ``telegram auth --user <ns>``),
- Telethon session: ``<data dir>/subs/<ns>/<session_name>.session``.

Backends are created lazily on the first tool call of a namespace, so a user
authorized with the CLI after the server started is picked up without a
restart. There is no browser form, OAuth AS or relay: credentials only come
from the local CLI.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from hull_core.storage import validate_sub
from loguru import logger

from ..backends.base import TelegramBackend
from ..config import Settings
from ..errors import redact_bot_token

_global_provider: TelegramAuthProvider | None = None


def get_provider() -> TelegramAuthProvider:
    """The process-global provider (created on first use)."""
    global _global_provider
    if _global_provider is None:
        _global_provider = TelegramAuthProvider()
    return _global_provider


def set_global_provider(provider: TelegramAuthProvider | None) -> None:
    """Replace the process-global provider (tests, shutdown)."""
    global _global_provider
    _global_provider = provider


def namespace_data_dir(namespace: str) -> Path:
    """Telethon session directory for ``namespace``: ``<data dir>/subs/<ns>``."""
    return Settings().data_dir / "subs" / validate_sub(namespace)


def settings_for_namespace(namespace: str) -> Settings | None:
    """Settings from the credentials saved for ``namespace``, or ``None``."""
    from ..credential_state import _read_single_user_config

    saved = _read_single_user_config(namespace)
    if not saved or not (
        saved.get("TELEGRAM_BOT_TOKEN") or saved.get("TELEGRAM_PHONE")
    ):
        return None
    return Settings.from_saved_config(saved, data_dir=namespace_data_dir(namespace))


def create_backend(settings: Settings, namespace: str) -> TelegramBackend:
    """Build (not connect) the backend matching ``settings.mode``."""
    if settings.mode == "bot":
        from ..backends.bot_backend import BotBackend

        assert settings.bot_token is not None
        return BotBackend(settings.bot_token)
    from ..backends.user_backend import UserBackend

    return UserBackend(settings, namespace=namespace)


class TelegramAuthProvider:
    """namespace -> connected :class:`TelegramBackend` registry."""

    def __init__(self, factory=create_backend) -> None:
        self._factory = factory
        self.active_clients: dict[str, TelegramBackend] = {}
        self._locks: dict[str, asyncio.Lock] = {}

    def resolve_backend(self, namespace: str) -> TelegramBackend | None:
        """The already-connected backend of ``namespace`` (no I/O)."""
        return self.active_clients.get(namespace)

    async def get(self, namespace: str) -> TelegramBackend | None:
        """Connected, authorized backend for ``namespace``.

        Returns ``None`` when the namespace has no saved credentials or its
        user-mode session is not authorized yet. Connection errors are
        re-raised with any bot token redacted and without the original
        exception chain (which can carry the token in a request URL).
        """
        backend = self.active_clients.get(namespace)
        if backend is not None:
            return backend
        lock = self._locks.setdefault(namespace, asyncio.Lock())
        async with lock:
            backend = self.active_clients.get(namespace)
            if backend is not None:
                return backend
            settings = settings_for_namespace(namespace)
            if settings is None:
                return None
            backend = self._factory(settings, namespace)
            try:
                await backend.connect()
                authorized = settings.mode == "bot" or await backend.is_authorized()
            except Exception as exc:
                await backend.disconnect()
                msg = (
                    f"Could not connect the Telegram backend for namespace "
                    f"{namespace!r}: {redact_bot_token(str(exc))}"
                )
                raise RuntimeError(msg) from None
            if not authorized:
                await backend.disconnect()
                logger.warning(
                    "Telegram session of namespace {} is not authorized; run "
                    "`telegram auth --phone <+number> --user {}`.",
                    namespace,
                    namespace,
                )
                return None
            self.active_clients[namespace] = backend
            logger.info("Connected Telegram backend for namespace {}", namespace)
            return backend

    async def revoke(self, namespace: str) -> bool:
        """Disconnect and forget the backend of ``namespace``."""
        backend = self.active_clients.pop(namespace, None)
        if backend is None:
            return False
        await backend.disconnect()
        return True

    async def shutdown(self) -> None:
        """Disconnect every backend concurrently (best effort)."""
        items = list(self.active_clients.items())
        self.active_clients.clear()

        async def _disconnect(namespace: str, backend: TelegramBackend) -> None:
            try:
                await backend.disconnect()
            except Exception as exc:
                logger.warning(
                    "Error disconnecting backend of namespace {}: {}",
                    namespace,
                    type(exc).__name__,
                )

        if items:
            await asyncio.gather(*(_disconnect(ns, b) for ns, b in items))
