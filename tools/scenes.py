"""Shared visual grammar for lecture scenes: one map, fixed node positions, reusable parts.

Every lecture scene uses a 1000x540 viewBox. Lecture 01 draws the delegation
skeleton (user, manager, worker and the request/response lanes) at the same
coordinates on every slide, so moving between slides only changes the focus
and the detail drawn underneath. A small locator map in the top-right corner
shows where the slide sits in the whole system.
"""
from __future__ import annotations

from html import escape

# One style block (inline SVG <style> is document-global) carries the shared vocabulary.
STYLE = """<style>
#deck .dk-scene svg .u-box{fill:#1f2734;stroke:#e9eef7;stroke-width:2.2}
#deck .dk-scene svg .m-box{fill:#173a39;stroke:#82dec6;stroke-width:2.6}
#deck .dk-scene svg .w-box{fill:#1b2847;stroke:#9bc2ff;stroke-width:2.6}
#deck .dk-scene svg .doc{fill:#3a2f1c;stroke:#ffcf86;stroke-width:2}
#deck .dk-scene svg .doc-fold{fill:none;stroke:#ffcf86;stroke-width:2}
#deck .dk-scene svg .chip{fill:#1b2b3d;stroke:#6c839d;stroke-width:2}
#deck .dk-scene svg .chip.clf{fill:#2a2550;stroke:#b7a6ff}
#deck .dk-scene svg .card{fill:#16243a;stroke:#3d5571;stroke-width:1.6}
#deck .dk-scene svg .card.mint{fill:#173a39;stroke:#82dec6}
#deck .dk-scene svg .card.amber{fill:#3a2f1c;stroke:#ffcf86}
#deck .dk-scene svg .card.coral{fill:#3a2224;stroke:#ff9f8f}
#deck .dk-scene svg .card.blue{fill:#1b2847;stroke:#9bc2ff}
#deck .dk-scene svg .card.know{fill:#2b2a1e;stroke:#e8d9a8}
#deck .dk-scene svg .lane{fill:none;stroke:#879cb3;stroke-width:3}
#deck .dk-scene svg .lane.mint{stroke:#82dec6}
#deck .dk-scene svg .lane.amber{stroke:#ffcf86}
#deck .dk-scene svg .lane.blue{stroke:#9bc2ff}
#deck .dk-scene svg .lane.coral{stroke:#ff9f8f}
#deck .dk-scene svg .lane.dash{stroke-dasharray:8 7}
#deck .dk-scene svg .lead{fill:none;stroke:#5d7590;stroke-width:1.6;stroke-dasharray:3 5}
#deck .dk-scene svg .dim{opacity:.26}
#deck .dk-scene svg .person{fill:#e9eef7}
#deck .dk-scene svg text.right{text-anchor:end}
#deck .dk-scene svg text.t-sm{font-size:16px;font-weight:500;fill:#b9c7d8}
#deck .dk-scene svg text.t-md{font-size:20px}
#deck .dk-scene svg text.t-tag{font-size:15px;font-weight:700;fill:#c3d0e0}
#deck .dk-scene svg text.c-mint{fill:#82dec6}
#deck .dk-scene svg text.c-blue{fill:#9bc2ff}
#deck .dk-scene svg text.c-amber{fill:#ffcf86}
#deck .dk-scene svg text.c-coral{fill:#ff9f8f}
#deck .dk-scene svg text.c-violet{fill:#cfc4ff}
#deck .dk-scene svg .mini rect,#deck .dk-scene svg .mini circle{fill:#1b2b3d;stroke:#4a5f77;stroke-width:6}
#deck .dk-scene svg .mini .on{fill:#173a39;stroke:#82dec6;stroke-width:9}
#deck .dk-scene svg .mini .frame{fill:#0f1a27;stroke:#304357;stroke-width:6}
#deck .dk-scene svg .mini path{stroke:#4a5f77;stroke-width:6;fill:none}
#deck .dk-scene svg .mini path.on{stroke:#82dec6;fill:none}
#deck .dk-slide.is-active .dk-body:has(.dk-scene.mapped){animation:mo-fade .35s ease-out both}
</style>"""

MARKERS = ("mint", "#82dec6"), ("blue", "#9bc2ff"), ("amber", "#ffcf86"), ("coral", "#ff9f8f"), ("gray", "#879cb3")


def defs(p: str) -> str:
    marks = "".join(
        f'<marker id="{p}-{n}" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
        f'<path d="M0 0L9 4.5L0 9z" fill="{c}"/></marker>' for n, c in MARKERS)
    return f"<defs>{marks}</defs>"


def t(x, y, s, cls="", size=None, anchor=None) -> str:
    style = f' style="font-size:{size}px"' if size else ""
    if anchor:
        cls = f"{cls} {'left' if anchor == 'start' else 'right'}".strip()
    return f'<text x="{x}" y="{y}" class="{cls}"{style}>{escape(s)}</text>'


def lane(p, pid, d, color="gray", arrow=True, dash=False, draw=None, extra="") -> str:
    cls = f"lane {'' if color == 'gray' else color}{' dash' if dash else ''}"
    m = f' marker-end="url(#{p}-{color})"' if arrow else ""
    anim = f' class="{cls} mo-draw" pathLength="1" style="--d:{draw}"' if draw is not None else f' class="{cls}"'
    return f'<path id="{p}-{pid}" d="{d}"{anim}{m}{extra}/>'


def pkt(p, pid, color="", dur=2.4, delay=0.0, r=7) -> str:
    return f'<circle class="mo-pkt {color}" r="{r}" cx="-30" cy="-30" data-path="{p}-{pid}" data-dur="{dur}" data-delay="{delay}"/>'


def person(x, y) -> str:
    return f'<circle class="person" cx="{x}" cy="{y - 7}" r="7"/><path class="person" d="M{x - 12} {y + 13}a12 11 0 0 1 24 0z"/>'


def doc(x, y, w, h, title, sub="") -> str:
    f = 14
    body = (f'<path class="doc" d="M{x} {y}H{x + w - f}L{x + w} {y + f}V{y + h}H{x}Z"/>'
            f'<path class="doc-fold" d="M{x + w - f} {y}V{y + f}H{x + w}"/>')
    cy = y + h / 2
    if sub:
        return body + t(x + w / 2, cy - 10, title, "t-md") + t(x + w / 2, cy + 14, sub, "t-sm", 14)
    return body + t(x + w / 2, cy, title, "t-md")


def box(x, y, w, h, cls, title, sub="", size=None, sub_size=None) -> str:
    out = f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="14"/>'
    cy = y + h / 2
    if sub:
        return out + t(x + w / 2, cy - 13, title, "", size) + t(x + w / 2, cy + 17, sub, "t-sm", sub_size)
    return out + t(x + w / 2, cy, title, "", size)


def g(content: str, dim=False, build=None, cls="") -> str:
    attrs = ""
    classes = " ".join(c for c in ("dim" if dim else "", cls) if c)
    if classes:
        attrs += f' class="{classes}"'
    if build is not None:
        attrs += f' data-build="{build}"'
    return f"<g{attrs}>{content}</g>"


# ---------------------------------------------------------------- the whole-system map
# Region keys: user, mgr, wkr, lanes, rail, know.
def mini_map(on: set[str], x=826, y=4, scale=0.165) -> str:
    alias = {"lanes": {"lane_top", "lane_bot"}}
    focus = set()
    for k in on:
        focus |= alias.get(k, {k})
    return (f'<g class="mini-full" transform="translate({x} {y}) scale({scale})" aria-hidden="true">'
            f'<rect x="0" y="0" width="1000" height="900" rx="30" fill="#0f1a27" stroke="#304357" stroke-width="6"/>'
            f'{full_map("mm", focus, labels=False)}</g>')


# ---------------------------------------------------------------- lecture 01 skeleton
# Fixed coordinates shared by every lecture 01 scene.
U = (30, 18, 190, 76)          # user
M = (30, 186, 190, 156)        # manager
W = (790, 186, 180, 156)       # worker
TOP, BOT = 215, 312            # request lane / response lane


ENDPOINTS = {"u2m": {"user", "mgr"}, "direct": {"user", "wkr"}, "lane_top": {"mgr", "wkr"}, "lane_bot": {"mgr", "wkr"},
             "doc": {"mgr"}, "reg": {"lane_top"}, "runner": {"lane_top"}, "entry": {"wkr"}, "w2r": {"wkr", "entry"}}


def close_focus(focus: set[str]) -> set[str]:
    """A lit connector always lights both ends; a lit box never lights connectors by itself."""
    out = set(focus)
    for k in list(focus):
        out |= ENDPOINTS.get(k, set())
    return out


def skeleton(p: str, focus: set[str], packets: tuple = (), labels=True, detail=False) -> str:
    """User, manager, worker and the three paths; parts not in focus are dimmed.

    detail=True adds the registration and runner nodes on the request path (lecture 01 only).
    """
    focus = close_focus(focus)

    def on(k):
        return k in focus or "all" in focus
    ux, uy, uw, uh = U
    mx, my, mw, mh = M
    wx, wy, ww, wh = W
    out = []
    out.append(g(lane(p, "u2m", f"M95 {uy + uh}V{my - 6}", "mint" if on("u2m") else "gray")
                 + lane(p, "m2u", f"M155 {my}V{uy + uh + 6}", "mint" if on("u2m") else "gray")
                 + (t(84, 140, "요청", "t-tag", anchor="end") + t(166, 140, "보고", "t-tag", anchor="start") if labels else ""),
                 dim=not on("u2m")))
    tag = "t-tag c-blue" if on("direct") else "t-tag"
    out.append(g(lane(p, "direct", f"M{ux + uw} 44H940V{wy - 6}", "blue" if on("direct") else "gray", dash=True)
                 + lane(p, "reply", f"M810 {wy}V128H200V{uy + uh + 6}", "blue" if on("direct") else "gray", dash=True)
                 + (t(580, 30, "직접 요청", tag) + t(500, 146, "같은 대화로 답 · 응답서 없음", tag) if labels else ""),
                 dim=not on("direct")))
    hot = on("lane_top") or on("doc")
    if detail:
        segs = [("l1", 220, 243), ("l2", 335, 362), ("l3", 492, 520), ("l5", 650, 786)]
        lit = {"l1": hot, "l2": on("lane_top") or on("reg"), "l3": on("lane_top") or on("runner"), "l5": on("lane_top")}
        for pid, a_, b_ in segs:
            h = lit[pid]
            out.append(g(lane(p, pid, f"M{a_} {TOP}H{b_}", "amber" if h else "gray"), dim=not h))
        out.append(g(doc(245, TOP - 32, 90, 64, "요청서"), dim=not hot))
        out.append(g(box(365, TOP - 32, 127, 64, "chip", "요청 등록", "ID 발급", 20, 14), dim=not (on("reg") or hot)))
        out.append(g(box(522, TOP - 32, 128, 64, "chip", "작업 실행기", "실행·시간 제한", 19, 14), dim=not (on("runner") or hot)))
    else:
        full = on("lane_top")
        out.append(g(lane(p, "l1", f"M220 {TOP}H406", "amber" if hot else "gray") + doc(410, TOP - 32, 90, 64, "요청서"), dim=not hot))
        out.append(g(lane(p, "l5", f"M500 {TOP}H786", "amber" if full else "gray"), dim=not full))
    hot = on("lane_bot")
    out.append(g(lane(p, "r1", f"M{wx} {BOT}H636", "amber" if hot else "gray")
                 + lane(p, "r2", f"M540 {BOT}H{mx + mw + 4}", "amber" if hot else "gray")
                 + doc(542, BOT - 32, 92, 64, "응답서", "같은 ID·상태"), dim=not hot))
    out.append(g(f'<rect class="u-box" x="{ux}" y="{uy}" width="{uw}" height="{uh}" rx="14"/>' + person(68, 56)
                 + t(140, 57, "사용자", "", 25), dim=not on("user")))
    out.append(g(box(mx, my, mw, mh, "m-box", "매니저", "판단·위임·판정", 27, 16), dim=not on("mgr")))
    out.append(g(box(wx, wy, ww, wh, "w-box", "워커", "실행", 27, 16), dim=not on("wkr")))
    out.extend(packets)
    return "".join(out)


def scene(p: str, body: str, label: str, on_map=("mgr", "wkr", "lanes", "user"), mobile="", caption="", mini=True) -> str:
    cap = f'<figcaption class="dk-caption">{escape(caption)}</figcaption>' if caption else ""
    return (f'<figure class="scene mapped"><svg viewBox="0 0 1000 540" role="img" aria-label="{escape(label)}">'
            f'{defs(p)}{body}{mini_map(set(on_map)) if mini else ""}</svg>{mobile}{cap}</figure>')


# ---------------------------------------------------------------- the canonical whole-system map (1000 x 900)
# Top band (y 0-345) is exactly the lecture 01 skeleton; lecture scenes are crops/zooms of this map.
# Region keys for focus: user, mgr, wkr, u2m, direct, lane_top, lane_bot, doc, reg, runner, clf,
# entry, rail, gates, job, know, all.
MAP_W, MAP_H = 1000, 900


def full_map(p: str, focus: set[str], labels=True) -> str:
    focus = close_focus(focus)
    on = lambda k: "all" in focus or k in focus
    out = [skeleton(p, focus, labels=labels)]
    wf = on("entry") or on("rail") or on("job") or on("gates")
    out.append(g('<rect x="20" y="380" width="960" height="196" rx="18" fill="#122436" stroke="#33506a" stroke-width="2" stroke-dasharray="8 6"/>'
                 + (t(966, 562, "작업 흐름", "t-tag", anchor="end") if labels else ""), dim=not wf))
    out.append(g(box(40, 432, 170, 60, "chip", "기록이 필요한가?", "세 질문", 18, 13), dim=not on("entry")))
    stops = [(310, "요청"), (490, "실행"), (670, "검증"), (850, "완료")]
    out.append(g(lane(p, "rail", "M214 462H930", "gray", arrow=False)
                 + "".join(f'<circle cx="{x}" cy="462" r="30" class="box"/>' + t(x, 463, s_, "", 17) for x, s_ in stops), dim=not on("rail")))
    out.append(g("".join(f'<rect x="{x - 5}" y="444" width="10" height="36" rx="3" fill="#ffcf86"/>' for x in (400, 580, 760)), dim=not (on("rail") or on("gates"))))
    out.append(g(lane(p, "w2r", "M880 342V404H125V428", "blue", dash=True)
                 + (t(500, 420, "워커가 일을 진행 — 기록이 필요하면 JOB으로 이 단계를 지난다", "t-sm", 15) if labels else ""),
                 dim=not (on("entry") or on("w2r"))))
    out.append(g('<path class="lead" d="M310 492V514M490 492V514M670 492V514M850 492V514"/>'
                 + '<rect class="card" x="260" y="514" width="640" height="48" rx="10"/>'
                 + t(580, 538, "JOB 폴더 — 요청 원문 · 승인 · 결정 · 실행 · 검증 · 결과 · 원본", "t-sm", 15), dim=not on("job")))
    # one connector between the whole knowledge block and everything above it
    kc = ('<rect x="40" y="590" width="920" height="40" rx="20" fill="#1e2a3a" stroke="#4a5f77" stroke-width="1.6"/>'
          + (t(500, 611, "⇅  지식 전체 ↔ 에이전트와 작업 흐름 전체 — 필요한 지식을 읽고, 결과와 교훈을 남긴다", "t-sm", 15) if labels else ""))
    out.append(g(kc, dim=not (on("know") or on("kconn"))))
    # finer keys light one knowledge card (k_rule ... k_real) or the daily strip (kloop); "know" lights all
    cards = [("k_rule", 50, "규칙", "운영 원칙"), ("k_mem", 236, "기억", "사용자 선호"), ("k_skill", 422, "스킬", "절차"),
             ("k_lesson", 608, "교훈", "사건·해결"), ("k_real", 794, "실물", "현재 파일")]
    any_k = on("know") or on("kloop") or any(on(k) for k, *_ in cards)
    out.append(g('<rect x="20" y="640" width="960" height="236" rx="18" fill="#141f33" stroke="#3a4a66" stroke-width="2"/>'
                 + (t(966, 860, "지식", "t-tag c-amber", anchor="end") if labels else ""), dim=not any_k))
    for k, x, h, s_ in cards:
        out.append(g(f'<rect class="card know" x="{x}" y="690" width="156" height="80" rx="12"/>' + t(x + 78, 718, h, "", 20)
                     + t(x + 78, 748, s_, "t-sm", 14), dim=not (on("know") or on(k))))
    strip = '<rect x="50" y="792" width="900" height="44" rx="10" fill="#2b2a1e" fill-opacity=".45" stroke="#e8d9a8" stroke-width="2.4" stroke-dasharray="8 5"/>'
    if labels:
        strip += t(500, 815, "매일 — 수집 → 가공·색인 → 야간 대조 → 점검", "t-sm", 15)
    out.append(g(strip, dim=not (on("know") or on("kloop"))))
    return "".join(out)


def map_svg(p: str, focus: set[str], labels=True, cls="") -> str:
    return (f'<svg class="{cls}" viewBox="0 0 {MAP_W} {MAP_H}" role="img" aria-label="전체 지도">'
            f'{defs(p)}{full_map(p, focus, labels)}</svg>')
