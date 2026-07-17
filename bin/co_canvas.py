#!/usr/bin/env python3
import argparse, json
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    args = ap.parse_args()
    vault = Path(args.vault)
    p = vault / "wiki" / "canvases" / "main.canvas"
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_text(json.dumps({"nodes": [{"id": "t", "type": "text", "x": 0, "y": 0, "width": 300, "height": 60, "text": "# Wiki Canvas"}], "edges": []}, indent=2), encoding="utf-8")
    json.loads(p.read_text(encoding="utf-8"))
    print(p)

if __name__ == "__main__":
    main()
