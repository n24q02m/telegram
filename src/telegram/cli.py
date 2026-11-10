"""Console-script entry: the hull consumer CLI builder.

Bare invocation and any leading-dash argv (``--http``, ``--host``, ``--port``)
start the server; a leading positional argv[0] runs a one-shot subcommand.
hull provides ``config``, ``status``, ``doctor`` and ``token hash``; this
module adds ``auth`` (``login`` is a deprecated alias) and replaces ``logout``
so it also revokes and deletes the Telethon session.

The MCP tools are callable here too, one ``<tool> <action>`` group per tool
(``message``, ``chat``, ``media``, ``contact``, ``settings``, ``help``). Each
command calls the same ``telegram.tools.dispatch`` entry point the server's
``@mcp.tool`` functions call, against a backend that is connected for exactly
that one call -- MCP is an adapter over these handlers, not a separate path.
``--json`` prints the tool result as JSON; a tool error goes to stderr and
exits 1. The MCP ``config`` tool is ``settings`` here, because ``config`` is
hull's operator command for the saved credential blob.

``auth`` / ``logout`` / the tool commands act on the machine that hosts the
server. ``--user <ns>`` targets one hull namespace: ``default`` (stdio,
``no-auth`` and ``token`` HTTP modes) or the ``namespace`` of a ``users.toml``
user (``multi`` mode).
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import json
import sys
from collections.abc import Awaitable, Callable
from typing import Any, TextIO

from hull_core.consumer_cli import build_cli
from hull_core.storage import validate_sub

from telegram.credential_state import DEFAULT_NAMESPACE, PLUGIN_NAME

_MARKER_LEAF = "tokens/app-identity"
_SESSION_LEAF = "session"

# Command name handed to hull's ``build_cli``. It is the documented console
# script (``[project.scripts]`` in pyproject.toml), so it is also the argparse
# ``prog`` of every subcommand parser and the prefix of ``--help``, ``status``,
# ``config``, ``doctor`` and unknown-subcommand output.
# The legacy ``better-telegram-mcp`` name survives only where it is a
# compatibility key -- ``sessions.SERVER_NAME`` for the migrated credential
# entry and ``config.LEGACY_DATA_DIR_NAME`` for the pre-rename data dir -- never
# in operator-facing text.
DISPLAY_NAME = "telegram"


def _serve(argv: list[str]) -> int | None:
    from telegram.server import main as server_main

    return server_main(argv)


def _namespace(value: str) -> str:
    """argparse type for ``--user``: a safe hull namespace name."""
    try:
        return validate_sub(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from None


def _add_user_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--user",
        type=_namespace,
        default=DEFAULT_NAMESPACE,
        metavar="NAMESPACE",
        help=(
            "hull namespace to act on (default: 'default', used by stdio and "
            "the no-auth/token HTTP modes; in multi mode use the user's "
            "users.toml namespace)"
        ),
    )


# --- auth / login ---


def _add_credential_args(p: argparse.ArgumentParser) -> None:
    """Add the mutually-exclusive bot-token / phone credential flags."""
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--bot-token",
        default=None,
        help="Bot API token from @BotFather (bot mode)",
    )
    group.add_argument(
        "--phone",
        default=None,
        help="Phone number in +<country><number> form (user mode, interactive)",
    )


def _configure_auth(p: argparse.ArgumentParser) -> None:
    p.description = (
        "Authenticate on this machine. Bot mode validates the token; phone "
        "mode runs the interactive OTP/2FA flow and stores the Telethon "
        "session on disk."
    )
    # Optional provider positional kept for CLI compatibility; telegram has a
    # single provider.
    p.add_argument(
        "provider",
        nargs="?",
        default="telegram",
        choices=["telegram"],
        help="Credential provider to authorize (only 'telegram')",
    )
    _add_credential_args(p)
    _add_user_arg(p)


def _configure_login(p: argparse.ArgumentParser) -> None:
    p.description = "Deprecated alias of `auth`."
    _add_credential_args(p)
    _add_user_arg(p)


def _handle_auth(args: argparse.Namespace) -> int:
    if args.bot_token:
        return _login_bot(args.bot_token, args.user)
    return _login_phone(args.phone, args.user)


def _handle_login(args: argparse.Namespace) -> int:
    print(
        "telegram: `login` is deprecated; use `auth` instead.",
        file=sys.stderr,
    )
    return _handle_auth(args)


def _login_bot(bot_token: str, namespace: str = DEFAULT_NAMESPACE) -> int:
    try:
        asyncio.run(_verify_bot_token(bot_token))
    except Exception as e:
        from telegram.errors import _sanitize_error

        print(f"Login failed: {_sanitize_error(str(e))}", file=sys.stderr)
        return 1

    from telegram.credential_state import _write_single_user_config

    _write_single_user_config({"TELEGRAM_BOT_TOKEN": bot_token}, namespace)
    print(f"Logged in (bot mode, namespace {namespace}). Credentials saved locally.")
    return 0


async def _verify_bot_token(bot_token: str) -> None:
    from telegram.backends.bot_backend import BotBackend

    backend = BotBackend(bot_token)
    try:
        await backend.connect()
    finally:
        await backend.disconnect()


def _login_phone(phone: str, namespace: str = DEFAULT_NAMESPACE) -> int:
    if not sys.stdin.isatty():
        print(
            "auth --phone requires an interactive terminal "
            "(the OTP code is prompted on stdin).",
            file=sys.stderr,
        )
        return 1

    try:
        result = asyncio.run(_run_phone_login(phone, namespace))
    except Exception as e:
        from telegram.errors import _sanitize_error

        print(f"Login failed: {_sanitize_error(str(e))}", file=sys.stderr)
        return 1

    who = result.get("authenticated_as") or "user"
    print(
        f"Logged in as {who} (user mode, namespace {namespace}). Session saved locally."
    )
    return 0


def _settings_for(namespace: str, config: dict[str, str] | None = None):
    """Settings whose ``data_dir`` holds the Telethon session of ``namespace``."""
    from telegram.config import Settings

    if namespace == DEFAULT_NAMESPACE:
        return Settings.from_saved_config(config) if config else Settings()
    from telegram.auth.telegram_auth_provider import namespace_data_dir

    return Settings.from_saved_config(
        config or {}, data_dir=namespace_data_dir(namespace)
    )


async def _run_phone_login(phone: str, namespace: str = DEFAULT_NAMESPACE) -> dict:
    from telegram.backends.user_backend import UserBackend
    from telegram.errors import _needs_2fa_password

    settings = _settings_for(namespace, {"TELEGRAM_PHONE": phone})
    backend = UserBackend(settings, namespace=namespace)
    await backend.connect()
    try:
        await backend.send_code(phone)
        code = _prompt_otp()
        try:
            result = await backend.sign_in(phone, code)
        except Exception as e:
            if not _needs_2fa_password(str(e)):
                raise
            password = _prompt_2fa_password()
            result = await backend.sign_in(phone, code, password=password)
        _persist_phone_identity(settings, phone, namespace)
        return result
    finally:
        await backend.disconnect()


def _prompt_otp() -> str:
    print(
        "Enter the OTP code sent to your Telegram app: ",
        end="",
        file=sys.stderr,
        flush=True,
    )
    return sys.stdin.readline().strip()


def _prompt_2fa_password() -> str:
    return getpass.getpass("Enter your 2FA password: ", stream=sys.stderr)


def _persist_phone_identity(
    settings, phone: str, namespace: str = DEFAULT_NAMESPACE
) -> None:
    from telegram.credential_state import _write_single_user_config

    _write_single_user_config({"TELEGRAM_PHONE": phone}, namespace)
    _store(_MARKER_LEAF, namespace).save({"api_id": str(settings.api_id)})


# --- logout ---


def _configure_logout(p: argparse.ArgumentParser) -> None:
    p.description = (
        "Revoke and delete the Telethon session and remove the saved "
        "credentials of one namespace."
    )
    p.add_argument("--yes", action="store_true", default=False)
    _add_user_arg(p)


def _confirmed(namespace: str, *, yes: bool) -> bool:
    if yes:
        return True
    if not sys.stdin.isatty():
        print(
            "telegram: refusing to log out without --yes in non-interactive mode",
            file=sys.stderr,
        )
        return False
    print(
        f"Remove the Telegram session and credentials of namespace "
        f"{namespace!r}? [y/N] ",
        end="",
        file=sys.stderr,
        flush=True,
    )
    if sys.stdin.readline().strip().lower() in ("y", "yes"):
        return True
    print("telegram: aborted", file=sys.stderr)
    return False


def _handle_logout(args: argparse.Namespace) -> int:
    namespace: str = args.user
    if not _confirmed(namespace, yes=args.yes):
        return 1

    settings = _settings_for(namespace)
    session_path = settings.session_path
    actions: list[str] = []

    if session_path.exists():
        try:
            asyncio.run(_revoke_session(settings, namespace))
            actions.append("revoked Telegram session server-side")
        except Exception as e:
            from telegram.errors import _sanitize_error

            print(
                "Warning: could not revoke session server-side: "
                f"{_sanitize_error(str(e))}",
                file=sys.stderr,
            )
        try:
            session_path.unlink()
            actions.append("deleted local session file")
        except FileNotFoundError:
            pass

    if _clear_single_user_config(namespace):
        actions.append("cleared saved credentials")
    if _clear_blob(_SESSION_LEAF, namespace):
        actions.append("cleared stored session blob")
    if _clear_blob(_MARKER_LEAF, namespace):
        actions.append("cleared api identity marker")

    if not actions:
        print("Nothing to log out.")
        return 0

    for action in actions:
        print(f"- {action}")
    print("Logged out.")
    return 0


async def _revoke_session(settings, namespace: str = DEFAULT_NAMESPACE) -> None:
    from telegram.backends.user_backend import UserBackend

    backend = UserBackend(settings, namespace=namespace)
    await backend.connect()
    try:
        await backend.log_out()
    finally:
        await backend.disconnect()


def _clear_single_user_config(namespace: str = DEFAULT_NAMESPACE) -> bool:
    from telegram.credential_state import (
        _delete_single_user_config,
        _read_single_user_config,
    )

    existed = bool(_read_single_user_config(namespace))
    _delete_single_user_config(namespace)
    return existed


def _store(leaf: str, namespace: str):
    from telegram.credential_state import plugin_store

    return plugin_store(leaf, namespace)


def _clear_blob(leaf: str, namespace: str) -> bool:
    store = _store(leaf, namespace)
    existed = store.has_stored_blob()
    store.clear()
    return existed


# --- tool commands ---
#
# One ``<tool> <action>`` group per MCP tool. Each group takes the tool's own
# arguments as flags and calls ``telegram.tools.dispatch`` -- the functions the
# server's ``@mcp.tool`` wrappers call -- so a CLI call and an MCP call share
# one argument model and one handler. Missing arguments are reported by the
# handler (the same message an MCP client sees), never by a second validator.

_MESSAGE_ACTIONS = (
    "send",
    "edit",
    "delete",
    "forward",
    "pin",
    "react",
    "search",
    "history",
)
_CHAT_ACTIONS = (
    "list",
    "info",
    "create",
    "join",
    "leave",
    "members",
    "admin",
    "settings",
    "topics",
)
_MEDIA_ACTIONS = (
    "send_photo",
    "send_file",
    "send_voice",
    "send_video",
    "download",
)
_CONTACT_ACTIONS = ("list", "search", "add", "block")
_CONFIG_ACTIONS = ("status", "set", "cache_clear")


def _chat_id(value: str) -> str | int:
    """argparse type: numeric ids become ``int``; ``@username`` stays a str."""
    try:
        return int(value)
    except ValueError:
        return value


def _add_tool_args(p: argparse.ArgumentParser) -> None:
    """Flags every tool command shares: ``--json`` and the namespace."""
    p.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        default=False,
        help="print the tool result as JSON on stdout",
    )
    _add_user_arg(p)


def _configure_message(p: argparse.ArgumentParser) -> None:
    p.description = (
        "MCP tool `message`: send, edit, delete, forward, pin, react, search, history."
    )
    p.add_argument("action", choices=_MESSAGE_ACTIONS)
    p.add_argument(
        "--chat-id",
        type=_chat_id,
        default=None,
        metavar="ID|@NAME",
        help="chat id or @username (negative ids need --chat-id=-100123...)",
    )
    p.add_argument("--text", default=None)
    p.add_argument("--message-id", type=int, default=None)
    p.add_argument("--reply-to", type=int, default=None)
    p.add_argument("--parse-mode", default=None, help="HTML, MarkdownV2 or Markdown")
    p.add_argument("--from-chat", type=_chat_id, default=None)
    p.add_argument("--to-chat", type=_chat_id, default=None)
    p.add_argument("--emoji", default=None)
    p.add_argument("--query", default=None)
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--offset-id", type=int, default=None)
    _add_tool_args(p)


def _configure_chat(p: argparse.ArgumentParser) -> None:
    p.description = "MCP tool `chat`: list, info, create, join, leave, members, admin, settings, topics."
    p.add_argument("action", choices=_CHAT_ACTIONS)
    p.add_argument(
        "--chat-id",
        type=_chat_id,
        default=None,
        metavar="ID|@NAME",
        help="chat id or @username (negative ids need --chat-id=-100123...)",
    )
    p.add_argument("--title", default=None)
    p.add_argument("--description", default=None)
    p.add_argument("--is-channel", action="store_true", default=False)
    p.add_argument("--link-or-hash", default=None, help="invite link or hash")
    p.add_argument("--user-id", type=int, default=None)
    p.add_argument("--demote", action="store_true", default=False)
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--topic-action", default=None)
    p.add_argument("--topic-id", type=int, default=None)
    p.add_argument("--topic-name", default=None)
    _add_tool_args(p)


def _configure_media(p: argparse.ArgumentParser) -> None:
    p.description = (
        "MCP tool `media`: send_photo, send_file, send_voice, send_video, download."
    )
    p.add_argument("action", choices=_MEDIA_ACTIONS)
    p.add_argument(
        "--chat-id",
        type=_chat_id,
        default=None,
        metavar="ID|@NAME",
        help="chat id or @username (negative ids need --chat-id=-100123...)",
    )
    p.add_argument("--file-path-or-url", default=None, help="local path or URL")
    p.add_argument("--message-id", type=int, default=None)
    p.add_argument("--caption", default=None)
    p.add_argument("--output-dir", default=None)
    p.add_argument("--file-id", default=None, help="bot mode download")
    _add_tool_args(p)


def _configure_contact(p: argparse.ArgumentParser) -> None:
    p.description = "MCP tool `contact`: list, search, add, block (user mode only)."
    p.add_argument("action", choices=_CONTACT_ACTIONS)
    p.add_argument("--query", default=None)
    p.add_argument("--phone", default=None)
    p.add_argument("--first-name", default=None)
    p.add_argument("--last-name", default=None)
    p.add_argument("--user-id", type=int, default=None)
    p.add_argument("--unblock", action="store_true", default=False)
    _add_tool_args(p)


def _configure_settings(p: argparse.ArgumentParser) -> None:
    p.description = (
        "MCP tool `config` (CLI name `settings`; `config` is the operator "
        "command): status, set, cache_clear."
    )
    p.add_argument("action", choices=_CONFIG_ACTIONS)
    p.add_argument("--message-limit", type=int, default=None)
    p.add_argument("--timeout", type=int, default=None)
    p.add_argument("--key", default=None, help="message_limit or timeout")
    p.add_argument("--value", default=None, help="new value for --key")
    _add_tool_args(p)


def _configure_help(p: argparse.ArgumentParser) -> None:
    p.description = (
        "MCP tool `help`: full documentation for any topic (no credentials needed)."
    )
    p.add_argument(
        "topic",
        nargs="?",
        default=None,
        metavar="TOPIC",
        help="telegram | messages | chats | media | contacts | all (default: all)",
    )
    p.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        default=False,
        help="print the documentation as a JSON envelope on stdout",
    )


def _summary(value: Any) -> str:
    """One-line rendering of a nested tool value for human output."""
    if isinstance(value, dict):
        parts = [f"{k}={_summary(v)}" for k, v in value.items() if v is not None]
        return "  ".join(parts) if parts else "{}"
    if isinstance(value, list):
        return f"{len(value)} items"
    return str(value)


def _print_human(payload: dict[str, Any], stream: TextIO) -> None:
    """Render a tool result as ``key: value`` lines (lists summarized)."""
    for key, value in payload.items():
        if isinstance(value, list):
            print(f"{key}: {len(value)}", file=stream)
            for item in value:
                print(f"  {_summary(item)}", file=stream)
        elif isinstance(value, dict):
            print(f"{key}:", file=stream)
            for inner_key, inner_value in value.items():
                print(f"  {inner_key}: {_summary(inner_value)}", file=stream)
        else:
            print(f"{key}: {value}", file=stream)


def _emit(payload: dict[str, Any], *, as_json: bool) -> int:
    """Print one tool result; an ``error`` envelope goes to stderr, exit 1."""
    failed = "error" in payload
    stream = sys.stderr if failed else sys.stdout
    if as_json:
        print(
            json.dumps(payload, ensure_ascii=False, indent=2, default=str),
            file=stream,
        )
    elif failed:
        print(payload["error"], file=stream)
    else:
        _print_human(payload, stream)
    return 1 if failed else 0


async def _one_shot(
    namespace: str, call: Callable[[Any], Awaitable[dict[str, Any]]]
) -> dict[str, Any]:
    """Run ``call`` against a backend that lives for exactly this call."""
    from telegram.tool_session import connected_backend

    async with connected_backend(namespace) as backend:
        return await call(backend)


def _run_tool(
    ns: argparse.Namespace, call: Callable[[Any], Awaitable[dict[str, Any]]]
) -> int:
    """Connect, run one dispatch call, print it; failures exit 1, never raise."""
    from telegram.errors import _sanitize_error
    from telegram.tool_session import ToolSessionError

    try:
        payload = asyncio.run(_one_shot(ns.user, call))
    except ToolSessionError as e:
        print(f"telegram: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"telegram: {_sanitize_error(str(e))}", file=sys.stderr)
        return 1
    return _emit(payload, as_json=ns.as_json)


def _handle_message(ns: argparse.Namespace) -> int:
    from telegram.tools.dispatch import run_message

    def call(backend):
        return run_message(
            backend,
            action=ns.action,
            chat_id=ns.chat_id,
            text=ns.text,
            message_id=ns.message_id,
            reply_to=ns.reply_to,
            parse_mode=ns.parse_mode,
            from_chat=ns.from_chat,
            to_chat=ns.to_chat,
            emoji=ns.emoji,
            query=ns.query,
            limit=ns.limit,
            offset_id=ns.offset_id,
        )

    return _run_tool(ns, call)


def _handle_chat(ns: argparse.Namespace) -> int:
    from telegram.tools.dispatch import run_chat

    def call(backend):
        return run_chat(
            backend,
            action=ns.action,
            chat_id=ns.chat_id,
            title=ns.title,
            description=ns.description,
            is_channel=ns.is_channel,
            link_or_hash=ns.link_or_hash,
            user_id=ns.user_id,
            demote=ns.demote,
            limit=ns.limit,
            topic_action=ns.topic_action,
            topic_id=ns.topic_id,
            topic_name=ns.topic_name,
        )

    return _run_tool(ns, call)


def _handle_media(ns: argparse.Namespace) -> int:
    from telegram.tools.dispatch import run_media

    def call(backend):
        return run_media(
            backend,
            action=ns.action,
            chat_id=ns.chat_id,
            file_path_or_url=ns.file_path_or_url,
            message_id=ns.message_id,
            caption=ns.caption,
            output_dir=ns.output_dir,
            file_id=ns.file_id,
        )

    return _run_tool(ns, call)


def _handle_contact(ns: argparse.Namespace) -> int:
    from telegram.tools.dispatch import run_contact

    def call(backend):
        return run_contact(
            backend,
            action=ns.action,
            query=ns.query,
            phone=ns.phone,
            first_name=ns.first_name,
            last_name=ns.last_name,
            user_id=ns.user_id,
            unblock=ns.unblock,
        )

    return _run_tool(ns, call)


def _handle_settings(ns: argparse.Namespace) -> int:
    from telegram.tools.dispatch import run_config

    def call(backend):
        return run_config(
            backend,
            action=ns.action,
            message_limit=ns.message_limit,
            timeout=ns.timeout,
            key=ns.key,
            value=ns.value,
        )

    return _run_tool(ns, call)


def _help_error(text: str) -> str | None:
    """``handle_help`` returns its own failures as a JSON string."""
    stripped = text.lstrip()
    if not stripped.startswith("{"):
        return None
    try:
        payload = json.loads(stripped)
    except ValueError:
        return None
    error = payload.get("error") if isinstance(payload, dict) else None
    return error if isinstance(error, str) else None


def _handle_help(ns: argparse.Namespace) -> int:
    """``help`` is documentation only: no backend, no credentials."""
    from telegram.tools.dispatch import run_help

    try:
        text = asyncio.run(run_help(ns.topic))
    except Exception as e:
        from telegram.errors import _sanitize_error

        print(f"telegram: {_sanitize_error(str(e))}", file=sys.stderr)
        return 1
    error = _help_error(text)
    if error is not None:
        return _emit({"error": error}, as_json=ns.as_json)
    if ns.as_json:
        print(
            json.dumps(
                {"topic": ns.topic or "all", "content": text},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(text)
    return 0


_OPERATOR_COMMANDS = (
    ("auth", "authorize this machine: --bot-token <token> | --phone <+number>"),
    ("login", "deprecated alias of auth"),
    ("logout", "revoke the Telegram session and delete saved credentials"),
    ("config", "operator: show or delete the saved credential config"),
    ("status", "operator: show whether credentials are configured"),
    ("doctor", "operator: print environment diagnostics"),
    ("token", "operator: hash a bearer token (`token hash`)"),
)

_TOOL_COMMANDS = (
    ("message", " | ".join(_MESSAGE_ACTIONS)),
    ("chat", " | ".join(_CHAT_ACTIONS)),
    ("media", " | ".join(_MEDIA_ACTIONS)),
    ("contact", " | ".join(_CONTACT_ACTIONS)),
    ("settings", " | ".join(_CONFIG_ACTIONS)),
    ("help", "[topic]"),
)


def _usage() -> str:
    """``--help``: operator commands and tool groups listed separately."""
    width = max(len(name) for name, _ in (*_OPERATOR_COMMANDS, *_TOOL_COMMANDS))
    lines = [
        f"usage: {DISPLAY_NAME} [-h] [--version] [<subcommand> ...]",
        "",
        "Without a subcommand the MCP server starts (stdio; --http for HTTP).",
        "",
        "operator commands (this machine's credentials and server config):",
        *[f"  {name:<{width}}  {text}" for name, text in _OPERATOR_COMMANDS],
        "",
        "tool commands (the MCP tools, one-shot; add --json for machine output):",
        *[f"  {name:<{width}}  {text}" for name, text in _TOOL_COMMANDS],
        "",
        "Run `<subcommand> --help` for the arguments of one command.",
    ]
    return "\n".join(lines)


# --- entry ---


def _extras() -> dict:
    return {
        "auth": (_configure_auth, _handle_auth),
        # `login` is a deprecated alias of `auth`, kept one release cycle.
        "login": (_configure_login, _handle_login),
        "logout": (_configure_logout, _handle_logout),
        # MCP tools, in the README's tool-table order.
        "message": (_configure_message, _handle_message),
        "chat": (_configure_chat, _handle_chat),
        "media": (_configure_media, _handle_media),
        "contact": (_configure_contact, _handle_contact),
        "settings": (_configure_settings, _handle_settings),
        "help": (_configure_help, _handle_help),
    }


def _version() -> str:
    from telegram import __version__

    return __version__


# hull built-ins that read the default-namespace config blob directly.
_STORE_BUILTINS = frozenset({"config", "status", "doctor"})


def _migrate_legacy_for_builtins(argv: list[str]) -> None:
    """Migrate a pre-hull ``config.enc`` entry before a store built-in runs.

    hull's ``config``/``status``/``doctor`` read only the PerPluginStore, so an
    upgraded install whose credentials still sit in the legacy entry would be
    reported as "not configured" until the server first starts. A failed
    migration is logged by type only and the built-in still runs.
    """
    if not argv or argv[0] not in _STORE_BUILTINS:
        return
    from telegram.credential_state import _read_single_user_config

    try:
        _read_single_user_config()
    except Exception as e:  # unreadable legacy file or store
        print(
            f"warning: legacy credential migration skipped ({type(e).__name__})",
            file=sys.stderr,
        )


def main(argv: list[str] | None = None) -> int:
    from telegram.config import quarantine_foreign_machine_key

    args = sys.argv[1:] if argv is None else argv
    # hull's built-ins (status/config/doctor) open the store directly; move a
    # pre-hull .secret aside first so they do not fail on it.
    quarantine_foreign_machine_key()
    if args in (["-h"], ["--help"]):
        # Operator commands and tool groups are listed separately; hull's own
        # usage prints one flat subcommand list.
        print(_usage())
        return 0
    _migrate_legacy_for_builtins(args)
    return build_cli(
        # The console-script name operators type, matching README and
        # pyproject.toml. The legacy `better-telegram-mcp` script is an alias of
        # this same entry point, so it reports the documented name too.
        DISPLAY_NAME,
        # Credential slug is "telegram", not the display name minus "-mcp", so
        # `config`/`status`/`doctor` read the same store the server writes to
        # (credential_state.PLUGIN_NAME) rather than deriving it from the name.
        plugin_name=PLUGIN_NAME,
        serve=_serve,
        extra=_extras(),
        version=_version(),
    )(argv)
