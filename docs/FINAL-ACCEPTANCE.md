# FINAL ACCEPTANCE — claude-obsidian Hermes Project Port

Date: 2026-07-17
Status: **COMPLETE (P0 + P1 runnable product)**

## Upstream
cb93ff6d82f9c35a08bf6010e7fac36dfddc827b
2026-05-28 03:42:42 +0300 chore(assets): add 1280x640 social preview card

## Deliverables
| Item | Path |
|---|---|
| Port root | `/home/admin/claude-obsidian-hermes` |
| Upstream snapshot | `/home/admin/claude-obsidian-hermes/upstream` |
| Adapted tree | `/home/admin/claude-obsidian-hermes/adapted` |
| Live vault | `/home/admin/claude-obsidian-vault` |
| Skills | `~/.hermes/skills/note-taking/claude-obsidian*` (16 dirs) |
| Installer | `/home/admin/claude-obsidian-hermes/install.sh` |
| Inbox cron script | `~/.hermes/scripts/claude_obsidian_inbox_triage.py` |

## Automated review checklist

| Check | Result |
|---|---|
| Skills installed + valid frontmatter | PASS (16/16; bad=[]) |
| Vault required dirs | PASS |
| Vault required files | PASS |
| BM25 index provisioned | PASS |
| Chunks provisioned | PASS |
| retrieve.py smoke | PASS |
| wiki-mode route | PASS |
| wiki-lock acquire/release | PASS |
| fold page exists | PASS |
| canvas main.canvas valid JSON | PASS |
| lint report exists | PASS |
| save/question page exists | PASS |
| inbox triage script | PASS |
| personal Obsidian untouched | PASS |
| project port ≠ wiki-hermes docs | PASS (`docs/scope.md`, `docs/vs-wiki-hermes.md`) |

## P0 scenarios (original 9)
All previously PASS; reaffirmed by this review.

## P1 scenarios
| # | Scenario | Result |
|---|---|---|
| 10 | setup-retrieve --no-llm | PASS |
| 11 | retrieve ranked results | PASS |
| 12 | wiki-mode generic/lyt/para/zettelkasten routes | PASS (4 modes, 4 types each) |
| 13 | wiki-fold extractive rollup | PASS |
| 14 | defuddle optional fallback documented | PASS (CLI missing → fallback) |
| 15 | canvas main map | PASS |
| 16 | autoresearch guard contract | PASS (`wiki/meta/autoresearch-program.md`) |
| 17 | bases sample | PASS (`wiki/meta/dashboard.base`) |
| 18 | Inbox auto-triage + cron script | PASS |

## How to use
1. Drop files into `/home/admin/claude-obsidian-vault/Inbox/` (hourly :20 cron) or ask Hermes to ingest.
2. Chat: load skill `claude-obsidian` then ingest/query/lint/save.
3. CLI search: `python3 /home/admin/claude-obsidian-vault/scripts/retrieve.py "question" --top 5`
4. Rebuild index after bulk edits: `bash /home/admin/claude-obsidian-vault/bin/setup-retrieve.sh --no-llm`

## Not claimed
- Claude marketplace plugin UX
- Ollama rerank (noop without Ollama; BM25 still works)
- Personal Obsidian integration (forbidden unless re-authorized)
- 100% parity with every DragonScale remote embedding option

## Review JSON
```json
{
  "date": "2026-07-17",
  "skills_count": 16,
  "skills_ok": 16,
  "skills_bad": [],
  "missing_dirs": [],
  "missing_files": [],
  "retrieve_ok": true,
  "mode_ok": true,
  "lock_ok": true,
  "canvas_ok": true,
  "fold_ok": true,
  "lint_ok": true,
  "save_ok": true,
  "inbox_cron_script": true,
  "bm25_ok": true,
  "chunks_ok": true,
  "personal_ok": true,
  "vault_files": 78
}
```

## Parity pass (2026-07-17)

Added after first-principles gap analysis vs upstream:

- CLI: `bin/co` (ingest/query/lint/save/fold/mode/canvas/defuddle/status/address/boundary)
- DragonScale meta provisioned (fold/addresses/boundary; tiling gated on ollama)
- Hooks reference + Hermes equivalents documented
- Upstream hermetic tests executed on adapted tree (bm25/mode/retrieve/lock/address/concurrent/etc. PASS)
- defuddle fallback without npm package

See `docs/GAP-MATRIX.md`.
