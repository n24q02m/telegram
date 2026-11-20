# Telegram Media

Send and download media files: photos, documents, voice messages, and videos.

## Actions

### send_photo
Send a photo.
- **chat_id** (required): Chat ID or username
- **file_path_or_url** (required): Local file path or URL
- **caption**: Photo caption

### send_file
Send a document/file.
- **chat_id** (required): Chat ID or username
- **file_path_or_url** (required): Local file path or URL
- **caption**: File caption

### send_voice
Send a voice message.
- **chat_id** (required): Chat ID or username
- **file_path_or_url** (required): Local file path or URL
- **caption**: Voice message caption

### send_video
Send a video.
- **chat_id** (required): Chat ID or username
- **file_path_or_url** (required): Local file path or URL
- **caption**: Video caption

### download
Download media from a message.
- **chat_id** (required): Chat ID or username
- **message_id** (required): Message containing media
- **file_id**: Required in bot mode, because the Bot API cannot look up a message's media by `chat_id` and `message_id`. Ignored in user mode.
- **output_dir**: Directory to save file (default: the system temp directory in bot mode, the server's working directory in user mode)
