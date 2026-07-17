# Obsidian mirror

## Destination (allowlisted only)
`D:\Documents\obsidian\claude-obsidian-vault`

## Source
`/home/admin/claude-obsidian-vault`

## Safety
- One-way: server -> Obsidian new folder
- Never writes: `考研`, `日记`, `大三下`, `.obsidian`, or other siblings
- Excludes heavy caches: `.vault-meta/chunks`, `.vault-meta/bm25`, locks

## Manual sync
```bash
bash /home/admin/claude-obsidian-hermes/bin/sync_obsidian_mirror.sh
```

## Notes for Kai
- Open this folder inside your existing vault (it is a subfolder)
- Or open it as a separate vault if you prefer isolation
- Lecture notes stay in `考研/` etc., untouched
