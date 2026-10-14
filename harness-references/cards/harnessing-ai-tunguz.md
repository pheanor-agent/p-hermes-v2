# Harnessing AI

- Source: https://tomtunguz.com/harnessing-ai/
- Alternate sources: none recorded
- Topics: overview, orchestration-workflow, context-memory-knowledge, case-implementation
- Publication date: unknown / not independently verified
- User-provided: True; date: 2026-06-01
- Knowledge registration: False; evidence: No exact reference card verified; references index has separate software-after-AI item only
- Source confirmation: URL/제공 사건은 원천 메시지 증거로 확인; 본문 전문 및 활용 근거 미확인
- Utilization: 사용자가 66자 요청과 함께 링크를 제공한 것이 DB 증거로 확인됨. 하네스에 관한 글로서 제목 수준에서 포함; 이번 조사에서 본문 내용/사용 근거를 확인하지 못해 요약을 확대하지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 원문 일부 확인

## Independent summary and scope

사용자가 66자 요청과 함께 링크를 제공한 것이 DB 증거로 확인됨. 하네스에 관한 글로서 제목 수준에서 포함; 이번 조사에서 본문 내용/사용 근거를 확인하지 못해 요약을 확대하지 않음.

## 상세 정리

### 핵심 주장
1. 소프트웨어 공학의 무게가 UI와 데이터 관리에서 "하네스"로 옮겨 간다. 하네스는 LLM을 신뢰할 수 있는 에이전트로 만드는 런타임, 제약, 신뢰성 계층이다.
2. 하네스는 일곱 요소로 설명된다. 문맥과 메모리, 도구와 행동, 오케스트레이션과 루프, 상태와 영속성, 샌드박스와 연산 환경, 관측과 거버넌스, 비용과 워크플로 최적화다.
3. 일반 모델은 업무마다 맞춤 검색이 필요하다. 같은 검색으로는 방사선 전문의와 법률 보조원의 문맥을 모두 채울 수 없다는 것이다.

### 구조와 패턴
- 문맥 데이터베이스는 조직이 실제로 일하는 방식, 곧 표준 절차를 "레시피"로 모은 것이다. 이를 처음 포착하고 조직 변화에 따라 계속 갱신한다.
- 도구는 레지스트리로 노출하고, 인자를 검증하며, 민감한 행동은 승인 뒤에 실행하고, 결과를 다시 루프에 넣는 구조로 설명된다. MCP가 이를 잇는 연결 조직으로 언급된다.
- 상태 영속성에서는 7단계 작업이 실패하면 처음부터가 아니라 8단계부터 재개해야 한다는 예를 든다. 파일 시스템, 체크포인트, 세션 스레드, 아티팩트 저장소가 이를 돕는다.
- 샌드박스는 격리된 작업 공간, 통제된 네트워크 출구, 모델 밖에 있는 자격 증명으로 구성된다.

### 적용 방법
- 하네스 설계 점검표로 쓸 수 있다. 일곱 요소 각각에 현재 구현이 있는지 확인하면 빠진 층이 드러난다.
- 재개 가능성은 체크포인트와 산출물 저장으로 확보한다. Hermes의 JOB 상태 기록과 대응시켜 볼 수 있다.

### 근거와 한계
- 개인 블로그 형태의 기고이며, 정량 근거와 사례 측정은 없다.
- 개념 프레임워크 성격이므로, 일곱 요소의 우선순위나 비용 효과는 작업별 측정이 필요하다.
- 원문 전체를 확인했다.

- 저자는 하네스의 가치를 "길들임(domestication)"으로 표현한다. 모델의 힘을 그대로 쓰는 것이 아니라 제약과 신뢰성 층으로 통제해 쓴다는 뜻이다.
- 원문은 "실패 시 처음부터가 아니라 다음 단계부터 재개" 같은 운영 원칙을 구체 예로 든다. 재개 설계를 점검하는 질문으로 쓰기 좋다.

- 일곱 요소는 서로 독립이 아니다. 예를 들어 관측 층이 없으면 루프 개선이 어렵고, 상태 층이 없으면 재개가 어렵다. 원문도 이 요소들이 함께 작동해야 신뢰성이 생긴다는 취지로 읽힌다.
- 원문 후반의 거버넌스와 비용 최적화 설명은 원칙 수준이며, 구체적 임계값이나 측정 방법은 담고 있지 않다.

### 연결
- [Agent harness technical debt](agent-harness-technical-debt.md) — 하네스가 커질 때 쌓이는 기술 부채
- [OpenAI harness engineering](openai-harness-engineering.md) — 에이전트 중심 저장소 운영 사례
- [Anthropic effective long-running agents](anthropic-effective-long-running-agents.md) — 여러 문맥 창에 걸친 재개 설계

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
