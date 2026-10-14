# typesafe-ai/skills — skills repository

- Source: https://github.com/typesafe-ai/skills
- Alternate sources: https://docs.typesafe.ai (공식 문서, `llms.txt` 포함). 사용자가 첨부한 스킬 문서에 이 문서 사이트의 개념·cookbook·SDK 페이지 링크 23개가 들어 있어 개별 카드 대신 이 카드의 대체 출처로 묶음.
- Topics: skills-tools, evaluation-observability-security, case-implementation
- Publication date: unknown / not independently verified
- User-provided: True; date: 2026-09-20
- Knowledge registration: True; evidence: knowledge/references/llm-course/New-Models/jev-llm.md; not indexed in reference index
- Source confirmation: 보존된 사용자 메시지 시각을 서울 날짜로 환산해 2026-09-20 제공을 확인함. 같은 내용의 반복 저장은 한 제공 사건으로 묶음. 등록 파일은 확인했으나 색인 등재는 미확인.
- Utilization: JEV 관련 사용자 검토 요청과 연결된 스킬 저장소. 링크와 등록 파일을 확인했으나 구체적인 Hermes/JEv 운영 채택 증거는 이 자료만으로 단정하지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 지식 기록 대조 + 원문 일부 확인

## Independent summary and scope

JEV 관련 사용자 검토 요청과 연결된 스킬 저장소. 링크와 등록 파일을 확인했으나 구체적인 Hermes/JEv 운영 채택 증거는 이 자료만으로 단정하지 않음.

## 상세 정리

### 핵심 주장
1. TypeSafe의 Jev는 에이전트가 비싼 작업을 시작하기 전에 "다음에 무엇을 할지"를 작은 판단 호출로 정하게 하는 API다. 응답은 자유 텍스트가 아니라 타입이 있는 값으로 온다. 선택지 중 하나(choice), 점수(score), 판단 보류(null) 세 가지다.
2. 이 저장소의 공식 스킬은 에이전트에게 Jev API 쓰는 법을 가르친다. 판단 결과를 실제 행동으로 바꾸는 라우터·레시피·에이전트 정책은 별도 커뮤니티 플레이북 저장소가 맡는다. 두 구성 요소를 구분해야 한다.
3. SDK를 import했거나 API 호출이 한 번 성공했다고 통합이 끝난 것이 아니다. 실제 작업 중에 에이전트가 라우터를 호출했다는 증거가 있어야 완료로 본다.

### 구조와 패턴
- 문서 사이트는 primitive(choice·score·null), 조합 패턴(composite scoring, fan-out), confidence, cookbook(분류·재정렬·인용 검사·함수 호출 등), Python/JavaScript SDK로 구성된다. 에이전트용 `llms.txt`도 있다.
- 사용자가 첨부한 설치 지시문은 여섯 단계로 이루어진다. ① 작업 맥락에서 Jev가 도움될 상황 3개 식별 ② 실행 환경(에이전트 종류·OS·터미널/파일/네트워크 권한) 판별 ③ 공식 문서와 플레이북 확인 ④ 오프라인 dry run 후 API 키를 비공개 환경변수로 설정해 실호출 확인 ⑤ 프로젝트 지침 파일(CLAUDE.md, AGENTS.md 등)에 호출 조건 추가 ⑥ 세 가지 시험으로 증명.
- 호출 조건 예: 큰 브라우저 조사, 실패한 방법 반복, 도구·스킬 여러 개 로드, 하위 에이전트 생성, 실행 경로 선택, 결과가 큰 행동 제안. 단순 답변·결정적 계산·일상적 파일 수정에는 호출하지 않는다.

### 적용 방법
- 처음에는 shadow 모드로 판단만 기록하고, 결정 로그를 본 뒤 active 전환을 정한다.
- 판단 호출에는 비밀 정보 없이 압축한 상태만 넘긴다. API 키는 대화에 붙여 넣거나 출력·커밋하지 않는다.
- 사용자가 우회를 명시하면 호출하지 않고, 되돌릴 수 없는 행동은 판단 결과와 무관하게 사람 확인을 거친다.
- 시험 세 가지: 호출을 건너뛰어야 할 단순 질문, 실제 경로 선택이 있는 작업, 라우터가 방법 변경을 권할 만한 반복 실패. 에이전트 행동과 라우터 로그를 함께 확인한다.
- 지침 파일에 문장을 넣는 것만으로 호출이 보장되지 않는다. 에이전트가 실제로 실행할 수 있는 도구 호출과 연결해야 한다.

### 근거와 한계
- 정리의 중심은 사용자가 제공한 설치 지시문과 저장소·문서 사이트 목차다. 판단 정확도, 확률 보정, 비용은 확인하지 않았다.
- 외부 유료 API에 의존하므로 서비스가 바뀌면 절차도 바뀐다. 설치 명령은 현재 QUICKSTART를 다시 확인한다.

### 연결
- [OpenAI skills concept](openai-skills-concept.md) — 스킬의 일반 개념과 MCP와의 역할 구분
- [OpenAI build skills](openai-build-skills.md) — 스킬의 위치와 배포 방식
- [Vercel AGENTS.md vs skills](vercel-agents-md-skills-evals.md) — 스킬 발동의 신뢰성 문제

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
