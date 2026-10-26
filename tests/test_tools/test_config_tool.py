from __future__ import annotations

import pytest

from telegram.tools.config_tool import handle_config


@pytest.mark.asyncio
async def test_status(mock_backend):
    result = await handle_config(mock_backend, "status")
    assert result["mode"] == "bot"
    assert result["connected"] is True
    assert result["authorized"] is True
    assert "config" in result
    assert "message_limit" in result["config"]
    assert "timeout" in result["config"]


@pytest.mark.asyncio
async def test_status_user_mode(mock_user_backend):
    result = await handle_config(mock_user_backend, "status")
    assert result["mode"] == "user"
    assert result["connected"] is True
    assert result["authorized"] is True


@pytest.mark.asyncio
async def test_status_shows_pending_auth(mock_backend):
    import telegram.server as srv

    old = srv._pending_auth
    try:
        srv._pending_auth = True
        result = await handle_config(mock_backend, "status")
        assert result["pending_auth"] is True
    finally:
        srv._pending_auth = old


@pytest.mark.asyncio
async def test_set_message_limit(mock_backend):
    result = await handle_config(mock_backend, "set", message_limit=50)
    assert result["updated"]["message_limit"] == 50
    assert result["current"]["message_limit"] == 50


@pytest.mark.asyncio
async def test_set_timeout(mock_backend):
    result = await handle_config(mock_backend, "set", timeout=60)
    assert result["updated"]["timeout"] == 60
    assert result["current"]["timeout"] == 60


@pytest.mark.asyncio
async def test_set_both(mock_backend):
    result = await handle_config(mock_backend, "set", message_limit=100, timeout=90)
    assert result["updated"]["message_limit"] == 100
    assert result["updated"]["timeout"] == 90


@pytest.mark.asyncio
async def test_set_no_params(mock_backend):
    result = await handle_config(mock_backend, "set")
    assert "error" in result
    assert "set requires" in result["error"]


@pytest.mark.asyncio
async def test_set_none_params(mock_backend):
    result = await handle_config(mock_backend, "set", message_limit=None, timeout=None)
    assert "error" in result
    assert "set requires" in result["error"]


@pytest.mark.asyncio
async def test_set_persists_across_calls(mock_backend):
    await handle_config(mock_backend, "set", message_limit=42)
    result = await handle_config(mock_backend, "status")
    assert result["config"]["message_limit"] == 42


@pytest.mark.asyncio
async def test_set_generic_key_value(mock_backend):
    """Generic key/value form (parity with the other servers' set)."""
    result = await handle_config(mock_backend, "set", key="message_limit", value="55")
    assert result["updated"]["message_limit"] == 55
    assert result["current"]["message_limit"] == 55


@pytest.mark.asyncio
async def test_set_generic_timeout(mock_backend):
    result = await handle_config(mock_backend, "set", key="timeout", value="75")
    assert result["updated"]["timeout"] == 75


@pytest.mark.asyncio
async def test_set_generic_missing_value(mock_backend):
    result = await handle_config(mock_backend, "set", key="message_limit")
    assert "error" in result
    assert "both key and value" in result["error"]


@pytest.mark.asyncio
async def test_set_generic_invalid_key(mock_backend):
    result = await handle_config(mock_backend, "set", key="mesage_limit", value="10")
    assert "error" in result
    assert "Invalid key" in result["error"]
    # Fuzzy suggestion points at the real key.
    assert "message_limit" in result["error"]


@pytest.mark.asyncio
async def test_set_generic_non_int_value(mock_backend):
    result = await handle_config(mock_backend, "set", key="timeout", value="abc")
    assert "error" in result
    assert "must be an integer" in result["error"]


@pytest.mark.asyncio
async def test_set_generic_persists_across_calls(mock_backend):
    await handle_config(mock_backend, "set", key="message_limit", value="33")
    result = await handle_config(mock_backend, "status")
    assert result["config"]["message_limit"] == 33


@pytest.mark.asyncio
async def test_cache_clear(mock_backend):
    result = await handle_config(mock_backend, "cache_clear")
    assert "message" in result
    assert "Cache cleared" in result["message"]
    mock_backend.clear_cache.assert_awaited_once()


@pytest.mark.asyncio
async def test_cache_clear_user_mode(mock_user_backend):
    result = await handle_config(mock_user_backend, "cache_clear")
    assert "Cache cleared" in result["message"]
    mock_user_backend.clear_cache.assert_awaited_once()


@pytest.mark.asyncio
async def test_unknown_action(mock_backend):
    result = await handle_config(mock_backend, "unknown")
    assert "error" in result
    assert "Unknown action" in result["error"]


@pytest.mark.asyncio
async def test_general_exception(mock_backend):
    mock_backend.is_connected.side_effect = RuntimeError("fail")
    result = await handle_config(mock_backend, "status")
    assert "error" in result
    assert "RuntimeError" in result["error"]


# Auth/send_code actions are not part of the config tool: credentials are
# set up with the `telegram auth` CLI (bot token, or phone + OTP/2FA).
