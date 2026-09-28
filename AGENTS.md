# AGENTS.md

This file defines how coding agents should contribute to `kurigram` on `dev`.

## Scope and defaults

- Base branch: `dev`
- Python: `>=3.8`
- Main tooling: `pytest`, `hatch`, `git`
- Source of truth: Parity with official `kurigram-org/kurigram` and Telegram Bot API 10.3+ / MTProto.
- Keep diffs focused; avoid unrelated refactors or reformatting.

## Codebase Architecture & Navigation

- `pyrogram/client.py`: Core `Client` class, session initialization, and dispatching.
- `pyrogram/session/`: MTProto Session, MTProto encryption, Auth Key exchange, and FloodWait retry handling.
- `pyrogram/methods/`: High-level MTProto and Bot API methods (`messages`, `chats`, `advanced`, `users`, etc.).
- `pyrogram/types/`: High-level models (`Message`, `Chat`, `User`, `Update`, `ReplyParameters`, `RichMessage`, etc.).
- `pyrogram/raw/`: Generated raw MTProto TL schema types and functions.
- `pyrogram/enums/`: Telegram enumerations (ParseMode, ChatType, MessageMediaType, etc.).
- `compiler/`: TL schema and error code compilers.

## Mandatory local checks before PR

Run the verification loop before finalizing changes:

```bash
# 1. Run the test suite
pytest tests -q

# 2. Run Bot API 10.3 / feature verification
python tests/audit_api_10.py
```

## Bot API & MTProto Rules (Critical)

1. **Parity with official Kurigram:**
   - Always match `kurigram-org/kurigram` patterns.
   - Do NOT add experimental multi-session pools or break backpressure queues unless explicitly requested.

2. **File Transfer & Streaming (`save_file.py`):**
   - Maintain `Queue(1)` backpressure to prevent unbounded RAM consumption during chunk reads.
   - Workers must safely drain via sentinel values (`await queue.put(None)`).

3. **Telegram Bot API 10.3 Specifications:**
   - Full support for `RichMessage` (Markdown & HTML rich formatting).
   - Support for `InputMediaLink` (sending media links via web preview).
   - Support for ephemeral messages (`delete_ephemeral_message`, `EphemeralMessageParameters`).
   - Support for `CommunityChatJoined` service message handling.
   - Full support for Paid Messages and Star gifts.

4. **FloodWait & Error Handling:**
   - Rate limiting is strictly respected via `sleep_threshold`.
   - Never perform rapid, unthrottled `edit_message_text` calls without interval checks (minimum 3-5 seconds recommended for progress bars).

## PR quality checklist

Before requesting review or completing a task:
1. All changes adhere to existing naming and typing standards.
2. Local tests pass (`pytest tests -q`).
3. No syntax regressions or broken imports across `pyrogram/`.
4. Working tree is clean and diffs are minimal.
