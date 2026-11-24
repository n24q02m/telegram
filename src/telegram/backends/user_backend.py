from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from loguru import logger
from telethon import TelegramClient
from telethon.tl.functions.contacts import (
    AddContactRequest,
    BlockRequest,
    UnblockRequest,
)
from telethon.tl.types import Channel, Chat, InputPhoneContact, User

from ..config import Settings
from .base import TelegramBackend
from .security import (
    SecurityError,
    fetch_url_safely,
    validate_file_path,
    validate_output_dir,
)


class UserBackend(TelegramBackend):
    def __init__(self, settings: Settings, backend=None, namespace: str = "default"):
        super().__init__("user")
        self._settings = settings
        self._client: TelegramClient | None = None
        self._backend = backend  # None -> on-disk .session file at connect()
        # hull namespace this backend serves; selects the api-identity marker.
        self._namespace = namespace

    def _session_store(self):
        from hull_core.storage import LocalFsBackend, StringSessionStore

        if self._backend is not None:
            # Injected credential backend: session_name is the StringSession's
            # hull sub (one blob per Telethon session).
            return StringSessionStore(
                "telegram", self._settings.session_name, backend=self._backend
            )
        profile = (
            None
            if self._settings.session_name == "default"
            else self._settings.session_name
        )
        return StringSessionStore(
            "telegram",
            None,
            backend=LocalFsBackend(base_dir=self._settings.data_dir),
            profile=profile,
        )

    def _migrate_legacy_session(self, store: Any) -> str | None:
        """One-time non-destructive migration from SQLite ``.session`` to encrypted StringSession."""
        existing = store.load()
        if existing:
            return existing
        legacy_path = (
            self._settings.data_dir / self._settings.session_name
        ).with_suffix(".session")
        if not legacy_path.is_file():
            return existing
        from telethon.sessions import SQLiteSession, StringSession

        sqlite_sess: SQLiteSession | None = None
        try:
            sqlite_sess = SQLiteSession(
                str(self._settings.data_dir / self._settings.session_name)
            )
            if not getattr(sqlite_sess, "auth_key", None):
                return existing
            session_str = StringSession.save(sqlite_sess)
            if not session_str:
                return existing
            store.save(session_str)
            verified = store.load()
            if verified != session_str:
                logger.warning(
                    "Encrypted StringSession verification mismatch during migration"
                )
                return existing
            return verified
        except Exception as exc:
            logger.warning(f"Skipping legacy .session migration: {type(exc).__name__}")
            return existing
        finally:
            if sqlite_sess is not None:
                try:
                    sqlite_sess.close()
                except Exception:
                    pass

    def _ensure_client(self) -> TelegramClient:
        if self._client is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        return self._client

    async def _prepare_session_file(self) -> None:
        """Prepare session directory and file with secure permissions."""

        def _sync_prepare():
            s = self._settings
            s.data_dir.mkdir(parents=True, exist_ok=True, mode=0o700)

            # Pre-create session file with secure permissions to avoid TOCTOU
            # where Telethon creates it with default (insecure) permissions
            session_path = s.data_dir / s.session_name
            actual_session_path = session_path.with_suffix(".session")
            try:
                fd = os.open(str(actual_session_path), os.O_CREAT | os.O_WRONLY, 0o600)
                os.close(fd)
            except OSError as e:
                # Windows may not support this or file already exists
                logger.debug("Could not pre-create session file: {e}", e=e)

        await asyncio.to_thread(_sync_prepare)

    async def _secure_session_file(self) -> None:
        """Ensure existing session files are secured with 0o600 permissions."""

        def _sync_secure():
            s = self._settings
            session_file = (s.data_dir / s.session_name).with_suffix(".session")
            if session_file.exists():
                try:
                    os.chmod(session_file, 0o600)
                except OSError as e:
                    logger.debug("Could not set session file permissions: {e}", e=e)

        await asyncio.to_thread(_sync_secure)

    async def _warn_on_api_identity_change(self) -> None:
        """Warn (do not act) when the recorded api_id differs from the current one.

        ``telegram auth --phone`` records the ``api_id`` the session
        was created under (via ``PerPluginStore``). A session's auth_key is bound
        to that api_id, so reconnecting under a different one silently fails to
        authorize. We only warn and point at ``logout``/``login`` -- clearing the
        session automatically would destroy a working login on a spurious marker
        read.
        """
        from ..credential_state import plugin_store

        def _sync_warn():
            try:
                marker = plugin_store("tokens/app-identity", self._namespace).load()
            except Exception as e:
                logger.debug("Could not read api identity marker: {e}", e=e)
                return
            if not marker:
                return
            recorded = marker.get("api_id")
            current = str(self._settings.api_id)
            if recorded and recorded != current:
                logger.warning(
                    "Telegram api_id changed since this session was created "
                    "(session api_id={recorded}, current api_id={current}). The "
                    "saved session may fail to authorize. Run "
                    "`telegram logout` then `telegram auth --phone <+number>` "
                    "to re-create it.",
                    recorded=recorded,
                    current=current,
                )

        await asyncio.to_thread(_sync_warn)

    @staticmethod
    def _serialize_message(msg: Any) -> dict[str, Any]:
        sender_id = None
        if msg.sender_id is not None:
            sender_id = msg.sender_id
        # Extract forum topic ID if present (Telegram forum/topic feature)
        # Forum messages have reply_to.forum_topic=True and reply_to.reply_to_top_id
        # Ordinary replies have reply_to.forum_topic=False (or no reply_to)
        topic_id = None
        if hasattr(msg, "reply_to") and msg.reply_to is not None:
            # Check if this is a forum topic message
            if getattr(msg.reply_to, "forum_topic", False):
                # reply_to_top_id is the topic root; reply_to_msg_id is the replied-to message
                topic_id = getattr(msg.reply_to, "reply_to_top_id", None)
                # Fallback: if reply_to_top_id is None, use reply_to_msg_id (topic root)
                if topic_id is None:
                    topic_id = getattr(msg.reply_to, "reply_to_msg_id", None)
        return {
            "message_id": msg.id,
            "text": msg.text or "",
            "date": str(msg.date) if msg.date else None,
            "sender_id": sender_id,
            "topic_id": topic_id,
        }

    @staticmethod
    def _serialize_dialog(d: Any) -> dict[str, Any]:
        title = getattr(d, "title", None) or getattr(d, "name", None) or ""
        return {
            "id": d.id,
            "title": title,
            "unread_count": getattr(d, "unread_count", 0),
        }

    @staticmethod
    def _serialize_user(u: Any) -> dict[str, Any]:
        return {
            "id": u.id,
            "first_name": getattr(u, "first_name", None) or "",
            "last_name": getattr(u, "last_name", None) or "",
            "username": getattr(u, "username", None),
            "phone": getattr(u, "phone", None),
        }

    # --- Connection ---
    def _is_externalized(self) -> bool:
        """True when the session must live in a credential backend, not on disk.

        An injected credential backend means the Telethon auth_key is stored
        as a StringSession in that backend instead of on disk. Without one
        (the default for stdio and HTTP deployments) the durable on-disk
        ``.session`` SQLite is used.
        """
        return self._backend is not None

    async def connect(self) -> None:
        s = self._settings

        from hull_core.storage import SaveOnChangeStringSession

        store = self._session_store()
        if self._is_externalized():
            initial_session = store.load()
        else:
            await self._warn_on_api_identity_change()
            s.data_dir.mkdir(parents=True, exist_ok=True)
            initial_session = self._migrate_legacy_session(store)

        session = SaveOnChangeStringSession(initial_session, sink=store.save)
        logger.debug("Connecting Telethon client with encrypted StringSession store")
        self._client = TelegramClient(session, s.api_id, s.api_hash)

        await self._client.connect()

        if not await self._client.is_user_authorized():
            logger.warning(
                "Session not authorized. Run `telegram auth --phone <+number>` to sign in."
            )

    async def disconnect(self) -> None:
        if self._client is not None:
            try:
                await self._client.disconnect()
            except Exception as e:
                logger.warning("Error during disconnect: {e}", e=e)
            self._client = None

    async def is_connected(self) -> bool:
        if self._client is None:
            return False
        # Telethon's is_connected() is a sync method
        connected = self._client.is_connected()
        if asyncio.iscoroutine(connected):
            return await connected
        return bool(connected)

    async def clear_cache(self) -> None:
        if self._client is not None and self._client.session:
            # Clear Telethon's entity cache by deleting cached entities
            try:
                self._client.session.save()
            except Exception as e:
                logger.warning("Error saving session during clear_cache: {e}", e=e)

    # --- Auth ---
    async def is_authorized(self) -> bool:
        if self._client is None:
            return False
        return await self._client.is_user_authorized()

    async def send_code(self, phone: str) -> None:
        client = self._ensure_client()
        await client.send_code_request(phone)

    async def sign_in(
        self, phone: str, code: str, *, password: str | None = None
    ) -> dict[str, Any]:
        client = self._ensure_client()
        try:
            await client.sign_in(phone, code)
        except Exception:
            if password:
                await client.sign_in(password=password)
            else:
                raise

        me = await client.get_me()
        # Local FS deployments secure the on-disk .session (0o600). On an
        # externalized backend the StringSession save-on-change sink persists the
        # auth_key and this is a no-op (no .session file exists to chmod).
        await self._secure_session_file()

        return {
            "authenticated_as": getattr(me, "first_name", ""),
            "username": getattr(me, "username", None),
        }

    async def log_out(self) -> bool:
        """Revoke the session with Telegram and clear stored session material.

        Telethon's ``log_out`` invalidates the auth key server-side. Used by
        the ``logout`` CLI subcommand.
        """
        client = self._ensure_client()
        revoked = await client.log_out()
        try:
            self._session_store().clear()
        except Exception as exc:
            logger.warning(f"Failed to clear StringSessionStore: {type(exc).__name__}")
        return revoked

    # --- Messages ---
    async def send_message(
        self,
        chat_id: str | int,
        text: str,
        *,
        reply_to: int | None = None,
        parse_mode: str | None = None,
    ) -> dict[str, Any]:
        client = self._ensure_client()
        msg = await client.send_message(
            chat_id, text, reply_to=reply_to, parse_mode=parse_mode
        )
        return self._serialize_message(msg)

    async def edit_message(
        self,
        chat_id: str | int,
        message_id: int,
        text: str,
        *,
        parse_mode: str | None = None,
    ) -> dict[str, Any]:
        client = self._ensure_client()
        msg = await client.edit_message(
            chat_id, message_id, text, parse_mode=parse_mode
        )
        return self._serialize_message(msg)

    async def delete_message(self, chat_id: str | int, message_id: int) -> bool:
        client = self._ensure_client()
        result = await client.delete_messages(chat_id, [message_id])
        # Telethon returns AffectedMessages; truthy if deleted
        return bool(result)

    async def forward_message(
        self, from_chat: str | int, to_chat: str | int, message_id: int
    ) -> dict[str, Any]:
        client = self._ensure_client()
        msg = await client.forward_messages(to_chat, message_id, from_chat)
        # forward_messages may return a list or single message
        if isinstance(msg, list):
            msg = msg[0]
        return self._serialize_message(msg)

    async def pin_message(self, chat_id: str | int, message_id: int) -> bool:
        client = self._ensure_client()
        await client.pin_message(chat_id, message_id)
        return True

    async def react_to_message(
        self, chat_id: str | int, message_id: int, emoji: str
    ) -> bool:
        client = self._ensure_client()
        from telethon.tl.functions.messages import SendReactionRequest
        from telethon.tl.types import ReactionEmoji

        await client(
            SendReactionRequest(
                peer=chat_id,
                msg_id=message_id,
                reaction=[ReactionEmoji(emoticon=emoji)],
            )
        )
        return True

    async def search_messages(
        self,
        query: str,
        *,
        chat_id: str | int | None = None,
        limit: int = 20,
    ) -> list[dict[str, Any]]:
        client = self._ensure_client()
        entity = chat_id if chat_id is not None else None
        # Bolt: Avoid the get_messages() anti-pattern, which just calls
        # iter_messages(...).collect(). Using async comprehensions improves
        # memory efficiency without worsening network latency.
        return [
            self._serialize_message(msg)
            async for msg in client.iter_messages(entity, search=query, limit=limit)
        ]

    async def get_history(
        self,
        chat_id: str | int,
        *,
        limit: int = 20,
        offset_id: int | None = None,
    ) -> list[dict[str, Any]]:
        client = self._ensure_client()
        kwargs: dict[str, Any] = {"limit": limit}
        if offset_id is not None:
            kwargs["offset_id"] = offset_id
        # Bolt: Avoid the get_messages() anti-pattern, which just calls
        # iter_messages(...).collect(). Using async comprehensions improves
        # memory efficiency without worsening network latency.
        return [
            self._serialize_message(m)
            async for m in client.iter_messages(chat_id, **kwargs)
        ]

    @staticmethod
    def _parse_schedule_at(schedule_at: str) -> datetime:
        """Parse an ISO-8601 datetime or Unix epoch seconds string into UTC."""
        raw = schedule_at.strip()
        if not raw:
            raise ValueError("schedule_at cannot be empty")
        if raw.isdigit():
            return datetime.fromtimestamp(int(raw), tz=UTC)
        normalized = f"{raw[:-1]}+00:00" if raw.endswith("Z") else raw
        dt = datetime.fromisoformat(normalized)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt

    @staticmethod
    def _parse_text_entities(
        text: str, parse_mode: str | None
    ) -> tuple[str, list[Any] | None]:
        """Parse formatted draft text cleanly without private client hooks."""
        if not parse_mode:
            return text, None
        mode = parse_mode.lower()
        if mode == "html":
            from telethon.extensions import html

            return html.parse(text)
        if mode in {"md", "markdown", "markdownv2"}:
            from telethon.extensions import markdown

            return markdown.parse(text)
        raise ValueError(f"Unsupported parse_mode: {parse_mode}")

    async def schedule_message(
        self,
        chat_id: str | int,
        action: str = "send",
        *,
        text: str | None = None,
        schedule_at: str | None = None,
        message_id: int | None = None,
        reply_to: int | None = None,
        parse_mode: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        client = self._ensure_client()
        if action == "send":
            if not text or not schedule_at:
                raise ValueError("schedule action 'send' requires text and schedule_at")
            dt = self._parse_schedule_at(schedule_at)
            msg = await client.send_message(
                chat_id,
                text,
                reply_to=reply_to,
                parse_mode=parse_mode,
                schedule=dt,
            )
            data = self._serialize_message(msg)
            data["scheduled"] = True
            data["schedule_at"] = dt.isoformat()
            return data
        if action == "list":
            from telethon.tl.functions.messages import GetScheduledHistoryRequest

            peer = await client.get_input_entity(chat_id)
            res = await client(GetScheduledHistoryRequest(peer=peer, hash=0))
            raw_msgs = list(getattr(res, "messages", []) or [])[:limit]
            items = [self._serialize_message(m) for m in raw_msgs]
            return {"chat_id": chat_id, "messages": items, "count": len(items)}
        if action == "delete":
            if message_id is None:
                raise ValueError("schedule action 'delete' requires message_id")
            from telethon.tl.functions.messages import DeleteScheduledMessagesRequest

            peer = await client.get_input_entity(chat_id)
            await client(DeleteScheduledMessagesRequest(peer=peer, id=[message_id]))
            return {"chat_id": chat_id, "deleted": True, "message_id": message_id}
        raise ValueError(f"Unknown schedule action: {action!r}")

    async def manage_draft(
        self,
        action: str = "get",
        *,
        chat_id: str | int | None = None,
        text: str | None = None,
        reply_to: int | None = None,
        parse_mode: str | None = None,
        limit: int = 20,
    ) -> dict[str, Any]:
        client = self._ensure_client()
        normalized = {
            "save": "save",
            "set": "save",
            "get": "get",
            "list": "get",
            "clear": "clear",
            "delete": "clear",
        }.get(action)
        if normalized is None:
            raise ValueError(f"Unknown draft action: {action!r}")

        if normalized == "save":
            if chat_id is None or text is None:
                raise ValueError("draft action 'save' requires chat_id and text")
            from telethon.tl.functions.messages import SaveDraftRequest
            from telethon.tl.types import InputReplyToMessage

            peer = await client.get_input_entity(chat_id)
            raw_text, entities = self._parse_text_entities(text, parse_mode)
            reply_obj = (
                InputReplyToMessage(reply_to_msg_id=reply_to)
                if reply_to is not None
                else None
            )
            await client(
                SaveDraftRequest(
                    peer=peer,
                    message=raw_text,
                    reply_to=reply_obj,
                    entities=entities,
                )
            )
            return {"chat_id": chat_id, "saved": True, "text": text}

        if normalized == "clear":
            if chat_id is None:
                raise ValueError("draft action 'clear' requires chat_id")
            from telethon.tl.functions.messages import SaveDraftRequest

            peer = await client.get_input_entity(chat_id)
            await client(SaveDraftRequest(peer=peer, message=""))
            return {"chat_id": chat_id, "cleared": True}

        if chat_id is not None:
            peer = await client.get_input_entity(chat_id)
            draft_or_list = await client.get_drafts(peer)
            drafts = (
                list(draft_or_list)
                if isinstance(draft_or_list, (list, tuple))
                else ([draft_or_list] if draft_or_list is not None else [])
            )
        else:
            drafts = list(await client.get_drafts())[:limit]

        items: list[dict[str, Any]] = []
        for d in drafts[:limit]:
            d_text = getattr(d, "text", None)
            if not d_text and getattr(d, "is_empty", False):
                continue
            item: dict[str, Any] = {
                "text": d_text or "",
                "date": str(d.date) if getattr(d, "date", None) else None,
                "reply_to_msg_id": getattr(d, "reply_to_msg_id", None),
            }
            entity = getattr(d, "entity", None)
            if entity is not None and getattr(entity, "id", None) is not None:
                item["chat_id"] = entity.id
            items.append(item)
        result: dict[str, Any] = {"drafts": items, "count": len(items)}
        if chat_id is not None:
            result["chat_id"] = chat_id
        return result

    # --- Chats ---
    async def list_chats(self, *, limit: int = 50) -> list[dict[str, Any]]:
        client = self._ensure_client()
        # Bolt: Using get_dialogs() is more efficient for simple listings as it
        # fetches all results in a single request, avoiding N+1 sequential I/O
        # overhead from async iteration over the stream.
        dialogs = await client.get_dialogs(limit=limit)
        return [self._serialize_dialog(d) for d in dialogs]

    async def get_chat_info(self, chat_id: str | int) -> dict[str, Any]:
        client = self._ensure_client()
        entity = await client.get_entity(chat_id)
        # get_entity is typed to also return a list; a scalar chat_id never does.
        info: dict[str, Any] = {"id": entity.id}  # ty: ignore[missing-union-attribute]
        if isinstance(entity, (Channel, Chat)):
            info["title"] = getattr(entity, "title", "")
            info["participants_count"] = getattr(entity, "participants_count", None)
        elif isinstance(entity, User):
            info["first_name"] = getattr(entity, "first_name", "")
            info["last_name"] = getattr(entity, "last_name", "")
            info["username"] = getattr(entity, "username", None)
        return info

    async def create_chat(
        self, title: str, *, is_channel: bool = False
    ) -> dict[str, Any]:
        client = self._ensure_client()
        if is_channel:
            from telethon.tl.functions.channels import CreateChannelRequest

            result = await client(
                CreateChannelRequest(title=title, about="", megagroup=False)
            )
        else:
            from telethon.tl.functions.messages import CreateChatRequest

            result = await client(CreateChatRequest(title=title, users=[]))
        # Extract chat from Updates
        chat = result.chats[0] if result.chats else None
        if chat:
            return {"id": chat.id, "title": getattr(chat, "title", title)}
        return {"title": title}

    async def join_chat(self, link_or_hash: str) -> bool:
        client = self._ensure_client()
        from telethon.tl.functions.messages import ImportChatInviteRequest

        if "joinchat/" in link_or_hash or "/+" in link_or_hash:
            # Extract hash from invite link
            invite_hash = link_or_hash.split("/")[-1]
            if invite_hash.startswith("+"):
                invite_hash = invite_hash[1:]
            await client(ImportChatInviteRequest(invite_hash))
        else:
            # Public username/link
            await client(ImportChatInviteRequest(link_or_hash))
        return True

    async def leave_chat(self, chat_id: str | int) -> bool:
        client = self._ensure_client()
        from telethon.tl.functions.channels import LeaveChannelRequest

        entity = await client.get_entity(chat_id)
        if isinstance(entity, Channel):
            await client(LeaveChannelRequest(entity))
        else:
            from telethon.tl.functions.messages import DeleteChatUserRequest

            me = await client.get_me()
            chat_id_int: int = entity.id  # ty: ignore[missing-union-attribute]
            user_id_int: int = me.id  # ty: ignore[missing-union-attribute]
            await client(
                DeleteChatUserRequest(chat_id=chat_id_int, user_id=user_id_int)
            )
        return True

    async def get_members(
        self, chat_id: str | int, *, limit: int = 50
    ) -> list[dict[str, Any]]:
        client = self._ensure_client()
        # Bolt: Avoid the get_participants() anti-pattern, which just calls
        # iter_participants(...).collect(). Using async comprehensions improves
        # memory efficiency without worsening network latency.
        return [
            self._serialize_user(user)
            async for user in client.iter_participants(chat_id, limit=limit)
        ]

    async def promote_admin(
        self, chat_id: str | int, user_id: int, *, demote: bool = False
    ) -> bool:
        client = self._ensure_client()
        from telethon.tl.functions.channels import EditAdminRequest
        from telethon.tl.types import ChatAdminRights

        if demote:
            rights = ChatAdminRights()
        else:
            rights = ChatAdminRights(
                post_messages=True,
                edit_messages=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                manage_call=True,
            )
        await client(
            EditAdminRequest(
                channel=chat_id, user_id=user_id, admin_rights=rights, rank=""
            )
        )
        return True

    async def update_chat_settings(self, chat_id: str | int, **kwargs: Any) -> bool:
        client = self._ensure_client()
        if "title" in kwargs:
            from telethon.tl.functions.channels import EditTitleRequest

            await client(EditTitleRequest(channel=chat_id, title=kwargs["title"]))
        if "description" in kwargs:
            from telethon.tl.functions.messages import EditChatAboutRequest

            await client(
                EditChatAboutRequest(peer=chat_id, about=kwargs["description"])
            )
        return True

    async def manage_topics(
        self, chat_id: str | int, action: str, **kwargs: Any
    ) -> dict[str, Any]:
        client = self._ensure_client()
        match action:
            case "list":
                from telethon.tl.functions.messages import GetForumTopicsRequest

                entity = await client.get_entity(chat_id)
                result = await client(
                    GetForumTopicsRequest(
                        peer=entity,
                        offset_date=None,
                        offset_id=0,
                        offset_topic=0,
                        limit=kwargs.get("limit", 100),
                    )
                )
                topics = [
                    {
                        "id": t.id,
                        "title": t.title,
                        "icon_emoji_id": getattr(t, "icon_emoji_id", None),
                    }
                    for t in result.topics
                ]
                return {"topics": topics, "count": len(topics)}
            case "create":
                from telethon.tl.functions.messages import CreateForumTopicRequest

                result = await client(
                    CreateForumTopicRequest(
                        peer=chat_id,
                        title=kwargs.get("name", "Topic"),
                        random_id=0,
                    )
                )
                return {"topic_id": result.updates[0].id if result.updates else None}
            case "close":
                from telethon.tl.functions.messages import EditForumTopicRequest

                await client(
                    EditForumTopicRequest(
                        peer=chat_id,
                        topic_id=kwargs["topic_id"],
                        closed=True,
                    )
                )
                return {"closed": True}
            case _:
                return {"error": f"Unknown topic action: {action}"}

    # --- Media ---
    async def send_media(
        self,
        chat_id: str | int,
        media_type: str,
        file_path_or_url: str,
        *,
        caption: str | None = None,
    ) -> dict[str, Any]:
        client = self._ensure_client()
        kwargs: dict[str, Any] = {}
        if caption:
            kwargs["caption"] = caption
        if media_type == "voice":
            kwargs["voice_note"] = True
        elif media_type == "video":
            kwargs["video_note"] = False

        if file_path_or_url.strip().lower().startswith(("http://", "https://")):
            file_to_send = await fetch_url_safely(file_path_or_url.strip())
        else:
            path = validate_file_path(file_path_or_url)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path_or_url}")
            max_size = 50 * 1024 * 1024  # 50MB
            if path.stat().st_size > max_size:
                msg_err = f"File size exceeds maximum allowed ({max_size} bytes)"
                raise SecurityError(msg_err)
            file_to_send = path
        msg = await client.send_file(chat_id, file_to_send, **kwargs)
        return self._serialize_message(msg)

    async def download_media(
        self,
        chat_id: str | int,
        message_id: int,
        *,
        file_id: str | None = None,
        output_dir: str | None = None,
    ) -> str:
        # file_id is a bot-mode-only concept (Bot API cannot look up a
        # message's media by chat_id/message_id); user mode always resolves
        # media via the Telethon chat/message lookup below, so it is ignored.
        client = self._ensure_client()
        messages = await client.get_messages(chat_id, ids=message_id)
        msg = (
            messages
            if not isinstance(messages, list)
            else messages[0]
            if messages
            else None
        )
        if msg is None or msg.media is None:
            msg_text = "Message has no media to download."
            raise ValueError(msg_text)

        download_path: Path | str | None = None
        if output_dir:
            safe_dir = validate_output_dir(output_dir)
            # Bolt: Move blocking I/O to a background thread
            await asyncio.to_thread(safe_dir.mkdir, parents=True, exist_ok=True)
            download_path = await client.download_media(msg, file=str(safe_dir))
        else:
            download_path = await client.download_media(msg)

        if download_path is None:
            msg_text = "Failed to download media."
            raise ValueError(msg_text)
        return str(download_path)

    # --- Contacts ---
    async def list_contacts(self) -> list[dict[str, Any]]:
        client = self._ensure_client()
        from telethon.tl.functions.contacts import GetContactsRequest

        result = await client(GetContactsRequest(hash=0))
        users = getattr(result, "users", [])
        return [self._serialize_user(u) for u in users]

    async def search_contacts(self, query: str) -> list[dict[str, Any]]:
        client = self._ensure_client()
        from telethon.tl.functions.contacts import SearchRequest

        result = await client(SearchRequest(q=query, limit=50))
        return [self._serialize_user(u) for u in result.users]

    async def add_contact(
        self, phone: str, first_name: str, *, last_name: str | None = None
    ) -> bool:
        client = self._ensure_client()
        result = await client(
            AddContactRequest(
                id=InputPhoneContact(
                    client_id=0,
                    phone=phone,
                    first_name=first_name,
                    last_name=last_name or "",
                ),
                first_name=first_name,
                last_name=last_name or "",
                phone=phone,
            )
        )
        return bool(result)

    async def block_user(self, user_id: int, *, unblock: bool = False) -> bool:
        client = self._ensure_client()
        if unblock:
            await client(UnblockRequest(id=user_id))
        else:
            await client(BlockRequest(id=user_id))
        return True
