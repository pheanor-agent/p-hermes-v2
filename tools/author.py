"""Author lectures 00-04 from the locked storyboard (tools/storyboard.py).

The storyboard is the single source for slide order, titles and the question each
slide answers; this file adds the eyebrow, the spoken copy and the scene. A slide's
'next question' is always the question of the slide that follows it, so the chain
in the deck matches the storyboard by construction. Scenes are crops of the one
canonical map in tools/scenes.py. A few figures, examples and simulators are kept
from the previous lectures (read from git revision OLD_REV, not from the files this
script overwrites).

Run: python3 tools/author.py  (then make build)
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

import scenes as S
import storyboard as SB
import author_01 as A1
from scenes import t, lane, pkt, g, box, doc, skeleton, scene, person

ROOT = Path(__file__).resolve().parents[1]
OLD_REV = "d667578"
FILES = {"00": "00-overview.html", "01": "01-orchestrator-worker.html", "02": "02-workflow.html",
         "03": "03-knowledge.html", "04": "04-integration.html"}
NAMES = {"00": "전체 그림", "01": "매니저와 워커", "02": "작업 흐름", "03": "지식", "04": "통합"}
VIA, DIRECT, TOP = SB.VIA, SB.DIRECT, SB.TOP


# ------------------------------------------------------------------ old material
_old: dict[str, str] = {}


def old(num: str) -> str:
    if num not in _old:
        _old[num] = subprocess.run(["git", "show", f"{OLD_REV}:site/lectures/{FILES[num]}"], cwd=ROOT,
                                   capture_output=True, text=True, check=True).stdout
    return _old[num]


def old_section(num: str, key: str) -> str:
    m = re.search(rf'<section class="slide"[^>]*data-slide-key="{key}"[^>]*>(.*?)</section>', old(num), re.S)
    if not m:
        raise KeyError(key)
    return m.group(1)


def old_fig(num: str, key: str) -> str:
    return re.search(r'<figure class="scene.*?</figure>', old_section(num, key), re.S).group(0)


def old_sim(num: str, key: str) -> str:
    return re.search(r'<div data-sim="[^"]+"[^>]*></div>', old_section(num, key)).group(0)


# ------------------------------------------------------------------ drawing helpers
def card(x, y, w, h, cls, title, subs=(), tsize=None, ssize=16, tcls="t-md", build=None, gap=26):
    if isinstance(subs, str):
        subs = (subs,)
    n = len(subs)
    top = y + h / 2 - (n * gap) / 2 - (4 if n else 0)
    out = f'<rect class="card {cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="12"/>'
    out += t(x + w / 2, top if n else y + h / 2, title, tcls, tsize)
    for i, s in enumerate(subs):
        out += t(x + w / 2, top + (i + 1) * gap, s, "t-sm", ssize)
    return g(out, build=build) if build is not None else out


def lead(d):
    return f'<path class="lead" d="{d}"/>'


def pulse(x, y, w, h, color="", rx=12):
    return f'<rect class="mo-pulse {color}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/>'


def mobile(*nodes, flow=False):
    return A1.mobile(*nodes, flow=flow)


def fig(p, body, label, view="0 0 1000 540", mob="", extra_defs=()):
    defs = S.defs(p) + "".join(S.defs(q) for q in extra_defs)
    return (f'<figure class="scene mapped"><svg viewBox="{view}" role="img" aria-label="{label}">'
            f'{defs}{body}</svg>{mob}</figure>')


KCYC = "M115 722H875V782H115Z"   # loop through the knowledge cycle nodes (map coordinates)


def map_layer(p, focus, extra="", labels=True):
    return S.full_map(p, focus, labels) + extra


def veils(top=0, wf=1, kn=2):
    """Veils over the three bands of the map, faded out in order (map coordinates)."""
    out = ""
    for y, h, d in ((0, 360, top), (360, 226, wf), (586, 314, kn)):
        if d is not None:
            out += f'<rect class="mo-unveil" x="0" y="{y}" width="1000" height="{h}" style="--d:{d}"/>'
    return out


def band(p, focus, top, height, extra=""):
    """Crop of the canonical map: map y=top is drawn at y=0 and clipped to `height`."""
    return (f'<clipPath id="{p}-clip"><rect x="0" y="0" width="1000" height="{height}"/></clipPath>'
            f'<g clip-path="url(#{p}-clip)"><g transform="translate(0 {-top})">{S.full_map(p, focus)}{extra}</g></g>')


WF_TOP, WF_H = 370, 216        # workflow band crop
KN_TOP, KN_H = 584, 300        # knowledge band crop


def wf(p, focus, extra=""):
    return band(p, focus, WF_TOP, WF_H, extra)


def kn(p, focus, extra=""):
    return band(p, focus, KN_TOP, KN_H, extra)


def kloop(p, dur=7.0):
    return f'<path id="{p}-kcyc" d="{KCYC}" fill="none" stroke="none"/>' + pkt(p, "kcyc", "", dur, .3, 8)


def via_packets(p):
    return (pkt(p, "u2m", "", 1.2, .2), pkt(p, "l1", "amber", .8, 1.4), pkt(p, "l5", "amber", 1.0, 2.2),
            pkt(p, "r1", "amber", 1.0, 3.4), pkt(p, "r2", "amber", 1.1, 4.4), pkt(p, "m2u", "", 1.2, 5.5))


def direct_packets(p, base=0.0):
    return (pkt(p, "direct", "blue", 2.4, base + .2), pkt(p, "reply", "blue", 2.4, base + 3.0))


# ------------------------------------------------------------------ lecture 00
def s00_cover():
    p = "o1"
    extra = "".join(via_packets(p)) + "".join(direct_packets(p, 1.0)) + kloop(p)
    body = map_layer(p, {"all"}, extra) + veils()
    return fig(p, body, "역할, 작업 흐름, 지식 세 층으로 그린 전체 지도. 요청은 매니저를 거치거나 워커에게 직접 간다",
               view="0 0 1000 900", mob=mobile("위: 역할", "가운데: 작업 흐름", "아래: 지식"))


def s00_example():
    p = "o3"
    cells = []
    for i in range(200):
        r, c = divmod(i, 20)
        x, y = 40 + c * 19, 92 + r * 25
        cls = "card amber" if i < 3 else "card"
        cells.append(f'<rect class="{cls}" x="{x}" y="{y}" width="15" height="19" rx="3"/>')
    ship = "".join(f'<rect class="card mint" x="{40 + (i % 20) * 19}" y="{92 + (i // 20) * 25}" width="15" height="19" rx="3"/>'
                   for i in range(3, 200, 5))
    body = t(40, 70, "문의.csv · 200행", "t-tag", anchor="start") + "".join(cells)
    body += lane(p, "a1", "M420 104H478", "amber") + pkt(p, "a1", "amber", 1.0, .4)
    body += card(482, 70, 200, 180, "amber", "맥락 창", ("배송 지연", "결제 오류", "배송 누락"), ssize=17, gap=30)
    body += lane(p, "a2", "M686 160H738", "amber")
    body += card(742, 96, 220, 128, "coral", "요약", ("배송 문의 2/3", "모델이 읽은 3행만"), tsize=22, ssize=17, gap=30)
    body += g(ship + card(40, 380, 920, 130, "mint", "200행을 모두 세면 — 배송 40건, 20%",
                         ("모델은 맥락 창에 들어오지 않은 197행을 알지 못한다",), tsize=26, ssize=18, gap=34), build=1)
    return fig(p, body, "200행 가운데 3행만 맥락 창에 들어가 요약이 2/3가 되지만 전체를 세면 20%다",
               mob=mobile("200행 중 3행만 읽음", "요약: 배송 문의 2/3", "전체: 배송 40건 · 20%"))


def s00_break():
    p = "o4"
    body = '<rect class="card blue" x="40" y="60" width="600" height="120" rx="14"/>' + t(60, 84, "세션 1", "t-tag c-blue", anchor="start")
    for k in range(9):
        x = 60 + k * 62
        body += f'<g class="mo-rise" style="--d:{k + 1}"><rect class="chip" x="{x}" y="104" width="54" height="56" rx="8"/>{t(x + 27, 132, "로그", "t-sm", 14)}</g>'
    body += g('<path d="M652 50L672 90L652 130L672 170L652 200" fill="none" stroke="#ff9f8f" stroke-width="4"/>'
              + t(662, 222, "끊김", "t-tag c-coral"), cls="mo-rise", )
    body += '<rect class="card" x="700" y="60" width="260" height="120" rx="14"/>' + t(720, 84, "세션 2", "t-tag", anchor="start")
    body += t(830, 132, "무엇을 하던 중이었지?", "t-md c-coral", 20)
    items = [(40, "목표가 밀려남", ("로그가 쌓일수록", "처음 목표가 창 밖으로")),
             (360, "진행 상태가 묻힘", ("어디까지 했는지가", "긴 대화 속에 흩어짐")),
             (680, "다음 세션은 처음부터", ("세션 기록이 남아도", "무엇부터 읽을지 모름"))]
    for k, (x, h, s) in enumerate(items, 1):
        body += card(x, 300, 280, 150, "coral", h, s, ssize=17, build=k)
    return fig(p, body, "세션 1의 로그가 쌓이다 끊기고, 세션 2는 무엇을 하던 중이었는지 모른다",
               mob=mobile("로그가 목표를 밀어냄", "진행 상태가 묻힘", "다음 세션은 처음부터"))


def s00_files():
    p = "o5"
    body = card(40, 150, 200, 120, "blue", "세션 1", ("일을 하다 끊김",), ssize=16)
    body += '<rect x="300" y="60" width="400" height="300" rx="18" fill="none" stroke="#ffcf86" stroke-width="2" stroke-dasharray="8 6"/>'
    body += t(500, 86, "대화 밖 · 파일", "t-tag c-amber")
    for k, (y, title, sub) in enumerate(((112, "요청서", "무엇을 · 어디까지"), (196, "JOB 폴더", "결정 · 실행 · 검증"), (280, "응답서", "결과 · 상태")), 1):
        body += g(doc(390, y, 220, 64, title, sub), build=k)
    body += lane(p, "w", "M242 210H384", "amber") + pkt(p, "w", "amber", 1.0, .3)
    body += g(lane(p, "r", "M616 210H756", "mint") + pkt(p, "r", "", 1.0, .2)
              + card(760, 150, 200, 120, "mint", "세션 2", ("파일부터 읽고 이어 감",), ssize=16), build=4)
    body += g(card(40, 410, 920, 100, "", "누가, 언제 읽어도 같은 내용", ("약속(요청)과 결과를 다시 대조할 수 있다",), tsize=24, ssize=18, gap=30), build=4)
    return fig(p, body, "세션 1이 요청서·JOB 폴더·응답서를 대화 밖 파일로 남기고 세션 2가 그 파일부터 읽는다",
               mob=mobile("세션 1이 파일로 남김", "요청서 · JOB · 응답서", "세션 2가 읽고 이어 감", flow=True))


def s00_layers():
    p = "o6"
    extra = kloop(p) + "".join(via_packets(p))
    body = f'<g transform="translate(0 0) scale(.6)">{map_layer(p, {"all"}, extra)}{veils()}</g>'
    rows = [(10, 196, "mint", "위 · 역할", ("누가 판단하고", "누가 실행하나")),
            (226, 124, "blue", "가운데 · 작업 흐름", ("기록이 필요한 일이", "지나는 단계")),
            (360, 170, "know", "아래 · 지식", ("다음 일에 읽히고", "다시 남는 기록"))]
    for k, (y, h, c, head, s) in enumerate(rows):
        body += g(lead(f"M604 {y + h / 2}H636") + card(640, y, 340, h, c, head, s, ssize=17), build=k + 1)
    return fig(p, body, "전체 지도를 위 역할, 가운데 작업 흐름, 아래 지식의 세 층으로 나눠 본다",
               mob=mobile("위: 역할", "가운데: 작업 흐름", "아래: 지식"))


def two_way(pa, pb, top_note=True):
    """The same skeleton twice: way A (via manager) and way B (direct), crossfading."""
    a = skeleton(pa, VIA, via_packets(pa))
    b = skeleton(pb, DIRECT, direct_packets(pb))
    tags = (g(f'<rect x="300" y="250" width="220" height="40" rx="20" fill="#173a39" stroke="#82dec6"/>' + t(410, 271, "① 매니저에게 맡기기", "t-tag c-mint"), cls="mo-alt-a")
            + g(f'<rect x="300" y="250" width="220" height="40" rx="20" fill="#1b2847" stroke="#9bc2ff"/>' + t(410, 271, "② 워커에게 직접", "t-tag c-blue"), cls="mo-alt-b"))
    return g(a, cls="mo-alt-a") + g(b, cls="mo-alt-b") + (tags if top_note else "")


def s00_entry():
    pa, pb = "oea", "oeb"
    body = two_way(pa, pb)
    for x, c, cls, head, s in ((40, "mint", "mo-alt-a", "① 매니저에게 맡기기", ("매니저가 판단해 요청서로 넘기고", "응답서를 받아 판정한다")),
                               (520, "blue", "mo-alt-b", "② 워커에게 직접 맡기기", ("워커가 판단부터 실행까지 하고", "같은 대화로 답한다"))):
        body += card(x, 386, 440, 140, "", head, s, ssize=17)
        body += g(f'<rect x="{x}" y="386" width="440" height="140" rx="12" fill="none" stroke="{"#82dec6" if c == "mint" else "#9bc2ff"}" stroke-width="3.5"/>', cls=cls)
    return fig(pa, body, "같은 골격에서 매니저를 거치는 길과 워커에게 직접 가는 길이 번갈아 재생된다", extra_defs=(pb,),
               mob=mobile("① 매니저에게: 요청서 · 응답서", "② 워커에게 직접: 같은 대화로 답"))


def s00_manager():
    p = "o7"
    body = skeleton(p, {"user", "mgr", "u2m"}, (pkt(p, "u2m", "", 1.2, .3), pkt(p, "m2u", "", 1.2, 2.0)))
    body += pulse(30, 186, 190, 156)
    items = [(40, "mint", "판단", ("무엇을 할지,", "누가 할지 정한다")), (360, "amber", "맡김", ("오래 걸리는 실행은", "요청서 한 장으로")),
             (680, "blue", "판정", ("돌아온 결과를", "실물과 대조한다"))]
    for k, (x, c, h, s) in enumerate(items, 1):
        body += g(lead(f"M125 342C125 370 {x + 140} 360 {x + 140} 396") + card(x, 396, 280, 128, c, h, s, ssize=17), build=k)
    return scene(p, body, "매니저는 판단하고, 맡기고, 판정한다", on_map=("user", "mgr"),
                 mobile=mobile("판단", "맡김", "판정", flow=True))


def s00_workflow():
    p = "o8"
    body = wf(p, {"wkr", "entry", "rail", "job"}, pkt(p, "rail", "amber", 4.0, .4))
    body += t(500, 236, "단계마다 남는 기록", "t-tag c-amber")
    stops = [(310, "요청", ("요청 원문", "승인")), (490, "실행", ("결정", "실행 기록")), (670, "검증", ("확인한 결과",)), (850, "완료", ("결과 보고", "남은 일"))]
    for k, (x, s, subs) in enumerate(stops, 1):
        body += g(lead(f"M{x} 214V262") + card(x - 84, 262, 168, 126, "amber", s, subs, ssize=16), build=k)
    body += g(card(30, 262, 220, 126, "", "아니오면", ("JOB 없이", "바로 처리"), ssize=16) + lead("M125 214V262"), build=1)
    body += g(card(30, 420, 940, 96, "", "기록이 필요한 일만 JOB이 되어 이 단계를 지난다", ("누가 일하든 같은 순서와 같은 조건",), tsize=23, ssize=17, gap=30), build=5)
    return fig(p, body, "가운데 띠: 기록이 필요한 일은 요청, 실행, 검증, 완료를 지나며 단계마다 기록을 남긴다",
               mob=mobile("기록이 필요한가?", "요청 → 실행 → 검증 → 완료", "단계마다 기록", flow=True))


def s00_knowledge():
    p = "o9"
    body = kn(p, {"know", "kconn"}, kloop(p))
    items = [(30, "일을 시작할 때", ("원칙과 이번 일에 맞는", "기록을 읽는다")), (350, "일하는 동안", ("찾은 기록이 지금도", "맞는지 확인한다")),
             (670, "일을 마치면", ("겪은 일을", "다시 기록으로 남긴다"))]
    for k, (x, h, s) in enumerate(items, 1):
        body += card(x, 340, 300, 140, "know", h, s, ssize=17, build=k)
    return fig(p, body, "아래 띠: 지식은 작업, 기록, 축적, 활용, 확인으로 돈다",
               mob=mobile("작업", "기록", "축적", "활용", "확인", flow=True))


def mini_rail(x, y, hot=2):
    out = f'<path d="M{x} {y}H{x + 330}" stroke="#879cb3" stroke-width="3"/>'
    for k, s in enumerate(("요청", "실행", "검증", "완료")):
        cx = x + 20 + k * 100
        cls = "card mint" if k == hot else "box"
        out += f'<circle class="{cls}" cx="{cx}" cy="{y}" r="24"/>' + t(cx, y + 1, s, "", 15)
    return out


def s00_verify():
    p = "o10"
    body = skeleton(p, {"lane_bot", "mgr", "wkr"}, (pkt(p, "r1", "amber", 1.0, .4), pkt(p, "r2", "amber", 1.2, 1.4)))
    body += pulse(542, 280, 92, 64, "amber", 6)
    body += g(f'<rect class="card mint" x="40" y="380" width="440" height="148" rx="14"/>'
              + t(260, 408, "① 일한 쪽의 검증", "t-md c-mint") + mini_rail(95, 452)
              + t(260, 500, "직접 맡든 요청서로 맡든, 일한 쪽이 실물과 대조", "t-sm", 15), build=1)
    body += g(card(520, 380, 440, 148, "amber", "② 맡긴 쪽의 판정", ("요청서로 맡긴 경우에만", "매니저가 응답서를 실물과 다시 대조"), ssize=16, gap=28)
              + lead("M588 346V378"), build=2)
    return scene(p, body, "확인은 두 겹: 일한 쪽의 검증 단계와, 맡긴 경우 매니저의 응답서 판정", on_map=("mgr", "lanes", "rail"),
                 mobile=mobile("① 일한 쪽의 검증", "② 맡긴 경우 매니저의 판정"))


def lecture_bands(p, packets=True):
    extra = kloop(p) if packets else ""
    body = map_layer(p, {"all"}, extra)
    rings = [(8, 6, 984, 346, "강의 01 · 역할"), (14, 374, 972, 208, "강의 02 · 작업 흐름"), (14, 584, 972, 298, "강의 03 · 지식")]
    for k, (x, y, w, h, label) in enumerate(rings, 1):
        body += g(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="20" fill="none" stroke="#82dec6" stroke-width="5"/>'
                  + f'<rect x="{x + w - 250}" y="{y + 8}" width="236" height="40" rx="20" fill="#173a39" stroke="#82dec6" stroke-width="2"/>'
                  + t(x + w - 132, y + 29, label, "t-tag c-mint", 19), build=k)
    body += g('<rect x="2" y="2" width="996" height="896" rx="24" fill="none" stroke="#ffcf86" stroke-width="6"/>'
              + '<rect x="372" y="852" width="256" height="40" rx="20" fill="#3a2f1c" stroke="#ffcf86" stroke-width="2"/>'
              + t(500, 873, "강의 04 · 요청 하나로 잇기", "t-tag c-amber", 19), build=4)
    return body


def s00_next():
    p = "o11"
    return fig(p, lecture_bands(p), "지도의 위 띠는 강의 01, 가운데 띠는 강의 02, 아래 띠는 강의 03, 전체는 강의 04가 맡는다",
               view="0 0 1000 900", mob=mobile("01 역할", "02 작업 흐름", "03 지식", "04 통합", flow=True))


# ------------------------------------------------------------------ lecture 01
def s01_modes():
    pa, pb = "m4a", "m4b"
    body = two_way(pa, pb)
    rows = [("판단", "매니저", "워커"), ("실행", "워커", "워커"), ("주고받는 것", "요청서 · 응답서", "없음"), ("답", "매니저가 판정 후 보고", "같은 대화로 바로")]
    body += '<rect class="card" x="40" y="362" width="920" height="170" rx="14"/>'
    body += t(450, 382, "① 매니저에게", "t-tag c-mint") + t(780, 374, "② 워커에게 직접", "t-tag c-blue")
    for k, (h, a, b) in enumerate(rows):
        y = 414 + k * 30
        body += t(150, y, h, "t-sm", 17) + t(450, y, a, "t-sm", 17) + t(780, y, b, "t-sm", 17)
    body += g('<rect x="300" y="366" width="300" height="162" rx="10" fill="none" stroke="#82dec6" stroke-width="3"/>', cls="mo-alt-a")
    body += g('<rect x="630" y="366" width="300" height="162" rx="10" fill="none" stroke="#9bc2ff" stroke-width="3"/>', cls="mo-alt-b")
    return fig(pa, body, "매니저에게 맡기는 길과 워커에게 직접 맡기는 길이 번갈아 재생되고, 판단·실행·주고받는 것·답이 어떻게 다른지 표로 비교한다",
               extra_defs=(pb,), mob=mobile("① 매니저에게: 판단은 매니저, 요청서 · 응답서", "② 워커에게 직접: 판단도 워커, 같은 대화로 답"))


def s01_user_choice():
    p = "m7"
    body = skeleton(p, {"user", "u2m", "direct"}, (pkt(p, "u2m", "", 1.2, .3), pkt(p, "direct", "blue", 2.2, .3)))
    body += pulse(30, 18, 190, 76, "", 14)
    body += g(lead("M125 342V384") + card(40, 384, 440, 144, "mint", "매니저에게", ("어렵거나 창의적인 일", "여러 단계에 걸치는 일", "결과를 따로 확인해야 하는 일"), ssize=17, gap=28), build=1)
    body += g(lead("M880 342V384") + card(520, 384, 440, 144, "blue", "워커에게 직접", ("간단한 일", "되돌릴 수 있는 일", "결과를 바로 볼 수 있는 일"), ssize=17, gap=28), build=2)
    return scene(p, body, "사용자는 간단하고 되돌릴 수 있는 일은 워커에게 직접, 어렵거나 창의적인 일은 매니저에게 맡긴다",
                 on_map=("user", "mgr", "wkr"), mobile=mobile("어렵거나 창의적 → 매니저", "간단하고 되돌릴 수 있음 → 워커"))


def weight(x, y, n, color):
    return "".join(f'<rect x="{x}" y="{y - k * 16}" width="70" height="12" rx="4" fill="{color}"/>' for k in range(n))


def s01_model_weight():
    p = "m8"
    body = skeleton(p, {"mgr", "wkr"}, labels=False)
    body += g(lead("M125 342V384") + '<rect class="card mint" x="40" y="384" width="440" height="144" rx="14"/>'
              + weight(70, 490, 4, "#82dec6") + t(300, 420, "무거운 모델 → 매니저", "t-md c-mint")
              + t(300, 456, "판단과 대화가 깊어", "t-sm", 17) + t(300, 484, "주고받기가 쾌적하다", "t-sm", 17), build=1)
    body += g(lead("M880 342V384") + '<rect class="card blue" x="520" y="384" width="440" height="144" rx="14"/>'
              + weight(550, 490, 1, "#9bc2ff") + t(780, 420, "가벼운 모델 → 워커", "t-md c-blue")
              + t(780, 456, "정해진 일을 길게 실행해도", "t-sm", 17) + t(780, 484, "비용이 적게 든다", "t-sm", 17), build=2)
    return scene(p, body, "판단을 맡는 매니저에는 무거운 모델, 실행을 맡는 워커에는 가벼운 모델", on_map=("mgr", "wkr"),
                 mobile=mobile("무거운 모델 → 매니저: 대화가 쾌적", "가벼운 모델 → 워커: 비용 절약"))


def s01_request():
    p = "m10"
    body = skeleton(p, {"mgr", "doc", "l1"}, (pkt(p, "l1", "amber", .8, .3),))
    body += pulse(410, 183, 90, 64, "amber", 6)
    body += lead("M410 247L60 398M500 247L940 398")
    body += '<rect class="card amber" x="40" y="398" width="920" height="128" rx="14"/>'
    fields = [("목표", "무엇을 끝낼지", "mint"), ("완성 기준", "어떻게 확인할지", ""), ("참조 경로", "무엇을 읽을지", ""), ("금지 범위", "무엇은 하지 않을지", "coral")]
    for k, (h, s, c) in enumerate(fields):
        x = 58 + k * 226
        body += card(x, 414, 210, 76, c, h, s, ssize=16, build=k + 1)
    body += t(500, 510, "사용자가 말하지 않은 범위 축소나 요청과 무관한 일은 넣지 않는다", "t-sm c-coral", 15)
    return scene(p, body, "요청서를 펼친 네 칸: 목표, 완성 기준, 참조 경로, 금지 범위", on_map=("mgr", "lanes"),
                 mobile=mobile("목표", "완성 기준", "참조 경로", "금지 범위"))


def s01_promise():
    p = "m11"
    body = skeleton(p, {"doc", "lane_top", "lane_bot"}, (pkt(p, "l5", "amber", 1.0, .3), pkt(p, "r1", "amber", 1.0, 2.0)))
    body += '<rect class="card amber" x="40" y="378" width="640" height="150" rx="14"/>' + t(60, 400, "요청서 · 요청 ID R-예시-01", "t-tag c-amber", anchor="start")
    rows = [("목표", "무엇을 끝낼지"), ("완성 기준", "어떻게 확인할지"), ("참조 경로", "무엇을 읽을지"), ("금지 범위", "무엇은 하지 않을지")]
    for k, (h, s) in enumerate(rows):
        x, y = 60 + (k % 2) * 310, 420 + (k // 2) * 52
        body += g(f'<rect class="card" x="{x}" y="{y}" width="290" height="44" rx="8"/>' + t(x + 16, y + 22, h, "t-tag c-amber", anchor="start")
                  + t(x + 274, y + 22, s, "t-sm", 15, anchor="end"), build=k + 1)
    body += g(lead("M588 346V378") + card(720, 378, 240, 150, "mint", "응답서가 오면", ("이 네 약속과", "하나씩 대조한다"), ssize=17), build=5)
    body += lead("M455 247V376")
    return scene(p, body, "요청 ID가 붙은 요청서의 네 칸은 각각 하나의 약속이고, 돌아온 응답서는 그 약속과 대조한다",
                 on_map=("lanes",), mobile=mobile("목표: 무엇을 끝낼지", "완성 기준: 어떻게 확인할지", "참조 경로: 무엇을 읽을지", "금지 범위: 하지 않을 것"))


def s01_approval():
    return A1.s_approval().replace("POLICY 개정", "원칙 개정")


def s01_register():
    return A1.s_register()


# ------------------------------------------------------------------ lecture 02
def s02_cover():
    p = "w1"
    extra = (lane(p, "fast", "M125 492V528H236", "blue", dash=True) + t(40, 556, "바로 처리 · 기록 없이", "t-sm c-blue", 15, anchor="start")
             + pkt(p, "fast", "blue", 1.6, .6) + pkt(p, "rail", "amber", 4.0, 1.8))
    body = wf(p, {"entry", "rail", "job"}, extra)
    body += g(card(40, 250, 440, 150, "blue", "바로 처리", ("짧고 되돌릴 수 있는 일", "결과만 확인하고 끝낸다"), ssize=17), build=1)
    body += g(card(520, 250, 440, 150, "amber", "JOB으로 기록", ("여러 단계에 걸치는 일", "단계마다 기록을 남긴다"), ssize=17), build=2)
    body += g(t(500, 450, "일을 하는 쪽이 이 갈림길에서 고른다 — 매니저든 워커든", "t-md", 21), build=3)
    return fig(p, body, "작업 흐름의 입구에서 일은 바로 처리하는 길과 JOB으로 기록하는 길로 나뉜다",
               mob=mobile("바로 처리: 기록 없이", "JOB: 단계마다 기록"))


def s02_three():
    p = "w2"
    body = wf(p, {"entry"})
    body += pulse(40, 62, 170, 60)
    qs = ["여러 단계에 걸치는가?", "나중에 되돌아볼 수 있는가?", "다음 작업의 근거가 되는가?"]
    for k, q in enumerate(qs):
        body += g(f'<rect class="card" x="40" y="{240 + k * 70}" width="520" height="58" rx="10"/>' + t(64, 269 + k * 70, f"{k + 1}. {q}", "t-md", 21, anchor="start"), build=k + 1)
    body += g(lead("M566 300H600") + card(604, 236, 356, 100, "amber", "하나라도 예", ("JOB으로 기록",), ssize=18), build=4)
    body += g(lead("M566 410H600") + card(604, 360, 356, 100, "blue", "모두 아니오", ("바로 처리",), ssize=18), build=5)
    return fig(p, body, "세 질문 가운데 하나라도 예이면 JOB으로 기록하고, 모두 아니오면 바로 처리한다",
               mob=mobile("여러 단계에 걸치나?", "되돌아볼 수 있나?", "다음 작업의 근거인가?", "하나라도 예 → JOB"))


def s02_folder():
    p = "w3"
    body = wf(p, {"job"})
    body += pulse(260, 144, 640, 48, "amber", 10)
    files = [("요청 원문", "무엇을 부탁받았나"), ("승인", "누가 무엇을 허락했나"), ("결정", "무엇을 왜 골랐나"), ("실행", "무엇을 했나"),
             ("검증", "어떻게 확인했나"), ("결과", "무엇이 남았나"), ("변경 전 원본", "되돌릴 곳")]
    for k, (h, s) in enumerate(files):
        x, y = 40 + (k % 4) * 232, 240 + (k // 4) * 120
        body += g(doc(x, y, 212, 96, h, s), build=1 if k < 4 else 2)
    body += g(card(504, 360, 444, 96, "mint", "폴더 하나만 열면", ("무엇을 왜 했고 어떻게 확인했는지",), ssize=16, gap=28), build=3)
    return fig(p, body, "JOB 폴더에는 요청 원문, 승인, 결정, 실행, 검증, 결과, 변경 전 원본이 함께 남는다",
               mob=mobile("요청 원문", "승인", "결정", "실행", "검증", "결과", "변경 전 원본"))


def s02_states():
    p = "w5"
    extra = pkt(p, "rail", "amber", 5.0, .4)
    body = wf(p, {"rail"}, extra)
    body += g(lead("M490 136V250") + card(300, 250, 380, 110, "mint", "상태 = 지금 있는 자리", ("예: 지금은 '실행' 단계",), ssize=17), build=1)
    body += g('<path d="M490 130C520 190 640 190 670 130" fill="none" stroke="#ffcf86" stroke-width="3" stroke-dasharray="6 5"/>'
              + card(600, 390, 360, 110, "amber", "전이 = 자리가 바뀌는 일", ("실행 → 검증",), ssize=17) + lead("M600 180L780 390"), build=2)
    body += g(card(40, 390, 520, 110, "", "넘어갈 조건은 미리 정해 둔다", ("조건을 채워야 다음 상태로 간다",), ssize=17), build=3)
    return fig(p, body, "상태는 지금 있는 단계이고, 전이는 다음 단계로 바뀌는 일이다",
               mob=mobile("상태: 지금 위치", "전이: 위치가 바뀜", "조건: 넘어갈 기준"))


def s02_gate():
    p = "w6"
    extra = (lane(p, "seg1", "M310 462H388", "amber", arrow=False) + pkt(p, "seg1", "amber", 1.1, .3, 10).replace('class="mo-pkt amber"', 'class="mo-pkt amber" data-loop="no"')
             + g(lane(p, "seg2", "M412 462H490", "amber", arrow=False) + pkt(p, "seg2", "amber", 1.0, 4.4, 10).replace('class="mo-pkt amber"', 'class="mo-pkt amber" data-loop="no"'), build=3))
    body = wf(p, {"rail", "gates", "job"}, extra)
    body += pulse(392, 70, 16, 44, "amber", 4)
    body += g('<path class="lane amber" d="M560 248C540 180 430 170 408 116" marker-end="url(#w6-amber)"/>'
              + card(430, 250, 360, 100, "amber", "검증 기록", ("일한 쪽이 남긴 확인 결과",), ssize=16), build=1)
    body += g('<rect x="395" y="74" width="10" height="36" rx="3" fill="#82dec6"/>' + t(400, 56, "열림", "t-tag c-mint"), build=2)
    body += card(40, 250, 340, 100, "coral", "말로는 열리지 않는다", ("“검증했어요” ✕",), ssize=17)
    body += g(card(40, 400, 920, 96, "mint", "약속한 기록이 실제로 있는지 확인한 뒤에 다음 단계를 연다", tsize=22), build=3)
    return fig(p, body, "토큰이 게이트 앞에서 멈추고, 검증 기록이 들어가면 게이트가 열려 다음 단계로 간다",
               mob=mobile("게이트 앞에서 멈춤", "기록이 들어감", "게이트가 열림", flow=True))


def s02_approval():
    p = "w8"
    body = wf(p, {"gates"})
    body += f'<rect class="u-box" x="40" y="260" width="250" height="120" rx="14"/>' + person(78, 300) + t(180, 300, "사용자", "t-md")
    body += t(165, 348, "“공개해도 됩니다”", "t-sm c-coral", 18)
    body += g(lane(p, "a1", "M296 320H356", "coral") + pkt(p, "a1", "coral", 1.0, 1.3)
              + card(360, 250, 300, 140, "coral", "승인 기록", ("누가 · 무엇을", "사용자 원문 그대로"), ssize=17), build=1)
    body += g(lane(p, "a2", "M666 320H726", "coral") + card(730, 250, 230, 140, "mint", "실행 경계", ("근거가 있을 때만", "다음 단계로"), ssize=17), build=2)
    body += g(card(40, 420, 920, 90, "", "승인을 지어내지 않는다 — 원문이 없으면 먼저 묻는다", tsize=22), build=3)
    return fig(p, body, "사용자 원문이 승인 기록으로 남고, 그 근거가 있을 때만 실행 경계를 넘는다",
               mob=mobile("사용자 원문", "승인 기록", "실행 경계", flow=True))


def s02_done():
    p = "w10"
    body = wf(p, {"rail"})
    body += '<rect class="card" x="60" y="260" width="880" height="48" rx="24"/>'
    body += '<rect x="64" y="264" width="740" height="40" rx="20" fill="#82dec6" class="mo-grow"/>'
    body += t(500, 285, "쓸 수 있는 결과", "t-md", 20).replace('class="t-md"', 'class="t-md" style="fill:#0f1a27"')
    body += g('<circle cx="840" cy="284" r="54" fill="#173a39" stroke="#82dec6" stroke-width="4"/>' + t(840, 284, "완료", "t-md c-mint", 24), build=1, cls="")
    body += g(card(60, 350, 420, 150, "mint", "끝까지 만든 것", ("쓸 수 있는 결과", "확인한 사실"), ssize=17), build=2)
    body += g(card(520, 350, 420, 150, "amber", "남은 일", ("무엇이 남았는지", "다음에 무엇을 할지"), ssize=17), build=3)
    return fig(p, body, "진행 막대가 쓸 수 있는 수준까지 차면 완료 도장을 찍고, 남은 일은 따로 적는다",
               mob=mobile("쓸 수 있는 결과", "남은 일을 분명히"))


def s02_stuck():
    p = "w11"
    body = wf(p, {"rail"})
    pairs = [("기록이 빠짐", "채우고 그 자리에서 다시"), ("같은 오류가 반복됨", "원인 하나를 고치고 다시"), ("시간이 모자람", "나누거나 시간을 늘려 다시")]
    for k, (a, b) in enumerate(pairs):
        y = 236 + k * 74
        body += g(card(40, y, 330, 60, "coral", a, tsize=20) + lane(p, f"p{k}", f"M376 {y + 30}H440", "mint") + card(446, y, 514, 60, "mint", b, tsize=20), build=k + 1)
    body += g(card(40, 462, 920, 60, "", "✕ 같은 요청을 그대로 반복하기 · ✕ 게이트를 넘기 위한 요청 만들기", tsize=19).replace('class="t-md"', 'class="t-md c-coral"'), build=4)
    return fig(p, body, "막힌 상태마다 맞는 행동이 있고, 같은 요청의 반복은 하지 않는다",
               mob=mobile("기록 누락 → 채우고 다시", "같은 오류 → 원인 고치고 다시", "시간 부족 → 나눠서 다시"))


# ------------------------------------------------------------------ lecture 03
def shift_people(x, label, sub, cls, icon):
    return (f'<rect class="card {cls}" x="{x}" y="70" width="230" height="170" rx="16"/>' + icon
            + t(x + 115, 186, label, "t-md") + t(x + 115, 216, sub, "t-sm", 15))


def sun(x, y):
    return f'<circle cx="{x}" cy="{y}" r="16" fill="#ffcf86"/>'


def moon(x, y):
    return f'<circle cx="{x}" cy="{y}" r="16" fill="#e8d9a8"/><circle cx="{x + 8}" cy="{y - 6}" r="14" fill="#16243a"/>'


def notebook(x, y, w=150, h=110, lit=True, label="인수인계 노트"):
    fill, stroke = ("#2b2a1e", "#e8d9a8") if lit else ("#1b2b3d", "#4a5f77")
    lines = "".join(f'<path d="M{x + 22} {y + 34 + k * 18}H{x + w - 22}" stroke="{stroke}" stroke-width="2" opacity=".6"/>' for k in range(3))
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2.4"/>'
            f'<path d="M{x + 12} {y}V{y + h}" stroke="{stroke}" stroke-width="3"/>{lines}' + t(x + w / 2, y + h + 22, label, "t-sm", 15))


def s03_cover():
    p = "k1"
    body = S.STYLE
    body += g(shift_people(40, "밤 근무자", "겪은 일을 안다", "", moon(155, 112) + person(155, 150)), cls="mo-rise")
    body += g(shift_people(730, "아침 근무자", "아무것도 모른다", "", sun(845, 112) + person(845, 150)), cls="mo-rise")
    body += notebook(425, 96) + lane(p, "n1", "M274 150H418", "amber") + lane(p, "n2", "M582 150H724", "amber") + pkt(p, "n1", "amber", 1.2, .5) + pkt(p, "n2", "amber", 1.2, 1.9)
    body += g(card(40, 300, 230, 120, "blue", "세션 1", ("일을 마치면 잊는다",), ssize=16)
              + card(730, 300, 230, 120, "blue", "세션 2", ("빈 머리로 시작한다",), ssize=16)
              + '<rect x="420" y="320" width="160" height="80" rx="10" fill="#2b2a1e" stroke="#e8d9a8" stroke-width="2" stroke-dasharray="6 5"/>'
              + t(500, 360, "? 넘겨줄 장치", "t-sm", 17), build=1)
    body += g(t(500, 470, "사람 자리에 에이전트를 놓으면 — 세션이 바뀔 때마다 새 사람이 출근한다", "t-md", 20), build=2)
    return S.scene(p, body, "밤 근무자와 아침 근무자 사이에 인수인계 노트가 있고, 같은 자리에 세션 1과 세션 2가 들어간다",
                   on_map=("know",), mobile=mobile("밤 근무자 → 노트 → 아침 근무자", "세션 1 → ? → 세션 2"))


def ctx_window(x, y, w, h, label="다음 에이전트의 맥락 창"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#1b2847" stroke="#9bc2ff" stroke-width="2.4"/>'
            + t(x + w / 2, y + 22, label, "t-tag c-blue"))


def s03_record():
    p = "k2"
    body = kn(p, {"kconn", "k_lesson"})
    body += '<rect x="40" y="320" width="280" height="200" rx="12" fill="#16243a" stroke="#3d5571" stroke-width="2"/>' + t(180, 344, "서랍 속", "t-tag")
    body += g(notebook(105, 370, lit=False, label="남겨 둔 기록"), cls="dim")
    body += g(lane(p, "o", "M326 420H436", "mint") + pkt(p, "o", "", 1.2, 1.3), build=1)
    body += g(ctx_window(440, 320, 520, 200) + notebook(500, 370) + t(810, 400, "펼쳐 읽을 때", "t-md c-mint", 21) + t(810, 434, "비로소 지식이 된다", "t-sm", 17), build=1)
    return fig(p, body, "서랍 속 기록은 흐리고, 다음 에이전트의 맥락 창에서 펼쳐 읽을 때 밝아진다",
               mob=mobile("서랍 속 기록: 아직 지식 아님", "맥락 창에서 읽힐 때 지식"))


def s03_limit():
    p = "k3"
    body = kn(p, {"know", "kconn"})
    for k in range(8):
        y = 500 - k * 22
        body += f'<g class="mo-rise" style="--d:{k + 1}"><rect class="card know" x="{60 + (k % 2) * 8}" y="{y}" width="240" height="18" rx="4"/></g>'
    body += t(184, 330, "계속 쌓이는 기록", "t-tag")
    body += ctx_window(360, 330, 260, 190, "한 번에 읽을 수 있는 양")
    for k in range(3):
        body += f'<rect class="card know" x="{390}" y="{378 + k * 40}" width="200" height="28" rx="4"/>'
    checks = ["찾을 수 있나", "지금도 맞나", "실제로 쓰이나"]
    body += t(800, 336, "넘겨준 경험이 제 몫을 하려면", "t-tag c-amber")
    for k, c in enumerate(checks):
        body += card(660, 360 + k * 54, 280, 44, "", f"□ {c}", tsize=19, build=k + 1)
    return fig(p, body, "기록은 계속 쌓이지만 한 번에 읽을 수 있는 양은 정해져 있어, 찾을 수 있나·지금도 맞나·쓰이나가 조건이 된다",
               mob=mobile("기록은 계속 쌓임", "읽을 양은 정해짐", "찾을 수 있나 · 맞나 · 쓰이나"))


def s03_axes():
    p = "k4"
    body = '<path d="M180 470H960" stroke="#879cb3" stroke-width="2.4" marker-end="url(#k4-gray)"/>'
    body += '<path d="M180 470V60" stroke="#879cb3" stroke-width="2.4" marker-end="url(#k4-gray)"/>'
    body += t(250, 500, "늘 맞음", "t-sm", 16) + t(900, 500, "지금만 맞음", "t-sm", 16) + t(570, 526, "얼마나 오래 맞나", "t-tag")
    rows = [("지킬 원칙", 110), ("사람", 182), ("일하는 방법", 254), ("겪은 일", 326), ("지금 상태", 398)]
    for name, y in rows:
        body += t(168, y, name, "t-sm", 16, anchor="end") + f'<path d="M180 {y}H960" stroke="#26384b" stroke-width="1"/>'
    body += t(60, 40, "무엇에 관한 것인가", "t-tag", anchor="start")
    cells = [(220, 110, "규칙", "늘 지킬 원칙", "mint"), (320, 182, "기억", "사람에 대해", "blue"), (420, 254, "스킬", "일하는 방법", "blue"),
             (620, 326, "교훈", "겪은 일", "know"), (820, 398, "실물", "지금의 상태", "amber")]
    for k, (x, y, h, s, c) in enumerate(cells, 1):
        body += g(f'<rect class="card {c}" x="{x}" y="{y - 30}" width="150" height="60" rx="10"/>' + t(x + 75, y - 9, h, "t-md", 20)
                  + t(x + 75, y + 16, s, "t-sm", 13), build=k)
    return fig(p, body, "가로는 얼마나 오래 맞는지, 세로는 무엇에 관한 것인지. 규칙, 기억, 스킬, 교훈, 실물 다섯 칸이 자리 잡는다",
               mob=mobile("규칙: 늘 지킬 원칙", "기억: 사람에 대해", "스킬: 일하는 방법", "교훈: 겪은 일", "실물: 지금의 상태"))


def s03_when():
    p = "k5"
    body = kn(p, {"kconn", "k_rule", "k_skill", "k_lesson"})
    body += pulse(600, 104, 160, 68)
    body += ctx_window(640, 330, 320, 190, "일하는 에이전트의 맥락 창")
    srcs = [(340, "원칙", "일을 시작할 때마다", "mint", False), (400, "자료", "비슷한 일을 만났을 때", "know", True), (460, "검색", "필요할 때 찾아서", "know", True)]
    for k, (y, h, s, c, dash) in enumerate(srcs):
        body += g(card(40, y - 26, 300, 52, c, h, tsize=19) + lane(p, f"s{k}", f"M346 {y}H{634}", "mint" if not dash else "amber", dash=dash)
                  + t(490, y - 12, s, "t-sm", 15) + pkt(p, f"s{k}", "" if not dash else "amber", 1.6, .4 + k * .8), build=k + 1)
    body += t(800, 420, "꼭 지킬 것은 늘", "t-sm", 17) + t(800, 452, "가끔 필요한 것은 찾아서", "t-sm", 17)
    return fig(p, body, "늘 지킬 원칙은 일을 시작할 때마다, 지난 경험은 비슷한 일을 만났을 때 찾아 읽는다",
               mob=mobile("원칙: 늘 읽음", "자료 · 검색: 일에 맞춰 찾아 읽음"))


def s03_canon():
    p = "k6"
    places = [(40, "게시판"), (370, "노트"), (700, "메신저")]
    body = "".join(card(x, 70, 260, 110, "", n, ("점검은 10시",), ssize=19) for x, n in places)
    body += g(card(40, 210, 260, 110, "mint", "게시판", ("점검은 11시 ✓",), ssize=19)
              + card(370, 210, 260, 110, "coral", "노트", ("점검은 10시 ✕",), ssize=19)
              + card(700, 210, 260, 110, "coral", "메신저", ("점검은 10시 ✕",), ssize=19)
              + t(500, 344, "한 곳만 고쳐지고, 나머지는 틀린 말을 한다", "t-sm c-coral", 17), build=1)
    body += g(card(370, 380, 260, 120, "mint", "정본 하나", ("점검은 11시",), ssize=19)
              + card(40, 400, 240, 80, "", "노트 → 정본을 보라", tsize=17) + card(720, 400, 240, 80, "", "메신저 → 정본을 보라", tsize=17)
              + lane(p, "c1", "M284 440H364", "mint") + lane(p, "c2", "M716 440H636", "mint"), build=2)
    return fig(p, body, "같은 공지를 세 곳에 적으면 한 곳만 고쳐져 서로 다른 말을 하고, 정본 하나와 그것을 가리키는 화살표로 정리한다",
               mob=mobile("세 곳에 복사", "한 곳만 고쳐짐", "정본 하나 + 가리키기", flow=True))


def s03_cycle():
    p = "k7"
    body = kn(p, {"know", "kconn", "kloop"}, kloop(p, 6.0) + pkt(p, "kcyc", "amber", 6.0, 3.3, 7))
    steps = [("작업", "일을 하며 겪는다"), ("기록", "겪은 일을 남긴다"), ("축적", "쌓고 정리한다"), ("활용", "다음 일에 읽힌다"), ("확인", "지금도 맞는지 본다")]
    for k, (h, s) in enumerate(steps):
        x = 30 + k * 190
        body += card(x, 330, 180, 110, "know", h, s, ssize=15, build=k + 1)
    body += g(t(500, 486, "한 번 적고 끝나는 문서가 아니라, 일과 함께 도는 순환", "t-md c-mint", 21), build=6)
    return fig(p, body, "작업, 기록, 축적, 활용, 확인이 다시 작업으로 이어지는 순환과 그 위의 정기 점검",
               mob=mobile("작업", "기록", "축적", "활용", "확인", flow=True))


def s03_start():
    p = "k8"
    body = ctx_window(600, 60, 360, 420, "일을 시작한 에이전트의 맥락 창")
    layers = [(110, "늘 들어오는 원칙", "모든 일에", "mint", "mint", False),
              (230, "맡긴 쪽이 골라 붙인 자료", "맡긴 일에만", "know", "amber", False),
              (350, "스스로 찾는 기록", "필요할 때", "know", "amber", True)]
    for k, (y, h, s, c, lc, dash) in enumerate(layers):
        body += g(card(40, y - 40, 300, 80, c, h, (s,), tsize=19, ssize=15) + lane(p, f"l{k}", f"M346 {y}H594", lc, dash=dash)
                  + pkt(p, f"l{k}", "" if lc == "mint" else "amber", 1.4, .4 + k * .7)
                  + f'<rect class="card {c}" x="630" y="{y - 26}" width="300" height="52" rx="8"/>' + t(780, y, h, "t-sm", 16), build=k + 1)
    body += g(card(40, 430, 520, 70, "blue", "워커에게 직접 맡긴 일에는 둘째 겹이 없다", tsize=18), build=4)
    return fig(p, body, "맥락 창에 세 겹이 들어온다: 늘 들어오는 원칙, 맡긴 쪽이 골라 붙인 자료, 스스로 찾는 기록",
               mob=mobile("늘: 원칙", "맡긴 일: 골라 붙인 자료", "필요할 때: 스스로 찾기"))


def s03_check():
    p = "k9"
    body = ""
    for k in range(6):
        body += f'<rect class="card know" x="{40 + (k % 3) * 70}" y="{110 + (k // 3) * 110}" width="60" height="90" rx="6"/>'
    body += t(145, 80, "찾은 후보", "t-tag")
    body += g('<path d="M260 100L330 180V300L260 380" fill="none" stroke="#ffcf86" stroke-width="3"/>' + t(330, 400, "원문을 열어 보면", "t-sm c-amber", 16)
              + "".join(f'<rect class="card know" x="{360 + (k % 2) * 70}" y="{140 + (k // 2) * 110}" width="60" height="90" rx="6"/>' for k in range(3)), build=1)
    body += g('<path d="M520 120L590 190V290L520 360" fill="none" stroke="#82dec6" stroke-width="3"/>' + t(590, 400, "지금 상태와 같은가", "t-sm c-mint", 16)
              + '<rect class="card mint" x="630" y="190" width="70" height="104" rx="6"/>', build=2)
    body += g(card(740, 170, 220, 140, "mint", "쓸 수 있는 근거", ("원문과 지금 상태로", "두 번 걸렀다"), ssize=15), build=3)
    body += card(40, 450, 920, 60, "", "지난주 기록이 맞아도, 오늘도 그런지는 지금 상태를 봐야 안다", tsize=19)
    return fig(p, body, "찾은 후보 여러 장이 원문 확인과 현재 상태 확인을 거치며 한두 장만 남는다",
               mob=mobile("찾은 후보", "원문 확인", "지금 상태 확인", "쓸 수 있는 근거", flow=True))


def s03_lesson():
    p = "k10"
    body = '<rect class="card know" x="40" y="60" width="520" height="300" rx="14"/>' + t(64, 90, "교훈", "t-tag", anchor="start")
    rows = [("무슨 일이 있었나", ""), ("왜 그랬나", ""), ("어떻게 풀었나", ""), ("이럴 때 다시 보라", "amber")]
    for k, (h, c) in enumerate(rows):
        y = 112 + k * 60
        body += g(f'<rect class="card {c}" x="64" y="{y}" width="472" height="48" rx="8"/>' + t(84, y + 24, h, "t-md", 20, anchor="start"), build=k + 1 if k < 3 else None)
    body += g(card(620, 60, 340, 120, "blue", "다음 사람", ("비슷한 상황을 만남",), ssize=16)
              + lane(p, "m", "M616 230H560", "amber") + pkt(p, "m", "amber", 1.2, 4.6)
              + card(620, 200, 340, 70, "amber", "“바닥에 물이 고이면”", tsize=18) + pulse(64, 292, 472, 48, "amber", 8), build=4)
    body += g(card(40, 400, 920, 110, "mint", "결론만 적으면 찾지 못한다", ("다음 사람은 자기가 겪는 상황으로 찾는다 — 그 상황을 함께 적어 둔다",), ssize=17, gap=30), build=5)
    return fig(p, body, "교훈 카드에 무슨 일·왜·어떻게 풀었나와 '이럴 때 다시 보라'를 남기면, 그 상황을 만난 다음 사람에게 걸려 나온다",
               mob=mobile("무슨 일이 있었나", "왜", "어떻게 풀었나", "이럴 때 다시 보라"))


def s03_tidy():
    p = "k12"
    body = ""
    for k in range(9):
        x = 60 + (k * 37) % 150
        y = 330 - k * 26
        body += f'<rect class="card know" x="{x}" y="{y}" width="150" height="40" rx="6" transform="rotate({(k * 7) % 15 - 7} {x + 75} {y + 20})"/>'
    body += t(150, 400, "쌓이기만 한 기록", "t-tag")
    acts = [("대조", "새 것을 기존 것과 맞춰 본다", ""), ("올림", "반복된 교훈은 규칙·절차로", "mint"), ("내림", "낡은 것은 치운다", "coral")]
    for k, (h, s, c) in enumerate(acts):
        body += card(320, 70 + k * 110, 330, 90, c, h, s, ssize=15, build=k + 1)
    body += g('<rect x="700" y="80" width="260" height="300" rx="12" fill="none" stroke="#82dec6" stroke-width="2.4"/>'
              + "".join(f'<path d="M700 {150 + k * 75}H960" stroke="#82dec6" stroke-width="2"/>' for k in range(3))
              + "".join(f'<rect class="card know" x="{716 + j * 60}" y="{98 + k * 75}" width="48" height="44" rx="4"/>' for k in range(4) for j in range(4) if (k + j) % 3)
              + t(830, 404, "정돈된 선반", "t-tag c-mint"), build=4)
    body += card(40, 450, 920, 60, "", "같은 실수가 세 번 적히면, 그것은 메모가 아니라 수칙에 넣을 일이다", tsize=19)
    return fig(p, body, "쌓이기만 한 카드 더미를 대조하고, 반복된 교훈은 올리고, 낡은 것은 내려 정돈된 선반으로 바꾼다",
               mob=mobile("대조", "올림: 반복된 교훈 → 규칙·절차", "내림: 낡은 것", flow=True))


def gauge(cx, cy, label, val, build):
    import math
    a = math.pi * (1 - val)
    x, y = cx + 80 * math.cos(a), cy - 80 * math.sin(a)
    return g(f'<path d="M{cx - 90} {cy}A90 90 0 0 1 {cx + 90} {cy}" fill="none" stroke="#304357" stroke-width="16"/>'
             f'<path d="M{cx - 90} {cy}A90 90 0 0 1 {cx + 90} {cy}" fill="none" stroke="#82dec6" stroke-width="16" pathLength="1" stroke-dasharray="{val} 1"/>'
             f'<path d="M{cx} {cy}L{x:.1f} {y:.1f}" stroke="#edf2fa" stroke-width="4"/><circle cx="{cx}" cy="{cy}" r="8" fill="#edf2fa"/>'
             + t(cx, cy + 36, label, "t-md", 20), build=build)


def s03_watch():
    p = "k13"
    body = kn(p, {"kloop", "know"})
    body += pulse(235, 20, 530, 38, "", 18)
    for k, (lab, v) in enumerate((("찾을 수 있나", .8), ("지금도 맞나", .6), ("실제로 쓰이나", .7))):
        body += gauge(190 + k * 310, 430, lab, v, k + 1)
    body += g(t(500, 520, "지식은 고장 나도 오류를 내지 않는다 — 정기적으로 직접 시험해 본다", "t-sm c-amber", 17), build=4)
    return fig(p, body, "정기 점검 계기판: 찾을 수 있나, 지금도 맞나, 실제로 쓰이나",
               mob=mobile("찾을 수 있나", "지금도 맞나", "실제로 쓰이나"))


def s03_close():
    p = "k14"
    cx, cy, r = 500, 250, 170
    ring = f'<path id="{p}-ring" d="M{cx} {cy - r}A{r} {r} 0 1 1 {cx - 0.1} {cy - r}" fill="none" stroke="#82dec6" stroke-width="3" stroke-dasharray="8 8"/>'
    body = ring + pkt(p, "ring", "", 8.0, .3, 10) + pkt(p, "ring", "amber", 8.0, 4.3, 10)
    nodes = [(0, "겪은 일을 남긴다"), (72, "정리한다"), (144, "다음 근무자가 읽는다"), (216, "지금도 맞는지 확인한다"), (288, "다시 일한다")]
    import math
    for k, (deg, label) in enumerate(nodes):
        a = math.radians(deg - 90)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        body += g(f'<rect class="card know" x="{x - 115:.0f}" y="{y - 26:.0f}" width="230" height="52" rx="26"/>' + t(x, y, label, "t-sm", 16), build=k + 1)
    body += notebook(440, 205, w=120, h=90, label="")
    body += g(t(500, 500, "어제의 실수를 오늘 되풀이하지 않는다", "t-md c-mint", 22), build=6)
    return fig(p, body, "교대 노트가 한 바퀴 돈다: 겪은 일을 남기고, 정리하고, 다음 근무자가 읽고, 확인하고, 다시 일한다",
               mob=mobile("남긴다", "정리한다", "읽는다", "확인한다", "다시 일한다", flow=True))


# ------------------------------------------------------------------ lecture 04
def life_packets(p, d=0.0):
    return (pkt(p, "u2m", "", 1.0, d + .2), pkt(p, "l1", "amber", .8, d + 1.2), pkt(p, "l5", "amber", 1.0, d + 2.0),
            pkt(p, "w2r", "blue", 1.6, d + 3.0), pkt(p, "rail", "amber", 2.6, d + 4.6), pkt(p, "kcyc", "", 3.0, d + 4.6),
            pkt(p, "r1", "amber", 1.0, d + 7.4), pkt(p, "r2", "amber", 1.1, d + 8.4), pkt(p, "m2u", "", 1.0, d + 9.5))


def s04_cover():
    p = "i1"
    extra = f'<path id="{p}-kcyc" d="{KCYC}" fill="none" stroke="none"/>' + "".join(life_packets(p))
    body = map_layer(p, {"all"}, extra)
    return fig(p, body, "요청 하나가 사용자에서 매니저, 요청서, 워커, 작업 흐름, 지식을 지나 응답서와 보고로 돌아오는 일생",
               view="0 0 1000 900", mob=mobile("요청", "판단 · 맡김", "실행 · 기록", "검증", "판정 · 보고", flow=True))


def s04_two_ways():
    pa, pb = "i4a", "i4b"
    a = S.full_map(pa, VIA | {"entry", "rail", "job"}) + "".join(
        (pkt(pa, "u2m", "", 1.0, .2), pkt(pa, "l1", "amber", .8, 1.2), pkt(pa, "l5", "amber", 1.0, 2.0), pkt(pa, "w2r", "blue", 1.4, 3.0),
         pkt(pa, "rail", "amber", 1.8, 4.4), pkt(pa, "r1", "amber", .9, 6.2), pkt(pa, "r2", "amber", .9, 7.0), pkt(pa, "m2u", "", 1.0, 7.8)))
    b = S.full_map(pb, DIRECT | {"entry", "rail", "job"}) + "".join(
        (pkt(pb, "direct", "blue", 1.8, .2), pkt(pb, "w2r", "blue", 1.4, 2.0), pkt(pb, "rail", "amber", 1.8, 3.4), pkt(pb, "reply", "blue", 1.8, 5.2)))
    clip = f'<clipPath id="{pa}-clip"><rect x="0" y="0" width="1000" height="590"/></clipPath>'
    tags = (g('<rect x="290" y="244" width="240" height="40" rx="20" fill="#173a39" stroke="#82dec6"/>' + t(410, 265, "① 매니저에게 맡기기", "t-tag c-mint"), cls="mo-alt-a")
            + g('<rect x="290" y="244" width="240" height="40" rx="20" fill="#1b2847" stroke="#9bc2ff"/>' + t(410, 265, "② 워커에게 직접", "t-tag c-blue"), cls="mo-alt-b"))
    body = clip + f'<g clip-path="url(#{pa}-clip)">' + g(a, cls="mo-alt-a") + g(b, cls="mo-alt-b") + "</g>" + tags
    return fig(pa, body, "같은 지도 위에서 매니저를 거치는 요청과 워커에게 직접 가는 요청이 번갈아 흐른다", view="0 0 1000 590",
               extra_defs=(pb,), mob=mobile("① 매니저 → 요청서 → 워커 → 작업 흐름 → 응답서 → 매니저", "② 워커 → 작업 흐름 → 같은 대화로 답"))


def s04_double():
    p = "i5"
    body = S.full_map(p, {"rail", "mgr", "lane_bot", "wkr"}, labels=True)
    clip = f'<clipPath id="{p}-clip"><rect x="0" y="0" width="1000" height="590"/></clipPath>'
    body = clip + f'<g clip-path="url(#{p}-clip)">{body}</g>'
    body += pulse(640, 432, 60, 60, "", 30) + pulse(542, 280, 92, 64, "amber", 6)
    body += g('<circle cx="580" cy="367" r="18" fill="#173a39" stroke="#82dec6" stroke-width="3"/>' + t(580, 368, "1", "t-md c-mint")
              + '<rect x="604" y="352" width="260" height="30" rx="15" fill="#173a39" stroke="#82dec6"/>' + t(734, 367, "일한 쪽의 검증", "t-tag c-mint"), build=1)
    body += g('<circle cx="246" cy="261" r="18" fill="#3a2f1c" stroke="#ffcf86" stroke-width="3"/>' + t(246, 262, "2", "t-md c-amber")
              + '<rect x="270" y="246" width="230" height="30" rx="15" fill="#3a2f1c" stroke="#ffcf86"/>' + t(385, 261, "맡긴 쪽의 판정", "t-tag c-amber"), build=2)
    return fig(p, body, "두 겹의 확인: 작업 흐름의 검증 단계(일한 쪽)와 응답서를 받은 매니저의 판정(맡긴 쪽)", view="0 0 1000 590",
               mob=mobile("① 일한 쪽의 검증", "② 맡긴 쪽의 판정"))


def s04_risk():
    p = "i6"
    rows = [("위험이 작다", "되돌리기 쉬운 작은 수정", 1), ("위험이 중간", "여러 파일 · 여러 단계", 2), ("위험이 크다", "공개 · 운영 · 되돌리기 어려움", 3)]
    layers = [("일한 쪽 검증", "mint"), ("맡긴 쪽 판정", "amber"), ("따로 다시 확인", "coral")]
    for k, (h, s, n) in enumerate(rows):
        y = 80 + k * 140
        body = (body if k else "") + card(40, y, 300, 110, "", h, s, ssize=15)
        for j in range(n):
            lh, c = layers[j]
            body += g(f'<rect class="card {c}" x="{370 + j * 200}" y="{y + 20}" width="186" height="70" rx="10"/>' + t(463 + j * 200, y + 55, lh, "t-sm", 17), build=k + 1)
    body += t(670, 52, "확인의 깊이", "t-tag")
    return fig(p, body, "위험이 클수록 일한 쪽의 검증, 맡긴 쪽의 판정 위에 따로 다시 확인하는 겹이 더해진다",
               mob=mobile("작다: 일한 쪽 검증", "중간: + 맡긴 쪽 판정", "크다: + 따로 다시 확인"))


def s04_change():
    p = "i8"
    body = card(40, 70, 280, 110, "mint", "매니저가 직접 고침", tsize=20) + card(40, 240, 280, 110, "blue", "직접 대화한 워커가 고침", tsize=19)
    body += lane(p, "a", "M326 125C420 125 420 200 476 200", "mint") + lane(p, "b", "M326 295C420 295 420 230 476 230", "blue")
    body += pkt(p, "a", "", 1.4, .4) + pkt(p, "b", "blue", 1.4, 1.2)
    body += g(card(480, 90, 220, 120, "amber", "원본 백업", ("고치기 전 그대로",), ssize=15)
              + card(720, 90, 240, 120, "amber", "변경 기록 한 줄", ("언제 · 무엇을 · 왜", "되돌릴 곳"), ssize=15), build=1)
    body += g(card(480, 240, 480, 110, "", "JOB이 있으면 그 폴더에, 없으면 파일 옆에", tsize=19), build=2)
    body += g(card(40, 400, 920, 100, "mint", "나중에 추적하고 되돌릴 수 있다", ("누가 고쳤든 같은 기록",), ssize=17), build=3)
    return fig(p, body, "매니저든 직접 대화한 워커든, 고친 뒤에는 원본 백업과 변경 기록 한 줄을 남긴다",
               mob=mobile("원본 백업", "변경 기록 한 줄", "추적 · 되돌리기"))


def s04_repo():
    p = "i9"
    body = skeleton(p, {"all"}, labels=False)
    files = [("reference/orchestrator.py", "매니저 쪽: 요청서를 쓰고 응답서를 판정", "M125 342V392", 40),
             ("reference/filesystem_transport.py", "파일로 주고받기", "M455 247V392", 360),
             ("reference/worker.py", "워커 쪽: 요청서를 읽고 응답서를 씀", "M880 342V392", 680)]
    for k, (f, s, d, x) in enumerate(files, 1):
        body += g(lead(d) + f'<rect class="card blue" x="{x}" y="392" width="290" height="92" rx="12"/>'
                  + t(x + 145, 422, f.split("/")[1], "t-md", 18) + t(x + 145, 456, s, "t-sm", 14), build=k)
    body += g(t(500, 516, "tests/ 의 테스트로 같은 흐름을 직접 돌려 볼 수 있다", "t-sm c-mint", 16), build=4)
    return scene(p, body, "공개 저장소의 참조 구현: 매니저 쪽, 파일 전달, 워커 쪽 코드와 테스트가 지도의 자리와 이어진다",
                 on_map=("user", "mgr", "wkr", "lanes"), mobile=mobile("orchestrator.py: 매니저 쪽", "filesystem_transport.py: 파일 전달", "worker.py: 워커 쪽", "tests/"))


def s04_recap():
    p = "i10"
    return fig(p, lecture_bands(p), "다섯 강의가 맡은 지도 구역이 차례로 켜지고, 요청이 확인된 결과가 되는 전체 그림으로 닫는다",
               view="0 0 1000 900", mob=mobile("00 전체", "01 역할", "02 작업 흐름", "03 지식", "04 통합", flow=True))


# ------------------------------------------------------------------ slide copy
# key: (eyebrow, [paragraphs], scene-or-sim, kind, em-phrase)
OLD = lambda num, key: (lambda: old_fig(num, key))
SIM = lambda num, key: ("sim", num, key)

SPEC = {
    # 00
    "00-01": ("p-hermes · 강의 00", ["p-hermes는 Hermes 엔진 위에 더한 로컬 운영 체계가 일을 나누고, 기록하고, 확인하는 방식을 설명합니다.",
                                    "위는 역할, 가운데는 작업 흐름, 아래는 지식입니다. 이 지도 한 장을 강의 내내 씁니다."], s00_cover, "cover", "확인된 결과"),
    "00-02": ("언어 모델", ["언어 모델은 지금 맥락 창에 들어 있는 글을 읽고, 다음에 올 말을 한 조각씩 이어 씁니다.",
                         "창에는 크기 제한이 있고, 창 밖의 내용이나 지난 세션은 알지 못합니다."], OLD("00", "00-02"), "concept", ""),
    "00-ex": ("실물 예시", ["맥락 창에 넣은 3행만 요약하면 배송 문의가 3건 중 2건으로 보입니다.",
                         "200행을 모두 세면 배송 문의는 40건, 20%입니다. 모델은 읽지 않은 행을 알 수 없습니다."], s00_example, "concept", ""),
    "00-03": ("에이전트", ["에이전트는 언어 모델이 도구로 파일을 읽고 명령을 실행한 뒤, 그 결과를 다시 읽고 다음 행동을 정하는 반복입니다.",
                        "그래서 실제 결과를 만들 수 있지만, 반복이 길어질수록 맥락 창이 차고 처음 목표가 흐려집니다."], OLD("00", "00-03"), "concept", ""),
    "00-04": ("긴 일의 문제", ["Hermes 엔진은 세션 기록을 저장합니다. 하지만 기록이 길어지면 목표와 진행 상태가 그 속에 묻힙니다.",
                           "세션이 바뀌면 다음 에이전트는 무엇부터 읽어야 할지 모른 채 시작합니다."], s00_break, "", ""),
    "00-05": ("파일로 남기기", ["요청과 결과를 대화 밖의 파일로 남기면, 세션이 끊겨도 다음 세션이 그 파일부터 읽고 이어 갑니다.",
                            "파일은 누가 언제 읽어도 같은 내용이라, 무엇을 약속했고 무엇이 돌아왔는지 다시 대조할 수 있습니다."], s00_files, "", ""),
    "00-06": ("세 층", ["위에서는 누가 판단하고 누가 실행하는지, 가운데에서는 일이 어떤 단계를 지나는지, 아래에서는 무엇을 읽고 남기는지를 봅니다.",
                      "남긴 기록은 아래 층에서 돌아 다음 일에 다시 읽힙니다."], s00_layers, "", ""),
    "00-entry": ("두 길", ["매니저에게 맡기면 매니저가 판단해 요청서로 워커에게 넘기고, 돌아온 응답서를 판정합니다.",
                         "워커에게 직접 맡기면 요청서 없이 같은 대화에서 판단부터 실행까지 이어집니다."], s00_entry, "", ""),
    "00-07": ("위 층 · 역할", ["매니저는 무엇을 할지 판단하고, 오래 걸리는 실행은 워커에게 맡기고, 돌아온 결과를 판정합니다.",
                           "워커는 맡은 일을 중간에 멈추지 않고 끝까지 수행합니다."], s00_manager, "", ""),
    "00-08": ("가운데 층 · 작업 흐름", ["기록이 필요한 일은 JOB이 되어 요청 → 실행 → 검증 → 완료를 지나고, 단계마다 기록이 남습니다.",
                                  "기록이 필요 없는 일은 JOB 없이 바로 처리합니다."], s00_workflow, "", ""),
    "00-09": ("아래 층 · 지식", ["에이전트는 일을 시작할 때 원칙과 이번 일에 맞는 기록을 읽고, 일을 마치면 겪은 일을 다시 남깁니다.",
                             "짧은 대화 하나에도 지식이 쓰입니다."], s00_knowledge, "", ""),
    "00-10": ("확인", ["확인은 두 겹입니다. 일한 쪽이 검증 단계에서 실물과 대조하고, 맡긴 경우에는 매니저가 응답서를 다시 대조합니다.",
                     "보고 문장만으로 완료라고 말하지 않습니다."], s00_verify, "", ""),
    "00-11": ("강의 순서", ["강의 01은 위 층의 역할, 02는 가운데 층의 작업 흐름, 03은 아래 층의 지식을 확대합니다.",
                         "강의 04에서는 요청 하나를 따라 세 층을 다시 잇습니다."], s00_next, "", ""),
    # 01
    "01-01": ("강의 01 · 두 역할", ["사용자가 일을 맡기는 길은 두 가지입니다. 매니저를 거치거나, 워커에게 직접 맡기거나.",
                                  "매니저가 워커에게 맡길 때 둘 사이에 오가는 것은 요청서와 응답서, 두 파일입니다."], lambda: A1.s_cover(), "cover", "끝까지 수행"),
    "01-02": ("나누는 이유", ["에이전트 하나가 계획부터 실행 로그까지 모두 들고 있으면, 맥락 창이 차면서 처음 목표와 완료 조건이 밀려납니다.",
                           "그래서 목표를 붙드는 쪽과 실행하는 쪽을 나눕니다."], lambda: A1.s_context(), "concept", ""),
    "01-03": ("파일로 주고받기", ["매니저가 요청서 파일을 쓰면, 워커가 그 파일을 읽고 수행한 뒤 응답서 파일을 씁니다.",
                              "파일은 세션이 끊겨도 남아, 무엇을 약속했고 무엇이 돌아왔는지 다시 확인할 수 있습니다."], lambda: A1.s_files(), "concept", ""),
    "01-modes": ("두 길", ["워커에게 직접 맡기면 워커가 그 대화 안에서 판단하고, 고치고, 기록하고, 같은 대화로 답합니다.",
                         "요청서와 응답서는 매니저를 거칠 때만 오갑니다. 길이 바뀌어도 워커는 같은 워커입니다."], s01_modes, "concept", ""),
    "01-04": ("매니저를 거치면", ["매니저는 실행 로그 없이 목표와 경계를 붙들고, 워커는 요청서 하나에 집중합니다.",
                              "결과는 만든 쪽이 아닌 매니저가 따로 확인합니다."], lambda: A1.s_why(), "", ""),
    "01-05": ("KEY IDEA", ["품질을 좌우하는 판단은 위에 남기고, 오래 걸리는 실행만 아래로 내려보냅니다."], None, "interlude", ""),
    "01-06": ("직접 할까, 맡길까", ["오래 걸리거나 결과가 큰 일은 워커에게 맡기고, 읽기·조사·작은 수정은 매니저가 직접 합니다.",
                                "설계·정책·글의 완성도·시각 결과처럼 품질을 좌우하는 판단은 매니저가 맡고, 실행량만 나눕니다."], SIM("01", "01-06"), "sim", ""),
    "01-user-choice": ("사용자의 선택", ["판단이 어렵거나 여러 단계에 걸치는 일은 매니저에게 맡겨, 판단과 확인을 따로 받습니다.",
                                      "간단하고 되돌릴 수 있는 일은 워커에게 직접 맡겨 바로 결과를 봅니다."], s01_user_choice, "", ""),
    "01-model-weight": ("모델의 무게", ["매니저는 사용자와 대화하며 판단하므로, 생각이 깊은 무거운 모델이 어울립니다.",
                                       "워커는 정해진 일을 길게 실행하므로 가벼운 모델로도 충분합니다. 직접 대화하는 워커는 일의 난이도에 맞춰 고릅니다."], s01_model_weight, "", ""),
    "01-07": ("요청서", ["요청서에는 목표, 완성 기준, 참조 경로, 금지 범위를 적습니다. 판단이 필요한 항목은 매니저가 미리 정해 둡니다.",
                       "사용자가 말하지 않은 범위 축소나 요청과 무관한 일은 넣지 않습니다."], s01_request, "", ""),
    "01-08": ("등록과 실행", ["요청서는 정해진 등록 경로 한 곳으로 들어가고, 이때 시도 한 번을 가리키는 요청 ID가 붙습니다. 작업 실행기가 이를 워커에게 넘기고 시간 제한을 지켜봅니다.",
                           "같은 목표를 다시 시도하면 새 요청 ID를 받습니다. 실행기가 함께 붙이는 자료 묶음은 강의 03에서 다룹니다."], s01_register, "", ""),
    "01-09": ("요청서의 약속", ["네 칸은 각각 하나의 약속입니다. 무엇을 끝낼지, 어떻게 확인할지, 무엇을 읽을지, 무엇은 하지 않을지.",
                             "약속이 분명해야 응답서가 돌아왔을 때 무엇과 대조할지 정해집니다."], s01_promise, "", ""),
    "01-ex": ("실물 예시", ["완성 기준에는 원자료를 어떻게 계산하고 대조할지를 씁니다.",
                         "20%라는 원하는 답을 완성 기준으로 미리 정하지 않습니다."], OLD("01", "01-example-request"), "concept", ""),
    "01-10": ("응답서", ["워커는 응답서에 자기 요청 ID와 네 가지 처리 상태 중 하나를 적어 돌려줍니다.",
                       "검증이 실패해도 만든 산출은 지우지 않고, 일부만 끝났으면 산출과 남은 일을 함께 적습니다."], lambda: A1.s_response(), "", ""),
    "01-11": ("판정과 복구", ["완료 보고를 받으면 핵심 수치 하나를 원천과 대조합니다. 일부만 끝났으면 한 번 이어 가고, 같은 사유로 두 번 막히면 멈추고 알립니다.",
                           "시간이 모자랐다면 같은 크기로 다시 보내지 않고, 범위를 나누거나 시간을 늘립니다."], SIM("01", "01-11"), "sim", ""),
    "01-12": ("승인 경계", ["영구 삭제, 외부 전송·게시, 자격증명·보안 설정, 운영 원칙 수정은 사용자만 승인합니다. 사용자의 원문이 있어야 실행합니다.",
                         "워커와 직접 대화할 때도 같습니다. 무응답이나 경과 시간은 승인이 아닙니다."], s01_approval, "", ""),
    # 02
    "02-01": ("강의 02 · 작업 흐름", ["짧고 되돌릴 수 있는 일은 기록 없이 바로 끝냅니다. 여러 단계에 걸치는 일은 JOB으로 기록을 남기며 단계를 지납니다.",
                                   "매니저든 워커든, 일을 하는 쪽이 이 갈림길에서 고릅니다."], s02_cover, "cover", "기록을 남기며"),
    "02-05": ("세 질문", ["여러 단계에 걸치는지, 나중에 되돌아볼 수 있는지, 다음 작업의 근거가 되는지 묻습니다.",
                       "직접 하든 맡기든 기준은 같습니다."], s02_three, "", ""),
    "02-06": ("JOB 폴더", ["JOB 폴더에는 요청 원문과 승인, 결정, 실행·검증 기록, 결과, 변경 전 원본이 함께 들어갑니다.",
                         "폴더 하나만 열면 무엇을 왜 했고 어떻게 확인했는지 이어서 볼 수 있습니다."], s02_folder, "", ""),
    "02-ex": ("실물 예시", ["요청 기록에 약속한 방법과 검증 기록에 남은 확인 결과를 나란히 읽습니다.",
                         "20%는 이 원자료를 계산한 결과이며, 미리 정해 둔 정답이 아닙니다."], OLD("02", "02-example-records"), "concept", ""),
    "02-02": ("상태와 전이", ["작업 흐름은 일을 몇 개의 상태로 나누고, 다음 상태로 넘어갈 조건을 미리 정해 둔 것입니다.",
                           "지금 있는 단계가 상태이고, 다음 단계로 바뀌는 일이 전이입니다."], s02_states, "concept", ""),
    "02-gate": ("게이트", ["게이트는 '검증했다'는 말이 아니라, 검증 기록이 실제로 있는지를 봅니다.",
                        "검증 기록은 일을 한 쪽이 남깁니다. 기록이 들어가야 다음 단계가 열립니다."], s02_gate, "", ""),
    "02-08": ("기록이 빠지면", ["게이트는 기록이 빠진 자리에서 멈추고, 무엇이 빠졌는지 알려 줍니다. 채우면 그 자리에서 이어 갑니다.",
                             "기록이 있다고 내용이 맞는 것은 아닙니다. 값이 맞는지는 검증 단계에서 원자료와 대조합니다."], SIM("02", "02-08"), "sim", ""),
    "02-09": ("승인 기록", ["승인 기록에는 사용자가 실제로 승인한 문장을 그대로 남깁니다.",
                         "승인이 없으면 만들어 내지 않고 먼저 묻습니다. 범주별 기준은 위키에 있습니다."], s02_approval, "", ""),
    "02-10": ("KEY IDEA", ["쓸 수 있는 결과를 끝까지 만들고, 남은 부분은 써 보며 다듬습니다."], None, "interlude", ""),
    "02-11": ("완료의 기준", ["100% 완성이나 완전한 증명을 기다리느라 멈추지 않습니다. 쓸 수 있는 결과를 먼저 완성합니다.",
                           "검증이 실패해도 산출은 보존하고, 부족한 점은 남은 일로 적습니다."], s02_done, "", ""),
    "02-12": ("막혔을 때", ["막히면 원인 하나를 고친 뒤 다시 갑니다. 같은 요청의 단순 반복이나 같은 크기의 재시도는 하지 않습니다.",
                         "다음 강의에서는 이렇게 남긴 기록이 어떻게 다음 일의 지식이 되는지 봅니다."], s02_stuck, "", ""),
    # 03 — copy comes from the storyboard's spoken takeaway and analogy
    "03-01": ("강의 03 · 지식", None, s03_cover, "cover", "모두 잊습니다"),
    "03-02": ("개념", None, s03_record, "", ""),
    "03-03": ("개념", None, s03_limit, "", ""),
    "03-04": ("구조", None, s03_axes, "", ""),
    "03-05": ("구조", None, s03_when, "", ""),
    "03-06": ("구조", None, s03_canon, "", ""),
    "03-07": ("순환", None, s03_cycle, "", ""),
    "03-08": ("순환", None, s03_start, "", ""),
    "03-09": ("순환", None, s03_check, "", ""),
    "03-ex": ("실물 예시", ["어떤 상황에서 나온 기록인지 날짜와 출처로 확인합니다.",
                         "지난 해결을 오늘 적용하기 전에는 지금 기준도 확인합니다."], OLD("03", "03-example-source"), "concept", ""),
    "03-10": ("순환", None, s03_lesson, "", ""),
    "03-11": ("KEY IDEA", ["겪은 일을 남겨야, 다음 사람이 같은 자리에서 넘어지지 않습니다."], None, "interlude", ""),
    "03-12": ("순환", None, s03_tidy, "", ""),
    "03-13": ("순환", None, s03_watch, "", ""),
    "03-14": ("정리", None, s03_close, "", ""),
    # 04
    "04-01": ("강의 04 · 통합", ["역할, 작업 흐름, 지식은 따로 배웠지만 실제로는 한 요청 안에서 함께 움직입니다.",
                               "이번 강의는 요청 하나를 처음부터 끝까지 따라가며 결과를 어떻게 확인하고 기록하는지 봅니다."], s04_cover, "cover", "일생"),
    "04-02": ("검증", ["언어 모델은 하지 않은 일도 그럴듯하게 '완료'라고 쓸 수 있습니다. 다음 말을 이어 쓰는 방식 때문입니다.",
                     "그래서 보고를 받으면 파일·테스트·페이지처럼 직접 볼 수 있는 것과 한 줄씩 맞춰 봅니다."], OLD("04", "04-02"), "concept", ""),
    "04-ex": ("실물 예시", ["완료 보고에 적힌 수치를 원자료로 다시 계산합니다.",
                         "보고와 계산이 다르면 실제 확인한 값으로 바로잡습니다."], OLD("04", "04-example-proof"), "concept", ""),
    "04-04": ("요청의 일생", ["매니저를 거치면 요청서와 응답서가 오가고, 직접 맡기면 같은 대화로 답이 옵니다.",
                           "어느 길이든 기록이 필요한 일은 같은 작업 흐름을 지나고, 같은 지식을 읽고 남깁니다."], s04_two_ways, "", ""),
    "04-05": ("두 겹의 확인", ["일한 쪽은 검증 단계에서 실물과 대조해 기록을 남깁니다.",
                           "요청서로 맡긴 경우에는 매니저가 응답서를 받아 다시 대조하고 판정합니다."], s04_double, "", ""),
    "04-06": ("확인의 깊이", ["되돌리기 쉬운 작은 수정은 일한 쪽의 검증으로 충분합니다.",
                           "공개나 운영처럼 되돌리기 어려운 일은 따로 다시 확인합니다. 화면 같은 시각 결과는 매니저가 직접 봅니다."], s04_risk, "", ""),
    "04-07": ("KEY IDEA", ["보고 문장이 아니라 실물이 완료를 정합니다."], None, "interlude", ""),
    "04-08": ("변경 기록", ["JOB이 있으면 그 폴더에 원본을 보관하고, 없으면 파일 옆에 백업을 둡니다.",
                         "언제, 무엇을, 왜 바꿨는지 한 줄로 남겨 두면 나중에 추적하고 되돌릴 수 있습니다."], s04_change, "", ""),
    "04-09": ("참조 구현", ["파일 전달 흐름의 공개 참조 구현과 테스트는 p-hermes 저장소에 있습니다. 공개 범위와 실제 운영의 차이는 위키에서 확인할 수 있습니다.",
                         "개념은 강의에서, 세부 절차와 계약은 위키에서 읽습니다."], s04_repo, "", ""),
    "04-10": ("정리", ["요청 하나가 확인된 결과가 되기까지, 각 강의는 그 길의 한 구간을 맡았습니다.",
                     "위키에는 세부 절차와 계약이, 저장소에는 참조 코드와 테스트가 있습니다."], s04_recap, "", ""),
}

PART_EYEBROW = {"개념": "개념 · 지식이란 무엇인가", "구조": "구조 · 지식은 어떻게 짜여 있나", "순환": "순환 · 지식은 어떻게 돌아가나", "정리": "정리 · 처음 질문으로"}


def next_questions():
    """For each slide key, the question answered by the following slide (across lectures)."""
    flat = [(num, row) for num, _, _, rows in SB.LECTURES for row in rows]
    out = {}
    for i, (num, row) in enumerate(flat):
        q = ""
        for _, nxt in flat[i + 1:]:
            if nxt[2]:
                q = nxt[2]
                break
        out[row[0]] = q
    return out


def section(num, row, nq):
    key, title, q, _, _, _ = row[:6]
    eyebrow, paras, maker, kind, em = SPEC[key]
    if num == "03" and paras is None:
        say, part, sit = row[6], row[7], row[8]
        paras = [say] + ([sit] if sit else [])
        eyebrow = PART_EYEBROW[part] if eyebrow != "강의 03 · 지식" else eyebrow
    if title.startswith("(KEY) "):
        title = title[6:]
    if em:
        assert em in title, (key, em)
        title = title.replace(em, f"<em>{em}</em>", 1)
    stage = ""
    if isinstance(maker, tuple):
        stage = old_sim(maker[1], maker[2])
    elif maker is not None:
        stage = maker()
    k = f' data-kind="{kind}"' if kind else ""
    ps = "".join(f"<p>{p}</p>" for p in paras)
    nxt = f'<p class="next">{nq}</p>' if nq and kind != "interlude" else ""
    kicker = ' data-kicker="KEY IDEA"' if kind == "interlude" else ""
    return (f'<section class="slide" data-eyebrow="{eyebrow}"{k}{kicker} data-slide-key="{key}">\n<h2>{title}</h2>\n'
            f'{stage}\n{ps}{nxt}\n</section>')


def with_style(slides: list[str]) -> list[str]:
    """Inline SVG <style> is document-global: put the shared vocabulary in the first scene once."""
    out, done = [], False
    for s in slides:
        if not done and "<svg" in s and "#deck .dk-scene svg .u-box" not in s:
            s = re.sub(r"(<svg\b[^>]*>)", lambda m: m.group(1) + S.STYLE, s, count=1)
            done = True
        elif "#deck .dk-scene svg .u-box" in s:
            done = True
        out.append(s)
    return out


def main():
    nq = next_questions()
    for num, name, _, rows in SB.LECTURES:
        slides = with_style([section(num, row, nq[row[0]]) for row in rows])
        head = (f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8"><title>{num} · {NAMES[num]}</title></head>\n<body>\n'
                f'<!-- 원고: tools/author.py가 tools/storyboard.py(잠긴 줄기)에서 생성합니다. 직접 고치지 말고 생성기를 고칩니다. -->\n')
        text = A1.rename(head + "\n".join(slides) + "\n</body></html>\n")
        (ROOT / "site/lectures" / FILES[num]).write_text(text, encoding="utf-8")
        print(num, len(slides))


if __name__ == "__main__":
    main()
