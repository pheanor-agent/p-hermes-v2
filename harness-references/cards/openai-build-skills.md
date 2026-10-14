# OpenAI — Build skills

- Source: https://learn.chatgpt.com/docs/build-skills
- Alternate sources: none recorded
- Topics: skills-tools, case-implementation
- Publication date: unknown / not independently verified
- User-provided: unknown; date: unknown
- Knowledge registration: True; evidence: knowledge/references/external/openai-build-skills.md
- Source confirmation: 등록된 reference record와 문서 확인; 현재 사용자 제공 여부를 이 감사에서 확정하지 않음
- Utilization: OpenAI skills의 호출·배포 문서 요약. Hermes의 호출 형식과 동등하다고 보지 않으며 vendor-specific 자료임.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 지식 기록 대조 + 원문 일부 확인

## Independent summary and scope

OpenAI skills의 호출·배포 문서 요약. Hermes의 호출 형식과 동등하다고 보지 않으며 vendor-specific 자료임.

## 상세 정리

### 핵심 주장
1. 스킬은 쓰는 화면에 따라 호출 방식이 다르다. Codex CLI와 IDE 확장에서는 `$`로 스킬을 부르고, ChatGPT 작업 화면에서는 `@스킬이름` 형식을 쓴다. "설명대로 안 된다"는 문제의 상당수가 이 화면 차이에서 온다.
2. 단독 스킬과 플러그인에 묶인 스킬은 쓸 수 있는 장소가 다르다. 단독 스킬은 데스크톱 앱, Codex CLI, IDE 확장에서 쓴다. 플러그인으로 묶으면 웹·데스크톱·모바일의 대화와 작업 화면에서도 쓸 수 있다.
3. 재사용·배포는 플러그인으로 한다. 플러그인은 스킬 여러 개, MCP 서버 연결, 표시용 자산을 한 패키지로 묶는다.

### 구조와 패턴
- 로컬 설치: 제공되는 스킬은 `$skill-installer <스킬>`로 Codex에 설치한다.
- 비활성화: Codex 설정 파일의 `[[skills.config]]` 항목으로 개별 스킬을 끈다.
- 선택 메타데이터: 스킬 폴더의 `agents/openai.yaml`에 표시 이름, 아이콘, 모델이 스스로 호출해도 되는지(`allow_implicit_invocation`) 등을 적는다.

### 적용 방법
- 스킬 하나는 한 작업에 집중시킨다.
- 결정적 동작이나 외부 도구가 필요할 때만 스크립트를 넣고, 나머지는 지시문으로 쓴다.
- 단계는 입력과 출력이 분명한 명령형 문장으로 쓴다.
- 스킬 설명이 실제로 의도한 상황에서 발동되는지 시험한다.
- 문서를 안내할 때는 어느 화면 기준인지 함께 적는다.

### 근거와 한계
- OpenAI 공식 문서를 2026-08 수집 기록과 원문 일부로 정리했다. 화면 구성과 기호는 도구 버전에 따라 바뀔 수 있다.
- OpenAI 제품 전용 규약이다. 다른 에이전트의 스킬 형식과 같다고 가정하지 않는다.

### 연결
- [OpenAI skills concept](openai-skills-concept.md) — 스킬이 MCP 서버와 어떻게 역할을 나누는지
- [Vercel AGENTS.md vs skills](vercel-agents-md-skills-evals.md) — 스킬을 항상 로드하는 문맥과 비교한 평가
- [Hermes official docs](hermes-official-docs.md) — Hermes의 스킬 체계 개요

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
