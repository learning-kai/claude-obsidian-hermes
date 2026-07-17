# Ollama / vector rerank status

Date: 2026-07-17

## Decision
**Not installed on this host.**

## Why
- Host RAM ~1.6G with Hermes cgroup MemoryMax=1G
- Memory notes forbid heavy concurrent local model stacks with Hermes
- BM25 retrieve already works without Ollama

## What you still have without Ollama
- `co query` / `retrieve.py` BM25 ranking
- noop rerank (order = BM25)
- semantic tiling remains gated (`dragonscale.mechanisms.semantic_tiling=false`)

## If later hardware allows
```bash
# only on a machine with spare RAM/GPU
curl -fsSL https://ollama.com/install.sh | sh
ollama pull nomic-embed-text
# then rerank/tiling can be enabled
```

Do **not** force-install on this VPS for now.
