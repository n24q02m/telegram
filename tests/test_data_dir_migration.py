"""One-time move of the pre-rename data dir (~/.better-telegram-mcp -> ~/.telegram).

The autouse ``_isolate_per_plugin_home`` fixture points HOME/USERPROFILE at a
per-test tmp dir, and each test additionally pins ``Path.home()`` to its own
``tmp_path`` so the real home directory is never touched.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from telegram import config as config_mod
from telegram.config import (
    DATA_DIR_NAME,
    LEGACY_DATA_DIR_NAME,
    QUARANTINED_SECRET_NAME,
    Settings,
    resolve_default_data_dir,
)


@pytest.fixture
def home(tmp_path, monkeypatch) -> Path:
    monkeypatch.setattr("pathlib.Path.home", lambda: tmp_path)
    return tmp_path


def _seed_legacy(home: Path) -> Path:
    legacy = home / LEGACY_DATA_DIR_NAME
    (legacy / "user_sessions").mkdir(parents=True)
    (legacy / "default.session").write_bytes(b"telethon-session-bytes")
    (legacy / ".secret").write_text("ab" * 32)
    (legacy / "user_sessions" / "sub-1.session").write_bytes(b"per-sub")
    return legacy


def test_names():
    assert DATA_DIR_NAME == ".telegram"
    assert LEGACY_DATA_DIR_NAME == ".better-telegram-mcp"


def test_no_dirs_returns_target_without_creating_it(home):
    resolved = resolve_default_data_dir()
    assert resolved == home / ".telegram"
    assert not resolved.exists()
    assert not (home / ".better-telegram-mcp").exists()


def test_legacy_only_is_moved_and_read_back(home):
    _seed_legacy(home)

    resolved = resolve_default_data_dir()

    target = home / ".telegram"
    assert resolved == target
    assert target.is_dir()
    assert not (home / ".better-telegram-mcp").exists()
    # Contents preserved byte-for-byte. The pre-hull 64-hex-char ``.secret``
    # is not a hull machine key, so it is renamed aside (never read or
    # deleted) to free hull's machine-key path.
    assert (target / "default.session").read_bytes() == b"telethon-session-bytes"
    assert not (target / ".secret").exists()
    assert (target / QUARANTINED_SECRET_NAME).read_text() == "ab" * 32
    assert (target / "user_sessions" / "sub-1.session").read_bytes() == b"per-sub"


def test_move_is_one_time(home):
    _seed_legacy(home)
    first = resolve_default_data_dir()
    second = resolve_default_data_dir()
    assert first == second == home / ".telegram"
    assert not (home / ".better-telegram-mcp").exists()


def test_rename_failure_falls_back_to_legacy(home, monkeypatch):
    legacy = _seed_legacy(home)

    def _boom(src, dst):
        raise PermissionError("file in use")

    monkeypatch.setattr(config_mod.os, "rename", _boom)

    resolved = resolve_default_data_dir()

    assert resolved == legacy
    assert (legacy / "default.session").exists()
    assert not (home / ".telegram").exists()


def test_readback_mismatch_falls_back_to_legacy(home, monkeypatch):
    legacy = _seed_legacy(home)
    # A rename that reports success but leaves nothing moved.
    monkeypatch.setattr(config_mod.os, "rename", lambda src, dst: None)

    resolved = resolve_default_data_dir()

    assert resolved == legacy
    assert (legacy / "default.session").exists()


def test_readback_mismatch_without_legacy_returns_target(home, monkeypatch):
    legacy = _seed_legacy(home)

    def _vanish(src, dst):
        # Source disappears but the target never materialises.
        shutil.rmtree(src)

    monkeypatch.setattr(config_mod.os, "rename", _vanish)

    resolved = resolve_default_data_dir()

    assert resolved == home / ".telegram"
    assert not legacy.exists()


def test_both_exist_target_with_state_wins(home):
    legacy = _seed_legacy(home)
    target = home / ".telegram"
    target.mkdir()
    (target / "new.session").write_bytes(b"new")

    resolved = resolve_default_data_dir()

    assert resolved == target
    # Legacy left untouched -- no merge, no deletion.
    assert (legacy / "default.session").exists()


@pytest.mark.parametrize("marker", [".secret", "user_sessions"])
def test_both_exist_target_state_markers(home, marker):
    _seed_legacy(home)
    target = home / ".telegram"
    target.mkdir()
    if marker == "user_sessions":
        (target / marker).mkdir()
    else:
        (target / marker).write_text("x")

    assert resolve_default_data_dir() == target


def test_both_exist_unrelated_target_keeps_legacy(home):
    legacy = _seed_legacy(home)
    target = home / ".telegram"
    target.mkdir()
    (target / "unrelated.txt").write_text("someone else's dir")

    resolved = resolve_default_data_dir()

    assert resolved == legacy
    assert (target / "unrelated.txt").exists()
    assert (legacy / "default.session").exists()


def test_settings_default_uses_migrated_dir(home, monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    _seed_legacy(home)

    s = Settings()

    assert s.data_dir == home / ".telegram"
    assert s.session_path == home / ".telegram" / "default.session"
    assert s.session_path.read_bytes() == b"telethon-session-bytes"


def test_settings_env_override_bypasses_migration(home, monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    legacy = _seed_legacy(home)
    custom = tmp_path / "custom"
    monkeypatch.setenv("TELEGRAM_DATA_DIR", str(custom))

    s = Settings()

    assert s.data_dir == custom
    # Explicit override: nothing moved.
    assert legacy.exists()
    assert not (home / ".telegram").exists()


def test_check_saved_sessions_after_migration(home, monkeypatch):
    monkeypatch.delenv("MCP_STORAGE_BACKEND", raising=False)
    from telegram.sessions import check_saved_sessions

    _seed_legacy(home)

    assert check_saved_sessions() is True
    assert (home / ".telegram" / "default.session").exists()
    assert not (home / ".better-telegram-mcp").exists()


def test_check_saved_sessions_honours_data_dir_override(home, monkeypatch, tmp_path):
    # The server reads and writes sessions under TELEGRAM_DATA_DIR, so the
    # saved-session probe must look there too -- and must not move the
    # legacy default dir as a side effect of an explicit override.
    monkeypatch.delenv("MCP_STORAGE_BACKEND", raising=False)
    from telegram.sessions import check_saved_sessions

    legacy = _seed_legacy(home)
    custom = tmp_path / "custom"
    custom.mkdir()
    monkeypatch.setenv("TELEGRAM_DATA_DIR", str(custom))

    assert check_saved_sessions() is False

    (custom / "default.session").write_bytes(b"custom-session")
    assert check_saved_sessions() is True
    assert legacy.exists()
    assert not (home / ".telegram").exists()
