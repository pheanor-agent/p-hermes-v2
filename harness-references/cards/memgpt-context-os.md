# MemGPT — Context OS

- Source: https://memgpt.readme.io/docs/memgpt-memories
- Alternate sources: https://arxiv.org/abs/2310.08560
- Topics: context-memory-knowledge, case-implementation
- Publication date: unknown / not independently verified
- User-provided: unknown; date: unknown
- Knowledge registration: True; evidence: knowledge/references/memory/memgpt-context-os.md
- Source confirmation: 등록된 지식 문서 요약 확인; 사용자 제공 여부는 감사 증거로 확정되지 않아 unknown
- Utilization: 컨텍스트를 계층형 메모리/페이지 교체로 관리하는 연구·구현 개념. Hermes memory authority나 운영 채택으로 취급하지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 원문 일부 확인

## Independent summary and scope

컨텍스트를 계층형 메모리/페이지 교체로 관리하는 연구·구현 개념. Hermes memory authority나 운영 채택으로 취급하지 않음.

## 상세 정리
### 핵심 주장
1. LLM은 문맥 창이 제한되어 긴 대화나 긴 문서를 다루기 어렵다. 이 논문은 이 한계를 가상 메모리로 넘자고 제안한다.
2. 운영체제가 실제 메모리와 디스크 사이에서 페이지를 주고받아 큰 가상 메모리를 보여 주듯이, 문맥 창과 외부 저장소 사이에서 정보를 옮긴다는 발상이다. 이를 "가상 문맥 관리"라고 부른다.
3. 이 설계를 구현한 시스템이 MemGPT다. 여러 저장소 계층을 관리해 문맥 창 밖의 정보를 필요할 때 가져온다.

### 구조와 패턴
- 두 영역에서 평가한다. 하나는 문맥 창을 훨씬 넘는 긴 문서 분석이고, 다른 하나는 여러 세션에 걸친 대화다.
- 다중 세션 대화에서는 에이전트가 사용자를 기억하고, 되돌아보고, 시간이 지나며 변하는 대화형 에이전트가 된다고 설명한다.
- 계층은 주 문맥(지금 보는 내용)과 외부 저장(필요할 때 검색하는 내용)으로 나뉘며, 이동은 에이전트가 결정한다.

### 적용 방법
- Hermes의 메모리와 세션 기록은 이 구조와 같은 계층으로 볼 수 있다. 자주 쓰는 사실은 주 문맥에, 긴 기록은 저장소에 두고 필요할 때 찾는 식이다.
- 어떤 정보를 주 문맥에 올릴지 정하는 규칙을 명시해야 문맥 낭비와 누락을 함께 줄일 수 있다.

### 근거와 한계
- 이 정리는 초록 수준만 확인했다. 실험 표, 비교 기준선, 세부 정책은 본문에서 확인해야 한다.
- 2023년 공개 연구이므로, 긴 문맥을 지원하는 모델이 나온 뒤 이 설계의 상대적 필요성은 달라졌을 수 있다. 이는 정리자의 판단이며 확인된 사실은 아니다.
- 저장소 계층의 실제 검색 정확도는 초록에서 확인할 수 없다.

### 연결
- [Letta context repositories](letta-context-repositories.md) — 같은 문제를 git과 파일로 푸는 후속 설계
- [Google context-aware multi-agent](google-context-aware-multi-agent.md) — 문맥을 원천과 뷰로 나누는 현대적 접근
- [JAZ harness as a language](jaz-harness-language.md) — 장기 기억을 루프 밖에 두지 않는 대안

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
