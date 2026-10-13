# How we built our multi-agent research system

- 원문: https://www.anthropic.com/engineering/multi-agent-research-system
- 출처 시점: 2025-06-13 (Anthropic Engineering 글의 알려진 게시일; 재확인 미수행)
- 주제: orchestration/workflow · evaluation/observability · 사례
- 상태: 사용자 제공 링크 여부 미확인; 외부 공식 사례로 추가. Hermes 도입 아님.
- 권리: 미확인. 요약·링크만; 전문 미보존.

## 자체 요약

리드 에이전트가 질의를 계획하고 서로 독립적인 탐색을 병렬 subagent에 위임하는 연구 시스템을 설명한다. breadth-first 탐색에서 병렬화가 강점을 보일 수 있지만, 시스템 구성·작업 분해·결과 합성·비용과 latency trade-off가 핵심이다. 공개된 성과 수치는 Anthropic 내부 평가의 출처 주장으로 취급한다.

## Hermes 관련성

독립 조사 태스크가 다수인 경우 fan-out의 이점을 검토할 때 참고할 수 있다. 일반 코딩이나 서로 의존하는 일에 병렬화가 우월하다는 보편적 증거가 아닙니다.
