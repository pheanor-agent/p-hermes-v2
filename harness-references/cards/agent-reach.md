# Agent Reach

- 원문: https://github.com/Panniantong/agent-reach
- 출처 시점: user-provided project link observed in 2026 conversation; current repository page surfaced 2026-10-14.
- 주제: skills/tools · security · case/implementation
- 상태: user-provided in a harness-adjacent context; knowledge registration/utilization not verified. No installation or configuration.
- 권리: GitHub search listing describes MIT; repository-specific license was not independently reviewed in this task.
- 정리 근거: 원문 일부 확인

## 자체 요약

An agent capability layer presented as selecting, installing, health-checking and routing among upstream information retrieval tools, with a skill as its agent-facing discovery mechanism. Project documentation indicates some integrations require authenticated accounts or explicit setup.

## 상세 정리

### 핵심 주장
- Agent Reach는 에이전트에게 웹 정보 접근 능력을 한 번에 붙이는 명령행 도구 묶음이다. 여러 플랫폼(웹 페이지, 영상 자막, RSS, 검색, 개발 플랫폼, 소셜 플랫폼 등)에 대해 접근 경로를 고르고, 점검하고, 필요하면 대체 경로로 바꾸는 역할을 한다고 저장소가 설명한다.
- 플랫폼마다 접근 경로에 "기본"과 "대체"를 두는 다중 백엔드 구조를 강조한다. 특정 경로가 막히면 다른 경로로 바꾸는 것이 목표다.
- 진단 명령으로 연결 상태를 확인할 수 있다고 소개한다. 설치와 설정의 상당 부분을 에이전트가 사용자를 대신해 수행하도록 설계되어 있다.

### 구조와 패턴
- 플랫폼별 채널 파일을 나눈 구조다. 특정 채널을 신뢰하지 않으면 해당 파일만 교체해 다른 채널에 영향을 주지 않는다고 적혀 있다.
- 인증이 필요한 플랫폼은 로컬 쿠키나 로그인 상태를 쓰며, 저장소는 이 정보가 로컬에만 남는다고 명시한다.
- 기능은 "설치 직후 쓸 수 있는 것"과 "설정 후 열리는 것"으로 나뉜다. 상당수 플랫폼은 로그인 없이 쓸 수 없다.
- 설치 명령은 기본적으로 환경을 읽기만 하고, 시스템 패키지 설치나 설정 쓰기는 명시적 인자가 있을 때만 수행한다고 안내한다. 드라이런 옵션으로 실제 변경 없이 계획만 볼 수 있다고 적혀 있다.
- 제거 절차도 문서화되어 있다. 설정 디렉터리와 스킬 파일, 메시지 도구의 MCP 설정을 지우며, 재설치를 위해 토큰만 남기는 옵션도 있다고 설명한다. 설치와 제거의 범위를 나눠 적어 둔 점은 운영 검토에 참고할 만하다.
- 접근 실패 시 상태 점검이 어느 채널이 살아 있는지 알려 주는 것이 핵심 기능으로 제시된다.

### 적용 방법
- 에이전트의 도구 표면을 설계할 때 참고할 만하다. 능력을 한 번에 여는 대신 플랫폼별 상태 점검과 대체 경로를 두는 구조가 참고점이다.
- 도입 전에 설치 명령이 무엇을 바꾸는지 드라이런으로 확인하는 절차가 필요하다. 설치 안내문을 호스트 변경 승인으로 읽으면 안 된다.
- 쿠키 기반 접근은 전용 계정을 쓰도록 저장소가 권고하며, 계정 제한 위험도 함께 기록해야 한다.
- 채택 여부를 정할 때는 기능 목록보다 각 채널의 인증 요건, 데이터 보관 위치, 제거 방법을 먼저 표로 정리하는 편이 안전하다.

### 근거와 한계
- 원문 일부 확인: 저장소 홈의 앞부분과 뒷부분만 열람했다. 설치 세부 절차, 테스트 결과, 채널별 상세 동작은 확인하지 않았다.
- 별 수, 포크 수, 후원 표시는 저장소 페이지의 주장일 뿐 독립 확인이 아니다. 라이선스는 페이지 표시 기준이며 파일별 조건은 확인하지 않았다.
- 외부 플랫폼 접근은 상대 측 정책과 차단에 따라 동작이 달라진다. 저장소 설명대로 대체 경로가 실제로 작동하는지는 실행하지 않았다.

### 연결
- [agent-skills-standard.md](agent-skills-standard.md) — 도구 능력을 에이전트가 발견하는 방식이 스킬 형식과 같은 질문을 던진다.
- [browser-harness.md](browser-harness.md) — 브라우저 기반 접근과 도구 표면 설계를 비교하기 좋다.
- [agent-harness-technical-debt.md](agent-harness-technical-debt.md) — 도구 표면이 하네스 구성요소로 어떻게 분류되는지 보여준다.

## Hermes 관련성

Tool surface and capability discovery are part of harness design, so this is an adjacent case. It is not a general agent runtime or workflow engine. Avoid interpreting its installation instructions as authorization to modify a Hermes host.
