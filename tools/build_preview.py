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
    "site/lectures/00-overview.html",
    "site/lectures/01-orchestrator-worker.html",
    "site/lectures/02-workflow.html",
    "site/lectures/04-image-pipeline.html",
    "site/lectures/05-integration.html",
    "site/assets/design-system.css",
    "site/vendor/reveal/reveal.css",
    "site/vendor/reveal/reveal.js",
    "site/vendor/reveal/LICENSE",
    "site/assets/illustrations/goal-attempt.svg",
    "site/assets/illustrations/context.svg",
    "site/assets/illustrations/handoff.svg",
    "site/assets/illustrations/verification.svg",
    "site/assets/illustrations/forgetting.webp",
    "site/assets/illustrations/handoff.webp",
    "site/assets/illustrations/verify.webp",
    "site/assets/illustrations/workflow.webp",
    "site/assets/illustrations/knowledge.webp",
    "site/assets/illustrations/image-pipeline.webp",
    "site/wiki/integration.html",
    "site/examples/integration-check/README.html",
    "site/examples/integration-check/PROMPT.html",
    "examples/integration-check/README.md",
    "examples/integration-check/AGENTS.md",
    "examples/integration-check/PROMPT.md",
    "examples/integration-check/src/__init__.py",
    "examples/integration-check/src/__main__.py",
    "examples/integration-check/src/integration_check.py",
    "examples/integration-check/fixtures/pass/request.json",
    "examples/integration-check/fixtures/pass/contract.json",
    "examples/integration-check/fixtures/pass/context.json",
    "examples/integration-check/fixtures/pass/catalog.json",
    "examples/integration-check/fixtures/missing/request.json",
    "examples/integration-check/fixtures/missing/contract.json",
    "examples/integration-check/fixtures/missing/context.json",
    "examples/integration-check/fixtures/missing/catalog.json",
    "examples/integration-check/tests/test_integration_check.py",
    "site/assets/illustrations/prompts.md",
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
    "site/wiki/environment/README.html",
    "site/wiki/reference/contracts.html",
    "site/wiki/reference/workflow.html",
    "site/wiki/reference/terms.html",
    "site/wiki/examples/README.html",
    "site/wiki/image-pipeline.html",
    "site/articles/why-file-handoffs.html",
    "site/examples/portable-worker/README.html",
    "site/examples/portable-worker/PROMPT.html",
    "examples/image-pipeline/README.md",
    "examples/image-pipeline/PROMPT.md",
    "examples/image-pipeline/task.md",
    "examples/image-pipeline/pyproject.toml",
    "examples/image-pipeline/fixtures/catalog.json",
    "examples/image-pipeline/fixtures/request.json",
    "examples/image-pipeline/fixtures/expected.json",
    "examples/image-pipeline/src/image_pipeline_demo/__init__.py",
    "examples/image-pipeline/src/image_pipeline_demo/__main__.py",
    "examples/image-pipeline/src/image_pipeline_demo/pipeline.py",
    "examples/image-pipeline/tests/test_pipeline.py",

    "site/code/examples/portable-worker/src/__init__.py.html",
    "site/code/examples/portable-worker/src/filesystem_transport.py.html",
    "site/code/examples/portable-worker/src/orchestrator.py.html",
    "site/code/examples/portable-worker/src/worker.py.html",
    "site/code/examples/portable-worker/tests/test_contracts.py.html",
    "site/downloads/examples/portable-worker/src/__init__.py",
    "site/downloads/examples/portable-worker/src/filesystem_transport.py",
    "site/downloads/examples/portable-worker/src/orchestrator.py",
    "site/downloads/examples/portable-worker/src/worker.py",
    "site/downloads/examples/portable-worker/tests/test_contracts.py",
    "site/assets/publish-design-system.css",
}

CSS = """*{box-sizing:border-box}body{margin:0;background:#f7f8fa;color:#17212b;font:16px/1.7 system-ui,-apple-system,"Segoe UI",sans-serif}header,main,footer{max-width:920px;margin:auto;padding:1.25rem}header{border-bottom:1px solid #d7dee8}header a,footer a{color:#315c8c}main{padding-top:2rem;padding-bottom:4rem}h1,h2,h3{line-height:1.25;color:#12233a;text-wrap:pretty;word-break:keep-all}h1{font-size:clamp(2rem,5vw,3.25rem)}h2{margin-top:2.25rem}a{color:#145ca8}a:focus-visible{outline:3px solid #efb544;outline-offset:3px}nav ul{padding-left:1.25rem}.card{padding:1rem 1.2rem;margin:1rem 0;border:1px solid #d7dee8;border-radius:12px;background:white}.muted{color:#536273}pre{overflow:auto;padding:1rem;background:#101a27;color:#e9f0fa;border-radius:10px;font:14px/1.55 ui-monospace,SFMono-Regular,monospace}code{font-family:ui-monospace,SFMono-Regular,monospace}p code,li code,td code{background:#e9edf3;padding:.1em .3em;border-radius:4px}table{border-collapse:collapse;width:100%;display:block;overflow-x:auto}th,td{border:1px solid #ccd5e0;text-align:left;vertical-align:top;padding:.55rem .7rem}th{background:#edf2f7}footer{border-top:1px solid #d7dee8;color:#536273;font-size:.9rem}.tag{font-size:.85rem;border:1px solid #b9c6d5;border-radius:99px;padding:.2rem .65rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:1rem}.grid .card{margin:.25rem 0}.download{font-size:.9rem} @media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;animation:none!important;transition:none!important}}"""
CSS += """\nbody{word-break:keep-all;line-break:strict}p,li,td{overflow-wrap:normal}pre,code{word-break:normal;overflow-wrap:normal}pre{max-width:100%}.grid{gap:1.25rem}.card{margin:1rem 0;padding:1.25rem}h1,h2,h3{text-wrap:balance}@media(max-width:760px){body{font-size:17px}header,main,footer{padding-left:1rem;padding-right:1rem}.grid{grid-template-columns:1fr}}@media(max-width:360px){body{font-size:16px}h1{font-size:2rem}}"""


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
    theme = '<style>body{background:#101824;color:#edf2fa}header,main,footer{border-color:#43536a}header{background:#101824;color:#b7c3d3}header a,footer a,a{color:#9bc2ff}h1,h2,h3{color:#edf2fa}.card{background:#192536;border-color:#43536a}.muted,footer{color:#b7c3d3}th{background:#253449}th,td{border-color:#43536a}</style>'
    return f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="p-hermes 재정비 파일럿 미리보기"><title>{escape(title)}</title><link rel="stylesheet" href="{base}assets/preview.css">{theme}</head><body><header><a href="{base}index.html">p-hermes 파일럿 미리보기</a></header><main>{body}</main><footer>사용자 리뷰용 파일럿 미리보기 · <a href="{base}index.html">처음으로</a></footer></body></html>'''


def prepare_lecture(source: Path, title: str, active: str) -> str:
    html = source.read_text(encoding="utf-8")
    html = html.replace("상위", "지휘")
    html = html.replace("실행 에이전트", "작업 에이전트")
    html = re.sub(r"(?<!\()워커", "작업 에이전트", html)
    html = html.replace("지휘 에이전트는", "지휘 에이전트(오케스트레이터)는", 1)
    html = html.replace("작업 에이전트는", "작업 에이전트(워커)는", 1)
    html = html.replace("read-back", "다시 읽기").replace("terminal 상태", "최종 상태(terminal)")
    html = re.sub(r'<div class="role-flow".*?</div><p class="callout">.*?</p>', '', html, count=1, flags=re.S)
    html = html.replace('<link rel="stylesheet" href="../assets/design-system.css">',
        '<link rel="stylesheet" href="../vendor/reveal/reveal.css"><link rel="stylesheet" href="../assets/design-system.css">')
    html = html.replace('<main id="main">', '<main id="main"><div class="reveal"><div class="slides">', 1)
    html = html.replace('</main>', '</div></div></main>', 1)
    flow = f'''<figure class="overall-flow" aria-label="전체 동작 흐름도. 이번 강의의 초점은 {escape(active)}입니다.">
<svg viewBox="0 0 1200 330" role="img" aria-labelledby="flow-title flow-desc"><title id="flow-title">요청에서 결과 보고까지 전체 동작 흐름</title><desc id="flow-desc">사람의 요청에서 지휘 에이전트, 작업 에이전트, 작업 흐름, 지식 참조, 산출, 검증을 거쳐 결과가 사람에게 돌아옵니다.</desc>
<path class="flow-track" d="M75 164 H1120 M80 230 H1040 C1040 300 80 300 80 218"/><g class="flow-nodes">
<g class="flow-node"><circle cx="80" cy="164" r="48"/><text x="80" y="158">사람의</text><text x="80" y="184">요청</text></g>
<g class="flow-node {'focus' if active == '지휘 에이전트' else ''}"><circle cx="240" cy="164" r="48"/><text x="240" y="158">지휘</text><text x="240" y="184">에이전트</text></g>
<g class="flow-node {'focus' if active == '작업 에이전트' else ''}"><circle cx="400" cy="164" r="48"/><text x="400" y="158">작업</text><text x="400" y="184">에이전트</text></g>
<g class="flow-node"><circle cx="560" cy="164" r="48"/><text x="560" y="158">작업</text><text x="560" y="184">흐름</text></g>
<g class="flow-node"><circle cx="720" cy="164" r="48"/><text x="720" y="158">지식</text><text x="720" y="184">참조</text></g>
<g class="flow-node"><circle cx="880" cy="164" r="48"/><text x="880" y="158">이미지</text><text x="880" y="184">산출</text></g>
<g class="flow-node"><circle cx="1040" cy="164" r="48"/><text x="1040" y="158">검증</text><text x="1040" y="184">보고</text></g></g>
<rect class="request-token" x="0" y="0" width="22" height="22" rx="7"><animateMotion dur="9s" repeatCount="indefinite" path="M80 230 H1040 C1040 300 80 300 80 218"/></rect></svg>
<ol class="flow-mobile"><span class="mobile-flow-track" aria-hidden="true"></span><span class="mobile-request-token" aria-hidden="true"></span><li>사람의 요청</li><li>지휘 에이전트 · 계획하고 요청서 작성</li><li{' aria-current="step"' if active == '작업 에이전트' else ''}>작업 에이전트 · 맡은 범위 수행</li><li>작업 흐름 · 조사 → 계획 → 승인 → 실행 → 검증</li><li>필요한 지식 참조</li><li>산출물 만들기 (예: 이미지)</li><li>실제 산출물 검증</li><li>결과 보고</li><li>사람에게 전달</li></ol>
<figcaption>요청 → 지휘(계획·요청서) → 작업 에이전트 → 조사·계획·승인·실행·검증 → 지식 참조 → 산출(예: 이미지) → 검증·보고 → 사람 · 초점: {escape(active)}</figcaption></figure>'''
    flow = re.sub(r'(<text x="\d+" y=")(135|158)(">)', lambda m: m.group(1) + str(int(m.group(2)) + 3) + m.group(3), flow)
    flow = re.sub(r'(<g class="flow-node(?: focus)?\s*"><)circle cx="(\d+)" cy="(\d+)" r="48"/>', lambda m: m.group(1) + f'rect x="{int(m.group(2))-70}" y="{int(m.group(3))-31}" width="140" height="62" rx="20"/>', flow)
    html = html.replace('<p class="synthetic">', flow + '<p class="synthetic">', 1)
    summary = re.search(r'(<h2>요청과 응답을 연결하고, 마지막에는 사람이 실물을 확인합니다</h2>)', html)
    if summary:
        diagram = '''<figure class="takeaway-diagram" aria-label="요청을 정하고 맡긴 뒤, 사람이 결과를 확인하는 세 단계"><svg viewBox="0 0 900 150" role="img" aria-labelledby="summary-title"><title id="summary-title">정하기, 맡기기, 직접 확인하기</title><path d="M160 75 H740" stroke="#43536a" stroke-width="7"/><g fill="#202f42" stroke="#74e0c0" stroke-width="4"><circle cx="160" cy="75" r="48"/><circle cx="450" cy="75" r="48"/><circle cx="740" cy="75" r="48"/></g><g fill="#edf2fa" text-anchor="middle" font-family="system-ui,sans-serif" font-size="21" font-weight="700"><text x="160" y="82">정하기</text><text x="450" y="82">맡기기</text><text x="740" y="82">직접 확인</text></g></svg><figcaption>목표와 경계 → 실행 → 응답과 산출물 대조</figcaption></figure>'''
        html = html[:summary.end()] + diagram + html[summary.end():]
    for heading, asset, alt in [
        ('언어 모델은 유능하지만', 'context.svg', '대화의 단편은 흩어지고 다음 작업으로 이어지는 요청 카드만 남는 모습'),
        ('세 역할과 두 파일이', 'handoff.svg', '지휘 에이전트와 작업 에이전트가 요청과 결과를 파일로 주고받는 모습'),
        ('목표와 요청 식별자는 서로 다른 것을 가리킵니다', 'goal-attempt.svg', '하나의 목표에서 실패한 시도와 수정한 새 시도가 갈라지는 모습'),
        ('파일을 따라가면 누가 무엇을 했는지 보입니다', 'verification.svg', '완료 보고를 실제 산출물과 대조하는 모습'),
    ]:
        match = re.search(r'(<h2>[^<]*' + re.escape(heading) + r'[^<]*</h2>)', html)
        if match:
            figure = f'<figure class="editorial-illustration"><img src="../assets/illustrations/{asset}" alt="{escape(alt)}"><figcaption>{escape(alt)}</figcaption></figure>'
            html = html[:match.end()] + figure + html[match.end():]
    html = html.replace('<body class="lecture">', '<body class="lecture"><div class="deck-title" aria-hidden="true">' + escape(title) + '</div>', 1)
    html = html.replace('</body>', '<script src="../vendor/reveal/reveal.js"></script><script>Reveal.initialize({hash:true,controls:true,progress:true,center:false,width:"100%",height:"100%",minScale:1,maxScale:1,transition:"slide",keyboard:true,overview:true,scrollActivationWidth:0});</script></body>', 1)
    html = html.replace('</head>', '''<style>
.lecture .topbar{max-width:none;margin:0;padding-left:clamp(1rem,3vw,2.5rem);background:var(--bg);color:var(--muted)}.lecture .footer{background:var(--bg);color:var(--muted)}
.lecture main{max-width:none;padding:0;margin:0}.lecture .reveal{width:100%;height:calc(100vh - 160px);font-size:16px}.lecture .reveal .slides{text-align:left;width:100%!important;height:100%!important;left:0!important;top:0!important;margin:0!important;transform:none!important}.lecture .reveal .slides>section{height:100%;width:100%!important;left:0!important;top:0!important;transform:none!important;display:none!important;overflow-y:auto;padding:clamp(1rem,3vw,2.5rem);text-align:left;background:var(--bg);border-radius:18px;color:var(--ink)}.lecture .reveal .slides>section.present{display:block!important}.lecture .reveal p,.lecture .reveal li,.lecture .reveal small,.lecture .reveal .map-node *,.lecture .reveal .axis-grid article *,.lecture .reveal .role-flow article *,.lecture .reveal .file-box *,.lecture .reveal .flow-label{color:var(--ink)!important}.lecture .reveal .file-box code{white-space:nowrap}.lecture .reveal small{font-size:14px!important}.lecture .reveal h1{font-size:clamp(1.8rem,4vw,3rem)}.lecture .reveal h2{font-size:clamp(1.45rem,3vw,2.1rem)}.lecture .reveal .chapter{border-top:0;padding-top:1.2rem}.lecture .reveal .route-list{counter-reset:route;list-style:none;position:relative;margin:1rem 0;padding:0 0 0 1.8rem}.lecture .reveal .route-list li{counter-increment:route;position:relative;max-width:none;border-left:2px solid var(--line);padding:.2rem 0 1rem 1rem}.lecture .reveal .route-list li::before{content:counter(route);position:absolute;left:-1rem;top:0;width:1.15rem;height:1.15rem;display:grid;place-items:center;border:2px solid var(--mint);border-radius:50%;background:var(--surface);color:var(--ink);font-size:14px;line-height:1}.lecture .reveal .route-list li:last-child{border-left-color:transparent}.lecture .reveal .overall-flow{margin:1.4rem 0 1rem;padding:.6rem;border:1px solid var(--line);border-radius:16px;background:var(--surface)}.overall-flow svg{display:block;width:100%;height:auto;max-height:26vh}.takeaway-diagram{max-width:860px;margin:1rem auto;text-align:center}.takeaway-diagram svg{width:100%;max-height:16vh}.flow-mobile{display:none}.flow-track{stroke:#43536a;stroke-width:7;stroke-linecap:round;fill:none}.flow-node circle,.flow-node rect{fill:#202f42;stroke:#9bc2ff;stroke-width:3}.flow-node text{fill:#edf2fa;text-anchor:middle;font:750 23px system-ui,sans-serif}.flow-node.focus circle,.flow-node.focus rect{fill:#1d4b49;stroke:#74e0c0;stroke-width:7}.request-token{fill:#ffd17d;filter:drop-shadow(0 0 7px #ffd17d)}.overall-flow figcaption{color:var(--muted);font-size:14px;line-height:1.25}.editorial-illustration figcaption{text-align:center;color:var(--muted);font-size:16px}.editorial-illustration{margin:1rem auto;max-width:600px}.editorial-illustration img{display:block;width:100%;max-height:30vh;object-fit:contain;border-radius:18px}.lecture .deck-title{display:none}.lecture .reveal .controls{color:var(--mint)}.lecture .reveal .progress{color:var(--mint)}@media(max-width:700px){.lecture .reveal{height:calc(100dvh - 190px)}.lecture .reveal .slides>section{padding:1rem}.overall-flow svg{display:none}.flow-mobile{display:block;position:relative;list-style:none;margin:.6rem 0;padding:0 0 0 1.4rem}.flow-mobile li{position:relative;margin:.35rem 0;padding:.35rem .55rem;border-left:3px solid var(--blue);background:var(--surface-2);font-size:14px}.flow-mobile>li::before{content:"";position:absolute;left:-1.28rem;top:.72rem;width:.55rem;height:.55rem;border-radius:50%;background:var(--blue)}.flow-mobile>li[aria-current="step"]{background:var(--surface);outline:2px solid var(--mint);font-weight:700}.mobile-flow-track{position:absolute;left:.4rem;top:.4rem;bottom:.4rem;width:2px;background:var(--line)}.mobile-request-token{display:block;position:absolute;z-index:2;left:-.06rem;top:0;width:14px;height:14px;border:2px solid var(--bg);border-radius:4px;background:var(--amber);filter:drop-shadow(0 0 4px var(--amber));pointer-events:none;animation:mobile-flow-route 9s linear infinite}@keyframes mobile-flow-route{0%,2%{top:0}44%{top:calc(100% - 18px)}92%,100%{top:0}}.editorial-illustration img{max-height:24vh}.overall-flow figcaption{display:none}}
@media(prefers-reduced-motion:reduce){.request-token,.mobile-request-token{display:none!important}.lecture .reveal .slides>section{transition:none!important}.lecture .reveal .progress{transition:none!important}}
</style></head>''', 1)
    return html.replace('</head>', '<link rel="icon" href="data:,"></head>', 1)


def prepare_overview(source: Path) -> str:
    """Render lecture 00 as a nine-slide, offline Reveal deck."""
    html = source.read_text(encoding="utf-8")
    start = html.index('<main id="main">')
    end = html.index('</main>', start) + len('</main>')
    flow = '''<figure class="mini-flow" aria-label="요청에서 결과 확인까지 이어지는 전체 동작 흐름"><svg viewBox="0 0 1200 112" role="img"><path d="M65 38H1135" stroke="#43536a" stroke-width="4"/><g font-family="system-ui" font-size="20" font-weight="700" text-anchor="middle"><g><rect x="15" y="18" width="145" height="40" rx="20"/><text x="87" y="44">요청</text></g><g><rect x="180" y="18" width="155" height="40" rx="20"/><text x="257" y="44">지휘</text></g><g><rect x="355" y="18" width="155" height="40" rx="20"/><text x="432" y="44">작업</text></g><g><rect x="530" y="18" width="155" height="40" rx="20"/><text x="607" y="44">흐름</text></g><g><rect x="705" y="18" width="155" height="40" rx="20"/><text x="782" y="44">지식</text></g><g><rect x="880" y="18" width="155" height="40" rx="20"/><text x="957" y="44">산출</text></g><g><rect x="1055" y="18" width="130" height="40" rx="20"/><text x="1120" y="44">검증</text></g></g></svg><ol class="mini-flow-mobile"><li>요청</li><li>지휘</li><li>작업 에이전트</li><li>작업 흐름</li><li>지식 참조</li><li>이미지 산출</li><li>검증·보고</li></ol></figure>'''
    flow_slide = '''<figure class="motion-flow"><svg id="journey" viewBox="0 0 1080 350" role="img" aria-labelledby="journey-title journey-desc"><title id="journey-title">요청 카드가 전체 작업 흐름을 따라 이동합니다</title><desc id="journey-desc">사람의 요청에서 지휘 에이전트, 작업 에이전트, 작업 흐름의 계획·승인·실행·검증, 지식 참조, 이미지 산출, 검증·보고를 거쳐 사람에게 돌아옵니다.</desc><path id="route" d="M70 140 H1010 Q1040 140 1040 170 V250 Q1040 280 1010 280 H70" fill="none" stroke="#43536a" stroke-width="7" stroke-linecap="round"/><g class="journey-node" data-step="0"><circle cx="70" cy="140" r="43"/><text x="70" y="135">사람의</text><text x="70" y="158">요청</text></g><g class="journey-node" data-step="1"><circle cx="250" cy="140" r="43"/><text x="250" y="135">지휘</text><text x="250" y="158">에이전트</text></g><g class="journey-node" data-step="2"><rect x="375" y="112" width="110" height="56" rx="18"/><text x="430" y="137">작업</text><text x="430" y="158">에이전트</text></g><g class="journey-node" data-step="3"><rect x="555" y="112" width="110" height="56" rx="18"/><text x="610" y="137">작업 흐름</text><text x="610" y="158">승인·검증</text></g><g class="journey-node" data-step="4"><rect x="735" y="112" width="110" height="56" rx="18"/><text x="790" y="137">지식</text><text x="790" y="158">참조</text></g><g class="journey-node" data-step="5"><rect x="915" y="112" width="110" height="56" rx="18"/><text x="970" y="137">산출</text><text x="970" y="158">이미지 등</text></g><g class="journey-node" data-step="6"><circle cx="970" cy="280" r="43"/><text x="970" y="275">검증·</text><text x="970" y="298">결과 보고</text></g><g class="journey-node" data-step="7"><circle cx="610" cy="280" r="43"/><text x="610" y="275">사람이</text><text x="610" y="298">확인</text></g><g class="journey-node" data-step="8"><circle cx="250" cy="280" r="43"/><text x="250" y="275">요청 카드</text><text x="250" y="298">돌아옴</text></g><rect id="request-card" x="0" y="0" width="28" height="22" rx="5"><path d="M5 6h18M5 11h18M5 16h12" stroke="#101824" stroke-width="2"/></rect></svg><ol class="mobile-journey"><li data-step="0">사람의 요청 · 목표와 완료 조건</li><li data-step="1">지휘 에이전트 · 계획과 요청서</li><li data-step="2">작업 에이전트 · 맡은 범위 수행</li><li data-step="3">작업 흐름 · 계획·승인·실행</li><li data-step="4">지식 참조 · 필요한 근거</li><li data-step="5">산출 · 예: 이미지</li><li data-step="6">검증 · 산출물 대조</li><li data-step="7">결과 보고 · 사람에게 전달</li><li data-step="8">사람 확인 · 다음 판단</li></ol><figcaption id="caption" aria-live="polite">사람이 목표와 완료 조건을 전합니다.</figcaption><div class="motion-controls"><button id="prev" type="button">이전 단계</button><button id="play" type="button" aria-pressed="false">자동 재생</button><button id="next" type="button">다음 단계</button><span id="step-label">1 / 9</span></div></figure>'''
    flow_slide = re.sub(r'(<g class="journey-node" data-step="[0-9]+"><)circle cx="([0-9]+)" cy="([0-9]+)" r="43"/>', lambda m: m.group(1) + f'rect x="{int(m.group(2))-70}" y="{int(m.group(3))-40}" width="140" height="80" rx="20"/>', flow_slide)
    parts = [
      '<section class="deck-slide cover"><p class="eyebrow">강의 00 · 전체 그림</p><h1>요청이 결과가 되기까지</h1><p class="lead">사람의 의도를 지휘 에이전트와 작업 에이전트가 이어받아, 확인 가능한 결과로 돌려주는 구조입니다.</p>'+flow+'<p>처음 등장: 지휘 에이전트(오케스트레이터) · 작업 에이전트(워커)</p></section>',
      '<section class="deck-slide core"><p class="eyebrow">핵심 흐름 · 단계별로 보기</p><h2>요청 카드는 경로를 따라 움직이고, 현재 단계가 밝혀집니다</h2>'+flow_slide+'<p class="synthetic">모든 예시는 교육용 합성 데이터입니다.</p></section>',
      '<section class="deck-slide"><p class="eyebrow">배경 · 왜 나누는가</p><h2>대화가 이어지는 것과 결과가 맞는 것은 다릅니다</h2><div class="visual-pair"><figure><img src="../assets/illustrations/forgetting.webp" alt="끊어진 대화 맥락을 찾아보는 로봇"><figcaption>맥락이 끊겨도 요청은 남깁니다</figcaption><small>ChatGPT 생성 일러스트</small></figure><figure><img src="../assets/illustrations/verify.webp" alt="완료 보고와 실제 산출물을 대조하는 로봇"><figcaption>보고 뒤에 실제 산출물을 확인합니다</figcaption><small>ChatGPT 생성 일러스트</small></figure></div><p>이어갈 정보는 기록으로, 완료 판단은 결과 확인으로 분리합니다.</p></section>',
      '<section class="deck-slide axis"><p class="eyebrow">축 1 · 지휘와 작업</p><h2>계획을 세우는 역할과 맡은 범위를 수행하는 역할</h2>'+flow+'<figure><img src="../assets/illustrations/handoff.webp" alt="지휘 에이전트와 작업 에이전트 사이에 요청과 결과가 오가는 모습"><figcaption>요청은 맡기고, 결과는 다시 확인합니다.</figcaption><small>ChatGPT 생성 일러스트</small></figure></section>',
      '<section class="deck-slide axis"><p class="eyebrow">축 2 · 작업 흐름</p><h2>계획·승인·실행·검증은 한 요청 안의 서로 다른 단계입니다</h2>'+flow+'<figure><img src="../assets/illustrations/workflow.webp" alt="작업 카드가 계획·승인·실행·검증 단계를 차례로 지나는 모습"><figcaption>요청은 각 단계를 거쳐 확인 가능한 결과가 됩니다.</figcaption><small>ChatGPT 생성 일러스트</small></figure></section>',
      '<section class="deck-slide axis"><p class="eyebrow">축 3 · 지식</p><h2>필요한 근거를 찾아 현재 상태와 대조합니다</h2>'+flow+'<figure><img src="../assets/illustrations/knowledge.webp" alt="자료에서 색인과 검색을 거쳐 필요한 근거를 찾는 모습"><figcaption>원천에서 근거를 찾아 현재 상태와 대조합니다.</figcaption><small>ChatGPT 생성 일러스트</small></figure><p>여기서는 역할만 표시합니다. 실제 지식 경로는 복구된 실물을 확인한 뒤 다룹니다.</p></section>',
      '<section class="deck-slide axis"><p class="eyebrow">축 4 · 이미지 생성</p><h2>요청을 구성하고 결과를 검사하는 파이프라인</h2>'+flow+'<figure><img src="../assets/illustrations/image-pipeline.webp" alt="카탈로그 선택부터 프롬프트 구성과 이미지 생성, 결과 검사까지의 흐름"><figcaption>카탈로그와 프롬프트를 거쳐 이미지를 만들고 검사합니다.</figcaption><small>ChatGPT 생성 일러스트</small></figure></section>',
      '<section class="deck-slide"><p class="eyebrow">하나의 요청 · 네 축 통과</p><h2>요청의 목표는 단계마다 더 구체적인 산출로 바뀝니다</h2>'+flow+'<div class="request-example"><span>합성 요청</span><b>→</b><span>지휘가 범위 정리</span><b>→</b><span>작업 흐름에서 승인</span><b>→</b><span>지식 참조·이미지 산출</span><b>→</b><span>결과 확인</span></div><p>예: 교육용 그림 한 장. 예시는 이 시스템의 작동만 보여주는 합성 상황입니다.</p></section>',
      '<section class="deck-slide"><p class="eyebrow">학습 경로</p><h2>전체에서 시작해 각 축의 질문으로 이동합니다</h2>'+flow+'<div class="learning-map"><span>00 전체 그림</span><b>→</b><span>01 지휘·작업</span><b>→</b><span>02 작업 흐름</span><b>→</b><span>03 지식*</span><b>→</b><span>04 이미지</span><b>→</b><span>05 통합</span></div><p>* 지식 강의는 실제 지식 시스템 복구 확인 뒤 작성합니다.</p></section>'
    ]
    deck = '<main id="main"><div class="reveal"><div class="slides">'+''.join(parts)+'</div></div></main>'
    html = html[:start] + deck + html[end:]
    html = html.replace('</header>', '<nav class="deck-nav" aria-label="슬라이드 이동"><button id="deck-prev" type="button">이전</button><span id="deck-count" aria-live="polite"></span><button id="deck-next" type="button">다음</button></nav></header>', 1)
    html = html.replace('</body>', '''<script>(()=>{const slides=[...document.querySelectorAll('.reveal .slides>section')];let i=0;function show(n){i=(n+slides.length)%slides.length;slides.forEach((s,j)=>{s.classList.toggle('present',i===j);s.hidden=i!==j});document.getElementById('deck-count').textContent=`${i+1} / ${slides.length}`}document.getElementById('deck-prev').onclick=()=>show(i-1);document.getElementById('deck-next').onclick=()=>show(i+1);document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();show(i+1)}else if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();show(i-1)}});show(0)})();
(()=>{const captions=['사람이 목표와 완료 조건을 전합니다.','지휘 에이전트가 계획하고 요청서를 만듭니다.','작업 에이전트가 맡은 범위를 수행합니다.','작업 흐름에서 계획·승인·실행·검증을 거칩니다.','필요한 지식을 찾아 근거를 확인합니다.','산출물을 만듭니다. 예를 들어 이미지가 있습니다.','산출물이 요청을 충족하는지 검증합니다.','결과를 사람에게 보고합니다.','사람이 확인하고 다음 판단을 합니다.'];let i=0,timer=null;const card=document.getElementById('request-card'),route=document.getElementById('route'),nodes=[...document.querySelectorAll('.journey-node,.mobile-journey li')];function set(n){i=(n+captions.length)%captions.length;document.getElementById('caption').textContent=captions[i];document.getElementById('step-label').textContent=(i+1)+' / '+captions.length;nodes.forEach((x,j)=>{x.classList.toggle('active',j%9===i);if(x.tagName==='LI'){if(j%9===i)x.setAttribute('aria-current','step');else x.removeAttribute('aria-current')}});if(matchMedia('(prefers-reduced-motion: reduce)').matches||route.getTotalLength===undefined)return;const p=route.getPointAtLength(route.getTotalLength()*i/(captions.length-1));card.setAttribute('transform',`translate(${p.x-14} ${p.y-65})`)}function stop(){clearInterval(timer);timer=null;document.getElementById('play').setAttribute('aria-pressed','false');document.getElementById('play').textContent='자동 재생'}document.getElementById('prev').onclick=()=>{stop();set(i-1)};document.getElementById('next').onclick=()=>{stop();set(i+1)};document.getElementById('play').onclick=()=>{if(timer){stop();return}document.getElementById('play').setAttribute('aria-pressed','true');document.getElementById('play').textContent='재생 멈춤';timer=setInterval(()=>set(i+1),1800)};document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){stop();set(i+1)}if(e.key==='ArrowLeft'){stop();set(i-1)}});set(0)})();</script><style>
.lecture,.reveal-viewport{background:var(--bg)!important}.lecture .topbar{max-width:none;margin:0;padding-left:clamp(1rem,3vw,2.5rem);background:var(--bg);color:var(--muted)}.lecture .footer{background:var(--bg);color:var(--muted)}.lecture main{max-width:none;padding:0;margin:0}.lecture .reveal{height:calc(100dvh - 130px);width:100%}.lecture .reveal .slides>section{height:100%;overflow:auto;padding:clamp(1rem,3vw,2.4rem);text-align:left;background:var(--bg);color:var(--ink)}.lecture .reveal .slides>section[hidden]{display:none!important}.lecture .reveal .slides>section.present{display:block}.lecture .reveal h1{font-size:clamp(2rem,5vw,3.7rem)}.lecture .reveal h2{font-size:clamp(1.6rem,3.5vw,2.6rem);max-width:27ch}.deck-slide{flex-direction:column;justify-content:center;gap:.35rem}.deck-nav{display:flex;align-items:center;gap:.5rem}.deck-nav button{min-height:38px;border:1px solid var(--line);border-radius:8px;background:var(--surface-2);color:var(--ink)}.deck-slide>p,.deck-slide>figure{max-width:1100px;width:100%;margin:.45rem auto}.mini-flow svg{width:100%;height:auto}.mini-flow rect{fill:#202f42;stroke:#9bc2ff;stroke-width:2}.mini-flow text{fill:#edf2fa}.mini-flow-mobile{display:none}.motion-flow{max-width:1080px!important;margin:.4rem auto!important;padding:.4rem 1rem;border:1px solid var(--line);border-radius:18px;background:var(--surface)}.motion-flow svg{width:100%;height:auto;max-height:42vh}.mobile-journey{display:none}.journey-node circle,.journey-node rect{fill:#202f42;stroke:#9bc2ff;stroke-width:3}.journey-node text{fill:#edf2fa;text-anchor:middle;font:700 17px system-ui,sans-serif}.journey-node.active circle,.journey-node.active rect{fill:#1d4b49;stroke:#74e0c0;stroke-width:6}.journey-node.active text{font-weight:800}.motion-flow #request-card{fill:#ffd17d;filter:drop-shadow(0 0 5px #ffd17d)}.motion-controls{display:flex;justify-content:center;gap:.7rem;align-items:center;flex-wrap:wrap}.motion-controls button{min-height:44px;padding:.35rem 1rem;border:1px solid var(--line);border-radius:10px;background:var(--surface-2);color:var(--ink);cursor:pointer}.motion-controls button:focus-visible{outline:3px solid var(--amber)}#caption{text-align:center;min-height:1.8em}.visual-pair{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;align-items:center}.visual-pair img,.deck-slide figure img{display:block;width:min(52vw,680px);max-width:100%;max-height:42vh;object-fit:contain;margin:auto}.deck-slide figure small,.visual-pair small{display:block;text-align:center;color:var(--muted);font-size:14px}.visual-pair figcaption,.deck-slide figcaption{text-align:center;color:var(--muted)}.rail,.request-example,.learning-map{display:flex;justify-content:center;align-items:center;gap:clamp(.3rem,1.4vw,1.2rem);flex-wrap:wrap;margin:1rem auto}.rail span,.request-example span,.learning-map span{padding:.7rem 1rem;border:1px solid var(--line);border-radius:12px;background:var(--surface);font-size:clamp(1rem,2vw,1.35rem)}.rail b,.request-example b,.learning-map b{color:var(--mint);font-size:1.5rem}.knowledge-rail span:nth-of-type(1),.knowledge-rail span:nth-of-type(2){opacity:.78}.image-rail span{border-color:var(--mint)}@media(max-width:600px){.lecture .reveal{height:calc(100dvh - 110px)}.deck-slide{justify-content:flex-start}.mini-flow svg{display:none}.mini-flow-mobile{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.35rem;padding:0;list-style:none}.mini-flow-mobile li{padding:.4rem .55rem;border:1px solid var(--line);border-radius:10px;background:var(--surface-2);font-size:15px;text-align:center}.motion-flow{padding:.25rem}.motion-flow>svg{display:none}.mobile-journey{display:grid;grid-template-columns:1fr 1fr;gap:.3rem .5rem;list-style:none;padding:0;margin:.5rem 0;max-height:38vh;overflow:auto}.mobile-journey li{padding:.35rem .45rem;border-left:3px solid var(--line);background:var(--surface-2);color:var(--ink)!important;font-size:15px;line-height:1.35}.mobile-journey li[aria-current="step"]{border-color:var(--mint);background:var(--surface);font-weight:750}.visual-pair{grid-template-columns:1fr;gap:.5rem}.visual-pair img,.deck-slide figure img{max-height:22vh}.rail,.request-example,.learning-map{gap:.3rem}.rail span,.request-example span,.learning-map span{padding:.45rem .6rem;font-size:1rem}}
@media(prefers-reduced-motion:reduce){.lecture .reveal .slides>section{transition:none!important}#request-card{display:none!important}}
</style></body>''',1)
    return html.replace('</head>', '<link rel="icon" href="data:,"></head>', 1)


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

    # 두 강의는 직접 만든 슬라이드와 자체 질문 연결을 보존해 그대로 게시한다.
    lecture_out = OUT / "lectures/01-orchestrator-worker.html"
    lecture_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / "site/lectures/01-orchestrator-worker.html", lecture_out)
    image_lecture_out = OUT / "lectures/04-image-pipeline.html"
    shutil.copyfile(SOURCE / "site/lectures/04-image-pipeline.html", image_lecture_out)
    overview_out = OUT / "lectures/00-overview.html"
    # 강의 00은 자체 슬라이드·단일 공유 SVG를 포함하므로 변환하지 않고 그대로 게시한다.
    shutil.copyfile(SOURCE / "site/lectures/00-overview.html", overview_out)
    workflow_out = OUT / "lectures/02-workflow.html"
    workflow_out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE / "site/lectures/02-workflow.html", workflow_out)
    integration_out = OUT / "lectures/05-integration.html"
    shutil.copyfile(SOURCE / "site/lectures/05-integration.html", integration_out)
    shutil.copyfile(SOURCE / "site/assets/design-system.css", OUT / "assets/design-system.css")
    for name in ("reveal.css", "reveal.js", "LICENSE"):
        dest = OUT / "vendor/reveal" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / "site/vendor/reveal" / name, dest)
    for name in ("context.svg", "handoff.svg", "goal-attempt.svg", "verification.svg", "prompts.md", "forgetting.webp", "handoff.webp", "verify.webp", "workflow.webp", "knowledge.webp", "image-pipeline.webp"):
        dest = OUT / "assets/illustrations" / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(SOURCE / "site/assets/illustrations" / name, dest)

    cards = [
        ("강의 00 · 전체 그림", "lectures/00-overview.html", "에이전트 시스템의 전체 흐름과 결과 확인을 살펴봅니다."),
        ("강의 01 · 지휘 에이전트와 작업 에이전트", "lectures/01-orchestrator-worker.html", "계획·위임 역할과 맡은 작업을 수행하는 역할을 구분합니다."),
        ("강의 02 · 작업 흐름", "lectures/02-workflow.html", "단계 계약과 검증을 전체 흐름 안에서 살펴봅니다."),
        ("강의 04 · 이미지 생성 파이프라인", "lectures/04-image-pipeline.html", "카탈로그·프롬프트·어댑터·검증의 흐름을 살펴봅니다."),
        ("강의 05 · 통합", "lectures/05-integration.html", "네 축을 요청부터 검증된 결과 보고까지 연결합니다."),
        ("왜 파일 handoff가 필요한가", "articles/why-file-handoffs.html", "요청과 결과를 파일로 주고받는 이유를 설명합니다."),
        ("환경", "wiki/environment/README.html", "실습 저장소와 실행 환경의 전제 조건을 확인합니다."),
        ("예제 안내", "wiki/examples/README.html", "portable worker 예제의 구성과 사용 경로를 살펴봅니다."),
        ("계약", "wiki/reference/contracts.html", "요청·응답 필드와 상태 전이를 찾아봅니다."),
        ("작업 흐름 참조", "wiki/reference/workflow.html", "현재 단계 계약, 검사, 활성 범위를 찾아봅니다."),
        ("용어", "wiki/reference/terms.html", "문서에서 사용하는 핵심 용어를 확인합니다."),
        ("이미지 생성 파이프라인 참조", "wiki/image-pipeline.html", "예제의 공개 계약과 확인 절차를 찾아봅니다."),
        ("통합 연결 계약", "wiki/integration.html", "요청·단계·지식·산출·검증의 연결 계약을 찾아봅니다."),
        ("portable worker 실행", "examples/portable-worker/README.html", "합성 fixture로 portable worker를 실행합니다."),
        ("작업 프롬프트", "examples/portable-worker/PROMPT.html", "예제에 사용할 안전한 작업 지시를 확인합니다."),
        ("이미지 파이프라인 예제", "examples/image-pipeline/README.html", "합성 입력으로 오프라인 파이프라인을 재현합니다."),
        ("이미지 파이프라인 과제", "examples/image-pipeline/PROMPT.html", "에이전트에게 맡길 안전한 테스트 과제를 확인합니다."),
        ("통합 예제", "examples/integration-check/README.html", "합성 입력으로 전체 연결을 오프라인에서 확인합니다."),
        ("통합 예제 과제", "examples/integration-check/PROMPT.html", "에이전트가 안전한 통합 계약을 점검합니다."),
        ("예제 코드·소스와 테스트", "code/index.html", "예제 구현과 테스트를 읽고 원본 파일을 내려받습니다."),
    ]

    sections = [("강의", cards[:5]), ("해설", cards[5:6]), ("위키", cards[6:13]), ("예제", cards[13:19]), ("예제 코드", cards[19:])]
    body = '<p class="tag">사용자 리뷰용</p><h1>p-hermes 재정비 파일럿 미리보기(리뷰용)</h1><p class="muted">처음 방문하면 강의 00부터 순서대로 시작합니다. 이어지는 각 강의는 앞선 질문을 받아 전체 흐름을 완성합니다.</p><section id="learning-start"><h2>처음 시작하는 학습 경로 · 강의 00~05</h2><ol><li><a href="lectures/00-overview.html">강의 00 · 전체 흐름</a></li><li><a href="lectures/01-orchestrator-worker.html">강의 01 · 지휘·작업 에이전트</a></li><li><a href="lectures/02-workflow.html">강의 02 · 작업 흐름</a></li><li><a href="lectures/03-knowledge.html">강의 03 · 지식 참조 (P4 통합 대기)</a></li><li><a href="lectures/04-image-pipeline.html">강의 04 · 이미지 생성</a></li><li><a href="lectures/05-integration.html">강의 05 · 통합</a></li></ol></section>'
    for heading, entries in sections:
        body += f'<section><h2>{heading}</h2><ul>' + "".join(f'<li><a href="{href}">{label}</a> — {desc}</li>' for label, href, desc in entries) + '</ul></section>'
    body += '<p>예제 코드는 HTML escape를 적용한 보기 화면과 원본 다운로드 링크를 함께 제공합니다. 입력은 합성 fixture이며 실서비스 연동은 하지 않습니다.</p>'
    (OUT / "index.html").write_text(page("p-hermes 재정비 파일럿 미리보기(리뷰용)", body), encoding="utf-8", newline="\n")

    # Copy the reviewed, publish-ready HTML pages and downloadable example sources.
    for rel in actual:
        if rel.startswith("site/wiki/") or rel.startswith("site/articles/") or rel.startswith("site/examples/") or rel.startswith("site/code/") or rel.startswith("site/downloads/"):
            dest = OUT / rel.removeprefix("site/")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if rel == "site/articles/why-file-handoffs.html":
                text = (SOURCE / rel).read_text(encoding="utf-8").replace("../../", "../")
                dest.write_text(text, encoding="utf-8", newline="\n")
            else:
                shutil.copyfile(SOURCE / rel, dest)
    # Example README and agent prompt are rendered from the reviewed Markdown sources.
    for name in ("README", "PROMPT"):
        source = SOURCE / f"examples/image-pipeline/{name}.md"
        rendered = page(f"이미지 파이프라인 · {name}", render_markdown(source.read_text(encoding="utf-8")), 2)
        target = OUT / f"examples/image-pipeline/{name}.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8", newline="\n")
    shutil.copyfile(SOURCE / "site/assets/publish-design-system.css", OUT / "assets/design-system.css")

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
    for rel in sorted(p for p in actual if p.startswith("site/code/")):
        html_rel = Path(rel.removeprefix("site/"))
        source_rel = Path(rel.removeprefix("site/code/"))
        download_rel = Path("downloads") / source_rel.with_suffix("")
        rows.append(f'<li><a href="{html_rel.as_posix().removeprefix("code/")}">{escape(source_rel.as_posix())}</a> · <a href="../{download_rel.as_posix()}">원본 다운로드</a></li>')
    code_body = '<p><a href="../index.html">← 미리보기 목차</a></p><h1>코드·예제·테스트</h1><p>화면은 HTML escape를 적용한 보기용입니다. 다운로드 파일도 같은 allowlist에서 생성됩니다.</p><ul>' + "".join(rows) + "</ul>"
    (OUT / "code/index.html").write_text(page("코드·예제·테스트", code_body, 1), encoding="utf-8", newline="\n")
    print(f"built preview: {len(ALLOWED)} source files, {len(items)} code files -> docs/preview")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
