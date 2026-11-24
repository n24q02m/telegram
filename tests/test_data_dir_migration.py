"""One-time non-destructive migration to ``~/.n24q02m/telegram/``."""

from __future__ import annotations

from pathlib import Path

from telegram.config import (
    DATA_DIR_NAME,
    LEGACY_DATA_DIR_NAME,
    QUARANTINED_SECRET_NAME,
    Settings,
    resolve_default_data_dir,
)


def _seed_dir(root: Path, *, with_foreign_secret: bool = True) -> Path:
    (root / "user_sessions").mkdir(parents=True, exist_ok=True)
    (root / "default.session").write_bytes(b"telethon-session-bytes")
    if with_foreign_secret:
        (root / ".secret").write_text("ab" * 32)
    (root / "user_sessions" / "sub-1.session").write_bytes(b"per-sub")
    return root


def test_legacy_constant_names():
    assert DATA_DIR_NAME == ".telegram"
    assert LEGACY_DATA_DIR_NAME == ".better-telegram-mcp"


def test_no_dirs_returns_canonical_target_without_creating_it():
    home = Path.home()
    resolved = resolve_default_data_dir()
    assert resolved == home / ".n24q02m" / "telegram"
    assert not resolved.exists()


def test_migrates_legacy_dot_telegram_non_destructively():
    home = Path.home()
    legacy = _seed_dir(home / ".telegram")

    resolved = resolve_default_data_dir()

    target = home / ".n24q02m" / "telegram"
    assert resolved == target
    assert target.is_dir()
    # Non-destructive: legacy files stay intact
    assert (legacy / "default.session").read_bytes() == b"telethon-session-bytes"
    assert (target / "default.session").read_bytes() == b"telethon-session-bytes"
    assert (target / "user_sessions" / "sub-1.session").read_bytes() == b"per-sub"
    assert not (target / ".secret").exists()
    assert (target / QUARANTINED_SECRET_NAME).read_text() == "ab" * 32


def test_migrates_legacy_better_telegram_mcp_when_dot_telegram_absent():
    home = Path.home()
    legacy = _seed_dir(home / LEGACY_DATA_DIR_NAME, with_foreign_secret=False)

    resolved = resolve_default_data_dir()

    target = home / ".n24q02m" / "telegram"
    assert resolved == target
    assert (legacy / "default.session").exists()
    assert (target / "default.session").read_bytes() == b"telethon-session-bytes"


def test_move_is_one_time_and_target_wins():
    home = Path.home()
    _seed_dir(home / ".telegram")
    target = home / ".n24q02m" / "telegram"
    target.mkdir(parents=True)
    (target / "new.session").write_bytes(b"new")

    first = resolve_default_data_dir()
    second = resolve_default_data_dir()

    assert first == second == target
    assert (target / "new.session").read_bytes() == b"new"
    assert not (target / "default.session").exists()


def test_env_overrides_n24q02m_home_xdg_and_data_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC")
    custom_root = tmp_path / "custom-home"
    monkeypatch.setenv("N24Q02M_HOME", str(custom_root))
    assert Settings().data_dir == custom_root / "telegram"

    monkeypatch.delenv("N24Q02M_HOME")
    monkeypatch.setenv("N24Q02M_USE_XDG", "1")
    xdg_data = tmp_path / "xdg-data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg_data))
    assert Settings().data_dir == xdg_data / "n24q02m" / "telegram"

    explicit = tmp_path / "explicit"
    monkeypatch.setenv("TELEGRAM_DATA_DIR", str(explicit))
    assert Settings().data_dir == explicit


def test_check_saved_sessions_uses_canonical_dir(monkeypatch):
    monkeypatch.delenv("MCP_STORAGE_BACKEND", raising=False)
    from telegram.sessions import check_saved_sessions

    home = Path.home()
    _seed_dir(home / ".telegram", with_foreign_secret=False)

    assert check_saved_sessions() is True
    assert (home / ".n24q02m" / "telegram" / "default.session").exists()


def test_check_saved_sessions_honours_data_dir_override(monkeypatch, tmp_path):
    monkeypatch.delenv("MCP_STORAGE_BACKEND", raising=False)
    from telegram.sessions import check_saved_sessions

    custom = tmp_path / "custom"
    custom.mkdir()
    monkeypatch.setenv("TELEGRAM_DATA_DIR", str(custom))

    assert check_saved_sessions() is False
    (custom / "default.session").write_bytes(b"custom-session")
    assert check_saved_sessions() is True
