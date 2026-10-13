# Graph of Thoughts: Solving Elaborate Problems with Large Language Models

- 원문: https://arxiv.org/abs/2308.09687
- 정식 출판: AAAI 2024, arXiv source page.
- 주제: orchestration/workflow · evaluation/observability · 연구 사례
- 상태: 사용자가 직접 제공; Hermes knowledge reference registration/운영 채택은 이번 조사에서 확인되지 않음.
- 권리: arXiv version license details not independently verified. URL·자체 요약 only; paper not preserved.

## 자체 요약

Graph of Thoughts는 LLM의 중간 생각/산출을 graph로 모델링하고, 의존관계·변환·평가·랭킹을 사용해 여러 경로의 결과를 결합하거나 개선하는 framework를 제안합니다. 논문은 sorting, set operations, keyword counting, document merging 등의 실험을 보고하며, 원문이 제시한 결과는 저자 평가 범위로 읽어야 합니다.

## Hermes 관련성

계획/추론 workflow의 graph abstraction과 작업 산출 간 dependency를 비교할 때 참고 가능합니다. 이는 durable multi-agent runtime graph와 같은 문제라고 단정할 수 없으며, 논문 성능 수치는 별도 재현 없이 제품 효과로 일반화하지 않습니다.
