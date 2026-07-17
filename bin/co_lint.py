#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from datetime import date
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    args = ap.parse_args()
    vault = Path(args.vault)
    pages = []
    for d in ["sources", "entities", "concepts", "domains", "comparisons", "questions", "meta", "folds"]:
        p = vault / "wiki" / d
        if p.exists():
            pages += [x for x in p.rglob("*.md") if x.is_file()]
    known = set()
    for p in pages:
        known.add(p.stem)
        t = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"^#\s+(.+)$", t, re.M)
        if m:
            known.add(m.group(1).strip())
    issues = []
    for p in pages:
        t = p.read_text(encoding="utf-8", errors="ignore")
        if p.stat().st_size < 30:
            issues.append({"level": "warn", "code": "empty_page", "path": str(p.relative_to(vault))})
        for m in WIKILINK.finditer(t):
            name = m.group(1).strip()
            if name.startswith(".") or name.startswith("wiki/"):
                continue
            exists = any((vault / "wiki" / sub / f"{name}.md").exists() for sub in ["sources", "entities", "concepts", "questions", "comparisons", "meta", "folds"])
            if name not in known and not exists:
                issues.append({"level": "warn", "code": "broken_wikilink", "path": str(p.relative_to(vault)), "link": name})
    man = vault / ".raw" / ".manifest.json"
    if man.exists():
        try:
            m = json.loads(man.read_text(encoding="utf-8"))
            for k in (m.get("sources") or {}):
                if not (vault / k).exists():
                    issues.append({"level": "error", "code": "manifest_missing", "path": k})
        except Exception as e:
            issues.append({"level": "error", "code": "manifest_invalid", "detail": str(e)})
    today = date.today().isoformat()
    report = vault / "wiki" / "meta" / f"lint-report-{today}.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "---", "type: meta", f'title: "Lint Report {today}"', f"created: {today}", "tags: [meta, lint]", "---", "",
        f"# Lint Report: {today}", "", "## Summary", f"- Pages scanned: {len(pages)}", f"- Issues found: {len(issues)}", "",
    ]
    if not issues:
        lines += ["## Issues", "- none"]
    else:
        lines.append("## Issues")
        for i in issues:
            lines.append(f"- `{i.get('level')}` {i.get('code')} {i.get('path','')} {i.get('link','')}")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"pages": len(pages), "issues": len(issues), "report": str(report.relative_to(vault))}, ensure_ascii=False))

if __name__ == "__main__":
    main()
