from fastmcp import FastMCP


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
