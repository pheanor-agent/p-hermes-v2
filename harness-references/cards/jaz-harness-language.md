# Harness as a Language: A Minimalist Agent Framework With Maximal Expressivity

- 원문: https://arxiv.org/abs/2609.26891 ; HTML: https://arxiv.org/html/2609.26891
- 출처 시점: arXiv v1 등록·JOB 분석 2026-09-27; 현재 arXiv 페이지는 v2 표기.
- 주제: 개요 · orchestration/workflow · context/memory · evaluation/security
- 상태: prior analysis와 `knowledge/references/github/jaz-harness-as-a-language.md` 등록 확인; 결론 C(참고만), Hermes runtime 도입·벤치마크 없음.
- 권리: arXiv 페이지 CC BY 4.0 표시; 원문/코드 미복사.

## 자체 요약

JAZ는 `invoke`를 중심으로 모델이 실행 가능한 코드를 생성하고, 호출 이력·입력·도구를 코드에서 참조하며 재귀 sub-invoke와 hook을 사용하는 미니멀 agent framework를 제안한다. 논문은 StuLife와 AppWorld의 특정 평가에서 성능·비용 결과를 보고한다. 생성 코드 실행, 예산, 검증과 관측의 경계가 핵심이다.

## Hermes 관련성

코드 기반 workflow의 표현력과 memory/재귀 loop의 실험 사례를 볼 수 있다. 기존 검토에서는 Hermes에서 해결할 측정된 pain point를 찾지 못해 참고 자료로만 분류했으며, 논문 결과는 자체 성능 주장으로 남겨야 합니다. arXiv에서 갱신된 버전과 이전 분석 대상 v1을 혼동하지 마세요.
