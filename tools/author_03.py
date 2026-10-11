"""Author lecture 03 (knowledge) on the shared skeleton positions of tools/scenes.py.

The upper band keeps lecture 01's user / manager / worker positions. Between
manager and worker sits the knowledge funnel (① 후보 → ② 더 찾기 → ③ 원문·실물);
the bottom zone is the knowledge shelf on overview slides and the detail card
on stage slides.
"""
from __future__ import annotations

import re
from pathlib import Path

import scenes as S
from scenes import t, lane, pkt, g, box, scene, person

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site/lectures/03-knowledge.html"


def keep(source, key):
    m = re.search(rf'<section class="slide"[^>]*data-slide-key="{key}"[^>]*>.*?</section>', source, re.S)
    if not m:
        raise KeyError(key)
    return m.group(0)


def set_next(sec, nxt):
    return re.sub(r'<p class="next">.*?</p>', f'<p class="next">{nxt}</p>', sec, count=1, flags=re.S)


def section(key, eyebrow, title, fig, paras, nxt, kind=""):
    k = f' data-kind="{kind}"' if kind else ""
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return (f'<section class="slide" data-eyebrow="{eyebrow}"{k} data-slide-key="{key}">\n<h2>{title}</h2>\n'
            f'{fig}\n{ps}<p class="next">{nxt}</p>\n</section>')


def mobile(*nodes):
    return '<div class="mobile-relationship relation-flow">' + "".join(f'<div class="relation-node">{n}</div>' for n in nodes) + "</div>"


# ------------------------------------------------------------------ knowledge skeleton
def kskel(p, focus, packets=(), shelf=True):
    on = lambda k: k in focus or "all" in focus
    out = []
    # actors (same positions as lecture 01)
    out.append(g('<rect class="u-box" x="30" y="18" width="190" height="76" rx="14"/>' + person(68, 56) + t(140, 57, "사용자", "", 25), dim=not on("user")))
    out.append(g(lane(p, "u2m", "M95 94V180", "gray") + lane(p, "direct", "M220 44H800V180", "blue" if on("direct") else "gray", dash=True)
                 + t(560, 30, "직접 대화", "t-tag c-blue" if on("direct") else "t-tag"), dim=not (on("direct") or on("user"))))
    out.append(g(box(30, 186, 190, 156, "m-box", "매니저", "판단·위임·판정", 27, 16), dim=not on("mgr")))
    out.append(g(box(790, 186, 180, 156, "w-box", "워커", "직접 대화·요청서 실행", 27, 15), dim=not on("wkr")))
    # funnel
    out.append(g(t(335, 170, "① 후보", "t-tag c-amber")
                 + '<rect class="card amber" x="250" y="186" width="170" height="74" rx="12"/>' + t(335, 212, "자료 묶음", "t-md") + t(335, 238, "요청서 실행 · 자동", "t-sm", 14)
                 + '<rect class="card blue" x="250" y="268" width="170" height="74" rx="12"/>' + t(335, 294, "직접 찾기", "t-md") + t(335, 320, "직접 대화 · 관련 작업", "t-sm", 14),
                 dim=not on("s1")))
    out.append(g(lane(p, "mpack", "M220 223H246", "mint", dash=True), dim=not on("s1")))
    out.append(g(t(525, 170, "② 더 찾기", "t-tag")
                 + '<rect class="card" x="450" y="186" width="150" height="156" rx="12"/>' + t(525, 246, "빈 곳만", "t-md") + t(525, 276, "새 질문 ·", "t-sm", 15) + t(525, 298, "비었거나 잘림", "t-sm", 15),
                 dim=not on("s2")))
    out.append(g(t(695, 170, "③ 판단", "t-tag c-mint")
                 + '<rect class="card mint" x="630" y="186" width="130" height="156" rx="12"/>' + t(695, 246, "원문", "t-md") + t(695, 276, "+", "t-sm", 15) + t(695, 300, "현재 파일", "t-md"),
                 dim=not on("s3")))
    hot = lambda a, b: on(a) or on(b)
    out.append(g(lane(p, "f12", "M420 264H446", "amber" if hot("s1", "s2") else "gray"), dim=not hot("s1", "s2")))
    out.append(g(lane(p, "f23", "M600 264H626", "gray"), dim=not hot("s2", "s3")))
    out.append(g(lane(p, "f3w", "M760 264H786", "mint" if hot("s3", "wkr") else "gray"), dim=not hot("s3", "wkr")))
    if shelf:
        cards = [(50, "교훈", "사건·해결"), (232, "이전 결정", "JOB 기록"), (414, "프로젝트", "지식"), (596, "정본", "현재 파일"), (778, "규칙·기억·스킬", "세션 시작")]
        sh = '<rect class="card know" x="40" y="430" width="920" height="96" rx="14"/>' + t(56, 446, "지식", "t-tag c-amber", anchor="start")
        for x, h, s in cards:
            sh += f'<rect class="chip" x="{x + 10}" y="456" width="152" height="58" rx="10"/>' + t(x + 86, 476, h, "", 18) + t(x + 86, 500, s, "t-sm", 13)
        out.append(g(sh, dim=not on("shelf")))
        feeds = [("k1", "M335 452V346", "amber", "교훈·결정·프로젝트", 335), ("k2", "M525 452V346", "gray", "색인·의미 검색", 525),
                 ("k3", "M695 452V346", "mint", "원문·현재 파일", 695), ("k4", "M864 452V346", "blue", "세션 시작 때 읽음", 864)]
        for pid, d, c, label, x in feeds:
            out.append(g(lane(p, pid, d, c) + t(x + 8, 392, label, "t-sm", 14, anchor="start"), dim=not on("feeds")))
    out.extend(packets)
    return "".join(out)


# ------------------------------------------------------------------ scenes
def s_cover():
    p = "k1c"
    pk = (pkt(p, "k1", "amber", 1.4, .3), pkt(p, "k2", "", 1.4, 1.1), pkt(p, "k3", "", 1.4, 1.9), pkt(p, "k4", "blue", 1.4, 2.7),
          pkt(p, "f3w", "", .6, 3.6))
    body = S.STYLE + kskel(p, {"shelf", "feeds", "wkr", "mgr", "s1", "s2", "s3"}, pk)
    return scene(p, body, "지식 선반에서 후보, 추가 검색, 원문과 현재 파일이 위로 올라와 매니저와 워커의 판단을 받친다",
                 on_map=("know",), mobile=mobile("세션 시작: 규칙·기억·스킬", "작업 전: 자료 묶음", "작업 중: 더 찾기", "판단: 원문·현재 파일"))


def s_funnel():
    p = "k4"
    body = kskel(p, {"s1", "s2", "s3", "wkr", "user", "direct", "mgr", "feeds", "shelf"}, (
        pkt(p, "direct", "blue", 2.6, .3), pkt(p, "f12", "amber", .6, 2.2), pkt(p, "f23", "", .6, 3.0), pkt(p, "f3w", "", .6, 3.8)))
    return scene(p, body, "지식은 후보, 더 찾기, 원문과 현재 파일의 세 단계 깔때기로 쓰이며, 진입 경로에 따라 다른 것은 첫 단계뿐이다",
                 on_map=("know", "wkr"), mobile=mobile("① 후보: 자료 묶음 또는 직접 찾기", "② 빈 곳만 더 찾기", "③ 원문과 현재 파일로 판단"))


def s_stage1():
    p = "k5"
    body = kskel(p, {"s1", "mgr", "wkr"}, (pkt(p, "mpack", "", .8, .3),), shelf=False)
    body += '<rect class="mo-pulse amber" x="250" y="186" width="170" height="74" rx="12"/>'
    body += '<path class="lead" d="M335 342V398"/>'
    body += '<rect class="card amber" x="40" y="398" width="920" height="128" rx="14"/>'
    body += t(60, 418, "자료 묶음 첫 줄의 상태 → 다음 행동", "t-tag c-amber", anchor="start")
    rows = [("찾음", "후보를 읽고 진행", "mint"), ("잘림", "핵심어로 한 번 더 찾기", "amber"),
            ("관련 없음", "다른 표현으로 한 번 더", "amber"), ("검색 오류·원본 없음", "직접 검색으로 대신, 결과에 적기", "coral")]
    for k, (st, act, c) in enumerate(rows):
        x = 58 + k * 226
        body += g(f'<rect class="card {c}" x="{x}" y="434" width="210" height="78" rx="10"/>' + t(x + 105, 460, st, "t-md", 18) + t(x + 105, 490, act, "t-sm", 14), build=k + 1)
    body += t(125, 364, "JOB 시작 때 같은 도구로", "t-sm c-mint", 14)
    return scene(p, body, "자료 묶음은 출처·날짜와 함께 후보와 검색 상태를 주고, 상태에 따라 다음 행동이 정해진다",
                 on_map=("know", "lanes"), mobile=mobile("찾음 → 진행", "잘림 → 한 번 더", "관련 없음 → 다른 표현으로", "검색 오류 → 직접 검색"))


def s_stage2():
    p = "k7"
    body = kskel(p, {"s2", "wkr"}, (pkt(p, "f12", "amber", .6, .3),), shelf=False)
    body += '<rect class="mo-pulse" x="450" y="186" width="150" height="156" rx="12"/>'
    body += '<path class="lead" d="M525 342V398"/>'
    body += g('<rect class="card" x="40" y="398" width="440" height="128" rx="14"/>' + t(60, 420, "언제 더 찾나", "t-tag", anchor="start")
              + t(60, 452, "· 작업 중 새로 생긴 질문", "t-sm", 16, anchor="start") + t(60, 480, "· 자료 묶음이 비었거나 잘렸거나 실패했을 때", "t-sm", 16, anchor="start")
              + t(60, 508, "· 이미 나온 후보는 다시 찾지 않는다", "t-sm c-coral", 16, anchor="start"), build=1)
    body += g('<rect class="card" x="500" y="398" width="460" height="128" rx="14"/>' + t(520, 420, "어떻게 찾나 — 같은 질문 “시간 부족”", "t-tag", anchor="start")
              + '<rect class="card amber" x="520" y="436" width="200" height="74" rx="10"/>' + t(620, 460, "단어 검색", "t-md", 18) + t(620, 488, "‘시간 초과’는 놓침", "t-sm c-coral", 14)
              + '<rect class="card mint" x="740" y="436" width="200" height="74" rx="10"/>' + t(840, 460, "의미 검색", "t-md", 18) + t(840, 488, "표현이 달라도 찾음", "t-sm c-mint", 14), build=2)
    return scene(p, body, "자료 묶음이 비었거나 잘렸을 때와 작업 중 새 질문만 더 찾고, 단어 검색이 놓치는 표현은 의미 검색으로 보완한다",
                 on_map=("know", "wkr"), mobile=mobile("새 질문만", "비었거나 잘렸을 때", "단어 검색 + 의미 검색"))


def s_stage3():
    p = "k8"
    body = kskel(p, {"s3", "wkr"}, (pkt(p, "f3w", "", .7, .3),), shelf=False)
    body += '<rect class="mo-pulse" x="630" y="186" width="130" height="156" rx="12"/>'
    body += '<path class="lead" d="M695 342V398"/>'
    body += g('<rect class="card amber" x="40" y="398" width="300" height="128" rx="14"/>' + t(190, 428, "후보", "t-md") + t(190, 460, "자료 묶음 · 검색 결과 · 요약", "t-sm", 15) + t(190, 488, "그대로 근거로 쓰지 않는다", "t-sm c-coral", 15), build=1)
    body += g(lane(p, "a1", "M344 462H366") + '<rect class="card" x="370" y="398" width="270" height="128" rx="14"/>' + t(505, 428, "교훈 원문", "t-md") + t(505, 460, "날짜·출처로", "t-sm", 15) + t(505, 488, "적용 범위 확인", "t-sm", 15), build=2)
    body += g(lane(p, "a2", "M644 462H666", "mint") + '<rect class="card mint" x="670" y="398" width="290" height="128" rx="14"/>' + t(815, 428, "현재 파일", "t-md") + t(815, 460, "지금 상태는 실물로", "t-sm", 15) + t(815, 488, "다르면 실물을 따른다", "t-sm c-mint", 15), build=3)
    return scene(p, body, "후보는 교훈 원문으로 적용 범위를, 현재 파일로 지금 상태를 확인한 뒤에야 판단 근거가 된다",
                 on_map=("know", "wkr"), mobile=mobile("후보", "교훈 원문: 적용 범위", "현재 파일: 지금 상태"))


def main():
    src = SRC.read_text(encoding="utf-8")
    old = {k: keep(src, k) for k in ("03-01", "03-02", "03-04", "03-05", "03-example-source", "03-08", "03-09", "03-10", "03-11")}
    slides = [
        section("03-01", "강의 03 · 지식", "지식은 에이전트의 <em>모든 판단</em> 밑에 있습니다", s_cover(),
                ["워커는 세션을 시작할 때 규칙·기억·스킬을 읽고, 일을 하면서 교훈·이전 결정·현재 파일을 꺼내 씁니다. 매니저도 같은 선반을 씁니다.",
                 "이 강의는 지식이 어디에 쌓이고, 어떤 순서로 꺼내 쓰이며, 작업 뒤에 어떻게 다시 쌓이는지 봅니다."],
                "에이전트에게 지식이란 무엇일까요?", "cover"),
        set_next(old["03-02"], "기록은 무엇을 어디에 남길까요?"),
        set_next(old["03-04"], "쌓인 지식은 어떤 순서로 꺼내 쓸까요?"),
        section("03-funnel", "깔때기", "지식은 <em>후보 → 원문 → 실물</em> 순서로 씁니다", s_funnel(),
                ["첫 단계는 후보를 받는 것입니다. 요청서로 실행되면 작업 실행기가 자료 묶음을 붙여 주고, 직접 대화에서는 워커가 관련 작업일 때 직접 찾습니다. 진입 경로에 따라 다른 것은 이 첫 단계뿐입니다.",
                 "그다음 빈 곳만 더 찾고, 마지막에 교훈 원문과 현재 파일로 판단합니다. 이 순서는 매니저와 워커 모두 같습니다."],
                "자료 묶음에는 무엇이 들어 있을까요?", "concept"),
        section("03-pack", "① 후보", "자료 묶음은 후보와 <em>검색 상태</em>를 함께 줍니다", s_stage1(),
                ["작업 실행기는 요청서의 제목과 목표로 교훈·이전 결정·프로젝트 지식을 찾아, 출처·날짜와 함께 짧은 목록으로 붙입니다. 매니저도 JOB을 시작할 때 같은 도구를 씁니다.",
                 "첫 줄의 상태를 봅니다. 비었거나 잘렸거나 검색이 실패했다면, 자료가 없다는 뜻이 아니므로 한 번 더 찾습니다."],
                "출처와 날짜가 적힌 후보를 함께 볼까요?"),
        set_next(old["03-example-source"], "후보만으로 모자라면 언제 더 찾을까요?"),
        section("03-search", "② 더 찾기", "빈 곳만 더 찾고, 이미 본 후보는 다시 찾지 않습니다", s_stage2(),
                ["작업 중 새로 생긴 질문이나, 자료 묶음이 비었거나 잘렸을 때만 직접 찾습니다. 같은 후보를 두 번 찾는 데 시간을 쓰지 않습니다.",
                 "단어 검색은 같은 단어가 들어간 기록만 찾습니다. 뜻은 같고 표현이 다른 기록은 의미 검색으로 보완하고, 긴 조사는 하위 에이전트로 나눕니다."],
                "찾은 후보는 그대로 근거가 될까요?"),
        section("03-verify", "③ 판단", "판단은 교훈 원문과 <em>현재 파일</em>로 합니다", s_stage3(),
                ["자료 묶음·검색 결과·요약은 모두 후보입니다. 교훈 원문에서 그때의 원인과 날짜를 보고 오늘 적용할 수 있는지 판단합니다.",
                 "지금 상태는 언제나 현재 파일로 확인합니다. 후보와 실물이 다르면 실물을 따르고, 그 차이가 다시 쓸 만하면 교훈으로 남깁니다."],
                "작업 단위에서는 지식이 어떻게 돌까요?"),
        set_next(old["03-05"], "작업이 끝나면 무엇을 남길까요?"),
        set_next(old["03-08"], "후보는 언제 절차가 될까요?"),
        old["03-09"],
        set_next(old["03-10"], "기록은 매일 어떻게 정리될까요?"),
        set_next(old["03-11"], "이 모든 조각이 요청 하나에서 어떻게 함께 움직일까요?"),
    ]
    head = src[: src.find("<section")]
    SRC.write_text(head + "\n".join(slides) + "\n</body></html>\n", encoding="utf-8")
    print("slides", len(slides))


if __name__ == "__main__":
    main()
