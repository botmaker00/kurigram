import time
import os
import hypercrypto
from pyrogram.crypto import aes

def test_hypercrypto_aes_ige():
    key = os.urandom(32)
    iv = os.urandom(32)
    data = os.urandom(1024 * 64)

    encrypted = aes.ige256_encrypt(data, key, iv)
    decrypted = aes.ige256_decrypt(encrypted, key, iv)

    assert decrypted == data, "AES-IGE encryption/decryption failed"

def test_hypercrypto_aes_ctr():
    key = os.urandom(32)
    iv = bytearray(os.urandom(16))
    data = os.urandom(1024 * 64)

    encrypted = aes.ctr256_encrypt(data, key, iv)
    decrypted = aes.ctr256_decrypt(encrypted, key, iv)

    assert decrypted == data, "AES-CTR encryption/decryption failed"

def test_hypercrypto_sha256():
    data = b"Hello, HyperCrypto!"
    digest = hypercrypto.sha256(data)
    assert len(digest) == 32
