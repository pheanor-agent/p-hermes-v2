"""Build the isolated pilot preview under docs/preview using only stdlib."""
from __future__ import annotations

from html import escape
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "preview"
OUT = ROOT / "docs" / "preview"

ALLOWED = {
    "site/lectures/01-orchestrator-worker.html",
    "site/vendor/reveal/reveal.css",
    "site/vendor/reveal/reveal.js",
    "site/vendor/reveal/LICENSE",
    "content/articles/why-file-handoffs.md",
    "content/reference/contracts.md",
    "content/tutorials/portable-worker.md",
    "publication/claude-code-mapping.md",
    "reference/__init__.py",
    "reference/filesystem_transport.py",
    "reference/orchestrator.py",
    "reference/worker.py",
    "examples/inputs/brief.txt",
    "examples/request.json",
    "tests/test_contracts.py",
}

CSS = """*{box-sizing:border-box}body{margin:0;background:#f7f8fa;color:#17212b;font:16px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif}header,main,footer{max-width:920px;margin:auto;padding:1.25rem}header{border-bottom:1px solid #d7dee8}header a,footer a{color:#315c8c}main{padding-top:2rem;padding-bottom:4rem}h1,h2,h3{line-height:1.25;color:#12233a}h1{font-size:clamp(2rem,5vw,3.25rem)}h2{margin-top:2.25rem}a{color:#145ca8}a:focus-visible{outline:3px solid #efb544;outline-offset:3px}nav ul{padding-left:1.25rem}.card{padding:1rem 1.2rem;margin:1rem 0;border:1px solid #d7dee8;border-radius:12px;background:white}.muted{color:#536273}pre{overflow:auto;padding:1rem;background:#101a27;color:#e9f0fa;border-radius:10px;font:14px/1.55 ui-monospace,SFMono-Regular,monospace}code{font-family:ui-monospace,SFMono-Regular,monospace}p code,li code,td code{background:#e9edf3;padding:.1em .3em;border-radius:4px}table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}th,td{border:1px solid #ccd5e0;text-align:left;vertical-align:top;padding:.55rem .7rem}th{background:#edf2f7}footer{border-top:1px solid #d7dee8;color:#536273;font-size:.9rem}.tag{font-size:.85rem;border:1px solid #b9c6d5;border-radius:99px;padding:.2rem .65rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem}.grid .card{margin:.25rem 0}.download{font-size:.9rem} @media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation:none!important;transition:none!important}}"""


def inline(text: str) -> str:
    s = escape(text, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: safe_link(m.group(2), m.group(1)), s)
    return s


def safe_link(href: str, label: str) -> str:
    u = urlsplit(href)
    if u.scheme.lower() in {"javascript", "data", "file"}:
        raise ValueError("unsafe markdown link")
    return f'<a href="{escape(href, quote=True)}">{label}</a>'


def render_markdown(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    paragraph: list[str] = []
    list_kind: str | None = None
    table: list[str] = []
    code: list[str] | None = None

    def flush_paragraph() -> None:
        if paragraph:
            out.append("<p>" + inline(" ".join(x.strip() for x in paragraph)) + "</p>")
            paragraph.clear()

    def flush_list() -> None:
        nonlocal list_kind
        if list_kind:
            out.append(f"</{list_kind}>")
            list_kind = None

    def flush_table() -> None:
        if not table:
            return
        rows = [[cell.strip() for cell in row.strip().strip("|").split("|")] for row in table]
        rows = [row for row in rows if not all(re.fullmatch(r":?-{3,}:?", c) for c in row)]
        if rows:
            out.append("<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in rows[0]) + "</tr></thead><tbody>")
            for row in rows[1:]:
                out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>")
            out.append("</tbody></table>")
        table.clear()

    for line in lines:
        if code is not None:
            if line.startswith("```"):
                out.append("<pre><code>" + escape("\n".join(code)) + "</code></pre>")
                code = None
            else:
                code.append(line)
            continue
        if line.startswith("```"):
            flush_paragraph(); flush_list(); flush_table(); code = []; continue
        if line.lstrip().startswith("|"):
            flush_paragraph(); flush_list(); table.append(line); continue
        flush_table()
        if not line.strip():
            flush_paragraph(); flush_list(); continue
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            flush_paragraph(); flush_list()
            level = len(m.group(1)); title = inline(m.group(2).strip())
            out.append(f"<h{level}>{title}</h{level}>"); continue
        m = re.match(r"^\s*[-*+]\s+(.+)$", line)
        ordered = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if m or ordered:
            flush_paragraph()
            kind = "ul" if m else "ol"
            if list_kind != kind:
                flush_list(); out.append(f"<{kind}>"); list_kind = kind
            out.append("<li>" + inline((m or ordered).group(1)) + "</li>"); continue
        flush_list(); paragraph.append(line)
    flush_paragraph(); flush_list(); flush_table()
    if code is not None:
        out.append("<pre><code>" + escape("\n".join(code)) + "</code></pre>")
    return "\n".join(out)


def page(title: str, body: str, depth: int = 0) -> str:
    base = "../" * depth
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="p-hermes 재정비 파일럿 미리보기"><title>{escape(title)}</title><link rel="stylesheet" href="{base}assets/preview.css"></head><body><header><a href="{base}index.html">p-hermes 파일럿 미리보기</a></header><main>{body}</main><footer>사용자 리뷰용 파일럿 미리보기 · <a href="{base}index.html">처음으로</a></footer></body></html>'''


def main() -> int:
    if not SOURCE.is_dir():
        raise SystemExit("preview source directory missing")
    actual = {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_file()}
    if actual != ALLOWED:
        raise SystemExit(f"preview allowlist mismatch: expected={len(ALLOWED)} actual={len(actual)}")
    for rel in actual:
        p = SOURCE / rel
        if p.is_symlink() or not p.resolve().is_relative_to(SOURCE.resolve()):
            raise SystemExit("preview source path escapes allowlist")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "assets").mkdir()
    (OUT / "assets/preview.css").write_text(CSS + "\n", encoding="utf-8")

    # Keep the teaching slide and local vendor assets together; no CDN dependency.
    lecture_out = OUT / "lectures/01-orchestrator-worker.html"
    lecture_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / "site/lectures/01-orchestrator-worker.html", lecture_out)
    for name in ("reveal.css", "reveal.js", "LICENSE"):
        dest = OUT / "vendor/reveal" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / "site/vendor/reveal" / name, dest)

    docs = [
        ("content/articles/why-file-handoffs.md", "articles/why-file-handoffs.html", "해설 · 왜 파일로 일을 맡길까요", "목표와 시도를 구분하고, 결과를 읽을 수 있는 합의로 남기는 이유를 설명합니다."),
        ("content/reference/contracts.md", "reference/contracts.html", "위키 · 파일 handoff 계약", "요청·응답 필드와 상태, 경계 조건을 빠르게 찾아봅니다."),
        ("content/tutorials/portable-worker.md", "tutorials/portable-worker.html", "실습 · portable worker 실행", "임시 폴더와 합성 입력으로 요청부터 terminal 응답까지 따라 합니다."),
        ("publication/claude-code-mapping.md", "publication/claude-code-mapping.html", "환경 대응표 · Claude Code / Codex / Python", "확인된 사례와 아직 제안인 적용 지점을 구분합니다."),
    ]
    cards = [
        ("강의", "lectures/01-orchestrator-worker.html", "오케스트레이터와 워커의 역할·파일 handoff를 장면과 함께 봅니다."),
        ("해설", "articles/why-file-handoffs.html", "파일 handoff가 시도 구분과 결과 확인에 주는 이점을 읽습니다."),
        ("위키", "reference/contracts.html", "portable 교육 킷의 요청·응답 계약과 실패 경계를 찾아봅니다."),
        ("실습", "tutorials/portable-worker.html", "합성 fixture로 worker와 검증 테스트를 실행하는 방법을 따라 합니다."),
        ("환경 대응표", "publication/claude-code-mapping.html", "Claude Code 사례, Codex 미검증 제안, generic Python 예시를 구분합니다."),
        ("코드", "code/index.html", "참조 모듈·예제·테스트를 읽고 개별 원본 파일을 내려받습니다."),
    ]
    for source, target, title, desc in docs:
        src = SOURCE / source
        body = f'<p class="muted">{escape(desc)}</p><p><a href="../index.html">← 미리보기 목차</a></p>' + render_markdown(src.read_text(encoding="utf-8"))
        dest = OUT / target; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(title, body, target.count("/")), encoding="utf-8", newline="\n")

    body = '<p class="tag">사용자 리뷰용</p><h1>p-hermes 재정비 파일럿 미리보기(리뷰용)</h1><p class="muted">요청에서 허용된 상위 에이전트·워커 파일럿 자료만 모았습니다. 기존 사이트 콘텐츠는 이 경로에서 대체하지 않습니다.</p><div class="grid">'
    body += "".join(f'<section class="card"><h2><a href="{href}">{label}</a></h2><p>{desc}</p></section>' for label, href, desc in cards)
    body += '</div><h2>코드로 확인하기</h2><p>코드 페이지는 HTML escape를 적용한 보기 화면과 원본 다운로드 링크를 함께 제공합니다. 예제는 합성 입력이며 실서비스 연동은 하지 않습니다.</p>'
    (OUT / "index.html").write_text(page("p-hermes 재정비 파일럿 미리보기(리뷰용)", body), encoding="utf-8", newline="\n")

    items = sorted(p for p in SOURCE.rglob("*") if p.is_file() and p.relative_to(SOURCE).as_posix().startswith(("reference/", "examples/", "tests/")))
    rows = []
    for src in items:
        rel = src.relative_to(SOURCE)
        public_rel = Path("downloads") / rel
        html_rel = Path("code") / Path(str(rel) + ".html")
        target = OUT / public_rel; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        code = escape(src.read_text(encoding="utf-8"))
        title = rel.as_posix()
        base = "../" * html_rel.as_posix().count("/")
        links = f'<p class="download"><a href="{base}{public_rel.as_posix()}">원본 파일 다운로드: {escape(title)}</a></p>'
        code_body = f'<p><a href="{base}index.html">← 미리보기</a> · <a href="{base}code/index.html">코드 목록</a></p><h1>{escape(title)}</h1>{links}<pre><code>{code}</code></pre>'
        dest = OUT / html_rel; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(page(title, code_body, html_rel.as_posix().count("/")), encoding="utf-8", newline="\n")
        rows.append(f'<li><a href="{html_rel.as_posix().removeprefix("code/")}">{escape(title)}</a> · <a href="../{public_rel.as_posix()}">download</a></li>')
    code_body = '<p><a href="../index.html">← 미리보기 목차</a></p><h1>코드·예제·테스트</h1><p>화면은 HTML escape를 적용한 보기용입니다. 다운로드 파일도 같은 allowlist에서 생성됩니다.</p><ul>' + "".join(rows) + "</ul>"
    (OUT / "code/index.html").write_text(page("코드·예제·테스트", code_body, 1), encoding="utf-8", newline="\n")
    print(f"built preview: {len(ALLOWED)} source files, {len(items)} code files -> docs/preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
