# AGENTS.md - telegram

Telegram MCP Server. Python 3.13, uv, src layout. Dual-mode: Bot API (httpx) + MTProto (Telethon).

## Build / Lint / Test Commands

```bash
uv sync --group dev                # Install dependencies
uv build                           # Build package (hatchling)
uv run ruff check .                # Lint
uv run ruff format --check .       # Format check
uv run ruff format .               # Format fix
uv run ruff check --fix .          # Lint fix
uv run ty check                    # Type check (Astral ty)
uv run pytest                      # Run all tests (integration excluded by default)
uv run pytest -m integration       # Run integration tests only
uv run telegram                    # Run server (stdio)

# Run a single test file
uv run pytest tests/test_config.py

# Run a single test function
uv run pytest tests/test_config.py::test_function_name -v

# Mise shortcuts
mise run setup     # Full dev environment setup
mise run lint      # ruff check + ruff format --check + ty check
mise run test      # pytest
mise run fix       # ruff check --fix --unsafe-fixes + ruff format
mise run dev       # uv run telegram
```

### Pytest Configuration

- `asyncio_mode = "auto"` -- no `@pytest.mark.asyncio` needed
- Default timeout: 30 seconds per test
- Integration tests excluded by default (`-m 'not integration'`)
- Test files: `test_*.py` in `tests/` directory

## Code Style

### Formatting (Ruff)

- **Line length**: 88 (E501 ignored -- long lines allowed)
- **Quotes**: Double quotes
- **Indent**: 4 spaces (Python), 2 spaces (JSON/YAML/TOML)
- **Line endings**: LF
- **Target**: Python 3.13

### Ruff Rules

`select = ["E", "F", "W", "I", "UP", "B", "C4"]`, `ignore = ["E501"]`

- `I` = isort, `UP` = pyupgrade, `B` = bugbear, `C4` = comprehensions

### Type Checker (ty)

Lenient: `unresolved-import`, `unresolved-attribute`, `possibly-unresolved-reference`, `invalid-return-type`, `invalid-argument-type`, `not-iterable`, `invalid-assignment` all `"ignore"`.

### Import Ordering (isort via Ruff)

1. Standard library (`import asyncio`, `import json`, `import os`)
2. Third-party (`from loguru import logger`, `from fastmcp import FastMCP`)
3. Local (`from telegram.config import Settings`)

Lazy imports inside functions for heavy deps and to avoid circular deps.

```python
import asyncio
import json
from pathlib import Path

from fastmcp import FastMCP
from loguru import logger

from telegram.config import Settings
from telegram.backends.base import TelegramBackend
```

### Type Hints

- Full type hints on all signatures: parameters and return types
- Modern syntax: `str | None`, `list[float]`, `dict[str, object]`
- `from __future__ import annotations` used in some files
- `py.typed` marker file present

### Naming Conventions

| Element            | Convention       | Example                              |
|--------------------|------------------|--------------------------------------|
| Functions/methods  | snake_case       | `send_message`, `_detect_mode`       |
| Private            | Leading `_`      | `_bot`, `_client`, `_ensure_auth`    |
| Classes            | PascalCase       | `Settings`, `BotBackend`, `UserBackend` |
| Constants          | UPPER_SNAKE_CASE | `_MAX_MESSAGE_LENGTH`, `_TIMEOUT`    |
| Modules            | snake_case       | `bot_backend.py`, `user_backend.py`  |

### Error Handling

- MCP tools return error strings: `return "Error: query is required..."` (not exceptions)
- try/except with `logger.debug()` / `logger.warning()` for non-fatal failures
- `match action:` for tool action dispatch
- `asyncio.to_thread()` for wrapping sync operations

### File Organization

```
src/telegram/
  __init__.py, __main__.py    # Package + entry
  config.py                   # Pydantic Settings (env prefix TELEGRAM_)
  server.py                   # FastMCP server with lifespan
  backends/
    base.py                   # TelegramBackend ABC
    bot_backend.py            # httpx -> Telegram Bot API
    user_backend.py           # Telethon MTProto client
  tools/                      # 6 tools: 4 domain mega-tools + config + help
    messages.py               # send, edit, delete, forward, pin, search
    chats.py                  # info, create, join, leave, settings
    media.py                  # send photo/file/voice/video, download
    contacts.py               # list, search, add, block
    config_tool.py            # status, set, cache_clear
    help.py                   # documentation lookup
  docs/                       # Tool documentation markdown
tests/                        # Test files mirror source modules
```

### Documentation

- Module-level docstrings on every file
- Google-style docstrings with `Args:`/`Returns:` sections
- Section separators: `# ---------------------------------------------------------------------------`

### Commits

Conventional Commits: `type(scope): message`. Automated semantic release.

### Pre-commit Hooks

1. Ruff lint (`--fix --target-version=py313`) + format
2. ty type check
3. pytest (`--timeout=30 --tb=short -q`)

## Architecture

- **Dual mode**: `Settings._detect_mode()` auto-selects bot/user based on env vars
- **Backend ABC**: `TelegramBackend` defines interface; `BotBackend` (httpx) and `UserBackend` (Telethon) implement it
- **Mega-tool pattern**: 6 tools (4 domain mega-tools + `config` + `help`) x N actions = full API coverage with minimal tool registration overhead
- **Session persistence**: `~/.telegram/<name>.session` for Telethon (MTProto); moved once from the pre-rename `~/.better-telegram-mcp/` by `config.resolve_default_data_dir()`
- **Auth flow**: credentials are set up locally with `telegram auth --bot-token ...` or `telegram auth --phone ...` (interactive phone -> OTP -> optional 2FA password); `login` is a deprecated alias and `better-telegram-mcp` a legacy command alias. `--user <ns>` writes a hull `multi` mode namespace. The MCP `config` tool has no auth or setup actions. Bot mode needs only `TELEGRAM_BOT_TOKEN`
- **Transports**: stdio by default; HTTP (`--http`) runs hull's transport with `~/.telegram/config.toml` (`no-auth` loopback only, `token`, or `multi` with `users.toml`)
- **Glama integration**: The display name cannot be set programmatically and must be updated manually via the Glama admin page. Although 'server.json' contains a 'title' property, it does not control the external Glama listing. The 'glama.json' file is used exclusively for ownership claiming via the 'maintainers' array.

## TODO / Backlog

- [ ] **Glama display name**: Cannot set programmatically. Update manually via Glama admin page.
