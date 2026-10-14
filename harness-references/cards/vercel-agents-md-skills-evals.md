# AGENTS.md outperforms skills in our agent evals

- 원문: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- 출처 시점: 원문 게시일 여기서는 확인하지 못함; 사용자 링크 제공 확인 2026-06-02 (KST).
- 주제: skills/tools · evaluation/observability
- 상태: 사용자 제공; 지식 references 등록 여부 확인되지 않음. 사례 비교, 채택 근거 아님.
- 권리: 미확인. 자체 요약·링크만; 원문·데이터 미복사.
- 정리 근거: 원문 전체 확인

## 자체 요약

Vercel이 특정 Next.js 작업 묶음과 agent configuration들에서 AGENTS.md, Skills, baseline을 비교한 평가 사례다. 검색 스니펫에는 baseline 53%, default skill 53%, 명시 지시가 있는 skill 79%, AGENTS.md index 100%로 소개된다. 이 비율은 해당 task set/configuration의 자체 평가 결과다.

## 상세 정리

### 핵심 주장
1. Next.js 16처럼 모델 학습 데이터에 없는 프레임워크 지식을 주는 방법으로, 스킬 묶음과 AGENTS.md 문서 색인을 비교한 평가 사례다.
2. 스킬을 기본 상태로만 둔 경우 평가 케이스의 56%에서 호출되지 않았고, 통과율은 기준선과 같은 53%였다.
3. 스킬 호출을 명시하면 발동률은 95% 이상, 통과율은 79%로 올랐다. 하지만 지시 문구에 따라 결과가 크게 달랐다.
4. 압축한 약 8KB 문서 색인을 AGENTS.md에 상시 넣었을 때 통과율은 100%였다. 문서를 먼저 참조하라는 한 줄 지시를 함께 넣었다.

### 구조와 패턴
- 스킬은 필요할 때만 불러와 문맥 부담이 적지만, 에이전트가 호출하지 않으면 효과가 없다.
- AGENTS.md는 매 턴 자동으로 읽히므로 호출 여부를 모델이 결정할 필요가 없다.
- "반드시 스킬을 호출하라"는 지시는 프로젝트 문맥을 놓치게 했고, "먼저 프로젝트를 살피고 나서 스킬을 쓰라"는 지시가 더 나은 결과를 냈다.
- 평가 세트는 테스트 누수를 없애고 구현 세부 대신 관찰 가능한 동작으로 판정하도록 고쳐졌다.

### 적용 방법
- 항상 필요한 사실은 상시 지침 파일에 짧은 색인으로 두고, 세부 문서는 경로로 연결해 필요할 때 읽게 한다.
- 스킬 구조를 정하기 전에 실제 평가 세트로 발동률과 통과율을 먼저 측정하고, 지시 문구도 평가 대상으로 둔다.
- Next.js 프로젝트라면 `npx @next/codemod@canary agents-md`가 버전에 맞는 문서를 내려받아 색인을 AGENTS.md에 넣는다고 소개된다.

### 근거와 한계
- 한 회사가 Next.js 16 API로 만든 자체 평가 결과다. 다른 프레임워크와 모델에서 같은 차이가 나는지는 원문에서 확인되지 않는다.
- 100% 통과는 작성자가 만든 평가 세트 기준이며, 그 세트는 모호한 항목을 고치고 Next.js 16 API 테스트를 더한 뒤 쓰였다.
- 같은 스킬이라도 지시 문구 하나로 결과가 달라졌으므로 결과는 민감하다.

### 연결
- [openai-build-skills.md](openai-build-skills.md) — 스킬의 위치와 설계 원칙을 비교하는 자료
- [openai-harness-engineering.md](openai-harness-engineering.md) — 저장소 안 지침 파일을 기록의 원천으로 둔 사례
- [anthropic-building-effective-agents.md](anthropic-building-effective-agents.md) — 도구 설명과 평가를 중시하는 원칙

## Hermes 관련성

always-on repo instructions와 필요 시 로드하는 skill을 나누고, 실행 지침의 discoverability를 테스트할 때 참고할 수 있다. 작은 vendor-specific task set을 전체 agent의 비교 우위나 일반화된 성능 보증으로 확대하지 않습니다.
