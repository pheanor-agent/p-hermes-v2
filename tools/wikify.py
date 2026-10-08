"""Give every wiki page the same reference-document layout.

Adds the shared wiki stylesheet, anchors for each section heading, and a
section table of contents so wiki pages read as lookup documents rather than
slides.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

TAG_RE = re.compile(r"<[^>]+>")


def slug(text: str, used: set[str]) -> str:
    base = re.sub(r"[^\w가-힣]+", "-", text.strip().lower()).strip("-") or "section"
    name, n = base, 2
    while name in used:
        name, n = f"{base}-{n}", n + 1
    used.add(name)
    return name


def namespace_svg_ids(page: str) -> str:
    """Keep inline wiki diagrams independent when they share marker names."""
    index = 0
    def replace_svg(match: re.Match) -> str:
        nonlocal index
        index += 1
        svg = match.group(0)
        for ident in set(re.findall(r'\bid="([^"]+)"', svg)):
            new = f'wiki-svg-{index}-{ident}'
            svg = svg.replace(f'id="{ident}"', f'id="{new}"')
            svg = svg.replace(f'url(#{ident})', f'url(#{new})')
            svg = svg.replace(f'href="#{ident}"', f'href="#{new}"')
        return svg
    return re.sub(r'<svg\b.*?</svg>', replace_svg, page, flags=re.S)


def transform(page: str, depth: int) -> str:
    page = namespace_svg_ids(page)
    prefix = "../" * depth
    if "wiki.css" not in page:
        page = page.replace("</head>", f'<link rel="stylesheet" href="{prefix}assets/wiki.css"></head>', 1)
    page = re.sub(r"<body([^>]*)>", lambda m: f'<body{m.group(1)} class="wiki-doc">' if "class=" not in m.group(1) else m.group(0), page, count=1)

    used: set[str] = set()
    toc = []

    def anchor(m: re.Match) -> str:
        attrs, inner = m.group(1), m.group(2)
        label = " ".join(html.unescape(TAG_RE.sub("", inner)).split())
        existing = re.search(r'id="([^"]+)"', attrs)
        ident = existing.group(1) if existing else slug(label, used)
        toc.append((ident, label))
        if existing:
            return m.group(0)
        return f'<h2{attrs} id="{ident}">{inner}</h2>'

    page = re.sub(r"<h2([^>]*)>(.*?)</h2>", anchor, page, flags=re.S)
    if len(toc) >= 3 and 'class="wiki-toc"' not in page:
        items = "".join(f'<li><a href="#{i}">{html.escape(t)}</a></li>' for i, t in toc)
        nav = f'<nav class="wiki-toc" aria-label="이 문서의 목차"><p>목차</p><ol>{items}</ol></nav>'
        page = re.sub(r"(<main[^>]*>)", r'\1<div class="wiki-layout">' + nav.replace("\\", "\\\\") + '<article class="wiki-body">', page, count=1)
        page = page.replace("</main>", "</article></div></main>", 1)
    else:
        page = re.sub(r"(<main[^>]*>)", r'\1<div class="wiki-layout wiki-single"><article class="wiki-body">', page, count=1)
        page = page.replace("</main>", "</article></div></main>", 1)
    return page


def build(wiki_dir: Path) -> list[Path]:
    written = []
    for path in sorted(wiki_dir.rglob("*.html")):
        if path == wiki_dir / "index.html":
            continue  # the wiki index shares the landing page style (build_site.page)
        depth = len(path.relative_to(wiki_dir.parent).parts) - 1
        path.write_text(transform(path.read_text(encoding="utf-8"), depth), encoding="utf-8", newline="\n")
        written.append(path)
    return written


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for p in build(root / "docs/wiki"):
        print(p)
