#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--port", required=True)
    args = ap.parse_args()
    vault = Path(args.vault)
    port = Path(args.port)
    skills = list(Path.home().joinpath(".hermes/skills/note-taking").glob("claude-obsidian*"))
    def load(p):
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
    out = {
        "vault": str(vault),
        "port": str(port),
        "skills": len(skills),
        "bm25": (vault / ".vault-meta/bm25/index.json").exists(),
        "chunks": (vault / ".vault-meta/chunks").exists() and any((vault / ".vault-meta/chunks").iterdir()),
        "transport": load(vault / ".vault-meta/transport.json"),
        "mode": (load(vault / ".vault-meta/mode.json") or {}).get("mode"),
        "dragonscale": load(vault / ".vault-meta/dragonscale.json"),
        "wiki_pages": sum(1 for _ in (vault / "wiki").rglob("*.md")),
        "address_counter": (vault / ".vault-meta/address-counter.txt").read_text(encoding="utf-8").strip() if (vault / ".vault-meta/address-counter.txt").exists() else None,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
