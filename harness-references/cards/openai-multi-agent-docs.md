# Orchestrating multiple agents and handing off work

- OpenAI Responses API: https://developers.openai.com/api/docs/guides/responses-multi-agent
- OpenAI API orchestration guide: https://platform.openai.com/docs/guides/agents/orchestration
- 출처 시점: 사용자가 링크 제공한 2026-09-23 (KST, 내부 evidence); 이번 세션에서 각 페이지의 최신 내용 확인은 생략.
- 주제: orchestration/workflow · tools
- 상태: 사용자 제공; knowledge references 등록/운영 활용 확인 안 됨. 참고 링크.
- 권리: 미확인. 자체 요약·링크만; 본문 미복사.
- 정리 근거: 원문 일부 확인

## 자체 요약

두 공식 개발자 문서 링크는 multi-agent 호출 및 agent 간 orchestration을 설명하는 문서 진입점이다. 실제 semantics, API 변경과 권한·비용 조건은 현재 문서와 SDK를 기준으로 다시 확인해야 한다.

## 상세 정리

### 핵심 주장
1. 다중 에이전트 응답에서 루트 에이전트는 하위 에이전트를 띄우고, 그 결과를 받아 최종 답을 만든다.
2. 하위 에이전트 동시 실행 수의 권장 기본값은 3이다.
3. 다중 에이전트를 켜면 문맥 압축이 자동으로 켜지고, 루트와 각 하위 에이전트는 독립된 문맥을 유지한다.

### 구조와 패턴
- 이벤트에 에이전트 이름 속성이 붙어 누가 무엇을 말했는지 추적할 수 있다. 응답 생명주기 이벤트는 개별 에이전트가 아니라 전체 응답에 속한다.
- 응답 압축 엔드포인트, 추론 요약, 최대 도구 호출 수 설정은 다중 에이전트 모드에서 지원되지 않는다.
- 시스템이 루트와 하위 에이전트에 공통 지침을 자동으로 덧붙이며, 사용자는 이를 제거할 수 없다.

### 적용 방법
- 설계 전에 다중 에이전트 모드와 호환되지 않는 기능 목록을 확인한다.
- 결과를 합칠 때 메시지의 출처 속성을 보존하면 어느 에이전트의 결과인지 추적할 수 있다.

### 근거와 한계
- 공식 API 문서라 기능 목록과 제약은 확인되지만, 성능 이득은 정량으로 나오지 않는다.
- 원문 일부만 확인했다(중간부 생략). 실제 호출 예시와 오류 처리는 원문에서 봐야 한다.
- 제공자 API에 묶인 설명이라 다른 실행 환경에서 같은 구조가 있다고 가정할 수 없다.

### 연결
- [Multi-agent orchestration patterns](multi-agent-orchestration-patterns.md) — 감독자와 워커를 나누는 실무 구성
- [Microsoft agent design patterns](microsoft-agent-design-patterns.md) — 패턴별 조정 비용 비교
- [Anthropic multi-agent research system](anthropic-multi-agent-research-system.md) — 리서치 작업의 조율 사례

## Hermes 관련성

agent delegation 및 상위 orchestrator와 하위 agent 사이의 구조를 비교할 때 참고할 수 있다. Hermes의 native tool/API와 같은 것으로 가정하지 않습니다.
