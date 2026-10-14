# How I built an AI marketing team with Claude Code (and Cowork)

- 원문: https://snow.runbear.io/how-i-built-an-ai-marketing-team-with-claude-code-and-cowork-f3405a53ee22
- 출처 시점: source date not confirmed; user link provided 2026-06-02 (KST). Related search result surfaced a Runbear experience article.
- 주제: orchestration/workflow · skills/tools · case/implementation
- 상태: user-provided; knowledge registration/utilization not verified. Practitioner case only.
- 권리: not checked; summary/link only.
- 정리 근거: 원문 일부 확인

## 자체 요약

A practitioner report describing an AI marketing team assembled around Claude Code and Cowork. It is an applied case, not a controlled evaluation; this card does not copy implementation content or claim a general workflow result.

## 상세 정리

### 핵심 주장
1. 마케팅 팀 운영을 AI에게 맡기는 방법을 "직원을 뽑듯 역할 설명서를 쓰라"는 관점으로 설명한다. 프롬프트보다 직무 기술서를 쓰는 것이 핵심이라는 주장이다.
2. 전체 구조는 대부분 마크다운 파일로 이루어진다. 회사 문서가 문맥을 제공하고, 각 에이전트는 파일 하나로 정의된다고 설명한다.
3. 처음에는 단일 세션에서 전략을 세우고, 필요한 것을 하나씩 요청하면서 시스템을 쌓아 갔다고 말한다.

### 구조와 패턴
- 에이전트 하나는 특정 폴더의 마크다운 파일로 정의된다. 최고 마케팅 책임자 역할의 에이전트가 하위 역할에 일을 나눈다.
- 실험 기능인 에이전트 팀 기능을 써서 한 에이전트가 다른 에이전트를 하위 프로세스처럼 띄운다.
- 초기 전략 산출물은 90일 콘텐츠 계획이었고, 블로그 주제와 배포 주기, 주간 목표로 구성됐다고 한다.

### 적용 방법
- 역할을 나누는 기준을 문서로 쓰면, 같은 지침을 여러 작업에서 재사용할 수 있다.
- 바로 실행하기보다 전략 산출물을 먼저 만들고, 그 계획을 기준으로 하위 작업을 나누는 순서가 유용하다.

### 근거와 한계
- 개인 실무 사례이며 성과 수치는 본문에서 확인되지 않았다. 마케팅 성과에 대한 주장은 검증되지 않았다.
- 원문 일부를 확인했다. 파일 예시와 주간 운영 흐름의 세부는 Part 1 글과 함께 확인해야 한다.
- 실험 기능에 기대는 설계이므로 안정성은 보장되지 않는다.

### 연결
- [Multi-agent orchestration patterns](multi-agent-orchestration-patterns.md) — 역할을 나눈 감독과 워커 구조
- [Anthropic multi-agent research system](anthropic-multi-agent-research-system.md) — 하위 에이전트 조율의 다른 사례
- [Hermes official docs](hermes-official-docs.md) — 역할별 메모리와 스킬 구분

## Hermes 관련성

Role/skill decomposition and multi-agent team organization may be useful comparison themes. Domain-specific workflow and author-reported outcomes need independent confirmation before reuse.
