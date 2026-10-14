# 멀티 에이전트 오케스트레이션 리퍼런스 모음

- Source: https://x.com/i/status/2037902655016804496
- Alternate sources: https://composio.dev/content/openclaw-vs-hermes-agent
- Topics: orchestration-workflow, evaluation-observability-security, case-implementation
- Publication date: unknown / not independently verified
- User-provided: unknown; date: unknown
- Knowledge registration: True; evidence: knowledge/references/multi-agent-orchestration-patterns.md
- Source confirmation: 지식 문서 존재 확인; 제공 시점/등록 요청/사용자 발화는 원천 증거로 미확정
- Utilization: OpenClaw/Hermes supervisor, supervisor-worker, sentinel 및 router 패턴을 모은 기존 요약. 2차 출처와 정량 주장은 독립 확인이 필요하며 정책/실행규칙이 아님.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 지식 기록 대조 + 원문 일부 확인

## Independent summary and scope

OpenClaw/Hermes supervisor, supervisor-worker, sentinel 및 router 패턴을 모은 기존 요약. 2차 출처와 정량 주장은 독립 확인이 필요하며 정책/실행규칙이 아님.

## 상세 정리

### 핵심 주장
1. 여러 에이전트 구성은 다섯 가지로 나눠 비교할 수 있다. 실행 에이전트와 감시 에이전트의 짝, 두 시스템을 잇는 하이브리드, supervisor-worker, 출력 검증 전담(sentinel), router + 전문 에이전트.
2. 차이는 누가 감독하는지, 품질 검증이 어디서 일어나는지, 대화가 반드시 끝나는지(종료 보장)에 있다.
3. 별도 감독 에이전트 없이 출력 검증 게이트만 덧붙이는 sentinel 방식이 기존 구조를 가장 적게 바꾸는 선택으로 정리되어 있다.

### 구조와 패턴
- **실행 + 감시 짝**: 한 에이전트가 실행하고 다른 에이전트가 출력 채널을 감시해 승인하거나 사람에게 올린다. 상태 요청·검토 요청·에스컬레이션·승인 네 가지 의도 표시를 쓰고, 최대 세 메시지로 대화가 끝나게 해 무한 핑퐁을 막는다.
- **하이브리드**: 고성능 모델 supervisor가 계획·분해하고, 다른 시스템의 워커들이 병렬 실행하며, supervisor가 검토한다. 한쪽이 실패하면 다른 쪽이 고친다. 종료 보장은 없다.
- **supervisor-worker**: supervisor가 요청을 분해·라우팅하고 결과를 통합·검증한다. 워커는 싼 전문 모델을 쓴다. 함정은 supervisor 병목, 잘못된 라우팅, 토큰 한계, 지연이다. 대응은 라우터 도입, 결정 로직 시험, 계층적 분해다.
- **sentinel**: 전문 에이전트들과 조정자 위에 출력 검증 전담 에이전트를 둔다. 치명적 문제는 예외 없이 파이프라인을 막고, 결제·보안 같은 핵심 흐름은 사람 승인을 받으며, 운영 전에는 관찰(shadow) 모드로 돌린다.
- **router + 전문 에이전트**: 분류기만 두고 감독은 없다. 지연이 낮고 단순하지만 통합·품질 게이트가 없어, 분류가 명확한 경우에만 맞는다.

### 적용 방법
- 에이전트끼리 주고받는 메시지에는 의도 표시와 최대 왕복 수를 정해 종료를 보장한다.
- 검증 게이트는 차단 기준(무조건 막을 것)과 사람 승인 대상을 따로 정한다.
- 새 검증 단계는 관찰 모드로 먼저 돌려 오탐을 본 뒤 차단으로 바꾼다.
- 분류가 명확한 요청은 router로, 분해·통합이 필요한 요청은 supervisor로 보낸다.

### 근거와 한계
- X 게시물, 업체 블로그, QA 도구 업체 자료를 모은 2차 정리다. 비용 40~60% 절감, 피드백 시간 30% 감소, 테스트 유지보수 50~70% 감소 같은 수치는 업체 자료의 주장이며 독립 확인되지 않았다.
- 원래 기록의 "우리 시스템 적용" 평가는 작성 당시 내부 판단이라 여기서는 옮기지 않았다.

### 연결
- [OpenAI multi-agent docs](openai-multi-agent-docs.md) — 하위 에이전트 수와 핸드오프를 다룬 공식 문서
- [Microsoft agent design patterns](microsoft-agent-design-patterns.md) — 조정 비용을 따지는 복잡도 기준
- [Raven composable agentic intelligence](raven-composable-agentic-intelligence.md) — 여러 전문 에이전트를 조합하는 다른 구조

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
