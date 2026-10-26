"""Helpers for reading the tools' structured output in tests.

``message`` / ``chat`` / ``contact`` / ``media`` return a FastMCP ``ToolResult``
(built by ``server._wrap_tool``) so that both response channels can be asserted:
the text block keeps the ``<untrusted_{tool}_content>`` XPIA boundary tags and
``structured_content`` carries the envelope markers. ``config`` returns a plain
dict, which FastMCP turns into ``structuredContent`` on the wire; ``help``
returns markdown text.

Use :func:`payload` to read what the tool returned and :func:`text` to assert on
the text block (markers, error messages).
"""

from __future__ import annotations

import json
from typing import Any

from fastmcp.tools import ToolResult
from mcp.types import TextContent


def payload(result: ToolResult | dict[str, Any]) -> dict[str, Any]:
    """Return the tool's structured payload."""
    if isinstance(result, ToolResult):
        assert result.structured_content is not None, (
            "tool emitted no structuredContent"
        )
        return result.structured_content
    return result


def text(result: ToolResult | dict[str, Any]) -> str:
    """Return the tool's text block, XPIA markers included."""
    if isinstance(result, ToolResult):
        return "".join(
            block.text for block in result.content if isinstance(block, TextContent)
        )
    return json.dumps(result, ensure_ascii=False, indent=2)
