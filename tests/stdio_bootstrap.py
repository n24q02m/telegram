"""Run the telegram CLI in a subprocess with the legacy config path isolated.

hull resolves the pre-hull ``config.enc`` through platformdirs, which on
Windows reads the profile folder through the shell API rather than from
``APPDATA`` / ``LOCALAPPDATA``. Redirecting HOME is therefore not enough to
keep a subprocess away from a developer's real legacy file: the default
namespace would migrate that entry and delete it. This bootstrap patches the
path from ``TELEGRAM_TEST_LEGACY_CONFIG`` before the CLI runs and refuses to
start without it.

``TELEGRAM_TEST_STUB_BOT=1`` replaces ``BotBackend.connect`` / ``disconnect``
with no-ops so a fake bot token reaches a running server without any network
call to Telegram.

Usage: ``python tests/stdio_bootstrap.py [cli args...]``.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

EXIT_UNSAFE = 3
BOOTSTRAP = Path(__file__).resolve()

# Credential and transport inputs that must not leak from a developer shell.
_SCRUBBED_ENV = (
    "MCP_STORAGE_BACKEND",
    "CREDENTIAL_SECRET",
    "MCP_TRANSPORT",
    "TRANSPORT_MODE",
)


def isolated_env(home: Path, **extra: str) -> dict[str, str]:
    """Build a subprocess environment rooted at ``home`` with no credentials."""
    env = {
        k: v
        for k, v in os.environ.items()
        if not k.startswith("TELEGRAM_") and k not in _SCRUBBED_ENV
    }
    env.update(
        {
            "HOME": str(home),
            "USERPROFILE": str(home),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "TELEGRAM_DATA_DIR": str(home / ".telegram"),
            "TELEGRAM_TEST_LEGACY_CONFIG": str(home / "legacy-mcp" / "config.enc"),
            "PYTHONIOENCODING": "utf-8",
        }
    )
    env.update(extra)
    return env


def _install_isolation() -> bool:
    legacy = os.environ.get("TELEGRAM_TEST_LEGACY_CONFIG", "")
    if not legacy:
        sys.stderr.write(
            "stdio_bootstrap: TELEGRAM_TEST_LEGACY_CONFIG is required; "
            "refusing to run against the real legacy config path\n"
        )
        return False

    import hull_core.storage.legacy_config_file as legacy_config_file

    legacy_path = Path(legacy)
    legacy_config_file.default_legacy_config_path = lambda: legacy_path

    if os.environ.get("TELEGRAM_TEST_STUB_BOT") == "1":
        from telegram.backends.bot_backend import BotBackend

        async def _no_op(self: BotBackend) -> None:
            return None

        BotBackend.connect = _no_op  # type: ignore[method-assign]
        BotBackend.disconnect = _no_op  # type: ignore[method-assign]
    return True


def main() -> int:
    if not _install_isolation():
        return EXIT_UNSAFE
    from telegram.cli import main as cli_main

    return cli_main(sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
