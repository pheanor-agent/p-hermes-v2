"""Build the public lecture and wiki site from authored sources."""
from __future__ import annotations

from html import escape
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
HOME = ROOT / "site" / "index.html"


def page(title: str, links: list[tuple[str, str]], depth: int = 1) -> str:
    items = "\n".join(
        f'<li><a href="{escape(href, quote=True)}">{escape(label)}</a></li>'
        for href, label in links
    )
    prefix = "../" * depth
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{escape(title)}</title><link rel="stylesheet" href="{prefix}assets/design-system.css">'
        '</head><body><header class="topbar"><a href="'
        f'{prefix}index.html">p-hermes</a></header><main><section class="hero">'
        f'<h1>{escape(title)}</h1><nav aria-label="목차"><ul>{items}</ul></nav>'
        '</section></main></body></html>'
    )


def build() -> None:
    """Build and validate a candidate before replacing the published tree."""
    global OUT
    if not HOME.is_file():
        raise FileNotFoundError(f"authored landing page missing: {HOME}")
    authored_home = HOME.read_bytes()
    prior_out = OUT
    with tempfile.TemporaryDirectory(prefix=".docs-build-", dir=ROOT) as work:
        work_path = Path(work)
        candidate = work_path / "docs"
        OUT = candidate
        try:
            _build()
            if (candidate / "index.html").read_bytes() != authored_home:
                raise RuntimeError("generated landing page differs from current authored source")
            env = os.environ.copy()
            env["DOCS_PATH"] = str(candidate)
            result = subprocess.run(
                [sys.executable, "-B", str(ROOT / "tools" / "check_site.py")],
                cwd=ROOT, env=env, text=True, capture_output=True,
            )
            if result.returncode:
                raise RuntimeError("candidate site validation failed:\n" + result.stdout + result.stderr)
            old = work_path / "old-docs"
            if prior_out.exists():
                os.replace(prior_out, old)
            try:
                os.replace(candidate, prior_out)
            except Exception:
                if old.exists() and not prior_out.exists():
                    os.replace(old, prior_out)
                raise
        finally:
            OUT = prior_out
    print(f"Built public site: {OUT}")


def _build() -> None:
    """Populate OUT from the authored site, then compile lecture/wiki indexes."""
    OUT.mkdir(parents=True)
    shutil.copytree(ROOT / "site", OUT, dirs_exist_ok=True, copy_function=shutil.copy2)

    # Keep the deployment surface focused; implementation material stays in GitHub.
    for name in ("articles", "code", "downloads", "examples", "vendor"):
        shutil.rmtree(OUT / name, ignore_errors=True)
    for name in ("examples", "environment"):
        shutil.rmtree(OUT / "wiki" / name, ignore_errors=True)

    for directory, title in (("lectures", "강의 목차"), ("wiki", "위키 목차")):
        source_dir = ROOT / "site" / directory
        files = sorted(p for p in source_dir.rglob("*.html") if p.name != "index.html")
        links: list[tuple[str, str]] = []
        if directory == "lectures":
            sys.path.insert(0, str(ROOT / "tools"))
            import deckify
            links = [(filename, f"{number} · {name}") for filename, number, name in deckify.LECTURES]
        else:
            import re
            for source in files:
                text = source.read_text(encoding="utf-8")
                heading = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
                label = re.sub(r"<[^>]+>", "", heading.group(1)).strip() if heading else source.stem
                links.append((source.relative_to(source_dir).as_posix(), label))
        index = OUT / directory / "index.html"
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(page(title, links), encoding="utf-8", newline="\n")

    sys.path.insert(0, str(ROOT / "tools"))
    import deckify
    deckify.build(ROOT / "site" / "lectures", OUT / "lectures")
    import wikify
    wikify.build(OUT / "wiki")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    actual = hashlib.sha256((OUT / "index.html").read_bytes()).hexdigest()
    source = hashlib.sha256(HOME.read_bytes()).hexdigest()
    if actual != source:
        raise RuntimeError(f"landing page verification failed: {actual} != {source}")


if __name__ == "__main__":
    build()
