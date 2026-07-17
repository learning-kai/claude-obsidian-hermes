# Scope: claude-obsidian project port to Hermes

Date: 2026-07-17

## Goal
Port **AgriciDaniel/claude-obsidian** as a runnable project on Hermes Agent — not a thin llm-wiki wrapper.

## Is
- Full upstream skill tree (15 skills) adapted for Hermes
- Upstream vault architecture: `.raw/` + `wiki/` + hot.md + manifest
- Scripts, templates, agents prompts, setup helpers
- Filesystem transport default

## Is not
- Claude Code marketplace plugin runtime (`.claude-plugin`)
- Writing Kai's personal Obsidian notes by default
- Merging kaoyan-intel execution ledger into the wiki
- Claiming 100% DragonScale/remote embedding parity in P0

## Relation to wiki-hermes
`wiki-hermes` = historical thin shell. **Not** the deliverable of this port.
This port's deliverable lives under:
- `/home/admin/claude-obsidian-hermes`
- `/home/admin/claude-obsidian-vault`
- `~/.hermes/skills/note-taking/claude-obsidian*`

## Phases
- **P0**: M0–M6 + docs — runnable upstream workflow on Hermes
- **P1**: retrieve/fold/mode/defuddle hardening
- **P2**: canvas depth, autoresearch guards, optional Obsidian new-folder mirror
