# HERMES.md — claude-obsidian Hermes Port Schema

Date: 2026-07-17
Upstream: https://github.com/AgriciDaniel/claude-obsidian

## Architecture
```
vault/
├── .raw/
├── wiki/   # sources entities concepts domains comparisons questions meta canvases folds
├── _templates/
├── scripts/
└── HERMES.md
```

## Rules
1. Never modify `.raw/**` after store
2. Obsidian-flavored markdown + YAML frontmatter + [[wikilinks]]
3. Ingest updates pages + index + log + hot + manifest
4. Default transport: filesystem on this vault

## Env
```bash
export CLAUDE_OBSIDIAN_VAULT=/path/to/vault
export CLAUDE_OBSIDIAN_PORT=/path/to/claude-obsidian-hermes
```
