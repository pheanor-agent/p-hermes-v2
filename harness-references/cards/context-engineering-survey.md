# A Survey of Context Engineering for Large Language Models

- 원문: https://arxiv.org/abs/2507.13334
- 출처 시점: arXiv 2025-07 submission; 현재 페이지는 v2 표시. 사용자가 링크 제공 2026-06-02 (KST).
- 주제: context/memory/knowledge · orchestration/workflow · evaluation
- 상태: 사용자 제공 링크; references 등록 여부 확인되지 않음. 문헌 survey 링크, 미도입.
- 권리: arXiv page license details were not checked; link and short original summary only.
- 정리 근거: 원문 일부 확인

## 자체 요약

대규모 언어모델에서 context retrieval/generation, context processing/management 및 RAG, memory, tool-integrated reasoning, multi-agent system 등 아키텍처 계층을 폭넓게 조사하는 ongoing survey다. 검색 결과에 1,300편 이상을 분석했다는 저자 설명이 있다.

## 상세 정리
### 핵심 주장
이 서베이는 LLM 성능이 추론 시점에 제공되는 맥락 정보에 크게 좌우된다는 전제에서 출발해, 맥락 엔지니어링을 단순한 프롬프트 작성보다 넓은 분야로 정의한다. 저자들은 맥락 엔지니어링을 기초 구성요소와 그것을 지능형 시스템으로 묶는 구현 방식으로 나누는 분류 체계를 제시한다. 원문 초록 기준으로 구성요소 쪽에는 맥락 검색과 생성(프롬프트 기반 생성과 외부 지식 획득), 맥락 처리(긴 시퀀스 처리, 자기 정제, 구조화된 정보 통합), 맥락 관리가 포함된다. 구현 쪽에는 검색 증강 생성, 메모리 시스템, 도구 통합 추론, 다중 에이전트 시스템 등이 다뤄진다.

### 구조와 패턴
핵심 구조는 '구성요소 → 구현'의 2층 분류다. 구성요소 층은 정보를 얻고(retrieval/generation), 가공하고(processing), 저장·갱신하는(management) 기능으로 나뉜다. 구현 층은 이 기능들이 결합되어 메모리, 도구 사용, 에이전트 협업으로 나타나는 방식을 설명한다. 이 분해는 하네스 설계자가 "문제가 어느 계층에서 생기는가"를 묻는 체크리스트로 쓰기 좋다. 예를 들어 에이전트가 오래된 사실을 따른다면 검색 계층의 문제인지, 관리(갱신·폐기) 계층의 문제인지 나눠 볼 수 있다.

### 적용 방법
Hermes 하네스를 검토할 때는 이 분류를 점검표로 쓸 수 있다. 시스템 프롬프트, 세션 요약, 장기 메모리, 도구 결과가 각각 어느 구성요소에 해당하는지 표로 정리하고, 빠진 계층(예: 맥락 처리의 압축·정제)을 찾는 방식이다. 다만 서베이는 문헌 지도이므로, 여기서 얻은 분류를 곧바로 설정 변경이나 구현 기준으로 삼으면 안 된다. 적용 전에는 각 주장이 어떤 실험에 근거하는지 개별 논문으로 내려가 확인해야 한다.

### 근거와 한계
원문 초록과 arXiv 메타데이터(버전 표시, 166쪽, 인용 수 표시)를 확인했다. 본문 전체, 분류표의 세부 항목, 인용된 개별 연구의 수치는 이번에 읽지 않았다. 따라서 이 digest는 분류 체계의 골격에 대한 설명이며, 개별 기법의 성능 주장은 검증된 내용이 아니다. 서베이는 저자들이 수집한 문헌의 선택에 따라 범위가 정해지므로, 누락된 흐름이 있을 가능성도 고려해야 한다. 논문은 계속 갱신되는 작업이므로 버전에 따라 내용이 달라질 수 있다.

### 연결
- [agentic-harness-evolution.md](agentic-harness-evolution.md) — 하네스가 시간에 따라 어떻게 변해 왔는지와 맥락 계층 설계를 함께 볼 수 있다.
- [memgpt-context-os.md](memgpt-context-os.md) — 맥락 관리 계층을 운영체제식 메모리 계층으로 구현한 사례다.
- [letta-context-repositories.md](letta-context-repositories.md) — 맥락 저장·갱신 구조를 구체 시스템 수준에서 비교하는 데 쓴다.

## Hermes 관련성

하네스의 컨텍스트·메모리 범위를 넓게 이해하고 후속 문헌을 탐색하는 입구로 유용하다. 페이지 길이·인용 수 등은 시간이 변하며, 이 라이브러리는 논문 전체의 체계적 품질 평가를 대체하지 않습니다.
