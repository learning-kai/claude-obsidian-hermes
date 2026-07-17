#!/usr/bin/env bash
set -euo pipefail
export CLAUDE_OBSIDIAN_VAULT="${CLAUDE_OBSIDIAN_VAULT:-/home/admin/claude-obsidian-vault}"
export CLAUDE_OBSIDIAN_MIRROR_KEY="${CLAUDE_OBSIDIAN_MIRROR_KEY:-/home/admin/.ssh/windows-tailscale}"
export CLAUDE_OBSIDIAN_MIRROR_HOST="${CLAUDE_OBSIDIAN_MIRROR_HOST:-Lenovo@100.75.182.32}"
python3 /home/admin/claude-obsidian-hermes/bin/sync_obsidian_mirror.py
