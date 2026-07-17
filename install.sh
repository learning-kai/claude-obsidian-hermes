#!/usr/bin/env bash
set -euo pipefail
PORT="/home/admin/claude-obsidian-hermes"
VAULT="${CLAUDE_OBSIDIAN_VAULT:-/home/admin/claude-obsidian-vault}"
SKILL_HOME="${HOME}/.hermes/skills/note-taking"
echo "[install] port=$PORT vault=$VAULT"
mkdir -p "$SKILL_HOME"
# reinstall skills from adapted
if [[ -d "$PORT/adapted/skills" ]]; then
  for d in "$PORT/adapted/skills"/*; do
    [[ -d "$d" ]] || continue
    name=$(basename "$d")
    dest="$SKILL_HOME/claude-obsidian-$name"
    rm -rf "$dest"
    cp -a "$d" "$dest"
  done
  # umbrella if present in skill home already
  if [[ -f "$SKILL_HOME/claude-obsidian/SKILL.md" ]]; then
    echo "[install] umbrella present"
  else
    echo "[install] warning: umbrella missing — restore from backup or re-run port bootstrap"
  fi
fi
mkdir -p "$VAULT"/{.raw,wiki/{sources,entities,concepts,domains,comparisons,questions,meta,canvases,folds,references},_templates,.vault-meta/locks,Inbox,scripts,bin}
echo "[install] vault dirs ok"
echo "[install] done. Use skill_view(name=claude-obsidian)"
