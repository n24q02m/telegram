from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from telegram.config import Settings


def _make_settings(tmp_path: Path) -> Settings:
    """Create Settings for user mode with a temp data dir."""
    return Settings(
        api_id=12345,
        api_hash="test_hash",
        phone="+84912345678",
        data_dir=tmp_path,
        session_name="test_session",
    )


def _mock_message(
    msg_id: int = 1,
    text: str = "hello",
    date: str = "2026-01-01",
    sender_id: int = 100,
) -> MagicMock:
    msg = MagicMock()
    msg.id = msg_id
    msg.text = text
    msg.date = date
    msg.sender_id = sender_id
    msg.media = None
    return msg


def _mock_dialog(
    dialog_id: int = 1, title: str = "Test Chat", unread: int = 0
) -> MagicMock:
    d = MagicMock()
    d.id = dialog_id
    d.title = title
    d.name = title
    d.unread_count = unread
    return d


def _mock_user(
    user_id: int = 100,
    first_name: str = "Test",
    last_name: str = "User",
    username: str = "testuser",
    phone: str = "+84912345678",
) -> MagicMock:
    u = MagicMock()
    u.id = user_id
    u.first_name = first_name
    u.last_name = last_name
    u.username = username
    u.phone = phone
    return u


@pytest.fixture
def mock_client():
    """Create a fully mocked TelegramClient."""
    client = AsyncMock()
    # is_connected is sync in Telethon, so use MagicMock
    client.is_connected = MagicMock(return_value=True)
    client.is_user_authorized = AsyncMock(return_value=True)
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    return client


@pytest.fixture
def mock_client_class(mock_client):
    """Patch TelegramClient constructor to return mock_client."""
    with patch(
        "telegram.backends.user_backend.TelegramClient",
        return_value=mock_client,
    ) as cls:
        yield cls


class TestConnect:
    async def test_connect_authorized(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        await backend.connect()

        mock_client_class.assert_called_once()
        mock_client.connect.assert_awaited_once()
        mock_client.is_user_authorized.assert_awaited_once()
        assert await backend.is_connected() is True

    async def test_connect_unauthorized_stays_connected(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.is_user_authorized = AsyncMock(return_value=False)
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        # Should NOT raise anymore - stays connected for runtime auth
        await backend.connect()

        # Client should still be available (not disconnected)
        assert backend._client is not None
        mock_client.connect.assert_awaited_once()


class TestDisconnect:
    async def test_disconnect(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        await backend.disconnect()

        mock_client.disconnect.assert_awaited()
        assert backend._client is None

    async def test_disconnect_exception_is_ignored(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.disconnect = AsyncMock(side_effect=Exception("Disconnect failed"))

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        # Should not raise despite disconnect error
        await backend.disconnect()

        mock_client.disconnect.assert_awaited()
        assert backend._client is None

    async def test_disconnect_when_not_connected(self, tmp_path):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        # Should not raise
        await backend.disconnect()


class TestIsConnected:
    async def test_not_connected_without_client(self, tmp_path):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        assert await backend.is_connected() is False

    async def test_is_connected_sync_return(
        self, tmp_path, mock_client, mock_client_class
    ):
        """When Telethon's is_connected() returns a sync bool."""
        from telegram.backends.user_backend import UserBackend

        mock_client.is_connected = MagicMock(return_value=True)
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        assert await backend.is_connected() is True

    async def test_is_connected_async_return(
        self, tmp_path, mock_client, mock_client_class
    ):
        """When Telethon's is_connected() returns a coroutine."""
        from telegram.backends.user_backend import UserBackend

        mock_client.is_connected = AsyncMock(return_value=True)
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        assert await backend.is_connected() is True


class TestSendMessage:
    async def test_send_message(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_message = AsyncMock(return_value=_mock_message())
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.send_message(123, "hello", reply_to=5, parse_mode="html")

        mock_client.send_message.assert_awaited_once_with(
            123, "hello", reply_to=5, parse_mode="html"
        )
        assert result["message_id"] == 1
        assert result["text"] == "hello"

    async def test_send_message_not_connected(self, tmp_path):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        with pytest.raises(RuntimeError, match="Not connected"):
            await backend.send_message(123, "hello")


class TestEditMessage:
    async def test_edit_message(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.edit_message = AsyncMock(return_value=_mock_message(text="edited"))

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.edit_message(123, 1, "edited")

        assert result["text"] == "edited"


class TestDeleteMessage:
    async def test_delete_message(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.delete_messages = AsyncMock(return_value=MagicMock())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.delete_message(123, 1)

        assert result is True


class TestForwardMessage:
    async def test_forward_message_single(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.forward_messages = AsyncMock(return_value=_mock_message(msg_id=2))

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.forward_message(100, 200, 1)

        assert result["message_id"] == 2

    async def test_forward_message_list_return(
        self, tmp_path, mock_client, mock_client_class
    ):
        """When forward_messages returns a list instead of single message."""
        from telegram.backends.user_backend import UserBackend

        msgs = [_mock_message(msg_id=5), _mock_message(msg_id=6)]
        mock_client.forward_messages = AsyncMock(return_value=msgs)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.forward_message(100, 200, 1)

        assert result["message_id"] == 5


class TestPinMessage:
    async def test_pin_message(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.pin_message = AsyncMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.pin_message(123, 42)

        assert result is True
        mock_client.pin_message.assert_awaited_once_with(123, 42)


class TestReactToMessage:
    async def test_react_to_message(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.react_to_message(123, 42, "thumbsup")

        assert result is True


class TestSearchMessages:
    async def test_search_global(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        msgs = [_mock_message(msg_id=i, text=f"msg{i}") for i in range(3)]

        mock_iter_messages = MagicMock()

        async def mock_iter(*args, **kwargs):
            mock_iter_messages(*args, **kwargs)
            for m in msgs:
                yield m

        mock_client.iter_messages = mock_iter

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.search_messages("test", limit=10)

        assert len(result) == 3
        assert result[0]["message_id"] == 0
        mock_iter_messages.assert_called_once_with(None, search="test", limit=10)

    async def test_search_per_chat(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        msgs = [_mock_message(msg_id=1, text="found")]

        mock_iter_messages = MagicMock()

        async def mock_iter(*args, **kwargs):
            mock_iter_messages(*args, **kwargs)
            for m in msgs:
                yield m

        mock_client.iter_messages = mock_iter

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.search_messages("test", chat_id=456, limit=5)

        assert len(result) == 1
        assert result[0]["text"] == "found"
        mock_iter_messages.assert_called_once_with(456, search="test", limit=5)


class TestGetHistory:
    async def test_get_history(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        msgs = [_mock_message(msg_id=i) for i in range(5)]

        mock_iter_messages = MagicMock()

        async def mock_iter(*args, **kwargs):
            mock_iter_messages(*args, **kwargs)
            for m in msgs:
                yield m

        mock_client.iter_messages = mock_iter

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.get_history(123, limit=5)

        assert len(result) == 5
        mock_iter_messages.assert_called_once_with(123, limit=5)

    async def test_get_history_with_offset(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_iter_messages = MagicMock()

        async def mock_iter(*args, **kwargs):
            mock_iter_messages(*args, **kwargs)
            for _ in []:
                yield _

        mock_client.iter_messages = mock_iter

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        await backend.get_history(123, limit=10, offset_id=50)

        mock_iter_messages.assert_called_once_with(123, limit=10, offset_id=50)


class TestListChats:
    async def test_list_chats(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        dialogs = [_mock_dialog(i, f"Chat {i}") for i in range(3)]

        mock_client.get_dialogs = AsyncMock(return_value=dialogs)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.list_chats(limit=10)

        assert len(result) == 3
        assert result[1]["title"] == "Chat 1"
        mock_client.get_dialogs.assert_awaited_once_with(limit=10)


class TestGetChatInfo:
    async def test_get_chat_info_channel(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telethon.tl.types import Channel

        from telegram.backends.user_backend import UserBackend

        entity = MagicMock(spec=Channel)
        entity.id = 123
        entity.title = "Test Channel"
        entity.participants_count = 500
        mock_client.get_entity = AsyncMock(return_value=entity)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.get_chat_info(123)

        assert result["id"] == 123
        assert result["title"] == "Test Channel"
        assert result["participants_count"] == 500

    async def test_get_chat_info_user(self, tmp_path, mock_client, mock_client_class):
        from telethon.tl.types import User

        from telegram.backends.user_backend import UserBackend

        entity = MagicMock(spec=User)
        entity.id = 456
        entity.first_name = "John"
        entity.last_name = "Doe"
        entity.username = "johndoe"
        mock_client.get_entity = AsyncMock(return_value=entity)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.get_chat_info(456)

        assert result["id"] == 456
        assert result["first_name"] == "John"
        assert result["username"] == "johndoe"

    async def test_get_chat_info_chat(self, tmp_path, mock_client, mock_client_class):
        from telethon.tl.types import Chat

        from telegram.backends.user_backend import UserBackend

        entity = MagicMock(spec=Chat)
        entity.id = 789
        entity.title = "Group Chat"
        entity.participants_count = 10
        mock_client.get_entity = AsyncMock(return_value=entity)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.get_chat_info(789)

        assert result["title"] == "Group Chat"


class TestCreateChat:
    async def test_create_group(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_result = MagicMock()
        mock_chat = MagicMock()
        mock_chat.id = 100
        mock_chat.title = "New Group"
        mock_result.chats = [mock_chat]
        mock_client.__call__ = AsyncMock(return_value=mock_result)
        mock_client.return_value = mock_result

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.create_chat("New Group")

        assert result["id"] == 100
        assert result["title"] == "New Group"

    async def test_create_channel(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_result = MagicMock()
        mock_chat = MagicMock()
        mock_chat.id = 200
        mock_chat.title = "New Channel"
        mock_result.chats = [mock_chat]
        mock_client.__call__ = AsyncMock(return_value=mock_result)
        mock_client.return_value = mock_result

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.create_chat("New Channel", is_channel=True)

        assert result["id"] == 200

    async def test_create_chat_no_chats_returned(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_result = MagicMock()
        mock_result.chats = []
        mock_client.__call__ = AsyncMock(return_value=mock_result)
        mock_client.return_value = mock_result

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.create_chat("Phantom")

        assert result == {"title": "Phantom"}


class TestJoinChat:
    async def test_join_invite_link(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.join_chat("https://t.me/joinchat/abc123")

        assert result is True

    async def test_join_plus_link(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.join_chat("https://t.me/+abc123")

        assert result is True

    async def test_join_public_link(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.join_chat("https://t.me/somepublicchannel")

        assert result is True

    async def test_join_public_username(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.join_chat("public_group")

        assert result is True


class TestLeaveChat:
    async def test_leave_channel(self, tmp_path, mock_client, mock_client_class):
        from telethon.tl.types import Channel

        from telegram.backends.user_backend import UserBackend

        entity = MagicMock(spec=Channel)
        entity.id = 123
        mock_client.get_entity = AsyncMock(return_value=entity)
        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.leave_chat(123)

        assert result is True

    async def test_leave_basic_group(self, tmp_path, mock_client, mock_client_class):
        from telethon.tl.types import Chat

        from telegram.backends.user_backend import UserBackend

        entity = MagicMock(spec=Chat)
        entity.id = 456
        mock_client.get_entity = AsyncMock(return_value=entity)
        mock_me = MagicMock()
        mock_me.id = 789
        mock_client.get_me = AsyncMock(return_value=mock_me)
        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.leave_chat(456)

        assert result is True


class TestGetMembers:
    async def test_get_members(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        users = [_mock_user(user_id=i) for i in range(3)]

        async def mock_iter_participants(*args, **kwargs):
            for u in users:
                yield u

        mock_client.iter_participants = MagicMock(side_effect=mock_iter_participants)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.get_members(123, limit=10)

        mock_client.iter_participants.assert_called_once_with(123, limit=10)
        assert len(result) == 3
        assert result[0]["first_name"] == "Test"


class TestPromoteAdmin:
    async def test_promote_admin(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.promote_admin(123, 456)

        assert result is True

    async def test_demote_admin(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.promote_admin(123, 456, demote=True)

        assert result is True


class TestUpdateChatSettings:
    async def test_update_title(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.update_chat_settings(123, title="New Title")

        assert result is True

    async def test_update_description(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        # Patch the EditAboutRequest import inside user_backend
        mock_edit_about = MagicMock()
        with patch.dict(
            "sys.modules",
            {
                "telethon.tl.functions.channels": MagicMock(
                    EditTitleRequest=MagicMock(),
                    EditAboutRequest=mock_edit_about,
                ),
            },
        ):
            settings = _make_settings(tmp_path)
            backend = UserBackend(settings)
            await backend.connect()

            result = await backend.update_chat_settings(123, description="New desc")

            assert result is True

    async def test_update_both(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "telethon.tl.functions.channels": MagicMock(
                    EditTitleRequest=MagicMock(),
                    EditAboutRequest=MagicMock(),
                ),
            },
        ):
            settings = _make_settings(tmp_path)
            backend = UserBackend(settings)
            await backend.connect()

            result = await backend.update_chat_settings(
                123, title="Title", description="Desc"
            )

            assert result is True


class TestClearCache:
    async def test_clear_cache(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_session = MagicMock()
        mock_client.session = mock_session

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        await backend.clear_cache()

        mock_session.save.assert_called_once()

    async def test_clear_cache_not_connected(self, tmp_path):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        # Should not raise
        await backend.clear_cache()

    async def test_clear_cache_exception_swallowed(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_session = MagicMock()
        mock_session.save.side_effect = Exception("Storage error")
        mock_client.session = mock_session

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        # Should not raise an exception
        await backend.clear_cache()

        mock_session.save.assert_called_once()


class TestManageTopics:
    async def test_topics_list(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_entity = MagicMock()
        mock_client.get_entity = AsyncMock(return_value=mock_entity)

        mock_topic1 = MagicMock()
        mock_topic1.id = 1
        mock_topic1.title = "General"
        mock_topic1.icon_emoji_id = None

        mock_topic2 = MagicMock()
        mock_topic2.id = 2
        mock_topic2.title = "Off-topic"
        mock_topic2.icon_emoji_id = 5368324170671202286

        mock_result = MagicMock()
        mock_result.topics = [mock_topic1, mock_topic2]
        mock_client.return_value = mock_result

        with patch.dict(
            "sys.modules",
            {
                "telethon.tl.functions.channels": MagicMock(
                    GetForumTopicsRequest=MagicMock(return_value=MagicMock()),
                ),
            },
        ):
            settings = _make_settings(tmp_path)
            backend = UserBackend(settings)
            await backend.connect()

            result = await backend.manage_topics(123, "list")

            assert result["count"] == 2
            assert result["topics"][0]["id"] == 1
            assert result["topics"][0]["title"] == "General"
            assert result["topics"][1]["id"] == 2
            assert result["topics"][1]["title"] == "Off-topic"

    async def test_topics_create(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_update = MagicMock()
        mock_update.id = 42
        mock_result = MagicMock()
        mock_result.updates = [mock_update]
        mock_client.return_value = mock_result

        with patch.dict(
            "sys.modules",
            {
                "telethon.tl.functions.channels": MagicMock(
                    CreateForumTopicRequest=MagicMock(return_value=MagicMock()),
                ),
            },
        ):
            settings = _make_settings(tmp_path)
            backend = UserBackend(settings)
            await backend.connect()

            result = await backend.manage_topics(123, "create", name="General")

            assert result["topic_id"] == 42

    async def test_topics_create_no_updates(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_result = MagicMock()
        mock_result.updates = []
        mock_client.return_value = mock_result

        with patch.dict(
            "sys.modules",
            {
                "telethon.tl.functions.channels": MagicMock(
                    CreateForumTopicRequest=MagicMock(return_value=MagicMock()),
                ),
            },
        ):
            settings = _make_settings(tmp_path)
            backend = UserBackend(settings)
            await backend.connect()

            result = await backend.manage_topics(123, "create", name="General")

            assert result["topic_id"] is None

    async def test_topics_close(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "telethon.tl.functions.channels": MagicMock(
                    EditForumTopicRequest=MagicMock(return_value=MagicMock()),
                ),
            },
        ):
            settings = _make_settings(tmp_path)
            backend = UserBackend(settings)
            await backend.connect()

            result = await backend.manage_topics(123, "close", topic_id=42)

            assert result == {"closed": True}

    async def test_topics_unknown(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.manage_topics(123, "unknown")

        assert "error" in result


class TestSendMedia:
    async def test_send_photo(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_file = AsyncMock(return_value=_mock_message())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.send_media(
            123, "photo", "https://example.com/photo.jpg", caption="Nice"
        )

        assert result["message_id"] == 1
        mock_client.send_file.assert_awaited_once_with(
            123, b"mock content", caption="Nice"
        )

    async def test_send_media_mixed_case_url(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_file = AsyncMock(return_value=_mock_message())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.send_media(
            123, "photo", "hTtPs://example.com/photo.jpg", caption="Nice"
        )

        assert result["message_id"] == 1
        mock_client.send_file.assert_awaited_once_with(
            123, b"mock content", caption="Nice"
        )

    async def test_send_voice(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_file = AsyncMock(return_value=_mock_message())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        f = tmp_path / "voice.ogg"
        f.write_text("audio")

        result = await backend.send_media(123, "voice", str(f))

        assert result["message_id"] == 1

        mock_client.send_file.assert_awaited_once_with(
            123, f.resolve(), voice_note=True
        )

    async def test_send_video(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_file = AsyncMock(return_value=_mock_message())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        f = tmp_path / "video.mp4"
        f.write_text("video")

        result = await backend.send_media(123, "video", str(f))

        assert result["message_id"] == 1

        mock_client.send_file.assert_awaited_once_with(
            123, f.resolve(), video_note=False
        )

    async def test_send_document(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_file = AsyncMock(return_value=_mock_message())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        f = tmp_path / "doc.pdf"
        f.write_text("doc")

        result = await backend.send_media(123, "document", str(f))

        assert result["message_id"] == 1

    async def test_send_media_missing_file_does_not_send(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        missing = tmp_path / "missing.txt"
        with pytest.raises(FileNotFoundError, match="File not found"):
            await backend.send_media(123, "document", str(missing))

        mock_client.send_file.assert_not_awaited()

    async def test_send_media_exact_max_file_size_succeeds(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_file = AsyncMock(return_value=_mock_message())

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        f = tmp_path / "exact.bin"
        with f.open("wb") as stream:
            stream.truncate(50 * 1024 * 1024)

        result = await backend.send_media(123, "document", str(f))

        assert result["message_id"] == 1
        mock_client.send_file.assert_awaited_once_with(123, f.resolve())

    @pytest.mark.asyncio
    async def test_send_media_file_too_large(
        self, tmp_path, mock_client, mock_client_class
    ):
        from unittest.mock import patch

        from telegram.backends.security import SecurityError
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        f = tmp_path / "huge.txt"
        f.write_text("X")
        with patch("pathlib.Path.stat") as mock_stat:
            mock_stat.return_value.st_size = 50 * 1024 * 1024 + 1
            with pytest.raises(
                SecurityError, match="File size exceeds maximum allowed"
            ):
                await backend.send_media(123, "document", str(f))
        mock_client.send_file.assert_not_awaited()


class TestDownloadMedia:
    async def test_download_media(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        msg = _mock_message()
        msg.media = MagicMock()  # has media
        mock_client.get_messages = AsyncMock(return_value=msg)
        mock_client.download_media = AsyncMock(return_value="/tmp/photo.jpg")

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.download_media(123, 1)

        assert result == "/tmp/photo.jpg"

    async def test_download_media_no_media_raises(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        msg = _mock_message()
        msg.media = None
        mock_client.get_messages = AsyncMock(return_value=msg)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        with pytest.raises(ValueError, match="no media"):
            await backend.download_media(123, 1)

    async def test_download_media_with_output_dir(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        msg = _mock_message()
        msg.media = MagicMock()
        mock_client.get_messages = AsyncMock(return_value=msg)
        mock_client.download_media = AsyncMock(return_value="/output/photo.jpg")

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.download_media(
            123, 1, output_dir=str(tmp_path / "output")
        )

        assert result == "/output/photo.jpg"
        # Verify output_dir was created
        assert (tmp_path / "output").exists()

    async def test_download_media_returns_list(
        self, tmp_path, mock_client, mock_client_class
    ):
        """When get_messages returns a list, use first element."""
        from telegram.backends.user_backend import UserBackend

        msg = _mock_message()
        msg.media = MagicMock()
        mock_client.get_messages = AsyncMock(return_value=[msg])
        mock_client.download_media = AsyncMock(return_value="/tmp/photo.jpg")

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.download_media(123, 1)

        assert result == "/tmp/photo.jpg"

    async def test_download_media_empty_list_raises(
        self, tmp_path, mock_client, mock_client_class
    ):
        """When get_messages returns empty list."""
        from telegram.backends.user_backend import UserBackend

        mock_client.get_messages = AsyncMock(return_value=[])

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        with pytest.raises(ValueError, match="no media"):
            await backend.download_media(123, 1)

    async def test_download_media_none_path_raises(
        self, tmp_path, mock_client, mock_client_class
    ):
        """When download_media returns None."""
        from telegram.backends.user_backend import UserBackend

        msg = _mock_message()
        msg.media = MagicMock()
        mock_client.get_messages = AsyncMock(return_value=msg)
        mock_client.download_media = AsyncMock(return_value=None)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        with pytest.raises(ValueError, match="Failed to download"):
            await backend.download_media(123, 1)

    async def test_download_media_ignores_file_id(
        self, tmp_path, mock_client, mock_client_class
    ):
        """user mode uses the Telethon chat/message lookup; file_id is a
        bot-mode-only concept and is accepted but ignored here."""
        from telegram.backends.user_backend import UserBackend

        msg = _mock_message()
        msg.media = MagicMock()
        mock_client.get_messages = AsyncMock(return_value=msg)
        mock_client.download_media = AsyncMock(return_value="/tmp/photo.jpg")

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.download_media(123, 1, file_id="unused-in-user-mode")

        assert result == "/tmp/photo.jpg"


class TestListContacts:
    async def test_list_contacts_returns_list(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        users = [_mock_user(user_id=i) for i in range(2)]
        contacts_result = MagicMock()
        contacts_result.users = users
        mock_client.return_value = contacts_result

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.list_contacts()

        assert len(result) == 2
        assert result[0]["first_name"] == "Test"

    async def test_list_contacts_returns_object_with_users(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        contacts_obj = MagicMock()
        contacts_obj.users = [_mock_user()]
        mock_client.return_value = contacts_obj

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.list_contacts()

        assert len(result) == 1


class TestSearchContacts:
    async def test_search_contacts(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_result = MagicMock()
        mock_result.users = [_mock_user(user_id=1), _mock_user(user_id=2)]
        mock_client.return_value = mock_result

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.search_contacts("Test")

        assert len(result) == 2


class TestAddContact:
    async def test_add_contact(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.add_contact("+1234567890", "John", last_name="Doe")

        assert result is True

    async def test_add_contact_no_last_name(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = MagicMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.add_contact("+1234567890", "Jane")

        assert result is True


class TestBlockUser:
    async def test_block_user(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.__call__ = AsyncMock()
        mock_client.return_value = None

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.block_user(123)

        assert result is True

    async def test_unblock_user(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.return_value = None

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.block_user(123, unblock=True)

        assert result is True


class TestIsAuthorized:
    async def test_is_authorized_true(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.is_user_authorized = AsyncMock(return_value=True)
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        assert await backend.is_authorized() is True

    async def test_is_authorized_false(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.is_user_authorized = AsyncMock(return_value=False)
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        assert await backend.is_authorized() is False

    async def test_is_authorized_no_client(self, tmp_path):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        assert await backend.is_authorized() is False


class TestSendCode:
    async def test_send_code(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_client.send_code_request = AsyncMock()
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        await backend.send_code("+84912345678")

        mock_client.send_code_request.assert_awaited_once_with("+84912345678")

    async def test_send_code_not_connected(self, tmp_path):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)

        with pytest.raises(RuntimeError, match="Not connected"):
            await backend.send_code("+84912345678")


class TestSignIn:
    async def test_sign_in_success(self, tmp_path, mock_client, mock_client_class):
        from telegram.backends.user_backend import UserBackend

        mock_me = MagicMock()
        mock_me.first_name = "Test"
        mock_me.username = "testuser"
        mock_client.sign_in = AsyncMock()
        mock_client.get_me = AsyncMock(return_value=mock_me)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.sign_in("+84912345678", "12345")

        mock_client.sign_in.assert_awaited_once_with("+84912345678", "12345")
        assert result["authenticated_as"] == "Test"
        assert result["username"] == "testuser"

    async def test_sign_in_2fa_with_password(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_me = MagicMock()
        mock_me.first_name = "Test"
        mock_me.username = "testuser"
        mock_client.sign_in = AsyncMock(
            side_effect=[Exception("SessionPasswordNeeded"), mock_me]
        )
        mock_client.get_me = AsyncMock(return_value=mock_me)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        result = await backend.sign_in("+84912345678", "12345", password="my2fapass")

        assert mock_client.sign_in.await_count == 2
        assert result["authenticated_as"] == "Test"

    async def test_sign_in_2fa_without_password_raises(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.sign_in = AsyncMock(side_effect=Exception("SessionPasswordNeeded"))

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        with pytest.raises(Exception, match="SessionPasswordNeeded"):
            await backend.sign_in("+84912345678", "12345")

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="Windows does not support Unix file permissions (chmod 0o600)",
    )
    async def test_connect_precreates_session_securely(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        # Remove session file if it exists so we can test TOCTOU-safe creation
        session_file = tmp_path / "test_session.session"
        if session_file.exists():
            session_file.unlink()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        assert session_file.exists()
        assert session_file.stat().st_mode & 0o777 == 0o600

    @pytest.mark.skipif(
        sys.platform == "win32",
        reason="Windows does not support Unix file permissions (chmod 0o600)",
    )
    async def test_sign_in_updates_existing_session_permissions(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        # Create a fake session file with insecure permissions
        session_file = tmp_path / "test_session.session"
        session_file.write_text("fake")
        session_file.chmod(0o644)

        mock_me = MagicMock()
        mock_me.first_name = "Test"
        mock_me.username = "testuser"
        mock_client.sign_in = AsyncMock()
        mock_client.get_me = AsyncMock(return_value=mock_me)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()
        await backend.sign_in("+84912345678", "12345")

        assert session_file.stat().st_mode & 0o777 == 0o600

    async def test_sign_in_chmod_handles_oserror(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        # Create a fake session file
        session_file = tmp_path / "test_session.session"
        session_file.write_text("fake")

        mock_me = MagicMock()
        mock_me.first_name = "Test"
        mock_me.username = "testuser"
        mock_client.sign_in = AsyncMock()
        mock_client.get_me = AsyncMock(return_value=mock_me)

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        with patch("telegram.backends.user_backend.os.chmod", side_effect=OSError):
            result = await backend.sign_in("+84912345678", "12345")

        assert result["authenticated_as"] == "Test"
        assert result["username"] == "testuser"


class TestSerializeMessage:
    def test_serialize_message_null_sender(self):
        from telegram.backends.user_backend import UserBackend

        msg = MagicMock()
        msg.id = 1
        msg.text = None
        msg.date = None
        msg.sender_id = None

        result = UserBackend._serialize_message(msg)

        assert result["message_id"] == 1
        assert result["text"] == ""
        assert result["date"] is None
        assert result["sender_id"] is None

    def test_serialize_message_topic_id_forum_message(self):
        """Forum topic message should have topic_id from reply_to_top_id."""
        from types import SimpleNamespace

        from telegram.backends.user_backend import UserBackend

        # Forum message with reply_to_top_id
        reply_to = SimpleNamespace(
            forum_topic=True,
            reply_to_top_id=12345,
            reply_to_msg_id=67890,  # replied-to message, not topic
        )
        msg = SimpleNamespace(
            id=1,
            text="test",
            date=None,
            sender_id=42,
            reply_to=reply_to,
        )

        result = UserBackend._serialize_message(msg)

        assert result["topic_id"] == 12345  # topic root, not replied-to message

    def test_serialize_message_topic_id_forum_fallback(self):
        """Forum message without reply_to_top_id falls back to reply_to_msg_id."""
        from types import SimpleNamespace

        from telegram.backends.user_backend import UserBackend

        # Forum message where reply_to_top_id is None (topic root message)
        reply_to = SimpleNamespace(
            forum_topic=True,
            reply_to_top_id=None,
            reply_to_msg_id=12345,  # topic root when reply_to_top_id is None
        )
        msg = SimpleNamespace(
            id=1,
            text="test",
            date=None,
            sender_id=42,
            reply_to=reply_to,
        )

        result = UserBackend._serialize_message(msg)

        assert result["topic_id"] == 12345

    def test_serialize_message_no_topic_for_ordinary_reply(self):
        """Ordinary reply (forum_topic=False) should have topic_id=None."""
        from types import SimpleNamespace

        from telegram.backends.user_backend import UserBackend

        # Ordinary reply, not in a forum topic
        reply_to = SimpleNamespace(
            forum_topic=False,
            reply_to_msg_id=999,  # replied-to message, NOT a topic
        )
        msg = SimpleNamespace(
            id=1,
            text="test",
            date=None,
            sender_id=42,
            reply_to=reply_to,
        )

        result = UserBackend._serialize_message(msg)

        assert result["topic_id"] is None  # not a forum topic

    def test_serialize_message_no_topic_no_reply(self):
        """Message without reply_to should have topic_id=None."""
        from types import SimpleNamespace

        from telegram.backends.user_backend import UserBackend

        msg = SimpleNamespace(
            id=1,
            text="test",
            date=None,
            sender_id=42,
            reply_to=None,
        )

        result = UserBackend._serialize_message(msg)

        assert result["topic_id"] is None

    def test_serialize_dialog_no_title(self):
        from telegram.backends.user_backend import UserBackend

        d = MagicMock(spec=[])  # No attributes
        d.id = 1
        # Simulate missing title and name
        type(d).title = property(lambda self: None)
        type(d).name = property(lambda self: None)
        type(d).unread_count = property(lambda self: 0)

        # Use a simpler mock
        d2 = MagicMock()
        d2.id = 1
        d2.title = None
        d2.name = None
        d2.unread_count = 0

        # getattr with default should return None, then fallback
        result = UserBackend._serialize_dialog(d2)
        assert result["id"] == 1


class TestUserBackendLogging:
    @pytest.fixture
    def mock_logger(self):
        with patch("telegram.backends.user_backend.logger") as mock:
            yield mock

    async def test_connect_logging(
        self, tmp_path, mock_client, mock_client_class, mock_logger
    ):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        # Force OSError in os.open
        with patch("os.open", side_effect=OSError("Permission denied")):
            backend = UserBackend(settings)
            await backend.connect()

        mock_logger.debug.assert_called()
        args, _ = mock_logger.debug.call_args
        assert "Could not pre-create session file" in args[0]

    async def test_disconnect_logging(
        self, tmp_path, mock_client, mock_client_class, mock_logger
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.disconnect = AsyncMock(side_effect=Exception("Disconnect failed"))
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()
        await backend.disconnect()

        mock_logger.warning.assert_called()
        args, _ = mock_logger.warning.call_args
        assert "Error during disconnect" in args[0]

    async def test_clear_cache_logging(
        self, tmp_path, mock_client, mock_client_class, mock_logger
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.session = MagicMock()
        mock_client.session.save = MagicMock(side_effect=Exception("Save failed"))
        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()
        await backend.clear_cache()

        mock_logger.warning.assert_called()
        args, _ = mock_logger.warning.call_args
        assert "Error saving session during clear_cache" in args[0]

    async def test_sign_in_chmod_logging(
        self, tmp_path, mock_client, mock_client_class, mock_logger
    ):
        from telegram.backends.user_backend import UserBackend

        # Setup for sign_in
        mock_me = MagicMock()
        mock_me.first_name = "Test"
        mock_me.username = "testuser"
        mock_client.sign_in = AsyncMock()
        mock_client.get_me = AsyncMock(return_value=mock_me)

        settings = _make_settings(tmp_path)
        # Create session file
        session_file = (settings.data_dir / settings.session_name).with_suffix(
            ".session"
        )
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        session_file.write_text("fake session")

        backend = UserBackend(settings)
        await backend.connect()

        # Force OSError in os.chmod
        with patch("os.chmod", side_effect=OSError("Operation not permitted")):
            await backend.sign_in("+84912345678", "12345")

        mock_logger.debug.assert_called()
        args, _ = mock_logger.debug.call_args
        assert "Could not set session file permissions" in args[0]

    async def test_secure_session_file_chmod_error_direct(self, tmp_path, mock_logger):
        from telegram.backends.user_backend import UserBackend

        settings = _make_settings(tmp_path)
        session_file = (settings.data_dir / settings.session_name).with_suffix(
            ".session"
        )
        settings.data_dir.mkdir(parents=True, exist_ok=True)
        session_file.write_text("test")

        backend = UserBackend(settings)

        with patch("os.chmod", side_effect=OSError("chmod failed")):
            await backend._secure_session_file()

        mock_logger.debug.assert_called()
        # Verify the specific message
        found = False
        for call in mock_logger.debug.call_args_list:
            if "Could not set session file permissions" in call[0][0]:
                found = True
                break
        assert found

    async def test_join_chat_plus_style_invite(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telethon.tl.functions.messages import ImportChatInviteRequest

        from telegram.backends.user_backend import UserBackend

        mock_client.sign_in = AsyncMock()
        mock_client.__call__ = AsyncMock()

        settings = _make_settings(tmp_path)
        backend = UserBackend(settings)
        await backend.connect()

        # This link should now trigger line 321
        await backend.join_chat("https://t.me/+abc123")

        # Verify ImportChatInviteRequest was called with 'abc123'
        # Telethon functions are usually called via client(Request(...))
        mock_client.assert_awaited()
        # Find the call with ImportChatInviteRequest
        found = False
        for call in mock_client.call_args_list:
            arg = call[0][0]
            if isinstance(arg, ImportChatInviteRequest) and arg.hash == "abc123":
                found = True
                break
        assert found


class TestApiIdentityMarker:
    """_warn_on_api_identity_change only warns when the recorded id differs."""

    # The marker is the real hull PerPluginStore blob under the fake home of
    # the autouse ``_isolate_per_plugin_home`` fixture (what `auth --phone`
    # writes), so these exercise the real read path.

    def _backend(self, tmp_path, api_id=12345, namespace="default"):
        from telegram.backends.user_backend import UserBackend

        settings = Settings(
            api_id=api_id,
            api_hash="test_hash",
            phone="+84912345678",
            data_dir=tmp_path,
            session_name="test_session",
        )
        return UserBackend(settings, namespace=namespace)

    @staticmethod
    def _record(api_id: str, namespace: str = "default") -> None:
        from telegram.credential_state import plugin_store

        plugin_store("tokens/app-identity", namespace).save({"api_id": api_id})

    async def test_no_marker_no_warning(self, tmp_path):
        backend = self._backend(tmp_path)
        with patch("telegram.backends.user_backend.logger") as mock_logger:
            await backend._warn_on_api_identity_change()
        mock_logger.warning.assert_not_called()

    async def test_matching_marker_no_warning(self, tmp_path):
        self._record("12345")
        backend = self._backend(tmp_path, api_id=12345)
        with patch("telegram.backends.user_backend.logger") as mock_logger:
            await backend._warn_on_api_identity_change()
        mock_logger.warning.assert_not_called()

    async def test_differing_marker_warns(self, tmp_path):
        self._record("99999")
        backend = self._backend(tmp_path, api_id=12345)
        with patch("telegram.backends.user_backend.logger") as mock_logger:
            await backend._warn_on_api_identity_change()
        mock_logger.warning.assert_called_once()

    async def test_marker_is_per_namespace(self, tmp_path):
        """A differing marker in namespace ``a`` does not warn for ``b``."""
        self._record("99999", "a")
        backend = self._backend(tmp_path, api_id=12345, namespace="b")
        with patch("telegram.backends.user_backend.logger") as mock_logger:
            await backend._warn_on_api_identity_change()
        mock_logger.warning.assert_not_called()

    async def test_marker_read_error_is_swallowed(self, tmp_path):
        backend = self._backend(tmp_path)
        with (
            patch(
                "telegram.credential_state.plugin_store",
                side_effect=Exception("backend down"),
            ),
            patch("telegram.backends.user_backend.logger") as mock_logger,
        ):
            await backend._warn_on_api_identity_change()
        mock_logger.warning.assert_not_called()


class TestLogOut:
    async def test_log_out_revokes_via_client(
        self, tmp_path, mock_client, mock_client_class
    ):
        from telegram.backends.user_backend import UserBackend

        mock_client.log_out = AsyncMock(return_value=True)
        backend = UserBackend(_make_settings(tmp_path))
        await backend.connect()

        result = await backend.log_out()

        assert result is True
        mock_client.log_out.assert_awaited_once()
