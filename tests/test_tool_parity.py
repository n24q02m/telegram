"""Tool-surface parity: the hull migration must not change what clients see.

``tests/fixtures/tools_expected.json`` was dumped from the pre-migration server
(SDK ``mcp.server.fastmcp``) with the relay-only surface removed: the
``config__open_relay`` tool and the four ``setup_*`` lines of the ``config``
description. Names, descriptions, input/output schemas and annotations must
match what the standalone FastMCP server advertises.

Standalone FastMCP serialises the same pydantic-derived schemas slightly
differently; only these presentation details are normalised away (and
asserted separately so a new difference cannot hide behind them):

- the SDK kept the docstring's trailing newline, FastMCP strips it;
- FastMCP drops the auto-generated ``title`` keys;
- FastMCP adds ``additionalProperties: false`` to argument schemas;
- FastMCP marks a wrapped scalar result with ``x-fastmcp-wrap-result``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from fastmcp import Client

from telegram.server import mcp

FIXTURE = Path(__file__).parent / "fixtures" / "tools_expected.json"
EXPECTED_NAMES = ["message", "chat", "media", "contact", "config", "help"]


def _expected() -> dict[str, dict[str, Any]]:
    return {t["name"]: t for t in json.loads(FIXTURE.read_text(encoding="utf-8"))}


async def _actual() -> dict[str, dict[str, Any]]:
    async with Client(mcp) as client:
        tools = await client.list_tools()
    dumped = [
        t.model_dump(mode="json", by_alias=True, exclude_none=True) for t in tools
    ]
    return {t["name"]: t for t in dumped}


def _normalise(schema: Any) -> Any:
    if isinstance(schema, dict):
        return {
            key: _normalise(value)
            for key, value in schema.items()
            if key not in ("title", "x-fastmcp-wrap-result")
            and not (key == "additionalProperties" and value is False)
        }
    if isinstance(schema, list):
        return [_normalise(item) for item in schema]
    return schema


async def test_exactly_six_tools() -> None:
    actual = await _actual()
    assert sorted(actual) == sorted(EXPECTED_NAMES)
    assert "config__open_relay" not in actual


@pytest.mark.parametrize("name", EXPECTED_NAMES)
async def test_tool_matches_fixture(name: str) -> None:
    actual = (await _actual())[name]
    expected = _expected()[name]
    assert actual["description"] == expected["description"].rstrip("\n")
    assert _normalise(actual["inputSchema"]) == _normalise(expected["inputSchema"])
    assert _normalise(actual.get("outputSchema")) == _normalise(
        expected.get("outputSchema")
    )
    assert actual["annotations"] == expected["annotations"]


@pytest.mark.parametrize("name", EXPECTED_NAMES)
async def test_only_known_presentation_differences(name: str) -> None:
    """The normalised keys are the only places the raw schemas may differ."""
    actual = (await _actual())[name]["inputSchema"]
    assert actual.get("additionalProperties") is False
    # No auto-generated title on the schema or on any property definition
    # (``chat`` has a real argument *named* ``title``, which stays).
    assert "title" not in actual
    assert all("title" not in prop for prop in actual["properties"].values())
    assert actual["type"] == "object"


async def test_config_description_has_no_relay_actions() -> None:
    desc = (await _actual())["config"]["description"]
    assert "setup_" not in desc
    assert "relay" not in desc.lower()
