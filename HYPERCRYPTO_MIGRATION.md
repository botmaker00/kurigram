# HyperCrypto Migration Report

## Overview
TgCrypto has been completely purged and replaced by HyperCrypto (`hypercrypto`) across the entire repository.

### Changes Made
- Removed `tgcrypto` dependency from `pyproject.toml` and substituted with `hypercrypto>=0.1.1`.
- Removed `tgcrypto` references in `README.md`.
- Refactored `pyrogram/crypto/aes.py` to directly use `hypercrypto.ige256_encrypt`, `hypercrypto.ige256_decrypt`, `hypercrypto.ctr256_encrypt`, and `hypercrypto.ctr256_decrypt`.
- Raised explicit `RuntimeError` if HyperCrypto import fails (no TgCrypto fallback or silent degradation).

## Performance Benchmarks
Tested on Python 3.12:
- AES-256-IGE Encryption/Decryption: Verified & operational.
- AES-256-CTR Encryption/Decryption: Verified & operational.
- SHA-256: Verified & operational via `hypercrypto.sha256`.

## Unit Test Status
`tests/test_crypto.py` passed with 3/3 tests succeeding.
