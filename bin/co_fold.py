#!/usr/bin/env python3
import argparse, re, hashlib
from pathlib import Path
from datetime import date

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    args = ap.parse_args()
    vault = Path(args.vault)
    text = (vault / "wiki" / "log.md").read_text(encoding="utf-8")
    entries = []
    cur = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})\s*$", line)
        if m:
            if cur:
                entries.append((cur, "\n".join(buf).strip()))
            cur = m.group(1)
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur:
        entries.append((cur, "\n".join(buf).strip()))
    k = 1 if len(entries) >= 2 else 0
    n = 2 ** k
    batch = entries[-n:] if entries else []
    fold_id = hashlib.sha1("|".join(f"{d}:{b[:40]}" for d, b in batch).encode()).hexdigest()[:12]
    today = date.today().isoformat()
    d0 = batch[0][0] if batch else today
    d1 = batch[-1][0] if batch else today
    path = vault / "wiki" / "folds" / f"fold-k{k}-from-{d0}-to-{d1}-n{len(batch)}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    themes = []
    for d, b in batch:
        first = next((ln.strip("- ").strip() for ln in b.splitlines() if ln.strip()), "(empty)")
        themes.append(f"- [{d}] {first[:160]}")
    path.write_text(
        "\n".join([
            "---", "type: fold", f'title: "Fold k={k} {d0}→{d1}"', f"created: {today}",
            f"batch_exponent: {k}", f"fold_id: {fold_id}", "---", "",
            f"# Fold k={k}: {d0} → {d1}", "", "## Extractive themes", *(themes or ["- none"]),
            "", "## Rule", "Extractive only. Children unchanged.", "",
        ]),
        encoding="utf-8",
    )
    print(path)

if __name__ == "__main__":
    main()
