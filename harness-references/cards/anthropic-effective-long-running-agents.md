# Effective harnesses for long-running agents

- 원문: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 출처 시점: 원문 추출본에서 게시일을 확인하지 못함; 직접 확인 2026-10-14.
- 주제: 개요 · orchestration/workflow · context/memory · 사례
- 상태: 요청 필수 핵심 자료; 제공 여부와 references 등록 여부는 이번 원천 검토에서 확인되지 않음. 패턴 참고, 도입 아님.
- 권리: 확인되지 않음. 자체 요약·링크만; 전문 미보존.
- 정리 근거: 원문 일부 확인

## 자체 요약

긴 작업이 여러 context window와 session을 넘을 때 compaction만으로는 부족할 수 있다고 설명한다. 첫 session은 요구사항·초기 환경·실행 스크립트를 준비하는 initializer로, 후속은 한 번에 작은 단위의 기능을 구현하고 구조화된 progress artifact와 깨끗한 작업 상태를 남기는 coding agent로 나눈다. feature list와 git history를 함께 handoff 자료로 사용한다.

## 상세 정리

### 핵심 주장
- 여러 context window와 session에 걸친 장기 작업은 compaction만으로 충분하지 않다. 세션이 바뀌면 에이전트는 이전 작업을 기억하지 못하므로, 교대 근무하는 엔지니어들처럼 명시적인 인수인계 산출물이 필요하다는 것이 핵심이다.
- 해결책은 두 역할로 나뉜다. 첫 세션의 initializer agent는 환경, 실행 스크립트, 진행 로그, 초기 git 커밋을 만든다. 이후 세션의 coding agent는 기능 하나씩 점진적으로 구현하고 깨끗한 상태로 마무리한다.
- 기능 목록(feature list)은 JSON으로 두고 각 항목에 passes 상태만 갱신하게 한다. 필자들은 모델이 Markdown보다 JSON을 덜 임의로 바꾼다고 보고했다.
- 실패 양상으로 세 가지를 든다. 한 번에 너무 많은 것을 하려다 기능이 반쯤 구현된 채 끊기는 것, 나중 세션이 진행 상황을 과대평가해 완료를 선언하는 것, 그리고 기능을 충분히 검증하지 않고 완료 표시하는 것이다.
- 테스트는 단위 테스트나 curl이 아니라 사용자 관점의 end-to-end 브라우저 자동화(예: Puppeteer MCP)로 해야 실제 버그가 드러났다고 기술한다.

### 구조와 패턴
- 진행 기록은 progress 파일과 git 히스토리를 함께 쓴다. 새 세션은 진행 파일과 커밋 로그를 읽고, 기본 테스트로 기존 버그를 확인한 뒤 한 기능을 고른다.
- init.sh 같은 실행 스크립트를 두어 개발 서버 기동 방법을 매번 추측하지 않게 한다.
- 정리된 표는 실패 모드와 해결을 짝지어 제시한다: 조기 완료 선언 → 기능 목록, 불완전한 상태 → git과 진행 노트, 조기 통과 표시 → 자체 검증, 실행 방법 탐색 → init.sh.

### 적용 방법
- 장기 작업을 시작할 때 요구사항을 검증 가능한 항목 목록으로 먼저 고정하고, 완료는 그 목록의 검증 결과로만 판단하는 절차가 출발점이다.
- 세션 종료 시 커밋과 진행 기록을 남기는 규칙, 세션 시작 시 그 기록을 읽는 규칙을 한 쌍으로 설계한다.
- 항목 삭제·수정을 금지하는 지시는 필자들이 강하게 쓴 방식이므로, 같은 효과를 원하면 상태 필드만 바꾸도록 쓰기 권한을 좁히는 것이 참고가 된다.

### 근거와 한계
- 원문 일부 확인: 원문을 열어 주요 절(문제 정의, 환경 관리, 진행, 테스트, 실패 표)을 읽었다. 중간 일부 구간은 추출 생략으로 직접 확인하지 못했다.
- 사례는 Claude Agent SDK와 claude.ai 복제 웹앱이라는 단일 과제에 한정된다. 성공률 같은 정량 비교 결과는 본문에서 확인하지 못했다.
- 저자들도 단일 범용 coding agent가 나은지, 전문화된 다중 에이전트가 나은지는 열린 질문으로 남긴다고 밝혔다. 웹 풀스택 개발 외 영역으로의 일반화도 미확인이다.

### 연결
- [anthropic-harness-design-long-running-apps.md](anthropic-harness-design-long-running-apps.md) — 같은 저자 계열의 후속 글로, 생성자와 평가자 분리로 확장된 설계
- [google-cloud-long-horizon-patterns.md](google-cloud-long-horizon-patterns.md) — 장기 과제의 상태 전달 패턴을 다른 기관 관점에서 비교할 때 참고
- [agentic-harness-evolution.md](agentic-harness-evolution.md) — 하네스 구성 요소의 진화 흐름 속에서 이 설계의 위치를 볼 때 참고

## Hermes 관련성

세션 간 상태 전달, 점진적 요구사항 충족, clean handoff를 설계할 때 참고할 수 있다. Anthropic의 Claude Agent SDK 및 웹앱 개발 조건의 사례이며 Hermes worker/JOB 절차와 동등하거나 운영 적용되었다는 뜻은 아닙니다.
