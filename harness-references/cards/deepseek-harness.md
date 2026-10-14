# DeepSeek Harness

- 원문: https://github.com/deepseek-ai/deepseek-harness
- 출처 시점: 사용자 링크 제공 확인 2026-08-12 (KST, 내부 증거); repository 직접 확인 2026-10-14.
- 주제: orchestration/workflow · skills/tools · 사례/구현
- 상태: 사용자 제공; `knowledge/references/github/deepseek-harness.md` 등록; 관련 JOB 조사·설계 산출물 확인. 채택·활성화와 무관.
- 권리: GitHub 페이지에 MIT license 표시 확인. 외부 원문·코드 미복사; 저장소 내 개별 third-party 조건은 별도.
- 정리 근거: 원문 일부 확인

## 자체 요약

DeepSeek가 공개한 dsh agent harness로 “Everything is a Plugin”을 설계 방향으로 내세우며, Cordis 기반 구성·도구·plugin 확장과 Web/Desktop 앱, 개발자 문서를 포함하는 대규모 구현 사례다. README는 developer preview 및 compatibility-breaking change 가능성을 알린다.

## 상세 정리
### 핵심 주장
DeepSeek Harness(dsh)는 "모든 것은 플러그인(Everything is a Plugin)"을 설계 원칙으로 내세운 오픈소스 에이전트 하네스다. README 기준으로 기능은 플러그인 구조 위에 올라가며, 조합 기반은 Cordis라는 프레임워크다. 프로젝트는 developer preview 단계이며, 호환성을 깨는 변경이 있을 수 있다고 명시한다. 즉 이 저장소의 핵심 주장은 "하네스의 기능 단위를 플러그인으로 분리하면 확장성과 조립 가능성이 높아진다"는 설계 방향이다.

### 구조와 패턴
README에서 확인된 구조적 요소는 다음과 같다. 첫째, 플러그인 경계가 기본 단위다. 둘째, Cordis 기반의 조립(composition) 층이 플러그인들을 묶는다. 셋째, 웹 UI 실행과 데스크톱 빌드가 같은 코어를 공유하는 것으로 보인다(Make 타겟으로 Web과 Desktop을 구분). 넷째, 저장소 안에 사용자 문서, 개발 가이드, 아키텍처 문서, 에이전트용 지침 파일(AGENTS.md)이 함께 있다. 이 구성은 "코어는 얇게, 기능은 플러그인으로" 나누는 패턴의 실제 배치를 보여 준다. 다만 아키텍처 문서 본문은 이번에 열지 않았으므로 내부 계약의 세부는 확인하지 못했다.

### 적용 방법
Hermes와 비교할 때 가장 실용적인 관점은 플러그인 경계다. 도구, 메모리, 실행 환경, UI 같은 기능을 어디서 끊어 등록하고, 호스트가 어떤 능력(capability)을 플러그인에 부여하는지 확인하면 된다. 참조용으로 쓸 때는 이 저장소의 아키텍처 문서를 먼저 읽고, 플러그인 등록 인터페이스를 Hermes의 플러그인 작성 방식과 나란히 놓고 비교하는 것이 좋다. 채택 여부는 별도 검토 대상이며, 이 digest는 도입 근거가 아니다.

### 근거와 한계
근거는 GitHub 저장소 페이지와 raw README다. 저장소에는 커밋이 2만 건 이상 있고 MIT 라이선스가 표시되어 있다. 그러나 README가 명시하듯 아직 developer preview이므로, 현재 구조가 안정적이라고 볼 수 없다. 보안 안내(SAFETY.md), 아키텍처 문서, 개발 가이드, 제3자 의존성 고지는 이번에 읽지 않았다. 따라서 실행 보안, 호스트 요구사항, 제3자 라이선스 조건은 확인되지 않은 상태다. 이 저장소를 실행하기 전에는 보안 안내를 먼저 검토해야 한다.

### 연결
- [code-as-agent-harness.md](code-as-agent-harness.md) — 하네스의 기능을 코드 단위로 구성하는 접근과 비교할 수 있다.
- [meta-harness.md](meta-harness.md) — 하네스를 다시 하네스로 조립하는 상위 구조 논의와 연결된다.
- [agent-harness-technical-debt.md](agent-harness-technical-debt.md) — 플러그인 확장이 누적시키는 기술 부채를 함께 점검하는 데 쓴다.

## Hermes 관련성

plugin 경계, capability 조립, 실제 프로젝트의 architecture 문서를 비교할 수 있다. Hermes 시스템 전반에 도입하거나 호환된다고 단정할 수 없으며, runtime 보안·라이선스·호스트 요구사항을 독립 검토해야 합니다.
