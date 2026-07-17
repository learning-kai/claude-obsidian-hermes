#!/usr/bin/env python3
"""URL -> clean markdown. Prefer defuddle-cli; else improved stdlib extractor."""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


class ReadableExtractor(HTMLParser):
    SKIP = {
        "script",
        "style",
        "nav",
        "footer",
        "header",
        "noscript",
        "aside",
        "form",
        "svg",
        "iframe",
        "button",
    }
    BLOCK = {"p", "div", "section", "article", "li", "ul", "ol", "br", "tr", "table", "blockquote", "pre"}
    HEAD = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}

    def __init__(self, base_url: str = ""):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.parts: list[str] = []
        self.skip = 0
        self.in_a = False
        self.a_href = ""
        self.a_text: list[str] = []
        self.title = ""
        self.in_title = False
        self.in_pre = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "title":
            self.in_title = True
        if tag == "pre" or tag == "code":
            self.in_pre = True
        if tag in self.HEAD:
            self.parts.append("\n\n" + self.HEAD[tag] + " ")
        elif tag == "li":
            self.parts.append("\n- ")
        elif tag == "br":
            self.parts.append("\n")
        elif tag in self.BLOCK:
            self.parts.append("\n\n")
        elif tag == "a":
            self.in_a = True
            self.a_href = attrs_d.get("href", "")
            self.a_text = []

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip:
            self.skip -= 1
            return
        if self.skip:
            return
        if tag == "title":
            self.in_title = False
        if tag in {"pre", "code"}:
            self.in_pre = False
        if tag == "a" and self.in_a:
            text = "".join(self.a_text).strip() or self.a_href
            href = urljoin(self.base_url, self.a_href) if self.a_href else ""
            if href and not href.startswith("javascript:"):
                self.parts.append(f"[{text}]({href})")
            else:
                self.parts.append(text)
            self.in_a = False
            self.a_href = ""
            self.a_text = []
        if tag in self.HEAD or tag in {"p", "div", "section", "article", "li", "blockquote"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if self.skip:
            return
        if self.in_title:
            self.title += data
            return
        if self.in_a:
            self.a_text.append(data)
            return
        if self.in_pre:
            self.parts.append(data)
            return
        t = data.strip()
        if t:
            self.parts.append(t + " ")


def strip_boilerplate(md: str) -> str:
    lines = []
    bad_pat = re.compile(
        r"^(cookie|accept all|sign in|log in|subscribe|newsletter|share this|related articles|advertisement)\b",
        re.I,
    )
    for ln in md.splitlines():
        s = ln.strip()
        if not s:
            lines.append("")
            continue
        if bad_pat.search(s) and len(s) < 80:
            continue
        lines.append(ln)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fallback(url: str) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; HermesCODefuddle/1.0)",
            "Accept": "text/html,application/xhtml+xml",
        },
    )
    raw = urlopen(req, timeout=30).read()
    # charset
    m = re.search(br"charset=([a-zA-Z0-9_\-]+)", raw[:2000], re.I)
    enc = m.group(1).decode("ascii", "ignore") if m else "utf-8"
    try:
        text = raw.decode(enc, errors="ignore")
    except Exception:
        text = raw.decode("utf-8", errors="ignore")

    # prefer <article> content if present
    am = re.search(r"<article\b[\s\S]*?</article>", text, re.I)
    chunk = am.group(0) if am else text
    # drop obvious chrome blocks
    chunk = re.sub(r"<nav\b[\s\S]*?</nav>", " ", chunk, flags=re.I)
    chunk = re.sub(r"<footer\b[\s\S]*?</footer>", " ", chunk, flags=re.I)
    chunk = re.sub(r"<header\b[\s\S]*?</header>", " ", chunk, flags=re.I)

    parser = ReadableExtractor(base_url=url)
    parser.feed(chunk)
    title = html.unescape(parser.title.strip()) if parser.title.strip() else urlparse(url).netloc
    body = strip_boilerplate("".join(parser.parts))
    if len(body) < 80:
        # last resort: all text
        parser2 = ReadableExtractor(base_url=url)
        parser2.feed(text)
        body = strip_boilerplate("".join(parser2.parts))
        if parser2.title.strip():
            title = html.unescape(parser2.title.strip())
    return f"---\nsource_url: {url}\nfetched: auto\nextractor: stdlib-readable\n---\n\n# {title}\n\n{body}\n"


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: co_defuddle.py <url> [--save path]")
    url = sys.argv[1]
    save_path = None
    if len(sys.argv) >= 4 and sys.argv[2] == "--save":
        save_path = sys.argv[3]
    out = None
    if shutil.which("defuddle"):
        cp = subprocess.run(["defuddle", url], capture_output=True, text=True)
        if cp.returncode == 0 and cp.stdout.strip():
            out = cp.stdout
    if out is None:
        out = fallback(url)
    if save_path:
        Path = __import__("pathlib").Path
        Path(save_path).write_text(out, encoding="utf-8")
        print(save_path)
    else:
        print(out)


if __name__ == "__main__":
    main()
