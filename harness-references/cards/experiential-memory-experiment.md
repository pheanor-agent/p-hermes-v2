# Experiential vs Synthetic Memory in Long-Running AI Agents

- 사용자가 제공한 소개 링크: https://blog.clawsouls.ai/ko/posts/experiential-memory-experiment/
- 보조 실험 repo: https://github.com/clawsouls/experiential-memory-dataset
- 출처 시점: 원문 date not confirmed; user URL provided 2026-06-02 (KST); experiment repo description inspected via search 2026-10-14.
- 주제: context/memory/knowledge · evaluation/observability
- 상태: user-provided; knowledge reference registration not verified. Controlled-memory comparison is a research lead, not Hermes adoption.
- 권리: article license not verified; no prompts/dataset copied.
- 정리 근거: 원문 일부 확인

## 자체 요약

The linked material concerns comparison of experiential versus synthetic memory for long-running agents. The linked dataset repository describes isolated sessions, memory retrieval and a blinded single human evaluator; these are source claims and deserve separate methodological review.

## 상세 정리

### 핵심 주장
이 실험은 장기 실행 AI 에이전트에게 메모리를 어떤 형태로 주는지에 따라 성능이 어떻게 달라지는지를 본다. 저자들이 제시한 핵심 발견은 세 가지다. 첫째, 정리된 합성(synthetic) 메모리만 준 조건이 메모리 없는 베이스라인보다 낮은 점수를 받았다. 둘째, 실제 협업에서 생긴 경험적(experiential) 메모리와 합성 메모리를 함께 준 하이브리드 조건이 가장 높았다. 셋째, 맥락 의존 판단 질문에서는 경험적 메모리가 가장 강했다. 저자들은 이 현상을 '과잉확신 효과'라고 부르며, 요약이 에이전트에게 불완전한 내용을 확신 있게 말하게 만든다고 해석한다.

### 구조와 패턴
실험 설계는 에이전트 하나, 과제 20개, 프로젝트 하나로 구성되며 메모리 조건은 A(경험적), B(합성), C(하이브리드), D(없음) 네 가지다. 평가는 IR, CT, AD, CD 네 범주에 대해 1~5점 척도로 이뤄졌다. 공개 데이터셋 저장소는 과제, 채점 기준, 조건별 응답, 점수 CSV, 블라인드 평가 절차를 포함한다. 또한 각 조건을 격리된 세션에서 실행하고 메모리 폴더만 바꾸는 방식을 택했다. 메모리 검색은 의미 기반 검색(RAG)을 썼다고 명시되어 있다. 구조적으로 보면 '원시 로그 + 구조화 요약'을 함께 두는 설계가 핵심 패턴이다.

### 적용 방법
Hermes의 메모리 설계를 검토할 때는 메모리 내용보다 메모리 평가 방법을 먼저 가져오는 것이 적절하다. 같은 과제 집합을 메모리 조건별로 격리 실행하고, 점수를 블라인드로 매기는 절차는 재현 가능한 비교 틀이 된다. 요약 메모리를 도입하기 전에 '메모리 없음' 베이스라인과 비교하는 단계를 넣는 것도 이 실험에서 얻을 수 있는 교훈이다. 실제 데이터를 복제하지 않고 방법론만 참고하는 방식이 맞다.

### 근거와 한계
블로그 본문과 데이터셋 저장소 소개를 읽었다. 저자들 스스로 밝히듯 이 결과는 단일 에이전트, 단일 프로젝트(TypeScript/Next.js), 질문 20개의 파일럿이다. 평가자는 단일 인간이며 프로젝트 리드가 수행해 블라인드가 완전하지 않았다. 점수는 검증된 심리측정 도구가 아니다. 또 실험에 쓴 모델은 Claude 계열이고, 메모리 파일과 평가 프롬프트가 한국어 중심이라 다른 언어와 모델에서 같은 순위가 나온다는 보장이 없다. 관련 Zenodo 논문과 후속 버전은 이번에 열지 않았다. 따라서 이 결과는 가설 생성의 근거로만 쓸 수 있다.

### 연결
- [supermemory.md](supermemory.md) — 메모리 저장과 검색을 제품 수준에서 다룬 사례와 비교할 수 있다.
- [letta-context-repositories.md](letta-context-repositories.md) — 맥락 저장소를 구조화하는 방식과 요약 메모리 문제를 함께 볼 수 있다.
- [anthropic-effective-long-running-agents.md](anthropic-effective-long-running-agents.md) — 장기 실행 에이전트에서 상태를 이어 가는 방법과 맞물린다.

## Hermes 관련성

Memory representation and evaluation methodology may inform later controlled comparison. Search snippet and dataset README are not sufficient to conclude memory quality or generalize results to Hermes; no user memory or corpus is reproduced here.
