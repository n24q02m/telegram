"""HTTP transport: the telegram FastMCP server behind hull auth.

Settings come from ``~/.telegram/config.toml`` ``[server]`` (hull
``load_settings``): ``host`` (default ``127.0.0.1``), ``port`` (default
``8000``), ``auth`` (``no-auth`` | ``token`` | ``multi``), ``token_hash``
(``token`` mode) and ``users_file`` (``multi`` mode). ``--host`` / ``--port``
override the file. hull serves MCP at ``/mcp`` and an unauthenticated
``GET /health``; ``no-auth`` refuses any non-loopback bind.

Stdio mode is handled in ``server.main()`` and never reaches this module.
"""

from __future__ import annotations

import asyncio
from pathlib import Path

from hull_core.auth.users import UsersError
from hull_core.config.settings import ConfigError, HullSettings, load_settings
from hull_core.server.http import run_http_server
from hull_core.server.run import ServerConfigError
from loguru import logger

CONFIG_DIR_NAME = ".telegram"


def config_dir() -> Path:
    """Directory holding ``config.toml`` (and ``users.toml``): ``~/.telegram``."""
    return Path.home() / CONFIG_DIR_NAME


def load_http_settings() -> HullSettings:
    """hull settings from ``~/.telegram/config.toml`` (defaults when absent)."""
    return load_settings(config_dir())


def start_http(*, host: str | None = None, port: int | None = None) -> int:
    """Serve over HTTP until interrupted; returns a process exit code.

    Invalid ``config.toml`` and unsafe binds (``no-auth`` on a non-loopback
    host) print one clear line to stderr and return ``2`` instead of a
    traceback.
    """
    import sys

    from ..server import mcp

    try:
        settings = load_http_settings()
        logger.info(
            "Starting HTTP server (auth={}) on {}:{}",
            settings.server.auth,
            host or settings.server.host,
            port or settings.server.port,
        )
        asyncio.run(run_http_server(mcp, settings, host=host, port=port))
    except (ConfigError, ServerConfigError, UsersError) as exc:
        sys.stderr.write(f"[telegram] {exc}\n")
        return 2
    except KeyboardInterrupt:
        return 0
    return 0
