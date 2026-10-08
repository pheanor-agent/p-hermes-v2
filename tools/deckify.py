"""Build every lecture as one 16:9 presentation deck with a shared frame.

Lecture sources live in ``site/lectures/NN-*.html`` as a list of
``<section class="slide" data-eyebrow=".." data-kind="cover|main|text|sim">``
blocks. Each slide has one ``<h2>`` title, an optional authored scene
(``<figure class="scene">`` with an SVG) or simulator (``<div data-sim="..">``),
body paragraphs and an optional ``<p class="next">`` question that hands over to
the following slide. ``data-layout="wide"`` puts the copy above a full-width scene
for wide strip diagrams. Motion (draw-in, packets, builds) is declared in the SVG
with ``mo-*`` classes and run by ``assets/motion.js``.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

LECTURES = [
    ("00-overview.html", "00", "전체 그림"),
    ("01-orchestrator-worker.html", "01", "매니저 에이전트와 작업 에이전트"),
    ("02-workflow.html", "02", "작업 흐름"),
    ("03-knowledge.html", "03", "지식"),
    ("04-integration.html", "04", "통합"),
]

# Retired lecture URLs keep working as redirects to their successors.
RETIRED = {
    "04-image-pipeline.html": "index.html",
    "05-integration.html": "04-integration.html",
}

CURRENT = ' aria-current="page"'
SECTION_RE = re.compile(r'<section class="slide"([^>]*)>(.*?)</section>', re.S)
TAG_RE = re.compile(r"<[^>]+>")

SHARED_DEFS = (
    '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
    '<marker id="mo-arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9z" fill="#879cb3"/></marker>'
    '<marker id="mo-arrow-mint" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9z" fill="#82dec6"/></marker>'
    '<marker id="mo-arrow-coral" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9z" fill="#ff9f8f"/></marker>'
    '</defs></svg>'
)


def text(fragment: str) -> str:
    return " ".join(html.unescape(TAG_RE.sub(" ", fragment)).split())


def attr(attrs: str, name: str) -> str:
    m = re.search(rf'{name}="([^"]*)"', attrs)
    return m.group(1) if m else ""


def parse(source: str, number: str) -> list[dict]:
    slides = []
    for idx, (attrs, body) in enumerate(SECTION_RE.findall(source), 1):
        title = re.search(r"<h2[^>]*>(.*?)</h2>", body, re.S)
        if not title:
            raise ValueError(f"강의 {number} {idx}장: h2 제목 없음")
        scene = re.search(r'<figure class="scene(?:\s+[^\"]*)?"[^>]*>.*?</figure>', body, re.S)
        sim = re.search(r'<div data-sim="[^"]+"[^>]*></div>', body)
        rest = body
        for m in (title, scene, sim):
            if m:
                rest = rest.replace(m.group(0), "", 1)
        nxt = re.search(r'<p class="next">(.*?)</p>', rest, re.S)
        if nxt:
            rest = rest.replace(nxt.group(0), "", 1)
        paras = re.findall(r'<p(\s+class="[^"]*")?>(.*?)</p>', rest, re.S)
        slides.append({
            "key": attr(attrs, "data-slide-key"),
            "eyebrow": attr(attrs, "data-eyebrow"),
            "kind": attr(attrs, "data-kind") or ("main" if scene or sim else "text"),
            "title": title.group(1).strip(),
            "scene": scene.group(0) if scene else "",
            "sim": sim.group(0) if sim else "",
            "paras": [(c or "", p.strip()) for c, p in paras],
            "next": nxt.group(1).strip() if nxt else "",
            "kicker": attr(attrs, "data-kicker"),
            "gap": attr(attrs, "data-build-gap"),
            "wide": attr(attrs, "data-layout") == "wide",
        })
    if not slides:
        raise ValueError(f"강의 {number}: 슬라이드 없음")
    return slides


def ambient(seed: int) -> str:
    """Deterministic drifting particles behind cover and interlude slides."""
    dots = []
    for k in range(26):
        x = (seed * 37 + k * 211) % 1600
        y = (seed * 53 + k * 137) % 900
        r = 2 + (k * 7 + seed) % 4
        dx = ((k * 29) % 70) - 35
        dy = ((k * 41) % 80) - 40
        t = 10 + (k * 3) % 12
        dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" style="--x:{dx}px;--y:{dy}px;--t:{t}s;--dl:-{k % 9}s"/>')
    lines = "".join(f'<path d="M{-50 + k * 420} 900C{200 + k * 420} {600 - k * 40} {300 + k * 380} {300 + k * 30} {700 + k * 300} -20"/>' for k in range(4))
    return f'<svg class="dk-ambient" viewBox="0 0 1600 900" preserveAspectRatio="none" aria-hidden="true">{lines}{"".join(dots)}</svg>'


def words(title: str) -> str:
    """Split a title into word spans for kinetic typography.

    Splitting happens only at real spaces, so a highlighted <em> phrase stays glued
    to the Korean particle that follows it (no stray space before "가", "라고"...).
    """
    protected = re.sub(r"<em>(.*?)</em>", lambda m: "<em>" + m.group(1).replace(" ", "\u00a0") + "</em>", title)
    return " ".join(f'<span class="w" style="--i:{i}">{w.replace(chr(160), " ")}</span>'
                    for i, w in enumerate(protected.split(" ")) if w)


def figure(scene: str) -> str:
    return re.sub(r'<figure class="scene(?=[\s"])', '<figure class="dk-scene', scene, count=1)


def sim_static(sim: str) -> str:
    name = attr(re.search(r'<div\b([^>]*)>', sim).group(1), "data-sim")
    examples = {
        "delegate": ("위임 판단의 예", ["수백 개 파일 일괄 변환", "긴 실행·큰 산출 → 작업자에 위임", "매니저는 목표와 결과 판정을 맡음"]),
        "verdict": ("완료 보고를 대조한 예", ["보고: 배송 문의 25%", "원자료: 전체 200건·배송 40건", "40÷200=20% → 보고 수정"]),
        "gate": ("기록 누락을 보완한 예", ["검증 기록 누락 → 단계 전이 정지", "실제로 대조하고 검증 기록 보완", "필수 기록 확인 → 다음 단계"]),
        "shelf": ("사건을 분류한 예", ["검사는 통과했지만 화면이 깨짐", "사건 기록 → 교훈 후보", "원인·수정·확인을 더해 검토"]),
        "lifecycle": ("문의 회고가 완료된 예", ["약속: 원자료 집계·대조", "산출: 집계.csv·회고 초안", "전체200·배송40 → 20% 대조", "확인한 결과와 남은 일 보고"]),
    }
    title, lines = examples[name]
    return '<div class="sim-static"><div class="example-doc result"><h3>' + html.escape(title) + '</h3>' + ''.join('<p>'+html.escape(line)+'</p>' for line in lines) + '</div></div>'


def static_reading(name: str, slides: list[dict]) -> str:
    """Linear no-JS reading path retaining authored explanations and checks."""
    sections = []
    for i, slide in enumerate(slides, 1):
        copy = "".join(f"<p>{p}</p>" for _, p in slide["paras"])
        # Keep evidence and reveal exercise answers in the linear no-JS path.
        scene = re.sub(r'<svg\b[^>]*>.*?</svg>', '', slide['scene'], flags=re.S)
        scene = re.sub(r'<div class="lesson-actions">.*?</div>', '', scene, flags=re.S)
        scene = re.sub(r'<div class="lesson-caption"[^>]*>.*?</div>', '', scene, flags=re.S)
        scene = re.sub(r'\s(?:id|aria-live|data-lesson-flow|data-act-groups)(?:="[^"]*")?', '', scene)
        scene = scene.replace("data-quiz-answer hidden", "data-quiz-answer")
        scene = re.sub(r'<button\b[^>]*>.*?</button>', "", scene, flags=re.S)
        labels = re.findall(r'<text\b[^>]*>(.*?)</text>', slide['scene'], re.S)
        if labels and 'recall-scene' not in slide['scene'] and 'lesson-flow' not in slide['scene']:
            scene += '<p class="static-evidence">그림의 관계: ' + ' · '.join(text(x) for x in labels) + '</p>'
        if slide["sim"]:
            scene += sim_static(slide["sim"])
        next_q = f'<p><b>다음 질문:</b> {slide["next"]}</p>' if slide["next"] else ""
        sections.append(f'<section><h2>{i:02d}. {slide["title"]}</h2>{copy}{scene}{next_q}</section>')
    return '<noscript><main class="dk-static"><h1>' + html.escape(name) + ' · 정적 읽기</h1>' + "".join(sections) + '</main></noscript>'


def render(number: str, name: str, slides: list[dict]) -> str:
    total = len(slides)
    nums = [n for _, n, _ in LECTURES]
    pos = nums.index(number)
    prev_lec = LECTURES[pos - 1] if pos > 0 else None
    next_lec = LECTURES[pos + 1] if pos + 1 < len(LECTURES) else None
    parts = []
    for i, s in enumerate(slides, 1):
        paras = "".join(
            f'<p class="dk-p{" mo-hint" if "hint" in c else ""}">{p}</p>' for c, p in s["paras"]
        )
        stage = figure(s["scene"]) if s["scene"] else (s["sim"] + sim_static(s["sim"]) if s["sim"] else "")
        layout = {"cover": "dk-cover", "sim": "dk-sim", "text": "dk-text", "interlude": "dk-interlude",
                  "concept": "dk-main dk-concept"}.get(s["kind"], "dk-main")
        if not stage and layout not in ("dk-cover", "dk-interlude"):
            layout = "dk-text"
        if s["wide"] and s["scene"]:
            layout += " dk-wide"  # wide strip diagram: copy on top, scene across the full width
        gap = f' data-build-gap="{s["gap"]}"' if s["gap"] else ""
        if layout == "dk-interlude":
            sub = "".join(f'<p class="dk-sub">{p}</p>' for _, p in s["paras"])
            parts.append(
                f'<article class="dk-slide dk-interlude" id="s{i}" data-index="{i}" data-slide-key="{html.escape(s["key"], quote=True)}" aria-label="{i} / {total}">{ambient(i + int(number) * 7)}'
                f'<div class="dk-rings" aria-hidden="true"><i></i><i></i><i></i></div>'
                f'<div class="dk-inner"><p class="dk-kicker">{html.escape(s["kicker"] or s["eyebrow"])}</p>'
                f'<h2 class="dk-title dk-big">{words(s["title"])}</h2>{sub}</div></article>'
            )
            continue
        if s["next"]:
            if i == total and next_lec:
                nxt = f'<p class="dk-next"><b>다음 질문 · 강의 {next_lec[1]}</b><a href="{next_lec[0]}">{s["next"]}</a></p>'
            else:
                nxt = f'<p class="dk-next"><b>다음 질문</b>{s["next"]}</p>'
        elif i == total and next_lec:
            nxt = f'<p class="dk-next"><b>다음 강의</b><a href="{next_lec[0]}">강의 {next_lec[1]} · {html.escape(next_lec[2])} →</a></p>'
        elif i == total:
            nxt = '<p class="dk-next"><b>마지막 장</b><a href="../index.html">강의 목록으로 →</a></p>'
        else:
            nxt = ""
        prev_q = [x for x in slides[: i - 1] if x["kind"] != "interlude"]
        before = prev_q[-1]["next"] if prev_q else ""
        previous = (f'<p class="dk-prev"><b>이어받은 질문</b>{before}</p>' if before
                    else '<p class="dk-prev"><b>강의의 출발점</b>전체 흐름에서 지금 볼 구간을 정합니다.</p>')
        parts.append(
            f'<article class="dk-slide {layout}" id="s{i}" data-index="{i}" data-slide-key="{html.escape(s["key"], quote=True)}" aria-label="{i} / {total}"{gap}>'
            + (ambient(i + int(number) * 7) if layout == "dk-cover" else "") +
            f'<header class="dk-head"><span class="dk-eyebrow">{html.escape(s["eyebrow"])}</span>'
            f'<span class="dk-count">{i:02d} / {total:02d}</span></header>'
            f'<h2 class="dk-title">{s["title"]}</h2>'
            f'<div class="dk-body"><div class="dk-copy">{paras}</div>{stage}</div>'
            f'<footer class="dk-foot">{previous}{nxt}</footer></article>'
        )
    lec_links = "".join(f'<a href="{f}"{CURRENT if n == number else ""}>{n}</a>' for f, n, _ in LECTURES)
    prev_link = f'<a class="dk-lec" href="{prev_lec[0]}">← 강의 {prev_lec[1]}</a>' if prev_lec else ""
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{number} · {html.escape(name)}</title><link rel="icon" href="data:,">
<link rel="preload" href="../assets/fonts/pretendard-subset.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="../assets/design-system.css">
<link rel="stylesheet" href="../assets/deck.css">
<link rel="stylesheet" href="../assets/motion.css">
<noscript><style>html,body.dk{{height:auto!important;overflow:auto!important}}.dk-viewport,.dk-controls{{display:none!important}}</style></noscript>
</head><body class="dk dk-course-{number}">
{SHARED_DEFS}
<div class="dk-viewport"><main class="dk-stage" id="deck" aria-label="강의 {number} · {html.escape(name)}">
<div class="dk-brand"><a href="../index.html">p-hermes</a><span>강의 {number} · {html.escape(name)}</span></div>
{''.join(parts)}
<div class="dk-progress"><span></span></div>
</main></div>
<nav class="dk-controls" aria-label="슬라이드 이동"><a class="dk-home" href="../index.html">강의 목록</a>{prev_link}<span class="dk-lecs">{lec_links}</span>
<button type="button" data-go="-1" aria-label="이전 장">←</button><span class="dk-live-count" aria-live="polite" aria-atomic="true"></span><button type="button" data-go="1" aria-label="다음 장">→</button>
<button type="button" data-motion-pause aria-pressed="false">일시정지</button><button type="button" data-motion-restart>다시 재생</button>
<button type="button" data-fs aria-label="전체 화면 (F)"><svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M1 6V1h5M12 1h5v5M17 12v5h-5M6 17H1v-5"/></svg></button></nav>
{static_reading(name, slides)}
<script src="../assets/motion.js"></script>
<script src="../assets/deck.js"></script>
</body></html>
"""


def redirect(target: str) -> str:
    return (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>이동한 강의</title>'
            f'<meta http-equiv="refresh" content="0; url={target}"><link rel="canonical" href="{target}"></head>'
            f'<body><p>강의 구성이 바뀌었습니다. <a href="{target}">새 위치로 이동</a></p></body></html>')


def build(source_dir: Path, out_dir: Path) -> list[Path]:
    missing = [f for f, _, _ in LECTURES if not (source_dir / f).is_file()]
    if missing:
        raise FileNotFoundError("필수 강의 원고 누락: " + ", ".join(missing))
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for fname, number, name in LECTURES:
        slides = parse((source_dir / fname).read_text(encoding="utf-8"), number)
        out = out_dir / fname
        out.write_text(render(number, name, slides), encoding="utf-8")
        written.append(out)
    mapping = ["stablekey,oldkey,newnumber,title,reason"]
    for fname, number, _ in LECTURES:
        slides = parse((source_dir / fname).read_text(encoding="utf-8"), number)
        for i, slide in enumerate(slides, 1):
            key = slide["key"] or f"{number}-{i:02d}"
            title = text(slide["title"]).replace('"', '""')
            is_new = "example-" in key
            reason = "신규 실물·비교 근거를 앞뒤 질문 흐름에 맞게 분리" if is_new else "원형 페이지 key를 유지하고 정확성 수정만 반영"
            mapping.append(f'{key},{"" if is_new else key},{number}-{i:02d},"{title}","{reason}"')
    (out_dir.parent / "lecture-slide-mapping.csv").write_text("\n".join(mapping) + "\n", encoding="utf-8")
    for old, target in RETIRED.items():
        out = out_dir / old
        out.write_text(redirect(target), encoding="utf-8")
        written.append(out)
    return written


def slide_counts(source_dir: Path) -> dict[str, int]:
    return {n: len(parse((source_dir / f).read_text(encoding="utf-8"), n)) for f, n, _ in LECTURES}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for p in build(root / "site/lectures", root / "docs/lectures"):
        print(p)
