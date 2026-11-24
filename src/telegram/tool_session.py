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


def _account_flag(account: str | None) -> str:
    return "" if not account else f" --account {account}"


def not_configured_hint(
    namespace: str = DEFAULT_NAMESPACE, account: str | None = None
) -> str:
    """Operator action that makes ``namespace`` (and optional ``account``) usable."""
    flag = f"{_user_flag(namespace)}{_account_flag(account)}"
    target = (
        f"account {account!r} in namespace {namespace!r}"
        if account
        else f"namespace {namespace!r}"
    )
    return (
        f"no Telegram credentials for {target}; run "
        f"`telegram auth --bot-token <token>{flag}` (bot mode, token from "
        f"@BotFather) or `telegram auth --phone <+number>{flag}` (user mode)"
    )


def load_settings(
    namespace: str = DEFAULT_NAMESPACE, *, account: str | None = None
) -> Settings | None:
    """Settings for ``namespace`` (and optional named ``account``), or ``None``.

    An explicit account (flag or ``TELEGRAM_ACCOUNT``) reads the named account
    registry directly; otherwise environment variables win for ``default``,
    falling back to the active stored credentials.
    """
    from .credential_state import (
        _read_single_user_config,
        resolve_account_name,
        resolve_credential_state,
    )

    acct = resolve_account_name(account)
    if namespace != DEFAULT_NAMESPACE:
        from .auth.telegram_auth_provider import settings_for_namespace

        return (
            settings_for_namespace(namespace)
            if acct is None
            else settings_for_namespace(namespace, account=acct)
        )

    if acct is not None:
        saved = _read_single_user_config(account=acct)
        if not saved:
            return None
        saved_settings = Settings.from_saved_config(saved)
        return saved_settings if saved_settings.is_configured else None

    settings = Settings()
    if settings.is_configured:
        return settings

    if resolve_credential_state() is not CredentialState.CONFIGURED:
        return None
    saved = _read_single_user_config()
    if not saved:
        return None
    saved_settings = Settings.from_saved_config(saved)
    return saved_settings if saved_settings.is_configured else None


@asynccontextmanager
async def connected_backend(
    namespace: str = DEFAULT_NAMESPACE, *, account: str | None = None
) -> AsyncGenerator[TelegramBackend]:
    """Connect a backend for one tool call and disconnect it afterwards."""
    from .credential_state import resolve_account_name

    acct = resolve_account_name(account)
    settings = (
        load_settings(namespace)
        if acct is None
        else load_settings(namespace, account=acct)
    )
    if settings is None:
        raise ToolSessionError(not_configured_hint(namespace, account=acct))

    from .auth.telegram_auth_provider import create_backend

    backend = create_backend(settings, namespace)
    await backend.connect()
    try:
        if settings.mode == "user" and not await backend.is_authorized():
            raise ToolSessionError(
                f"the Telegram session of namespace {namespace!r} is not "
                "authorized; run "
                f"`telegram auth --phone <+number>{_user_flag(namespace)}{_account_flag(acct)}` on "
                "this machine, then retry"
            )
        yield backend
    finally:
        await backend.disconnect()
