# 과거 등록 참고 자료 재고표

과거 색인에서 확인한 39개 자료를 여섯 주제로 탐색합니다. 원출처·참조 파일을 찾지 못한 상태도 표시하며, 제목과 기존 기록을 바탕으로 분류한 자료는 원문을 새로 검증한 것으로 해석하지 않습니다.

- [전체 JSON](inventory.json) · [전체 CSV](inventory.csv) · [메인 목차](../CATALOG.md)
- 여러 주제에 속한 자료는 각 주제에서 반복 표시됩니다. 고유 항목 수는 39개입니다.
- `main_card`는 라이브러리 루트를 기준으로 한 경로입니다. `classification_evidence`와 `summary_evidence`는 분류·요약의 근거를 나타냅니다.

## 개요

- **Harness engineering: leveraging Codex in an agent-first world** — [상세 카드](../cards/openai-harness-engineering.md) · [원문](https://openai.com/ko-KR/index/harness-engineering)
  - OpenAI의 agent-first 제품 개발 경험담은 짧은 AGENTS.md를 백과사전보다 지도로 쓰고, 근거가 되는 저장소 문서를 기록 시스템으로 두며, 구조·제약·평가·관측을 도구와 자동 검사에 녹이는 방식을 설명한다. 격리 worktree와 로그·지표 등 에이전트가 관찰·검증 가능한 작업 환경도 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Software After AI (Harnessing AI) — Tomasz Tunguz** — [상세 카드](../cards/harnessing-ai-tunguz.md) · [원문](https://tomtunguz.com/harnessing-ai)
  - Tomasz Tunguz는 LLM을 신뢰 가능한 에이전트로 만드는 런타임·제약·신뢰성 층을 하네스로 설명하고, 문맥·도구·오케스트레이션·상태·샌드박스·관측·비용의 일곱 구성요소를 제시한다. 이는 저자의 개념 프레임이며 운영 채택 증거는 아니다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-01)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **하네스 엔지니어링: AI 에이전트 시대, 경쟁력은 모델이 아니라 마구에서 나온다** — [원문](https://wikidocs.net/blog/@jaehong/9481)
  - 에이전트 신뢰성을 모델 자체보다 도구·상태·컨텍스트·검증을 포함한 하네스 설계와 연결하는 개요 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **EP 86: 진짜 내 일을 위한 Agentic Workflow** — [원문](https://aifrontier.kr/ko/episodes/ep86)
  - 팟캐스트 인터뷰에서 실제 소프트웨어 개발 사례를 통해 에이전트 워크플로의 적용과 한계를 다룬다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **우리, 프로그래머들 — .md로 코딩하는 시대** — [원문](https://velog.io/@teo/we-programmer)
  - AI 시대 개발자의 역할과 에이전트 코드 생성·제어를 다룬 한국어 글을 요약한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

## 작업 흐름·위임

- **A Survey of Context Engineering for Large Language Models** — [상세 카드](../cards/context-engineering-survey.md) · [원문](https://arxiv.org/abs/2507.13334)
  - 대규모 언어모델에서 context retrieval/generation, context processing/management 및 RAG, memory, tool-integrated reasoning, multi-agent system 등 아키텍처 계층을 폭넓게 조사하는 ongoing survey다. 검색 결과에 1,300편 이상을 분석했다는 저자 설명이 있다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Architecting efficient context-aware multi-agent framework for production** — [상세 카드](../cards/google-context-aware-multi-agent.md) · [원문](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production)
  - Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working context를 구분하는 구조를 설명한다. 검색 결과는 context processing과 효율적 multi-agent 운영을 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Common workflow patterns for AI agents—and when to use them** — [상세 카드](../cards/claude-workflow-patterns.md) · [원문](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)
  - 고정 순서의 sequential, 독립 작업의 parallel, 평가 후 반복 개선하는 evaluator-optimizer 패턴을 비교한다. 먼저 단일 agent로 시도하고, 실제 latency 병목·독립성·측정된 품질 향상이 확인될 때에만 더 복잡한 패턴을 선택하라고 권한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **How I built an AI marketing team with Claude Code (and Cowork)** — [상세 카드](../cards/runbear-ai-marketing-team.md) · [원문](https://snow.runbear.io/how-i-built-an-ai-marketing-team-with-claude-code-and-cowork-f3405a53ee22)
  - A practitioner report describing an AI marketing team assembled around Claude Code and Cowork. It is an applied case, not a controlled evaluation; this card does not copy implementation content or claim a general workflow result.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Software After AI (Harnessing AI) — Tomasz Tunguz** — [상세 카드](../cards/harnessing-ai-tunguz.md) · [원문](https://tomtunguz.com/harnessing-ai)
  - Tomasz Tunguz는 LLM을 신뢰 가능한 에이전트로 만드는 런타임·제약·신뢰성 층을 하네스로 설명하고, 문맥·도구·오케스트레이션·상태·샌드박스·관측·비용의 일곱 구성요소를 제시한다. 이는 저자의 개념 프레임이며 운영 채택 증거는 아니다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-01)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **하네스 엔지니어링: AI 에이전트 시대, 경쟁력은 모델이 아니라 마구에서 나온다** — [원문](https://wikidocs.net/blog/@jaehong/9481)
  - 에이전트 신뢰성을 모델 자체보다 도구·상태·컨텍스트·검증을 포함한 하네스 설계와 연결하는 개요 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Good Spec: 좋은 명세 작성 가이드** — [원문](https://addyosmani.com/blog/good-spec)
  - 구현 전에 요구사항과 명세를 명확히 해 에이전트가 작업할 계약을 제공하는 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **AutoResearch - 자율적 연구 시스템** — [원문](https://github.com/karpathy/autoresearch)
  - 연구자가 프로그램 지침과 제한된 실험 루프를 통해 모델 학습 실험을 반복하는 구현 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **crewAI** — [원문](https://github.com/crewAIInc/crewAI)
  - crewAI 저장소의 멀티 에이전트 프레임워크 구현을 가리키는 색인 항목이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **EP 86: 진짜 내 일을 위한 Agentic Workflow** — [원문](https://aifrontier.kr/ko/episodes/ep86)
  - 팟캐스트 인터뷰에서 실제 소프트웨어 개발 사례를 통해 에이전트 워크플로의 적용과 한계를 다룬다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Everything Claude Code** — [원문](https://github.com/affaan-m/everything-claude-code)
  - Claude Code 관련 워크플로·도구·지침을 모은 공개 저장소로, 범위와 내용은 upstream에서 확인해야 한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Andrej Karpathy Skills — forrestchang** — [원문](https://github.com/forrestchang/andrej-karpathy-skills)
  - LLM 코딩의 단순성·목표 중심 실행 등을 가이드로 묶은 공개 skill 파일이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Harness - Agent Team & Skill Architect** — [원문](https://github.com/revfactory/harness)
  - 전문 에이전트 팀, 역할 간 위임, 스킬 생성과 검증을 묶은 Claude Code 플러그인 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Hyperagents 검토** — [원문](https://github.com/facebookresearch/hyperagents)
  - Hyperagents 연구/구현을 검토한 기록이며, 운영 성능이나 채택 근거로 보지 않는다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **langgraph** — [원문](https://github.com/langchain-ai/langgraph)
  - LangGraph 저장소의 그래프 기반 에이전트 워크플로 구현을 가리키는 참고 링크다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Skills For Real Engineers - mattpocock/skills** — [원문](https://github.com/mattpocock/skills)
  - 엔지니어링 작업을 위한 재사용 가능한 스킬 모음이며, 구현 방식은 저장소별로 달라질 수 있다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Superpowers: 개발 작업을 구조화한 에이전트 스킬** — [원문](https://github.com/obra/superpowers)
  - 브레인스토밍부터 테스트·리뷰까지 소프트웨어 개발을 구조화한 에이전트 스킬 모음이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Claude Code loop — Boris Cherny (index label)** — 원출처 URL 미확인
  - Claude Code 작업 루프에 관한 것으로 보이는 인덱스 항목이나 출처 URL·본문은 확인되지 않았다.
  - 출처 상태: indexed-only · 제공: unknown
  - 등록 확인: index entry present; no reference or wiki page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Claude Code loop engineering 20-step (index label)** — 원출처 URL 미확인
  - 20단계 Claude Code loop 자료로 보이는 인덱스 항목이며 URL과 본문은 확인되지 않았다.
  - 출처 상태: indexed-only · 제공: unknown
  - 등록 확인: index entry present; no reference or wiki page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **우리, 프로그래머들 — .md로 코딩하는 시대** — [원문](https://velog.io/@teo/we-programmer)
  - AI 시대 개발자의 역할과 에이전트 코드 생성·제어를 다룬 한국어 글을 요약한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

## 문맥·메모리·지식

- **Harness engineering: leveraging Codex in an agent-first world** — [상세 카드](../cards/openai-harness-engineering.md) · [원문](https://openai.com/ko-KR/index/harness-engineering)
  - OpenAI의 agent-first 제품 개발 경험담은 짧은 AGENTS.md를 백과사전보다 지도로 쓰고, 근거가 되는 저장소 문서를 기록 시스템으로 두며, 구조·제약·평가·관측을 도구와 자동 검사에 녹이는 방식을 설명한다. 격리 worktree와 로그·지표 등 에이전트가 관찰·검증 가능한 작업 환경도 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **A Survey of Context Engineering for Large Language Models** — [상세 카드](../cards/context-engineering-survey.md) · [원문](https://arxiv.org/abs/2507.13334)
  - 대규모 언어모델에서 context retrieval/generation, context processing/management 및 RAG, memory, tool-integrated reasoning, multi-agent system 등 아키텍처 계층을 폭넓게 조사하는 ongoing survey다. 검색 결과에 1,300편 이상을 분석했다는 저자 설명이 있다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Agent Skills** — [상세 카드](../cards/agent-skills-standard.md) · [원문](https://agentskills.io/home)
  - Agent Skills는 에이전트가 절차적 능력과 도메인 지식을 발견·로드할 수 있도록 디렉터리와 `SKILL.md` 중심으로 구성하는 portable format을 표방한다. 규격 본문과 구현별 지원 범위를 원문에서 구분해 확인해야 한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Architecting efficient context-aware multi-agent framework for production** — [상세 카드](../cards/google-context-aware-multi-agent.md) · [원문](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production)
  - Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working context를 구분하는 구조를 설명한다. 검색 결과는 context processing과 효율적 multi-agent 운영을 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Software After AI (Harnessing AI) — Tomasz Tunguz** — [상세 카드](../cards/harnessing-ai-tunguz.md) · [원문](https://tomtunguz.com/harnessing-ai)
  - Tomasz Tunguz는 LLM을 신뢰 가능한 에이전트로 만드는 런타임·제약·신뢰성 층을 하네스로 설명하고, 문맥·도구·오케스트레이션·상태·샌드박스·관측·비용의 일곱 구성요소를 제시한다. 이는 저자의 개념 프레임이며 운영 채택 증거는 아니다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-01)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Experiential vs Synthetic Memory in Long-Running AI Agents** — [상세 카드](../cards/experiential-memory-experiment.md) · [원문](https://blog.clawsouls.ai/ko/posts/experiential-memory-experiment)
  - The linked material concerns comparison of experiential versus synthetic memory for long-running agents. The linked dataset repository describes isolated sessions, memory retrieval and a blinded single human evaluator; these are source claims and deserve separate methodological review.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **하네스 엔지니어링: AI 에이전트 시대, 경쟁력은 모델이 아니라 마구에서 나온다** — [원문](https://wikidocs.net/blog/@jaehong/9481)
  - 에이전트 신뢰성을 모델 자체보다 도구·상태·컨텍스트·검증을 포함한 하네스 설계와 연결하는 개요 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Anthropic Skills repository** — [원문](https://github.com/anthropics/skills)
  - Anthropic Skills 저장소는 반복 작업 지침과 관련 리소스를 패키지화하는 구현 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Hippo Memory** — [원문](https://github.com/kitfunso/hippo-memory)
  - 에이전트 기억 저장소의 구현 사례를 가리키며, 구체 동작은 저장소 원문 확인이 필요하다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Knowledge system architecture** — 원출처 URL 미확인
  - 지식 시스템의 구성과 지식 관리 개념을 다루는 색인 항목이다; 참조 원문은 찾지 못했다.
  - 출처 상태: indexed-only · 제공: unknown
  - 등록 확인: index entry present; no reference or wiki page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Letta / MemGPT memory** — [원문](https://letta.com)
  - Letta/MemGPT 계열의 에이전트 기억 설계를 가리키는 항목으로, 상세 출처는 별도 확인이 필요하다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Mem0 memory architecture** — [원문](https://mem0.ai/research)
  - 대화에서 정보를 추출·검색하는 장기 기억 설계와 그래프 관계 모델을 요약한 항목이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Seo Joon Kim: Memory** — [원문](https://seojoonkim.medium.com/memory-d6f559f1fe73)
  - 개인 블로그의 메모리 관련 자료를 가리키며, 제목만으로 상세 내용을 확정할 수 없다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Supermemory — agent memory post** — [원문](https://x.com/DhravyaShah/status/2035517012647272689)
  - Supermemory의 에이전트 메모리 관련 게시물 링크로, 원문 확인 없이는 세부 주장을 확정하지 않는다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Weaviate: Context Engineering for AI Agents** — [원문](https://weaviate.io/blog/context-engineering)
  - 에이전트 컨텍스트의 실패 유형과 검색·메모리 설계 대응을 소개하는 기술 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

## 스킬·도구

- **Agent Skills** — [상세 카드](../cards/agent-skills-standard.md) · [원문](https://agentskills.io/home)
  - Agent Skills는 에이전트가 절차적 능력과 도메인 지식을 발견·로드할 수 있도록 디렉터리와 `SKILL.md` 중심으로 구성하는 portable format을 표방한다. 규격 본문과 구현별 지원 범위를 원문에서 구분해 확인해야 한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **AGENTS.md outperforms skills in our agent evals** — [상세 카드](../cards/vercel-agents-md-skills-evals.md) · [원문](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
  - Vercel이 특정 Next.js 작업 묶음과 agent configuration들에서 AGENTS.md, Skills, baseline을 비교한 평가 사례다. 검색 스니펫에는 baseline 53%, default skill 53%, 명시 지시가 있는 skill 79%, AGENTS.md index 100%로 소개된다. 이 비율은 해당 task set/configuration의 자체 평가 결과다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **How I built an AI marketing team with Claude Code (and Cowork)** — [상세 카드](../cards/runbear-ai-marketing-team.md) · [원문](https://snow.runbear.io/how-i-built-an-ai-marketing-team-with-claude-code-and-cowork-f3405a53ee22)
  - A practitioner report describing an AI marketing team assembled around Claude Code and Cowork. It is an applied case, not a controlled evaluation; this card does not copy implementation content or claim a general workflow result.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Skillify OpenClaw 적용 분석** — 원출처 URL 미확인
  - Skillify의 실패-수정 루프를 OpenClaw 구성에 맞춰 테스트, resolver, 점검 흐름으로 옮긴 설계안이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Skillify: 에이전트 실수를 영구적 구조적 수정으로 변환** — [원문](https://x.com/garrytan/status/2046876981711769720)
  - 에이전트 실패를 재사용 가능한 스킬과 결정적 도구·테스트로 바꾸자는 Skillify 패턴을 정리한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Good Spec: 좋은 명세 작성 가이드** — [원문](https://addyosmani.com/blog/good-spec)
  - 구현 전에 요구사항과 명세를 명확히 해 에이전트가 작업할 계약을 제공하는 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Anthropic Skill Generator (Skill Creator)** — [원문](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
  - Anthropic의 Skill Creator가 스킬 구성, 점진적 공개와 평가 반복을 안내하는 자료다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Anthropic tools repository** — [원문](https://github.com/anthropics/anthropic-tools)
  - Anthropic의 저장소로, 공개된 도구·에이전트 구현 자료를 제공하는 출처다; 세부 내용은 원문 확인이 필요하다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Anthropic Skills repository** — [원문](https://github.com/anthropics/skills)
  - Anthropic Skills 저장소는 반복 작업 지침과 관련 리소스를 패키지화하는 구현 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Everything Claude Code** — [원문](https://github.com/affaan-m/everything-claude-code)
  - Claude Code 관련 워크플로·도구·지침을 모은 공개 저장소로, 범위와 내용은 upstream에서 확인해야 한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Andrej Karpathy Skills — forrestchang** — [원문](https://github.com/forrestchang/andrej-karpathy-skills)
  - LLM 코딩의 단순성·목표 중심 실행 등을 가이드로 묶은 공개 skill 파일이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Harness - Agent Team & Skill Architect** — [원문](https://github.com/revfactory/harness)
  - 전문 에이전트 팀, 역할 간 위임, 스킬 생성과 검증을 묶은 Claude Code 플러그인 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Skills For Real Engineers - mattpocock/skills** — [원문](https://github.com/mattpocock/skills)
  - 엔지니어링 작업을 위한 재사용 가능한 스킬 모음이며, 구현 방식은 저장소별로 달라질 수 있다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **steipete/agent-scripts** — [원문](https://github.com/steipete/agent-scripts)
  - 에이전트 보조 스크립트 저장소를 가리키는 참고 링크다; 세부 내용은 원문 확인 전 미확정이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Superpowers: 개발 작업을 구조화한 에이전트 스킬** — [원문](https://github.com/obra/superpowers)
  - 브레인스토밍부터 테스트·리뷰까지 소프트웨어 개발을 구조화한 에이전트 스킬 모음이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **스킬 시스템 종합 분석: 설계 제안서** — 원출처 URL 미확인
  - 스킬 설계·평가·라우팅 검증을 교차 비교한 설계 제안서의 요약 페이지다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

## 평가·관측·보안

- **Harness engineering: leveraging Codex in an agent-first world** — [상세 카드](../cards/openai-harness-engineering.md) · [원문](https://openai.com/ko-KR/index/harness-engineering)
  - OpenAI의 agent-first 제품 개발 경험담은 짧은 AGENTS.md를 백과사전보다 지도로 쓰고, 근거가 되는 저장소 문서를 기록 시스템으로 두며, 구조·제약·평가·관측을 도구와 자동 검사에 녹이는 방식을 설명한다. 격리 worktree와 로그·지표 등 에이전트가 관찰·검증 가능한 작업 환경도 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **A Survey of Context Engineering for Large Language Models** — [상세 카드](../cards/context-engineering-survey.md) · [원문](https://arxiv.org/abs/2507.13334)
  - 대규모 언어모델에서 context retrieval/generation, context processing/management 및 RAG, memory, tool-integrated reasoning, multi-agent system 등 아키텍처 계층을 폭넓게 조사하는 ongoing survey다. 검색 결과에 1,300편 이상을 분석했다는 저자 설명이 있다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **AGENTS.md outperforms skills in our agent evals** — [상세 카드](../cards/vercel-agents-md-skills-evals.md) · [원문](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
  - Vercel이 특정 Next.js 작업 묶음과 agent configuration들에서 AGENTS.md, Skills, baseline을 비교한 평가 사례다. 검색 스니펫에는 baseline 53%, default skill 53%, 명시 지시가 있는 skill 79%, AGENTS.md index 100%로 소개된다. 이 비율은 해당 task set/configuration의 자체 평가 결과다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Common workflow patterns for AI agents—and when to use them** — [상세 카드](../cards/claude-workflow-patterns.md) · [원문](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them)
  - 고정 순서의 sequential, 독립 작업의 parallel, 평가 후 반복 개선하는 evaluator-optimizer 패턴을 비교한다. 먼저 단일 agent로 시도하고, 실제 latency 병목·독립성·측정된 품질 향상이 확인될 때에만 더 복잡한 패턴을 선택하라고 권한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Experiential vs Synthetic Memory in Long-Running AI Agents** — [상세 카드](../cards/experiential-memory-experiment.md) · [원문](https://blog.clawsouls.ai/ko/posts/experiential-memory-experiment)
  - The linked material concerns comparison of experiential versus synthetic memory for long-running agents. The linked dataset repository describes isolated sessions, memory retrieval and a blinded single human evaluator; these are source claims and deserve separate methodological review.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **하네스 엔지니어링: AI 에이전트 시대, 경쟁력은 모델이 아니라 마구에서 나온다** — [원문](https://wikidocs.net/blog/@jaehong/9481)
  - 에이전트 신뢰성을 모델 자체보다 도구·상태·컨텍스트·검증을 포함한 하네스 설계와 연결하는 개요 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Skillify OpenClaw 적용 분석** — 원출처 URL 미확인
  - Skillify의 실패-수정 루프를 OpenClaw 구성에 맞춰 테스트, resolver, 점검 흐름으로 옮긴 설계안이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Skillify: 에이전트 실수를 영구적 구조적 수정으로 변환** — [원문](https://x.com/garrytan/status/2046876981711769720)
  - 에이전트 실패를 재사용 가능한 스킬과 결정적 도구·테스트로 바꾸자는 Skillify 패턴을 정리한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Anthropic Skill Generator (Skill Creator)** — [원문](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
  - Anthropic의 Skill Creator가 스킬 구성, 점진적 공개와 평가 반복을 안내하는 자료다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **AutoResearch - 자율적 연구 시스템** — [원문](https://github.com/karpathy/autoresearch)
  - 연구자가 프로그램 지침과 제한된 실험 루프를 통해 모델 학습 실험을 반복하는 구현 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Knowledge system architecture** — 원출처 URL 미확인
  - 지식 시스템의 구성과 지식 관리 개념을 다루는 색인 항목이다; 참조 원문은 찾지 못했다.
  - 출처 상태: indexed-only · 제공: unknown
  - 등록 확인: index entry present; no reference or wiki page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Show HN: Continue? Y/N: A 60-second game about AI agent permission fatigue** — [원문](https://llmgame.scalex.dev)
  - 에이전트 권한 확인이 반복될 때의 사용자 피로를 게임 형식으로 보여주는 자료다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Skills For Real Engineers - mattpocock/skills** — [원문](https://github.com/mattpocock/skills)
  - 엔지니어링 작업을 위한 재사용 가능한 스킬 모음이며, 구현 방식은 저장소별로 달라질 수 있다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Superpowers: 개발 작업을 구조화한 에이전트 스킬** — [원문](https://github.com/obra/superpowers)
  - 브레인스토밍부터 테스트·리뷰까지 소프트웨어 개발을 구조화한 에이전트 스킬 모음이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Weaviate: Context Engineering for AI Agents** — [원문](https://weaviate.io/blog/context-engineering)
  - 에이전트 컨텍스트의 실패 유형과 검색·메모리 설계 대응을 소개하는 기술 글이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Claude Code loop engineering 20-step (index label)** — 원출처 URL 미확인
  - 20단계 Claude Code loop 자료로 보이는 인덱스 항목이며 URL과 본문은 확인되지 않았다.
  - 출처 상태: indexed-only · 제공: unknown
  - 등록 확인: index entry present; no reference or wiki page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **스킬 시스템 종합 분석: 설계 제안서** — 원출처 URL 미확인
  - 스킬 설계·평가·라우팅 검증을 교차 비교한 설계 제안서의 요약 페이지다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

## 사례·구현

- **Harness engineering: leveraging Codex in an agent-first world** — [상세 카드](../cards/openai-harness-engineering.md) · [원문](https://openai.com/ko-KR/index/harness-engineering)
  - OpenAI의 agent-first 제품 개발 경험담은 짧은 AGENTS.md를 백과사전보다 지도로 쓰고, 근거가 되는 저장소 문서를 기록 시스템으로 두며, 구조·제약·평가·관측을 도구와 자동 검사에 녹이는 방식을 설명한다. 격리 worktree와 로그·지표 등 에이전트가 관찰·검증 가능한 작업 환경도 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Architecting efficient context-aware multi-agent framework for production** — [상세 카드](../cards/google-context-aware-multi-agent.md) · [원문](https://developers.googleblog.com/en/architecting-efficient-context-aware-multi-agent-framework-for-production)
  - Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working context를 구분하는 구조를 설명한다. 검색 결과는 context processing과 효율적 multi-agent 운영을 강조한다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **How I built an AI marketing team with Claude Code (and Cowork)** — [상세 카드](../cards/runbear-ai-marketing-team.md) · [원문](https://snow.runbear.io/how-i-built-an-ai-marketing-team-with-claude-code-and-cowork-f3405a53ee22)
  - A practitioner report describing an AI marketing team assembled around Claude Code and Cowork. It is an applied case, not a controlled evaluation; this card does not copy implementation content or claim a general workflow result.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-02)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Software After AI (Harnessing AI) — Tomasz Tunguz** — [상세 카드](../cards/harnessing-ai-tunguz.md) · [원문](https://tomtunguz.com/harnessing-ai)
  - Tomasz Tunguz는 LLM을 신뢰 가능한 에이전트로 만드는 런타임·제약·신뢰성 층을 하네스로 설명하고, 문맥·도구·오케스트레이션·상태·샌드박스·관측·비용의 일곱 구성요소를 제시한다. 이는 저자의 개념 프레임이며 운영 채택 증거는 아니다.
  - 출처 상태: derived-only · 제공: 사용자 제공 확인 (2026-06-01)
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: 기존 주 manifest의 주제 기록

- **Skillify OpenClaw 적용 분석** — 원출처 URL 미확인
  - Skillify의 실패-수정 루프를 OpenClaw 구성에 맞춰 테스트, resolver, 점검 흐름으로 옮긴 설계안이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Anthropic tools repository** — [원문](https://github.com/anthropics/anthropic-tools)
  - Anthropic의 저장소로, 공개된 도구·에이전트 구현 자료를 제공하는 출처다; 세부 내용은 원문 확인이 필요하다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **AutoResearch - 자율적 연구 시스템** — [원문](https://github.com/karpathy/autoresearch)
  - 연구자가 프로그램 지침과 제한된 실험 루프를 통해 모델 학습 실험을 반복하는 구현 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **crewAI** — [원문](https://github.com/crewAIInc/crewAI)
  - crewAI 저장소의 멀티 에이전트 프레임워크 구현을 가리키는 색인 항목이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **EP 86: 진짜 내 일을 위한 Agentic Workflow** — [원문](https://aifrontier.kr/ko/episodes/ep86)
  - 팟캐스트 인터뷰에서 실제 소프트웨어 개발 사례를 통해 에이전트 워크플로의 적용과 한계를 다룬다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Everything Claude Code** — [원문](https://github.com/affaan-m/everything-claude-code)
  - Claude Code 관련 워크플로·도구·지침을 모은 공개 저장소로, 범위와 내용은 upstream에서 확인해야 한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Harness - Agent Team & Skill Architect** — [원문](https://github.com/revfactory/harness)
  - 전문 에이전트 팀, 역할 간 위임, 스킬 생성과 검증을 묶은 Claude Code 플러그인 사례다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Hippo Memory** — [원문](https://github.com/kitfunso/hippo-memory)
  - 에이전트 기억 저장소의 구현 사례를 가리키며, 구체 동작은 저장소 원문 확인이 필요하다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Hyperagents 검토** — [원문](https://github.com/facebookresearch/hyperagents)
  - Hyperagents 연구/구현을 검토한 기록이며, 운영 성능이나 채택 근거로 보지 않는다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **langgraph** — [원문](https://github.com/langchain-ai/langgraph)
  - LangGraph 저장소의 그래프 기반 에이전트 워크플로 구현을 가리키는 참고 링크다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Letta / MemGPT memory** — [원문](https://letta.com)
  - Letta/MemGPT 계열의 에이전트 기억 설계를 가리키는 항목으로, 상세 출처는 별도 확인이 필요하다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Mem0 memory architecture** — [원문](https://mem0.ai/research)
  - 대화에서 정보를 추출·검색하는 장기 기억 설계와 그래프 관계 모델을 요약한 항목이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **steipete/agent-scripts** — [원문](https://github.com/steipete/agent-scripts)
  - 에이전트 보조 스크립트 저장소를 가리키는 참고 링크다; 세부 내용은 원문 확인 전 미확정이다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **Claude Code loop — Boris Cherny (index label)** — 원출처 URL 미확인
  - Claude Code 작업 루프에 관한 것으로 보이는 인덱스 항목이나 출처 URL·본문은 확인되지 않았다.
  - 출처 상태: indexed-only · 제공: unknown
  - 등록 확인: index entry present; no reference or wiki page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **스킬 시스템 종합 분석: 설계 제안서** — 원출처 URL 미확인
  - 스킬 설계·평가·라우팅 검증을 교차 비교한 설계 제안서의 요약 페이지다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

- **우리, 프로그래머들 — .md로 코딩하는 시대** — [원문](https://velog.io/@teo/we-programmer)
  - AI 시대 개발자의 역할과 에이전트 코드 생성·제어를 다룬 한국어 글을 요약한다.
  - 출처 상태: derived-only · 제공: unknown
  - 등록 확인: index entry present; reference file missing; wiki derived page located · 분류 근거: title-and-existing-wiki-or-index-record; original source not re-opened for this inventory entry

## 확인 범위

원출처가 없는 항목과 과거 색인·파생 문서만 남은 항목을 삭제하거나 검증된 자료로 승격하지 않았습니다. 직접 원문 전체를 읽은 자료인지, 기존 기록을 요약한 자료인지는 각 상세 카드와 분류 근거를 함께 확인하세요. 제3자 원문·코드·이미지를 재배포하지 않으며 최신 라이선스는 원출처에서 확인해야 합니다.
