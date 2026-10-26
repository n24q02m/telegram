# telegram

mcp-name: io.github.n24q02m/better-telegram-mcp

**Telegram for AI agents: messages, chats, media, and contacts in bot and user-account modes.**

<!-- Badge Row 1: Status -->
[![Mode](https://img.shields.io/badge/mode-stdio_%C2%B7_http_self--host-5C6BC0)](#setup)
[![CI](https://github.com/n24q02m/telegram/actions/workflows/ci.yml/badge.svg)](https://github.com/n24q02m/telegram/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/n24q02m/telegram/graph/badge.svg?token=d0fef60a-542e-4be2-9528-6e3a12931067)](https://codecov.io/gh/n24q02m/telegram)
[![PyPI](https://img.shields.io/pypi/v/n24q02m-telegram?logo=pypi&logoColor=white)](https://pypi.org/project/n24q02m-telegram/)
[![Docker](https://img.shields.io/docker/v/n24q02m/telegram?label=docker&logo=docker&logoColor=white&sort=semver)](https://hub.docker.com/r/n24q02m/telegram)
[![License: Apache-2.0](https://img.shields.io/github/license/n24q02m/telegram)](https://www.apache.org/licenses/LICENSE-2.0)

<!-- Badge Row 2: Tech -->
[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)](#)
[![Telegram](https://img.shields.io/badge/Telegram-Bot_API_+_MTProto-26A5E4?logo=telegram&logoColor=white)](https://core.telegram.org)
[![MCP](https://img.shields.io/badge/MCP-000000?logo=anthropic&logoColor=white)](#)
[![semantic-release](https://img.shields.io/badge/semantic--release-e10079?logo=semantic-release&logoColor=white)](https://github.com/python-semantic-release/python-semantic-release)
[![Renovate](https://img.shields.io/badge/renovate-enabled-1A1F6C?logo=renovatebot&logoColor=white)](https://github.com/renovatebot/renovate)

<!-- BEGIN: AUTO-GENERATED-CROSS-PROMO -->
<details>
  <summary><strong>Sister projects from n24q02m</strong> (click to expand)</summary>

| Project | Tagline | Tag |
|---|---|---|
| [agent-chat-plugin](https://github.com/n24q02m/agent-chat-plugin) | Peer AI agents chat in a shared folder — no human relay, no orchestrator, wor... | Tooling |
| [better-code-review-graph](https://github.com/n24q02m/better-code-review-graph) | Knowledge graph for token-efficient code reviews -- semantic search and call-... | MCP |
| [better-drive](https://github.com/n24q02m/better-drive) | 2-way Google Drive sync with .driveignore filter — rclone engine, Windows tray | Tooling |
| [better-email-mcp](https://github.com/n24q02m/better-email-mcp) | IMAP/SMTP email for AI agents -- read, send, organize folders, and manage att... | MCP |
| [better-godot-mcp](https://github.com/n24q02m/better-godot-mcp) | Composite MCP server for Godot Engine -- 17 composite tools for AI-assisted g... | MCP |
| [better-notion-mcp](https://github.com/n24q02m/better-notion-mcp) | Markdown-first Notion for AI agents -- pages, databases, blocks, and comments... | MCP |
| [better-semantic-release](https://github.com/n24q02m/better-semantic-release) | Drop-in python-semantic-release fork with built-in release-safety guards (orp... | Tooling |
| [better-telegram-mcp](https://github.com/n24q02m/better-telegram-mcp) | Telegram for AI agents -- messages, chats, media, and contacts across both bo... | MCP |
| [better-workspace-mcp](https://github.com/n24q02m/better-workspace-mcp) | Google Workspace MCP server (Docs/Drive/Calendar/Gmail/Sheets/Slides/Tasks/Ch... | MCP |
| [claude-plugins](https://github.com/n24q02m/claude-plugins) | Claude Code plugin marketplace for the n24q02m MCP servers -- install web sea... | Marketplace |
| [imagine-mcp](https://github.com/n24q02m/imagine-mcp) | Image and video understanding + generation for AI agents -- across Gemini, Op... | MCP |
| [jules-task-archiver](https://github.com/n24q02m/jules-task-archiver) | Chrome Extension for bulk operations on Jules tasks via batchexecute API -- a... | Tooling |
| [mcp-core](https://github.com/n24q02m/mcp-core) | Shared foundation for building MCP servers -- Streamable HTTP transport, OAut... | MCP |
| [mnemo-mcp](https://github.com/n24q02m/mnemo-mcp) | Persistent AI memory with hybrid search and embedded sync. Open, free, unlimi... | MCP |
| [qwen3-embed](https://github.com/n24q02m/qwen3-embed) | Lightweight Qwen3 text embedding and reranking via ONNX Runtime and GGUF | Library |
| [skret](https://github.com/n24q02m/skret) | Secrets without the server. | CLI |
| [tacet](https://github.com/n24q02m/tacet) | A self-distilling neuro-symbolic cascade that amortises LLM cost across knowl... | Tooling |
| [web-core](https://github.com/n24q02m/web-core) | Shared web infrastructure package for search, scraping, HTTP security, and st... | Library |
| [wet-mcp](https://github.com/n24q02m/wet-mcp) | Open-source MCP server for AI agents: web search, content extraction, and lib... | MCP |

</details>
<!-- END: AUTO-GENERATED-CROSS-PROMO -->

## Table of contents

- [Features](#features)
- [Install](#install)
- [Setup](#setup)
- [Smithery](#smithery)
- [Configuration](#configuration)
- [HTTP mode](#http-mode)
- [CLI](#cli)
- [Tools](#tools)
- [Comparison](#comparison)
- [Security](#security)
- [Build from Source](#build-from-source)
- [Trust Model](#trust-model)
- [License](#license)



<a href="https://glama.ai/mcp/servers/n24q02m/better-telegram-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/n24q02m/better-telegram-mcp/badge" alt="better-telegram-mcp MCP server" />
</a>

## Features

- **Dual mode** -- Bot API (httpx) for bots, MTProto (Telethon) for user accounts
- **6 tools** with action dispatch: `message`, `chat`, `media`, `contact`, `config`, `help`
- **Auto-detect mode** -- Set a bot token for bot mode, or a phone number for user mode
- **Local CLI auth** -- `telegram auth` handles the bot token, or phone + OTP + 2FA, on the machine that runs the server
- **Stdio or HTTP** -- stdio by default; HTTP with no-auth (loopback only), a single bearer token, or per-user tokens
- **Tool annotations** -- Each tool declares `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`
- **MCP Resources** -- Documentation available as `telegram://docs/*` resources
- **Security hardened** -- SSRF protection, path traversal prevention, error sanitization, prompt-injection boundary tags on Telegram content

## Install

```bash
# Claude Code plugin (stdio, bot mode)
/plugin marketplace add n24q02m/claude-plugins
/plugin install better-telegram-mcp@n24q02m-plugins

# Direct uvx invocation (stdio, bot mode)
claude mcp add telegram -e TELEGRAM_BOT_TOKEN=123456:ABC-DEF -- uvx n24q02m-telegram

# Docker stdio
docker run -i --rm -e TELEGRAM_BOT_TOKEN=123456:ABC-DEF n24q02m/telegram
```

The package is `n24q02m-telegram` (formerly `better-telegram-mcp`; the old
package receives one final release then freezes). The MCP Registry id stays
`io.github.n24q02m/better-telegram-mcp`, the Docker image is
`n24q02m/telegram`, and the legacy `better-telegram-mcp` command is kept as an
alias of `telegram`. Local data moves once from `~/.better-telegram-mcp` to
`~/.telegram` on first start.

### Install matrix

| Client | Install |
|:-------|:--------|
| Claude Code | `/plugin marketplace add n24q02m/claude-plugins` + `/plugin install better-telegram-mcp@n24q02m-plugins` (stdio bot mode), or `claude mcp add` as in the block above |
| Cursor / Windsurf / Gemini CLI / any MCP client | `mcpServers` JSON in the client's config: stdio `command`, or `type: "http"` + `url` pointing at a server you run (see [HTTP mode](#http-mode)) |

**Install with AI agent** -- paste this to your AI coding agent:

> Install MCP server `telegram` following the steps at
> https://raw.githubusercontent.com/n24q02m/claude-plugins/main/plugins/better-telegram-mcp/setup-with-agent.md

## Setup

Credentials are configured on the machine that runs the server.

**Bot mode:** set `TELEGRAM_BOT_TOKEN` in the client config, or save it once:

```bash
telegram auth --bot-token 123456:ABC-DEF
```

**User mode:** sign in interactively with your phone number. Telegram sends an
OTP; a 2FA password is prompted if the account has one. The Telethon session
is stored on disk.

```bash
telegram auth --phone +15551234567
```

Check the result with `telegram status`. The server reads saved credentials at
startup, so restart it after `telegram auth`. Without any credentials the
stdio server prints these instructions to stderr and exits with status 1.

## Smithery

Also listed on [Smithery](https://smithery.ai/servers/n24q02m/better-telegram-mcp).
Per [`smithery.yaml`](smithery.yaml), Smithery starts the server over **stdio** with
`uvx --python 3.13 n24q02m-telegram` and takes **no install-time configuration**
(empty `configSchema`). Credentials come from the `TELEGRAM_BOT_TOKEN` env var or
a prior `telegram auth` (see [Setup](#setup)).

## Configuration

Settings load from `TELEGRAM_`-prefixed environment variables (Pydantic Settings).
Env vars take precedence over credentials saved by `telegram auth`.

| Variable | Required | Description |
|:---------|:---------|:------------|
| `TELEGRAM_BOT_TOKEN` | Bot mode | Bot token from [@BotFather](https://t.me/BotFather) (format `123456789:ABCdef...`) |
| `TELEGRAM_PHONE` | User mode | Phone number in `+<country><number>` form |
| `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` | No | Override the bundled public API pair |
| `USE_BUNDLED_TELEGRAM_CLIENT` | No | Set to `false` to require your own API pair |
| `TELEGRAM_SESSION_NAME` | No | Telethon session file name (default `default`) |
| `TELEGRAM_DATA_DIR` | No | Session directory (default `~/.telegram`) |
| `MCP_TRANSPORT` | No | Set to `http` to start in HTTP mode (`--http` or `TRANSPORT_MODE=http` also work) |

There is no `TELEGRAM_PASSWORD` env var: `telegram auth` prompts for the 2FA
password and never stores it in the environment.

## HTTP mode

`telegram --http` serves MCP at `/mcp` and an unauthenticated `GET /health`.
Settings live in `~/.telegram/config.toml`:

```toml
[server]
host = "127.0.0.1"   # default; --host overrides
port = 8000          # default; --port overrides
auth = "token"       # "no-auth" | "token" | "multi"
token_hash = "scrypt$..."
```

| `auth` | Who can connect | Credentials used |
|:-------|:----------------|:-----------------|
| `no-auth` | Anyone who can reach the port; loopback binds only (a non-loopback host is refused) | The default credentials |
| `token` | Clients sending `Authorization: Bearer <token>` matching `token_hash` | The default credentials |
| `multi` | Users listed in `users.toml` (default `~/.telegram/users.toml`), each with their own token | Each user's own namespace |

Create a token hash with `telegram token hash` (it reads the token from stdin
or a prompt, never from the command line). In `multi` mode, add users by
editing `users.toml` and restarting the server:

```toml
[users.alice]
token_hash = "scrypt$..."
enabled = true
namespace = "alice"
```

Then authorize Telegram for that user on the server machine:

```bash
telegram auth --phone +15551234567 --user alice
```

To reach a server on another machine, put it behind a TLS-terminating reverse
proxy or a private network and use `token` or `multi` auth.

## CLI

The `telegram` console script (installed by `uvx` / `pip`; `better-telegram-mcp`
is a legacy alias) starts the MCP server when run without a subcommand. Flags
that are not a subcommand are passed through to the server (for example
`--http`, `--host`, `--port`).

```bash
telegram            # start the MCP server (stdio)
telegram --http     # start in HTTP mode
telegram --version  # print the version
```

| Subcommand | Usage | Description |
|:-----------|:------|:------------|
| `auth` | `auth --bot-token <token>` or `auth --phone <+number>`, optional `--user <ns>` | Authorize this machine. Bot mode validates the token; phone mode runs the interactive OTP/2FA flow and stores the Telethon session on disk |
| `login` | Same arguments as `auth` | Deprecated alias of `auth` |
| `logout` | `logout [--yes] [--user <ns>]` | Revoke the Telegram session, delete the session file and the saved credentials |
| `config` | `config status`, `config delete --yes` | Show or delete the saved credential config |
| `status` | `status` | Show whether credentials are configured |
| `doctor` | `doctor` | Print environment diagnostics |
| `token` | `token hash` | Hash a bearer token for `config.toml` / `users.toml` |

`--user` selects the storage namespace (default `default`, used by stdio and
the `no-auth` / `token` HTTP modes). Unknown subcommands exit with status 2.

## Tools

| Tool | Actions | Description |
|:-----|:--------|:------------|
| `message` | `send`, `edit`, `delete`, `forward`, `pin`, `react`, `search`, `history` | Send, edit, delete, forward messages. Pin, react, search, browse history |
| `chat` | `list`, `info`, `create`, `join`, `leave`, `members`, `admin`, `settings`, `topics` | List and manage chats, groups, channels. Members, admin, forum topics |
| `media` | `send_photo`, `send_file`, `send_voice`, `send_video`, `download` | Send photos, files, voice notes, videos. Download media from messages |
| `contact` | `list`, `search`, `add`, `block` | List, search, add contacts. Block/unblock users (user mode only) |
| `config` | `status`, `set`, `cache_clear` | Server status, runtime settings (`message_limit`, `timeout`), cache |
| `help` | -- | Full documentation for any topic |

### MCP Resources

| URI | Content |
|:----|:--------|
| `telegram://docs/messages` | Message operations reference |
| `telegram://docs/chats` | Chat management reference |
| `telegram://docs/media` | Media send/download reference |
| `telegram://docs/contacts` | Contact management reference |
| `telegram://stats` | All documentation combined |

## Comparison

How telegram stacks up against direct competitors in each pillar:

| Capability | telegram | chigwell/telegram-mcp | sparfenyuk/mcp-telegram | guangxiangdebizi/telegram-mcp |
|---|---|---|---|---|
| Bot API mode (bot token) | Yes (httpx) | No | No | Yes |
| MTProto user-account mode | Yes (Telethon) | Yes | Yes | No |
| Send / edit / delete messages | Yes | Yes | No (read-only, draft only) | Yes (send only) |
| Media download from messages | Yes | Yes | Yes | No (send only) |
| Contact management (add / block) | Yes (user mode) | Yes | Partial (list only) | No |
| Multi-user HTTP, per-user isolation | Yes (per-user tokens and namespaces) | No | No | No |
| SSRF protection | Yes (URL validation + DNS-rebinding) | ? | ? | No |
| Path-traversal prevention | Yes | Yes (real-path allowed-root) | ? | No |
| Self-hostable | Yes | Yes | Yes | Yes |

## Security

- **SSRF Protection** -- All URLs validated against internal/private IP ranges, DNS rebinding blocked
- **Path Traversal Prevention** -- File paths validated, sensitive directories blocked
- **Session File Security** -- 600 permissions; the 2FA password is prompted, never stored in env vars
- **Error Sanitization** -- Credentials and bot tokens are never leaked in error messages or logs
- **Prompt-injection boundaries** -- Telegram content returned by tools is wrapped in untrusted-content tags

## Build from Source

```bash
git clone https://github.com/n24q02m/telegram.git
cd telegram
uv sync
uv run telegram
```

## Trust Model

The project does not operate a hosted Telegram endpoint. The server runs on
infrastructure you control, and credentials never leave that machine.

| Data | Location | Protection |
|---|---|---|
| Saved credentials (bot token / phone) | `~/.telegram/config.json`; `~/.telegram/subs/<ns>/config.json` in `multi` mode | AES-256-GCM with the machine key `~/.telegram/.secret` |
| Telethon sessions | `~/.telegram/<name>.session`; `~/.telegram/subs/<ns>/` in `multi` mode | File permission 0600 |
| HTTP bearer tokens | `token_hash` in `config.toml` / `users.toml` | Stored only as scrypt hashes |

Anyone with access to your OS user account can read these files.

## License

Apache-2.0 -- See [LICENSE](LICENSE).
