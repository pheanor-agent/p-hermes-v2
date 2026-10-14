# Code as Agent Harness

- 원문: https://arxiv.org/abs/2605.18747
- 출처 시점: arXiv entry 2026-05 (정확한 날짜 미확인); retrieved 2026-10-14.
- 주제: overview · context/memory/knowledge · orchestration/workflow · evaluation
- 상태: 이번 외부 조사에서 발견한 관련 survey; 사용자 제공 근거·knowledge 등록·Hermes 활용은 확인되지 않음.
- 권리: arXiv page license icon indicates CC BY 4.0; article/body not copied.
- 정리 근거: 지식 기록 기준(원문 미열람)

## 자체 요약

코드를 단순 결과물이 아니라 agent의 reasoning, action, environment modeling, execution verification을 연결하는 operational substrate로 보는 관점을 제안한다. Abstract 요약은 harness interface·mechanism·evaluation/evolution을 층으로 묶고, state, memory, tool use와 safety oversight를 연구 과제로 다룬다고 설명한다.

## 상세 정리

### 핵심 주장
- 코드를 단순한 산출물이 아니라, 에이전트의 추론·행동·환경 모델링·실행 검증을 잇는 운영 기반으로 보자는 관점이 기록되어 있다.
- 이 관점에서 하네스 인터페이스, 실행 메커니즘, 평가와 진화를 층으로 묶고, 상태·메모리·도구 사용·안전 감독을 아직 남은 연구 과제로 두는 것으로 기록되어 있다.

### 구조와 패턴
- 개관(survey) 형식의 논문으로 기록되어 있으며, 관련 논문을 모은 공개 목록 저장소가 함께 언급된다.
- 분류는 하네스 인터페이스, 실행 메커니즘, 평가·진화의 세 층으로 정리되어 있다.

### 적용 방법
- 원문을 열람하지 못해 구체적 적용 절차는 정리하지 않는다. 연구 동향을 파악하는 목록으로 먼저 쓰고, 채택 판단은 원문 확인 뒤 별도로 해야 한다.

### 근거와 한계
- 지식 기록 기준(원문 미열람)이다. arXiv 초록 페이지에서는 제목, 분야, 제출 월, 라이선스 표시만 추출되었고 초록 본문은 확인되지 않았다. 위 내용은 카드 기록을 옮긴 것이며 논문의 주장과 실험 결과는 검증되지 않았다.
- 논문의 평가 방법이나 벤치마크, 제시된 프레임워크의 세부 구성은 확인하지 못했다.
- 권리는 arXiv 페이지의 CC BY 4.0 표시에 따르며, 본문은 복사하지 않았다.
- 사용자 제공 근거와 실제 활용 여부는 확인되지 않았다.

### 연결
- [agentic-harness-evolution.md](agentic-harness-evolution.md) — 하네스 구성 요소가 시간에 따라 어떻게 바뀌는지 비교하는 짝 자료다.
- [agent-harness-technical-debt.md](agent-harness-technical-debt.md) — 같은 하네스 층위를 운영 부채 관점에서 다룬 자료다.
- [meta-harness.md](meta-harness.md) — 하네스를 다시 설계하고 평가하는 메타 수준의 접근과 대조할 수 있다.

## Hermes 관련성

실행 환경 자체를 표현·검증하는 코드/절차의 역할을 연구 관점에서 정리한다. 논문 제안과 실험적 주장으로 분류하며 Hermes에서 채택·검증된 접근으로 보지 않습니다.
