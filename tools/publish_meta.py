"""Add share/search metadata to published pages and write sitemap.xml and robots.txt."""
from __future__ import annotations

from html import escape, unescape
from pathlib import Path
import re

BASE = "https://pheanor-agent.github.io/p-hermes-v2/"
IMAGE = BASE + "assets/og.png"
SITE_NAME = "p-hermes"
FALLBACK = "에이전트, 작업 흐름, 지식의 세 층으로 p-hermes를 이해하는 한국어 강의와 위키입니다."
NOT_INDEXED = {"404.html"}


def is_redirect(text: str) -> bool:
    return 'http-equiv="refresh"' in text


def url_for(rel: str) -> str:
    return BASE + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)


def tags(rel: str, text: str) -> str:
    """Return the head tags a page should carry; the authored home writes the same set by hand."""
    title = re.search(r"<title>(.*?)</title>", text, re.S)
    title = unescape(title.group(1).strip()) if title else SITE_NAME
    desc = re.search(r'<meta name="description" content="([^"]*)"', text)
    desc = unescape(desc.group(1)) if desc else FALLBACK
    out = []
    if 'name="description"' not in text:
        out.append(f'<meta name="description" content="{escape(desc)}">')
    if 'rel="canonical"' not in text and rel not in NOT_INDEXED:
        out.append(f'<link rel="canonical" href="{url_for(rel)}">')
    out += [
        '<link rel="icon" href="' + BASE + 'assets/favicon.svg" type="image/svg+xml">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        '<meta property="og:locale" content="ko_KR">',
        f'<meta property="og:title" content="{escape(title)}">',
        f'<meta property="og:description" content="{escape(desc)}">',
        f'<meta property="og:url" content="{url_for(rel)}">',
        f'<meta property="og:image" content="{IMAGE}">',
        '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]
    return "".join(out)


def apply(out: Path) -> list[str]:
    """Inject metadata into pages that lack it and return the indexable page list."""
    indexed = []
    for path in sorted(out.rglob("*.html")):
        rel = path.relative_to(out).as_posix()
        text = path.read_text(encoding="utf-8")
        if is_redirect(text):
            continue
        if 'property="og:title"' not in text:
            text = re.sub(r'<link rel="icon" href="data:,">', "", text)
            text = text.replace("</head>", tags(rel, text) + "</head>", 1)
            path.write_text(text, encoding="utf-8", newline="\n")
        if rel not in NOT_INDEXED:
            indexed.append(rel)
    urls = "".join(f"<url><loc>{url_for(rel)}</loc></url>" for rel in indexed)
    (out / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n',
        encoding="utf-8", newline="\n")
    (out / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n",
                                    encoding="utf-8", newline="\n")
    return indexed
