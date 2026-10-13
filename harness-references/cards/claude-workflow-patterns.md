# Common workflow patterns for AI agents—and when to use them

- 원문: https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them
- 출처 시점: 원문 게시일 여기서는 확인하지 못함; 사용자 링크 제공 확인 2026-06-02 (KST).
- 주제: orchestration/workflow · evaluation/observability
- 상태: 사용자 제공 링크; 지식 references 등록 여부 확인되지 않음. 패턴 가이드, 운영 채택 아님.
- 권리: 미확인. 자체 요약·링크만; 전문 미보존.

## 자체 요약

고정 순서의 sequential, 독립 작업의 parallel, 평가 후 반복 개선하는 evaluator-optimizer 패턴을 비교한다. 먼저 단일 agent로 시도하고, 실제 latency 병목·독립성·측정된 품질 향상이 확인될 때에만 더 복잡한 패턴을 선택하라고 권한다.

## Hermes 관련성

작업 그래프·위임·review topology를 고를 때 간단한 선택 기준이 된다. 저자의 패턴 설명이지 각 구조의 통제된 비교 결과나 Hermes 도입 근거는 아닙니다.
