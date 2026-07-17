#!/usr/bin/env bash
set -euo pipefail
REPO_URL="${REPO_URL:-https://github.com/learning-kai/claude-obsidian-hermes.git}"
TARGET="${TARGET:-$HOME/claude-obsidian-hermes}"
VAULT="${CLAUDE_OBSIDIAN_VAULT:-$HOME/claude-obsidian-vault}"
if [[ ! -d "$TARGET/.git" ]]; then
  git clone "$REPO_URL" "$TARGET"
else
  git -C "$TARGET" pull --ff-only || true
fi
cd "$TARGET"
if [[ ! -d "$VAULT/wiki" ]]; then
  cp -a vault-template "$VAULT"
fi
mkdir -p "$HOME/.hermes/skills/note-taking"
for d in adapted/skills/*; do
  [[ -d "$d" ]] || continue
  name=$(basename "$d")
  rm -rf "$HOME/.hermes/skills/note-taking/claude-obsidian-$name"
  cp -a "$d" "$HOME/.hermes/skills/note-taking/claude-obsidian-$name"
done
echo "Installed repo: $TARGET"
echo "Vault: $VAULT"
echo "Next: export CLAUDE_OBSIDIAN_VAULT and CLAUDE_OBSIDIAN_PORT, then run bin/co doctor"
