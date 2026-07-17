# SECURITY

Date: 2026-07-17

## Allow write
- `/home/admin/claude-obsidian-hermes/**`
- `/home/admin/claude-obsidian-vault/**`
- `~/.hermes/skills/note-taking/claude-obsidian*/**`

## Deny by default
- `D:\Documents\obsidian/**` and any personal Obsidian vault notes
- `.obsidian` plugin config of personal vaults
- Unrelated mutation of `/home/admin/kaoyan-intel/**` (ledger stays separate)
- Mutating `.raw/**` after ingest (immutable sources)

## Env
```bash
export CLAUDE_OBSIDIAN_VAULT=/home/admin/claude-obsidian-vault
export CLAUDE_OBSIDIAN_PORT=/home/admin/claude-obsidian-hermes
```

## Obsidian mirror (authorized)
- Allow write on Windows ONLY: `D:\Documents\obsidian\claude-obsidian-vault`
- Deny: `考研`, `日记`, `大三下`, `.obsidian`, other siblings
- Source: `/home/admin/claude-obsidian-vault`
- Sync: `bash /home/admin/claude-obsidian-hermes/bin/sync_obsidian_mirror.sh` or `co mirror`
- Updated: 2026-07-17
