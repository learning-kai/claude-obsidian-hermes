# migration-map

Date: 2026-07-17
Upstream: https://github.com/AgriciDaniel/claude-obsidian

## Skills (15)

| Upstream | Priority | Hermes name | Disposition |
|---|---|---|---|
| wiki | P0 | claude-obsidian-wiki | adapt+install |
| wiki-ingest | P0 | claude-obsidian-wiki-ingest | adapt+install |
| wiki-query | P0 | claude-obsidian-wiki-query | adapt+install |
| wiki-lint | P0 | claude-obsidian-wiki-lint | adapt+install |
| save | P0 | claude-obsidian-save | adapt+install |
| wiki-cli | P0 | claude-obsidian-wiki-cli | adapt (filesystem primary) |
| obsidian-markdown | P0 | claude-obsidian-obsidian-markdown | adapt+install |
| wiki-retrieve | P1 | claude-obsidian-wiki-retrieve | adapt+install; feature-detect |
| wiki-fold | P1 | claude-obsidian-wiki-fold | adapt+install |
| wiki-mode | P1 | claude-obsidian-wiki-mode | adapt+install |
| defuddle | P1 | claude-obsidian-defuddle | adapt; CLI optional |
| canvas | P1/P2 | claude-obsidian-canvas | adapt+install |
| autoresearch | P1/P2 | claude-obsidian-autoresearch | adapt+install; needs guards |
| think | P1 | claude-obsidian-think | adapt+install |
| obsidian-bases | P1 | claude-obsidian-obsidian-bases | adapt+install |

## Other assets

| Asset | Disposition |
|---|---|
| scripts/* | P0 copy into vault/port; smoke mode/lock/transport |
| bin/* | P0 copy; setup-vault adapted for Hermes paths |
| _templates/* | P0 copy to vault |
| agents/* | P0 keep as Hermes subagent prompt packs |
| WIKI.md / AGENTS.md | P0 keep + HERMES.md schema |
| .claude-plugin / .cursor / .windsurf | drop from runtime |
| hooks/* | document only; no Claude PostToolUse |
| sample wiki/* | optional seed; not required |

## Tool mapping (Claude → Hermes)

| Claude Code | Hermes |
|---|---|
| Read | `read_file` |
| Write | `write_file` |
| Edit | `patch` |
| Glob / Grep | `search_files` |
| Bash | `terminal` |
| WebFetch / WebSearch | `web_search` / HTTP via tools |

Default transport: **filesystem** against `$CLAUDE_OBSIDIAN_VAULT`.
obsidian-cli / MCP: optional only.
