"""Build the public lecture and wiki site from authored sources."""
from __future__ import annotations

from html import escape
from pathlib import Path
import hashlib
import re
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
HOME = ROOT / "site" / "index.html"


WIKI_NOTES = {
    "integration.html": ("강의 04 참조", "요청과 결과를 식별자·상태·산출물로 다시 대조하는 방법"),
    "knowledge-context.html": ("강의 03 참조", "무엇을 어디에 남기고, 언제 어떤 지식을 읽는지"),
    "reference/contracts.html": ("강의 01 참조", "요청서와 응답서의 칸, 종결 상태, 공개 범위의 차이"),
    "reference/terms.html": ("용어", "역할·단계·상태 이름을 한 표로 맞춰 읽기"),
    "reference/workflow.html": ("강의 02 참조", "처리 경로, JOB 단계 계약, 승인 기록과 복구 규칙"),
}


def page(title: str, lead: str, cards: list[tuple[str, str, str, str]], depth: int = 1) -> str:
    """Render a lecture/wiki index with the landing page's own style and card grid."""
    prefix = "../" * depth
    style = re.search(r"<style>(.*?)</style>", HOME.read_text(encoding="utf-8"), re.S).group(1)
    style = style.replace('url("assets/', f'url("{prefix}assets/')
    items = "\n".join(
        f'<a class="course" href="{escape(href, quote=True)}"><span class="number">{escape(tag)}</span>'
        f'<h3>{escape(label)}</h3><p>{escape(note)}</p><span class="open">열기 →</span></a>'
        for href, tag, label, note in cards
    )
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{escape(title)} · p-hermes</title><link rel="icon" href="data:,"><style>{style}</style></head><body>'
        f'<header class="top"><a class="brand" href="{prefix}index.html">p-hermes</a><nav aria-label="주 메뉴">'
        f'<a href="{prefix}lectures/index.html">강의</a><a href="{prefix}wiki/index.html">위키</a>'
        '<a href="https://github.com/pheanor-agent/p-hermes-v2">저장소 ↗</a></nav></header>'
        f'<main class="main"><div class="heading"><h2>{escape(title)}</h2><p>{escape(lead)}</p></div>'
        f'<nav class="courses" aria-label="{escape(title)}">{items}</nav></main>'
        f'<footer class="footer"><span>p-hermes · 에이전트 시스템을 이해하는 강의와 참조</span>'
        f'<nav aria-label="홈"><a href="{prefix}index.html">홈으로 →</a></nav></footer></body></html>'
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

    # Indexes reuse the landing page: lecture cards come from its course grid, wiki cards from page headings.
    home = HOME.read_text(encoding="utf-8")
    plain = lambda s: re.sub(r"<[^>]+>", "", s).strip()
    lecture_cards = [
        (href.removeprefix("lectures/"), plain(tag), plain(label), plain(note))
        for href, tag, label, note in re.findall(
            r'<a class="course" href="([^"]+)"><span class="number">(.*?)</span><h3>(.*?)</h3><p>(.*?)</p>', home)
    ]
    wiki_dir = ROOT / "site" / "wiki"
    wiki_cards = []
    for source in sorted(p for p in wiki_dir.rglob("*.html") if p.name != "index.html"):
        rel = source.relative_to(wiki_dir).as_posix()
        heading = re.search(r"<h1[^>]*>(.*?)</h1>", source.read_text(encoding="utf-8"), re.S)
        tag, note = WIKI_NOTES.get(rel, ("위키", ""))
        wiki_cards.append((rel, tag, plain(heading.group(1)) if heading else source.stem, note))
    for directory, title, lead, cards in (
        ("lectures", "강의 목차", "전체 그림에서 시작해 역할, 작업 흐름, 지식, 통합 순서로 읽습니다.", lecture_cards),
        ("wiki", "위키 목차", "강의에서 본 개념의 세부 계약·경로·용어를 찾아봅니다.", wiki_cards),
    ):
        index = OUT / directory / "index.html"
        index.parent.mkdir(parents=True, exist_ok=True)
        index.write_text(page(title, lead, cards), encoding="utf-8", newline="\n")

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
