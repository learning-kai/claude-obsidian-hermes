#!/usr/bin/env python3
"""Ingest local file into claude-obsidian vault with extractive synthesis."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from co_reindex_lib import reindex  # type: ignore


def slug(s: str) -> str:
    s = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "", s).strip()
    return re.sub(r"\s+", "-", s)[:80] or "source"


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode("utf-8", errors="ignore")


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2]
    return text


def extract_summary(text: str, max_chars: int = 600) -> str:
    text = strip_frontmatter(text)
    text = re.sub(r"```[\s\S]*?```", " ", text)
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    usable = []
    for p in paras:
        line = re.sub(r"^#+\s*", "", p)
        line = re.sub(r"\s+", " ", line).strip()
        if len(line) < 40:
            continue
        if line.startswith("|") and line.count("|") > 2:
            continue
        usable.append(line)
        if sum(len(x) for x in usable) >= max_chars:
            break
    if not usable:
        for ln in text.splitlines():
            ln = ln.strip()
            if len(ln) >= 20 and not ln.startswith("#"):
                usable.append(ln)
            if sum(len(x) for x in usable) >= max_chars:
                break
    out = " ".join(usable)
    return (out[:max_chars].rstrip() + ("…" if len(out) > max_chars else "")) or "_No extractable prose summary._"


def extract_headings(text: str, limit: int = 12) -> list[str]:
    heads = []
    for m in re.finditer(r"^(#{1,3})\s+(.+)$", text, re.M):
        h = re.sub(r"[#*`]+", "", m.group(2)).strip()
        if h and h not in heads:
            heads.append(h)
        if len(heads) >= limit:
            break
    return heads


BOOST = [
    "信号与系统", "抽样定理", "傅里叶变换", "傅里叶分析", "拉普拉斯", "奥本海姆", "周巧娣",
    "杭电", "电子信息", "线性代数", "概率论", "复试", "初试", "大纲", "LTI", "843", "845",
]


def extract_keywords(text: str, limit: int = 8) -> list[str]:
    text_l = text.lower()
    stop_en = {
        "the","and","for","with","this","that","from","are","was","were","have","has","not","but",
        "you","your","into","about","type","title","created","updated","tags","status","source",
        "summary","notes","http","https","com","www","use","used","using","auto","page","file",
        "domain","example","learn","more","need","permission","avoid","operations","documentation",
        "examples","without","needing","markdown",
    }
    stop_zh = {
        "我们","你们","他们","以及","如果","因为","所以","但是","然后","可以","进行","通过","一个",
        "没有","不是","已经","还是","或者","这个","那个","先按","不当","为主","为辅","相关","方向",
        "本文","整理","以下","上述","包括","其中","同时","目前","之后","之前","建议","要点","内容",
        "复习","考试","范围","关系","专业课","备考","线索",
    }
    counts: dict[str, float] = {}

    for w in re.findall(r"[a-z][a-z0-9\-]{2,}", text_l):
        if w in stop_en:
            continue
        counts[w] = counts.get(w, 0) + 1.0

    # numbers like 843/845
    for w in re.findall(r"\b\d{3,4}\b", text):
        counts[w] = counts.get(w, 0) + 2.0

    for m in re.finditer(r"^#{1,3}\s+(.+)$", text, re.M):
        h = re.sub(r"[#*`\[\]()（）]", "", m.group(1)).strip()
        for run in re.findall(r"[\u4e00-\u9fffA-Za-z0-9]{2,24}", h):
            if run in stop_zh or run.lower() in stop_en:
                continue
            counts[run] = counts.get(run, 0) + 3.5

    for run in re.findall(r"[\u4e00-\u9fff]{3,16}", text):
        if run in stop_zh:
            continue
        counts[run] = counts.get(run, 0) + 1.3
        for n in (5, 4, 3):
            if len(run) < n:
                continue
            for i in range(0, len(run) - n + 1, n):  # non-overlapping windows reduce noise
                g = run[i:i+n]
                if g in stop_zh:
                    continue
                counts[g] = counts.get(g, 0) + (0.7 if n >= 4 else 0.4)

    for b in BOOST:
        if b.lower() in text_l or b in text:
            counts[b] = counts.get(b, 0) + 6.0

    ranked = sorted(counts.items(), key=lambda x: (-x[1], -len(x[0]), x[0]))
    out: list[str] = []
    for w, score in ranked:
        if score < 1.5:
            continue
        wl = w.lower()
        if wl in stop_en or w in stop_zh:
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]{1,2}", w) and w not in {"杭电", "复试", "初试"}:
            continue
        if re.fullmatch(r"[a-z]{1,3}", wl):
            continue
        if any(w != y and w in y for y in out):
            continue
        out.append(w)
        if len(out) >= limit:
            break
    return out


def ensure_index_bullet(vault: Path, section: str, page_name: str, note: str) -> None:
    idx = vault / "wiki" / "index.md"
    if not idx.exists():
        return
    it = idx.read_text(encoding="utf-8")
    header = f"## {section}\n"
    if header not in it or f"[[{page_name}]]" in it:
        return
    idx.write_text(it.replace(header, header + f"- [[{page_name}]] — {note}\n", 1), encoding="utf-8")


def rebuild_section_index(vault: Path, sub: str, title: str) -> None:
    folder = vault / "wiki" / sub
    folder.mkdir(parents=True, exist_ok=True)
    pages = sorted([x.stem for x in folder.glob("*.md") if x.name != "_index.md"])
    today = date.today().isoformat()
    lines = [
        "---", "type: meta", f'title: "{title} Index"', f"updated: {today}", "tags: [meta, index]", "---", "",
        f"# {title} Index", "",
    ]
    if pages:
        lines.append("## Pages")
        for n in pages:
            lines.append(f"- [[{n}]]")
    else:
        lines.append("_No pages yet._")
    lines.append("")
    (folder / "_index.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", required=True)
    ap.add_argument("--source", required=True)
    ap.add_argument("--title", default="")
    ap.add_argument("--no-reindex", action="store_true")
    args = ap.parse_args()

    vault = Path(args.vault).resolve()
    src = Path(args.source).expanduser().resolve()
    if not src.is_file():
        raise SystemExit(f"not a file: {src}")

    title = args.title or src.stem
    today = date.today().isoformat()
    data = src.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    text = read_text(src)

    raw_name = f"{today}-{slug(title)}-{h[:10]}{src.suffix or '.md'}"
    raw = vault / ".raw" / raw_name
    raw.parent.mkdir(parents=True, exist_ok=True)
    if not raw.exists():
        shutil.copy2(src, raw)

    summary = extract_summary(text)
    headings = extract_headings(text)
    keywords = extract_keywords(text)

    page_rel = f"wiki/sources/{slug(title)}.md"
    page = vault / page_rel
    page.parent.mkdir(parents=True, exist_ok=True)

    # concept seeds with quality gate
    concept_pages: list[str] = []
    concepts_dir = vault / "wiki" / "concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    for kw in keywords:
        if re.fullmatch(r"[a-z0-9\-]{1,3}", kw.lower()):
            continue
        if re.fullmatch(r"[\u4e00-\u9fff]{1,2}", kw) and kw not in {"杭电", "复试", "初试"}:
            continue
        if len(kw) < 3 and not re.search(r"[A-Za-z0-9]", kw):
            continue
        cslug = slug(kw)
        if not cslug or cslug.lower() in {"type","title","markdown","http","https","example","domain","auto","use"}:
            continue
        cpath = concepts_dir / f"{cslug}.md"
        if cpath.exists():
            ct = cpath.read_text(encoding="utf-8", errors="ignore")
            if slug(title) not in ct:
                cpath.write_text(ct.rstrip() + f"\n\n## Mentions\n- Seen in [[{slug(title)}]] ({today})\n", encoding="utf-8")
            concept_pages.append(f"wiki/concepts/{cslug}.md")
        else:
            cpath.write_text(
                "\n".join([
                    "---", "type: concept", f'title: "{kw}"', f"created: {today}", f"updated: {today}",
                    "tags: [concept, auto]", "status: seed", "---", "", f"# {kw}", "",
                    "## Definition", f"_Auto-seeded from source [[{slug(title)}]]. Expand later._", "",
                    "## Why it appeared", summary[:240], "",
                    "## Sources", f"- [[{slug(title)}]]", "",
                    "## Links", "- [[claude-obsidian-hermes-port]]", "",
                ]),
                encoding="utf-8",
            )
            concept_pages.append(f"wiki/concepts/{cslug}.md")
            ensure_index_bullet(vault, "Concepts", cslug, f"auto from {slug(title)}")
        if len(concept_pages) >= 3:
            break

    head_block = "\n".join(f"- {h}" for h in headings[:10]) or "- _none detected_"
    kw_block = ", ".join(keywords) if keywords else "_none_"
    concept_links = "\n".join(f"- [[{Path(p).stem}]]" for p in concept_pages) or "- _none_"

    page.write_text(
        "\n".join([
            "---", "type: source", f'title: "{title}"', f"created: {today}", f"updated: {today}",
            "tags: [source]", "status: developing", f"sha256_16: {h[:16]}", "---", "",
            f"# {title}", "", "## Summary", summary, "", "## Outline", head_block, "",
            "## Keywords", kw_block, "", "## Related concepts", concept_links, "",
            "## Raw", f"`.raw/{raw_name}`", f"- original: `{src}`", "",
            "## Notes", "_Machine synthesis is extractive. Agent may deepen entities/claims next._", "",
        ]),
        encoding="utf-8",
    )

    man_path = vault / ".raw" / ".manifest.json"
    man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.exists() else {"version": 1, "sources": {}, "address_map": {}}
    man.setdefault("sources", {})
    man.setdefault("address_map", {})
    key = f".raw/{raw_name}"
    man["sources"][key] = {
        "hash": h[:16],
        "ingested_at": today,
        "pages_created": [page_rel] + concept_pages,
        "pages_updated": ["wiki/index.md", "wiki/log.md", "wiki/hot.md"],
        "original": str(src),
        "keywords": keywords,
    }
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")

    ensure_index_bullet(vault, "Sources", slug(title), f"ingested {today}")
    rebuild_section_index(vault, "sources", "Sources")
    rebuild_section_index(vault, "concepts", "Concepts")

    log = vault / "wiki" / "log.md"
    prev = log.read_text(encoding="utf-8") if log.exists() else "# Wiki Log\n"
    log.write_text(prev + f"\n## {today}\n- ingest: `{key}` title={title} concepts={len(concept_pages)} keywords={keywords[:5]}\n", encoding="utf-8")

    (vault / "wiki" / "hot.md").write_text(
        "\n".join([
            "---", "type: meta", "title: Hot Cache", f"updated: {today}", "---", "",
            "# Recent Context", "", "## Last Updated", f"{today}. Ingested [[{slug(title)}]].", "",
            "## Key Recent Facts", f"- Source: [[{slug(title)}]]", f"- Summary: {summary[:180]}",
            f"- Keywords: {', '.join(keywords[:6]) if keywords else 'n/a'}", "",
            "## Recent Changes", f"- Created/updated source page and {len(concept_pages)} concept seed(s)", "",
            "## Active Threads", "- Expand auto-seeded concepts if important", "",
        ]),
        encoding="utf-8",
    )

    reidx = {"ok": False, "skipped": True}
    if not args.no_reindex:
        try:
            reidx = reindex(vault)
        except Exception as e:
            reidx = {"ok": False, "error": str(e)}

    print(json.dumps({
        "ok": True,
        "raw": key,
        "page": page_rel,
        "concepts": concept_pages,
        "keywords": keywords,
        "reindexed": reidx,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
