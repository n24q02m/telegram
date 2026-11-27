"""MCP 2026-07-28 extension helpers: skills, elicitation fallback, and files."""

from __future__ import annotations

import logging
import mimetypes
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_context
from hull_core.server import (
    FILES_EXTENSION_ID,
    SKILLS_EXTENSION_ID,
    ElicitationOutcome,
    attach_skills_provider,
    build_file_payload,
    elicit_with_fallback,
)

logger = logging.getLogger(__name__)


def resolve_skills_dir() -> Path | None:
    """Locate bundled skills either inside the installed package or repo root."""
    package_skills = Path(__file__).resolve().parent / "skills"
    if package_skills.is_dir():
        return package_skills
    repo_skills = Path(__file__).resolve().parents[2] / "skills"
    if repo_skills.is_dir():
        return repo_skills
    return None


def attach_bundled_skills(mcp_server: FastMCP) -> Any | None:
    """Attach the ``io.modelcontextprotocol/skills`` provider when available."""
    skills_dir = resolve_skills_dir()
    if skills_dir is None:
        logger.warning("Skills directory not found; skipping SkillsDirectoryProvider")
        return None
    return attach_skills_provider(mcp_server, skills_dir)


def get_active_context() -> Any | None:
    """Return the active FastMCP request context, or ``None`` outside a request."""
    try:
        return get_context()
    except RuntimeError:
        return None


def _read_session_extensions(session: Any) -> Mapping[str, Any] | None:
    for container_attr in ("client_params", "client_capabilities"):
        container = getattr(session, container_attr, None)
        if container is None:
            continue
        caps = getattr(container, "capabilities", container)
        extensions = getattr(caps, "extensions", None)
        if isinstance(extensions, Mapping):
            return extensions
    return None


def client_supports_extension(ctx: Any, extension_id: str) -> bool:
    """Return ``True`` when the active MCP client advertised *extension_id*."""
    if ctx is None:
        return False
    session = getattr(ctx, "session", None)
    if session is None:
        return False
    extensions = _read_session_extensions(session)
    if not extensions:
        return False
    return extension_id in extensions


async def confirm_sensitive_action(
    prompt: str,
    *,
    default: bool = True,
    title: str = "Confirm sensitive Telegram action",
    description: str = "Approve or decline this Telegram operation.",
    cli_prompt: Callable[[str], bool] | None = None,
) -> tuple[bool, ElicitationOutcome[Any]]:
    """Request interactive confirmation via MCP elicitation with headless/CLI fallback."""
    ctx = get_active_context()
    outcome = await elicit_with_fallback(
        ctx,
        prompt,
        bool,
        default=default,
        response_title=title,
        response_description=description,
    )
    if outcome.status == "accepted":
        return bool(outcome.data), outcome
    if outcome.status in ("declined", "cancelled"):
        return False, outcome
    if ctx is None and cli_prompt is not None:
        confirmed = bool(cli_prompt(prompt))
        return confirmed, ElicitationOutcome(
            status="accepted" if confirmed else "declined",
            data=confirmed,
            used_fallback=True,
            reason="cli_fallback",
        )
    resolved = default if outcome.data is None else bool(outcome.data)
    return resolved, outcome


def build_media_resource_data(
    file_path: str | Path,
    *,
    uri: str,
    description: str | None = None,
    files_supported: bool | None = None,
) -> dict[str, Any]:
    """Build an ``io.modelcontextprotocol/files`` payload or graceful fallback."""
    path_obj = Path(file_path)
    if files_supported is None:
        files_supported = client_supports_extension(
            get_active_context(), FILES_EXTENSION_ID
        )
    if files_supported and path_obj.is_file():
        data = path_obj.read_bytes()
        payload = build_file_payload(
            data,
            filename=path_obj.name,
            uri=uri,
            description=description,
        )
        return {
            **payload,
            "path": str(path_obj),
            "resource_uri": uri,
            "files_supported": True,
        }

    guessed_mime = mimetypes.guess_type(path_obj.name)[0] or "application/octet-stream"
    size_bytes = path_obj.stat().st_size if path_obj.is_file() else None
    fallback: dict[str, Any] = {
        "extension": None,
        "files_supported": False,
        "path": str(file_path),
        "filename": path_obj.name,
        "mimeType": guessed_mime,
        "resource_uri": uri,
    }
    if size_bytes is not None:
        fallback["sizeBytes"] = size_bytes
    return fallback


def enrich_media_download_result(
    result: dict[str, Any],
    *,
    chat_id: int | str | None,
    message_id: int | None,
) -> dict[str, Any]:
    """Attach MCP ``files`` metadata or resource reference to a download tool result."""
    raw_path = result.get("path")
    if not isinstance(raw_path, str) or not raw_path:
        return result
    ctx = get_active_context()
    if ctx is None:
        return result
    path_obj = Path(raw_path)
    uri = (
        f"telegram://media/{chat_id}/{message_id}"
        if chat_id is not None and message_id is not None
        else f"file:///{path_obj.name}"
    )
    files_supported = client_supports_extension(ctx, FILES_EXTENSION_ID)
    enriched = dict(result)
    enriched["resource_uri"] = uri
    enriched["files_supported"] = files_supported
    if files_supported and path_obj.is_file():
        enriched["file"] = build_file_payload(
            path_obj.read_bytes(),
            filename=path_obj.name,
            uri=uri,
        )
    return enriched


__all__ = [
    "FILES_EXTENSION_ID",
    "SKILLS_EXTENSION_ID",
    "attach_bundled_skills",
    "build_media_resource_data",
    "client_supports_extension",
    "confirm_sensitive_action",
    "enrich_media_download_result",
    "get_active_context",
    "resolve_skills_dir",
]
