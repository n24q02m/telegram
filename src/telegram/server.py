from __future__ import annotations

import functools
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP
from hull_core.auth import current_user
from loguru import logger
from mcp.types import ToolAnnotations

from telegram import __version__

from .backends.base import TelegramBackend
from .config import Settings
from .security import build_external_tool_result
from .tools.chats import ChatOptions, handle_chats
from .tools.config_tool import handle_config
from .tools.contacts import ContactsOptions, handle_contacts
from .tools.help_tool import handle_help
from .tools.media import MediaOptions, handle_media
from .tools.messages import MessagesArgs, handle_messages
from .utils.formatting import err, ok

# Silence httpx INFO-level request logs so the bot token in the request URL
# (https://api.telegram.org/bot<TOKEN>/...) cannot leak into stderr.
logging.getLogger("httpx").setLevel(logging.WARNING)

DEFAULT_NAMESPACE = "default"
# The repo README documents the hull setup (CLI auth + config.toml modes).
SETUP_DOCS_URL = "https://github.com/n24q02m/telegram#setup"

# Backend of the ``default`` namespace: stdio, and HTTP ``no-auth`` / ``token``
# mode (hull maps both to ``default``). Other namespaces (HTTP ``multi`` mode)
# are served by ``auth.telegram_auth_provider``.
_backend: TelegramBackend | None = None
_settings: Settings | None = None
_pending_auth: bool = False
_unconfigured: bool = False
_runtime_config: dict[str, int] = {
    "message_limit": 20,
    "timeout": 30,
}


def _namespace() -> str:
    return current_user().namespace


def get_backend() -> TelegramBackend:
    """The connected backend of the caller's hull namespace.

    ``default`` (stdio, ``no-auth``, ``token``) uses the global backend
    created by the lifespan; any other namespace uses the backend the
    per-namespace provider has already connected.
    """
    namespace = _namespace()
    if namespace != DEFAULT_NAMESPACE:
        from .auth.telegram_auth_provider import get_provider

        backend = get_provider().resolve_backend(namespace)
        if backend is None:
            msg = f"No connected Telegram backend for namespace {namespace!r}."
            raise RuntimeError(msg)
        return backend

    if _backend is None:
        msg = "Backend not initialized. Server lifespan not started."
        raise RuntimeError(msg)
    return _backend


def get_settings() -> Settings:
    if _settings is None:
        msg = "Settings not initialized. Server lifespan not started."
        raise RuntimeError(msg)
    return _settings


async def _ready_backend() -> TelegramBackend | None:
    """Backend for this call, or ``None`` when the namespace is not ready."""
    namespace = _namespace()
    if namespace == DEFAULT_NAMESPACE:
        if _unconfigured or _pending_auth:
            return None
        return get_backend()

    from .auth.telegram_auth_provider import get_provider

    return await get_provider().get(namespace)


def _is_unconfigured(namespace: str) -> bool:
    if namespace == DEFAULT_NAMESPACE:
        return _unconfigured
    from .auth.telegram_auth_provider import settings_for_namespace

    return settings_for_namespace(namespace) is None


def _user_flag(namespace: str) -> str:
    return "" if namespace == DEFAULT_NAMESPACE else f" --user {namespace}"


def _not_ready_response() -> dict[str, Any]:
    namespace = _namespace()
    flag = _user_flag(namespace)
    if _is_unconfigured(namespace):
        setup: dict[str, Any] = {
            "bot_mode": {
                "command": f"telegram auth --bot-token <token>{flag}",
                "how": "Get token from @BotFather on Telegram",
            },
            "user_mode": {
                "command": f"telegram auth --phone <+number>{flag}",
                "how": "Interactive OTP/2FA (API credentials have built-in defaults)",
            },
        }
        if namespace == DEFAULT_NAMESPACE:
            setup["bot_mode"]["env_var"] = "TELEGRAM_BOT_TOKEN"
            setup["user_mode"]["env_vars"] = ["TELEGRAM_PHONE"]
        return ok({"error": "Not configured", "setup": setup})
    return err(
        "Telegram session not authenticated. "
        f"Run `telegram auth --phone <+number>{flag}` on the server machine, "
        "then restart the server."
    )


def _ensure_settings() -> Settings:
    """Initialize settings for the ``default`` namespace.

    Env vars win; otherwise the credentials saved by ``telegram auth`` are
    loaded explicitly (never exported into ``os.environ``, which would leak
    them to every subprocess).
    """
    settings = Settings()
    if not settings.is_configured:
        from .credential_state import (
            _read_single_user_config,
            resolve_credential_state,
        )

        state = resolve_credential_state()
        if state.value == "configured":
            saved_config = _read_single_user_config()
            if saved_config:
                settings = Settings.from_saved_config(saved_config)
    return settings


def _create_backend_instance(settings: Settings) -> TelegramBackend:
    """Create a backend instance based on settings mode."""
    if settings.mode == "bot":
        from .backends.bot_backend import BotBackend

        assert settings.bot_token is not None
        return BotBackend(settings.bot_token)
    else:
        from .backends.user_backend import UserBackend

        assert settings.api_id is not None
        assert settings.api_hash is not None
        return UserBackend(settings)


async def _shutdown_provider() -> None:
    from .auth import telegram_auth_provider

    provider = telegram_auth_provider._global_provider
    if provider is not None:
        await provider.shutdown()


@asynccontextmanager
async def _lifespan(server: FastMCP) -> AsyncIterator[None]:
    global _backend, _settings, _pending_auth, _unconfigured
    _settings = _ensure_settings()

    if not _settings.is_configured:
        _unconfigured = True
        logger.warning(
            "No Telegram credentials configured for the default namespace. "
            "help and config tools available; other tools will show setup "
            "instructions. Run `telegram auth --bot-token <token>` or "
            "`telegram auth --phone <+number>` (or set TELEGRAM_BOT_TOKEN), "
            "then restart."
        )
        try:
            yield
        finally:
            _unconfigured = False
            await _shutdown_provider()
        return

    logger.info("Mode: {}", _settings.mode)
    _backend = _create_backend_instance(_settings)
    await _backend.connect()
    logger.info("Connected to Telegram ({})", _settings.mode)

    if _settings.mode == "user" and not await _backend.is_authorized():
        _pending_auth = True
        logger.warning(
            "Session not authorized. Run `telegram auth --phone <+number>` "
            "and restart the server."
        )

    try:
        yield
    finally:
        await _backend.disconnect()
        await _shutdown_provider()
        logger.info("Disconnected from Telegram")


mcp = FastMCP(
    "telegram",
    version=__version__,
    lifespan=_lifespan,
)


def _wrap_tool(tool_name: str):
    """Decorate an ``@mcp.tool`` so external Telegram content is XPIA-marked.

    The wrapped tool returns a plain ``dict``; this turns it into a FastMCP
    ``ToolResult`` so both response channels are defended: the text block
    gains ``<untrusted_{tool}_content>`` boundary tags and ``structuredContent``
    carries the envelope markers (a client reading structured output never sees
    the text block). FastMCP still derives the tool's ``outputSchema`` from the
    wrapped function's ``-> dict`` annotation, which ``functools.wraps`` keeps
    reachable via ``__wrapped__``.

    Applied only to tools that surface arbitrary users' authored content
    (message, chat, contact, media); config/help return the server's own state
    and stay plain dicts.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            result = await func(*args, **kwargs)
            return build_external_tool_result(tool_name, result)

        return wrapper

    return decorator


# --- Tools ---


@mcp.tool(
    annotations=ToolAnnotations(
        title="Telegram Messages",
        read_only_hint=False,
        destructive_hint=True,
        idempotent_hint=False,
        open_world_hint=True,
    )
)
@_wrap_tool("message")
async def message(
    action: str,
    chat_id: str | int | None = None,
    text: str | None = None,
    message_id: int | None = None,
    reply_to: int | None = None,
    parse_mode: str | None = None,
    from_chat: str | int | None = None,
    to_chat: str | int | None = None,
    emoji: str | None = None,
    query: str | None = None,
    limit: int = 20,
    offset_id: int | None = None,
) -> dict[str, Any]:
    """Send, edit, delete, forward, pin, react, search, and get message history.

    Actions (chat_id: "@username" | int):
    - send (chat_id, text -> reply_to, parse_mode)
    - edit (chat_id, message_id, text -> parse_mode)
    - delete (chat_id, message_id)
    - forward (from_chat, to_chat, message_id)
    - pin (chat_id, message_id)
    - react (chat_id, message_id, emoji)
    - search (query -> chat_id, limit=20)
    - history (chat_id -> limit=20, offset_id)
    """
    backend = await _ready_backend()
    if backend is None:
        return _not_ready_response()

    args = MessagesArgs(
        action=action,
        chat_id=chat_id,
        text=text,
        message_id=message_id,
        reply_to=reply_to,
        parse_mode=parse_mode,
        from_chat=from_chat,
        to_chat=to_chat,
        emoji=emoji,
        query=query,
        limit=limit,
        offset_id=offset_id,
    )
    return await handle_messages(backend, args)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Telegram Chats",
        read_only_hint=False,
        destructive_hint=True,
        idempotent_hint=False,
        open_world_hint=True,
    )
)
@_wrap_tool("chat")
async def chat(
    action: str,
    chat_id: str | int | None = None,
    title: str | None = None,
    description: str | None = None,
    is_channel: bool = False,
    link_or_hash: str | None = None,
    user_id: int | None = None,
    demote: bool = False,
    limit: int = 50,
    topic_action: str | None = None,
    topic_id: int | None = None,
    topic_name: str | None = None,
) -> dict[str, Any]:
    """List, create, join, leave, manage members, settings, and topics.

    Actions:
    - list (-> limit=50)
    - info (chat_id)
    - create (title -> is_channel)
    - join (link_or_hash)
    - leave (chat_id)
    - members (chat_id -> limit=50)
    - admin (chat_id, user_id -> demote)
    - settings (chat_id, title|description)
    - topics (chat_id, topic_action -> topic_id, topic_name)
    """
    backend = await _ready_backend()
    if backend is None:
        return _not_ready_response()

    opts = ChatOptions(
        chat_id=chat_id,
        title=title,
        description=description,
        is_channel=is_channel,
        link_or_hash=link_or_hash,
        user_id=user_id,
        demote=demote,
        limit=limit,
        topic_action=topic_action,
        topic_id=topic_id,
        topic_name=topic_name,
    )
    return await handle_chats(backend, action, opts)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Telegram Media",
        read_only_hint=False,
        destructive_hint=False,
        idempotent_hint=False,
        open_world_hint=True,
    )
)
@_wrap_tool("media")
async def media(
    action: str,
    chat_id: str | int | None = None,
    file_path_or_url: str | None = None,
    message_id: int | None = None,
    caption: str | None = None,
    output_dir: str | None = None,
    file_id: str | None = None,
) -> dict[str, Any]:
    """Send photos, files, voice, video, and download media from messages.

    Actions (file_path_or_url: local path or URL):
    - send_photo (chat_id, file_path_or_url -> caption)
    - send_file (chat_id, file_path_or_url -> caption)
    - send_voice (chat_id, file_path_or_url -> caption)
    - send_video (chat_id, file_path_or_url -> caption)
    - download (chat_id, message_id -> output_dir; bot mode also requires file_id)
    """
    backend = await _ready_backend()
    if backend is None:
        return _not_ready_response()

    opts = MediaOptions(
        chat_id=chat_id,
        file_path_or_url=file_path_or_url,
        message_id=message_id,
        caption=caption,
        output_dir=output_dir,
        file_id=file_id,
    )
    return await handle_media(backend, action, opts)


@mcp.tool(
    annotations=ToolAnnotations(
        title="Telegram Contacts",
        read_only_hint=False,
        destructive_hint=False,
        idempotent_hint=False,
        open_world_hint=True,
    )
)
@_wrap_tool("contact")
async def contact(
    action: str,
    query: str | None = None,
    phone: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    user_id: int | None = None,
    unblock: bool = False,
) -> dict[str, Any]:
    """Manage contacts: list, search, add, and block/unblock users (user mode only).

    Actions:
    - list: Show all contacts
    - search (query): Find contacts by name
    - add (phone, first_name -> last_name)
    - block (user_id -> unblock=true)
    """
    backend = await _ready_backend()
    if backend is None:
        return _not_ready_response()

    opts = ContactsOptions(
        query=query,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        user_id=user_id,
        unblock=unblock,
    )
    return await handle_contacts(backend, action, options=opts)


def _unconfigured_status(namespace: str) -> dict[str, Any]:
    flag = _user_flag(namespace)
    return ok(
        {
            "mode": None,
            "connected": False,
            "authorized": False,
            "configured": False,
            "config": _runtime_config,
            "setup": {
                "bot_mode": f"Run `telegram auth --bot-token <token>{flag}` "
                "(get from @BotFather)",
                "user_mode": f"Run `telegram auth --phone <+number>{flag}`"
                " (API credentials have built-in defaults)",
            },
            "hint": "Configure with the `telegram auth` CLI on the server "
            "machine, then restart the server.",
        }
    )


@mcp.tool(
    annotations=ToolAnnotations(
        title="Telegram Config",
        read_only_hint=False,
        destructive_hint=False,
        idempotent_hint=True,
        open_world_hint=False,
    )
)
async def config(
    action: str,
    message_limit: int | None = None,
    timeout: int | None = None,
    key: str | None = None,
    value: str | None = None,
) -> dict[str, Any]:
    """Server configuration and runtime settings.

    Actions (required params):
    - status: Show connection state, mode, and current config
    - set (key+value, or message_limit|timeout): Update a runtime limit.
      Generic form: set(key='message_limit', value='50'). Typed sugar:
      set(message_limit=50).
    - cache_clear: Clear internal caches
    """
    namespace = _namespace()
    if namespace == DEFAULT_NAMESPACE:
        # A configured-but-unauthorized user session still reports status.
        backend = None if _unconfigured else get_backend()
    else:
        from .auth.telegram_auth_provider import get_provider

        backend = await get_provider().get(namespace)

    if backend is None:
        if action == "status" and _is_unconfigured(namespace):
            return _unconfigured_status(namespace)
        return _not_ready_response()
    return await handle_config(
        backend,
        action,
        message_limit=message_limit,
        timeout=timeout,
        key=key,
        value=value,
    )


@mcp.tool(
    annotations=ToolAnnotations(
        title="Telegram Help",
        read_only_hint=True,
        destructive_hint=False,
        idempotent_hint=True,
        open_world_hint=False,
    )
)
async def help(topic: str | None = None) -> str:
    """Get full documentation for any topic.

    Topics: telegram | messages | chats | media | contacts | all (default: all)
    """
    return await handle_help(topic)


# --- Resources ---
from .resources import register_resources  # noqa: E402

register_resources(mcp)


_UNCONFIGURED_STDIO_HINT = (
    "[telegram] No Telegram credentials configured for stdio mode.\n"
    "\n"
    "Run one of:\n"
    "  telegram auth --bot-token <token>   (bot mode, get token from @BotFather)\n"
    "  telegram auth --phone <+number>     (user mode, interactive OTP/2FA)\n"
    "  (login is a deprecated alias of auth)\n"
    "\n"
    "Or set TELEGRAM_BOT_TOKEN in your plugin/server env config.\n"
    "Check the result with `telegram status`.\n"
    f"Documentation: {SETUP_DOCS_URL}\n"
)


def _parse_serve_args(argv: list[str]):
    import argparse

    parser = argparse.ArgumentParser(prog="telegram", add_help=False)
    parser.add_argument("--http", action="store_true", default=False)
    parser.add_argument("--host", default=None)
    parser.add_argument("--port", type=int, default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Start the server: stdio by default, HTTP with ``--http``.

    ``MCP_TRANSPORT=http`` / ``TRANSPORT_MODE=http`` also select HTTP.
    ``--host`` / ``--port`` override ``~/.telegram/config.toml`` ``[server]``.
    """
    import os
    import sys

    args = _parse_serve_args(sys.argv[1:] if argv is None else argv)
    is_http = (
        args.http
        or os.environ.get("MCP_TRANSPORT") == "http"
        or os.environ.get("TRANSPORT_MODE") == "http"
    )

    if not is_http:
        # Credentials come from env, the encrypted saved config or a saved
        # Telethon session; only a truly unconfigured stdio server exits.
        from .credential_state import CredentialState, resolve_credential_state

        if resolve_credential_state() != CredentialState.CONFIGURED:
            sys.stderr.write(_UNCONFIGURED_STDIO_HINT)
            return 1
        # show_banner=False: the banner also runs a PyPI version check.
        mcp.run(transport="stdio", show_banner=False)
        return 0

    from .transports.http import start_http

    return start_http(host=args.host, port=args.port)
