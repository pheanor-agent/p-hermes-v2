# Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses

- 원문: https://arxiv.org/abs/2604.25850
- 출처 시점: arXiv page shows v4; retrieved 2026-10-14.
- 주제: evaluation/observability · orchestration/workflow · case/implementation
- 상태: 외부 검색에서 발견한 인접 연구; 사용자 제공·지식 등록·Hermes 활용 확인되지 않음.
- 권리: arXiv page license details not verified; link and original summary only.
- 정리 근거: 지식 기록 기준(원문 미열람)

## 자체 요약

제목과 arXiv abstract page를 확인한 결과, coding-agent harness를 observability 중심으로 자동 진화시키는 접근을 다룬 연구다. 본문과 벤치마크 설계·결과를 이번 범위에서 읽지 않았으므로 구체적 성능 수치나 실험 결론을 인용하지 않습니다.

## 상세 정리

### 핵심 주장
- 이 연구는 코딩 에이전트의 하네스를 관측 결과에 기반해 자동으로 진화시키는 접근을 다룬다. 제목이 가리키는 방향은 하네스 자체를 설계 대상으로 두고, 관측 데이터로 그 구성요소를 고치는 것이다.
- 핵심 질문은 관측 가능성과 하네스 변경 사이의 연결에 있다. 어떤 신호를 보고 어떤 하네스 변경을 채택하는지가 연구의 중심으로 보인다.
- 성능 수치와 실험 결론은 이번 정리에서 확인하지 못했으므로 인용하지 않는다.

### 구조와 패턴
- 제목으로 드러나는 구조는 관측 단계와 진화 단계의 반복이다. 실행 기록을 수집하고, 개선 후보를 만들고, 평가해 채택하는 순환으로 읽힌다.
- 모델이 아니라 하네스의 코드나 설정이 탐색 대상이라는 점이 특징으로 보인다.

### 적용 방법
- 현재 단계에서는 연구 후보로만 둔다. 실제 적용 전에 원문의 실험 조건, 벤치마크, 채택 기준을 읽고 판단해야 한다.
- 자체 하네스에 옮긴다면 먼저 관측 신호를 정하고 변경 전후를 비교할 기준을 세운다. 자동 변경을 바로 채택하지 않고 검토 단계를 둔다.

### 근거와 한계
- 원문은 열람하지 않았다. 초록 본문이 페이지에서 추출되지 않아 제목과 메타데이터만 확인했다.
- 라이선스는 확인하지 못했고, 원문 텍스트는 옮기지 않았다. 이 정리는 제목 수준의 판단이므로 방법과 결과에 대한 주장으로 읽으면 안 된다.

### 연결
- [meta-harness.md](meta-harness.md) — 하네스 전체를 최적화하는 인접 연구로, 탐색 대상이 같은 계열이다.
- [agent-harness-technical-debt.md](agent-harness-technical-debt.md) — 하네스 구성요소를 줄이거나 바꾸는 판단 기준을 제공한다.
- [claude-code-loop-engineering-20-step.md](claude-code-loop-engineering-20-step.md) — 관측과 반복 실행을 묶는 실무 루프와 비교하기 좋다.

## Hermes 관련성

telemetry/evaluation feedback과 harness change 사이의 관계를 조사할 추가 연구 후보로 분류했다. 현재는 title/abstract-level lead이며, 권고나 검증 결과로 취급하지 않습니다.
