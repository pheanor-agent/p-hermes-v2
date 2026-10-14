# Meta-Harness: End-to-End Optimization of Model Harnesses

- 원문: https://arxiv.org/abs/2603.28052 ; 코드: https://github.com/stanford-iris-lab/meta-harness
- 출처 시점: 논문 2026-03-30 (arXiv 기록); 사용자 repository 링크 제공 확인 2026-06-27 (KST).
- 주제: context/memory/knowledge · evaluation · 사례/구현
- 상태: 사용자 제공 code link; `knowledge/references/github/meta-harness.md` 등록, 논문 및 구현을 references/index에 기록. 연구/실험 참고, 도입 아님.
- 권리: arXiv 페이지 CC BY 4.0 표시; 공개 코드 저장소에 LICENSE 파일 존재하나 본 조사에서 조건 검토 안 함. 원문/코드 미복사.
- 정리 근거: 원문 일부 확인

## 자체 요약

고정된 base model 주변의 task-specific harness를 검색·최적화하는 framework다. proposer가 이전 후보의 코드·실행 trace·평가 결과를 탐색하고 새 후보를 제안하며 이를 반복 실행·평가한다. 논문은 text classification과 retrieval-augmented math 등 특정 benchmark의 결과를 보고한다.

## 상세 정리
### 핵심 주장
1. LLM 시스템의 성능은 모델 가중치뿐 아니라 하네스 코드, 즉 무엇을 저장하고 무엇을 찾아 모델에 보여 줄지 정하는 코드에 크게 좌우된다.
2. 하네스는 여전히 사람이 손으로 설계하는 경우가 많다.
3. 기존 텍스트 최적화 도구는 피드백을 너무 압축한다. 점수만 보거나, 짧은 요약만 보거나, 이전 시도를 기억하지 못한다. 그래서 하네스 탐색에 맞지 않는다고 주장한다.
4. 이를 해결하기 위해 Meta-Harness라는 바깥 루프 시스템을 제안한다. 이 시스템은 에이전트형 제안자가 파일 시스템을 통해 모든 이전 후보의 코드, 점수, 실행 추적을 열어 보고 다음 후보를 만든다.

### 구조와 패턴
- 제안자는 이전 후보 전체에 접근한다. 압축된 요약이 아니라 원본 추적을 읽는다는 점이 핵심 차이다.
- 저자들은 세 과제에서 결과를 보고한다. 온라인 텍스트 분류에서는 기존 문맥 관리 시스템보다 7.7점 높고 문맥 토큰은 4배 적게 쓴다고 한다. 수학 추론에서는 한 번 찾은 하네스가 여러 보류 모델에서 평균 4.7점 높다고 한다. 에이전트 코딩에서는 TerminalBench-2에서 사람이 만든 최고 기준선을 넘었다고 한다.
- 이 수치들은 저자들이 보고한 출처 주장이며, 과제와 모델 조건에 묶인다.

### 적용 방법
- Hermes에서 하네스 개선을 시도한다면, 이전 시도의 코드와 실행 기록을 파일로 남겨 제안자가 직접 읽을 수 있게 하는 구조가 대응된다.
- 점수만 보고 고치는 방식보다, 실패 추적을 함께 보는 방식이 더 나은 근거를 준다는 것이 이 논문의 교훈이다.
- 실제 적용은 평가 세트와 비용 상한을 먼저 정하고, 사람이 최종 후보를 승인하는 절차가 필요하다.

### 근거와 한계
- 초록과 서론 일부를 확인했다. 실험 세부와 전체 결과표는 확인하지 못했다.
- 자동 탐색은 평가 세트에 과적합될 위험이 있다. 보류 모델 결과가 있다는 점은 완화 근거이지만 완전한 해결은 아니다.
- 이 정리는 정리자가 읽은 범위에서 작성되었으며, 코드 저장소는 재현하지 않았다.

### 연결
- [JAZ harness as a language](jaz-harness-language.md) — 최소 하네스라는 반대 방향의 탐구
- [Raven composable agentic intelligence](raven-composable-agentic-intelligence.md) — 하네스를 자동으로 만들고 발전시키는 다른 시도
- [Agent harness technical debt](agent-harness-technical-debt.md) — 하네스가 커질 때의 부담

## Hermes 관련성

하네스 설계가 추상 논의에 그치지 않도록 후보·실행·평가 기록을 연결하는 연구 사례다. 벤치마크에서 보고된 효과는 Hermes 환경에서의 성능 근거가 아니며, 코드 저장소 README도 실험적 상태를 경고합니다.
