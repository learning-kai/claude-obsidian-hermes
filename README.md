# claude-obsidian-hermes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/learning-kai/claude-obsidian-hermes?display_name=tag)](https://github.com/learning-kai/claude-obsidian-hermes/releases/latest)
[![Hermes](https://img.shields.io/badge/runtime-Hermes%20Agent-blue)](https://hermes-agent.nousresearch.com/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)](https://github.com/learning-kai/claude-obsidian-hermes)
[![Upstream](https://img.shields.io/badge/upstream-claude--obsidian-6f42c1)](https://github.com/AgriciDaniel/claude-obsidian)

> **One sentence:** A Hermes-native port of [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) — keep the second-brain vault workflow (`.raw/` + `wiki/`, skills, retrieve, lint) without Claude Code.

**Languages:** English | [中文文档](README.zh-CN.md)

## Why

[claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) is a strong Claude Code + Obsidian second brain.
Many Hermes users want the same vault architecture without living inside Claude Code. This repo ports the project structure, adapted skills, scripts, and a practical `co` CLI for server-side agent workflows.

## Core Features

- **15 upstream skills** adapted for Hermes (`adapted/skills/`)
- **Upstream vault layout**: immutable `.raw/`, generated `wiki/`, hot/index/log/manifest
- **`bin/co` CLI**: ingest · ingest-url · query · lint · save · fold · mode · doctor · reindex · mirror
- **BM25 retrieve** via `setup-retrieve.sh --no-llm` (no GPU required)
- **Clean vault-template** (no personal notes)
- **Docs**: gap matrix, acceptance notes, optional Obsidian mirror guide

## Screenshots & Demo

This is a CLI/agent toolkit (no GUI app). Typical loop:

```text
co ingest note.md  ->  .raw/ + wiki/sources/  ->  co query "keyword"  ->  co lint/doctor
```

Optional: open the vault in Obsidian to browse `wiki/` pages and wikilinks.

## Quick Start

### One-line bootstrap (macOS / Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/learning-kai/claude-obsidian-hermes/master/scripts/bootstrap.sh | bash
```

### One-line bootstrap (Windows PowerShell)

```powershell
irm https://raw.githubusercontent.com/learning-kai/claude-obsidian-hermes/master/scripts/bootstrap.ps1 | iex
```

### Manual install

```bash
git clone https://github.com/learning-kai/claude-obsidian-hermes.git
cd claude-obsidian-hermes
cp -a vault-template "$HOME/claude-obsidian-vault"
export CLAUDE_OBSIDIAN_VAULT="$HOME/claude-obsidian-vault"
export CLAUDE_OBSIDIAN_PORT="$PWD"

mkdir -p ~/.hermes/skills/note-taking
for d in adapted/skills/*; do
  name=$(basename "$d")
  rm -rf "$HOME/.hermes/skills/note-taking/claude-obsidian-$name"
  cp -a "$d" "$HOME/.hermes/skills/note-taking/claude-obsidian-$name"
done

./bin/co status
./bin/co ingest ./README.md "readme-seed"
./bin/co query "claude-obsidian"
./bin/co doctor
```

In Hermes chat: load skill **`claude-obsidian`** after skills are installed into your profile.

## Engineering Quality

No standard Node/Rust application build is required. Verification is Python/shell hermetic tests + CLI smoke (`co doctor`).

- Hermetic script tests under `adapted/tests/` (wiki-mode, retrieve, bm25, lock)
- Path allowlists for optional Windows Obsidian mirror helpers
- Secret scan / large-file hygiene before publish
- No personal live vault notes in this repository

```bash
cd adapted
python3 tests/test_wiki_mode.py
python3 tests/test_retrieve.py
bash tests/test_wiki_lock.sh
```

There is no Node/Rust application build. Quality evidence is Python/shell hermetic tests + CLI smoke.

## Project Docs

| Doc | Purpose |
|---|---|
| [docs/scope.md](docs/scope.md) | Scope / non-goals |
| [docs/GAP-MATRIX.md](docs/GAP-MATRIX.md) | Parity vs upstream |
| [docs/FINAL-ACCEPTANCE.md](docs/FINAL-ACCEPTANCE.md) | Verification notes |
| [docs/OBSIDIAN-MIRROR.md](docs/OBSIDIAN-MIRROR.md) | Optional Obsidian mirror |
| [docs/SECURITY.md](docs/SECURITY.md) | Path allowlists |

## Privacy & Security

- Do not commit personal vaults, `.env`, or credentials
- Mirror helpers (if used) must target an explicit new-folder allowlist only
- Immutable rule: never rewrite `.raw/**` after ingest
- This repo ships a template vault only

## Release & Updates

- Releases: https://github.com/learning-kai/claude-obsidian-hermes/releases
- Prefer tagged releases for install scripts
- Pull latest `master` or pin a release tag for stability

## Roadmap

- [x] Hermes skill adaptation + `co` CLI
- [x] BM25 retrieve without GPU
- [x] Vault template + docs
- [ ] Optional packaged Hermes skill bundle install story
- [ ] Cleaner URL extraction when `defuddle-cli` is present
- [ ] Optional Ollama rerank/tiling guide for larger hosts

## Contributing

Issues and PRs welcome. Please:
1. Keep personal notes out of PRs
2. Run relevant `adapted/tests/*` when touching scripts
3. Update both README.md and README.zh-CN.md for user-facing changes

## Troubleshooting

| Symptom | Try |
|---|---|
| `co query` misses new pages | `./bin/co reindex` |
| doctor fails missing dirs | re-copy `vault-template` or `./bin/co scaffold` |
| Ollama errors in retrieve | expected without Ollama; BM25 still works |
| Windows mirror fails | check SSH key/host and allowlisted dest folder only |

## License

MIT - see [LICENSE](./LICENSE).

## Attribution

Upstream: [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) (MIT).
See `adapted/LICENSE` and `adapted/ATTRIBUTION.md`.
