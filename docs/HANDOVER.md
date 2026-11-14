# Telegram MCP Handover

## Current product

Telegram MCP exposes Telegram messaging, chat, media, and contact operations through 6 MCP tools (`message`, `chat`, `media`, `contact`, `config`, `help`). It supports Bot API and MTProto user-account modes over local stdio, and an HTTP transport for self-hosted deployments.

**Version: 4.24.0** -- `project.version` in `pyproject.toml`; the release tooling keeps `server.json` and `.claude-plugin/plugin.json` on the same value. Re-read `pyproject.toml` before relying on this line, because a release moves it.

The server is built on hull (`n24q02m-hull`, imported as `hull_core`) and standalone FastMCP 3. hull provides the HTTP transport and bearer auth, the encrypted per-plugin credential store, and the shared CLI built-ins. There is no browser credential form, OAuth server, relay or hosted endpoint.

The public contract is defined by the repository README, `server.json`, package metadata, and the documented MCP tools.

## Build and verify

- Python: 3.13
- Install: `uv sync --group dev`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format --check .`
- Types: `uv run ty check`
- Tests: `uv run pytest --cov --cov-report=term-missing -q` (coverage gate 95%)

The default test run includes MCP protocol tests over stdio (`tests/test_stdio_direct.py`) and HTTP loopback (`tests/test_transports/test_http.py`) with fake credentials and no network calls to Telegram. Live and end-to-end tests (`-m live`, `-m e2e`) require Telegram credentials and an approved test account. A representative live check must call a domain operation such as listing chats; configuration status alone is only a handshake.

## Runtime and data boundaries

- Bot mode uses `TELEGRAM_BOT_TOKEN` or a token saved by `telegram auth --bot-token`.
- User mode uses `telegram auth --phone` (interactive OTP / 2FA) and stores the Telethon session in the data directory (`~/.telegram` by default).
- HTTP settings live in `~/.telegram/config.toml` `[server]`: `host` (default `127.0.0.1`), `port` (default `8000`), `auth` (`no-auth` | `token` | `multi`). `no-auth` refuses non-loopback binds.
- `multi` mode maps each `users.toml` user to a storage namespace. Credentials for a namespace are written with `telegram auth --user <ns>` and stored under `~/.telegram/subs/<ns>/`. Credential state must remain isolated per namespace.
- Upgrades migrate once: the pre-hull shared `config.enc` entry moves into the default namespace, and a pre-hull `~/.telegram/.secret` that is not a hull machine key is renamed aside.

Do not put credentials, OTPs, session files, or raw protocol transcripts in the repository. Do not use external infrastructure as a source of truth for local development or verification.

## Recent source decisions

- Moved from mcp-core to hull: relay form, OAuth AS, pending-OTP store, in-memory session store and the `config__open_relay` tool were removed. Setup is local CLI only.
- HTTP transport is a thin wrapper over hull `run_http_server`, configured by `~/.telegram/config.toml`.
- The CLI uses hull `build_cli`: `auth`, `login` (deprecated alias), `logout` plus hull's `config`, `status`, `doctor`, `token hash`; `--user` selects the namespace.
- CLI-first tool surface: every MCP tool is also a `<tool> <action>` CLI command (`message`, `chat`, `media`, `contact`, `settings`, `help`). Both surfaces call the same `telegram.tools.dispatch` entry (which builds the tool's own argument model and calls the handler); the CLI connects a backend for one call through `telegram.tool_session.connected_backend` instead of the server lifespan. The MCP `config` tool is the CLI `settings` group, because `config` is hull's operator command. Keep the two surfaces wired to the same dispatch function when a tool gains an argument.
- Removed the Cloudflare Worker hosting surface earlier; self-hosting is Docker or the Python package.

## In-flight and release notes

`n24q02m-hull` comes from PyPI under the range `>=0.7.0,<0.8` declared in `pyproject.toml`; re-read that range and the published hull version before a release, because hull's own pin moves them together.

Source changes require repository-native checks and CI readback before merge. BETA/package publication and live protocol evidence are separate from source merge. Stable promotion is a separate release decision and is not implied by this handover.

Rollback is the normal reviewed revert of the source commit and package dependency update. Preserve the prior lockfile and source revision in version control; do not delete local credential or session data as part of a code rollback.

## Week-one operator checklist

1. Confirm the intended transport (stdio or HTTP) and credential mode (bot or user).
2. Install with the documented `uv` command.
3. Run lint, type, and Python tests.
4. Exercise one representative read-only Telegram domain operation with approved credentials.
5. For HTTP `multi` mode, confirm two users resolve to separate namespaces.
6. Review the exact CI run and artifact identity before using a BETA package.

## Triage

- Server exits 1 on stdio start: no credentials; run `telegram auth` or set `TELEGRAM_BOT_TOKEN`.
- Server exits 2 in HTTP mode: invalid `config.toml` / `users.toml`, or `no-auth` on a non-loopback host; the stderr line names the problem.
- Machine key errors: check `~/.telegram/.secret` is hull's 32-byte key; a renamed `.secret.legacy-credential-store` is expected after an upgrade.
- Authentication failures: distinguish missing credentials, malformed credential input, and provider rejection before rotating anything.
