"""One-shot backend sessions for the ``telegram <tool>`` commands.

The MCP server owns a process-wide backend started by its lifespan. A CLI tool
command is a one-shot process that never starts a server, so it resolves the
same settings (environment first, then the credentials ``telegram auth``
saved) and connects a backend for exactly one call.

``--user <ns>`` selects a hull namespace the way the operator commands do:
``default`` (stdio, ``no-auth`` and ``token`` HTTP modes) or the namespace of a
``users.toml`` user (``multi`` mode).
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from .backends.base import TelegramBackend
from .config import Settings
from .credential_state import DEFAULT_NAMESPACE, CredentialState


class ToolSessionError(RuntimeError):
    """A tool command cannot open a Telegram backend."""


def _user_flag(namespace: str) -> str:
    return "" if namespace == DEFAULT_NAMESPACE else f" --user {namespace}"


def not_configured_hint(namespace: str = DEFAULT_NAMESPACE) -> str:
    """Operator action that makes ``namespace`` usable from the CLI."""
    flag = _user_flag(namespace)
    return (
        f"no Telegram credentials for namespace {namespace!r}; run "
        f"`telegram auth --bot-token <token>{flag}` (bot mode, token from "
        f"@BotFather) or `telegram auth --phone <+number>{flag}` (user mode)"
    )


def load_settings(namespace: str = DEFAULT_NAMESPACE) -> Settings | None:
    """Settings for ``namespace``, or ``None`` when nothing is configured.

    Environment variables win for the ``default`` namespace; otherwise the
    credentials saved by ``telegram auth`` are loaded explicitly (never
    exported into ``os.environ``, which would leak them to every subprocess).
    """
    if namespace != DEFAULT_NAMESPACE:
        from .auth.telegram_auth_provider import settings_for_namespace

        return settings_for_namespace(namespace)

    settings = Settings()
    if settings.is_configured:
        return settings

    from .credential_state import _read_single_user_config, resolve_credential_state

    if resolve_credential_state() is not CredentialState.CONFIGURED:
        return None
    saved = _read_single_user_config()
    if not saved:
        return None
    saved_settings = Settings.from_saved_config(saved)
    return saved_settings if saved_settings.is_configured else None


@asynccontextmanager
async def connected_backend(
    namespace: str = DEFAULT_NAMESPACE,
) -> AsyncGenerator[TelegramBackend]:
    """Connect a backend for one tool call and disconnect it afterwards."""
    settings = load_settings(namespace)
    if settings is None:
        raise ToolSessionError(not_configured_hint(namespace))

    from .auth.telegram_auth_provider import create_backend

    backend = create_backend(settings, namespace)
    await backend.connect()
    try:
        if settings.mode == "user" and not await backend.is_authorized():
            raise ToolSessionError(
                f"the Telegram session of namespace {namespace!r} is not "
                "authorized; run "
                f"`telegram auth --phone <+number>{_user_flag(namespace)}` on "
                "this machine, then retry"
            )
        yield backend
    finally:
        await backend.disconnect()
