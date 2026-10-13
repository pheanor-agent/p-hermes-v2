# Harness design for long-running application development

- 원문: https://www.anthropic.com/engineering/harness-design-long-running-apps
- 출처 시점: 추출 페이지에서 게시 날짜 확인 불가; 직접 확인 2026-10-14.
- 주제: 개요 · orchestration/workflow · evaluation · 사례
- 상태: 인접 핵심 자료로 원천 확인; 사용자가 직접 URL을 제공했는지는 미확인. 설계 참고, Hermes에서 미실행.
- 권리: 확인되지 않음. 요약·링크만; 전문 미보존.

## 자체 요약

복잡한 응용 개발에 planner, generator, evaluator 역할을 나누고, 큰 작업을 작은 단위로 쪼개며, context reset 때 구조화된 handoff를 사용한 사례다. 생성자가 자기 결과를 과대평가할 수 있어 독립 evaluator와 명시적 기준을 두는 접근을 설명한다. 단, 별도 에이전트와 reset은 orchestration 복잡도·token·latency를 증가시킨다.

## Hermes 관련성

작성자와 평가자 분리, 명시 기준, handoff를 비교하는 자료다. 평가자 분리만으로 객관성·안전성이 확보되는 것은 아니며, deterministic test·외부 evidence를 대체하지 않습니다.
