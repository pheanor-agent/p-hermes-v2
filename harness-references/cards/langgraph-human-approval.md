# Add human-in-the-loop review to LangGraph tool calls

- 원문: https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop
- 출처 시점: documentation URL; 사용자 링크 제공 확인 2026-10-02 (KST); current content not rechecked.
- 주제: orchestration/workflow · evaluation/observability/security
- 상태: 사용자 제공; internal knowledge registration not verified. Implementation-document reference only.
- 권리: terms not checked; link and summary only.

## 자체 요약

LangGraph documentation page for adding human-in-the-loop review to tool calls. The reference concerns a framework-specific implementation pattern; this library does not assert its current API compatibility or safe deployment.

## Hermes 관련성

외부 효과 전 human checkpoint와 graph state resume 패턴을 비교할 때 참고 가능. Hermes의 approval ingress/state gates와 동등하다고 간주하지 않습니다.
