# Hooks on Hermes

Upstream Claude Code hooks (`hooks.json`) are **not** executed by Hermes.

Equivalents:
- multi-writer safety: `scripts/wiki-lock.sh`
- inbox automation: cron `claude_obsidian_inbox_triage.py`
- transport: filesystem default via `.vault-meta/transport.json`
- git auto-commit: not enabled (manual only)

Upstream hook files kept here for reference.
