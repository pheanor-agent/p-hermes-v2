# Building effective agents

- 원문: https://www.anthropic.com/engineering/building-effective-agents
- 출처 시점: 원문 게시 시점 2024-12 (Anthropic 공식 글); 직접 확인 2026-10-14.
- 주제: 개요 · orchestration/workflow · skills/tools
- 상태: 사용자 제공 링크 확인(2026-06-02 KST, 내부 출처 증거); 지식 references 등록은 확인되지 않음. 배경 참고.
- 권리: 미확인. 자체 요약·링크만; 전문 미보존.

## 자체 요약

필요 이상으로 복잡한 agent framework부터 도입하지 말고, 단순한 prompt/workflow로 시작해 평가를 통해 부족함이 확인된 경우에만 routing, parallelization, evaluator-optimizer 등 복잡성을 추가하라는 원칙을 제시한다. 도구 인터페이스와 문서화의 품질도 중요하게 다룬다.

## Hermes 관련성

하네스의 복잡도를 실제 문제·측정·검증에 맞춰 늘리는 기본 비교 기준이다. 가이드의 패턴은 결과를 보장하지 않으며, 실제 적용 판단에는 작업별 평가가 필요합니다.
