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

try:
    import hypercrypto

    log.info("Using HyperCrypto")

    def ige256_encrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return hypercrypto.ige256_encrypt(data, key, iv)

    def ige256_decrypt(data: bytes, key: bytes, iv: bytes) -> bytes:
        return hypercrypto.ige256_decrypt(data, key, iv)

    def ctr256_encrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return hypercrypto.ctr256_encrypt(data, key, bytes(iv) if isinstance(iv, bytearray) else iv)

    def ctr256_decrypt(data: bytes, key: bytes, iv: bytearray, state: bytearray = None) -> bytes:
        return hypercrypto.ctr256_decrypt(data, key, bytes(iv) if isinstance(iv, bytearray) else iv)

    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )
except ImportError as e:
    log.error("HyperCrypto is required for Kurigram cryptographic operations!")
    raise RuntimeError(
        "HyperCrypto is missing! Kurigram requires hypercrypto to perform cryptographic operations. "
        "Please install hypercrypto: pip install hypercrypto"
    ) from e
