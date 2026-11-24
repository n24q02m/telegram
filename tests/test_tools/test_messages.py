from __future__ import annotations

from unittest.mock import AsyncMock

import pytest

from telegram.backends.base import ModeError
from telegram.tools.messages import MessagesArgs, handle_messages


@pytest.mark.asyncio
async def test_send(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="send", chat_id=123, text="hello")
    )
    assert result["message_id"] == 1
    mock_backend.send_message.assert_awaited_once_with(
        123, "hello", reply_to=None, parse_mode=None
    )


@pytest.mark.asyncio
async def test_send_with_reply_and_parse_mode(mock_backend):
    result = await handle_messages(
        mock_backend,
        MessagesArgs(
            action="send",
            chat_id=123,
            text="hi",
            reply_to=5,
            parse_mode="HTML",
        ),
    )
    assert result["message_id"] == 1
    mock_backend.send_message.assert_awaited_once_with(
        123, "hi", reply_to=5, parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_send_missing_params(mock_backend):
    result = await handle_messages(mock_backend, MessagesArgs(action="send"))
    assert "error" in result

    result = await handle_messages(
        mock_backend, MessagesArgs(action="send", chat_id=123)
    )
    assert "error" in result


@pytest.mark.asyncio
async def test_edit(mock_backend):
    result = await handle_messages(
        mock_backend,
        MessagesArgs(action="edit", chat_id=123, message_id=1, text="edited"),
    )
    assert result["message_id"] == 1
    mock_backend.edit_message.assert_awaited_once_with(
        123, 1, "edited", parse_mode=None
    )


@pytest.mark.asyncio
async def test_edit_missing_params(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="edit", chat_id=123, text="x")
    )
    assert "error" in result

    result = await handle_messages(
        mock_backend, MessagesArgs(action="edit", chat_id=123, message_id=1)
    )
    assert "error" in result


@pytest.mark.asyncio
async def test_delete(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="delete", chat_id=123, message_id=1)
    )
    assert result["deleted"] is True


@pytest.mark.asyncio
async def test_delete_missing_params(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="delete", chat_id=123)
    )
    assert "error" in result


@pytest.mark.asyncio
async def test_forward(mock_backend):
    result = await handle_messages(
        mock_backend,
        MessagesArgs(
            action="forward",
            from_chat=1,
            to_chat=2,
            message_id=10,
        ),
    )
    assert result["message_id"] == 2


@pytest.mark.asyncio
async def test_forward_missing_params(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="forward", from_chat=1, to_chat=2)
    )
    assert "error" in result


@pytest.mark.asyncio
async def test_pin(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="pin", chat_id=123, message_id=1)
    )
    assert result["pinned"] is True


@pytest.mark.asyncio
async def test_pin_missing_params(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="pin", chat_id=123)
    )
    assert "error" in result


@pytest.mark.asyncio
async def test_react(mock_backend):
    result = await handle_messages(
        mock_backend,
        MessagesArgs(action="react", chat_id=123, message_id=1, emoji="👍"),
    )
    assert result["reacted"] is True


@pytest.mark.asyncio
async def test_react_missing_params(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="react", chat_id=123, message_id=1)
    )
    assert "error" in result


@pytest.mark.asyncio
async def test_search(mock_backend):
    result = await handle_messages(
        mock_backend, MessagesArgs(action="search", query="test", limit=10)
    )
    assert result["messages"] == []
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_search_missing_params(mock_backend):
    result = await handle_messages(mock_backend, MessagesArgs(action="search"))
    assert "error" in result


@pytest.mark.asyncio
async def test_history(mock_backend):
    result = await handle_messages(
        mock_backend,
        MessagesArgs(action="history", chat_id=123, limit=5, offset_id=100),
    )
    assert result["messages"] == []
    assert result["count"] == 0


@pytest.mark.asyncio
async def test_history_missing_params(mock_backend):
    result = await handle_messages(mock_backend, MessagesArgs(action="history"))
    assert "error" in result


@pytest.mark.asyncio
async def test_unknown_action(mock_backend):
    result = await handle_messages(mock_backend, MessagesArgs(action="unknown"))
    assert "error" in result
    assert "Unknown action" in result["error"]


@pytest.mark.asyncio
async def test_mode_error(mock_backend):
    mock_backend.search_messages.side_effect = ModeError("user")
    result = await handle_messages(
        mock_backend, MessagesArgs(action="search", query="test")
    )
    assert "error" in result
    assert "user mode" in result["error"]


@pytest.mark.asyncio
async def test_general_exception(mock_backend):
    mock_backend.send_message.side_effect = RuntimeError("boom")
    result = await handle_messages(
        mock_backend, MessagesArgs(action="send", chat_id=1, text="x")
    )
    assert "error" in result
    assert "RuntimeError" in result["error"]


@pytest.mark.asyncio
async def test_unknown_action_suggestion(mock_backend):
    # 'sendd' should suggest 'send'
    result = await handle_messages(mock_backend, MessagesArgs(action="sendd"))
    assert "error" in result
    assert "Unknown action 'sendd'." in result["error"]
    assert "Did you mean 'send'?" in result["error"]
    assert (
        "Valid: delete|draft|edit|forward|history|pin|react|schedule|search|send"
        in result["error"]
    )


async def test_schedule_dispatch_and_validation(mock_backend):
    mock_backend.schedule_message = AsyncMock(
        return_value={"scheduled": True, "message_id": 9}
    )
    res = await handle_messages(
        mock_backend,
        MessagesArgs(
            action="schedule",
            chat_id=123,
            text="ping",
            schedule_at="2026-12-01T09:00:00Z",
        ),
    )
    assert res["scheduled"] is True
    err_no_chat = await handle_messages(mock_backend, MessagesArgs(action="schedule"))
    assert "requires chat_id" in err_no_chat["error"]
    err_no_time = await handle_messages(
        mock_backend, MessagesArgs(action="schedule", chat_id=123, text="ping")
    )
    assert "requires chat_id, text, and schedule_at" in err_no_time["error"]
    err_del = await handle_messages(
        mock_backend,
        MessagesArgs(action="schedule", chat_id=123, schedule_action="delete"),
    )
    assert "requires chat_id and message_id" in err_del["error"]


async def test_draft_dispatch_and_validation(mock_backend):
    mock_backend.manage_draft = AsyncMock(return_value={"drafts": [], "count": 0})
    res = await handle_messages(mock_backend, MessagesArgs(action="draft"))
    assert res == {"drafts": [], "count": 0}
    err_save = await handle_messages(
        mock_backend, MessagesArgs(action="draft", draft_action="save")
    )
    assert "requires chat_id and text" in err_save["error"]
    err_clear = await handle_messages(
        mock_backend, MessagesArgs(action="draft", draft_action="clear")
    )
    assert "requires chat_id" in err_clear["error"]
