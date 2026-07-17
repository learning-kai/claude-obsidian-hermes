# Improvements applied

Date: 2026-07-17

## Done
1. **Richer ingest synthesis**
   - summary / outline / keywords
   - auto concept seeds (quality-gated)
   - auto reindex after ingest
2. **Better URL clean**
   - improved stdlib readable extractor
   - `co ingest-url`
3. **Weekly doctor cron**
   - job: claude-obsidian 每周健康检查 (`30 9 * * 1`)
   - silent when healthy
4. **Ollama**
   - NOT installed (1.6G RAM / Hermes cgroup)
   - documented in `docs/OLLAMA-STATUS.md`
5. **Ops**
   - `co doctor`, `co reindex` retained

## Verify commands
```bash
co doctor
co lint
co ingest ./note.md
co query "关键词"
```
