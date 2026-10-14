# Harness design for long-running application development

- 원문: https://www.anthropic.com/engineering/harness-design-long-running-apps
- 출처 시점: 추출 페이지에서 게시 날짜 확인 불가; 직접 확인 2026-10-14.
- 주제: 개요 · orchestration/workflow · evaluation · 사례
- 상태: 인접 핵심 자료로 원천 확인; 사용자가 직접 URL을 제공했는지는 미확인. 설계 참고, Hermes에서 미실행.
- 권리: 확인되지 않음. 요약·링크만; 전문 미보존.
- 정리 근거: 원문 일부 확인

## 자체 요약

복잡한 응용 개발에 planner, generator, evaluator 역할을 나누고, 큰 작업을 작은 단위로 쪼개며, context reset 때 구조화된 handoff를 사용한 사례다. 생성자가 자기 결과를 과대평가할 수 있어 독립 evaluator와 명시적 기준을 두는 접근을 설명한다. 단, 별도 에이전트와 reset은 orchestration 복잡도·token·latency를 증가시킨다.

## 상세 정리

### 핵심 주장
- 프론트엔드 디자인 품질과 장시간 자율 소프트웨어 개발, 두 문제에서 기존 하네스가 천장에 닿았다는 문제의식에서 출발한다. 프롬프트 개선과 단일 에이전트 하네스만으로는 복잡한 작업에서 방향을 잃는다는 것이다.
- 핵심 처방은 생성자(generator)와 평가자(evaluator)를 분리하는 것이다. 자기 결과를 평가하는 에이전트는 결과를 지나치게 긍정적으로 평가하는 경향이 있어, 별도의 회의적인 평가자를 튜닝하는 쪽이 더 다루기 쉽다고 본다.
- 주관적인 디자인 품질을 채점 가능하게 만들기 위해 네 가지 기준(디자인 품질, 독창성, 기술적 완성도, 기능성)을 정의한다. 독창성과 디자인 품질에 더 큰 가중치를 두어 템플릿풍 결과를 밀어냈다고 적는다.
- 긴 작업에서는 compaction보다 context reset이 낫다고 주장한다. compaction은 같은 에이전트가 요약된 이력으로 계속하므로 맥락 불안(context anxiety)이 남을 수 있는 반면, reset은 구조화된 인수인계와 함께 깨끗한 상태에서 다시 시작한다.
- 최종 구조는 planner, generator, evaluator 세 에이전트다. 플래너가 스펙을 작업 단위로 쪼개고, 생성자가 구현하며, 평가자가 기준에 따라 검증한다.

### 구조와 패턴
- 평가자는 few-shot 예시와 점수 분해(score breakdown)로 교정해, 반복 과정에서 점수가 흔들리는 현상(score drift)을 줄였다.
- 인수인계는 구조화된 아티팩트로 한다. reset 후 새 에이전트가 이전 상태와 다음 단계를 바로 이어받을 수 있어야 한다.
- 부록에는 플래너가 만든 계획 예시가 있으며, 제품 개요와 기능별 사용자 스토리를 포함한다.

### 적용 방법
- 작성자와 평가자를 다른 프롬프트·다른 역할로 분리하고, 평가 기준을 문서로 먼저 고정하는 절차를 검토할 수 있다.
- 평가 기준의 가중치를 명시하면 생성 결과의 편향을 방향성 있게 조정할 수 있다는 점이 실무 힌트다.
- 다만 reset은 토큰·지연 비용을 늘리므로, 작업 길이와 실패 빈도를 보고 compaction과 reset 중 무엇을 쓸지 결정해야 한다.

### 근거와 한계
- 원문 일부 확인: 원문 앞부분과 뒷부분, 부록을 읽었다. 중간 구간(평가 실험 세부와 결과 수치)은 추출에서 생략되어 직접 확인하지 못했다.
- 평가자도 여전히 LLM이므로 생성 결과에 관대할 수 있다는 점을 저자가 인정한다. 평가자 분리가 객관성을 보장하지는 않는다.
- 주관적 디자인 기준은 저자의 취향에 맞춰 교정된 것이다. 다른 취향이나 도메인에 그대로 옮길 수 있는지는 확인되지 않았다.
- 본문에 정량적 성능 비교가 있는지 이번 추출 범위에서는 확인하지 못했다. 성능 주장은 원문 확인 전까지 정성적 설명으로만 취급한다.

### 연결
- [anthropic-effective-long-running-agents.md](anthropic-effective-long-running-agents.md) — 이 글이 확장한 선행 설계로, initializer와 coding agent의 출발점
- [anthropic-building-effective-agents.md](anthropic-building-effective-agents.md) — 에이전트 워크플로 패턴의 일반 원칙과 비교할 때 참고
- [agent-harness-technical-debt.md](agent-harness-technical-debt.md) — 역할 분리와 reset이 늘리는 오케스트레이션 복잡도를 점검할 때 참고

## Hermes 관련성

작성자와 평가자 분리, 명시 기준, handoff를 비교하는 자료다. 평가자 분리만으로 객관성·안전성이 확보되는 것은 아니며, deterministic test·외부 evidence를 대체하지 않습니다.
