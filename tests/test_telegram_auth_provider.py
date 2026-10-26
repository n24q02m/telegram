"""Per-namespace backends for hull's ``multi`` HTTP mode.

``TelegramAuthProvider`` keeps one connected backend per non-default
namespace. Credentials come from ``telegram auth --user <ns>`` (the
``subs/<ns>/config`` PerPluginStore leaf); no network call is made here: the
backend factory is replaced by an in-memory double.
"""

from __future__ import annotations

import asyncio

import pytest

from telegram.auth import telegram_auth_provider as tap
from telegram.auth.telegram_auth_provider import (
    TelegramAuthProvider,
    create_backend,
    get_provider,
    namespace_data_dir,
    set_global_provider,
    settings_for_namespace,
)
from telegram.backends.bot_backend import BotBackend
from telegram.backends.user_backend import UserBackend
from telegram.credential_state import _write_single_user_config
from tests.conftest import MockBackend

# Fake tokens with the real shape (``<bot id>:<35+ char secret>``), so the
# redaction regex applies to them.
FAKE_TOKEN_A = "111111:" + "A" * 35
FAKE_TOKEN_B = "222222:" + "B" * 35


class _Factory:
    """Backend factory double that records (namespace, settings) per build."""

    def __init__(self, *, authorized: bool = True, connect_error=None) -> None:
        self.calls: list[tuple[str, object]] = []
        self.built: dict[str, MockBackend] = {}
        self._authorized = authorized
        self._connect_error = connect_error

    def __call__(self, settings, namespace):
        backend = MockBackend(settings.mode)
        backend.is_authorized.return_value = self._authorized
        if self._connect_error is not None:
            backend.connect.side_effect = self._connect_error
        self.calls.append((namespace, settings))
        self.built[namespace] = backend
        return backend


def _save_bot(namespace: str, token: str) -> None:
    _write_single_user_config({"TELEGRAM_BOT_TOKEN": token}, namespace)


def _save_phone(namespace: str, phone: str = "+10000000000") -> None:
    _write_single_user_config({"TELEGRAM_PHONE": phone}, namespace)


# --- module helpers ---


def test_get_provider_is_a_lazy_singleton():
    first = get_provider()
    assert isinstance(first, TelegramAuthProvider)
    assert get_provider() is first
    replacement = TelegramAuthProvider()
    set_global_provider(replacement)
    assert get_provider() is replacement


def test_namespace_data_dir_nests_under_subs(_isolate_per_plugin_home):
    path = namespace_data_dir("alice")
    assert path.parts[-2:] == ("subs", "alice")
    assert str(path).startswith(str(_isolate_per_plugin_home))


@pytest.mark.parametrize("bad", ["../escape", "a/b", ""])
def test_namespace_data_dir_rejects_unsafe_names(bad):
    with pytest.raises(ValueError):
        namespace_data_dir(bad)


def test_settings_for_namespace_none_without_credentials():
    assert settings_for_namespace("nobody") is None


def test_settings_for_namespace_none_for_config_without_credential():
    _write_single_user_config({"TELEGRAM_SESSION_NAME": "x"}, "partial")
    assert settings_for_namespace("partial") is None


def test_settings_for_namespace_bot():
    _save_bot("a", FAKE_TOKEN_A)
    settings = settings_for_namespace("a")
    assert settings is not None
    assert settings.mode == "bot"
    assert settings.bot_token == FAKE_TOKEN_A
    assert settings.data_dir == namespace_data_dir("a")


def test_settings_for_namespace_user():
    _save_phone("u")
    settings = settings_for_namespace("u")
    assert settings is not None
    assert settings.mode == "user"
    assert settings.data_dir == namespace_data_dir("u")


def test_namespace_config_does_not_leak_into_default():
    from telegram.credential_state import _read_single_user_config

    _save_bot("a", FAKE_TOKEN_A)
    assert _read_single_user_config() is None
    assert settings_for_namespace("b") is None


def test_create_backend_bot():
    _save_bot("a", FAKE_TOKEN_A)
    settings = settings_for_namespace("a")
    assert settings is not None
    assert isinstance(create_backend(settings, "a"), BotBackend)


def test_create_backend_user_uses_namespace():
    _save_phone("u")
    settings = settings_for_namespace("u")
    assert settings is not None
    backend = create_backend(settings, "u")
    assert isinstance(backend, UserBackend)


# --- TelegramAuthProvider.get ---


async def test_get_returns_none_without_credentials():
    factory = _Factory()
    provider = TelegramAuthProvider(factory=factory)
    assert await provider.get("nobody") is None
    assert factory.calls == []
    assert provider.active_clients == {}


async def test_get_connects_bot_backend_and_caches_it():
    _save_bot("a", FAKE_TOKEN_A)
    factory = _Factory()
    provider = TelegramAuthProvider(factory=factory)

    backend = await provider.get("a")
    assert backend is factory.built["a"]
    backend.connect.assert_awaited_once()
    # Bot mode does not need an authorization round-trip.
    backend.is_authorized.assert_not_awaited()
    assert provider.resolve_backend("a") is backend

    assert await provider.get("a") is backend
    assert len(factory.calls) == 1


async def test_multi_namespaces_resolve_separate_backends():
    _save_bot("a", FAKE_TOKEN_A)
    _save_bot("b", FAKE_TOKEN_B)
    factory = _Factory()
    provider = TelegramAuthProvider(factory=factory)

    backend_a = await provider.get("a")
    backend_b = await provider.get("b")

    assert backend_a is not None and backend_b is not None
    assert backend_a is not backend_b
    tokens = {ns: settings.bot_token for ns, settings in factory.calls}
    assert tokens == {"a": FAKE_TOKEN_A, "b": FAKE_TOKEN_B}
    dirs = {ns: settings.data_dir for ns, settings in factory.calls}
    assert dirs == {"a": namespace_data_dir("a"), "b": namespace_data_dir("b")}
    assert provider.resolve_backend("a") is backend_a
    assert provider.resolve_backend("b") is backend_b


async def test_get_user_mode_authorized():
    _save_phone("u")
    factory = _Factory(authorized=True)
    provider = TelegramAuthProvider(factory=factory)
    backend = await provider.get("u")
    assert backend is factory.built["u"]
    backend.is_authorized.assert_awaited_once()


async def test_get_user_mode_unauthorized_returns_none_and_disconnects():
    _save_phone("u")
    factory = _Factory(authorized=False)
    provider = TelegramAuthProvider(factory=factory)
    assert await provider.get("u") is None
    factory.built["u"].disconnect.assert_awaited_once()
    assert provider.resolve_backend("u") is None


async def test_unauthorized_namespace_is_retried_after_cli_auth():
    _save_phone("u")
    factory = _Factory(authorized=False)
    provider = TelegramAuthProvider(factory=factory)
    assert await provider.get("u") is None
    factory._authorized = True
    assert await provider.get("u") is not None
    assert len(factory.calls) == 2


async def test_connect_error_is_redacted_without_chain():
    _save_bot("a", FAKE_TOKEN_A)
    leak = RuntimeError(f"GET https://api.telegram.org/bot{FAKE_TOKEN_A}/getMe failed")
    factory = _Factory(connect_error=leak)
    provider = TelegramAuthProvider(factory=factory)

    with pytest.raises(RuntimeError) as excinfo:
        await provider.get("a")

    message = str(excinfo.value)
    assert "'a'" in message
    assert FAKE_TOKEN_A not in message
    assert excinfo.value.__cause__ is None
    assert excinfo.value.__suppress_context__ is True
    factory.built["a"].disconnect.assert_awaited_once()
    assert provider.resolve_backend("a") is None


async def test_concurrent_get_builds_one_backend():
    _save_bot("a", FAKE_TOKEN_A)
    factory = _Factory()
    provider = TelegramAuthProvider(factory=factory)

    results = await asyncio.gather(*(provider.get("a") for _ in range(5)))

    assert len(factory.calls) == 1
    assert all(r is results[0] for r in results)


# --- revoke / shutdown ---


async def test_revoke_disconnects_and_forgets():
    _save_bot("a", FAKE_TOKEN_A)
    provider = TelegramAuthProvider(factory=_Factory())
    backend = await provider.get("a")
    assert backend is not None

    assert await provider.revoke("a") is True
    backend.disconnect.assert_awaited_once()
    assert provider.resolve_backend("a") is None
    assert await provider.revoke("a") is False


async def test_shutdown_disconnects_all_and_survives_errors(caplog):
    _save_bot("a", FAKE_TOKEN_A)
    _save_bot("b", FAKE_TOKEN_B)
    factory = _Factory()
    provider = TelegramAuthProvider(factory=factory)
    await provider.get("a")
    await provider.get("b")
    factory.built["a"].disconnect.side_effect = OSError(f"boom {FAKE_TOKEN_A}")

    await provider.shutdown()

    factory.built["a"].disconnect.assert_awaited_once()
    factory.built["b"].disconnect.assert_awaited_once()
    assert provider.active_clients == {}


async def test_shutdown_with_no_backends_is_a_noop():
    provider = TelegramAuthProvider(factory=_Factory())
    await provider.shutdown()
    assert provider.active_clients == {}


def test_default_factory_is_create_backend():
    assert TelegramAuthProvider()._factory is tap.create_backend
