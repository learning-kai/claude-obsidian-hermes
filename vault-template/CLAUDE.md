# HERMES.md — claude-obsidian Hermes Port Schema

Date: 2026-07-17
Upstream: https://github.com/AgriciDaniel/claude-obsidian
Port: /home/admin/claude-obsidian-hermes
Vault: /home/admin/claude-obsidian-vault

You operate the claude-obsidian knowledge companion on Hermes Agent.

## Architecture
```
vault/
├── .raw/          # immutable sources + .manifest.json
├── wiki/          # generated KB
│   ├── index.md, log.md, hot.md, overview.md
│   ├── sources/, entities/, concepts/, domains/
│   ├── comparisons/, questions/, meta/, canvases/, folds/, references/
├── _templates/
├── scripts/
└── HERMES.md
```

## Rules
1. Never modify `.raw/**` after store
2. Obsidian-flavored markdown + YAML frontmatter + [[wikilinks]]
3. Ingest updates pages + index + log + hot + manifest
4. Query: hot → index → pages; cite sources; file good answers
5. Transport default: Hermes filesystem tools on this vault only
6. Do not write personal Obsidian notes unless newly authorized folder

## Routing
Use skill `claude-obsidian` route table to subskills `claude-obsidian-<name>`.
