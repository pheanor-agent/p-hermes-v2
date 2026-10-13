"""Lecture 01 scenes on the shared skeleton (tools/scenes.py), used by tools/author.py.

Keeps simulator, interlude and the request example slides from the current
source and rewrites the diagram slides so every scene reuses the same fixed
user / manager / worker / lane positions.
"""
from __future__ import annotations

import re
from pathlib import Path

import scenes as S
from scenes import t, lane, pkt, g, box, doc, skeleton, scene

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site/lectures/01-orchestrator-worker.html"


def keep(source: str, key: str) -> str:
    m = re.search(rf'<section class="slide"[^>]*data-slide-key="{key}"[^>]*>.*?</section>', source, re.S)
    if not m:
        raise KeyError(key)
    return m.group(0)


def section(key, eyebrow, title, fig, paras, nxt, kind=""):
    k = f' data-kind="{kind}"' if kind else ""
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return (f'<section class="slide" data-eyebrow="{eyebrow}"{k} data-slide-key="{key}">\n<h2>{title}</h2>\n'
            f'{fig}\n{ps}<p class="next">{nxt}</p>\n</section>')


def mobile(*nodes, flow=False):
    cls = "relation-flow" if flow else "relation-parts"
    return f'<div class="mobile-relationship {cls}">' + "".join(f'<div class="relation-node">{n}</div>' for n in nodes) + "</div>"


# ------------------------------------------------------------------ scenes
def s_cover():
    p = "c1"
    body = S.STYLE + skeleton(p, {"all"}, (
        pkt(p, "u2m", "", 1.4, 0.4), pkt(p, "l1", "amber", .9, 1.4), pkt(p, "l5", "amber", 1.0, 2.4),
        pkt(p, "r1", "amber", 1.0, 4.6), pkt(p, "r2", "amber", 1.2, 5.6), pkt(p, "m2u", "", 1.4, 6.9),
        pkt(p, "direct", "blue", 3.0, 2.2), pkt(p, "reply", "blue", 2.6, 5.4)))
    body += g(t(500, 420, "사용자는 매니저와 대화하거나, 워커와 직접 대화합니다", "t-md")
              + t(500, 456, "매니저가 맡길 때는 요청서와 응답서, 두 파일로만 주고받습니다", "t-sm", 18), cls="mo-rise")
    return scene(p, body, "사용자와 매니저, 작업 에이전트가 요청서와 응답서로 이어진 위임 경로",
                 mobile=mobile("사용자", "매니저: 판단", "요청서 ⇄ 응답서", "작업자: 수행"))


def s_context():
    p = "c2"
    body = skeleton(p, {"mgr", "wkr", "doc", "lane_bot", "lane_top"}, labels=False)
    body += g(t(125, 300, "목표·경계만", "t-tag c-mint") + t(880, 300, "요청서 + 실행 로그", "t-tag c-blue"))
    # problem strip: one context window overflowing
    strip = ['<rect class="card coral" x="40" y="392" width="920" height="132" rx="14"/>',
             t(60, 414, "혼자 다 하면 — 맥락 창 하나에 전부", "t-tag c-coral", anchor="start")]
    strip.append('<rect class="card" x="60" y="430" width="880" height="76" rx="10"/>')
    strip.append(g('<rect class="card coral" x="70" y="442" width="150" height="52" rx="8"/>' + t(145, 468, "목표·완료 조건", "t-sm c-coral", 16), cls="mo-shake"))
    for k in range(7):
        x = 232 + k * 100
        strip.append(f'<g class="mo-rise" style="--d:{k + 2}"><rect class="chip" x="{x}" y="442" width="90" height="52" rx="8"/>{t(x + 45, 468, f"로그 {k + 1}", "t-sm", 16)}</g>')
    body += "".join(strip)
    return scene(p, body, "한 에이전트의 맥락 창이 실행 로그로 차서 목표가 밀려나는 문제와, 매니저와 작업 에이전트로 나눈 해결",
                 mobile=mobile("혼자: 목표가 밀려남", "나누면: 매니저는 목표·경계", "작업자: 요청서 + 로그"))


def s_files():
    p = "c3"
    body = skeleton(p, {"mgr", "wkr", "doc", "lane_bot", "lane_top"}, (
        pkt(p, "l1", "amber", .9, .3), pkt(p, "l5", "amber", 1.0, 1.3), pkt(p, "r1", "amber", 1.1, 3.6), pkt(p, "r2", "amber", 1.3, 4.6)))
    body += g('<rect class="card" x="180" y="400" width="640" height="118" rx="14"/>'
              + t(500, 432, "파일은 세션이 끊겨도 남습니다", "t-md")
              + t(500, 468, "누가 언제 읽어도 같은 내용 — 약속(요청서)과 결과(응답서)를 다시 대조할 수 있다", "t-sm", 17)
              + t(500, 498, "통신은 파일로만, 대화 채널에 직접 게시하지 않는다", "t-sm c-amber", 16), cls="mo-rise")
    body += f'<path class="lead" d="M290 247V398"/><path class="lead" d="M588 344V398"/>'
    return scene(p, body, "매니저가 쓴 요청서가 작업 에이전트에게 가고, 응답서가 같은 길로 돌아오는 파일 통신",
                 mobile=mobile("요청서 전달", "산출 생성", "같은 ID로 응답", flow=True))


def s_modes():
    p = "c4"
    body = skeleton(p, {"user", "wkr", "direct"}, (
        pkt(p, "u2m", "", 1.4, .4), pkt(p, "direct", "blue", 2.6, 1.2), pkt(p, "reply", "blue", 2.4, 4.0)))
    cards = [
        (40, "mint", "매니저와 대화", ["매니저가 판단하고", "직접 하거나 워커에 맡긴다"], "c-mint"),
        (360, "blue", "워커와 직접 대화", ["워커가 매니저 역할을 겸하고", "답은 같은 대화로 돌려준다"], "c-blue"),
        (680, "amber", "요청서로 실행", ["요청서대로 끝까지 수행하고", "답은 응답서 파일로"], "c-amber"),
    ]
    for k, (x, c, head, lines, tc) in enumerate(cards, 1):
        body += g(f'<rect class="card {c}" x="{x}" y="398" width="280" height="122" rx="14"/>'
                  + t(x + 140, 428, head, f"t-md {tc}") + t(x + 140, 462, lines[0], "t-sm", 17) + t(x + 140, 490, lines[1], "t-sm", 17),
                  build=k)
    body += '<path class="lead" d="M125 342V396"/><path class="lead" d="M507 50V396"/><path class="lead" d="M880 342V396"/>'
    return scene(p, body, "사용자가 매니저와 대화하는 경우, 워커와 직접 대화하는 경우, 워커가 요청서로 실행되는 경우의 역할 차이",
                 mobile=mobile("매니저와 대화 → 매니저가 판단", "워커와 직접 대화 → 워커가 매니저 역할 겸함", "요청서로 실행 → 워커"))


def s_why():
    p = "c5"
    body = skeleton(p, {"mgr", "wkr", "lane_bot", "doc", "lane_top"}, labels=False)
    items = [(40, "mint", "① 맥락 보존", "매니저는 실행 로그 없이", "목표와 경계를 붙든다", "M125 342V396"),
             (360, "amber", "③ 확인 분리", "만든 쪽이 아닌 매니저가", "응답서를 실물과 대조", "M588 344V396"),
             (680, "blue", "② 끝까지 수행", "작업은 요청서만 보고", "응답서까지 한 번에", "M880 342V396")]
    for k, (x, c, head, a, b, lead) in enumerate(items, 1):
        body += g(f'<path class="lead" d="{lead}"/><rect class="card {c}" x="{x}" y="398" width="280" height="122" rx="14"/>'
                  + t(x + 140, 430, head, "t-md") + t(x + 140, 464, a, "t-sm", 17) + t(x + 140, 492, b, "t-sm", 17), build=k)
    return scene(p, body, "역할을 나누면 지켜지는 세 가지: 맥락 보존, 끝까지 수행, 확인 분리",
                 mobile=mobile("목표 유지", "실행 집중", "결과 독립 대조"))


def s_request():
    p = "c8"
    body = skeleton(p, {"mgr", "doc", "l1"}, (pkt(p, "l1", "amber", .8, .3),))
    body += '<rect class="mo-pulse amber" x="245" y="183" width="90" height="64" rx="6"/>'
    body += '<path class="lead" d="M245 247L60 398M335 247L940 398"/>'
    body += '<rect class="card amber" x="40" y="398" width="920" height="128" rx="14"/>'
    fields = [("목표", "사용자 원 요청 전체"), ("완성 기준", "필수 5개 이내 · 나머지 선택"),
              ("참조 경로", "배경·이력은 절대경로로"), ("금지 범위", "4개 범주 + 사용자 명시분")]
    for k, (h, s) in enumerate(fields):
        x = 58 + k * 226
        c = "coral" if h == "금지 범위" else ("mint" if h == "목표" else "")
        body += g(f'<rect class="card {c}" x="{x}" y="414" width="210" height="76" rx="10"/>' + t(x + 105, 438, h, "t-md") + t(x + 105, 468, s, "t-sm", 15), build=k + 1)
    body += t(500, 510, "중간 보고·방어 문구·요청과 무관한 메타 작업은 넣지 않는다", "t-sm c-coral", 15)
    return scene(p, body, "요청서를 펼친 네 칸: 목표, 완성 기준, 참조 경로, 금지 범위",
                 mobile=mobile("목표", "완성 기준", "참조 경로", "금지 범위"))


def s_register():
    p = "c10"
    body = skeleton(p, {"reg", "runner", "lane_top"}, detail=True, packets=(
        pkt(p, "l2", "amber", .7, .3), pkt(p, "l3", "amber", .7, 1.0), pkt(p, "l5", "amber", .9, 1.7),
        pkt(p, "pack", "", 1.2, 1.0)))
    body += t(428, 266, "유일한 등록 경로", "t-sm c-amber", 15)
    body += g('<rect class="card know" x="560" y="430" width="230" height="80" rx="12"/>'
              + t(675, 456, "작업 전 자료 묶음", "t-md") + t(675, 486, "관련 교훈 · 이전 결정", "t-sm", 16)
              + lane(p, "pack", "M675 428V380H643V252", "mint"), build=1)
    body += g('<rect class="card" x="40" y="430" width="380" height="80" rx="12"/>'
              + t(230, 456, "등록할 때 요청 ID가 붙는다", "t-md") + t(230, 486, "응답서도 같은 ID로 돌아온다", "t-sm", 16)
              + '<path class="lead" d="M428 247V428"/>', build=2)
    return scene(p, body, "요청서가 요청 등록과 작업 실행기를 거쳐 워커에게 가고, 실행기가 작업 전 자료 묶음을 함께 전달",
                 on_map=("lanes", "wkr"), mobile=mobile("요청 등록", "참조·교훈 묶음", "작업자 실행", flow=True))


def s_ids():
    p = "c11"
    body = skeleton(p, {"reg", "lane_bot"}, detail=True)
    body += '<rect class="mo-pulse" x="365" y="183" width="127" height="64" rx="14"/>'
    body += '<path class="lead" d="M428 247V392"/>'
    body += '<rect class="card mint" x="60" y="392" width="880" height="34" rx="10"/>' + t(500, 410, "하나의 목표 — 문의 회고 초안", "t-tag c-mint")
    tries = [(60, "amber", "R-예시-01", "일부 완료 · 시간 부족"), (360, "", "R-예시-02", "원인 1줄 + 바꾼 점 1줄"), (660, "mint", "R-예시-03", "완료 · 산출과 대조")]
    for k, (x, c, rid, st) in enumerate(tries, 1):
        arrow = lane(p, f"a{k}", f"M{x - 40} 482H{x - 6}") if k > 1 else ""
        body += g(arrow + f'<path class="lead" d="M{x + 140} 426V440"/><rect class="card {c}" x="{x}" y="440" width="280" height="84" rx="12"/>'
                  + t(x + 140, 466, f"시도 {k} · {rid}", "t-md") + t(x + 140, 498, st, "t-sm", 16), build=k)
    return scene(p, body, "하나의 목표 아래 시도마다 새 요청 ID를 받고, 응답서는 자기 시도의 ID를 가리킨다",
                 on_map=("lanes",), mobile=mobile("같은 목표", "시도 1 / 2 / 3", "시도마다 새 요청 ID"))


def s_response():
    p = "c12"
    body = skeleton(p, {"wkr", "lane_bot", "mgr"}, (pkt(p, "r1", "amber", 1.0, .2),))
    body += '<rect class="mo-pulse amber" x="542" y="280" width="92" height="64" rx="6"/>'
    states = [(40, "mint", "완료", "필수 항목이 쓸 만함"), (270, "amber", "일부 완료", "누락 · 시간 부족"),
              (500, "coral", "실행 실패", "오류로 산출 실패"), (730, "coral", "진행 보류", "승인·입력·권한 필요")]
    for k, (x, c, h, s) in enumerate(states):
        cx = x + 115
        body += lane(p, f"s{k}", f"M588 346C588 400 {cx} 380 {cx} 440", {"mint": "mint", "amber": "amber"}.get(c, "coral"))
        body += f'<rect class="card {c}" x="{x}" y="444" width="230" height="80" rx="12"/>' + t(cx, 470, h, "t-md") + t(cx, 500, s, "t-sm", 15)
        body += pkt(p, f"s{k}", c if c != "mint" else "", 1.2, 1.4 + k * 1.6, 6)
    return scene(p, body, "응답서는 같은 요청 ID와 네 가지 처리 상태 중 하나를 담아 매니저에게 돌아온다",
                 on_map=("lanes", "mgr"), mobile=mobile("완료", "일부 완료", "실패", "진행 보류"))


def s_approval():
    p = "c14"
    body = skeleton(p, {"user", "mgr", "wkr", "direct"}, labels=False)
    # approval request goes up from manager to the user and comes back as a stamp
    body += lane(p, "ask", "M125 186V100", "coral", draw=0) + t(112, 143, "승인 요청", "t-tag c-coral", anchor="end")
    body += pkt(p, "ask", "coral", 1.4, .6)
    body += g('<circle cx="236" cy="56" r="20" fill="#3a2224" stroke="#ff9f8f" stroke-width="2.5"/>' + t(236, 57, "원문", "t-sm c-coral", 13), build=2)
    body += t(830, 160, "직접 대화 워커도 같다", "t-sm c-blue", 15)
    body += '<rect class="card coral" x="250" y="390" width="710" height="134" rx="14"/>'
    body += t(270, 414, "사용자 원문이 있어야 실행 — 매니저도, 직접 대화 워커도 대신 승인하지 않는다", "t-tag c-coral", anchor="start")
    cats = [("영구 삭제", "되돌릴 수 없는 삭제"), ("외부 전송·게시", "보내거나 게시"), ("자격증명·보안", "권한·보안 설정"), ("운영 원칙", "POLICY 개정")]
    for k, (h, s) in enumerate(cats):
        x = 266 + k * 172
        body += g(f'<rect class="card" x="{x}" y="430" width="160" height="78" rx="10"/>' + t(x + 80, 456, h, "t-md", 18) + t(x + 80, 486, s, "t-sm", 14), build=1)
    body += g('<rect class="card" x="40" y="390" width="190" height="134" rx="14"/>' + t(135, 430, "그 밖의 결정", "t-md")
              + t(135, 462, "근거·가정을 기록하고", "t-sm", 15) + t(135, 486, "스스로 진행", "t-sm", 15) + t(135, 510, "무응답 ≠ 승인", "t-sm c-coral", 15), build=3)
    body += '<path class="lead" d="M125 342V388"/>'
    return scene(p, body, "네 가지 범주는 매니저가 사용자에게 승인을 요청하고 사용자 원문이 있어야 실행한다",
                 on_map=("user", "mgr"), mobile=mobile("영구 삭제", "외부 전송·게시", "자격증명·보안 설정", "운영 원칙 수정"))


def rename(text: str) -> str:
    for a, b in (("작업 에이전트(워커)", "워커"), ("작업 에이전트", "워커"), ("작업자:", "워커:"), ("작업자 실행", "워커 실행"), ("작업 쪽은", "워커 쪽은"), ("작업은 요청서만", "워커는 요청서만")):
        text = text.replace(a, b)
    return text
