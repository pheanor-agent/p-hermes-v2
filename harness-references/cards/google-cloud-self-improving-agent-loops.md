# 7 Rules for Self-Improving Agent Loops

- Source: https://x.com/i/status/2086874630032073142
- Alternate sources: https://google.github.io/agents-cli
- Topics: evaluation-observability-security, orchestration-workflow, case-implementation
- Publication date: unknown / not independently verified
- User-provided: True; date: 2026-08-11
- Knowledge registration: True; evidence: knowledge/references/agent-evaluation/google-cloud-self-improving-agent-loops.md
- Source confirmation: 사용자 첨부 Notes 및 X 본문 대조를 기존 JOB 기록으로 확인; 첨부 원문은 현재 지정 cache 경로에서 찾지 못함
- Utilization: 측정-채점-수정 루프, 독립 grader, held-out set 및 deterministic check를 요약한 자료. 해당 JOB의 synthetic pilot 설계 근거와 분리해 표기; 전역 자동수정 채택 아님.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 원문 일부 확인

## Independent summary and scope

측정-채점-수정 루프, 독립 grader, held-out set 및 deterministic check를 요약한 자료. 해당 JOB의 synthetic pilot 설계 근거와 분리해 표기; 전역 자동수정 채택 아님.

## 상세 정리
### 핵심 주장
1. 코딩 에이전트가 다른 에이전트를 만들고 개선하는 시대에는, 엔지니어링의 핵심이 코드 작성에서 "무엇이 좋은가"를 정의하고 측정하는 일로 옮겨 간다.
2. 루프(지침 작성 → 실행 → 실패 지점 찾기 → 고치기 → 반복)는 자동화할 수 있지만, "더 나음"의 기준은 사람이 정해야 한다.
3. 얕은 지표를 주면 에이전트는 점수는 높지만 실제로는 나쁜 결과를 낼 수 있다. 그리고 자기 기준으로는 성공했다고 보고한다.
4. 공개 벤치마크는 기업 고유의 환불 규칙, 에스컬레이션 기준, 준수 문구 같은 기준을 잘 재지 않는다. 그래서 팀마다 직접 지표를 만들어야 한다.

### 구조와 패턴
- 지표가 프롬프트·코드·행동 전부의 상위에 있다는 관점이다. 루프는 지표가 보상하는 방향으로 셋을 모두 바꾼다.
- 예시로 "응답 전에 유지 제안을 먼저 한다"는 규칙을 든다. 내부 추론에서는 맞아도 최종 답변에서 빠지는 실패가 있어, 추론이 아니라 최종 응답을 채점하는 평가가 필요하다는 것이다.
- 맞춤 지표는 0/1 점수와 한 줄 사유를 갖는 형태로 정의하고, 버전 관리하며 새 실패가 나올 때마다 날카롭게 다듬는다.
- agents-cli는 ADK로 만든 에이전트에 대해 이 루프를 몇 개의 명령으로 실행하도록 돕는 오픈소스 도구로 소개된다.

### 적용 방법
- 루프를 돌리기 전에 "좋음"을 정의하는 지표와 그 지표의 채점 방식을 먼저 문서로 고정한다.
- 채점 대상은 중간 추론이 아니라 사용자가 실제로 받는 출력으로 한다.
- 지표를 최적화하는 루프가 지표 자체를 바꾸지 못하도록, 지표 정의는 루프 밖에서 사람이 관리한다.

### 근거와 한계
- 원문은 구글 클라우드 팀의 제품 소개 성격의 글이며, 개선율 같은 정량 결과는 이 정리에서 확인하지 못했다.
- 이 정리는 원문 앞부분의 원칙과 예시 위주로 확인했다. 나머지 규칙 목록의 세부 내용은 원문에서 다시 확인해야 한다.
- 이 루프를 Hermes 작업에 자동 적용하는 것은 별도 설계와 승인이 필요하며, 이 글은 그 근거가 되지 못한다.

- 원문이 강조하는 점은 지표가 곧 산출물이라는 것이다. 따라서 지표 정의 문서는 코드와 같은 방식으로 버전을 남기고 리뷰해야 한다.

### 연결
- [Agent harness technical debt](agent-harness-technical-debt.md) — 평가와 관측 없이 하네스가 커지는 위험
- [Google Cloud long-horizon patterns](google-cloud-long-horizon-patterns.md) — 같은 제공자의 장기 작업 패턴
- [Anthropic building effective agents](anthropic-building-effective-agents.md) — 평가 기반 반복 개선의 원칙

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
