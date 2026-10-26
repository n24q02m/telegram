# Privacy Policy — telegram

**Last updated:** 2026-10-12

## Data Collection

The telegram MCP server acts as a bridge between MCP clients (Claude, Cursor, etc.) and the Telegram API. It does **not** collect, store, or transmit any user data beyond what is necessary for the current operation.

The project does not operate a hosted endpoint or an auth relay. The server runs on a machine you control, and sign-in (bot token, or phone + OTP + 2FA) happens locally through the `telegram auth` command.

## Local Storage

- Saved credentials (bot token or phone number) are encrypted with AES-256-GCM under a machine key at `~/.telegram/.secret` and stored in `~/.telegram/config.json` (`~/.telegram/subs/<namespace>/` for multi-user HTTP mode).
- OTP codes and 2FA passwords are used only during `telegram auth` and are never written to disk or environment variables.
- Telegram session files are stored locally at `~/.telegram/` (moved once from the pre-rename `~/.better-telegram-mcp/`) with `600` permissions (owner-only).
- Session files contain your Telegram authentication. Treat them like passwords.
- Credentials and session files are never transmitted to any server other than Telegram.

## Telegram API Access

When authenticated, the MCP server can access your Telegram account with the same permissions as the official Telegram app. This includes reading/sending messages, managing contacts, and accessing chat history.

## Third-Party Services

- **Telegram API** (`api.telegram.org`, MTProto): Your data is subject to [Telegram's Privacy Policy](https://telegram.org/privacy).

## Contact

For privacy concerns, open an issue at [github.com/n24q02m/telegram/issues](https://github.com/n24q02m/telegram/issues).
