from __future__ import annotations

import json

from fastmcp import FastMCP


def _parse_chat_ref(chat_id: str) -> int | str:
    try:
        return int(chat_id)
    except ValueError:
        return chat_id


def register_resources(mcp: FastMCP) -> None:
    @mcp.resource("telegram://docs/messages")
    async def docs_messages() -> str:
        from .tools.help_tool import handle_help

        return await handle_help("messages")

    @mcp.resource("telegram://docs/chats")
    async def docs_chats() -> str:
        from .tools.help_tool import handle_help

        return await handle_help("chats")

    @mcp.resource("telegram://docs/media")
    async def docs_media() -> str:
        from .tools.help_tool import handle_help

        return await handle_help("media")

    @mcp.resource("telegram://docs/contacts")
    async def docs_contacts() -> str:
        from .tools.help_tool import handle_help

        return await handle_help("contacts")

    @mcp.resource("telegram://stats")
    async def stats() -> str:
        from .tools.help_tool import handle_help

        return await handle_help("all")

    @mcp.resource("telegram://media/{chat_id}/{message_id}")
    async def media_resource(chat_id: str, message_id: str) -> str:
        from .extensions import build_media_resource_data
        from .server import _not_ready_response, _ready_backend
        from .utils.formatting import err

        backend = await _ready_backend()
        if backend is None:
            return json.dumps(_not_ready_response(), ensure_ascii=False)

        try:
            resolved_message_id = int(message_id)
        except ValueError:
            return json.dumps(
                err(f"Invalid message_id {message_id!r}: must be an integer."),
                ensure_ascii=False,
            )

        resolved_chat = _parse_chat_ref(chat_id)
        try:
            path = await backend.download_media(resolved_chat, resolved_message_id)
        except Exception as exc:
            return json.dumps(err(str(exc)), ensure_ascii=False)

        payload = build_media_resource_data(
            path,
            uri=f"telegram://media/{chat_id}/{message_id}",
            description=f"Telegram media for chat {chat_id} message {message_id}",
        )
        return json.dumps(payload, ensure_ascii=False)
