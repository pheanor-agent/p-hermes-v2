# Graph of Thoughts: Solving Elaborate Problems with Large Language Models

- 원문: https://arxiv.org/abs/2308.09687
- 정식 출판: AAAI 2024, arXiv source page.
- 주제: orchestration/workflow · evaluation/observability · 연구 사례
- 상태: 사용자가 직접 제공; Hermes knowledge reference registration/운영 채택은 이번 조사에서 확인되지 않음.
- 권리: arXiv version license details not independently verified. URL·자체 요약 only; paper not preserved.
- 정리 근거: 원문 일부 확인

## 자체 요약

Graph of Thoughts는 LLM의 중간 생각/산출을 graph로 모델링하고, 의존관계·변환·평가·랭킹을 사용해 여러 경로의 결과를 결합하거나 개선하는 framework를 제안합니다. 논문은 sorting, set operations, keyword counting, document merging 등의 실험을 보고하며, 원문이 제시한 결과는 저자 평가 범위로 읽어야 합니다.

## 상세 정리

### 핵심 주장
1. 기존 프롬프팅은 사고를 사슬(Chain-of-Thought)이나 나무(Tree of Thoughts)로 제한한다. 이 연구는 LLM이 만든 정보를 임의의 그래프로 모델링하자고 제안한다.
2. 그래프에서 정점은 "LLM의 생각(thought)"이고, 간선은 생각 사이의 의존성이다.
3. 이 구조로 여러 생각을 합치고, 생각 묶음을 요약하며, 피드백 루프로 생각을 다듬을 수 있다고 주장한다.
4. 저자들은 정렬 과제에서 Tree of Thoughts 대비 품질을 62% 높이면서 비용은 31% 넘게 줄였다고 보고한다. 이는 논문의 보고 수치로, 실험 조건에 따라 달라지는 출처 주장이다.

### 구조와 패턴
- 생각 변환(thought transformation)을 추가할 수 있도록 확장 가능한 구조로 설계되었다.
- 재귀와 피드백을 명시적 그래프 연산으로 표현해, 사고의 반복과 결합을 다룬다.
- 인간의 사고에 있는 재귀·네트워크 구조와 연결 짓는 것이 저자들의 문제의식이다.

### 적용 방법
- Hermes처럼 작업을 여러 노드로 나눌 때, 노드 결과를 합치는 "병합" 연산과 결과를 되먹이는 "피드백" 연산을 명시적으로 설계하는 발상으로 쓸 수 있다.
- 다만 실제 적용 전에는 같은 과제에서 단순 방식과 비용·품질을 비교해야 한다.

### 근거와 한계
- 원문 초록과 서론 위주로 확인했다. 실험 세부 설정과 전체 결과표는 이 정리에서 확인하지 못했다.
- 정렬 같은 합성 과제 중심이므로, 개방형 업무 에이전트에 그대로 일반화된다는 근거는 없다.
- 코드 저장소가 공개되어 있다고 원문에 명시되어 있으나, 이 정리에서 재현하지 않았다.
- 논문은 기존 방식이 사고를 한 방향으로 쌓는 데 머문다고 보고, 그래프 구조가 결합과 되먹임을 가능하게 한다고 주장한다. 이 점에서 "합치기"와 "다듬기"가 별도의 연산으로 정의된다.
- 비용 절감 수치는 정렬 과제라는 조건에 묶인다. 다른 과제에서 같은 효과가 나는지는 확인되지 않았다.

### 연결
- [Graph engineering with Claude Code](graph-engineering-claude-codez.md) — 에이전트 작업을 그래프로 설계하는 실무 관점
- [Raven composable agentic intelligence](raven-composable-agentic-intelligence.md) — 여러 하네스를 조합하는 다른 접근
- [Meta-harness](meta-harness.md) — 하네스 자체를 탐색하는 연구

## Hermes 관련성

계획/추론 workflow의 graph abstraction과 작업 산출 간 dependency를 비교할 때 참고 가능합니다. 이는 durable multi-agent runtime graph와 같은 문제라고 단정할 수 없으며, 논문 성능 수치는 별도 재현 없이 제품 효과로 일반화하지 않습니다.
