# Agentic Engineering Patterns

- 원문: https://simonwillison.net/guides/agentic-engineering-patterns/
- 출처 시점: 안내서가 갱신형으로 운영됨; 고정 게시일 없음. 사용자 링크 제공 확인 2026-06-02 (KST).
- 주제: 개요 · orchestration/workflow · evaluation/observability · skills/tools
- 상태: 사용자 제공 링크; 지식 references 등록 여부 확인되지 않음. 지속 갱신 안내서, 운영 채택 아님.
- 권리: 미확인. 요약·링크만; 원문 미보존.
- 정리 근거: 지식 기록 기준(원문 미열람)

## 자체 요약

코딩 agent와 함께 일하는 실무 패턴을 모은 갱신형 guide다. git 사용, 테스트 우선, subagent, 선형 코드베이스 walkthrough, 수동 테스트와 결과 검증 같은 주제를 다룬다. 패턴 카탈로그이므로 각 항목의 범위와 게시 시점은 개별 글에서 확인해야 한다.

## 상세 정리

### 핵심 주장
1. 코딩 에이전트(Claude Code, OpenAI Codex 등)에서 좋은 결과를 얻는 방법을 패턴 모음으로 정리한 연재 가이드다.
2. 가이드는 원칙, 기본 작업 방식, 구체 사례로 구성된다. 목차에는 "에이전트 공학이란 무엇인가"가 맨 앞에 있다.
3. 목차에는 검토되지 않은 코드를 동료에게 넘기는 문제가 별도 항목으로 있어, 검토 책임을 강조하는 것으로 보인다.

### 구조와 패턴
- 원칙 장과 실전 장이 나뉜다. 실전 장에는 작은 도구를 만드는 사례가 포함된다.
- 각 패턴은 짧은 글 단위로 독립되어 있어 필요한 항목만 골라 읽을 수 있다.

### 적용 방법
- Hermes 작업에서 에이전트 결과를 받을 때, "검토되지 않은 결과를 넘기지 않는다"는 항목을 체크리스트로 쓸 수 있다.
- 작은 도구 단위로 나눠 맡기는 사례는 JOB을 작게 쪼개는 원칙과 연결된다.

### 근거와 한계
- 이 정리는 가이드 첫머리와 목차만 확인했다. 개별 패턴 본문은 열람하지 않았으므로 내용 주장은 하지 않는다.
- 연재가 진행 중이므로 항목이 바뀔 수 있다.
- 스폰서 문구는 내용과 무관하다.

### 연결
- [OpenAI harness engineering](openai-harness-engineering.md) — 에이전트가 쓴 코드를 운영하는 사례
- [Vercel AGENTS.md vs skills](vercel-agents-md-skills-evals.md) — 지침 파일의 효과에 대한 평가
- [Anthropic building effective agents](anthropic-building-effective-agents.md) — 단순한 패턴부터 시작하라는 원칙

## Hermes 관련성

agent 실행을 실제 개발 도구·테스트·검토 루프에 연결하는 대중적 실무 reference다. 공식 제품 사양이나 통제된 benchmark는 아니며, 관찰된 경험과 저자의 권고로 해석합니다.
