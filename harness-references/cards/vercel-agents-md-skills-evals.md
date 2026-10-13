# AGENTS.md outperforms skills in our agent evals

- 원문: https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals
- 출처 시점: 원문 게시일 여기서는 확인하지 못함; 사용자 링크 제공 확인 2026-06-02 (KST).
- 주제: skills/tools · evaluation/observability
- 상태: 사용자 제공; 지식 references 등록 여부 확인되지 않음. 사례 비교, 채택 근거 아님.
- 권리: 미확인. 자체 요약·링크만; 원문·데이터 미복사.

## 자체 요약

Vercel이 특정 Next.js 작업 묶음과 agent configuration들에서 AGENTS.md, Skills, baseline을 비교한 평가 사례다. 검색 스니펫에는 baseline 53%, default skill 53%, 명시 지시가 있는 skill 79%, AGENTS.md index 100%로 소개된다. 이 비율은 해당 task set/configuration의 자체 평가 결과다.

## Hermes 관련성

always-on repo instructions와 필요 시 로드하는 skill을 나누고, 실행 지침의 discoverability를 테스트할 때 참고할 수 있다. 작은 vendor-specific task set을 전체 agent의 비교 우위나 일반화된 성능 보증으로 확대하지 않습니다.
