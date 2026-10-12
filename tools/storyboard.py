"""Render the lecture storyboard (00, 01, 02, 04) as one review page.

Each slide row lists the question it answers; the 'next question' of a slide is
the question of the following slide, so the chain is consistent by construction.
Thumbnails are the canonical map (tools/scenes.py) with the slide's focus lit.
Output: docs/storyboard/index.html (review only, not linked from the site).
"""
from __future__ import annotations

from html import escape
from pathlib import Path

import scenes as S

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/storyboard/index.html"

# (key, title, question it answers, figure/motion note, status, focus)
TOP = {"user", "mgr", "wkr", "u2m", "direct", "lane_top", "lane_bot"}
VIA = {"user", "mgr", "wkr", "u2m", "lane_top", "lane_bot"}
DIRECT = {"user", "wkr", "direct"}
WF = {"wkr", "entry", "rail", "job"}
L00 = ("00", "전체 그림", "왜 구조가 필요한가", [
    ("00-01", "요청 하나가 확인된 결과가 되기까지, 그 과정 전체를 한 장의 지도로 볼 수 있습니다.", "", "전체 지도가 위(역할)→가운데(작업 흐름)→아래(지식) 순서로 그려지고, 요청 점이 '매니저에게' 또는 '워커에게 직접' 두 길 중 하나로 들어간다", "수정·모션", {"all"}),
    ("00-02", "언어 모델은 읽어 들인 문맥 안에서만 다음 말을 이어 씁니다.", "언어 모델은 무엇을 읽고 무엇을 쓸까요?", "현행 유지(맥락 창); 200행 격자에서 3행만 맥락 창으로 → 요약 2/3 vs 실제 20%", "수정·모션", set()),
    ("00-03", "여기에 도구와 반복을 더하면, 말만이 아니라 실제 일을 하는 에이전트가 됩니다.", "말만 이어 쓰는 모델이 어떻게 실제 일을 할까요?", "현행 순환 장면", "유지", set()),
    ("00-04", "그런데 대화 기록만으로는 긴 일을 끝까지 이어 가기 어렵습니다.", "대화 하나로 긴 일을 끝까지 이어 갈 수 있을까요?", "세션 1이 끊김 → 요청서·JOB·응답서는 남음 → 다음 세션이 읽음", "수정·모션", set()),
    ("00-05", "그래서 요청과 결과를 대화 밖의 파일로 남겨, 언제든 다시 읽을 수 있게 합니다.", "", "유지", "유지", set()),
    ("00-06", "이렇게 남는 기록을 한눈에 보려면, 전체를 세 층으로 나눠 보면 됩니다.", "이런 기록은 전체 체계의 어디에 놓일까요?", "전체 지도를 세 띠로 보여 줌. 지식 블록은 연결 띠 하나로 위 전체와 이어짐", "수정", {"all"}),
    ("00-entry", "일을 맡기는 길은 두 가지입니다. 매니저에게 맡기거나, 워커에게 직접 맡기거나.", "맨 위 층에서는 누가 누구와 이야기할까요?", "위 띠: ① 매니저에게 맡기면 요청서·응답서로 워커에게 ② 워커에게 직접 맡기면 같은 대화로 답", "신규", TOP),
    ("00-07", "매니저는 판단하고 맡기고 판정하고, 워커는 일을 끝까지 수행합니다.", "매니저는 무엇을 맡을까요?", "사용자–매니저 대화와 매니저 강조", "수정", {"user", "mgr", "u2m"}),
    ("00-08", "기록이 필요한 일은 정해진 단계를 지나며, 그 자리마다 기록이 남습니다.", "여러 단계에 걸친 일은 어디에 기록할까요?", "가운데 띠: 워커가 '기록이 필요한가?'를 거쳐 요청▮실행▮검증▮완료, JOB 폴더", "수정", WF),
    ("00-09", "이 모든 동작은 쌓아 둔 지식을 읽으며 움직입니다.", "에이전트와 작업 흐름은 무엇을 읽고 움직일까요?", "지식 블록 전체가 연결 띠로 위 전체와 이어짐. 아래 점선 띠(매일 수집→가공·색인→야간 대조→점검)는 이름만 보여 주고 상세는 강의 03", "수정", {"know", "kconn"}),
    ("00-10", "결과는 말이 아니라 실물을 보고 확인합니다.", "보고된 결과는 그대로 믿어도 될까요?", "두 겹: 일한 쪽(워커)의 검증 단계 + 맡긴 경우에만 매니저의 응답서 판정", "수정", {"rail", "lane_bot", "mgr"}),
    ("00-11", "이 지도의 각 층을 차례로 확대해 보는 것이 이어지는 강의의 순서입니다.", "", "다섯 층을 차례로 확대한 지도로 정리", "신규", {"all"}),
])
L01 = ("01", "매니저와 워커", "누가 무엇을 주고받나", [
    ("01-01", "매니저는 판단하고, 워커는 끝까지 수행합니다. 이 강의는 두 역할이 무엇을 주고받는지 봅니다.", "두 역할은 정확히 무엇을 주고받을까요?", "위 띠 전체 + 두 길 토큰", "수정", TOP),
    ("01-02", "에이전트 하나가 모든 것을 기억하며 하기에는, 한 번에 읽을 수 있는 양이 부족합니다.", "에이전트 하나로는 왜 부족할까요?", "골격 + '혼자 다 하면' 로그 띠", "유지(시범)", {"mgr", "wkr"}),
    ("01-03", "그래서 일을 나누고, 나눈 경계를 파일로 주고받습니다.", "맡긴 일과 결과는 어떻게 주고받을까요?", "요청서·응답서 경로 토큰", "유지(시범)", VIA),
    ("01-modes", "워커에게는 직접 맡기는 길도 있습니다. 이때는 요청서 없이 같은 대화에서 판단부터 실행까지 이어집니다.", "사용자는 언제나 매니저를 거쳐야 할까요?", "전용 모션: [매니저에게 맡기기 | 워커에게 직접] 전환. 직접일 때 매니저는 흐려지고, 워커가 판단까지 맡아 같은 대화로 답(요청서·응답서 없음)", "재작성·모션", DIRECT),
    ("01-04", "역할을 나누면 세 가지가 지켜집니다. 판단의 맥락이 보존되고, 맡긴 일은 끝까지 수행되고, 확인이 따로 이루어집니다.", "매니저를 거치면 무엇이 달라질까요?", "맥락 보존·끝까지 수행·확인 분리", "유지(시범)", VIA),
    ("01-05", "(KEY) 매니저가 판단하고, 워커가 실행합니다.", "", "유지", "유지", set()),
    ("01-06", "무엇을 직접 할지는 일의 무게와 판단의 종류로 정합니다. 읽고 조사하고 작게 고치는 일은 매니저가 직접 합니다.", "매니저는 무엇을 직접 하고 무엇을 맡길까요?", "시뮬레이터 + 예외 설명: 읽기·조사·작은 수정은 매니저가 직접", "수정", {"mgr"}),
    ("01-user-choice", "사용자도 같은 기준으로 길을 고릅니다. 간단하고 되돌릴 수 있는 일은 워커에게 직접, 어렵거나 창의적인 일은 매니저에게 맡깁니다.", "사용자는 어떤 길을 고를까요?", "사용자 기준으로 두 경로를 나란히 비교", "신규", DIRECT),
    ("01-model-weight", "어울리는 모델의 무게도 역할마다 다릅니다. 가벼운 모델로 워커 일을 맡기면 비용을 아끼고, 무거운 모델로 판단을 맡기면 대화가 쾌적해집니다.", "역할마다 어울리는 모델의 무게는 어떻게 다를까요?", "가벼운 모델=워커, 무거운 모델=매니저 원칙", "신규", {"mgr", "wkr"}),
    ("01-07", "맡길 때 요청서에 적을 것은 네 칸이면 충분합니다. 목표, 완성 기준, 참조 경로, 금지 범위입니다.", "맡기기로 했다면 요청서에는 무엇을 적을까요?", "요청서 펼침 네 칸", "유지(시범)", {"mgr", "doc"}),
    ("01-ex", "실제 요청서 한 장으로 이 네 칸이 무엇을 약속하는지 함께 읽습니다.", "네 칸을 실제 요청서에 어떻게 적을까요?", "강의 유일 실물 예시", "유지", set()),
    ("01-08", "등록된 요청에는 한 번의 시도를 뜻하는 요청 ID가 붙고, 작업 실행기가 이어받습니다.", "등록된 요청은 어떻게 실행될까요?", "이 장에서만 요청서 길에 '요청 등록·작업 실행기' 세부 노드와 시도별 요청 ID가 펼쳐짐. 자료 묶음은 '강의 03에서' 예고", "수정", {"wkr", "lane_top"}),
    ("01-10", "응답서에는 그 요청 ID와 처리 상태가 적혀 돌아옵니다.", "응답서의 처리 상태는 각각 무엇을 뜻할까요?", "응답서 → 네 상태", "유지(시범)", {"wkr", "lane_bot", "mgr"}),
    ("01-11", "응답을 받으면 판정하고, 막혔다면 원인을 고쳐 새 요청으로 다시 보냅니다.", "응답서를 받은 매니저는 무엇을 할까요?", "시뮬레이터 유지", "유지", {"mgr", "lane_bot"}),
    ("01-12", "그리고 누구도 스스로 승인할 수 없는 일이 네 가지 있는데, 그 승인은 언제나 사용자의 문장으로 남습니다.", "누구도 스스로 승인할 수 없는 일은 무엇일까요?", "매니저·직접 대화 워커 모두 사용자에게 승인 요청 → 원문", "유지(시범)", {"u2m", "direct"}),
])
L02 = ("02", "작업 흐름", "어떤 순서로 통과하나", [
    ("02-01", "일 중에는 바로 끝낼 일과, 기록을 남기며 지나가야 하는 일이 있습니다.", "여러 단계에 걸친 일은 어떤 순서로 기록하고 통과시킬까요?", "가운데 띠 확대: 바로 처리 / JOB 두 갈래", "수정", {"entry", "rail"}),
    ("02-05", "여러 단계에 걸치거나, 되돌아볼 가능성이 있거나, 다음 작업의 근거가 되는 일 — 하나라도 해당하면 JOB으로 기록합니다.", "기록이 필요한 일은 어떻게 가려낼까요?", "일을 하는 쪽이 세 질문으로 판단(분류기 그림 삭제 — 기존 02-04 흡수)", "합침", {"entry"}),
    ("02-06", "JOB은 기록을 남기는 작업 단위이며, 지나간 자리마다 파일이 남습니다.", "JOB 폴더에는 무엇이 들어갈까요?", "궤도 아래 JOB 폴더가 펼쳐짐", "수정", {"job"}),
    ("02-ex", "실제 JOB 기록 한 건을 요청부터 검증까지 이어서 읽어 봅니다.", "약속과 대조 기록에는 실제로 무엇이 적힐까요?", "강의 유일 실물 예시", "유지", set()),
    ("02-02", "상태는 지금 어디에 있는지이고, 전이는 상태가 바뀌는 일입니다.", "단계는 어떻게 넘어갈까요?", "궤도 위 토큰이 상태 사이를 이동", "합침·모션", {"rail"}),
    ("02-gate", "단계와 단계 사이에는 게이트가 있어, 약속한 기록을 확인한 뒤에 다음 단계를 엽니다.", "넘어갈 조건은 누가, 무엇으로 확인할까요?", "핵심 모션: 토큰이 게이트 앞에서 멈춤 → 기록 카드가 들어가면 열림. 검증 단계의 기록은 일한 쪽이 남김", "합침·모션", {"rail", "gates", "job"}),
    ("02-08", "기록이 빠지면 게이트는 그 자리에서 멈추고, 무엇이 빠졌는지 알려 줍니다.", "필요한 기록이 빠지면 어떤 일이 생길까요?", "시뮬레이터 + '기록은 있지만 계산이 틀림' 경우", "수정", {"rail", "gates"}),
    ("02-09", "승인은 지어내지 않습니다. 승인한 사용자 문장을 근거로 함께 남깁니다.", "승인 근거는 누가, 무엇으로 남길까요?", "사용자 원문 → 승인 기록 → 실행 경계 (01-12와 같은 사용자 상자)", "수정", {"gates"}),
    ("02-10", "(KEY) 완벽보다 끝까지입니다.", "", "유지", "유지", set()),
    ("02-11", "그래서 쓸 수 있는 결과를 남기고, 남은 일은 분명히 적어 둡니다.", "언제 '됐다'고 말할 수 있을까요?", "진행 막대 85%에서 완료 도장", "모션", {"rail"}),
    ("02-12", "막히면 고쳐서 다시 가되, 같은 막힘을 되풀이하지 않습니다.", "막혔을 때는 무엇을 반복하지 말아야 할까요?", "상태–행동 짝 바로잡음", "수정", {"rail"}),
])
# Lecture 03 rows carry four extra fields: plain takeaway, part, an everyday situation that shows why the
# slide matters, and its kind. Order is concept -> structure -> cycle; no interface names or measured figures.
# One analogy (a shift handover) runs through the lecture and closes it.
L03 = ("03", "지식", "지난 경험을 다음 일에 어떻게 넘겨주나 — 개념 → 구조 → 순환", [
    ("03-01", "에이전트는 일을 마치면 겪은 일을 모두 잊습니다.", "어제 배운 것을 오늘의 에이전트는 알고 있을까요?", "교대 근무 그림: 밤 근무자가 겪은 일을 아침 근무자는 모름. 둘 사이에 놓인 건 인수인계 노트 한 권. 같은 그림의 사람 자리에 에이전트가 들어감(세션이 끝나면 머릿속이 비워짐)", "신규·모션", set(),
     "에이전트는 세션이 끝나면 겪은 일을 잊습니다. 다음 에이전트에게 경험을 넘겨주는 장치가 필요합니다. 이 강의는 그 장치를 다룹니다.", "개념",
     "병원이나 공장에서는 근무자가 바뀌어도 일이 이어진다. 앞 근무자가 겪은 일을 인수인계로 넘겨주기 때문이다. 에이전트도 같다. 세션이 바뀔 때마다 새 사람이 출근하는 셈이다.", "비유"),
    ("03-02", "그래서 경험을 기록으로 남겨 다음 에이전트에게 넘겨야 합니다.", "에이전트에게 '지식'이란 무엇일까요?", "노트가 서랍에 있을 때는 흐리고, 아침 근무자가 펼쳐 읽는 순간 밝아짐 → 같은 장면을 '파일'과 '맥락 창'으로 바꿔 보임", "수정", set(),
     "남겨 둔 것만으로는 부족합니다. 다음 에이전트의 맥락 창에 들어와 읽혀야 비로소 지식이 됩니다.", "개념",
     "인수인계 노트가 서랍 속에만 있으면 아침 근무자는 같은 실수를 한다. 노트는 펼쳐 읽혔을 때만 쓸모가 있다.", "비유"),
    ("03-03", "그런데 기록은 계속 쌓이는데, 에이전트가 한 번에 읽을 수 있는 양은 정해져 있습니다.", "넘겨준 경험이 제 몫을 하려면 무엇이 필요할까요?", "노트 한 장에 세 개의 체크: 필요할 때 찾을 수 있나 · 지금도 맞나 · 실제로 일에 쓰였나. 이 세 조건을 강의 끝까지 따라감", "신규", set(),
     "찾을 수 없거나, 낡았거나, 아무도 쓰지 않는 기록은 지식이 아닙니다. 이 세 조건이 뒤의 모든 구조를 설명합니다.", "개념",
     "두꺼운 노트라도 원하는 내용을 못 찾거나, 지난달 이야기라 지금과 다르거나, 아무도 펼쳐 보지 않으면 소용없다.", "비유"),
    ("03-04", "그래서 기록을 성격에 따라 나눠 두고, 무엇을 언제 읽을지 정해 둡니다.", "모든 경험을 노트 한 권에 적으면 될까요?", "두 축 그림: 가로=얼마나 오래 맞나(늘 맞음 ↔ 지금만 맞음), 세로=무엇에 관한 것인가. 다섯 칸이 자리 잡음: 규칙(늘 지킬 원칙) · 기억(사람에 대해) · 스킬(일하는 방법) · 교훈(겪은 일) · 실물(지금의 상태)", "수정·모션", {"know"},
     "늘 맞는 원칙과 지금만 맞는 사실을 섞어 두면, 원칙은 묻히고 사실은 낡습니다. 그래서 성격에 따라 칸을 나눕니다.", "구조",
     "'환자 이름을 두 번 확인한다'는 늘 맞는 원칙이고, '3번 침대 환자는 오늘 금식'은 오늘만 맞는 사실이다. 둘을 같은 줄에 적으면 내일 아침에 무엇이 아직 유효한지 알 수 없다.", "비유"),
    ("03-05", "늘 지킬 원칙은 일을 시작할 때마다 읽고, 지난 경험은 비슷한 일을 만났을 때 찾아 읽습니다.", "나눠 둔 지식은 각각 언제 읽힐까요?", "다섯 칸 위에 시계: 규칙=일을 시작할 때 늘 · 기억=그 사람과 일할 때 · 스킬=그 일을 할 때 · 교훈=비슷한 일을 만났을 때 · 실물=확인이 필요한 그 순간. 지도 아래 띠와 연결 띠가 켜짐", "신규·모션", {"know", "kconn"},
     "어디에 두느냐가 언제 읽히느냐를 정합니다. 꼭 지켜야 할 것은 늘 읽히는 칸에, 가끔 필요한 것은 찾을 수 있는 칸에 둡니다.", "구조",
     "모든 근무자가 꼭 알아야 할 것은 교대 때마다 소리 내어 읽고, 가끔 필요한 요령은 매뉴얼에 넣어 두고 찾아본다.", "비유"),
    ("03-06", "같은 내용을 여러 곳에 두면 언젠가 서로 달라지므로, 원본은 한 곳에만 둡니다.", "같은 내용을 여러 곳에 적어 두면 더 안전할까요?", "같은 문장이 세 곳에 복사됨 → 한 곳만 고쳐지고 나머지 둘이 낡아 서로 다른 말을 함 → 정본 하나와 그곳을 가리키는 화살표로 정리", "신규", {"know"},
     "사본은 반드시 낡습니다. 내용마다 기준이 되는 원본(정본)을 하나 정하고, 다른 곳은 그것을 가리키게 합니다.", "구조",
     "벽 게시판과 노트와 메신저에 같은 공지를 적어 두면, 바뀐 날 한 곳만 고쳐지고 나머지는 틀린 공지로 남는다.", "비유"),
    ("03-07", "이렇게 나눠 둔 기록은 일할 때마다 읽히고, 확인되고, 새로 쌓이고, 정리되며 돕니다.", "이 구조 위에서 지식은 어떻게 움직일까요?", "다섯 칸 위로 원이 그려짐: 일을 시작하며 읽고 → 읽은 것을 확인하고 → 일이 끝나면 남기고 → 쌓인 것을 정리하고 → 다시 읽힘. 이후 장마다 오른쪽 위에 이 원을 두고 현재 단계를 켬", "신규·모션", {"know", "kconn", "kloop"},
     "지식은 한 번 적고 끝나는 문서가 아니라, 일과 함께 계속 도는 순환입니다.", "순환", "", ""),
    ("03-08", "일을 시작할 때는 늘 읽는 원칙에 더해, 이번 일에 맞는 기록을 골라 읽습니다.", "일을 시작할 때 필요한 지식은 어떻게 들어올까요?", "세 겹 화살표가 맥락 창으로: 늘 들어오는 원칙 / 맡긴 사람이 일에 맞춰 골라 붙여 주는 자료 / 일하는 쪽이 스스로 찾는 것. 바로 맡은 일에는 둘째 겹이 없다는 표시", "수정·모션", {"kconn", "lane_top", "direct"},
     "모든 지식을 늘 읽을 수는 없습니다. 꼭 필요한 것만 늘 읽고, 나머지는 일에 맞춰 골라 받거나 스스로 찾습니다.", "순환",
     "아침 근무자는 공통 수칙은 매일 듣고, 담당 환자 기록은 받아서 보고, 처음 보는 증상은 직접 찾아본다.", "비유"),
    ("03-09", "찾은 기록은 지금도 맞는지 원본과 현재 상태로 확인한 뒤에 씁니다.", "찾아 낸 지식은 그대로 믿어도 될까요?", "후보 카드 여러 장 → 원문을 열어 맞는지 → 지금 상태와 같은지, 두 번 걸러져 한두 장만 남음", "합침·모션", {"k_lesson", "k_real", "kconn"},
     "찾은 것이 지금도 맞는지는 원문과 현재 상태를 직접 봐야 압니다. 이것이 '맞는 지식'의 조건입니다.", "순환",
     "지난주 노트에 '3번 침대 금식'이라 적혀 있어도, 오늘 그 환자가 그대로인지는 침대에 가서 봐야 안다.", "비유"),

    ("03-10", "일을 마치면 다음 사람이 비슷한 상황에서 찾을 수 있게 교훈을 남깁니다.", "일이 끝나면 무엇을 남겨야 다음에 활용할 수 있을까요?", "교훈 카드: 무슨 일이 있었나 · 왜 · 어떻게 풀었나 + '이럴 때 다시 보라'. 다음 장면에서 누군가 그 상황을 만나자 이 카드가 걸려 나옴", "수정·모션", {"job", "kconn", "k_lesson"},
     "다음 사람은 결론이 아니라 자기가 겪는 상황으로 찾습니다. 그래서 '어떤 상황에서 필요한가'를 함께 남겨야 필요한 순간에 찾을 수 있는 지식이 됩니다.", "순환",
     "'밸브를 잠갔다'만 적힌 노트는 찾기 어렵다. '바닥에 물이 고이면 → 이 밸브'라고 적혀 있어야 다음 사람이 찾는다.", "비유"),
    ("03-11", "(KEY) 기록하지 않은 실패는 되풀이됩니다.", "", "유지", "유지", set(), "", "순환", "", ""),
    ("03-12", "쌓이기만 한 기록은 찾기 어려워지므로, 꾸준히 다듬고 되풀이된 교훈은 원칙으로 올립니다.", "남긴 지식은 그대로 쌓아 두면 될까요?", "쌓이는 카드 더미 → 매일 조금씩: 새 것은 기존 것과 대조 · 반복된 교훈은 규칙과 절차로 올림 · 낡은 것은 내림. 더미가 정돈된 선반으로 바뀜", "재작성·모션", {"kloop", "k_lesson", "k_rule", "k_skill"},
     "지식은 양이 늘수록 찾기 어렵고 낡은 것이 섞입니다. 꾸준히 대조하고, 반복된 것은 원칙으로 올리고, 낡은 것은 내려야 합니다.", "순환",
     "같은 실수가 노트에 세 번 적히면, 그것은 더 이상 메모가 아니라 수칙에 넣을 일이다.", "비유"),
    ("03-13", "이 순환은 멈춰도 티가 나지 않으므로, 필요할 때 찾을 수 있는지, 내용이 지금도 맞는지, 실제로 쓰이는지를 정기적으로 확인합니다.", "이 순환이 제대로 돈다는 것은 어떻게 알까요?", "03-03의 세 체크가 계기판으로 돌아옴: 찾을 수 있나 · 맞나 · 쓰이나. 지식은 고장 나도 조용하므로 정기적으로 시험해 봄", "신규", {"kloop", "know"},
     "지식은 고장 나도 오류를 내지 않습니다. 찾을 수 있는지, 맞는지, 쓰이는지를 꾸준히 확인해야 순환이 멈춘 것을 알 수 있습니다.", "순환", "", ""),
    ("03-14", "이렇게 한 바퀴가 돌면 어제의 실수를 오늘 되풀이하지 않습니다.", "처음의 질문, 어제의 경험은 오늘 어떻게 넘어왔을까요?", "03-01 교대 그림으로 돌아와 한 바퀴 재생: 겪은 일을 남기고 → 정리하고 → 다음 근무자가 읽고 → 확인하고 일함. 마지막에 지도 전체가 켜지며 강의 04로", "신규·모션", {"all"},
     "개념(넘겨줄 경험) 위에 구조(칸과 정본)를 세우고, 순환(읽기·확인·남기기·정리)으로 돌리면 같은 실수를 두 번 하지 않습니다.", "정리", "", ""),
])
L04 = ("04", "통합", "어떻게 확인하고 닫나", [
    ("04-01", "이제 지도 위에서 요청 하나의 일생을 처음부터 끝까지 따라가 봅니다.", "이 모든 조각이 요청 하나에서 어떻게 함께 움직일까요?", "전체 지도", "수정", {"all"}),
    ("04-02", "검증은 말한 것과 실제를 맞춰 보는 일입니다.", "확인이란 정확히 무엇일까요?", "보고 ≠ 실제 세 줄", "유지", set()),
    ("04-ex", "보고 문장을 원자료 계산과 대조해 직접 확인해 봅니다.", "원자료와 보고 값이 다르면 어떻게 고칠까요?", "강의 유일 실물 예시", "유지", set()),
    ("04-03", "요청 하나는 매니저를 거치거나 워커에게 직접 가거나, 두 길 중 하나로 흐릅니다.", "실제 요청 하나는 어떤 순서로 흘러갈까요?", "핵심 모션: 전체 지도 위 토큰, [매니저에게 맡기기 | 워커에게 직접] 두 시나리오. 01-modes와 같은 전환 버튼", "재작성·모션", {"all"}),
    ("04-two-checks", "맡긴 일일수록 확인은 두 겹이 됩니다. 일한 쪽의 검증과, 맡긴 쪽의 판정.", "맡긴 일은 어떻게 확인할까요?", "일한 쪽의 검증 단계 + 맡긴 쪽의 응답서 판정", "신규", {"rail", "mgr", "lane_bot"}),
    ("04-04", "위험이 클수록 따로 다시 확인합니다.", "결과는 얼마나 확인해야 충분할까요?", "두 겹의 확인에 위험별 깊이를 더함", "수정", {"rail", "mgr", "lane_bot"}),
    ("04-05", "(KEY) 확인된 것만 완료라고 말합니다.", "", "유지", "유지", set()),
    ("04-06", "직접 고쳤을 때도 원본 백업과 변경 기록을 남깁니다.", "직접 고친 것도 기록을 남길까요?", "매니저·직접 대화 워커 모두 같은 변경 기록", "수정", {"mgr", "wkr"}),
    ("04-07", "이 흐름을 구현한 코드와 테스트는 저장소에서 다시 볼 수 있습니다.", "이 흐름을 구현한 코드는 어디서 볼 수 있을까요?", "세 상자 모두 GitHub에 연결", "수정", set()),
    ("04-08", "다섯 강의를 한 장의 지도로 되돌아보면, 요청이 확인된 결과가 되는 전체 그림으로 닫습니다.", "다섯 강의를 한 장으로 정리하면 무엇이 남을까요?", "지도에서 강의별 구간이 차례로 켜짐", "수정·모션", {"all"}),
])
LECTURES = [L00, L01, L02, L03, L04]
PARTS = {"개념": "지식이란 무엇인가", "구조": "지식은 어떻게 짜여 있나", "순환": "지식은 어떻게 돌아가나", "정리": "처음 질문으로 돌아가기"}

AUDIT = [
    ("구현 세부가 큰 그림을 덮음", "지도에 요청 등록·작업 실행기·분류기가 있어 길이 복잡했다", "지도에는 사용자·매니저·워커·요청서·응답서만. 등록·실행기는 01-08 한 장에서만 펼침"),
    ("분류기", "메시지를 관찰해 결과 파일만 남기는 장치(경로·승인과 무관)를 요청이 거치는 관문처럼 그렸다", "강의 그림에서 삭제. JOB 여부는 '일을 하는 쪽이 세 질문으로'로 통일(02-05)"),
    ("매니저가 실행하는 것처럼 보임", "매니저 선이 작업 흐름으로 들어가고, 검증에 '매니저 판정'이 붙어 직접 대화에도 매니저가 끼는 것처럼 보였다", "작업 흐름에는 워커만 들어감. 매니저 판정은 위 띠의 응답서 판정(맡긴 경우만)으로 분리. 04-04에서 '두 겹의 확인'으로 설명"),
    ("지식이 일부 항목만 연결됨", "화살표가 규칙·실물 칸에만 붙어 다른 지식이 무시되는 것처럼 보였다", "지식 블록 전체와 위 전체를 잇는 연결 띠 하나(읽기 ↑ · 남기기 ↓)"),
    ("직접 대화 경로가 흩어짐", "직접 대화가 지도 한쪽 점선으로만 나와 이해하기 어려웠다", "00-entry에서 두 길 소개 → 01-modes 전용 모션 → 04-03 같은 전환 버튼으로 재등장"),
    ("지식 강의가 장치 나열로 붕 뜸", "장치(검색·대기열·대조…)를 하나씩 소개해 왜 필요한지와 전체 흐름이 잘 안 보였다. 이미 멈춘 장치(매일 위키 요약)도 섞여 있었다", "개념(지식=넘겨주는 경험, 좋은 지식의 세 조건) → 구조(성격별 칸, 읽히는 때, 정본) → 순환(읽기·확인·남기기·정리) 순서로 재구성. 교대 근무 비유 하나로 처음과 끝을 잇고, 인터페이스 이름과 운영 수치는 강의에서 뺌"),
    ("새 용어 부담", "강의마다 용어가 몰려 나왔다", "강의별 새 용어를 아래처럼 제한하고, 다른 강의에서는 지도 위치로만 가리킴"),
]
TERMS = [("00", "언어 모델 · 맥락 창 · 에이전트 · 매니저 · 워커 · 작업 흐름 · 지식"), ("01", "요청서 · 응답서 · 요청 ID · 처리 상태 · 작업 실행기(01-08만) · 승인 범주"),
         ("02", "JOB · 세 질문 · 상태와 전이 · 게이트 · 승인 기록"), ("03", "지식(넘겨주는 경험) · 찾힘·맞음·쓰임 · 다섯 칸 · 정본 · 순환(읽기·확인·남기기·정리)"), ("04", "두 겹의 확인 · 변경 기록")]


def two_ways():
    import scenes as S2
    def panel(pid, focus, packets, title, sub):
        body = S2.skeleton(pid, focus, packets)
        return (f"<div class='way'><div class='wt'>{title}</div><div class='ws'>{sub}</div>"
                f"<svg viewBox='0 0 1000 360'>{S2.defs(pid)}{body}</svg></div>")
    a = panel("wa", VIA, (S2.pkt("wa", "u2m", "", 1.2, .2), S2.pkt("wa", "l1", "amber", .8, 1.4), S2.pkt("wa", "l5", "amber", 1.0, 2.2),
                          S2.pkt("wa", "r1", "amber", 1.0, 3.6), S2.pkt("wa", "r2", "amber", 1.2, 4.6), S2.pkt("wa", "m2u", "", 1.2, 6.0)),
              "① 매니저에게 맡기기", "사용자 → 매니저(판단) → 요청서 → 워커(실행) → 응답서 → 매니저(판정) → 사용자")
    b = panel("wb", DIRECT, (S2.pkt("wb", "direct", "blue", 2.4, .2), S2.pkt("wb", "reply", "blue", 2.4, 3.2)),
              "② 워커에게 직접 맡기기", "사용자 → 워커(판단·실행) → 같은 대화로 답. 매니저·요청서·응답서 없음")
    return f"<div class='ways'>{a}{b}</div>"


CSS = """
body{margin:0;background:#0d1722;color:#e6edf6;font:16px/1.55 Pretendard,system-ui,sans-serif}
main{max-width:1280px;margin:0 auto;padding:40px 32px 80px}
h1{font-size:34px;margin:0 0 6px}h2{font-size:26px;margin:56px 0 6px}
.lead{color:#9fb0c4;margin:0 0 20px}
.map{background:#132130;border:1px solid #304357;border-radius:14px;padding:16px}
.map svg{width:100%;height:auto;display:block}
.rule{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:16px 0}
.rule div{background:#132130;border:1px solid #304357;border-radius:10px;padding:12px 14px;font-size:15px;color:#c3d0e0}
.rule b{display:block;color:#82dec6;margin-bottom:4px}
table{width:100%;border-collapse:collapse;margin-top:12px}
td,th{border-bottom:1px solid #26384b;padding:10px 8px;vertical-align:top;text-align:left;font-size:15px}
th{color:#9fb0c4;font-weight:600;font-size:13px}
td.n{color:#9fb0c4;width:34px}td.th{width:230px}
td.th svg{width:230px;height:auto;display:block;background:#0f1a27;border-radius:6px}
.t{font-weight:700;color:#f4f7fb}.q{color:#9bc2ff;font-size:14px;margin-top:4px}
.nx{color:#ffcf86;font-size:13px;margin-top:4px}.say{color:#dfe7f1;font-size:15px;margin-top:6px;padding-left:10px;border-left:3px solid #82dec6}
.sit{background:#2a2414;border:1px solid #6b5a2e;border-radius:8px;padding:8px 10px;margin-top:8px;color:#f1e6c8;font-size:14.5px}.sit b{display:block;color:#ffcf86;font-size:12px;margin-bottom:2px}
tr.part td{background:#17283a;color:#82dec6;font-weight:700;font-size:15px;padding:8px 12px;border-radius:8px}\n.lit{color:#82dec6;font-size:12px;margin-top:6px}
.ways{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px}.way{background:#132130;border:1px solid #304357;border-radius:12px;padding:12px}
.way svg{width:100%;height:auto;display:block}.wt{font-weight:700;font-size:18px}.ws{color:#9fb0c4;font-size:14px;margin:2px 0 8px}
table.audit td{font-size:14px}table.audit td:first-child{font-weight:700;color:#ffcf86;width:160px}
.tag{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:700;background:#26384b;color:#c3d0e0;white-space:nowrap}
.tag.new{background:#1b2847;color:#9bc2ff}.tag.mo{background:#173a39;color:#82dec6}.tag.keep{background:#1f2734;color:#93a6bb}.tag.hold{background:#3a2f1c;color:#ffcf86}
svg text{font-family:Pretendard,system-ui,sans-serif;fill:#edf2fa;font-size:25px;font-weight:650;text-anchor:middle;dominant-baseline:middle}
svg text.sub{font-size:19px;font-weight:450;fill:#b9c7d8}
svg text.lbl{font-size:19px;font-weight:600;fill:#c3d0e0}
svg text.left{text-anchor:start}
svg .box{fill:#1b2b3d;stroke:#6c839d;stroke-width:2}
td.th svg .dim{opacity:.1}
@media (max-width:760px){
 body{font-size:15px}main{padding:20px 14px 60px}h1{font-size:24px}h2{font-size:21px;margin-top:40px}
 .map{padding:8px}.rule,.ways{grid-template-columns:1fr!important}
 table,tbody,tr,td{display:block;width:auto}tr:first-child:has(th){display:none}
 table:not(.audit) tr{border:1px solid #26384b;border-radius:12px;margin:12px 0;padding:6px 4px;background:#111d2b}
 table:not(.audit) td{border:0;padding:6px 8px}td.n{display:inline-block!important;width:auto}
 td.th{width:auto}td.th svg{width:100%}
 table.audit tr{border-bottom:1px solid #26384b;padding:8px 0}table.audit td{border:0;padding:3px 4px}table.audit td:first-child{width:auto}
}
""" + S.STYLE.replace("<style>", "").replace("</style>", "").replace("#deck .dk-scene svg ", "svg ").replace("#deck .dk-slide.is-active .dk-body:has(.dk-scene.mapped){animation:mo-fade .35s ease-out both}", "")


CONNECTORS = [("u2m", "사용자↔매니저"), ("direct", "사용자↔워커 직접"), ("doc", "매니저→요청서"), ("lane_top", "요청서→워커"),
              ("lane_bot", "워커→응답서→매니저"), ("entry", "워커→작업 흐름 입구"), ("rail", "단계 궤도"), ("gates", "게이트"),
              ("job", "JOB 폴더"), ("know", "지식↔위 전체 연결 띠"), ("kconn", "지식↔위 전체 연결 띠"), ("kloop", "매일 정리 띠")]


def lit_connectors(focus):
    if not focus:
        return ""
    if "all" in focus:
        return "전체"
    f = S.close_focus(focus)
    names = []
    for k, n in CONNECTORS:
        hit = k in f and not (k == "doc" and "lane_top" in f)
        if hit and n not in names:
            names.append(n)
    return " · ".join(names) or "연결선 없음(상자만)"


def tag(status):
    cls = "new" if ("신규" in status or "재작성" in status) else "mo" if ("모션" in status or "시범" in status) else "keep" if status == "유지" else "hold" if "보류" in status else ""
    return f'<span class="tag {cls}">{escape(status)}</span>'


def main():
    parts = [f"<!doctype html><html lang='ko'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>p-hermes 강의 스토리보드</title><style>{CSS}</style></head><body><main>",
             "<h1>p-hermes 강의 개편 스토리보드 (검토용)</h1>",
             "<p class='lead'>강의 00~04 전체. 강의 03(지식)은 2026-10-11 지식 시스템 개선(JOB-4294~4301) 결과로 개편했다. 각 장의 '다음 질문'은 다음 장이 답하는 질문이다.</p>",
             "<h2>전체 지도 (단일 정의)</h2><p class='lead'>모든 그림은 이 지도의 한 구역을 확대한 것이다. 위 띠는 강의 01 시범본 골격과 같은 좌표다. 작업 흐름에는 워커만 들어가고, 매니저의 판정은 위 띠의 응답서 경로(맡긴 경우)에만 있다. 지식은 블록 전체가 연결 띠 하나로 위 전체와 이어진다.</p>",
             f"<div class='map'>{S.map_svg('mapfull', {'all'})}</div>",
             "<div class='rule' style='grid-template-columns:repeat(4,1fr)'><div><b>역할 표현</b>실행은 워커, 매니저는 판단·위임·응답서 판정. 매니저의 직접 처리는 01-06 한 곳에서 예외로만</div><div><b>강의별 확대 구역</b>00 전체 → 01 위 띠(역할) → 02 가운데 띠(작업 흐름) → 03 아래 띠(지식) → 04 전체</div>"
             "<div><b>장 사이</b>같은 골격을 같은 자리에 두고 강조만 옮긴다. 아래쪽은 세부 카드 자리. 오른쪽 위 작은 지도에 현재 위치 표시</div>"
             "<div><b>강의 사이</b>마지막 장에서 다음 구역을 켜고, 다음 강의 표지가 그 구역 확대로 시작한다</div></div>",
             "<div class='rule'><div><b>부품</b>사용자=흰 테두리+사람, 매니저=민트, 워커=파랑, 요청서·응답서=접힌 주황 문서, 직접 대화=파란 점선, 게이트=노란 막대, 지식=연노랑 카드, 승인=산호 도장</div>"
             "<div><b>용어</b>매니저 · 워커 · 요청서 · 응답서 · 작업 실행기 · JOB · 게이트 · 기록(과거) · 실물(지금). 분류기는 강의에서 다루지 않음</div>"
             "<div><b>실물 예시</b>강의당 1장. 나머지 예시는 본문으로 흡수하거나 삭제</div></div>"]
    parts.append("<h2>두 가지 쓰는 법 (01-modes 전용 모션의 정지 화면)</h2><p class='lead'>같은 골격에서 길만 바뀐다. 실제 강의에서는 전환 버튼으로 두 경로가 번갈아 재생된다. 04-03에서도 같은 버튼을 쓴다.</p>")
    parts.append(two_ways())
    parts.append("<h2>흐름 점검 — 사실 정정이 이해를 어렵게 만든 곳과 정리</h2><table class='audit'><tr><th>문제</th><th>무엇이 어려웠나</th><th>정리</th></tr>"
                 + "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td><td>{escape(c)}</td></tr>" for a, b, c in AUDIT) + "</table>")
    parts.append("<table class='audit'><tr><th>강의</th><th>이 강의에서 처음 나오는 용어</th></tr>" + "".join(f"<tr><td>{a}</td><td>{escape(b)}</td></tr>" for a, b in TERMS) + "</table>")
    n = 0
    for num, name, question, slides in LECTURES:
        parts.append(f"<h2>강의 {num} · {escape(name)}</h2><p class='lead'>맡는 질문: {escape(question)} · {len(slides)}장</p>")
        parts.append("<table><tr><th>#</th><th>지도 위치</th><th>제목 · 답하는 질문 → 다음 질문</th><th>그림·모션</th><th>처리</th></tr>")
        part = None
        for i, row in enumerate(slides):
            key, title, q, fig, status, focus = row[:6]
            say, sec = (row[6], row[7]) if len(row) > 6 else ("", None)
            sit, basis = (row[8], row[9]) if len(row) > 8 else ("", "")
            if sec and sec != part:
                part = sec
                parts.append(f"<tr class='part'><td colspan='5'>{escape(sec)} · {escape(PARTS.get(sec, ''))}</td></tr>")
            n += 1
            nxt = slides[i + 1][2] if i + 1 < len(slides) else ""
            if i + 1 < len(slides) and not nxt and i + 2 < len(slides):
                nxt = slides[i + 2][2]
            thumb = S.map_svg(f"t{n}", focus, labels=False) if focus else "<div style='color:#5d7590;font-size:13px'>지도 없음(개념·예시·KEY)</div>"
            parts.append(f"<tr><td class='n'>{i + 1}</td><td class='th'>{thumb}</td><td><div class='t'>{escape(title)}</div>"
                         + (f"<div class='sit'><b>왜 필요한가 · {escape(basis)}</b>{escape(sit)}</div>" if sit else "")
                         + (f"<div class='say'>{escape(say)}</div>" if say else "")
                         + (f"<div class='q'>답하는 질문: {escape(q)}</div>" if q else "")
                         + (f"<div class='nx'>다음 질문 → {escape(nxt)}</div>" if nxt and q else "")
                         + (f"<div class='lit'>강조되는 연결: {escape(lit_connectors(focus))}</div>" if focus else "")
                         + f"</td><td>{escape(fig)}</td><td>{tag(status)}</td></tr>")
        parts.append("</table>")
    parts.append("</main></body></html>")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(OUT, n)


if __name__ == "__main__":
    main()
