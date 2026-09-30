"""Rebuild every lecture as one 16:9 presentation deck with a shared layout.

Each source lecture keeps its own diagram SVGs and diagram CSS, but the slide
frame (title, explanation, diagram stage, question rail, navigation) comes from
one template so all lectures look and behave the same.
"""
from __future__ import annotations

import html
import re
from pathlib import Path
import xml.etree.ElementTree as ET

LECTURES = [
    ("00-overview.html", "00", "전체 그림"),
    ("01-orchestrator-worker.html", "01", "지휘 에이전트와 작업 에이전트"),
    ("02-workflow.html", "02", "작업 흐름"),
    ("03-knowledge.html", "03", "지식 참조"),
    ("04-image-pipeline.html", "04", "이미지 생성 파이프라인"),
    ("05-integration.html", "05", "통합"),
]

CURRENT = ' aria-current="page"'
SECTION_RE = re.compile(r'<section class="slide[^"]*"[^>]*>(.*?)</section>', re.S)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S)
TAG_RE = re.compile(r"<[^>]+>")


def text(fragment: str) -> str:
    return " ".join(html.unescape(TAG_RE.sub(" ", fragment)).split())


def inner(fragment: str, pattern: str) -> str | None:
    m = re.search(pattern, fragment, re.S)
    return m.group(1).strip() if m else None


def strip_containers(section: str, classes: tuple[str, ...]) -> str:
    """Drop overview-map style blocks (e.g. 04/05 top flow bar) from a slide."""
    for cls in classes:
        section = re.sub(
            rf'<(figure|div|nav)[^>]*class="[^"]*\b{cls}\b[^"]*"[^>]*>.*?</\1>', "", section, flags=re.S
        )
    return section


def pick_diagram(section: str) -> tuple[str | None, str]:
    """Return (svg, wrapper_classes) for the largest diagram in the slide."""
    best = None
    for m in SVG_RE.finditer(section):
        if best is None or len(m.group(0)) > len(best.group(0)):
            best = m
    if best is None:
        return None, ""
    before = section[: best.start()]
    # Keep the class names of still-open ancestor elements so the lecture's own
    # diagram CSS (often scoped like `.flow-panel svg .node`) still matches.
    stack: list[str] = []
    for tag in re.finditer(r"<(/?)(div|figure|span)\b([^>]*)>", before):
        if tag.group(1):
            if stack:
                stack.pop()
        else:
            cls = re.search(r'class="([^"]*)"', tag.group(3))
            stack.append(cls.group(1) if cls else "")
    return best.group(0), "|".join(c for c in stack if c)


def overview_svg(svg: str, level: int, focus: str) -> str:
    # Same map on every page; readable labels and separate request/return lanes.
    nodes = [
        (1, 'person', 24, 254, 180, '사람', '요청 · 완료 조건'),
        (1, 'model', 272, 254, 230, '언어 모델', '맥락으로 응답 생성'),
        (3, 'orchestrator', 272, 78, 230, '지휘 에이전트', '목표 · 범위 · 위임'),
        (4, 'worker', 24, 78, 210, '작업 에이전트', '맡은 범위 처리'),
        (5, 'workflow', 568, 78, 230, '작업 흐름', '단계 · 전이'),
        (6, 'knowledge', 568, 254, 230, '지식 참조', '원문 · 근거'),
        (7, 'pipeline', 568, 430, 230, '산출 파이프라인', '구성 → 결과물'),
        (8, 'verify', 854, 430, 170, '검증', '실제 결과 대조'),
        (8, 'report', 854, 254, 170, '결과 보고', '확인한 결과'),
    ]
    wires = [
        (1, 'M204 303H272', 238, 240, '대화'),
        (3, 'M387 254V176', 438, 214, '목표'),
        (4, 'M272 110H234', 253, 61, '위임'),
        (4, 'M234 152H272', 253, 204, '응답'),
        (5, 'M502 127H568', 535, 98, '경계'),
        (6, 'M683 176V254', 730, 220, '근거'),
        (7, 'M683 352V430', 730, 397, '구성'),
        (8, 'M798 479H854', 826, 402, '대조'),
        (8, 'M939 430V352', 986, 397, '보고'),
    ]
    chunks = [
        '<svg class="dk-map" style="--dk-map-arrow:url(#map-arrow)" viewBox="0 0 1048 558" role="img" aria-label="사람의 요청에서 결과 보고까지 이어지는 전체 흐름">',
        '<defs><marker id="map-arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8z" fill="#879cb3"/></marker></defs>',
        '<text class="focus-label" x="24" y="28">지금 보는 부분 · ' + html.escape(focus) + '</text>',
    ]
    for step, d, x, y, label in wires:
        # The conversation link is replaced by a visible gap on the second page.
        if step == 1 and level == 2:
            continue
        chunks.append(f'<g data-step="{step}"><path class="wire" marker-end="url(#map-arrow)" d="{d}"/><text class="wire-label" x="{x}" y="{y}">{label}</text></g>')
    if level == 2:
        chunks.append('<g class="gap" data-step="2"><path d="M204 303H226M250 303H272" fill="none" stroke="#ffad9f" stroke-width="3" stroke-dasharray="5 4"/><circle cx="238" cy="303" r="17" fill="#132130" stroke="#ffad9f"/><text class="wire-label" x="238" y="383">공백</text></g>')
    for step, cls, x, y, width, label, sub in nodes:
        chunks.append(f'<g class="node {cls}" data-step="{step}"><rect x="{x}" y="{y}" width="{width}" height="98" rx="9"/><text x="{x+width/2}" y="{y+40}">{label}</text><text class="sub" x="{x+width/2}" y="{y+72}">{sub}</text></g>')
    chunks.append('</svg>')
    svg = ''.join(chunks)
    def mark(m: re.Match) -> str:
        tag = m.group(0)
        step = int(m.group(1))
        extra = ("revealed " if step <= level else "") + ("current" if step == level else "")
        if 'class="' in tag:
            return tag.replace('class="', f'class="{extra} ', 1)
        return tag[:-1] + f' class="{extra.strip()}">'

    svg = re.sub(r'<[a-z]+\b[^>]*data-step="(\d+)"[^>]*>', mark, svg)
    svg = re.sub(
        r'(<text[^>]*class="[^"]*focus-label[^"]*")([^>]*>).*?(</text>)',
        lambda m: m.group(1).replace('focus-label', 'focus-label show') + m.group(2) + "지금 보는 부분 · " + html.escape(focus) + m.group(3),
        svg,
        flags=re.S,
    )
    return svg


def light_layers(svg: str, level: int) -> str:
    """Static version of the per-slide JS that switched on diagram layers <= slide."""
    def mark(m: re.Match) -> str:
        tag = m.group(0)
        if int(m.group(2)) > level:
            return tag
        if 'class="' in tag:
            return tag.replace('class="', 'class="on active ', 1)
        return tag[:-1] + ' class="on active">'

    return re.sub(r'<[a-z]+\b[^>]*data-(layer|level)="(\d+)"[^>]*>', mark, svg)


GROUP_RE = re.compile(
    r'<g>\s*<rect class="(box[^"]*)" x="([\d.]+)" y="([\d.]+)" width="([\d.]+)" height="([\d.]+)" rx="([\d.]+)"/>'
    r'\s*<text x="([\d.]+)" y="([\d.]+)">(.*?)</text>\s*</g>',
    re.S,
)


def relayout_rows(svg: str) -> str:
    """Evenly re-space a row of boxes when the source coordinates overlap."""
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not vb:
        return svg
    width = float(vb.group(1))
    groups = list(GROUP_RE.finditer(svg))
    rows: dict[float, list[re.Match]] = {}
    for g in groups:
        rows.setdefault(float(g.group(3)), []).append(g)
    for y, row in rows.items():
        row.sort(key=lambda g: float(g.group(2)))
        xs = [(float(g.group(2)), float(g.group(4))) for g in row]
        overlap = any(a[0] + a[1] > b[0] - 8 for a, b in zip(xs, xs[1:]))
        if len(row) < 2 or not (overlap or xs[-1][0] + xs[-1][1] > width - 10):
            continue
        n, margin, gap = len(row), 16.0, 22.0
        w = min(170.0, (width - 2 * margin - (n - 1) * gap) / n)
        total = n * w + (n - 1) * gap
        start = (width - total) / 2
        old_c = [x + ww / 2 for x, ww in xs]
        new_x = [start + i * (w + gap) for i in range(n)]
        new_c = [x + w / 2 for x in new_x]
        h = float(row[0].group(5))
        cy = y + h / 2

        def remap(x: float) -> float:
            if x <= old_c[0]:
                return new_c[0] + (x - old_c[0]) * w / xs[0][1]
            if x >= old_c[-1]:
                return new_c[-1] + (x - old_c[-1]) * w / xs[-1][1]
            for a in range(n - 1):
                if old_c[a] <= x <= old_c[a + 1]:
                    t = (x - old_c[a]) / (old_c[a + 1] - old_c[a])
                    return new_c[a] + t * (new_c[a + 1] - new_c[a])
            return x

        for g, nx in zip(row, new_x):
            label = g.group(9)
            units = sum(1.0 if ord(ch) > 0x2E80 else 0.55 for ch in text(label)) or 1
            size = max(14.0, min(17.0, (w - 12) / units))
            fs = f' style="font-size:{size:.1f}px"' if size < 17 else ""
            new = (
                f'<g><rect class="{g.group(1)}" x="{nx:.1f}" y="{y:g}" width="{w:.1f}" height="{h:g}" rx="{g.group(6)}"/>'
                f'<text x="{nx + w / 2:.1f}" y="{g.group(8)}"{fs}>{label}</text></g>'
            )
            svg = svg.replace(g.group(0), new, 1)
        # Wires on this row: rebuild as arrows between neighbouring boxes.
        segs = "".join(f"M{new_x[i] + w:.1f} {cy:g}H{new_x[i + 1] - 4:.1f}" for i in range(n - 1))

        def fix_wire(m: re.Match) -> str:
            d = m.group(2)
            ys = {float(v) for v in re.findall(r"M[\d.]+ ([\d.]+)H", d)}
            if ys and ys <= {cy, y + 40}:
                return f'{m.group(1)}d="{segs}"'
            return m.group(0)

        svg = re.sub(r'(<path class="wire"[^>]*?)d="([^"]*)"', fix_wire, svg)
        if 'marker-end' not in svg.split('class="wire"', 1)[-1].split(">", 1)[0]:
            svg = svg.replace('<path class="wire"', '<path class="wire" marker-end="url(#arrow)"', 1)

        def fix_dash(m: re.Match) -> str:
            d = re.sub(r"M([\d.]+)", lambda k: f"M{remap(float(k.group(1))):.1f}", m.group(2))
            d = re.sub(r"H([\d.]+)", lambda k: f"H{remap(float(k.group(1))):.1f}", d)
            return f"{m.group(1)}d=\"{d}\""

        svg = re.sub(r'(<path class="dash"[^>]*?)d="([^"]*)"', fix_dash, svg)
        svg = re.sub(
            r'(<text class="small" x=")([\d.]+)(")',
            lambda k: f"{k.group(1)}{remap(float(k.group(2))):.1f}{k.group(3)}",
            svg,
        )
    return svg


def uniq_ids(svg: str, prefix: str) -> str:
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in ids:
        svg = svg.replace(f'id="{i}"', f'id="{prefix}{i}"')
        svg = svg.replace(f"url(#{i})", f"url(#{prefix}{i})")
        svg = svg.replace(f'href="#{i}"', f'href="#{prefix}{i}"')
    root = ET.fromstring(svg)
    marker = next(root.iter('marker'), None)
    if marker is None:
        defs = ET.SubElement(root, 'defs')
        marker = ET.SubElement(defs, 'marker', {'id':prefix+'arrow','markerWidth':'8','markerHeight':'8','refX':'7','refY':'4','orient':'auto'})
        ET.SubElement(marker,'path',{'d':'M0 0L8 4L0 8z','fill':'#879cb3'})
    # Inherited lecture CSS still contains url(#arrow). Bind every SVG's wires
    # to its own namespaced marker rather than to a document-wide identifier.
    root.set('style', root.get('style','')+f';--dk-arrow:url(#{marker.get("id")})')
    return ET.tostring(root, encoding='unicode')


def readable_labels(svg: str) -> str:
    """Wrap long node labels at spaces instead of shrinking Korean letters.

    Coordinates, connections and text are preserved. Only a box's text block is
    recentered when its labels require two lines at the presentation font size.
    """
    root = ET.fromstring(svg)
    labels = list(root.iter('text'))
    for t in labels:
        declared = t.get('font-size')
        if declared and float(declared) < 18:
            t.set('class', (t.get('class', '') + ' dk-svg-note').strip())

    def units(value: str) -> float:
        return sum(1 if ord(c) > 0x2E80 else (.34 if c.isspace() else .62) for c in value)

    for rect in root.iter('rect'):
        x, y, w, h = (float(rect.get(k, '0')) for k in ('x', 'y', 'width', 'height'))
        inside = [t for t in labels if x < float(t.get('x', '-1')) < x+w
                  and y < float(t.get('y', '-1')) < y+h and t.text]
        if not inside:
            continue
        inside.sort(key=lambda t: float(t.get('y', '0')))
        blocks = []
        changed = False
        for t in inside:
            size = 18 if set(t.get('class', '').split()) & {'small', 'sub', 'dk-svg-note'} else 22
            value = t.text or ''
            rows = [value]
            words = value.split()
            if units(value) * size > w-20 and len(words) > 1:
                split = min(range(1, len(words)), key=lambda k: max(units(' '.join(words[:k])), units(' '.join(words[k:]))))
                rows = [' '.join(words[:split]), ' '.join(words[split:])]
                changed = True
            blocks.append((t, size, rows))
        if not changed:
            continue
        total_height = sum(size*1.16*len(rows) for _, size, rows in blocks)
        cursor = y+(h-total_height)/2
        for t, size, rows in blocks:
            t.text = None
            baseline = cursor+size*.85
            t.set('y', f'{baseline:.1f}')
            for j, row in enumerate(rows):
                child = ET.SubElement(t, 'tspan', {'x':t.get('x','0'), 'y':f'{baseline+j*size*1.16:.1f}'})
                child.text = row
            cursor += size*1.16*len(rows)
    return ET.tostring(root, encoding='unicode')


def parse(source: str, number: str) -> tuple[str, list[dict]]:
    style = "\n".join(re.findall(r"<style>(.*?)</style>", source, re.S))
    sections = SECTION_RE.findall(source)
    shared_svg = None
    if number == "00":
        shared_svg, _ = pick_diagram(sections[0])
    slides = []
    for idx, sec in enumerate(sections, 1):
        attrs = re.search(r'<section class="slide[^"]*"([^>]*)>', source.split("</section>")[idx - 1]).group(1)
        focus = inner(attrs, r'data-focus="([^"]*)"') or ""
        head = inner(sec, r"<header[^>]*>(.*?)</header>") or ""
        eyebrow = text(re.sub(r"\d+\s*/\s*\d+", "", head))
        body = strip_containers(sec, ("whole-map", "whole-flow", "overall-flow"))
        body = re.sub(r"<header.*?</header>", "", body, flags=re.S)
        rail = inner(body, r'<nav[^>]*class="[^"]*\bquestion-rail\b[^"]*"[^>]*>(.*?)</nav>') or inner(body, r"<nav[^>]*>(.*?)</nav>") or ""
        body = re.sub(r"<nav.*?</nav>", "", body, flags=re.S)
        prev = inner(rail, r"←[^<]*</b>\s*(?:<br>)?(.*?)</(?:span|a)>")
        nxt = inner(rail, r"→[^<]*</b>\s*(?:<br>)?(.*?)</(?:span|a)>")
        title = inner(body, r"<h[12][^>]*>(.*?)</h[12]>") or ""
        img = re.search(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', body)
        if number == "00":
            svg, wrap = shared_svg, "diagram-frame"
            svg = overview_svg(svg, idx, focus)
        else:
            svg, wrap = pick_diagram(body)
            if svg:
                svg = readable_labels(relayout_rows(light_layers(svg, idx)))
        caption = inner(body, r"<figcaption[^>]*>(.*?)</figcaption>") or inner(body, r'<p class="diagram-caption"[^>]*>(.*?)</p>')
        body_wo_svg = SVG_RE.sub("", body)
        copy = re.sub(r"<h[12].*?</h[12]>", "", body_wo_svg, count=1, flags=re.S)
        copy = re.sub(r"<figcaption.*?</figcaption>", "", copy, flags=re.S)
        paras = [p.strip() for p in re.findall(r"<p\b[^>]*>(.*?)</p>", copy, re.S)]
        paras = [p for p in paras if text(p) and text(p) != text(caption or "") and "eyebrow" not in p]
        slides.append(
            {
                "eyebrow": eyebrow,
                "title": title,
                "paras": paras,
                "svg": uniq_ids(svg, f"s{idx}-") if svg else None,
                "wrap": wrap,
                "caption": text(caption) if caption else "",
                "img": img.groups() if img else None,
                "prev": prev,
                "next": nxt,
            }
        )
    return style, slides


def wrap_prose(fragment: str) -> str:
    """Allow stage sequences to wrap after arrows without splitting their names."""
    return "".join(
        part if part.startswith("<") else part.replace("→", "→<wbr>")
        for part in re.split(r"(<[^>]+>)", fragment)
    )


def render(number: str, name: str, style: str, slides: list[dict]) -> str:
    total = len(slides)
    idx_num = [n for _, n, _ in LECTURES]
    pos = idx_num.index(number)
    prev_lec = LECTURES[pos - 1] if pos > 0 else None
    next_lec = LECTURES[pos + 1] if pos + 1 < len(LECTURES) else None
    parts = []
    for i, s in enumerate(slides, 1):
        cover = i == 1
        paras = "".join(f'<p class="dk-p">{wrap_prose(p)}</p>' for p in s["paras"])
        art = ""
        if cover and s["img"]:
            art = f'<img class="dk-art" src="{s["img"][0]}" alt="{s["img"][1]}">'
        diagram = ""
        if s["svg"]:
            cap = f'<p class="dk-caption">{html.escape(s["caption"])}</p>' if s["caption"] else ""
            # Re-create the original ancestor chain (display:contents) for CSS scoping.
            chain = [c for c in s["wrap"].split("|") if c]
            open_w = "".join(f'<div class="dk-wrap {c}">' for c in chain)
            close_w = "</div>" * len(chain)
            diagram = f'<figure class="dk-diagram"><p class="dk-pan-hint">도해를 좌우로 밀어 전체 흐름을 보세요.</p>{open_w}{s["svg"]}{close_w}{cap}</figure>'
        nxt = ""
        if s["next"] and len(text(s["next"])) > 2:
            if i == total and next_lec:
                nxt = f'<p class="dk-next"><b>다음 질문 · 강의 {next_lec[1]}</b><a href="{next_lec[0]}">{html.escape(text(s["next"]))}</a></p>'
            else:
                nxt = f'<p class="dk-next"><b>다음 질문</b>{html.escape(text(s["next"]))}</p>'
        elif i == total and next_lec:
            nxt = f'<p class="dk-next"><b>다음 강의</b><a href="{next_lec[0]}">강의 {next_lec[1]} · {next_lec[2]} →</a></p>'
        elif i == total:
            nxt = '<p class="dk-next"><b>마지막 장</b><a href="../index.html">강의 목록으로 →</a></p>'
        previous = f'<p class="dk-prev"><b>이어받은 질문</b>{html.escape(text(s["prev"]))}</p>' if s['prev'] else '<p class="dk-prev"><b>강의의 출발점</b>전체 흐름에서 현재 구간을 살펴봅니다.</p>'
        layout = "dk-cover" if cover else ("dk-main" if diagram else "dk-text")
        parts.append(
            f'<article class="dk-slide {layout}" id="s{i}" data-index="{i}" aria-label="{i} / {total}">'
            f'<header class="dk-head"><span class="dk-eyebrow">{html.escape(s["eyebrow"])}</span>'
            f'<span class="dk-count">{i:02d} / {total:02d}</span></header>'
            f'<h2 class="dk-title">{s["title"]}</h2>'
            f'<div class="dk-body">{diagram}<div class="dk-copy">{paras}{art}</div></div>'
            f'<footer class="dk-foot">{previous}{nxt}</footer></article>'
        )
    lec_links = "".join(
        f'<a href="{f}"{CURRENT if n == number else ""}>{n}</a>' for f, n, _ in LECTURES
    )
    prev_link = f'<a class="dk-lec" href="{prev_lec[0]}">← 강의 {prev_lec[1]}</a>' if prev_lec else ""
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{number} · {html.escape(name)}</title><link rel="icon" href="data:,">
<link rel="stylesheet" href="../assets/design-system.css">
<style>{style}</style>
<link rel="stylesheet" href="../assets/deck.css">
</head><body class="dk dk-course-{number}">
<div class="dk-viewport"><main class="dk-stage" id="deck" aria-label="강의 {number} · {html.escape(name)}">
<div class="dk-brand"><a href="../index.html">p-hermes</a><span>강의 {number} · {html.escape(name)}</span></div>
{''.join(parts)}
<div class="dk-progress"><span></span></div>
</main></div>
<nav class="dk-controls" aria-label="슬라이드 이동"><a class="dk-home" href="../index.html">강의 목록</a>{prev_link}<span class="dk-lecs">{lec_links}</span>
<button type="button" data-go="-1" aria-label="이전 슬라이드">←</button><span class="dk-live-count" aria-live="polite" aria-atomic="true"></span><button type="button" data-go="1" aria-label="다음 슬라이드">→</button>
<button type="button" data-fs aria-label="전체 화면 (F)">⛶</button></nav>
<script src="../assets/deck.js"></script>
</body></html>
"""


def build(source_dir: Path, out_dir: Path) -> list[Path]:
    written = []
    missing = [fname for fname, _, _ in LECTURES if not (source_dir / fname).is_file()]
    if missing:
        raise FileNotFoundError('필수 강의 원고 누락: ' + ', '.join(missing))
    out_dir.mkdir(parents=True, exist_ok=True)
    for fname, number, name in LECTURES:
        src = source_dir / fname
        style, slides = parse(src.read_text(encoding="utf-8"), number)
        out = out_dir / fname
        out.write_text(render(number, name, style, slides), encoding="utf-8")
        written.append(out)
    return written


if __name__ == "__main__":
    import sys

    root = Path(__file__).resolve().parents[1]
    for p in build(root / "site/lectures", root / "docs/lectures"):
        print(p)
    sys.exit(0)
