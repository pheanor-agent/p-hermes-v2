# Meta-Harness: End-to-End Optimization of Model Harnesses

- 원문: https://arxiv.org/abs/2603.28052 ; 코드: https://github.com/stanford-iris-lab/meta-harness
- 출처 시점: 논문 2026-03-30 (arXiv 기록); 사용자 repository 링크 제공 확인 2026-06-27 (KST).
- 주제: context/memory/knowledge · evaluation · 사례/구현
- 상태: 사용자 제공 code link; `knowledge/references/github/meta-harness.md` 등록, 논문 및 구현을 references/index에 기록. 연구/실험 참고, 도입 아님.
- 권리: arXiv 페이지 CC BY 4.0 표시; 공개 코드 저장소에 LICENSE 파일 존재하나 본 조사에서 조건 검토 안 함. 원문/코드 미복사.

## 자체 요약

고정된 base model 주변의 task-specific harness를 검색·최적화하는 framework다. proposer가 이전 후보의 코드·실행 trace·평가 결과를 탐색하고 새 후보를 제안하며 이를 반복 실행·평가한다. 논문은 text classification과 retrieval-augmented math 등 특정 benchmark의 결과를 보고한다.

## Hermes 관련성

하네스 설계가 추상 논의에 그치지 않도록 후보·실행·평가 기록을 연결하는 연구 사례다. 벤치마크에서 보고된 효과는 Hermes 환경에서의 성능 근거가 아니며, 코드 저장소 README도 실험적 상태를 경고합니다.
