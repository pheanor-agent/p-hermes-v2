# AI agent design patterns (Microsoft Azure Architecture Center)

- 원문: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
- 출처 시점: living documentation; 사용자 링크 제공 확인 2026-10-02 (KST); page body not rechecked.
- 주제: overview · orchestration/workflow · evaluation/security
- 상태: user-provided reference; registration/utilization in Hermes not verified.
- 권리: terms not checked; link and original short summary only.
- 정리 근거: 원문 일부 확인

## 자체 요약

Microsoft Architecture Center guide on AI agent design patterns, useful as a vendor architecture overview. This card does not claim specific current pattern details without a fresh page review.

## 상세 정리
### 핵심 주장
1. 에이전트 시스템은 복잡도 단계가 있다. 직접 모델 호출, 도구를 가진 단일 에이전트, 다중 에이전트 오케스트레이션 순으로 올라간다.
2. 각 단계는 조정 비용, 지연, 비용을 더한다. 그래서 요구를 신뢰성 있게 충족하는 가장 낮은 단계를 고르라고 권한다.
3. 프롬프트 엔지니어링으로 풀리는 문제라면 에이전트가 필요 없다는 점을 먼저 확인해야 한다.

### 구조와 패턴
- 원문 표는 네 단계를 제시한다. 직접 모델 호출은 분류·요약·번역 같은 단일 단계 작업에 쓴다. 단일 에이전트는 한 도메인 안에서 도구를 고르고 여러 번 호출하며 결과를 다듬는다. 그 위에 다중 에이전트 오케스트레이션이 있다.
- 오케스트레이션 패턴은 순차, 동시(병렬), 그룹 대화, 핸드오프, 매니저 중심 같은 형태로 나뉜다고 설명된다. 각 패턴은 작업 흐름의 의존 관계에 따라 고른다.
- 단일 에이전트가 기본값으로 충분한 경우가 많다고 말하며, 기업 사례에서는 이 단계가 가장 흔한 기본값이라고 설명한다.

### 적용 방법
- Hermes에서 새 자동화를 설계할 때, 먼저 단일 호출과 도구 하나로 풀리는지 측정한다.
- 다중 에이전트를 쓰기로 했다면 의존 관계가 실제로 병렬인지, 순차인지 그림으로 확인한 뒤 패턴을 고른다.
- 조정 비용이 늘면 실패 지점도 늘어나므로, 각 단계의 검증과 재개 지점을 함께 정한다.

### 근거와 한계
- 설계 지침 문서이며, 패턴별 정량 비교 결과는 확인하지 못했다.
- 원문 앞부분의 단계 구분과 선택 기준 위주로 확인했다. 개별 패턴의 세부 예시와 코드는 원문에서 확인해야 한다.
- Azure 중심의 예시이므로, 다른 플랫폼에 옮길 때는 개념만 가져오는 것이 안전하다.

### 연결
- [Anthropic building effective agents](anthropic-building-effective-agents.md) — 단순함에서 시작하라는 같은 원칙
- [Multi-agent orchestration patterns](multi-agent-orchestration-patterns.md) — 다중 에이전트 조율의 실무 사례
- [OpenAI multi-agent docs](openai-multi-agent-docs.md) — 핸드오프와 하위 에이전트 구조

## Hermes 관련성

외부 vendor framework로 pattern taxonomy를 비교할 때 보조 참조다. 제품-specific diagrams/patterns와 Hermes operations를 동일시하지 않습니다.
