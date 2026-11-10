"""One shared entry point per MCP tool.

``server.py``'s ``@mcp.tool`` functions resolve the backend of the caller's
hull namespace, then call the ``run_*`` function below; the ``telegram
<tool>`` CLI commands open a one-shot backend and call the same function.
Each argument model is built exactly once here, so the MCP surface and the CLI
surface cannot drift apart when a tool gains a parameter.

The XPIA envelope (``build_external_tool_result``) stays in ``server.py``: it
defends an MCP client from external content, while a CLI caller is the
operator reading their own terminal.
"""

from __future__ import annotations

from typing import Any

from ..backends.base import TelegramBackend
from .chats import ChatOptions, handle_chats
from .config_tool import handle_config
from .contacts import ContactsOptions, handle_contacts
from .help_tool import handle_help
from .media import MediaOptions, handle_media
from .messages import MessagesArgs, handle_messages


async def run_message(
    backend: TelegramBackend,
    *,
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
    """Run one ``message`` tool action (send/edit/delete/.../history)."""
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


async def run_chat(
    backend: TelegramBackend,
    *,
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
    """Run one ``chat`` tool action (list/info/create/.../topics)."""
    options = ChatOptions(
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
    return await handle_chats(backend, action, options)


async def run_media(
    backend: TelegramBackend,
    *,
    action: str,
    chat_id: str | int | None = None,
    file_path_or_url: str | None = None,
    message_id: int | None = None,
    caption: str | None = None,
    output_dir: str | None = None,
    file_id: str | None = None,
) -> dict[str, Any]:
    """Run one ``media`` tool action (send_photo/.../download)."""
    options = MediaOptions(
        chat_id=chat_id,
        file_path_or_url=file_path_or_url,
        message_id=message_id,
        caption=caption,
        output_dir=output_dir,
        file_id=file_id,
    )
    return await handle_media(backend, action, options)


async def run_contact(
    backend: TelegramBackend,
    *,
    action: str,
    query: str | None = None,
    phone: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    user_id: int | None = None,
    unblock: bool = False,
) -> dict[str, Any]:
    """Run one ``contact`` tool action (list/search/add/block)."""
    options = ContactsOptions(
        query=query,
        phone=phone,
        first_name=first_name,
        last_name=last_name,
        user_id=user_id,
        unblock=unblock,
    )
    return await handle_contacts(backend, action, options=options)


async def run_config(
    backend: TelegramBackend,
    *,
    action: str,
    message_limit: int | None = None,
    timeout: int | None = None,
    key: str | None = None,
    value: str | None = None,
) -> dict[str, Any]:
    """Run one ``config`` tool action (status/set/cache_clear)."""
    return await handle_config(
        backend,
        action,
        message_limit=message_limit,
        timeout=timeout,
        key=key,
        value=value,
    )


async def run_help(topic: str | None = None) -> str:
    """Run the ``help`` tool: documentation text, or its own error JSON."""
    return await handle_help(topic)
