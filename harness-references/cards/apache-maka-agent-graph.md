# Apache Maka: Agent Graph and stream scheduling draft

- 원문 (영어): https://github.com/apache/maka/blob/main/docs/architecture/agent-graph-stream-scheduling-draft.md
- 원문 (중국어): https://github.com/apache/maka/blob/main/docs/architecture/agent-graph-stream-scheduling-draft.zh-CN.md
- 저장소: https://github.com/apache/maka (사용자가 저장소 링크로 처음 제공)
- 출처 시점: live draft; retrieved 2026-10-14. 원문 링크 제공 2026-10-13 (KST, 내부 증거).
- 주제: orchestration/workflow · evaluation/observability · case/implementation
- 상태: 사용자 제공 링크; 현행 knowledge registration/활용 확인되지 않음. 초안 문서로 기록.
- 권리: Apache project repository; file-level license/NOTICE applicability not checked. 내용 미복사.

## 자체 요약

Apache Maka의 agent graph와 stream scheduling architecture draft로, graph scheduling과 runtime events/child sessions 관계를 논한다. 문서 자체가 draft이므로 변경 가능성이 있으며, normative/stable contract로 해석하면 안 됩니다.

## Hermes 관련성

그래프형 multi-agent workflow와 scheduling boundary의 현재 설계 논의 비교에 유용하다. 초안 상태의 제안이며 Hermes 구현·채택 또는 성능 검증 결과가 아닙니다.
