#!/usr/bin/env python3
import argparse, sys
from pathlib import Path
from datetime import date

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--title", default="session-note")
    args = ap.parse_args()
    vault = Path(args.vault)
    today = date.today().isoformat()
    body = sys.stdin.read() if not sys.stdin.isatty() else f"Saved session note on {today}."
    slug = args.title.replace(" ", "-")[:80]
    page = vault / "wiki" / "questions" / f"{today}-{slug}.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(
        "\n".join([
            "---", "type: question", f'title: "{args.title}"', f"created: {today}", f"updated: {today}",
            "tags: [question, saved]", "---", "", f"# {args.title}", "", body, "",
        ]),
        encoding="utf-8",
    )
    idx = vault / "wiki" / "index.md"
    if idx.exists():
        it = idx.read_text(encoding="utf-8")
        if slug not in it and "## Questions" in it:
            idx.write_text(it.replace("## Questions\n", f"## Questions\n- [[{today}-{slug}]] — saved note\n", 1), encoding="utf-8")
    log = vault / "wiki" / "log.md"
    log.write_text(log.read_text(encoding="utf-8") + f"\n## {today}\n- save: `{page.relative_to(vault)}`\n", encoding="utf-8")
    print(page)

if __name__ == "__main__":
    main()
