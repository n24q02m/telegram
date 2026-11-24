# Telegram Messages

Manage messages: send, schedule, drafts, edit, delete, forward, pin, react, search, and browse history.

## Actions

### send
Send a new message to a chat.
- **chat_id** (required): Chat ID or username
- **text** (required): Message text
- **reply_to**: Message ID to reply to
- **parse_mode**: "HTML" or "Markdown"

### edit
Edit an existing message.
- **chat_id** (required): Chat ID or username
- **message_id** (required): Message to edit
- **text** (required): New text
- **parse_mode**: "HTML" or "Markdown"

### delete
Delete a message.
- **chat_id** (required): Chat ID or username
- **message_id** (required): Message to delete

### forward
Forward a message between chats.
- **from_chat** (required): Source chat ID
- **to_chat** (required): Destination chat ID
- **message_id** (required): Message to forward

### pin
Pin a message in a chat.
- **chat_id** (required): Chat ID or username
- **message_id** (required): Message to pin

### react
Add an emoji reaction to a message.
- **chat_id** (required): Chat ID or username
- **message_id** (required): Message to react to
- **emoji** (required): Emoji character (e.g. "👍")

### search
Search messages (user mode only).
- **query** (required): Search query
- **chat_id**: Limit search to specific chat
- **limit**: Max results (default: 20)

### history
Get chat message history (user mode only; in bot mode it returns an empty list, because the Bot API cannot read chat history).
- **chat_id** (required): Chat ID or username
- **limit**: Max messages (default: 20)
- **offset_id**: Start from this message ID

### schedule
Schedule messages or manage scheduled messages (user mode only).
- **chat_id** (required): Chat ID or username
- **schedule_action**: `"send"` (default), `"list"`, or `"delete"`
- **text** (required for `send`): Message text
- **schedule_at** (required for `send`): ISO-8601 timestamp or Unix epoch seconds
- **message_id** (required for `delete`): Scheduled message ID
- **reply_to**: Message ID to reply to (`send`)
- **parse_mode**: "HTML" or "Markdown" (`send`)
- **limit**: Max scheduled messages (`list`, default: 20)

### draft
Save, inspect, or clear cloud message drafts (user mode only).
- **draft_action**: `"save"`, `"get"` (default when `text` omitted), or `"clear"`
- **chat_id** (required for `save` / `clear`; optional filter for `get`): Chat ID or username
- **text** (required for `save`): Draft message text
- **reply_to**: Message ID to reply to (`save`)
- **parse_mode**: "HTML" or "Markdown" (`save`)
- **limit**: Max drafts when listing (`get`, default: 20)
