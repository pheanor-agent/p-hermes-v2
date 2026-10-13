# 전체 목차

카드에는 원문 링크와 자체 요약이 있습니다. `provided`는 사용자가 대화에서 직접 건넨 링크를 내부 근거로 확인한 경우, `registered`는 현재 또는 과거 지식 문서에 별도 기록이 확인된 경우입니다. 표의 상태는 도입·운영 채택이 아닙니다.

## 개요

- [Agent harness technical debt](cards/agent-harness-technical-debt.md) — 하네스 구성요소와 기술부채·복잡성의 시간가치.
- [Anthropic: Building effective agents](cards/anthropic-building-effective-agents.md) — 단순하고 조합 가능한 agent/workflow 설계.
- [Anthropic: Harness design for long-running application development](cards/anthropic-harness-design-long-running-apps.md) — planner/generator/evaluator 구조와 장기 작업.
- [Code as Agent Harness](cards/code-as-agent-harness.md) — 코드 기반 harness 관점의 연구 survey.
- [Raven: Harness of Harnesses](cards/raven-composable-agentic-intelligence.md) — composable agentic intelligence; 초록 수준.
- [Context Engineering survey](cards/context-engineering-survey.md) — 관련 context·memory·tool-use 문헌의 survey.
- [Microsoft AI agent design patterns](cards/microsoft-agent-design-patterns.md) — vendor architecture guide; 최신 내용 재검토 필요.
- [Flowkater: 에이전틱 엔지니어링 9가지 역량](cards/flowkater-agentic-engineering-skills.md) — 실무 에세이; 경험 기반 주장.

- [Harness engineering: leveraging Codex in an agent-first world](cards/openai-harness-engineering.md) — OpenAI의 agent-first 제품 개발 경험담은 짧은 AGENTS.md를 백과사전보다 지도로 쓰고, 근거가 되는 저장소 문서를 기록 시스템으로 두며, 구조·제약·평가·관측을 도구와 자동 검사에 녹이는… 활용/등록은 카드에서 확인.
- [Effective harnesses for long-running agents](cards/anthropic-effective-long-running-agents.md) — 긴 작업이 여러 context window와 session을 넘을 때 compaction만으로는 부족할 수 있다고 설명한다. 활용/등록은 카드에서 확인.
- [Agents are hard](cards/agents-are-hard.md) — 에이전트 시스템 구축에서 모델 능력 외의 어려움—환경, 도구, 피드백, 반복 실행 및 실패 처리—을 다루는 실무 관점 글이다. 활용/등록은 카드에서 확인.
- [Agentic Engineering Patterns](cards/simon-willison-agentic-engineering.md) — 코딩 agent와 함께 일하는 실무 패턴을 모은 갱신형 guide다. 활용/등록은 카드에서 확인.
- [Harness as a Language: A Minimalist Agent Framework With Maximal Expressivity](cards/jaz-harness-language.md) — JAZ는 `invoke`를 중심으로 모델이 실행 가능한 코드를 생성하고, 호출 이력·입력·도구를 코드에서 참조하며 재귀 sub-invoke와 hook을 사용하는 미니멀 agent framework를 제안한다. 활용/등록은 카드에서 확인.
- [Harnessing AI](cards/harnessing-ai-tunguz.md) — URL/제공 사건은 원천 메시지 증거로 확인; 본문 전문 및 활용 근거 미확인; 활용/등록은 카드에서 확인.
## Orchestration / workflow

- [Anthropic: Effective harnesses for long-running agents](cards/anthropic-effective-long-running-agents.md) — initializer, feature list, 진행 파일과 session 간 handoff.
- [Anthropic: Multi-agent research system](cards/anthropic-multi-agent-research-system.md) — orchestrator-worker와 병렬 연구의 적용 조건.
- [Graph of Thoughts](cards/graph-of-thoughts.md) — 산출물 graph와 변환·평가; agent runtime과 구별.
- [Claude workflow patterns](cards/claude-workflow-patterns.md) — sequential, parallel, evaluator-optimizer.
- [Loop Engineering (Addy Osmani)](cards/addy-loop-engineering.md) — 자동화·worktree·skill·subagent·memory를 포함하는 지속 루프.
- [Harness as a Language / JAZ](cards/jaz-harness-language.md) — 재귀 `invoke`, 실행 코드와 hook 기반 연구 프레임워크.
- [OpenAI multi-agent API 문서](cards/openai-multi-agent-docs.md) — API/SDK 공식 orchestration 안내.
- [Hermes 공식 문서](cards/hermes-official-docs.md) — loops, context files, session storage, prompt assembly, memory.
- [Apache Maka Agent Graph](cards/apache-maka-agent-graph.md) — durable scheduling/graph draft; 초안 주의.
- [Microsoft AI agent design patterns](cards/microsoft-agent-design-patterns.md) — AI agent architecture guide.
- [LangGraph human approval](cards/langgraph-human-approval.md) — tool-call human-in-the-loop 구현 문서.
- [Agents are hard](cards/agents-are-hard.md) — 하네스 주변의 일반 구현 난점.

- [Harness design for long-running application development](cards/anthropic-harness-design-long-running-apps.md) — 복잡한 응용 개발에 planner, generator, evaluator 역할을 나누고, 큰 작업을 작은 단위로 쪼개며, context reset 때 구조화된 handoff를 사용한 사례다. 활용/등록은 카드에서 확인.
- [Building effective agents](cards/anthropic-building-effective-agents.md) — 필요 이상으로 복잡한 agent framework부터 도입하지 말고, 단순한 prompt/workflow로 시작해 평가를 통해 부족함이 확인된 경우에만 routing, parallelization… 활용/등록은 카드에서 확인.
- [Architecting efficient context-aware multi-agent framework for production](cards/google-context-aware-multi-agent.md) — Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working… 활용/등록은 카드에서 확인.
- [Agentic Engineering Patterns](cards/simon-willison-agentic-engineering.md) — 코딩 agent와 함께 일하는 실무 패턴을 모은 갱신형 guide다. 활용/등록은 카드에서 확인.
- [DeepSeek Harness](cards/deepseek-harness.md) — DeepSeek가 공개한 dsh agent harness로 “Everything is a Plugin”을 설계 방향으로 내세우며, Cordis 기반 구성·도구·plugin 확장과 Web/Desktop 앱… 활용/등록은 카드에서 확인.
- [AAABench](cards/aaabench.md) — Unreal Engine Editor를 MCP로 제어해 coding agent가 장기 open-world game 제작을 수행하는 benchmark/harness 사례다. 활용/등록은 카드에서 확인.
- [A Survey of Context Engineering for Large Language Models](cards/context-engineering-survey.md) — 대규모 언어모델에서 context retrieval/generation, context processing/management 및 RAG, memory, tool-integrated reasoning… 활용/등록은 카드에서 확인.
- [Code as Agent Harness](cards/code-as-agent-harness.md) — 코드를 단순 결과물이 아니라 agent의 reasoning, action, environment modeling, execution verification을 연결하는 operational substrate로… 활용/등록은 카드에서 확인.
- [Raven: The Harness of Harnesses for Composable Agentic Intelligence](cards/raven-composable-agentic-intelligence.md) — arXiv에 등록된 “harness of harnesses” composable agentic intelligence 연구다. 활용/등록은 카드에서 확인.
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](cards/agentic-harness-evolution.md) — 제목과 arXiv abstract page를 확인한 결과, coding-agent harness를 observability 중심으로 자동 진화시키는 접근을 다룬 연구다. 활용/등록은 카드에서 확인.
- [How I built an AI marketing team with Claude Code (and Cowork)](cards/runbear-ai-marketing-team.md) — A practitioner report describing an AI marketing team assembled around Claude Code and Cowork. 활용/등록은 카드에서 확인.
- [에이전틱 엔지니어링 시대의 생존 스킬 9가지](cards/flowkater-agentic-engineering-skills.md) — 글은 에이전트 시대의 엔지니어링을 직접 타이핑이 아니라 일을 잘게 나누고, context를 설계하며, 완료 조건을 정의하고, 실패를 복구하며, 관측·메모리·병렬 작업·추상화·taste를 관리하는 것으로 설명합니다. 활용/등록은 카드에서 확인.
- [Graph Engineering with Claude: 14-Step roadmap from 0 to graph architect](cards/graph-engineering-claude-codez.md) — X 본문 일부 미확인; 지식 레코드 요약 기반; 활용/등록은 카드에서 확인.
- [Loop Engineering: The 20-Step Roadmap From Prompter to Loop Designer](cards/claude-code-loop-engineering-20-step.md) — 사용자 제공 텍스트 및 지식 문서 요약 확인; 외부 X 페이지는 로그인 게이트; 활용/등록은 카드에서 확인.
- [7 Rules for Self-Improving Agent Loops](cards/google-cloud-self-improving-agent-loops.md) — 사용자 첨부 Notes 및 X 본문 대조를 기존 JOB 기록으로 확인; 첨부 원문은 현재 지정 cache 경로에서 찾지 못함; 활용/등록은 카드에서 확인.
- [멀티 에이전트 오케스트레이션 리퍼런스 모음](cards/multi-agent-orchestration-patterns.md) — 지식 문서 존재 확인; 제공 시점/등록 요청/사용자 발화는 원천 증거로 미확정; 활용/등록은 카드에서 확인.
- [5 design patterns for long-horizon agent harness](cards/google-cloud-long-horizon-patterns.md) — X URL 및 내부 참조 기록(익명) 등록/검토 기록 확인; 첨부 Notes 전문은 지정 경로에서 찾지 못해 공개 라이브러리에 재배포하지 않음; 활용/등록은 카드에서 확인.
- [Harnessing AI](cards/harnessing-ai-tunguz.md) — URL/제공 사건은 원천 메시지 증거로 확인; 본문 전문 및 활용 근거 미확인; 활용/등록은 카드에서 확인.
## Context / memory / knowledge

- [OpenAI: Harness engineering](cards/openai-harness-engineering.md) — 저장소 지식, AGENTS.md 맵, 구조적 제약과 관측.
- [Google: Context-aware multi-agent framework](cards/google-context-aware-multi-agent.md) — context engineering과 저장 상태/활성 context 분리.
- [Letta: Context Repositories](cards/letta-context-repositories.md) — git 추적 context 저장소와 점진 공개.
- [Agentic Engineering Patterns (Simon Willison)](cards/simon-willison-agentic-engineering.md) — coding-agent 작업 패턴·검증 습관.
- [Flowkater: 에이전틱 엔지니어링 역량](cards/flowkater-agentic-engineering-skills.md) — decomposition, context, recovery, observability 등.
- [Hermes 공식 문서](cards/hermes-official-docs.md) — Hermes 기능의 1차 문서 진입점.
- [Context Engineering survey](cards/context-engineering-survey.md) — RAG, memory, context management의 넓은 문헌 지도.
- [Experiential vs Synthetic Memory](cards/experiential-memory-experiment.md) — 장기 agent memory의 실험 사례; 재현과 외적 타당성 주의.

- [Effective harnesses for long-running agents](cards/anthropic-effective-long-running-agents.md) — 긴 작업이 여러 context window와 session을 넘을 때 compaction만으로는 부족할 수 있다고 설명한다. 활용/등록은 카드에서 확인.
- [Loop Engineering](cards/addy-loop-engineering.md) — 에이전트를 사람이 매번 prompting하기보다 목표를 반복 실행하는 loop를 설계하는 관점으로 자동화·worktree·skills·connectors·subagents·memory를 논한다. 활용/등록은 카드에서 확인.
- [Agent Skills](cards/agent-skills-standard.md) — 형식 참고 자료. Hermes 호환성 증명이 아님.
- [Meta-Harness: End-to-End Optimization of Model Harnesses](cards/meta-harness.md) — 고정된 base model 주변의 task-specific harness를 검색·최적화하는 framework다. 활용/등록은 카드에서 확인.
- [Harness as a Language: A Minimalist Agent Framework With Maximal Expressivity](cards/jaz-harness-language.md) — JAZ는 `invoke`를 중심으로 모델이 실행 가능한 코드를 생성하고, 호출 이력·입력·도구를 코드에서 참조하며 재귀 sub-invoke와 hook을 사용하는 미니멀 agent framework를 제안한다. 활용/등록은 카드에서 확인.
- [Code as Agent Harness](cards/code-as-agent-harness.md) — 코드를 단순 결과물이 아니라 agent의 reasoning, action, environment modeling, execution verification을 연결하는 operational substrate로… 활용/등록은 카드에서 확인.
- [MemGPT — Context OS](cards/memgpt-context-os.md) — 등록된 지식 문서 요약 확인; 사용자 제공 여부는 감사 증거로 확정되지 않아 unknown; 활용/등록은 카드에서 확인.
- [Supermemory — Memory and Context Engine for AI](cards/supermemory.md) — 기존 reference 파일 확인; 제공 시점은 미확정; 활용/등록은 카드에서 확인.
- [codebase-memory-mcp — external read-only reference](cards/codebase-memory-mcp.md) — 지식 문서 확인; 사용자 제공 여부 및 활용 시점은 미확정; 활용/등록은 카드에서 확인.
- [OpenAI — Skills concept](cards/openai-skills-concept.md) — 등록된 reference record와 문서 확인; 사용자 제공 여부는 미확정; 활용/등록은 카드에서 확인.
- [5 design patterns for long-horizon agent harness](cards/google-cloud-long-horizon-patterns.md) — X URL 및 내부 참조 기록(익명) 등록/검토 기록 확인; 첨부 Notes 전문은 지정 경로에서 찾지 못해 공개 라이브러리에 재배포하지 않음; 활용/등록은 카드에서 확인.
- [Harnessing AI](cards/harnessing-ai-tunguz.md) — URL/제공 사건은 원천 메시지 증거로 확인; 본문 전문 및 활용 근거 미확인; 활용/등록은 카드에서 확인.
## Skills / tools

- [Agent Skills standard](cards/agent-skills-standard.md) — SKILL.md 기반 재사용 capability 형식.
- [Vercel: AGENTS.md vs Skills evaluation](cards/vercel-agents-md-skills-evals.md) — Next.js 작업에서의 제한된 비교 실험.
- [Browser Harness](cards/browser-harness.md) — 브라우저/CDP 도구 사례; 성숙도·텔레메트리 주의.
- [DeepSeek Harness](cards/deepseek-harness.md) — plugin-oriented agent runtime 사례.

- [Building effective agents](cards/anthropic-building-effective-agents.md) — 필요 이상으로 복잡한 agent framework부터 도입하지 말고, 단순한 prompt/workflow로 시작해 평가를 통해 부족함이 확인된 경우에만 routing, parallelization… 활용/등록은 카드에서 확인.
- [Loop Engineering](cards/addy-loop-engineering.md) — 에이전트를 사람이 매번 prompting하기보다 목표를 반복 실행하는 loop를 설계하는 관점으로 자동화·worktree·skills·connectors·subagents·memory를 논한다. 활용/등록은 카드에서 확인.
- [OpenAI multi-agent and orchestration API guides](cards/openai-multi-agent-docs.md) — 두 공식 개발자 문서 링크는 multi-agent 호출 및 agent 간 orchestration을 설명하는 문서 진입점이다. 활용/등록은 카드에서 확인.
- [Hermes official documentation: harness-related features](cards/hermes-official-docs.md) — Loops, context files, session persistence, prompt construction 및 memory는 하네스의 상호 연결된 층을 설명하는 공식 제품 문서다. 활용/등록은 카드에서 확인.
- [Introducing Context Repositories: Git-based Memory for Coding Agents](cards/letta-context-repositories.md) — Letta Code의 agent context를 로컬 파일시스템과 Git으로 version 관리하고, context 정리·검색·재구성에 terminal과 subagent를 이용하는 접근을 설명한다. 활용/등록은 카드에서 확인.
- [Agentic Engineering Patterns](cards/simon-willison-agentic-engineering.md) — 코딩 agent와 함께 일하는 실무 패턴을 모은 갱신형 guide다. 활용/등록은 카드에서 확인.
- [Agent Skills](cards/agent-skills-standard.md) — 형식 참고 자료. Hermes 호환성 증명이 아님.
- [How I built an AI marketing team with Claude Code (and Cowork)](cards/runbear-ai-marketing-team.md) — A practitioner report describing an AI marketing team assembled around Claude Code and Cowork. 활용/등록은 카드에서 확인.
- [Agent Reach](cards/agent-reach.md) — An agent capability layer presented as selecting, installing, health-checking and routing among upstream information… 활용/등록은 카드에서 확인.
- [Supermemory — Memory and Context Engine for AI](cards/supermemory.md) — 기존 reference 파일 확인; 제공 시점은 미확정; 활용/등록은 카드에서 확인.
- [codebase-memory-mcp — external read-only reference](cards/codebase-memory-mcp.md) — 지식 문서 확인; 사용자 제공 여부 및 활용 시점은 미확정; 활용/등록은 카드에서 확인.
- [OpenAI — Build skills](cards/openai-build-skills.md) — 등록된 reference record와 문서 확인; 현재 사용자 제공 여부를 이 감사에서 확정하지 않음; 활용/등록은 카드에서 확인.
- [OpenAI — Skills concept](cards/openai-skills-concept.md) — 등록된 reference record와 문서 확인; 사용자 제공 여부는 미확정; 활용/등록은 카드에서 확인.
- [typesafe-ai/skills — skills repository](cards/typesafe-ai-skills.md) — GLM 사용자 발화에서 요청 확인; 등록 파일 존재, index 미등재. 관련 활용 증거는 별도 검토 필요; 활용/등록은 카드에서 확인.
## Evaluation / observability / security

- [Vercel: AGENTS.md vs Skills evaluation](cards/vercel-agents-md-skills-evals.md) — 작은 task set과 pass-rate 측정의 범위.
- [Anthropic: Harness design](cards/anthropic-harness-design-long-running-apps.md) — 별도 evaluator와 주관적 품질 기준의 설계.
- [Meta-Harness](cards/meta-harness.md) — 후보 하네스 제안·실행·평가를 반복하는 자동 탐색.
- [JAZ](cards/jaz-harness-language.md) — 관측, 예산, 검증 hook 및 임의 코드 실행 경계.
- [Agents are hard](cards/agents-are-hard.md) — 일반적인 실패·구현 난점의 보조 자료.
- [Agentic Harness Engineering](cards/agentic-harness-evolution.md) — observability 기반 자동 진화 연구; 초록 수준.
- [Code as Agent Harness](cards/code-as-agent-harness.md) — 평가·검증 문제를 다룬 survey 관점.

- [Hidden Technical Debt of AI Systems: Agent Harness](cards/agent-harness-technical-debt.md) — 모델과 환경 사이의 하네스를 prompt/persona, tool surface, rollout protocol, context manager, memory, sub-agent topology… 활용/등록은 카드에서 확인.
- [Harness engineering: leveraging Codex in an agent-first world](cards/openai-harness-engineering.md) — OpenAI의 agent-first 제품 개발 경험담은 짧은 AGENTS.md를 백과사전보다 지도로 쓰고, 근거가 되는 저장소 문서를 기록 시스템으로 두며, 구조·제약·평가·관측을 도구와 자동 검사에 녹이는… 활용/등록은 카드에서 확인.
- [How we built our multi-agent research system](cards/anthropic-multi-agent-research-system.md) — 리드 에이전트가 질의를 계획하고 서로 독립적인 탐색을 병렬 subagent에 위임하는 연구 시스템을 설명한다. 활용/등록은 카드에서 확인.
- [Common workflow patterns for AI agents—and when to use them](cards/claude-workflow-patterns.md) — 고정 순서의 sequential, 독립 작업의 parallel, 평가 후 반복 개선하는 evaluator-optimizer 패턴을 비교한다. 활용/등록은 카드에서 확인.
- [Loop Engineering](cards/addy-loop-engineering.md) — 에이전트를 사람이 매번 prompting하기보다 목표를 반복 실행하는 loop를 설계하는 관점으로 자동화·worktree·skills·connectors·subagents·memory를 논한다. 활용/등록은 카드에서 확인.
- [Agentic Engineering Patterns](cards/simon-willison-agentic-engineering.md) — 코딩 agent와 함께 일하는 실무 패턴을 모은 갱신형 guide다. 활용/등록은 카드에서 확인.
- [AAABench](cards/aaabench.md) — Unreal Engine Editor를 MCP로 제어해 coding agent가 장기 open-world game 제작을 수행하는 benchmark/harness 사례다. 활용/등록은 카드에서 확인.
- [browser-harness (browser-use)](cards/browser-harness.md) — Chrome DevTools Protocol을 통해 agent가 브라우저를 다루고, 실행 중 helper를 작성하거나 도메인 skill을 축적하는 구현 사례다. 활용/등록은 카드에서 확인.
- [A Survey of Context Engineering for Large Language Models](cards/context-engineering-survey.md) — 대규모 언어모델에서 context retrieval/generation, context processing/management 및 RAG, memory, tool-integrated reasoning… 활용/등록은 카드에서 확인.
- [Apache Maka Agent Graph and stream scheduling draft](cards/apache-maka-agent-graph.md) — Apache Maka의 agent graph와 stream scheduling architecture draft로, graph scheduling과 runtime events/child sessions 관계를… 활용/등록은 카드에서 확인.
- [Add human-in-the-loop review to LangGraph tool calls](cards/langgraph-human-approval.md) — LangGraph documentation page for adding human-in-the-loop review to tool calls. 활용/등록은 카드에서 확인.
- [AI agent design patterns](cards/microsoft-agent-design-patterns.md) — Microsoft Architecture Center guide on AI agent design patterns, useful as a vendor architecture overview. 활용/등록은 카드에서 확인.
- [Experiential vs Synthetic Memory in Long-Running AI Agents](cards/experiential-memory-experiment.md) — The linked material concerns comparison of experiential versus synthetic memory for long-running agents. 활용/등록은 카드에서 확인.
- [Agent Reach](cards/agent-reach.md) — An agent capability layer presented as selecting, installing, health-checking and routing among upstream information… 활용/등록은 카드에서 확인.
- [에이전틱 엔지니어링 시대의 생존 스킬 9가지](cards/flowkater-agentic-engineering-skills.md) — 글은 에이전트 시대의 엔지니어링을 직접 타이핑이 아니라 일을 잘게 나누고, context를 설계하며, 완료 조건을 정의하고, 실패를 복구하며, 관측·메모리·병렬 작업·추상화·taste를 관리하는 것으로 설명합니다. 활용/등록은 카드에서 확인.
- [Graph of Thoughts: Solving Elaborate Problems with Large Language Models](cards/graph-of-thoughts.md) — Graph of Thoughts는 LLM의 중간 생각/산출을 graph로 모델링하고, 의존관계·변환·평가·랭킹을 사용해 여러 경로의 결과를 결합하거나 개선하는 framework를 제안합니다. 활용/등록은 카드에서 확인.
- [Loop Engineering: The 20-Step Roadmap From Prompter to Loop Designer](cards/claude-code-loop-engineering-20-step.md) — 사용자 제공 텍스트 및 지식 문서 요약 확인; 외부 X 페이지는 로그인 게이트; 활용/등록은 카드에서 확인.
- [7 Rules for Self-Improving Agent Loops](cards/google-cloud-self-improving-agent-loops.md) — 사용자 첨부 Notes 및 X 본문 대조를 기존 JOB 기록으로 확인; 첨부 원문은 현재 지정 cache 경로에서 찾지 못함; 활용/등록은 카드에서 확인.
- [멀티 에이전트 오케스트레이션 리퍼런스 모음](cards/multi-agent-orchestration-patterns.md) — 지식 문서 존재 확인; 제공 시점/등록 요청/사용자 발화는 원천 증거로 미확정; 활용/등록은 카드에서 확인.
- [codebase-memory-mcp — external read-only reference](cards/codebase-memory-mcp.md) — 지식 문서 확인; 사용자 제공 여부 및 활용 시점은 미확정; 활용/등록은 카드에서 확인.
- [5 design patterns for long-horizon agent harness](cards/google-cloud-long-horizon-patterns.md) — X URL 및 내부 참조 기록(익명) 등록/검토 기록 확인; 첨부 Notes 전문은 지정 경로에서 찾지 못해 공개 라이브러리에 재배포하지 않음; 활용/등록은 카드에서 확인.
- [typesafe-ai/skills — skills repository](cards/typesafe-ai-skills.md) — GLM 사용자 발화에서 요청 확인; 등록 파일 존재, index 미등재. 관련 활용 증거는 별도 검토 필요; 활용/등록은 카드에서 확인.
## 사례 / 구현

- [OpenAI: Harness engineering](cards/openai-harness-engineering.md) — agent-first 제품 코드베이스 사례.
- [Anthropic: Long-running agents](cards/anthropic-effective-long-running-agents.md) — 여러 세션에 걸친 software-development 사례.
- [DeepSeek Harness](cards/deepseek-harness.md) — plugin 중심 구현.
- [OpenAI multi-agent API 문서](cards/openai-multi-agent-docs.md) — multi-agent API/SDK.
- [Agent Reach](cards/agent-reach.md) — tool/capability discovery layer.
- [Meta-Harness](cards/meta-harness.md) — text classification·Terminal-Bench 예시.
- [AAABench](cards/aaabench.md) — Unreal Editor 제어를 이용하는 장기 게임 제작 벤치마크.
- [Browser Harness](cards/browser-harness.md) — CDP 브라우저 자동화 구현.
- [Hermes 공식 문서](cards/hermes-official-docs.md) — 제품 자체의 기능 문서.
- [Runbear AI marketing team](cards/runbear-ai-marketing-team.md) — domain-specific multi-agent practitioner case.
- [Agent Reach](cards/agent-reach.md) — tool surface/capability selection 사례.
- [Raven](cards/raven-composable-agentic-intelligence.md) — 초록 수준의 composable harness 연구.
- [Graph of Thoughts](cards/graph-of-thoughts.md) — graph-based reasoning workflow research.
- [Flowkater](cards/flowkater-agentic-engineering-skills.md) — practitioner experience report.

- [Harness design for long-running application development](cards/anthropic-harness-design-long-running-apps.md) — 복잡한 응용 개발에 planner, generator, evaluator 역할을 나누고, 큰 작업을 작은 단위로 쪼개며, context reset 때 구조화된 handoff를 사용한 사례다. 활용/등록은 카드에서 확인.
- [How we built our multi-agent research system](cards/anthropic-multi-agent-research-system.md) — 리드 에이전트가 질의를 계획하고 서로 독립적인 탐색을 병렬 subagent에 위임하는 연구 시스템을 설명한다. 활용/등록은 카드에서 확인.
- [Architecting efficient context-aware multi-agent framework for production](cards/google-context-aware-multi-agent.md) — Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working… 활용/등록은 카드에서 확인.
- [Introducing Context Repositories: Git-based Memory for Coding Agents](cards/letta-context-repositories.md) — Letta Code의 agent context를 로컬 파일시스템과 Git으로 version 관리하고, context 정리·검색·재구성에 terminal과 subagent를 이용하는 접근을 설명한다. 활용/등록은 카드에서 확인.
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](cards/agentic-harness-evolution.md) — 제목과 arXiv abstract page를 확인한 결과, coding-agent harness를 observability 중심으로 자동 진화시키는 접근을 다룬 연구다. 활용/등록은 카드에서 확인.
- [Apache Maka Agent Graph and stream scheduling draft](cards/apache-maka-agent-graph.md) — Apache Maka의 agent graph와 stream scheduling architecture draft로, graph scheduling과 runtime events/child sessions 관계를… 활용/등록은 카드에서 확인.
- [Graph Engineering with Claude: 14-Step roadmap from 0 to graph architect](cards/graph-engineering-claude-codez.md) — X 본문 일부 미확인; 지식 레코드 요약 기반; 활용/등록은 카드에서 확인.
- [Loop Engineering: The 20-Step Roadmap From Prompter to Loop Designer](cards/claude-code-loop-engineering-20-step.md) — 사용자 제공 텍스트 및 지식 문서 요약 확인; 외부 X 페이지는 로그인 게이트; 활용/등록은 카드에서 확인.
- [MemGPT — Context OS](cards/memgpt-context-os.md) — 등록된 지식 문서 요약 확인; 사용자 제공 여부는 감사 증거로 확정되지 않아 unknown; 활용/등록은 카드에서 확인.
- [7 Rules for Self-Improving Agent Loops](cards/google-cloud-self-improving-agent-loops.md) — 사용자 첨부 Notes 및 X 본문 대조를 기존 JOB 기록으로 확인; 첨부 원문은 현재 지정 cache 경로에서 찾지 못함; 활용/등록은 카드에서 확인.
- [멀티 에이전트 오케스트레이션 리퍼런스 모음](cards/multi-agent-orchestration-patterns.md) — 지식 문서 존재 확인; 제공 시점/등록 요청/사용자 발화는 원천 증거로 미확정; 활용/등록은 카드에서 확인.
- [Supermemory — Memory and Context Engine for AI](cards/supermemory.md) — 기존 reference 파일 확인; 제공 시점은 미확정; 활용/등록은 카드에서 확인.
- [codebase-memory-mcp — external read-only reference](cards/codebase-memory-mcp.md) — 지식 문서 확인; 사용자 제공 여부 및 활용 시점은 미확정; 활용/등록은 카드에서 확인.
- [OpenAI — Build skills](cards/openai-build-skills.md) — 등록된 reference record와 문서 확인; 현재 사용자 제공 여부를 이 감사에서 확정하지 않음; 활용/등록은 카드에서 확인.
- [5 design patterns for long-horizon agent harness](cards/google-cloud-long-horizon-patterns.md) — X URL 및 내부 참조 기록(익명) 등록/검토 기록 확인; 첨부 Notes 전문은 지정 경로에서 찾지 못해 공개 라이브러리에 재배포하지 않음; 활용/등록은 카드에서 확인.
- [Harnessing AI](cards/harnessing-ai-tunguz.md) — URL/제공 사건은 원천 메시지 증거로 확인; 본문 전문 및 활용 근거 미확인; 활용/등록은 카드에서 확인.
- [typesafe-ai/skills — skills repository](cards/typesafe-ai-skills.md) — GLM 사용자 발화에서 요청 확인; 등록 파일 존재, index 미등재. 관련 활용 증거는 별도 검토 필요; 활용/등록은 카드에서 확인.
## URL·중복 처리

같은 자료의 OpenAI 한국어/영어 경로와 arXiv abstract/HTML은 한 주자료에 묶고 보조 URL을 남겼습니다. 서로 다른 관점·산출물이 있는 Anthropic의 두 장기 작업 글은 별도 카드입니다. 추적 파라미터와 URL 끝 구두점만 정리했으며, 경로·버전이 의미를 가질 수 있는 URL은 그대로 유지했습니다.

## 보완 추가 (2026-10-14)

- [Claude Code memory 문서](cards/claude-code-memory-docs.md) — 공식 문서 링크. 활용 증거 없음(unknown).
- [Codex AGENTS.md 문서](cards/codex-agents-md-docs.md) — 공식 문서 링크. 활용 증거 없음(unknown).
