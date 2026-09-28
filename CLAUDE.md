# CLAUDE.md

Use @AGENTS.md as the source of truth for contribution workflow, checks, and Telegram Bot API / MTProto rules in this repository.

## Commands

Use these verified command forms for working with this repository:

| Task | Command |
|---|---|
| Tests | `pytest tests -q` |
| Audit Bot API | `python tests/audit_api_10.py` |
| Build Package | `hatch build` |
| Clean Build | `make clean-build` |
