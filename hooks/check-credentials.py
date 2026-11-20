#!/usr/bin/env python3
"""PreToolUse hook: block when telegram credentials are not configured.

Blocking -- Telegram tools cannot function without credentials.
Allows config and help tools through so the user can initiate setup.
"""

import json
import os
import sys

# Add plugins root to sys.path for shared utilities if running inside marketplace
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
try:
    from mcp_common import read_mcp_hook_input
except ImportError:

    def read_mcp_hook_input() -> dict:
        data = None
        try:
            data = json.loads(sys.stdin.read(64 * 1024))
        except Exception:
            pass
        if not isinstance(data, dict):
            print(
                json.dumps(
                    {
                        "decision": "block",
                        "reason": "Invalid input: payload must be a JSON dictionary",
                    }
                )
            )
            sys.exit(2)
        return data


SERVER_NAME = "better-telegram-mcp"
# Either TELEGRAM_PHONE (user mode) or TELEGRAM_BOT_TOKEN (bot mode) is required.
# TELEGRAM_API_ID / TELEGRAM_API_HASH have built-in defaults and are not checked here.
# Claude Code passes the plugin's TELEGRAM_BOT_TOKEN option to hooks as
# CLAUDE_PLUGIN_OPTION_TELEGRAM_BOT_TOKEN; only the server gets TELEGRAM_BOT_TOKEN.
CREDENTIAL_KEYS = [
    "TELEGRAM_PHONE",
    "TELEGRAM_BOT_TOKEN",
    "CLAUDE_PLUGIN_OPTION_TELEGRAM_BOT_TOKEN",
]
# `telegram auth` saves credentials to hull's store at ~/.telegram/config.json;
# hull also reads the pre-rename ~/.telegram-mcp/ and ~/.better-telegram-mcp/.
STORE_DIRS = (".telegram", ".telegram-mcp", ".better-telegram-mcp")
# Tools that work without credentials
EXEMPT_SUFFIXES = ("__setup", "__help", "__config")


def _is_configured() -> bool:
    for k in CREDENTIAL_KEYS:
        if os.environ.get(k):
            return True
    home = os.path.expanduser("~")
    for store_dir in STORE_DIRS:
        if os.path.exists(os.path.join(home, store_dir, "config.json")):
            return True
    config_file = home + "/.config/mcp/config.enc"
    if os.path.exists(config_file):
        return True
    return False


def main() -> None:
    data = read_mcp_hook_input()

    tool_name = data.get("tool_name")
    if not isinstance(tool_name, str):
        tool_name = ""
    if tool_name.endswith(EXEMPT_SUFFIXES):
        sys.exit(0)

    if not _is_configured():
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": (
                        "telegram credentials not configured. "
                        "Set the plugin's TELEGRAM_BOT_TOKEN option (bot mode), "
                        "or run `telegram auth --bot-token <token>` or "
                        "`telegram auth --phone <+number>` (user mode) in a terminal, "
                        "then restart Claude Code. "
                        "Check the result with `telegram status`."
                    ),
                }
            )
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
