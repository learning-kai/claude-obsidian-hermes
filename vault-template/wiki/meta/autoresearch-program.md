---
type: meta
title: autoresearch program (Hermes guards)
---

# autoresearch guards (P1)

Before running autoresearch on Hermes:

1. **Confirm topic** with user intent (or explicit prior instruction).
2. **Depth cap**: default max 3 search rounds, max 5 sources filed.
3. **No personal Obsidian writes**.
4. **Egress**: only public web; no secrets in prompts.
5. **Stop** if vault disk / rate limits fail.
6. Always update index/log/hot + manifest for each source.
7. Prefer filesystem transport.

This file is the guardrail contract for `claude-obsidian-autoresearch`.
