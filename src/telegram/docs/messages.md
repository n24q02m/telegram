# Telegram Messages

Manage messages: send, edit, delete, forward, pin, react, search, and browse history.

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
