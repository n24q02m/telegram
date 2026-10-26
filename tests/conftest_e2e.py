"""Shared E2E test infrastructure for the telegram MCP server.

Provides:
- --setup CLI option (env | plugin)
- MCP tool-result parsing helpers
"""

from __future__ import annotations


def pytest_addoption(parser):
    """Add the --setup CLI option."""
    parser.addoption(
        "--setup",
        choices=["env", "plugin"],
        default="env",
        help=(
            "Server setup mode: env (credentials from env vars or `telegram auth`, "
            "run from source) or plugin (published package via uvx)"
        ),
    )


def parse_result(r) -> str:
    """Extract text from MCP tool result. Raise on error."""
    if hasattr(r, "isError") and r.isError:
        raise AssertionError(f"Tool returned error: {r.content[0].text}")
    return r.content[0].text


def parse_result_allow_error(r) -> str:
    """Extract text from MCP tool result, including errors."""
    return r.content[0].text
