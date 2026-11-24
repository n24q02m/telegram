"""UserBackend uses a backend-held StringSession when a credential backend is injected."""

from __future__ import annotations

from pathlib import Path

import pytest
from hull_core.storage import InMemoryBackend, SaveOnChangeStringSession

from telegram.backends.user_backend import UserBackend
from telegram.config import Settings


class FakeStringSessionClient:
    """Stand-in for telethon.TelegramClient that records the session passed in.

    UserBackend.connect() constructs a TelegramClient(session, api_id, api_hash);
    in unit tests we patch TelegramClient with this double so no live MTProto
    socket is opened.
    """

    def __init__(self, session, api_id=None, api_hash=None):
        self.session = session
        self._connected = False
        self._authorized = False

    async def connect(self):
        self._connected = True

    async def disconnect(self):
        self._connected = False

    def is_connected(self):
        return self._connected

    async def is_user_authorized(self):
        return self._authorized


def _settings(tmp_path) -> Settings:
    return Settings(
        api_id=37984984,
        api_hash="2f5f4c76c4de7c07302380c788390100",
        phone="+10000000000",
        session_name="deadbeefdeadbeef",
        data_dir=tmp_path,
    )


async def test_connect_uses_string_session_from_backend(monkeypatch, tmp_path):
    monkeypatch.setenv("CREDENTIAL_SECRET", "test-secret")
    captured = {}

    def _fake_client(session, *a, **kw):
        captured["session"] = session
        return FakeStringSessionClient(session)

    monkeypatch.setattr("telegram.backends.user_backend.TelegramClient", _fake_client)
    backend = UserBackend(_settings(tmp_path), backend=InMemoryBackend())
    await backend.connect()
    # With an injected backend the client is constructed with a SaveOnChangeStringSession,
    # NOT a filesystem path string.
    assert isinstance(captured["session"], SaveOnChangeStringSession)
    # No .session file was created on disk.
    assert not list(tmp_path.glob("*.session"))


async def test_save_on_change_flushes_to_backend(monkeypatch, tmp_path):
    monkeypatch.setenv("CREDENTIAL_SECRET", "test-secret")
    mem = InMemoryBackend()

    def _fake_client(session, *a, **kw):
        return FakeStringSessionClient(session)

    monkeypatch.setattr("telegram.backends.user_backend.TelegramClient", _fake_client)
    backend = UserBackend(_settings(tmp_path), backend=mem)
    await backend.connect()
    # Simulate a Telethon-internal rewrite (DC migration / key rotation).
    backend._client.session.save()  # ty: ignore[missing-union-attribute]
    assert mem.get("telegram/subs/deadbeefdeadbeef/session") is not None


async def test_empty_backend_starts_unauthorized(monkeypatch, tmp_path):
    monkeypatch.setenv("CREDENTIAL_SECRET", "test-secret")

    def _fake_client(session, *a, **kw):
        return FakeStringSessionClient(session)

    monkeypatch.setattr("telegram.backends.user_backend.TelegramClient", _fake_client)
    backend = UserBackend(_settings(tmp_path), backend=InMemoryBackend())
    await backend.connect()
    assert await backend.is_authorized() is False


async def test_local_default_uses_encrypted_string_session_and_migrates_sqlite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Local default mode stores StringSession encrypted and migrates legacy .session non-destructively."""
    from unittest.mock import patch

    from telethon.crypto import AuthKey
    from telethon.sessions import SQLiteSession, StringSession

    from telegram.backends.user_backend import UserBackend
    from telegram.config import Settings

    monkeypatch.delenv("CREDENTIAL_SECRET", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv("USERPROFILE", str(tmp_path / "home"))
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Seed legacy SQLite session with a deterministic valid 256-byte key.
    legacy = SQLiteSession(str(data_dir / "default"))
    legacy.set_dc(2, "149.154.167.40", 443)
    legacy.auth_key = AuthKey(bytes(range(256)))
    expected_str = StringSession.save(legacy)
    legacy.close()
    legacy_file = data_dir / "default.session"
    assert legacy_file.is_file()

    captured: list[object] = []

    class FakeClient:
        def __init__(self, session, api_id, api_hash):
            captured.append(session)
            self.session = session

        async def connect(self):
            return None

        async def is_user_authorized(self):
            return True

        async def log_out(self):
            return True

        async def disconnect(self):
            return None

    settings = Settings(api_id=12345, api_hash="test_hash", data_dir=data_dir)
    backend = UserBackend(settings)
    with patch("telegram.backends.user_backend.TelegramClient", FakeClient):
        await backend.connect()
        assert (data_dir / "session.json").is_file()
        assert legacy_file.is_file()  # Non-destructive: kept on disk.
        assert isinstance(captured[0], StringSession)
        assert backend._session_store().load() == expected_str
        assert await backend.log_out() is True
        assert backend._session_store().load() is None


async def test_local_named_session_uses_profile_and_skips_corrupt_legacy(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Named session uses profiles/<name>/session.json and ignores corrupt legacy .session."""
    from unittest.mock import patch

    from telegram.backends.user_backend import UserBackend
    from telegram.config import Settings

    monkeypatch.delenv("CREDENTIAL_SECRET", raising=False)
    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    corrupt_legacy = data_dir / "account-work.session"
    corrupt_legacy.write_bytes(b"not-a-sqlite-db")

    class FakeClient:
        def __init__(self, session, api_id, api_hash):
            self.session = session

        async def connect(self):
            return None

        async def is_user_authorized(self):
            return False

    settings = Settings(
        api_id=12345,
        api_hash="test_hash",
        data_dir=data_dir,
        session_name="account-work",
    )
    backend = UserBackend(settings)
    with patch("telegram.backends.user_backend.TelegramClient", FakeClient):
        await backend.connect()
    assert corrupt_legacy.is_file()
    assert backend._session_store().load() is None
