# 하네스 엔지니어링 참고 라이브러리

에이전트 하네스의 설계·운영·평가에 관한 공개 자료를 주제별로 정리한 독립 탐색 폴더입니다. 원문 전문이나 사용자 대화는 포함하지 않습니다. 각 카드는 원문 링크, 한 문단 요약, 링크를 열지 않고도 참고할 수 있는 상세 정리(핵심 주장·구조와 패턴·적용 방법·근거와 한계·연결), 출처·권리·활용 상태를 기록합니다. 상세 정리를 무엇을 근거로 썼는지는 카드의 "정리 근거" 줄과 manifest의 `digest_basis`에 있습니다.

## 빠른 시작

1. [개요와 읽기 순서](#읽기-순서)
2. [전체 목차](CATALOG.md)
3. 관심 주제의 하위 목차를 열고 개별 카드를 읽습니다.
4. [manifest.json](manifest.json) 또는 [manifest.csv](manifest.csv)로 출처·상태를 기계적으로 조회합니다.
5. [조사 방법과 한계](SURVEY.md)에서 수집 범위·포함 및 제외 기준을 확인합니다.
6. [과거 참고 색인 39건 재고표](legacy-index-inventory/README.md)에서 기존 색인 자료의 주제별 요약·원문 링크·대응 카드를 탐색합니다.
7. [필드 정의](METADATA.md), [권리/라이선스](LICENSE), [갱신 방법](MAINTENANCE.md)을 확인합니다.

## 주제별 목차

- [개요](CATALOG.md#개요)
- [Orchestration / workflow](CATALOG.md#orchestration--workflow)
- [Context / memory / knowledge](CATALOG.md#context--memory--knowledge)
- [Skills / tools](CATALOG.md#skills--tools)
- [Evaluation / observability / security](CATALOG.md#evaluation--observability--security)
- [사례 / 구현](CATALOG.md#사례--구현)

## 읽기 순서

### 입문
1. [Agent harness technical debt](cards/agent-harness-technical-debt.md) — 무엇을 하네스로 볼지와 모델 발전에 따른 과잉 설계 위험.
2. [Anthropic: Building effective agents](cards/anthropic-building-effective-agents.md) — 단순한 패턴부터 시작하는 기본 원칙.
3. [OpenAI: Harness engineering](cards/openai-harness-engineering.md) — 저장소를 에이전트가 읽고 검증할 환경으로 설계한 사례.

### 실무 설계
4. [Anthropic: Long-running agents](cards/anthropic-effective-long-running-agents.md) — 다중 context window에서 계획·진행·handoff.
5. [Google: Context-aware multi-agent](cards/google-context-aware-multi-agent.md) — session과 working context를 분리하는 구조.
6. [Claude workflow patterns](cards/claude-workflow-patterns.md) — sequential/parallel/evaluator-optimizer 선택과 trade-off.
7. [Vercel: AGENTS.md와 Skills 평가](cards/vercel-agents-md-skills-evals.md) — task 조건과 측정 범위를 확인하며 읽습니다.

### 연구와 비교 사례
8. [Meta-Harness](cards/meta-harness.md) → [JAZ](cards/jaz-harness-language.md) — 하네스 탐색·최소 언어 모델의 연구 결과를 적용 한계와 함께 봅니다.
9. [DeepSeek Harness](cards/deepseek-harness.md) → [AAABench](cards/aaabench.md) → [Browser Harness](cards/browser-harness.md) — 실행 가능한 구현 사례와 maturity/security 경계.

## 해석 원칙

- 참고 자료는 운영 채택, 안전성 인증 또는 Hermes에서의 성능 검증을 뜻하지 않습니다.
- 출처의 자체 주장·벤치마크는 출처 주장으로 표시하며 독립 재현과 구분합니다.
- 제공 링크·첨부, 지식 등록, 조사/JOB 검토, 실제 운영 적용은 별개의 상태입니다. `unknown`은 확인 실패/미확인을 의미하며 `false`로 간주하지 않습니다.
- 출처에 라이선스가 명시되지 않거나 확인되지 않으면 요약과 링크만 제공합니다. 외부 원문·코드·이미지는 복사하지 않습니다.
- 공개 자료의 출처·권리 상태가 바뀔 수 있으므로 이용 전 원문과 최신 라이선스를 재확인하세요.

## 독립 배포와 권리

이 폴더는 다른 저장소로 복사해도 탐색 가능한 상대 링크, manifest, 자체 라이선스, 메타데이터 설명, 유지보수 절차를 포함합니다. 자체 MIT 허용은 카드의 자체 요약/metadata에만 적용되며 링크된 제3자 자료에는 적용되지 않습니다. 각 원문과 최신 권리를 따로 확인하세요. 상세 범위와 조사 수치는 [SURVEY.md](SURVEY.md)에 있습니다.
