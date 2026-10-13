# Hidden Technical Debt of AI Systems: Agent Harness

- 원문: https://leehanchung.github.io/blogs/2026/05/08/hidden-technical-debt-agent-harness/
- 출처 시점: 2026-05-08 (원문 표기)
- 주제: 개요 · evaluation/security · orchestration
- 상태: 사용자 제공 링크 확인; Hermes 지식 references에 등록 기록 있음; 분석 참고, 도입 근거 아님.
- 권리: 미확인. 공개 요약·링크만; 원문 미보존.

## 자체 요약

모델과 환경 사이의 하네스를 prompt/persona, tool surface, rollout protocol, context manager, memory, sub-agent topology, guardrail, verifier, observability 등으로 나눈다. 하네스를 OS에 비유하되, 모델 역량이 상승하면 한때 필요한 scaffolding이 불필요한 유지보수 부채가 될 수 있으므로 하네스의 구성요소를 영구 제품 표면으로 가정하지 말라는 논지다.

## Hermes 관련성

용어 범위를 넓히고 외부 하네스 사례를 비교할 때 유용하다. 논설적 전망이며 Hermes 구현이 실제로 부채가 되었거나 폐기되어야 한다는 실측은 아니다. 현재 실패·비용·운영 데이터를 별도로 대조해야 한다.

## 제공·활용·권리

사용자 링크 제공을 확인했습니다. 내부 references의 요약은 확인됐으나 Hermes 운영 채택 증거는 아닙니다. 라이선스 미확인으로 텍스트·이미지를 복사하지 않았습니다.
