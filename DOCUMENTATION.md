# Kurigram Documentation

Welcome to the definitive, production-grade documentation for **Kurigram**.

Kurigram is an actively maintained, elegant, modern, and asynchronous Telegram MTProto API framework in Python for both user accounts and bot identities. Designed as a next-generation drop-in replacement for Pyrogram, Kurigram provides first-class support for the latest Telegram features—including Telegram Bot API 10.1, 10.2, and 10.3 specifications, Rich Messages, Telegram Business, Telegram Stories, Forum Topics, Star Payments & Gifts, Ephemeral Messages, Communities, and native HyperCrypto hardware-accelerated encryption.

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Installation](#2-installation)
- [3. Telegram API Credentials](#3-telegram-api-credentials)
- [4. First Kurigram Application](#4-first-kurigram-application)
- [5. User Account Login](#5-user-account-login)
- [6. Bot Login](#6-bot-login)
- [7. Client Configuration](#7-client-configuration)
- [8. Client Lifecycle](#8-client-lifecycle)
- [9. Handlers](#9-handlers)
- [10. Decorators](#10-decorators)
- [11. Filters](#11-filters)
- [12. Messages](#12-messages)
- [13. Sending Messages](#13-sending-messages)
- [14. Media Uploading](#14-media-uploading)
- [15. Media Downloading](#15-media-downloading)
- [16. File IDs and Telegram Media](#16-file-ids-and-telegram-media)
- [17. Chats](#17-chats)
- [18. Users and Members](#18-users-and-members)
- [19. Iterators](#19-iterators)
- [20. Callback Queries](#20-callback-queries)
- [21. Inline Queries](#21-inline-queries)
- [22. Inline Keyboards](#22-inline-keyboards)
- [23. Reply Keyboards](#23-reply-keyboards)
- [24. Commands](#24-commands)
- [25. Inline Mode](#25-inline-mode)
- [26. Web Apps](#26-web-apps)
- [27. Chat Join Requests](#27-chat-join-requests)
- [28. Polls](#28-polls)
- [29. Reactions](#29-reactions)
- [30. Stories](#30-stories)
- [31. Topics / Forum](#31-topics--forum)
- [32. Business Features](#32-business-features)
- [33. Gifts / Stars / Payments](#33-gifts--stars--payments)
- [34. Rich Messages](#34-rich-messages)
- [35. Ephemeral Messages](#35-ephemeral-messages)
- [36. Draft Messages](#36-draft-messages)
- [37. Communities](#37-communities)
- [38. Subscription Updates](#38-subscription-updates)
- [39. Enums](#39-enums)
- [40. Types](#40-types)
- [41. Parse Modes and Formatting](#41-parse-modes-and-formatting)
- [42. Message Entities](#42-message-entities)
- [43. Raw MTProto API](#43-raw-mtproto-api)
- [44. Raw Updates](#44-raw-updates)
- [45. Error Handling](#45-error-handling)
- [46. FloodWait and Rate Limits](#46-floodwait-and-rate-limits)
- [47. Proxy Support](#47-proxy-support)
- [48. Storage and Sessions](#48-storage-and-sessions)
- [49. Crypto](#49-crypto)
- [50. Performance](#50-performance)
- [51. Asyncio](#51-asyncio)
- [52. Synchronous Usage](#52-synchronous-usage)
- [53. Custom Filters](#53-custom-filters)
- [54. Custom Handlers](#54-custom-handlers)
- [55. Middleware / Plugins / Extensibility](#55-middleware--plugins--extensibility)
- [56. Logging and Debugging](#56-logging-and-debugging)
- [57. Production Deployment](#57-production-deployment)
- [58. Environment Variables](#58-environment-variables)
- [59. Complete Bot Example](#59-complete-bot-example)
- [60. Complete Userbot Example](#60-complete-userbot-example)
- [61. Complete Media Bot Example](#61-complete-media-bot-example)
- [62. Pyrogram Compatibility](#62-pyrogram-compatibility)
- [63. Migration Guide](#63-migration-guide)
- [64. Bot API 10.1 / 10.2 / 10.3 Compatibility](#64-bot-api-101--102--103-compatibility)
- [65. API Reference](#65-api-reference)
- [66. Method Reference Format](#66-method-reference-format)
- [67. Type Reference Format](#67-type-reference-format)
- [68. Security](#68-security)
- [69. Common Mistakes](#69-common-mistakes)
- [70. FAQ](#70-faq)
- [71. Best Practices](#71-best-practices)
- [72. Version Information](#72-version-information)

---
## 1. Introduction

### What Kurigram Is
**Kurigram** is an asynchronous Python framework built directly on Telegram's binary MTProto 2.0 protocol (Layer 227). Unlike HTTP Bot API wrappers that connect via JSON endpoints (`api.telegram.org`), Kurigram establishes direct TCP/TLS MTProto sessions to Telegram's distributed Data Centers (DCs).

### What Problem It Solves
- **Universal Client Capabilities**: Kurigram seamlessly runs both **User Accounts** (creating custom clients, automation tools, or userbots) and **Bot Identities** (operating bots over MTProto with no HTTP size caps).
- **Direct MTProto Speed**: Large files (up to 2,000 MB for standard accounts and 4,000 MB for Telegram Premium users) can be uploaded and downloaded without the 50 MB HTTP Bot API restriction.
- **Modern Telegram Protocol Features**: Native support for Stories, Business accounts, Star gifts, Forum topics, Reactions, Ephemeral messages, and Rich layout blocks.
- **Cryptographic Performance**: Features built-in acceleration powered by **HyperCrypto** (Rust-based AES-IGE/CTR) and TgCrypto.

---
## 2. Installation

### Stable Installation
Install Kurigram from PyPI:
```bash
pip install kurigram
```

### High-Performance Installation (Recommended)
Install Kurigram with native cryptographic acceleration and fast event loops:
```bash
pip install kurigram[fast]
```
The `fast` extra installs:
- `hypercrypto>=0.1.1`: Rust-implemented AES-256-IGE and AES-256-CTR cryptographic engine.
- `uvloop<=0.22.1`: Fast event loop implementation for Linux and macOS.

### Development Installation
To install the latest development snapshot directly from GitHub:
```bash
pip install https://github.com/KurimuzonAkuma/kurigram/archive/dev.zip --force-reinstall
```

### Python and OS Requirements
- **Python**: `>=3.8` (fully tested across Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, and 3.14).
- **Operating Systems**: Linux (Ubuntu, Debian, Alpine, CentOS), Windows 10/11, macOS, and Android (Termux).

---
## 3. Telegram API Credentials

To communicate with Telegram Data Centers, you must obtain API credentials:
1. Log in with your phone number at [https://my.telegram.org](https://my.telegram.org).
2. Go to **API development tools** and create a new application.
3. Note your numeric **API ID** (`api_id`) and 32-character hexadecimal **API Hash** (`api_hash`).
4. If developing a bot, obtain a **Bot Token** (`bot_token`) from [@BotFather](https://t.me/BotFather).

> [!WARNING]
> Never commit `api_hash`, `bot_token`, or `.session` files to public version control. Keep them in environment variables or `.env` files.

---
## 4. First Kurigram Application

Create a file named `bot.py`:

```python
import os
from pyrogram import Client, filters

app = Client(
    "my_first_app",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message):
    await message.reply_text("Hello from Kurigram!")

if __name__ == "__main__":
    app.run()
```

### How It Works:
- `Client("my_first_app", ...)`: Initializes the MTProto client session.
- `@app.on_message(filters.command("start"))`: Registers an event handler that filters for the `/start` command.
- `await message.reply_text(...)`: Sends an MTProto message response back to the sender.
- `app.run()`: Starts the event loop, connects to the DC, listens for incoming events, and cleanly handles termination signals.

---
## 5. User Account Login

Kurigram allows user accounts to log in and interact with Telegram:

```python
import os
from pyrogram import Client

app = Client(
    "my_user_session",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    phone_number="+1234567890"  # Optional: prompted in terminal if omitted
)

async def main():
    async with app:
        me = await app.get_me()
        print(f"Logged in as: {me.first_name} (@{me.username}) [ID: {me.id}]")

if __name__ == "__main__":
    app.run(main())
```

### Supported Login Flows:
1. **Interactive Terminal Login**: Prompts securely for phone number, login code, and 2FA password.
2. **In-Memory Sessions**: Run ephemeral sessions without creating sqlite files on disk:
   ```python
   app = Client("memory_session", api_id=API_ID, api_hash=API_HASH, in_memory=True)
   ```
3. **Session Strings**: Export session state to a portable string:
   ```python
   session_str = await app.export_session_string()
   # Restore on any server:
   app = Client("app", session_string=session_str)
   ```

---
## 6. Bot Login

Bot identities authenticate via MTProto using their Bot Token:

```python
import os
from pyrogram import Client

app = Client(
    "bot_session",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

app.run()
```

### Bot Capabilities & Differences:
- Connects directly to MTProto servers using `auth.importBotAuthorization`.
- Supports downloading and uploading files up to 2,000 MB (compared to 50 MB on HTTP Bot API).
- Does not have a dialogue list (`get_dialogs()` is restricted to user accounts).

---
## 7. Client Configuration

The `Client` class offers comprehensive configuration options:

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `name` | `str` | *Required* | Name of the session. |
| `api_id` | `int \| str` | `None` | Telegram API ID from my.telegram.org. |
| `api_hash` | `str` | `None` | Telegram API Hash from my.telegram.org. |
| `bot_token` | `str` | `None` | Bot Token for bot authentication. |
| `session_string`| `str` | `None` | Serialized session string to restore state without file. |
| `in_memory` | `bool` | `False` | Run session in RAM without creating an sqlite file. |
| `workers` | `int` | `min(32, cpu+4)` | Maximum concurrent worker tasks processing incoming updates. |
| `workdir` | `str \| Path` | Script dir | Directory where `.session` database files are stored. |
| `plugins` | `dict` | `None` | Smart plugin settings dict: `dict(root="plugins")`. |
| `parse_mode` | `ParseMode` | `DEFAULT` | Text parse mode (`DEFAULT` parses Markdown & HTML). |
| `no_updates` | `bool` | `False` | Disables update stream; ideal for cron jobs/CLI tools. |
| `skip_updates`| `bool` | `True` | Ignores pending updates that arrived while the client was offline. |
| `takeout` | `bool` | `False` | Enables takeout session with higher rate-limits for data export. |
| `sleep_threshold`| `int` | `10` | Auto-sleeps on FloodWait if wait time is under this threshold. |
| `hide_password`| `bool` | `False` | Hides 2FA password in terminal prompt. |
| `max_concurrent_transmissions` | `int` | `1` | Maximum parallel chunk streams for media upload/download. |
| `proxy` | `dict \| str`| `None` | SOCKS4, SOCKS5, or HTTP proxy configuration. |
| `ipv6` | `bool` | `False` | Connects to Telegram servers using IPv6. |
| `test_mode` | `bool` | `False` | Connects to Telegram Test Data Centers (Test DC). |

---
## 8. Client Lifecycle

Kurigram supports multiple lifecycle models:

### 1. Simple Blocking `app.run()`
```python
app.run()
```

### 2. Async Context Manager
```python
async def main():
    async with app:
        await app.send_message("me", "Online via context manager!")

asyncio.run(main())
```

### 3. Explicit `start()` and `stop()`
```python
await app.start()
# Execute operations...
await app.stop()
```

### 4. `idle()` and `compose()`
```python
from pyrogram import Client, idle, compose

async def main():
    apps = [Client("bot1"), Client("bot2")]
    await compose(apps)

# Or with idle:
async def run_single():
    await app.start()
    await idle()
    await app.stop()
```

---
## 9. Handlers

Kurigram includes **30 distinct handler types** in `pyrogram.handlers`:

| Handler | Update Object | Description |
| :--- | :--- | :--- |
| `MessageHandler` | `Message` | Incoming messages in private, group, or channel chats. |
| `EditedMessageHandler` | `Message` | Edited messages. |
| `DeletedMessagesHandler` | `List[Message]` | Notification of deleted messages. |
| `CallbackQueryHandler` | `CallbackQuery` | Inline keyboard button clicks. |
| `InlineQueryHandler` | `InlineQuery` | Inline search queries (`@bot query`). |
| `ChosenInlineResultHandler`| `ChosenInlineResult`| Result chosen by user from an inline query. |
| `ChatMemberUpdatedHandler` | `ChatMemberUpdated` | Member joins, leaves, promotions, bans. |
| `ChatJoinRequestHandler` | `ChatJoinRequest` | Join requests to private channels or groups. |
| `StoryHandler` | `Story` | New or updated Telegram Stories. |
| `PollHandler` | `Poll` | Poll votes and state changes. |
| `MessageReactionHandler` | `MessageReactionUpdated`| Reactions added or removed from messages. |
| `MessageReactionCountHandler`| `MessageReactionCountUpdated`| Reaction counter changes in public channels. |
| `BusinessConnectionHandler`| `BusinessConnection` | Telegram Business connection updates. |
| `BusinessMessageHandler` | `Message` | Messages received through Telegram Business connections. |
| `EditedBusinessMessageHandler`| `Message` | Edited business messages. |
| `DeletedBusinessMessagesHandler`| `List[Message]` | Deleted business messages. |
| `ChatBoostHandler` | `ChatBoostUpdated` | Channel or supergroup boost events. |
| `PreCheckoutQueryHandler` | `PreCheckoutQuery` | Payments & Telegram Stars pre-checkout validation. |
| `ShippingQueryHandler` | `ShippingQuery` | Shipping query updates for invoices. |
| `PurchasedPaidMediaHandler`| `PurchasedPaidMedia` | Star payments for locked paid media. |
| `UserStatusHandler` | `User` | User online/offline status updates. |
| `RawUpdateHandler` | `raw.base.Update` | Raw MTProto update dispatch (Layer 227). |
| `ConnectHandler` | `Client` | Dispatched when the client establishes DC connection. |
| `DisconnectHandler` | `Client` | Dispatched when the client disconnects. |
| `StartHandler` | `Client` | Dispatched upon client start. |
| `StopHandler` | `Client` | Dispatched upon client stop. |
| `ErrorHandler` | `Exception` | Dispatched when an unhandled exception occurs in a handler. |

---
## 10. Decorators

All handlers have matching decorator methods on `Client`:

```python
@app.on_message(filters.text)
async def message_handler(client, message):
    ...

@app.on_callback_query()
async def callback_handler(client, query):
    ...

@app.on_story()
async def story_handler(client, story):
    ...

@app.on_chat_join_request()
async def join_handler(client, request):
    ...

@app.on_business_message()
async def business_handler(client, message):
    ...
```

### Handler Groups:
Handlers in group 0 run first. Handlers in group 1, 2, ... run sequentially or concurrently depending on propagation:
```python
@app.on_message(group=1)
async def logging_handler(client, message):
    print(f"Logged message {message.id}")
```
To stop propagation to subsequent groups, raise `pyrogram.StopPropagation`. To continue, raise `pyrogram.ContinuePropagation`.

---
## 11. Filters

Kurigram provides **100 public filters** in `pyrogram.filters`. Combine them with `&` (AND), `|` (OR), and `~` (NOT):

### Filter Highlights:
- **Chat Types**: `filters.private`, `filters.group`, `filters.supergroup`, `filters.channel`.
- **Direction**: `filters.incoming`, `filters.outgoing`, `filters.me`, `filters.bot`.
- **Content**: `filters.text`, `filters.caption`, `filters.media`, `filters.photo`, `filters.video`, `filters.document`, `filters.audio`, `filters.voice`, `filters.sticker`, `filters.poll`, `filters.dice`, `filters.web_page`.
- **Interactions**: `filters.command("cmd")`, `filters.regex(r"pattern")`, `filters.reply`, `filters.forwarded`, `filters.mentioned`.
- **Modern Telegram**: `filters.business`, `filters.story`, `filters.paid_message`, `filters.gift`, `filters.gift_code`, `filters.topic`, `filters.quote`, `filters.media_spoiler`.

```python
# Match private text commands from a specific user
@app.on_message(filters.private & filters.command("admin") & filters.user(12345678))
async def admin_filter_example(client, message):
    await message.reply("Authorized admin command.")
```

---
## 12. Messages

Messages are represented by `pyrogram.types.Message`.

### Core Attributes:
- `message.id`: Unique identifier within the chat.
- `message.chat`: `Chat` object of the conversation.
- `message.from_user`: `User` object of the sender.
- `message.text`: Message text.
- `message.caption`: Media caption.
- `message.reply_to_message`: The message being replied to.
- `message.story`: `Story` object if replying to a story.
- `message.ephemeral_message_id`: ID of ephemeral message if applicable.

### Bound Methods:
```python
await message.reply_text("Reply text")
await message.edit_text("New edited text")
await message.delete()
await message.forward(target_chat_id)
await message.copy(target_chat_id)
await message.pin()
await message.react("👍")
```

---
## 13. Sending Messages

Kurigram provides high-level methods for sending all Telegram message types:

```python
# Text message
await app.send_message(chat_id, "Hello **world**!", parse_mode=enums.ParseMode.MARKDOWN)

# Photo
await app.send_photo(chat_id, "photo.jpg", caption="Caption text")

# Video
await app.send_video(chat_id, "video.mp4", duration=120, supports_streaming=True)

# Document
await app.send_document(chat_id, "report.pdf", caption="Report")

# Audio and Voice
await app.send_audio(chat_id, "track.mp3", title="Track", performer="Artist")
await app.send_voice(chat_id, "voice.ogg", duration=15)

# Location & Venue
await app.send_location(chat_id, latitude=37.7749, longitude=-122.4194)

# Dice
await app.send_dice(chat_id, emoji="🎯")

# Media Album
await app.send_media_group(
    chat_id,
    media=[
        types.InputMediaPhoto("img1.jpg", caption="Album"),
        types.InputMediaPhoto("img2.jpg")
    ]
)
```

---
## 14. Media Uploading

Kurigram supports media uploads from:
1. File paths (`str` or `pathlib.Path`).
2. In-memory binary buffers (`io.BytesIO`).
3. HTTP/HTTPS URLs.
4. Telegram `file_id` strings.

### Upload Progress:
```python
async def progress(current, total):
    print(f"Uploaded {current} / {total} bytes ({current / total * 100:.1f}%)")

await app.send_document(
    chat_id,
    "archive.tar.gz",
    progress=progress
)
```

---
## 15. Media Downloading

Download files of any size (up to 2,000 MB for standard accounts and 4,000 MB for Premium):

```python
# Download media from a message
path = await app.download_media(message, file_name="downloads/")

# With progress callback
async def download_progress(current, total):
    print(f"Downloaded {current} / {total} bytes")

await app.download_media(
    message.document.file_id,
    file_name="output.pdf",
    progress=download_progress
)
```

---
## 16. File IDs and Telegram Media

Telegram media is identified by a unique `file_id`. When you receive a `file_id` from Telegram, you can resend it without re-uploading the file:

```python
# Re-sending existing media instantly
await app.send_photo(target_chat_id, message.photo.file_id)
```
Kurigram decodes file IDs into raw MTProto locations (`InputFileLocation`, `InputPhotoFileLocation`, `InputDocumentFileLocation`) automatically.

---
## 17. Chats

Manage chats, supergroups, and channels:

```python
chat = await app.get_chat(chat_id)
print(f"Title: {chat.title}, Members: {chat.members_count}")

# Update metadata
await app.set_chat_title(chat_id, "New Title")
await app.set_chat_description(chat_id, "Updated description")
await app.set_chat_photo(chat_id, photo="avatar.jpg")

# Admin rights promotion
await app.promote_chat_member(
    chat_id,
    user_id,
    privileges=types.ChatAdministratorRights(
        can_manage_chat=True,
        can_delete_messages=True,
        can_manage_video_chats=True,
        can_send_welcome_messages=True  # Bot API 10.3 / Layer 227
    )
)
```

---
## 18. Users and Members

Query users and manage chat restrictions:

```python
user = await app.get_users("username")
print(f"User: {user.first_name} [ID: {user.id}], Premium: {user.is_premium}")

# Ban or unban members
await app.ban_chat_member(chat_id, user.id)
await app.unban_chat_member(chat_id, user.id)
```

---
## 19. Iterators

Kurigram provides asynchronous generators that automatically handle pagination:

```python
# Chat history
async for msg in app.get_chat_history(chat_id, limit=50):
    print(f"[{msg.id}] {msg.text}")

# Chat members
async for member in app.get_chat_members(chat_id):
    print(f"Member: {member.user.first_name}")

# Dialogs
async for dialog in app.get_dialogs(limit=20):
    print(f"Dialog: {dialog.chat.title or dialog.chat.first_name}")
```

---
## 20. Callback Queries

Handle inline button interactions:

```python
@app.on_message(filters.command("menu"))
async def send_menu(client, message):
    kb = types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("Option 1", callback_data="opt1")]
    ])
    await message.reply("Choose an option:", reply_markup=kb)

@app.on_callback_query()
async def callback_handler(client, query: types.CallbackQuery):
    if query.data == "opt1":
        await query.answer("Option 1 chosen!", show_alert=True)
        await query.edit_message_text("Option 1 confirmed.")
```

---
## 21. Inline Queries

Respond to inline searches:

```python
@app.on_inline_query()
async def inline_query_handler(client, inline_query: types.InlineQuery):
    results = [
        types.InlineQueryResultArticle(
            title="Kurigram Framework",
            input_message_content=types.InputTextMessageContent(
                "Read the docs at https://docs.kurigram.icu"
            ),
            description="Modern MTProto framework for Python"
        )
    ]
    await inline_query.answer(results, cache_time=300)
```

---
## 22. Inline Keyboards

Kurigram supports all inline button types, including Bot API 10.3 additions:

```python
keyboard = types.InlineKeyboardMarkup([
    [
        types.InlineKeyboardButton("URL", url="https://kurigram.icu"),
        types.InlineKeyboardButton("Callback", callback_data="data")
    ],
    [
        types.InlineKeyboardButton("Copy Text", copy_text=types.CopyTextButton("pip install kurigram")),
        types.InlineKeyboardButton("Disabled Button", disabled=True)
    ],
    [
        types.InlineKeyboardButton("Web App", web_app=types.WebAppInfo(url="https://example.com"))
    ]
])
```

---
## 23. Reply Keyboards

Custom persistent keyboards:

```python
reply_markup = types.ReplyKeyboardMarkup(
    [
        ["/help", "/settings"],
        [types.KeyboardButton("Send Contact", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
await app.send_message(chat_id, "Menu:", reply_markup=reply_markup)
```

---
## 24. Commands

The `filters.command` filter parses commands and arguments:

```python
@app.on_message(filters.command(["ban", "kick"], prefixes=["/", "!", "."]))
async def command_handler(client, message):
    # message.command contains: ['ban', 'username']
    if len(message.command) > 1:
        target = message.command[1]
        await message.reply(f"Processing ban for {target}")
```

---
## 25. Inline Mode

Configure inline mode via [@BotFather](https://t.me/BotFather), then answer queries with articles, photos, videos, or documents using `InlineQueryResult*` types.

---
## 26. Web Apps

Integrate Telegram Mini Apps:
- `types.WebAppInfo(url="https://...")` in buttons.
- `types.WebAppData` when the Mini App sends data back to the bot.
- `types.WebAppInitData` for cryptographic verification of user data.

---
## 27. Chat Join Requests

Handle channel and group join requests:

```python
@app.on_chat_join_request()
async def join_request_listener(client, request: types.ChatJoinRequest):
    print(f"Join request from {request.from_user.id} for {request.chat.title}")
    await client.approve_chat_join_request(request.chat.id, request.from_user.id)
```

---
## 28. Polls

Send and inspect polls:

```python
await app.send_poll(
    chat_id,
    question="Favorite Python framework?",
    options=["Kurigram", "AIOHTTP", "FastAPI"],
    is_anonymous=True,
    type=enums.PollType.REGULAR
)

@app.on_poll()
async def poll_update(client, poll: types.Poll):
    print(f"Poll {poll.id} total voters: {poll.total_voter_count}")
```

---
## 29. Reactions

Manage message reactions:

```python
# Send an emoji reaction
await app.send_reaction(chat_id, message_id, emoji="🔥")

# Send paid Telegram Stars reaction
await app.send_paid_reaction(chat_id, message_id, count=5)

# Handle incoming reaction updates
@app.on_message_reaction()
async def reaction_handler(client, reaction: types.MessageReactionUpdated):
    print(f"User {reaction.user.id} reacted with {reaction.new_reaction}")
```

---
## 30. Stories

First-class support for Telegram Stories:

```python
# Post a story
story = await app.send_story(
    chat_id="me",
    media="story_clip.mp4",
    caption="Story posted via Kurigram!",
    period=24 * 3600
)

# Listen for new stories
@app.on_story()
async def story_listener(client, story: types.Story):
    print(f"New story from {story.sender_chat.title}")
```

---
## 31. Topics / Forum

Manage forum topics in supergroups:

```python
# Create a forum topic
topic = await app.create_forum_topic(chat_id, title="Bug Reports", icon_color=0x6FB9F0)

# Send message to topic
await app.send_message(chat_id, "Topic message", message_thread_id=topic.id)

# Close or delete topic
await app.close_forum_topic(chat_id, topic.id)
await app.delete_forum_topic(chat_id, topic.id)
```

---
## 32. Business Features

Telegram Business features for enterprise accounts:

```python
@app.on_business_connection()
async def business_conn(client, connection: types.BusinessConnection):
    print(f"Business connection active for {connection.user.first_name}")

@app.on_business_message()
async def business_msg(client, message: types.Message):
    await message.reply_text("Thank you for reaching out! Our team will reply shortly.")
```

---
## 33. Gifts / Stars / Payments

Kurigram supports Telegram Stars and Collectible Gifts:

```python
# Check star balance
balance = await app.get_stars_balance()
print(f"Current Stars Balance: {balance.balance}")

# Send a gift
await app.send_gift(
    user_id=12345678,
    gift_id=54321,
    text="Happy Birthday!",
    is_private=False
)

# Inspect upgraded / collectible gift
gift_info = await app.get_upgraded_gift(gift_slug="collectible-slug")
```

---
## 34. Rich Messages

Kurigram implements a complete end-to-end pipeline for **Rich Messages** (Bot API 10.1 - 10.3):

### Core Types:
- `types.InputRichMessage`: Top-level outgoing rich container supporting `blocks`, `media`, `markdown`, or `html`.
- `types.InputRichMessageMedia`: Embedded media items linkable via `tg://photo?id=` or `tg://video?id=`.
- `types.RichBlock`: Layout blocks:
  - `InputRichBlockParagraph`
  - `InputRichBlockSectionHeading`
  - `InputRichBlockTable` (supports `is_compact`, bordered, and striped formatting)
  - `InputRichBlockBlockQuotation`
  - `InputRichBlockExpandableBlockQuotation`
  - `InputRichBlockDocument` (embedded documents with captions)
  - `InputRichBlockButtons` (matrices of rich inline buttons)

### Example:
```python
rich_msg = types.InputRichMessage(
    blocks=[
        types.InputRichBlockSectionHeading(
            text=types.RichTextBold("Release Notes v2.2"),
            size="h1"
        ),
        types.InputRichBlockParagraph(
            text=types.RichText("Below are the performance benchmarks:")
        ),
        types.InputRichBlockTable(
            cells=[
                [types.RichBlockTableCell(types.RichText("Engine"), is_header=True), types.RichBlockTableCell(types.RichText("Throughput"), is_header=True)],
                [types.RichBlockTableCell(types.RichText("HyperCrypto")), types.RichBlockTableCell(types.RichText("420 MB/s"))]
            ],
            is_compact=True
        ),
        types.InputRichBlockButtons(
            buttons=[[types.RichMessageButton("View Benchmarks", url="https://example.com")]]
        )
    ]
)

await app.send_rich_message(chat_id, rich_msg)
```

---
## 35. Ephemeral Messages

Send and update ephemeral messages:

```python
# Ephemeral parameters
params = types.EphemeralMessageParameters(ephemeral_message_id=42)

# Edit ephemeral text
await app.edit_ephemeral_message_text(
    chat_id,
    ephemeral_message_parameters=params,
    text="Ephemeral notification updated."
)
```

---
## 36. Draft Messages

Save and update cloud drafts with interruption controls:

```python
await app.send_message_draft(
    chat_id=chat_id,
    text="Draft message content...",
    can_stop=True,
    keep_on_stop=False
)
```

---
## 37. Communities

Service events for Telegram Communities are parsed into high-level types:
- `types.Community`
- `types.CommunityChatAdded`
- `types.CommunityChatRemoved`
- `types.CommunityChatJoined`

---
## 38. Subscription Updates

Handle bot subscription renewals and cancellations via `types.BotSubscriptionUpdated`.

---
## 39. Enums

Kurigram includes **91 public enums** in `pyrogram.enums`.

### Core Enums:
- `ChatType`: `PRIVATE`, `GROUP`, `SUPERGROUP`, `CHANNEL`, `BOT`.
- `ChatMemberStatus`: `OWNER`, `ADMINISTRATOR`, `MEMBER`, `RESTRICTED`, `LEFT`, `BANNED`.
- `ParseMode`: `DEFAULT`, `MARKDOWN`, `HTML`, `DISABLED`.
- `MessageMediaType`: `PHOTO`, `VIDEO`, `DOCUMENT`, `AUDIO`, `VOICE`, `STICKER`, `ANIMATION`, etc.
- `ButtonStyle`: `DEFAULT`, `PRIMARY`, `DANGER`, `SUCCESS`.

---
## 40. Types

Kurigram provides **482 public types** in `pyrogram.types`. All types derive from `pyrogram.types.Object`, supporting dictionary conversion, JSON serialization, and pretty-printing.

---
## 41. Parse Modes and Formatting

### Default Parse Mode:
By default (`enums.ParseMode.DEFAULT`), Kurigram parses both Markdown and HTML simultaneously:
```python
await app.send_message(chat_id, "<b>Bold HTML</b> and **Bold Markdown**")
```
To use strict Markdown or HTML, pass `parse_mode=enums.ParseMode.MARKDOWN` or `enums.ParseMode.HTML`.

---
## 42. Message Entities

Kurigram supports all MTProto entity types:
- `MessageEntityBold`, `MessageEntityItalic`, `MessageEntityUnderline`, `MessageEntityStrike`
- `MessageEntityCode`, `MessageEntityPre`
- `MessageEntitySpoiler`
- `MessageEntityBlockquote`, `MessageEntityExpandableBlockquote`
- `MessageEntityCustomEmoji`

---
## 43. Raw MTProto API

Invoke raw MTProto functions directly using `client.invoke()`:

```python
from pyrogram import raw

# Call raw users.GetFullUser
user_full = await app.invoke(
    raw.functions.users.GetFullUser(
        id=await app.resolve_peer("username")
    )
)
print("About:", user_full.about)
```

---
## 44. Raw Updates

Listen to unhandled or new MTProto updates:

```python
from pyrogram import raw

@app.on_raw_update()
async def raw_update_handler(client, update: raw.base.Update, users: dict, chats: dict):
    print("Raw Update:", type(update).__name__)
```

---
## 45. Error Handling

Catch exceptions from `pyrogram.errors`:

```python
from pyrogram.errors import FloodWait, BadRequest, PeerIdInvalid

try:
    await app.send_message(chat_id, "Message")
except FloodWait as e:
    print(f"Sleeping for {e.value} seconds...")
    await asyncio.sleep(e.value)
except PeerIdInvalid:
    print("Invalid chat ID.")
except BadRequest as e:
    print(f"Bad request: {e}")
```

---
## 46. FloodWait and Rate Limits

When rate limits are exceeded, Telegram returns `FloodWait` with the required wait time in seconds.

### Automatic Sleep Threshold:
Configure `sleep_threshold` on the `Client` to automatically sleep on short FloodWaits:
```python
app = Client("my_bot", sleep_threshold=30)  # Auto-sleeps up to 30 seconds
```

---
## 47. Proxy Support

Connect through SOCKS4, SOCKS5, or HTTP proxies via `python-socks`:

```python
app = Client(
    "proxied_bot",
    proxy=dict(
        scheme="socks5",
        hostname="127.0.0.1",
        port=1080,
        username="proxy_user",
        password="proxy_password"
    )
)
```

---
## 48. Storage and Sessions

Session authentication keys are saved in SQLite database files (`session_name.session`).

### In-Memory Sessions:
```python
app = Client("memory_bot", in_memory=True)
```

### Portable Session String:
```python
session_string = await app.export_session_string()
app = Client("restored_app", session_string=session_string)
```

---
## 49. Crypto

Kurigram automatically selects the fastest available cryptographic backend:
1. **HyperCrypto**: Rust-implemented AES-256-IGE/CTR cipher routines (fastest).
2. **TgCrypto**: C-implemented MTProto cryptographic acceleration.
3. **PyAes**: Pure-Python fallback (bundled by default).

---
## 50. Performance

### Tips for Maximum Throughput:
1. Install `hypercrypto` (`pip install kurigram[fast]`).
2. Use `uvloop` on Linux/macOS.
3. Configure `max_concurrent_transmissions=3` for parallel multi-part file transfers.
4. Increase `workers=32` for high-concurrency bot workloads.

---
## 51. Asyncio

Kurigram is built around standard Python `asyncio`. Use `asyncio.gather()` for concurrent tasks and avoid blocking I/O calls in event handlers.

---
## 52. Synchronous Usage

Kurigram includes automatic `async_to_sync` wrappers: outside an active event loop, Client methods can be called synchronously:

```python
from pyrogram import Client

app = Client("my_sync_app")
app.start()
app.send_message("me", "Hello synchronously!")
app.stop()
```

---
## 53. Custom Filters

Create custom filters with `filters.create`:

```python
from pyrogram import filters

async def is_admin_check(_, client, message):
    member = await message.chat.get_member(message.from_user.id)
    return member.status in (enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR)

is_admin = filters.create(is_admin_check)

@app.on_message(filters.group & is_admin)
async def admin_only_handler(client, message):
    await message.reply("Admin command received.")
```

---
## 54. Custom Handlers

Subclass `pyrogram.handlers.Handler` to define custom event routing logic.

---
## 55. Middleware / Plugins / Extensibility

Organize handlers modularly using Smart Plugins:

```python
# Directory structure:
# plugins/
#   start.py
#   echo.py

app = Client("my_bot", plugins=dict(root="plugins"))
app.run()
```
Inside `plugins/start.py`:
```python
from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start_plugin(client, message):
    await message.reply("Hello from a Smart Plugin!")
```

---
## 56. Logging and Debugging

Enable debug logging to inspect MTProto frames and connection diagnostics:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("pyrogram").setLevel(logging.DEBUG)
```

---
## 57. Production Deployment

### Systemd Service Example (`/etc/systemd/system/kurigram_bot.service`):
```ini
[Unit]
Description=Kurigram Production Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/opt/kurigram_bot
ExecStart=/opt/kurigram_bot/venv/bin/python main.py
Restart=always
RestartSec=10
EnvironmentFile=/opt/kurigram_bot/.env

[Install]
WantedBy=multi-user.target
```

---
## 58. Environment Variables

Recommended `.env` configuration template:
```env
API_ID=12345678
API_HASH=abcdef0123456789abcdef0123456789
BOT_TOKEN=123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
WORKERS=16
MAX_CONCURRENT_TRANSMISSIONS=3
```

---
## 59. Complete Bot Example

```python
import os
import logging
from pyrogram import Client, filters, types

logging.basicConfig(level=logging.INFO)

app = Client(
    "prod_bot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"]
)

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: types.Message):
    kb = types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("Docs", url="https://docs.kurigram.icu")],
        [types.InlineKeyboardButton("Click Me", callback_data="btn_click")]
    ])
    await message.reply_text("Welcome to the Kurigram Bot!", reply_markup=kb)

@app.on_callback_query(filters.regex("^btn_click$"))
async def callback_handler(client: Client, query: types.CallbackQuery):
    await query.answer("Button clicked successfully!", show_alert=True)
    await query.edit_message_text("Action confirmed via Kurigram MTProto.")

if __name__ == "__main__":
    app.run()
```

---
## 60. Complete Userbot Example

```python
import os
from pyrogram import Client, filters, types

app = Client(
    "user_client",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"]
)

@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping(client: Client, message: types.Message):
    await message.edit_text("Pong! 🏓 Running on Kurigram MTProto.")

if __name__ == "__main__":
    app.run()
```

---
## 61. Complete Media Bot Example

```python
import os
from pyrogram import Client, filters, types

app = Client(
    "media_bot",
    api_id=int(os.environ["API_ID"]),
    api_hash=os.environ["API_HASH"],
    bot_token=os.environ["BOT_TOKEN"],
    max_concurrent_transmissions=3
)

@app.on_message(filters.document | filters.video | filters.photo)
async def media_handler(client: Client, message: types.Message):
    status_msg = await message.reply("Starting download...")
    
    async def dl_progress(current, total):
        pct = current / total * 100
        # Update progress every 20%
        if int(pct) % 20 == 0:
            try:
                await status_msg.edit_text(f"Downloading: {pct:.1f}%")
            except Exception:
                pass

    file_path = await message.download(progress=dl_progress)
    await status_msg.edit_text("Download complete! Uploading...")

    await client.send_document(
        message.chat.id,
        file_path,
        caption="Re-uploaded via Kurigram"
    )
    await status_msg.delete()
    os.remove(file_path)

if __name__ == "__main__":
    app.run()
```

---
## 62. Pyrogram Compatibility

Kurigram is designed as a drop-in replacement for Pyrogram. Code written for Pyrogram runs seamlessly under Kurigram with zero modifications to `import pyrogram` statements.

---
## 63. Migration Guide

### Upgrading from Pyrogram:
1. Uninstall existing Pyrogram installation:
   ```bash
   pip uninstall pyrogram
   ```
2. Install Kurigram:
   ```bash
   pip install kurigram[fast]
   ```
3. Run your existing codebase directly—no import or method changes required.

---
## 64. Bot API 10.1 / 10.2 / 10.3 Compatibility

| Feature | Bot API Version | Kurigram Public API | MTProto Layer | Pipeline Status |
| :--- | :---: | :--- | :---: | :---: |
| **Rich Text Types (25+)** | 10.1 | `types.RichText*` | Layer 227 | **PASS** |
| **Rich Blocks (20+)** | 10.1 | `types.RichBlock*`, `types.InputRichBlock*` | Layer 227 | **PASS** |
| **Rich Message Drafts** | 10.1 | `client.send_rich_message_draft()` | Layer 227 | **PASS** |
| **Chat Join Request Query**| 10.1 | `client.answer_chat_join_request_query()` | Layer 227 | **PASS** |
| **InputMediaLink** | 10.1 | `types.InputMediaLink` | Layer 227 | **PASS** |
| **Unique Gift Info** | 10.1 | `types.UniqueGiftInfo` | Layer 227 | **PASS** |
| **InputRichMessageMedia** | 10.2 | `types.InputRichMessageMedia`, `InputRichMessage.media` | Layer 227 | **PASS** |
| **InputMediaVoiceNote** | 10.2 | `types.InputMediaVoiceNote` | Layer 227 | **PASS** |
| **Ephemeral Messages** | 10.2 | `types.EphemeralMessageParameters`, `edit_ephemeral_*` | Layer 227 | **PASS** |
| **Communities** | 10.2 | `types.Community*`, `Message._parse_service()` | Layer 227 | **PASS** |
| **BotSubscriptionUpdated**| 10.2 | `types.BotSubscriptionUpdated` | Layer 227 | **PASS** |
| **Disabled Buttons** | 10.3 | `InlineKeyboardButton(disabled=True)`, `DisabledButton` | Layer 227 | **PASS** |
| **Force Reply Serialization**| 10.3 | `InlineKeyboardMarkup(force_reply=...)` | Layer 227 | **PASS** |
| **Welcome Messages Admin Right**| 10.3 | `ChatAdministratorRights.can_send_welcome_messages` | Layer 227 | **PASS** |
| **Draft Interruption Flags**| 10.3 | `can_stop`, `keep_on_stop` in `send_message_draft()` | Layer 227 | **PASS** |
| **MessageGenerationStopped**| 10.3 | `types.MessageGenerationStopped._parse()` | Layer 227 | **PASS** |
| **RichBlockDocument** | 10.3 | `types.RichBlockDocument`, `types.InputRichBlockDocument` | Layer 227 | **PASS** |
| **Compact Tables** | 10.3 | `InputRichBlockTable(is_compact=True)` | Layer 227 | **PASS** |
| **Expandable Quotations** | 10.3 | `InputRichBlockExpandableBlockQuotation` | Layer 227 | **PASS** |

---
## 65. API Reference

Kurigram provides **429 Client methods**, **30 Handlers**, **100 Filters**, **482 Types**, **91 Enums**, and **866 Errors**.

---
## 66. Method Reference Format

### `Client.send_message()`
**Purpose**: Sends a text message to a chat.
**Signature**:
```python
async def send_message(
    chat_id: Union[int, str],
    text: str,
    parse_mode: Optional[enums.ParseMode] = None,
    entities: Optional[List[types.MessageEntity]] = None,
    disable_web_page_preview: Optional[bool] = None,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    reply_parameters: Optional[types.ReplyParameters] = None,
    schedule_date: Optional[datetime] = None,
    protect_content: Optional[bool] = None,
    message_thread_id: Optional[int] = None,
    business_connection_id: Optional[str] = None,
    reply_markup: Optional[Union[types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove, types.ForceReply]] = None
) -> types.Message
```
**Example**:
```python
await app.send_message(chat_id, "Hello **Kurigram**!")
```

---
## 67. Type Reference Format

### `types.Message`
**Purpose**: Represents an individual message in a chat.
**Important Attributes**:
- `id` (`int`): Unique message ID.
- `chat` (`types.Chat`): Chat where message was sent.
- `from_user` (`types.User`): Sender.
- `text` (`str`): Text content.
- `caption` (`str`): Media caption.
- `reply_to_message` (`types.Message`): Replied message.
- `date` (`datetime`): Timestamp.

---
## 68. Security

- Store credentials in environment variables.
- Restrict file paths when downloading user media to prevent path traversal attacks.
- Secure `.session` files with permissions `600` on Linux systems.

---
## 69. Common Mistakes

1. **`PEER_ID_INVALID`**: Occurs when trying to interact with a user/channel the client has never encountered. Resolve by fetching the user first or having them start the bot.
2. **`FloodWait`**: Telegram rate limits. Set `sleep_threshold` on Client or handle `except FloodWait as e: await asyncio.sleep(e.value)`.
3. **Calling async methods synchronously inside an event loop**: Always use `await` when calling Kurigram methods inside `async def` functions.

---
## 70. FAQ

- **Can Kurigram be used for bots and userbots?** Yes, both bot identities and user accounts are fully supported.
- **Is Kurigram faster than standard Pyrogram?** Yes, Kurigram integrates HyperCrypto in Rust for accelerated MTProto encryption.
- **Are Pyrogram plugins compatible?** Yes, Kurigram's Smart Plugins system maintains 100% compatibility.

---
## 71. Best Practices

1. Use `uvloop` and `hypercrypto` for maximum networking and encryption speed.
2. Never block the event loop with synchronous I/O operations (`time.sleep` -> `asyncio.sleep`).
3. Set sensible `sleep_threshold` values to smoothly handle short FloodWaits.
4. Clean up temporary downloaded files after processing.

---
## 72. Version Information

- **Kurigram Version**: `2.2.25`
- **MTProto Protocol Layer**: `Layer 227`
- **Telegram Bot API Compatibility**: Full coverage up to **Bot API 10.3**
- **Documentation Verification Date**: 2026-09-28
- **Repository Branch**: `dev`
- **License**: GNU Lesser General Public License v3.0 (LGPL-3.0)

---
