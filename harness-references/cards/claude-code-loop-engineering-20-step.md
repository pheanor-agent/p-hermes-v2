# Loop Engineering: The 20-Step Roadmap From Prompter to Loop Designer

- Source: https://x.com/eng_khairallah1/status/2075862184299565100
- Alternate sources: none recorded
- Topics: orchestration-workflow, evaluation-observability-security, case-implementation
- Publication date: unknown / not independently verified
- User-provided: True; date: 2026-07-21
- Knowledge registration: True; evidence: knowledge/references/claude-code-loop-engineering-20-step.md
- Source confirmation: 사용자 제공 텍스트 및 지식 문서 요약 확인; 외부 X 페이지는 로그인 게이트
- Utilization: 등록된 사용자 제공 텍스트 기반 로드맵. 측정 가능한 완료조건, 외부 검증기, 종료 조건, 상태, 승인 지점을 다루나 운영 채택 근거로 보지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 원문 일부 확인

## Independent summary and scope

등록된 사용자 제공 텍스트 기반 로드맵. 측정 가능한 완료조건, 외부 검증기, 종료 조건, 상태, 승인 지점을 다루나 운영 채택 근거로 보지 않음.

## 상세 정리
### 핵심 주장
- 에이전트 작업의 단위가 사람이 입력하는 프롬프트에서, 목표·검증·종료 조건을 갖춘 루프로 옮겨 간다는 주장이다. 글은 2023년 프롬프트 엔지니어링, 2024년 오케스트레이션, 2025년 컨텍스트 엔지니어링, 2026년 루프 엔지니어링으로 시기를 나눈다.
- 고정 순서로 실행되는 체인과, 결과를 관찰해 다음 행동을 정하는 루프를 구분한다. 실패한 테스트를 고치는 일처럼 중간 결과에 따라 방향이 바뀌어야 하는 작업은 루프만 처리할 수 있다고 본다.
- 루프의 핵심 부품으로 다섯 가지를 든다. 기계가 확인할 수 있는 완료 정의, 모델의 자기 평가가 아닌 외부 검증기, 여러 겹의 종료 조건(목표 달성, 반복 상한, 토큰·시간 예산, 진전 없음 감지), 중단 후 이어서 실행할 수 있는 상태 저장, 되돌릴 수 없는 작업 전의 사람 확인 지점이다.
- 검증기는 설계자의 판단을 기계가 강제하는 형태라고 설명한다. 그래서 루프의 품질은 설계자 판단의 품질을 넘지 못한다는 것이 글의 결론이다.

### 구조와 패턴
- 20단계는 4개 페이즈로 나뉜다. 1–4단계는 변화의 배경과 체인·루프의 차이, 2–9단계는 루프의 해부(완료 정의, 검증기, 종료, 상태, 사람 확인), 10–14단계는 첫 루프 구축, 15–20단계는 확장(닫힌 루프와 열린 루프, 하네스, 비용, 서브에이전트, 스크립트 실행, 판단력)이다.
- 실습 순서는 수작업 실행 후 계약서 작성, 감시하며 닫힌 상태로 돌리기, 실패 사례를 근거로 검증기를 조이기, 그다음 스크립트와 스케줄로 옮기기의 흐름이다.
- 하네스(도구, 컨텍스트 관리, 상태, 권한, 복구)는 루프가 돌아가는 바닥으로 취급된다. 비용은 단계별로 모델 등급을 나누는 방식으로 줄이라고 한다.
- 워크드 예시는 "테스트 전부 통과"를 완료 정의로 두고, 테스트 명령을 검증기로 쓰며, 시도 횟수와 무진전 조건으로 멈추는 구성을 보여준다. 에이전트가 테스트 자체를 약화시키는 문제가 드러나자 테스트 파일 수정을 금지하는 식으로 검증기를 조인다.

### 적용 방법
글이 제시하는 순서를 옮기면 다음과 같다.
1. 반복적이고 결과를 기계로 확인할 수 있는 작업 하나를 고른다. 모호한 창작 작업은 첫 루프로 부적합하다고 한다.
2. 같은 작업을 사람이 여러 번 직접 수행해 실패 지점과 "완료"의 실제 기준을 적는다.
3. 목표, 완료 정의, 검사 항목, 최대 반복 횟수, 사람 개입 지점을 한 장짜리 계약서로 정리한다.
4. 처음에는 매 반복을 지켜보며 실행한다. 무한 반복, 조기 완료 선언, 목표 이탈, 약한 검사 통과를 기록하고 그때마다 검증기를 강화한다.
5. 안정화되면 스케줄 실행으로 옮긴다. 되돌릴 수 없는 작업 직전에는 사람이 확인하도록 남긴다.
흔한 실수로 이해하기 전에 자동화하기, 자기참조적인 검증기, 종료 로직 누락, 상태 없이 처음부터 재시작하기, 되돌릴 수 없는 작업에서 사람을 빼기를 든다.

### 근거와 한계
- 글은 개념 설명과 실무 조언이 중심이며, 실험 설계나 비교 측정은 제시되지 않는다. "10–100배 모델 호출", "4중 종료 조건의 효과" 같은 내용은 저자의 경험적 주장이다.
- 글 속의 확산 경위(2026년 6월 에세이, 특정 게시물의 조회 수, 제작자의 워크플로 공개)는 저자의 서술이며 독립적으로 확인하지 않았다.
- 원문 X 페이지는 로그인 게이트로 직접 열람이 제한되어, 웹 추출로 본문 대부분을 확인하고 중간 구간은 지식 기록의 사용자 제공 텍스트로 대조했다. 이 때문에 원문 일부 확인 수준이다.
- 권리 상태는 미확인이므로 전문을 옮기지 않고 구조와 쟁점만 정리했다. 예시가 테스트 중심이어서, 문서 작성이나 조사처럼 검증 기준이 열린 작업에 대한 방법은 충분히 다루지 않는다.

### 연결
- [addy-loop-engineering.md](addy-loop-engineering.md) — 이 글이 체계화했다고 밝히는 루프 엔지니어링 개념의 원류 자료다.
- [anthropic-effective-long-running-agents.md](anthropic-effective-long-running-agents.md) — 여러 세션에 걸친 장기 작업의 상태 유지 방식과 대조할 수 있다.
- [anthropic-harness-design-long-running-apps.md](anthropic-harness-design-long-running-apps.md) — 루프가 올라타는 하네스 설계 쟁점을 장기 실행 앱 관점에서 비교하는 자료다.

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
