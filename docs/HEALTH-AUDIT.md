# Health Audit & Optimization Report

Date: 2026-07-17

## First principles

| Layer | Question | Result |
|---|---|---|
| Correctness | Do core ops work? | Skills 17, doctor ok, lint 0 issues, retrieve works |
| Completeness | Missing product pieces? | No P0/P1 blockers; Ollama optional only |
| Integrity | Index/manifest/pages consistent? | Index rebuilt from disk; manifest raw files present |
| Operability | Can user run without chat? | `co` CLI + doctor/reindex |
| Safety | Personal Obsidian? | Untouched |

## Findings before fix

1. **Lint noise**: empty `wiki/*/ _index.md` stubs (4 warns)
2. **Index drift**: top-level `wiki/index.md` lagged new sources (health/parity/inbox)
3. **Retrieve staleness**: new pages not searchable until manual reindex (`health` → 0 hits)
4. **Ops gap**: no first-class `doctor` / `reindex` commands
5. **Non-issue**: `ollama unreachable` is expected without Ollama (BM25 still works)
6. **Non-issue**: Claude hooks marketplace not applicable on Hermes

## Fixes applied

| Fix | Detail |
|---|---|
| Fill `_index.md` | sources/entities/concepts/domains listings |
| Rebuild `wiki/index.md` | from actual pages on disk |
| Auto-reindex on `co ingest` | best-effort `setup-retrieve.sh --no-llm` |
| `co reindex` | manual full rebuild |
| `co doctor` | structural health JSON |
| Rebuilt BM25 | 20 pages indexed |
| hot/log updated | audit trail |

## Re-verify

```json
{
  "doctor_ok": true,
  "lint_issues": 0,
  "query_health_has_hits": true,
  "skills": 17,
  "has_reindex": true,
  "has_doctor_cmd": true,
  "ingest_auto_reindex": true,
  "index_has_health": true,
  "index_has_parity": true
}
```

Doctor: `{'vault': '/home/admin/claude-obsidian-vault', 'skills': 17, 'issues': [], 'error': 0, 'warn': 0, 'ok': True}`

## Remaining optional optimizations (not blockers)

1. Install Ollama + nomic-embed-text if you want cosine rerank / semantic tiling
2. Install defuddle-cli if you want prettier URL extraction than HTML fallback
3. Optional Obsidian new-folder mirror (needs your re-authorization)
4. Periodic `co doctor` via cron (weekly) — optional
5. Richer agent synthesis on ingest (currently stub source pages; agent still expands concepts)

## Verdict

**Functional health: PASS.**  
Worth-optimizing items that were real (index drift / reindex / lint stubs / doctor) are done.
Product is ready for daily use via skill `claude-obsidian` or `co`.
