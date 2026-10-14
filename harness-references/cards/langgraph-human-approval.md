# Add human-in-the-loop review to LangGraph tool calls

- 원문: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop
- 출처 시점: documentation URL; 사용자 링크 제공 확인 2026-10-02 (KST); current content not rechecked.
- 주제: orchestration/workflow · evaluation/observability/security
- 상태: 사용자 제공; internal knowledge registration not verified. Implementation-document reference only.
- 권리: terms not checked; link and summary only.
- 정리 근거: 원문 일부 확인

## 자체 요약

LangGraph documentation page for adding human-in-the-loop review to tool calls. The reference concerns a framework-specific implementation pattern; this library does not assert its current API compatibility or safe deployment.

## 상세 정리

### 핵심 주장
1. 사람 검토는 그래프 실행 중간에 "중단(interrupt)"으로 넣을 수 있다. 중단 지점에서 그래프 상태가 저장되고, 외부 입력이 올 때까지 기다린다.
2. 중단은 노드 안 어디에서나 호출할 수 있고, 조건에 따라 동적으로 걸 수 있다. 정해진 지점에서만 멈추는 정적 중단점과 구분된다.
3. 중단 시 전달되는 값은 호출자에게 `__interrupt__` 필드로 돌아가, 그래프가 무엇을 기다리는지 알 수 있다.

### 구조와 패턴
- 체크포인터가 그래프 상태를 저장하고, `thread_id`가 상태의 커서 역할을 한다. 같은 ID를 쓰면 같은 체크포인트에서 재개되고, 새 ID를 쓰면 빈 상태의 새 스레드가 된다.
- 재개는 Command로 그래프를 다시 호출해 이루어지며, 그 값이 중단 지점의 반환값이 된다.
- 도구 호출 직전에 승인을 받는 패턴이 제목에 나온다.

### 적용 방법
- 민감한 도구 호출 앞에 중단을 두고, 승인 결정(승인·수정·거절)을 재개 입력으로 받는 구조가 가능하다.
- Hermes의 승인 게이트와 비교하면, 중단 지점의 상태 저장과 승인 근거 기록을 함께 설계해야 재개 시 같은 결정이 보장된다.

### 근거와 한계
- LangGraph 공식 how-to 문서 일부를 확인했다. 전체 예제 코드와 버전별 차이는 이 정리에서 확인하지 못했다.
- 프레임워크 기능 설명이며, 승인 정책의 적절성이나 운영 효과에 대한 근거는 없다.
- 재개 시 같은 thread_id를 쓰면 중단 시점의 상태가 그대로 이어진다. 그래서 승인 기록과 재개 키를 함께 남겨야 "어떤 상태에 대한 승인인지"가 추적된다.
- 중단을 조건부로 거는 기능은 "위험할 때만 사람에게 묻기"에 맞는다. 모든 호출을 멈추면 비용과 지연이 커지므로, 조건을 명확히 정해야 한다.

### 연결
- [Graph engineering with Claude Code](graph-engineering-claude-codez.md) — 그래프 노드와 엣지의 설계 감각
- [Anthropic building effective agents](anthropic-building-effective-agents.md) — 사람 확인 지점을 두라는 원칙
- [Agent harness technical debt](agent-harness-technical-debt.md) — 승인과 관측이 빠진 하네스의 위험

## Hermes 관련성

외부 효과 전 human checkpoint와 graph state resume 패턴을 비교할 때 참고 가능. Hermes의 approval ingress/state gates와 동등하다고 간주하지 않습니다.
