# CLAUDE.md - telegram

MCP server for Telegram. Python 3.13, uv, hatchling, src layout. Built on
[hull](https://github.com/n24q02m/hull) (`n24q02m-hull`, imported as
`hull_core`) and standalone FastMCP 3.

Dual mode: Bot API (httpx) and MTProto user accounts (Telethon).
6 tools: `message`, `chat`, `media`, `contact`, `config`, `help`.

## Commands

```bash
uv sync --group dev          # Setup
uv run ruff check .          # Lint
uv run ruff format --check . # Format check
uv run ty check              # Type check
uv run pytest                # Tests (integration/live/full/e2e markers excluded)
uv run pytest --cov --cov-report=term-missing -q   # Coverage (gate: 95%)
uv run ruff check --fix . && uv run ruff format .  # Fix
```

## Source layout

```
src/telegram/
  cli.py               # hull build_cli: auth / login / logout + hull built-ins
  server.py            # FastMCP("telegram") + lifespan + 6 tools + main()
  config.py            # Pydantic Settings (env prefix TELEGRAM_), data dir
                       # move, pre-hull .secret quarantine
  credential_state.py  # PerPluginStore("telegram") config per namespace +
                       # one-time legacy config.enc migration
  sessions.py          # SERVER_NAME, credential field names, saved-session check
  errors.py            # redact_bot_token, error sanitization, 2FA detection
  security.py          # XPIA boundary tags for external Telegram content
  resources.py         # telegram://docs/* resources
  auth/
    telegram_auth_provider.py  # Per-namespace backends for hull `multi` mode
  backends/            # TelegramBackend ABC -> BotBackend (httpx), UserBackend (Telethon)
  backends/security.py # validate_url, validate_file_path, validate_output_dir
  transports/
    http.py            # start_http: hull run_http_server + ~/.telegram/config.toml
  tools/               # messages, chats, media, contacts, config_tool, help_tool
```

## Transports and auth modes

Stdio is the default (`mcp.run(transport="stdio")`). Without credentials the
stdio server prints the `telegram auth` hint to stderr and exits 1 before any
MCP output.

HTTP is opted into with `--http`, `MCP_TRANSPORT=http` or
`TRANSPORT_MODE=http`. Settings come from `~/.telegram/config.toml`:

```toml
[server]
host = "127.0.0.1"   # default; --host overrides
port = 8000          # default; --port overrides
auth = "token"       # "no-auth" | "token" | "multi"
token_hash = "scrypt$..."   # token mode: output of `telegram token hash`
# users_file = "users.toml" # multi mode; defaults to ~/.telegram/users.toml
# rpm = 60                  # optional per-client rate limit
```

- `no-auth`: loopback binds only; a non-loopback host is refused (exit 2).
- `token`: one bearer token, compared against `token_hash`.
- `multi`: per-user bearer tokens from `users.toml`; each user maps to a
  storage namespace. Users are administered host-side by editing the file
  and restarting:

  ```toml
  [users.alice]
  token_hash = "scrypt$..."
  enabled = true
  namespace = "alice"
  ```

hull serves MCP at `/mcp` and a public `GET /health`. An invalid
`config.toml` / `users.toml` prints one line to stderr and exits 2.

There is no browser setup form, OAuth server, relay or hosted endpoint.
Credentials only come from env vars or the local CLI.

## Storage

- Credentials: hull `PerPluginStore("telegram")`, encrypted with the machine
  key `~/.telegram/.secret`.
  - `default` namespace (stdio, `no-auth`, `token`): `~/.telegram/config.json`.
  - Other namespaces (`multi`): `~/.telegram/subs/<ns>/config.json`.
- Telethon sessions: `~/.telegram/<session_name>.session` (default namespace)
  and `~/.telegram/subs/<ns>/<session_name>.session`, permission 600.
- Migrations, run once:
  - `~/.better-telegram-mcp/` is renamed to `~/.telegram/`.
  - The pre-hull shared `config.enc` entry (`better-telegram-mcp`) moves into
    the default namespace on first read; only that entry is removed.
  - A pre-hull `~/.telegram/.secret` that is not a 32-byte hull key is renamed
    to `.secret.legacy-credential-store` (never read or deleted).

The default-namespace backend is created at startup, so run `telegram auth`
before starting the server (or restart after). Other namespaces connect on
their first tool call.

## CLI

```bash
telegram                                  # start the server (stdio)
telegram --http [--host H] [--port P]     # start the HTTP server
telegram auth --bot-token <token> [--user <ns>]
telegram auth --phone <+number> [--user <ns>]   # interactive OTP / 2FA
telegram login ...                        # deprecated alias of auth
telegram logout [--yes] [--user <ns>]     # revoke session, delete credentials
telegram config status | config delete --yes
telegram status
telegram doctor
telegram token hash                       # reads the token from stdin / prompt
```

`--user` selects the hull namespace (default `default`). Unknown subcommands
and argument errors exit 2.

## Env vars

- `TELEGRAM_BOT_TOKEN` -- bot mode (wins over saved credentials)
- `TELEGRAM_PHONE` -- user mode phone
- `TELEGRAM_API_ID` + `TELEGRAM_API_HASH` -- optional; bundled public defaults
- `USE_BUNDLED_TELEGRAM_CLIENT` -- set false to require your own API pair
- `TELEGRAM_SESSION_NAME`, `TELEGRAM_DATA_DIR` -- optional
- `MCP_TRANSPORT` / `TRANSPORT_MODE` -- `http` selects HTTP

There is no `TELEGRAM_PASSWORD`: 2FA is prompted by `telegram auth` and never
stored in the environment.

## Notes

- Config tool actions: `status`, `set`, `cache_clear`.
- `message`, `chat`, `media` and `contact` results carry XPIA boundary tags in
  the text block and envelope markers in `structuredContent`.
- Bot tokens never reach logs: httpx logs at WARNING and `redact_bot_token`
  scrubs error text.
- Security: SSRF protection, path traversal prevention, error sanitization.

## Release

- Conventional Commits (`fix:` / `feat:`). Tag format: `v{version}`.
- CD: semantic release -> PyPI `n24q02m-telegram` -> Docker multi-arch
  (`n24q02m/telegram`, `ghcr.io/n24q02m/telegram`) -> MCP Registry.
- `n24q02m-hull` is pinned to a git commit until it is published to PyPI;
  replace it with a version range before the next PyPI release.

## Pre-commit hooks

1. Ruff lint (`--fix`) + format
2. ty type check
3. pytest (`--tb=short -q`)
4. Commit message: Conventional Commits

## E2E

Protocol tests live in this repo and drive the server over the MCP wire
protocol (`ClientSession` + `stdio_client`):

- `tests/test_stdio_direct.py` -- default run. Spawns the CLI through
  `tests/stdio_bootstrap.py` (isolated home and legacy config path, Bot API
  connect stubbed): credential gate, `initialize`, `tools/list`, `help`.
- `tests/test_transports/test_http.py` -- HTTP loopback: wrong token 401,
  right token, public `/health`, `no-auth` + `0.0.0.0` refused, multi
  namespaces.
- `tests/test_live_protocol.py` (`-m live`) and `tests/test_e2e.py`
  (`-m e2e`) -- real Telegram; need `TELEGRAM_BOT_TOKEN` or a user session
  authorized with `telegram auth`.
