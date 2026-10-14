# OpenAI — Skills concept

- Source: https://developers.openai.com/plugins/concepts/skills.md
- Alternate sources: none recorded
- Topics: skills-tools, context-memory-knowledge
- Publication date: unknown / not independently verified
- User-provided: unknown; date: unknown
- Knowledge registration: True; evidence: knowledge/references/external/openai-plugin-skills-concept.md
- Source confirmation: 등록된 reference record와 문서 확인; 사용자 제공 여부는 미확정
- Utilization: 재사용 가능한 instruction/reference/script 단위 및 MCP와의 경계를 설명하는 벤더 개념 자료. Hermes 운영정책으로 채택하지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 지식 기록 대조 + 원문 일부 확인

## Independent summary and scope

재사용 가능한 instruction/reference/script 단위 및 MCP와의 경계를 설명하는 벤더 개념 자료. Hermes 운영정책으로 채택하지 않음.

## 상세 정리

### 핵심 주장
1. 스킬은 지시문·참고 자료·스크립트를 묶은 재사용 가능한 작업 단위다. frontmatter와 본문으로 된 `SKILL.md` 하나가 중심이 된다.
2. 스킬과 MCP 서버는 서로 보완한다. 스킬은 "어떻게 일하는가"를, MCP 서버는 "어떤 도구에 접근하는가"를 담당한다.
3. 이미지 생성 화면의 템플릿 갤러리는 별도 템플릿 시스템이 아니라 스킬로 저장되고 호출된다. 사용자 정의 템플릿을 만드는 것은 사실상 자기 스킬 하나를 만드는 일이다.

### 구조와 패턴
- 스킬 폴더 = `SKILL.md`(이름·설명 frontmatter + 절차 본문) + 필요한 참고 파일·스크립트.
- 배포 단위는 플러그인이다. 스킬 여러 개, MCP 서버 연결, 표시용 자산을 하나로 묶는다.
- 로컬에서 쓸 때는 스킬 폴더를 직접 만들고, 다른 사람에게 배포할 때는 플러그인을 권장한다.

### 적용 방법
- 반복하는 작업 방식은 스킬로, 외부 시스템 접근은 MCP 서버로 나눠 설계한다. 한 파일에 섞지 않는다.
- "템플릿"이나 "프리셋" 기능을 따로 만들기 전에, 스킬로 저장·호출하는 구조로 충분한지 먼저 본다.
- 스킬 설명(frontmatter)은 발동 조건을 정하는 부분이므로 본문보다 신중하게 쓴다.

### 근거와 한계
- OpenAI 공식 개념 문서를 2026-08 수집 기록과 원문 일부로 정리했다. 문서는 도구 버전에 따라 바뀔 수 있다.
- 템플릿=스킬 구조는 X 게시물의 관찰을 공식 문서로 확인한 기록에 근거한다. OpenAI 제품 기준의 설명이다.

### 연결
- [OpenAI build skills](openai-build-skills.md) — 스킬을 두는 위치와 배포 방식
- [Vercel AGENTS.md vs skills](vercel-agents-md-skills-evals.md) — 스킬이 실제로 발동되지 않은 평가 사례
- [Hermes official docs](hermes-official-docs.md) — Hermes의 스킬과 메모리 구분

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
