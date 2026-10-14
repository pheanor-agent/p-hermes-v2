# Building effective agents

- 원문: https://www.anthropic.com/engineering/building-effective-agents
- 출처 시점: 2024-12-19 게시(Erik S., Barry Zhang, Anthropic). 이후 예시 모델명·SDK 이름이 갱신됨. 정리 기준 원문 확인 2026-10-14.
- 주제: 개요 · orchestration/workflow · skills/tools
- 상태: 사용자 제공 링크 확인(2026-06-02 KST, 내부 출처 증거); 지식 references 등록은 확인되지 않음. 배경 참고.
- 권리: 미확인. 자체 요약·정리와 링크만; 전문 미보존.
- 정리 근거: 원문 전체 확인

## 자체 요약

필요 이상으로 복잡한 agent framework부터 도입하지 말고, 단순한 prompt/workflow로 시작해 평가를 통해 부족함이 확인된 경우에만 routing, parallelization, evaluator-optimizer 등 복잡성을 추가하라는 원칙을 제시한다. 도구 인터페이스와 문서화의 품질도 중요하게 다룬다.

## 상세 정리

### 핵심 주장
1. 성공한 사례들은 복잡한 framework가 아니라 단순하고 조합 가능한 패턴으로 만들어졌다.
2. **workflow**(정해진 코드 경로로 LLM과 도구를 엮음)와 **agent**(모델이 스스로 절차와 도구 사용을 정함)를 구분한다. 둘을 합쳐 agentic system이라 부른다.
3. agentic system은 지연과 비용을 내고 성능을 산다. 단일 LLM 호출에 retrieval과 예시를 붙이는 것으로 충분한 경우가 많으니, 그 이상은 필요가 측정으로 확인될 때만 더한다.
4. framework는 시작을 빠르게 해주지만 prompt와 응답을 가리는 추상층이 디버깅을 어렵게 하고 불필요한 복잡성을 부른다. 먼저 API를 직접 쓰고, framework를 쓰더라도 내부 동작을 이해해야 한다.
5. 성공 원칙은 세 가지다. 설계를 단순하게, 계획 단계를 드러내 투명하게, 도구 인터페이스(ACI)를 문서화하고 시험해 정교하게.

### 구조와 패턴
- **기본 블록 — augmented LLM**: 모델에 검색·도구·메모리를 붙인 것. 용도에 맞게 붙이고, 모델이 쓰기 쉬운 잘 문서화된 인터페이스로 제공한다(예: MCP).
- **prompt chaining**: 단계를 순서대로 잇고 중간에 코드 검사(gate)를 둔다. 작업을 고정된 하위 단계로 나눌 수 있을 때. 예: 개요 작성 → 기준 검사 → 본문 작성.
- **routing**: 입력을 분류해 전문화된 경로로 보낸다. 범주가 뚜렷하고 분류가 정확할 때. 예: 문의 유형별 처리, 쉬운 질문은 작은 모델로.
- **parallelization**: 독립 하위 작업을 동시에(sectioning) 하거나 같은 작업을 여러 번 돌려 표를 모은다(voting). 예: 응답 생성과 guardrail 검사를 분리, 취약점 검토를 여러 프롬프트로.
- **orchestrator-workers**: 중앙 LLM이 하위 작업을 그때그때 정해 워커에 맡기고 결과를 합친다. parallelization과 달리 하위 작업이 미리 정해지지 않는다. 예: 여러 파일을 고치는 코딩, 여러 출처 조사.
- **evaluator-optimizer**: 생성 LLM과 평가 LLM이 반복한다. 평가 기준이 분명하고 피드백으로 실제 개선될 때.
- **autonomous agent**: 사용자와 과업을 정한 뒤 도구 결과 같은 환경의 실제 신호를 보며 스스로 반복한다. 체크포인트·막힐 때 사람에게 돌아오고, 최대 반복 수 같은 종료 조건을 둔다.

### 적용 방법
- 단일 호출 + 검색·예시로 해결되는지 먼저 측정했는가?
- 단계가 고정이면 workflow, 단계 수를 미리 알 수 없을 때만 agent를 쓴다.
- agent에는 sandbox 시험, guardrail, 종료 조건, 사람 확인 지점을 둔다(비용 증가와 오류 누적 위험).
- 도구 설계: 모델이 쓰기 전에 생각할 여유를 주고, 인터넷에 흔한 형식을 쓰며, 줄 수 세기·문자열 escape 같은 부담을 없앤다.
- 도구 설명은 신입 개발자용 docstring처럼: 사용 예, 경계 사례, 입력 형식, 비슷한 도구와의 구분을 적는다. 여러 입력으로 시험해 반복되는 실수를 고친다.
- poka-yoke: 실수하기 어렵게 인자를 바꾼다. 원문 사례로, 작업 디렉터리를 옮긴 뒤 상대 경로 오류가 나자 절대 경로만 받게 해 문제를 없앴다. SWE-bench 작업에서 전체 프롬프트보다 도구 최적화에 더 많은 시간을 썼다고 한다.

### 근거와 한계
- 고객 지원과 코딩 agent를 잘 맞는 분야로 든다. 코딩은 테스트로 결과를 검증할 수 있어서다. 다만 테스트 통과가 시스템 요구 전체를 보장하지 않으므로 사람 검토가 여전히 중요하다고 적는다.
- 고객 사례 경험에 기반한 실무 지침이며, 패턴별 정량 비교는 없다.
- 예시 모델명·SDK 이름은 원문이 갱신되며 바뀌었다. 패턴 설명이 정리의 중심이다.

### 연결
- [Claude workflow patterns](claude-workflow-patterns.md) — 같은 패턴의 선택 기준을 더 자세히
- [Multi-agent research system](anthropic-multi-agent-research-system.md) — orchestrator-workers의 실제 적용
- [Effective harnesses for long-running agents](anthropic-effective-long-running-agents.md) — 여러 context window에 걸친 agent
- [Agent harness technical debt](agent-harness-technical-debt.md) — 과잉 설계 위험이라는 같은 문제의식

## Hermes 관련성

하네스의 복잡도를 실제 문제·측정·검증에 맞춰 늘리는 기본 비교 기준이다. 가이드의 패턴은 결과를 보장하지 않으며, 실제 적용 판단에는 작업별 평가가 필요합니다.
