import asyncio
import io
import math
import os
import pytest
from unittest.mock import AsyncMock, MagicMock

import pyrogram
from pyrogram import raw, types


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
async def test_save_file_standard():
    app = pyrogram.Client(":memory:", api_id=12345, api_hash="0123456789abcdef0123456789abcdef")

    invoked_rpcs = []

    async def fake_invoke(query):
        invoked_rpcs.append(query)
        await asyncio.sleep(0.001)
        return True

    mock_sess = MagicMock()
    mock_sess.invoke = AsyncMock(side_effect=fake_invoke)

    app.get_session = AsyncMock(return_value=mock_sess)
    app.storage = MagicMock()
    app.storage.dc_id = AsyncMock(return_value=2)
    app.loop = asyncio.get_running_loop()
    app.rnd_id = MagicMock(return_value=12345678)
    app.me = MagicMock(is_premium=False)

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
    assert mock_sess.invoke.call_count == 3
