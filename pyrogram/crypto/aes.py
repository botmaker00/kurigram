#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import logging

log = logging.getLogger(__name__)

BACKEND = None


def xor(a: bytes, b: bytes) -> bytes:
    return int.to_bytes(
        int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
        len(a),
        "big",
    )


try:
    import hypercrypto

    _test_k = b"\x00" * 32
    _test_iv = b"\x00" * 32
    _test_data = b"\x00" * 16
    assert hypercrypto.ige256_encrypt(_test_data, _test_k, _test_iv) is not None
    assert hypercrypto.ctr256_encrypt(_test_data, _test_k, _test_iv[:16]) is not None

    BACKEND = "HyperCrypto"
    log.info("Using HyperCrypto")

    def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return hypercrypto.ige256_encrypt(data, key, iv)

    def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return hypercrypto.ige256_decrypt(data, key, iv)

    def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        state = state if state is not None else bytearray(1)
        dlen = len(data)
        if dlen == 0:
            return b""

        out = bytearray(dlen)
        offset = 0

        if state[0] > 0:
            avail = 16 - state[0]
            take = min(dlen, avail)
            ks = hypercrypto.ctr256_encrypt(b"\x00" * 16, key, bytes(iv))
            for i in range(take):
                out[i] = data[i] ^ ks[state[0] + i]
            offset += take

        rem = dlen - offset
        if rem > 0:
            curr_iv_val = int.from_bytes(iv, "big")
            if offset > 0:
                curr_iv_val = (curr_iv_val + 1) & ((1 << 128) - 1)

            rem_data = data[offset:] if offset > 0 else data
            enc_rem = hypercrypto.ctr256_encrypt(rem_data, key, curr_iv_val.to_bytes(16, "big"))
            out[offset:] = enc_rem

        total = state[0] + dlen
        blocks = total // 16
        state[0] = total % 16
        if blocks > 0:
            new_iv_val = (int.from_bytes(iv, "big") + blocks) & ((1 << 128) - 1)
            iv[:] = new_iv_val.to_bytes(16, "big")

        return bytes(out)

    def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return ctr256_encrypt(data, key, iv, state)

except Exception as e:
    log.warning("HyperCrypto not available or failed self-test (%s)", e)
    try:
        import tgcrypto

        _test_k = b"\x00" * 32
        _test_iv = bytearray(32)
        _test_st = bytearray(1)
        _test_data = b"\x00" * 16
        assert tgcrypto.ige256_encrypt(_test_data, _test_k, _test_iv) is not None
        assert tgcrypto.ctr256_encrypt(_test_data, _test_k, _test_iv[:16], _test_st) is not None

        BACKEND = "TgCrypto"
        log.info("Using TgCrypto")

        def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
            return tgcrypto.ige256_encrypt(data, key, iv)

        def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
            return tgcrypto.ige256_decrypt(data, key, iv)

        def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
            return tgcrypto.ctr256_encrypt(data, key, iv, state or bytearray(1))

        def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
            return tgcrypto.ctr256_decrypt(data, key, iv, state or bytearray(1))

    except Exception as e2:
        import pyaes

        BACKEND = "PyAES"
        log.warning(
            "HyperCrypto and TgCrypto missing or failed! "
            "Kurigram will work the same, but at a much slower speed. "
            "More info: https://docs.kurigram.icu"
        )
        log.warning("Using PyAES fallback (%s)", e2)

        def ige(data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
            cipher = pyaes.AES(key)

            iv_1 = iv[:16]
            iv_2 = iv[16:]

            chunks = [data[i : i + 16] for i in range(0, len(data), 16)]

            if encrypt:
                for i, chunk in enumerate(chunks):
                    iv_1 = chunks[i] = xor(cipher.encrypt(xor(chunk, iv_1)), iv_2)
                    iv_2 = chunk
            else:
                for i, chunk in enumerate(chunks):
                    iv_2 = chunks[i] = xor(cipher.decrypt(xor(chunk, iv_2)), iv_1)
                    iv_1 = chunk

            return b"".join(chunks)

        def ctr(data: bytes, key: bytes, iv: bytearray, state: bytearray) -> bytes:
            cipher = pyaes.AES(key)

            out = bytearray(data)
            chunk = cipher.encrypt(iv)

            for i in range(0, len(data), 16):
                for j in range(0, min(len(data) - i, 16)):
                    out[i + j] ^= chunk[state[0]]

                    state[0] += 1

                    if state[0] >= 16:
                        state[0] = 0

                    if state[0] == 0:
                        for k in range(15, -1, -1):
                            try:
                                iv[k] += 1
                                break
                            except ValueError:
                                iv[k] = 0

                        chunk = cipher.encrypt(iv)

            return bytes(out)

        def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
            return ige(data, key, iv, True)

        def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
            return ige(data, key, iv, False)

        def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
            return ctr(data, key, iv, state or bytearray(1))

        def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
            return ctr(data, key, iv, state or bytearray(1))
