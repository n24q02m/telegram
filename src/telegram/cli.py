"""Console-script entry: the hull consumer CLI builder.

Bare invocation and any leading-dash argv (``--http``, ``--host``, ``--port``)
start the server; a leading positional argv[0] runs a one-shot operator
subcommand. hull provides ``config``, ``status``, ``doctor`` and
``token hash``; this module adds ``auth`` (``login`` is a deprecated alias)
and replaces ``logout`` so it also revokes and deletes the Telethon session.

``auth`` / ``logout`` act on the machine that hosts the server. ``--user <ns>``
targets one hull namespace: ``default`` (stdio, ``no-auth`` and ``token`` HTTP
modes) or the ``namespace`` of a ``users.toml`` user (``multi`` mode).
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import sys

from hull_core.consumer_cli import build_cli
from hull_core.storage import validate_sub

from telegram.credential_state import DEFAULT_NAMESPACE, PLUGIN_NAME

_MARKER_LEAF = "tokens/app-identity"
_SESSION_LEAF = "session"


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


# --- entry ---


def _extras() -> dict:
    return {
        "auth": (_configure_auth, _handle_auth),
        # `login` is a deprecated alias of `auth`, kept one release cycle.
        "login": (_configure_login, _handle_login),
        "logout": (_configure_logout, _handle_logout),
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
    _migrate_legacy_for_builtins(args)
    return build_cli(
        # Display name kept at the published package's console name
        # (sessions.SERVER_NAME), which is also the key of the legacy
        # credential entry migrated by credential_state.
        "better-telegram-mcp",
        # Credential slug is "telegram", not the console name minus "-mcp"
        # ("better-telegram"), so `config`/`status`/`doctor` read the same
        # store the server writes to (credential_state.PLUGIN_NAME).
        plugin_name=PLUGIN_NAME,
        serve=_serve,
        extra=_extras(),
        version=_version(),
    )(argv)
