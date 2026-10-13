# Orchestrating multiple agents and handing off work

- OpenAI Responses API: https://developers.openai.com/api/docs/guides/responses-multi-agent
- OpenAI API orchestration guide: https://platform.openai.com/docs/guides/agents/orchestration
- 출처 시점: 사용자가 링크 제공한 2026-09-23 (KST, 내부 evidence); 이번 세션에서 각 페이지의 최신 내용 확인은 생략.
- 주제: orchestration/workflow · tools
- 상태: 사용자 제공; knowledge references 등록/운영 활용 확인 안 됨. 참고 링크.
- 권리: 미확인. 자체 요약·링크만; 본문 미복사.

## 자체 요약

두 공식 개발자 문서 링크는 multi-agent 호출 및 agent 간 orchestration을 설명하는 문서 진입점이다. 실제 semantics, API 변경과 권한·비용 조건은 현재 문서와 SDK를 기준으로 다시 확인해야 한다.

## Hermes 관련성

agent delegation 및 상위 orchestrator와 하위 agent 사이의 구조를 비교할 때 참고할 수 있다. Hermes의 native tool/API와 같은 것으로 가정하지 않습니다.
