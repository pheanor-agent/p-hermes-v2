# Harness as a Language: A Minimalist Agent Framework With Maximal Expressivity

- 원문: https://arxiv.org/abs/2609.26891 ; HTML: https://arxiv.org/html/2609.26891
- 출처 시점: arXiv v1 등록·JOB 분석 2026-09-27; 현재 arXiv 페이지는 v2 표기.
- 주제: 개요 · orchestration/workflow · context/memory · evaluation/security
- 상태: prior analysis와 `knowledge/references/github/jaz-harness-as-a-language.md` 등록 확인; 결론 C(참고만), Hermes runtime 도입·벤치마크 없음.
- 권리: arXiv 페이지 CC BY 4.0 표시; 원문/코드 미복사.
- 정리 근거: 원문 일부 확인

## 자체 요약

JAZ는 `invoke`를 중심으로 모델이 실행 가능한 코드를 생성하고, 호출 이력·입력·도구를 코드에서 참조하며 재귀 sub-invoke와 hook을 사용하는 미니멀 agent framework를 제안한다. 논문은 StuLife와 AppWorld의 특정 평가에서 성능·비용 결과를 보고한다. 생성 코드 실행, 예산, 검증과 관측의 경계가 핵심이다.

## 상세 정리
### 핵심 주장
1. 현대 에이전트는 "도구 호출과 관찰을 번갈아 하는 루프"를 기본으로 한다. 그런데 장기 기억과 자기 개선은 보통 루프 밖의 별도 시스템으로 붙인다.
2. JAZ는 이 가설을 시험하는 최소 하네스다. 루프 자체 외에는 거의 아무것도 없는 구조로, 장기 기억이나 자기 개선이 가능한지 본다.
3. 단일 원시 연산 invoke만 노출한다. LLM은 임의의 실행 코드를 쓸 수 있고(재귀적 invoke 포함), LLM이 보는 모든 입력과 상호작용 이력은 코드 환경의 변수가 된다.
4. 프로그래머는 제약과 관찰을 위한 훅만 붙인다.

### 구조와 패턴
- invoke를 "구현을 LLM이 매 호출마다 제공하는 함수"로 보는 언어적 관점에서 출발한다.
- 기존 코드 모드(code-mode) 에이전트 루프를 일반화한 형태라고 설명된다.
- 평가는 수동 도구나 외부 메모리·파일 시스템 없이 프롬프트만으로 워크플로를 수행하는지를 본다.

### 적용 방법
- Hermes의 무거운 보조 시스템이 정말 필요한지 따져 볼 때 참고할 수 있다. 같은 과제에서 최소 하네스와 비교하는 실험을 설계하면 된다.
- 훅으로 제약을 거는 방식은 승인 게이트를 설계하는 데 개념적으로 연결된다.

### 근거와 한계
- 초록 위주로 확인했다. 실험 과제 목록과 수치는 이 정리에서 확인하지 못했다.
- 아직 사전 인쇄 성격의 연구이며, 프로덕션 검증 근거는 없다.
- "최소 하네스"의 장점이 실제 업무 신뢰성에서도 나타나는지는 별도 측정이 필요하다.

- 저자들은 최소 하네스의 조건을 두 가지로 든다. 코드를 쓸 수 있다는 것, 그리고 LLM이 보는 모든 것이 코드 환경의 변수라는 것이다. 이 두 조건이 있으면 별도 도구 없이도 많은 작업이 가능하다고 주장한다.
- 훅은 감시와 제약의 지점이다. 승인 게이트와 감사 기록을 훅 위치에 두는 설계가 가능하다는 점은 개념적 연결이다.

### 연결
- [Meta-harness](meta-harness.md) — 하네스 탐색을 자동화하는 다른 연구
- [Raven composable agentic intelligence](raven-composable-agentic-intelligence.md) — 하네스를 조합하는 방향
- [MemGPT context OS](memgpt-context-os.md) — 장기 기억을 별도 계층으로 두는 기존 접근

## Hermes 관련성

코드 기반 workflow의 표현력과 memory/재귀 loop의 실험 사례를 볼 수 있다. 기존 검토에서는 Hermes에서 해결할 측정된 pain point를 찾지 못해 참고 자료로만 분류했으며, 논문 결과는 자체 성능 주장으로 남겨야 합니다. arXiv에서 갱신된 버전과 이전 분석 대상 v1을 혼동하지 마세요.
