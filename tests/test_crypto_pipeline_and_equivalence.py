import asyncio
import hashlib
import os
import random
from io import BytesIO
from unittest.mock import AsyncMock, MagicMock
import pytest
import tgcrypto
import hypercrypto

from pyrogram.crypto import aes, mtproto
from pyrogram import raw
from pyrogram.raw.core import Message, Long
from pyrogram.methods.advanced.save_file import SaveFile


def test_crypto_backend_selection():
    assert aes.BACKEND in ("HyperCrypto", "TgCrypto", "PyAES")


def test_ige_equivalence():
    sizes = [16, 32, 64, 256, 4096, 65536]
    for size in sizes:
        key = random.randbytes(32)
        iv = random.randbytes(32)
        data = random.randbytes(size)

        res_hc = hypercrypto.ige256_encrypt(data, key, iv)
        res_tg = tgcrypto.ige256_encrypt(data, key, iv)
        assert res_hc == res_tg

        assert hypercrypto.ige256_decrypt(res_hc, key, iv) == data
        assert tgcrypto.ige256_decrypt(res_tg, key, iv) == data


def test_ctr_equivalence_and_split():
    sizes = [1, 7, 15, 16, 17, 31, 32, 33, 255, 256, 257, 4096, 65536]
    for size in sizes:
        key = random.randbytes(32)
        iv_start = random.randbytes(16)
        data = random.randbytes(size)

        # Single call
        iv_hc = bytearray(iv_start)
        st_hc = bytearray(1)
        res_hc = aes.ctr256_encrypt(data, key, iv_hc, st_hc)

        iv_tg = bytearray(iv_start)
        st_tg = bytearray(1)
        res_tg = tgcrypto.ctr256_encrypt(data, key, iv_tg, st_tg)

        assert res_hc == res_tg
        assert iv_hc == iv_tg
        assert st_hc == st_tg

        # Split call
        if size >= 3:
            p1 = size // 3
            p2 = (2 * size) // 3
            d1, d2, d3 = data[:p1], data[p1:p2], data[p2:]

            iv_split = bytearray(iv_start)
            st_split = bytearray(1)
            res_split = (
                aes.ctr256_encrypt(d1, key, iv_split, st_split)
                + aes.ctr256_encrypt(d2, key, iv_split, st_split)
                + aes.ctr256_encrypt(d3, key, iv_split, st_split)
            )

            assert res_split == res_tg
            assert iv_split == iv_tg
            assert st_split == st_tg


def test_mtproto_roundtrip():
    auth_key = os.urandom(256)
    auth_key_id = os.urandom(8)
    session_id = os.urandom(8)
    salt = random.randint(0, 2**63 - 1)

    ping = raw.functions.Ping(ping_id=12345)
    msg_id = (random.randint(100000, 999999) * 2) + 1
    seq_no = 1

    message = Message(
        msg_id=msg_id,
        seq_no=seq_no,
        length=len(ping.write()),
        body=ping
    )

    # Server sending to client
    data = Long(salt) + session_id + message.write()
    padding = os.urandom(-(len(data) + 12) % 16 + 12)
    msg_key = mtproto._sha256(auth_key[96:128] + data + padding)[8:24]
    aes_key, aes_iv = mtproto.kdf(auth_key, msg_key, False)
    packed = auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)

    unpacked = mtproto.unpack(BytesIO(packed), session_id, auth_key, auth_key_id)
    assert unpacked.msg_id == msg_id
    assert unpacked.seq_no == seq_no
    assert unpacked.body.ping_id == 12345


class MockStorage:
    async def dc_id(self):
        return 2


class MockClient(SaveFile):
    def __init__(self):
        self.save_file_semaphore = asyncio.Semaphore(1)
        self.loop = asyncio.get_event_loop()
        self.executor = None
        self.me = MagicMock()
        self.me.is_premium = False
        self.storage = MockStorage()
        self.session_mock = AsyncMock()
        self.session_mock.invoke = AsyncMock()

    def rnd_id(self):
        return 99999

    async def get_session(self, dc_id, is_media=True):
        return self.session_mock


@pytest.mark.asyncio
async def test_save_file_missing_part_retry():
    client = MockClient()
    file_bytes = b"Hello World Missing Part Test Data"
    f = BytesIO(file_bytes)
    f.name = "small.dat"

    res = await client.save_file(f, file_id=12345, file_part=0)
    assert isinstance(res, raw.types.InputFile)
    assert res.id == 12345
    assert res.md5_checksum == ""


@pytest.mark.asyncio
async def test_save_file_fresh_upload_md5():
    client = MockClient()
    file_bytes = b"Hello World Fresh Upload MD5 Test Data"
    expected_md5 = hashlib.md5(file_bytes).hexdigest()
    f = BytesIO(file_bytes)
    f.name = "small.dat"

    res = await client.save_file(f)
    assert isinstance(res, raw.types.InputFile)
    assert res.id == 99999
    assert res.md5_checksum == expected_md5


def test_mtproto_backend_tied_to_aes_backend(monkeypatch):
    assert aes.BACKEND == "HyperCrypto"
    auth_key = os.urandom(256)
    msg_key = os.urandom(16)

    # When aes.BACKEND is "HyperCrypto"
    res_kdf = mtproto.kdf(auth_key, msg_key, True)
    expected_hc = hypercrypto.kdf(auth_key, msg_key, True)
    assert res_kdf == expected_hc

    # When monkeypatched to "TgCrypto"
    monkeypatch.setattr(aes, "BACKEND", "TgCrypto")
    import importlib
    import pyrogram.crypto.mtproto as mtproto_mod
    importlib.reload(mtproto_mod)

    hc_called = False
    def mock_hc_kdf(*args, **kwargs):
        nonlocal hc_called
        hc_called = True
        return hypercrypto.kdf(*args, **kwargs)

    monkeypatch.setattr(hypercrypto, "kdf", mock_hc_kdf)

    res_kdf_fallback = mtproto_mod.kdf(auth_key, msg_key, True)
    assert not hc_called, "hypercrypto.kdf should NOT be called when aes.BACKEND != 'HyperCrypto'"
    assert res_kdf_fallback == expected_hc

    # Restore mtproto module
    monkeypatch.undo()
    importlib.reload(mtproto_mod)
