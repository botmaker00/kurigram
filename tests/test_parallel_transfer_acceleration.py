import asyncio
import io
import math
import os
import pytest
from unittest.mock import AsyncMock, MagicMock

import pyrogram
from pyrogram import raw, types
from pyrogram.file_id import FileId, FileType


@pytest.mark.asyncio
async def test_socket_tuning():
    from pyrogram.connection.transport.tcp.tcp import TCP

    tcp = TCP(ipv6=False, proxy=None, crypto_executor_workers=1)
    mock_writer = MagicMock()
    mock_sock = MagicMock()
    mock_writer.get_extra_info.return_value = mock_sock
    tcp.writer = mock_writer

    tcp._tune_socket()
    assert mock_sock.setsockopt.call_count >= 3


@pytest.mark.asyncio
async def test_get_media_sessions_pool():
    app = pyrogram.Client(":memory:", api_id=12345, api_hash="0123456789abcdef0123456789abcdef")
    
    mock_session_1 = MagicMock()
    mock_session_2 = MagicMock()
    mock_session_3 = MagicMock()

    created_sessions = [mock_session_1, mock_session_2, mock_session_3]
    call_idx = 0

    async def fake_get_session(dc_id, is_media=False, temporary=False):
        nonlocal call_idx
        sess = created_sessions[call_idx]
        call_idx += 1
        return sess

    app.get_session = fake_get_session

    pool = await app.get_media_sessions(dc_id=2, count=3)
    assert len(pool) == 3
    assert pool[0] is mock_session_1
    assert pool[1] is mock_session_2
    assert pool[2] is mock_session_3

    # Subsequent call reuses the existing pool without re-creating
    pool2 = await app.get_media_sessions(dc_id=2, count=3)
    assert pool2 == pool
    assert call_idx == 3


@pytest.mark.asyncio
async def test_save_file_parallel():
    app = pyrogram.Client(":memory:", api_id=12345, api_hash="0123456789abcdef0123456789abcdef")
    
    invoked_rpcs = []

    async def fake_invoke(query):
        invoked_rpcs.append(query)
        await asyncio.sleep(0.001)
        return True

    mock_sess1 = MagicMock()
    mock_sess1.invoke = AsyncMock(side_effect=fake_invoke)
    mock_sess2 = MagicMock()
    mock_sess2.invoke = AsyncMock(side_effect=fake_invoke)

    async def fake_get_media_sessions(dc_id, count=4):
        return [mock_sess1, mock_sess2]

    app.get_media_sessions = fake_get_media_sessions
    app.storage = MagicMock()
    app.storage.dc_id = AsyncMock(return_value=2)

    # 1.5 MB test file -> 3 parts of 512KB
    file_bytes = b"X" * (1536 * 1024)
    bio = io.BytesIO(file_bytes)
    bio.name = "test_upload.dat"

    progress_calls = []

    def on_progress(current, total):
        progress_calls.append((current, total))

    result = await app.save_file(bio, progress=on_progress)

    assert isinstance(result, raw.types.InputFile)
    assert result.parts == 3
    assert len(invoked_rpcs) == 3
    # Check that both sessions received parts (parallel distribution)
    assert mock_sess1.invoke.call_count >= 1
    assert mock_sess2.invoke.call_count >= 1
    assert len(progress_calls) == 3
    assert progress_calls[-1] == (len(file_bytes), len(file_bytes))


@pytest.mark.asyncio
async def test_get_file_pipelined_prefetch():
    app = pyrogram.Client(":memory:", api_id=12345, api_hash="0123456789abcdef0123456789abcdef")

    chunk_size = 1024 * 1024
    # 3.5 MB file: 3 full 1MB chunks + 1 0.5MB chunk
    chunk_0 = b"A" * chunk_size
    chunk_1 = b"B" * chunk_size
    chunk_2 = b"C" * chunk_size
    chunk_3 = b"D" * (512 * 1024)

    chunks_by_offset = {
        0: chunk_0,
        chunk_size: chunk_1,
        2 * chunk_size: chunk_2,
        3 * chunk_size: chunk_3,
    }

    invoked_offsets = []

    async def fake_invoke(query, sleep_threshold=30):
        offset = query.offset
        invoked_offsets.append(offset)
        data = chunks_by_offset.get(offset, b"")
        await asyncio.sleep(0.001)
        return raw.types.upload.File(type=raw.types.storage.FilePartial(), mtime=0, bytes=data)

    mock_sess1 = MagicMock()
    mock_sess1.invoke = AsyncMock(side_effect=fake_invoke)
    mock_sess2 = MagicMock()
    mock_sess2.invoke = AsyncMock(side_effect=fake_invoke)

    async def fake_get_session(dc_id, is_media=False, temporary=False):
        return mock_sess1

    async def fake_get_media_sessions(dc_id, count=4):
        return [mock_sess1, mock_sess2]

    app.get_session = fake_get_session
    app.get_media_sessions = fake_get_media_sessions

    # Dummy FileId
    file_id = FileId(
        major=4,
        minor=30,
        file_type=FileType.DOCUMENT,
        dc_id=2,
        media_id=123456,
        access_hash=7891011,
        file_reference=b"ref123"
    )

    yielded_chunks = []
    progress_updates = []

    def on_progress(current, total):
        progress_updates.append((current, total))

    async for chunk in app.get_file(file_id, file_size=int(3.5 * 1024 * 1024), progress=on_progress):
        yielded_chunks.append(chunk)

    assert len(yielded_chunks) == 4
    assert yielded_chunks[0] == chunk_0
    assert yielded_chunks[1] == chunk_1
    assert yielded_chunks[2] == chunk_2
    assert yielded_chunks[3] == chunk_3

    # All 4 chunks were fetched across sessions
    assert len(invoked_offsets) == 4
    assert invoked_offsets == [0, chunk_size, 2 * chunk_size, 3 * chunk_size]
    # Check that sessions were distributed
    assert mock_sess1.invoke.call_count >= 1
    assert mock_sess2.invoke.call_count >= 1
    assert len(progress_updates) == 4
    assert progress_updates[-1][0] == int(3.5 * 1024 * 1024)
