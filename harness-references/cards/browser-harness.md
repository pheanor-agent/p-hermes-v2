# browser-harness (browser-use)

- 원문: https://github.com/browser-use/browser-harness
- 출처 시점: 사용자 링크 제공 확인 2026-07-04 (KST); 기존 knowledge 카드 검토 2026-07-04.
- 주제: skills/tools · security · 사례/구현
- 상태: `knowledge/references/github/browser-harness.md` 등록; 기존 평가는 미도입·참고. 현재 upstream 상태 재검증은 하지 않음.
- 권리: 기존 카드에 MIT라고 기록됐으나 이번 원문 재검증은 안 됨. 코드·원문 미복사.
- 정리 근거: 원문 일부 확인

## 자체 요약

Chrome DevTools Protocol을 통해 agent가 브라우저를 다루고, 실행 중 helper를 작성하거나 도메인 skill을 축적하는 구현 사례다. 기존 검토는 Alpha maturity, optional cloud/OAuth, PostHog telemetry를 위험으로 기록했다.

## 상세 정리
### 핵심 주장
- LLM이 Chrome DevTools Protocol(CDP)의 WebSocket으로 실제 브라우저를 직접 제어하게 하는 하네스다. 고정된 도구 목록 대신, 에이전트가 작업 중 빠진 helper를 스스로 작성해 쓰는 것이 핵심 주장이다.
- 작업을 거듭하면서 사이트별 지식을 domain skill로 쌓아 다음 작업에 재사용한다는 것이 두 번째 주장이다. 저장소는 이를 '자기 치유(self-healing)' 하네스라고 부른다.
- 설치는 uv 기반 Python 환경에 스킬을 등록하고 로컬 브라우저에 연결하는 방식으로 안내된다. 로컬 브라우저 녹화 여부는 사용자에게 묻도록 되어 있다.
- 클라우드 브라우저 확장(병렬 실행, 프록시, CAPTCHA 등)과 MCP 서버(browser-harness-mcp)를 제공해 다른 MCP 클라이언트에서도 같은 도구를 쓸 수 있다고 소개한다.

### 구조와 패턴
- 핵심 패키지는 고정되어 보호되고, 에이전트는 로컬 작업 공간의 agent_helpers 파일에 helper를 추가하는 구조다.
- 저장소 구성은 설치 안내(install.md), 에이전트용 사용 지침(SKILL.md), 상호작용 스킬(interaction-skills), 도메인 스킬 폴더, 테스트, MCP 문서로 나뉜다.
- 제어 단위는 DOM과 JS 실행 수준이며, 스크린샷 기반 데스크톱 제어와는 범위가 다르다.

### 적용 방법
- 고정 도구 표면이 특정 사이트 패턴을 감당하지 못할 때, 에이전트가 helper를 작성하고 검증하는 방식의 장단점을 비교 실험 설계로 옮겨볼 수 있다.
- 도메인별 스킬 축적은 사이트 지식을 문서로 남기는 절차로 이식할 수 있다. 다만 축적된 스킬이 항상 정확하다는 보장은 없으므로 검증 절차가 필요하다.
- 개인 로그인 세션을 쓰는 경우 원격 측정 설정과 클라우드 연동 여부를 설치 전에 명시적으로 결정해야 한다.

### 근거와 한계
- 원문 일부 확인: GitHub 저장소 메인 페이지(소개, 설치 방식, 파일 구성, 라이선스 표기)를 읽었다. SKILL.md, install.md, 소스 코드는 열람하지 않았다.
- 기존 knowledge 기록(2026-07-04)에는 버전 0.1.4 Alpha, 별 수, Posthog 원격 측정 등이 적혀 있었다. 이번 메인 페이지 열람에서는 버전과 원격 측정 항목을 확인하지 못했으므로, 해당 기록은 재검증되지 않은 상태로 둔다.
- 라이선스 MIT 표기는 저장소 페이지에서 확인되었다. 파일 단위 세부 조건은 확인하지 않았다.
- 이 카드는 참고 자료이며, 이번 작업에서 설치·활성화하거나 Hermes 도구 체계에 도입하지 않았다. 현재 Hermes의 브라우저 도구와의 비교 결론은 별도 검토가 필요하다.

### 연결
- [code-as-agent-harness.md](code-as-agent-harness.md) — 에이전트가 코드를 작성해 도구를 확장하는 접근을 비교할 때 참고
- [agent-harness-technical-debt.md](agent-harness-technical-debt.md) — 자가 생성 helper가 누적시키는 유지보수 부채를 점검할 때 참고
- [meta-harness.md](meta-harness.md) — 하네스 자체를 조정하는 관점과 대조할 때 참고

## Hermes 관련성

DOM/CDP 기반 브라우저 자동화와 고정 도구 표면의 trade-off를 비교할 수 있다. 현재 Hermes browser/computer-use 기능과 겹치는 범위가 있어 설치·활성화 후보로 해석하지 않습니다.
