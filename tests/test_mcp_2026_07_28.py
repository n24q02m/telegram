"""Tests for MCP 2026-07-28 extensions: skills, elicitation fallback, and files."""

from __future__ import annotations

import asyncio
import base64
import json
import os
import socket
import sys
from contextlib import suppress
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import mcp.types as mt
import pytest
import uvicorn
from fastmcp import Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport
from fastmcp.server.elicitation import (
    AcceptedElicitation,
    CancelledElicitation,
    DeclinedElicitation,
)
from fastmcp.skills import SkillsClientExtension
from hull_core.config.settings import HullSettings, ServerSettings
from hull_core.server import FILES_EXTENSION_ID, SKILLS_EXTENSION_ID
from hull_core.server.http import build_http_app
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.streamable_http import streamable_http_client

import telegram.extensions as ext_mod
import telegram.server as srv
from telegram.config import Settings

_STDIO_SERVER_SCRIPT = """
import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import telegram.server as srv
from telegram.config import Settings

media_path = Path(os.environ["TELEGRAM_TEST_MEDIA_PATH"])
audit_path = Path(os.environ["TELEGRAM_TEST_AUDIT_PATH"])


def _record(name, *args, **kwargs):
    with audit_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps({"method": name, "args": list(args), "kwargs": kwargs}) + "\\n")


backend = MagicMock()
backend.connect = AsyncMock()
backend.disconnect = AsyncMock()
backend.is_authorized = AsyncMock(return_value=True)


async def _delete_message(chat_id, message_id):
    _record("delete_message", chat_id, message_id)
    return True


async def _leave_chat(chat_id):
    _record("leave_chat", chat_id)
    return True


async def _promote_admin(chat_id, user_id, demote=False):
    _record("promote_admin", chat_id, user_id, demote=demote)
    return True


async def _block_user(user_id, unblock=False):
    _record("block_user", user_id, unblock=unblock)
    return True


async def _download_media(chat_id, message_id, output_dir=None, file_id=None):
    _record("download_media", chat_id, message_id, output_dir=output_dir, file_id=file_id)
    return str(media_path)


backend.delete_message = AsyncMock(side_effect=_delete_message)
backend.leave_chat = AsyncMock(side_effect=_leave_chat)
backend.promote_admin = AsyncMock(side_effect=_promote_admin)
backend.block_user = AsyncMock(side_effect=_block_user)
backend.download_media = AsyncMock(side_effect=_download_media)

srv._ensure_settings = lambda: Settings(bot_token="123456:TESTTOKEN")
srv._create_backend_instance = lambda settings: backend
srv.mcp.run(transport="stdio", show_banner=False)
"""


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _write_stdio_script(tmp_path: Path) -> tuple[Path, Path, Path]:
    media_file = tmp_path / "sample.png"
    media_bytes = b"\x89PNG\r\n\x1a\nfake-png-payload"
    media_file.write_bytes(media_bytes)
    audit_file = tmp_path / "audit.jsonl"
    script_file = tmp_path / "stdio_mock_server.py"
    script_file.write_text(_STDIO_SERVER_SCRIPT, encoding="utf-8")
    return script_file, media_file, audit_file


def _read_audit(audit_file: Path) -> list[dict]:
    if not audit_file.exists():
        return []
    return [
        json.loads(line)
        for line in audit_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _read_text(res: mt.ReadResourceResult) -> str:
    item = res.contents[0]
    assert isinstance(item, mt.TextResourceContents)
    return item.text


def _make_mock_backend(media_path: Path) -> MagicMock:
    backend = MagicMock()
    backend.connect = AsyncMock()
    backend.disconnect = AsyncMock()
    backend.is_authorized = AsyncMock(return_value=True)
    backend.delete_message = AsyncMock(return_value=True)
    backend.leave_chat = AsyncMock(return_value=True)
    backend.promote_admin = AsyncMock(return_value=True)
    backend.block_user = AsyncMock(return_value=True)
    backend.download_media = AsyncMock(return_value=str(media_path))
    return backend


# --- Unit tests for telegram.extensions & resources ---


def test_resolve_skills_dir_prefers_package_then_repo(monkeypatch, tmp_path):
    fake_pkg = tmp_path / "pkg" / "telegram"
    fake_pkg.mkdir(parents=True)
    fake_file = fake_pkg / "extensions.py"
    fake_file.write_text("", encoding="utf-8")
    pkg_skills = fake_pkg / "skills"
    pkg_skills.mkdir()

    monkeypatch.setattr(ext_mod, "__file__", str(fake_file))
    assert ext_mod.resolve_skills_dir() == pkg_skills

    pkg_skills.rmdir()
    assert ext_mod.resolve_skills_dir() is None


def test_attach_bundled_skills_skips_when_missing(monkeypatch):
    monkeypatch.setattr(ext_mod, "resolve_skills_dir", lambda: None)
    assert ext_mod.attach_bundled_skills(MagicMock()) is None


def test_client_supports_extension_variants():
    assert ext_mod.client_supports_extension(None, FILES_EXTENSION_ID) is False
    assert (
        ext_mod.client_supports_extension(
            SimpleNamespace(session=None), FILES_EXTENSION_ID
        )
        is False
    )

    session_params = SimpleNamespace(
        client_params=SimpleNamespace(
            capabilities=SimpleNamespace(extensions={FILES_EXTENSION_ID: {}})
        )
    )
    assert (
        ext_mod.client_supports_extension(
            SimpleNamespace(session=session_params), FILES_EXTENSION_ID
        )
        is True
    )
    assert (
        ext_mod.client_supports_extension(
            SimpleNamespace(session=session_params), SKILLS_EXTENSION_ID
        )
        is False
    )

    session_caps = SimpleNamespace(
        client_params=None,
        client_capabilities=SimpleNamespace(extensions={SKILLS_EXTENSION_ID: {}}),
    )
    assert (
        ext_mod.client_supports_extension(
            SimpleNamespace(session=session_caps), SKILLS_EXTENSION_ID
        )
        is True
    )


@pytest.mark.asyncio
async def test_confirm_sensitive_action_cli_and_elicit_paths(monkeypatch):
    monkeypatch.setattr(ext_mod, "get_active_context", lambda: None)
    confirmed_yes, outcome_yes = await ext_mod.confirm_sensitive_action(
        "Delete?", cli_prompt=lambda _: True
    )
    assert confirmed_yes is True
    assert outcome_yes.used_fallback is True
    assert outcome_yes.reason == "cli_fallback"

    confirmed_no, outcome_no = await ext_mod.confirm_sensitive_action(
        "Delete?", cli_prompt=lambda _: False
    )
    assert confirmed_no is False
    assert outcome_no.status == "declined"

    confirmed_headless, outcome_headless = await ext_mod.confirm_sensitive_action(
        "Delete?", default=True
    )
    assert confirmed_headless is True
    assert outcome_headless.status == "fallback"

    fake_ctx = SimpleNamespace(
        elicit=AsyncMock(return_value=AcceptedElicitation(data=False))
    )
    monkeypatch.setattr(ext_mod, "get_active_context", lambda: fake_ctx)
    confirmed_false, outcome_false = await ext_mod.confirm_sensitive_action("Delete?")
    assert confirmed_false is False
    assert outcome_false.status == "accepted"

    fake_ctx.elicit = AsyncMock(return_value=DeclinedElicitation())
    confirmed_dec, outcome_dec = await ext_mod.confirm_sensitive_action("Delete?")
    assert confirmed_dec is False
    assert outcome_dec.status == "declined"

    fake_ctx.elicit = AsyncMock(return_value=CancelledElicitation())
    confirmed_can, outcome_can = await ext_mod.confirm_sensitive_action("Delete?")
    assert confirmed_can is False
    assert outcome_can.status == "cancelled"


def test_build_media_resource_data_with_and_without_files(tmp_path):
    sample = tmp_path / "photo.png"
    sample.write_bytes(b"png-bytes")

    with_files = ext_mod.build_media_resource_data(
        sample, uri="telegram://media/1/2", files_supported=True
    )
    assert with_files["extension"] == FILES_EXTENSION_ID
    assert with_files["files_supported"] is True
    assert with_files["mimeType"] == "image/png"
    assert with_files["sizeBytes"] == 9
    assert base64.b64decode(with_files["resource"]["blob"]) == b"png-bytes"

    without_files = ext_mod.build_media_resource_data(
        sample, uri="telegram://media/1/2", files_supported=False
    )
    assert without_files["extension"] is None
    assert without_files["files_supported"] is False
    assert without_files["sizeBytes"] == 9
    assert "resource" not in without_files


def test_enrich_media_download_result_guards():
    assert ext_mod.enrich_media_download_result({}, chat_id=1, message_id=2) == {}
    assert ext_mod.enrich_media_download_result(
        {"path": "/tmp/x.jpg"}, chat_id=1, message_id=2
    ) == {"path": "/tmp/x.jpg"}


@pytest.mark.asyncio
async def test_media_resource_error_paths(monkeypatch, tmp_path):
    media_res = (
        await srv.mcp.get_resource_template("telegram://media/{chat_id}/{message_id}")
    ).fn

    old_b, old_p, old_u = srv._backend, srv._pending_auth, srv._unconfigured
    try:
        srv._backend = None
        srv._pending_auth = False
        srv._unconfigured = True
        unconf = json.loads(await media_res("123", "1"))
        assert unconf["error"] == "Not configured"

        backend = _make_mock_backend(tmp_path / "a.bin")
        srv._backend = backend
        srv._unconfigured = False
        bad_id = json.loads(await media_res("@chan", "not-an-int"))
        assert "Invalid message_id" in bad_id["error"]

        backend.download_media = AsyncMock(
            side_effect=NotImplementedError("file_id required")
        )
        err_res = json.loads(await media_res("@chan", "99"))
        assert "file_id required" in err_res["error"]
    finally:
        srv._backend, srv._pending_auth, srv._unconfigured = old_b, old_p, old_u


# --- Real E2E over stdio ---


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_stdio_e2e_skills_2026_07_28(tmp_path):
    script_file, media_file, audit_file = _write_stdio_script(tmp_path)
    env = {
        **os.environ,
        "TELEGRAM_TEST_MEDIA_PATH": str(media_file),
        "TELEGRAM_TEST_AUDIT_PATH": str(audit_file),
        "PYTHONIOENCODING": "utf-8",
    }
    transport = StdioTransport(
        command=sys.executable,
        args=[str(script_file)],
        env=env,
    )
    async with Client(transport, extensions=[SkillsClientExtension()]) as client:
        skills = await client.list_skills()
        names = {s.frontmatter.root["name"] for s in skills}
        assert {"channel-post", "setup-bot"}.issubset(names)

        skill_doc = await client.get_skill("skill://channel-post/SKILL.md")
        assert skill_doc is not None
        res_blocks = await client.read_resource("skill://channel-post/SKILL.md")
        assert "channel-post" in res_blocks[0].text

        # On MCP 2026-07-28, ctx.elicit triggers fallback=True seamlessly
        del_res = await client.call_tool(
            "message", {"action": "delete", "chat_id": 100, "message_id": 7}
        )
        assert del_res.structured_content["deleted"] is True

    calls = [c["method"] for c in _read_audit(audit_file)]
    assert "delete_message" in calls


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_stdio_e2e_clientsession_elicitation_and_files(tmp_path):
    script_file, media_file, audit_file = _write_stdio_script(tmp_path)
    env = {
        **os.environ,
        "TELEGRAM_TEST_MEDIA_PATH": str(media_file),
        "TELEGRAM_TEST_AUDIT_PATH": str(audit_file),
        "PYTHONIOENCODING": "utf-8",
    }
    params = StdioServerParameters(
        command=sys.executable, args=[str(script_file)], env=env
    )

    # 1. Declining & accepting elicitation via real ClientSession over stdio
    prompts_seen: list[str] = []

    async def decline_then_accept_elicit(_ctx, params):
        prompts_seen.append(params.message)
        if "Delete message" in params.message or "Leave chat" in params.message:
            return mt.ElicitResult(action="decline")
        if "Promote user" in params.message:
            return mt.ElicitResult(action="cancel")
        if "Block user" in params.message:
            return mt.ElicitResult(action="accept", content={"value": False})
        return mt.ElicitResult(action="accept", content={"value": True})

    async with stdio_client(params) as (read_s, write_s):
        async with ClientSession(
            read_s,
            write_s,
            elicitation_callback=decline_then_accept_elicit,
            extensions={FILES_EXTENSION_ID: {}},
        ) as session:
            await session.initialize()

            # skill:// resources over ClientSession
            resources = await session.list_resources()
            uris = {str(r.uri) for r in resources.resources}
            assert "skill://setup-bot/SKILL.md" in uris
            skill_read = await session.read_resource("skill://setup-bot/SKILL.md")
            assert "setup-bot" in _read_text(skill_read)

            # Declined / cancelled / False sensitive ops do NOT call backend
            r_del = await session.call_tool(
                "message", {"action": "delete", "chat_id": 10, "message_id": 20}
            )
            assert r_del.structured_content["cancelled"] is True
            assert r_del.structured_content["confirmed"] is False

            r_leave = await session.call_tool(
                "chat", {"action": "leave", "chat_id": 10}
            )
            assert r_leave.structured_content["cancelled"] is True

            r_admin = await session.call_tool(
                "chat", {"action": "admin", "chat_id": 10, "user_id": 55}
            )
            assert r_admin.structured_content["cancelled"] is True

            r_block = await session.call_tool(
                "contact", {"action": "block", "user_id": 99}
            )
            assert r_block.structured_content["cancelled"] is True

            # Media download + telegram://media resource with io.modelcontextprotocol/files
            dl = await session.call_tool(
                "media", {"action": "download", "chat_id": 123, "message_id": 42}
            )
            assert dl.structured_content["files_supported"] is True
            assert dl.structured_content["file"]["extension"] == FILES_EXTENSION_ID
            assert (
                base64.b64decode(dl.structured_content["file"]["resource"]["blob"])
                == media_file.read_bytes()
            )

            media_read = await session.read_resource("telegram://media/123/42")
            media_json = json.loads(_read_text(media_read))
            assert media_json["extension"] == FILES_EXTENSION_ID
            assert media_json["mimeType"] == "image/png"

    assert len(prompts_seen) == 4
    audited = [c["method"] for c in _read_audit(audit_file)]
    assert "delete_message" not in audited
    assert "leave_chat" not in audited
    assert "promote_admin" not in audited
    assert "block_user" not in audited
    assert audited.count("download_media") == 2


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_stdio_e2e_headless_fallback_and_no_files(tmp_path):
    script_file, media_file, audit_file = _write_stdio_script(tmp_path)
    env = {
        **os.environ,
        "TELEGRAM_TEST_MEDIA_PATH": str(media_file),
        "TELEGRAM_TEST_AUDIT_PATH": str(audit_file),
        "PYTHONIOENCODING": "utf-8",
    }
    params = StdioServerParameters(
        command=sys.executable, args=[str(script_file)], env=env
    )

    async with stdio_client(params) as (read_s, write_s):
        async with ClientSession(read_s, write_s) as headless_session:
            await headless_session.initialize()
            r_del_ok = await headless_session.call_tool(
                "message", {"action": "delete", "chat_id": 10, "message_id": 21}
            )
            assert r_del_ok.structured_content["deleted"] is True

            dl_fallback = await headless_session.call_tool(
                "media", {"action": "download", "chat_id": 123, "message_id": 42}
            )
            assert dl_fallback.structured_content["files_supported"] is False
            assert "file" not in dl_fallback.structured_content

            media_fb = await headless_session.read_resource("telegram://media/123/42")
            fb_json = json.loads(_read_text(media_fb))
            assert fb_json["files_supported"] is False
            assert fb_json["extension"] is None
            assert "resource" not in fb_json


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_stdio_e2e_elicitation_accept(tmp_path):
    script_file, media_file, audit_file = _write_stdio_script(tmp_path)
    env = {
        **os.environ,
        "TELEGRAM_TEST_MEDIA_PATH": str(media_file),
        "TELEGRAM_TEST_AUDIT_PATH": str(audit_file),
        "PYTHONIOENCODING": "utf-8",
    }
    params = StdioServerParameters(
        command=sys.executable, args=[str(script_file)], env=env
    )

    async def accept_all_elicit(_ctx, params):
        return mt.ElicitResult(action="accept", content={"value": True})

    async with stdio_client(params) as (read_s, write_s):
        async with ClientSession(
            read_s, write_s, elicitation_callback=accept_all_elicit
        ) as accept_session:
            await accept_session.initialize()
            r_leave_ok = await accept_session.call_tool(
                "chat", {"action": "leave", "chat_id": 11}
            )
            assert r_leave_ok.structured_content["left"] is True
            r_admin_ok = await accept_session.call_tool(
                "chat",
                {"action": "admin", "chat_id": 11, "user_id": 77, "demote": True},
            )
            assert r_admin_ok.structured_content["demoted"] is True
            r_block_ok = await accept_session.call_tool(
                "contact", {"action": "block", "user_id": 88}
            )
            assert r_block_ok.structured_content["blocked"] is True


# --- Real E2E over Streamable HTTP ---


@pytest.mark.asyncio
@pytest.mark.timeout(90)
async def test_streamable_http_e2e_skills_elicitation_and_files(tmp_path):
    media_file = tmp_path / "http_sample.png"
    media_bytes = b"\x89PNG\r\n\x1a\nhttp-media"
    media_file.write_bytes(media_bytes)
    backend = _make_mock_backend(media_file)

    old_b, old_s, old_p, old_u, old_ens, old_create = (
        srv._backend,
        srv._settings,
        srv._pending_auth,
        srv._unconfigured,
        srv._ensure_settings,
        srv._create_backend_instance,
    )
    srv._ensure_settings = lambda: Settings(bot_token="123456:HTTPTOKEN")
    srv._create_backend_instance = lambda _settings: backend
    srv._backend = backend
    srv._settings = Settings(bot_token="123456:HTTPTOKEN")
    srv._pending_auth = False
    srv._unconfigured = False

    port = _free_port()
    app = build_http_app(
        srv.mcp,
        HullSettings(config_dir=tmp_path, server=ServerSettings(auth="no-auth")),
    )
    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error")
    server = uvicorn.Server(config)
    serve_task = asyncio.create_task(server.serve())
    try:
        for _ in range(100):
            if server.started:
                break
            await asyncio.sleep(0.05)
        assert server.started
        url = f"http://127.0.0.1:{port}/mcp"

        # 1. FastMCP Client over Streamable HTTP with SkillsClientExtension (2026-07-28)
        async with Client(
            StreamableHttpTransport(url),
            extensions=[SkillsClientExtension()],
        ) as http_client:
            skills = await http_client.list_skills()
            names = {s.frontmatter.root["name"] for s in skills}
            assert {"channel-post", "setup-bot"}.issubset(names)
            skill_res = await http_client.read_resource("skill://setup-bot/SKILL.md")
            assert "setup-bot" in skill_res[0].text

        # 2. ClientSession over Streamable HTTP with elicitation + files extension
        async def http_elicit(_ctx, params):
            if "Leave chat" in params.message:
                return mt.ElicitResult(action="decline")
            return mt.ElicitResult(action="accept", content={"value": True})

        async with streamable_http_client(url) as (read_s, write_s):
            async with ClientSession(
                read_s,
                write_s,
                elicitation_callback=http_elicit,
                extensions={FILES_EXTENSION_ID: {}},
            ) as session:
                await session.initialize()

                # Declined leave aborts without calling backend.leave_chat
                res_leave = await session.call_tool(
                    "chat", {"action": "leave", "chat_id": 500}
                )
                assert res_leave.structured_content["cancelled"] is True
                backend.leave_chat.assert_not_awaited()

                # Accepted delete calls backend.delete_message
                res_del = await session.call_tool(
                    "message", {"action": "delete", "chat_id": 500, "message_id": 1}
                )
                assert res_del.structured_content["deleted"] is True
                backend.delete_message.assert_awaited_once_with(500, 1)

                # files extension payload over Streamable HTTP
                dl = await session.call_tool(
                    "media", {"action": "download", "chat_id": 500, "message_id": 2}
                )
                assert dl.structured_content["file"]["extension"] == FILES_EXTENSION_ID
                assert (
                    base64.b64decode(dl.structured_content["file"]["resource"]["blob"])
                    == media_bytes
                )
                media_res = await session.read_resource("telegram://media/500/2")
                assert (
                    json.loads(_read_text(media_res))["extension"] == FILES_EXTENSION_ID
                )

        # 3. ClientSession over Streamable HTTP WITHOUT files extension (graceful fallback)
        async with streamable_http_client(url) as (read_s, write_s):
            async with ClientSession(read_s, write_s) as fallback_session:
                await fallback_session.initialize()
                dl_fb = await fallback_session.call_tool(
                    "media", {"action": "download", "chat_id": 500, "message_id": 2}
                )
                assert dl_fb.structured_content["files_supported"] is False
                assert "file" not in dl_fb.structured_content
    finally:
        server.should_exit = True
        with suppress(asyncio.CancelledError):
            await serve_task
        (
            srv._backend,
            srv._settings,
            srv._pending_auth,
            srv._unconfigured,
            srv._ensure_settings,
            srv._create_backend_instance,
        ) = (
            old_b,
            old_s,
            old_p,
            old_u,
            old_ens,
            old_create,
        )
