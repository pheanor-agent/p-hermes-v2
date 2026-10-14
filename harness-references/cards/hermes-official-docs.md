# Hermes: 하네스·작업 흐름·컨텍스트 공식 문서

- 시작점: https://hermes-agent.nousresearch.com/docs/
- 요청에서 직접 제공된 문서: [Loops](https://hermes-agent.nousresearch.com/docs/user-guide/features/loops), [Context files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files), [Session storage](https://hermes-agent.nousresearch.com/docs/developer-guide/session-storage), [Prompt assembly](https://hermes-agent.nousresearch.com/docs/developer-guide/prompt-assembly), [Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory).
- 출처 시점: 공식 문서; 사용자 링크 제공 확인 2026-10-06 (KST; session log evidence).
- 주제: orchestration/workflow · context/memory/knowledge · skills/tools.
- 상태: Hermes 공식 문서 링크; 이번 조사에서 각 문서 본문 전수 다운로드·검증은 하지 않음. Hermes 기능의 현행 동작은 문서와 현재 runtime을 구분해야 함.
- 권리: 별도 라이선스 검토 안 함; 요약·링크만, 원문 미보존.
- 정리 근거: 원문 전체 확인

## 자체 요약

Loops, context files, session persistence, prompt construction 및 memory는 하네스의 상호 연결된 층을 설명하는 공식 제품 문서다. 이 URL들은 같은 문서가 아니라 개별 기능 설명으로 계속 갱신될 수 있다.

## 상세 정리

### 핵심 주장
1. Hermes는 경험에서 스킬을 만들고, 사용 중 개선하며, 세션을 넘어 사용자 모델을 쌓는 자율 에이전트로 소개된다. 코딩 보조 도구나 단일 API 챗봇 래퍼가 아니라는 점을 앞세운다.
2. 설치는 Windows·macOS 데스크톱 설치기와 명령줄 설치 스크립트로 나뉜다. 설치 후 `hermes setup --portal` 한 번의 OAuth로 모델과 도구 4종(웹 검색, 이미지 생성, TTS, 브라우저)을 함께 연결한다고 안내한다.
3. 실행 위치는 저가 VPS, GPU 클러스터, 유휴 시 비용이 거의 없는 서버리스 인프라(Daytona, Modal)까지 열려 있고, 메신저로 원격 에이전트와 대화할 수 있다.

### 구조와 패턴
- 랜딩 페이지는 설치, 빠른 시작, 설정, 메신저 게이트웨이, 봇 모드, 도구, 메모리, 스킬, MCP, 음성, 컨텍스트 파일, 보안, FAQ 순으로 주제를 나열한다.
- 메모리는 세션을 넘어 자라는 지속 메모리, 스킬은 에이전트가 만들고 재사용하는 절차적 메모리로 구분된다.
- 컨텍스트 파일은 모든 대화를 형성하는 프로젝트 문맥으로 소개되며, 문서는 /docs/llms.txt와 /docs/llms-full.txt로도 제공된다.

### 적용 방법
- 설치 소유권·데이터 위치는 설치 문서, 설정 파일·모델·provider는 설정 문서로 나뉘므로 운영 지침에서도 둘을 구분해 적는다.
- 메모리(사실 축적)와 스킬(절차 재사용)을 나누는 기준으로 이 두 정의를 쓴다. 이는 정리자의 적용안이며 원문의 권고가 아니다.

### 근거와 한계
- 원문은 랜딩 페이지 한 장이다. 링크된 하위 문서(Loops, Context files, Session storage, Prompt assembly, Memory) 본문은 포함되지 않아 세부 동작은 확인하지 못했다.
- 자기 소개 문구(자율 에이전트, 자가 개선)는 제품 측 주장이며 독립 검증이 아니다. 로컬 설치의 실측과 구분한다.
- 플랫폼 지원 범위와 설치 세부는 별도 문서로 나뉘어 있어 이 원문만으로는 확인되지 않는다.

### 연결
- [openai-skills-concept.md](openai-skills-concept.md) — 스킬을 워크플로 층으로 보는 다른 제공자의 설계
- [vercel-agents-md-skills-evals.md](vercel-agents-md-skills-evals.md) — 상시 문맥과 온디맨드 스킬의 비교
- [letta-context-repositories.md](letta-context-repositories.md) — 메모리를 파일로 관리하는 다른 접근

## Hermes 관련성

이 자료집의 연구/외부 구현과 Hermes 자체 기능을 비교하기 위한 현행 공식 문서 진입점이다. 공개한 내용은 문서의 요약이며, local worker/distribution에만 있는 동작·설정까지 일반 Hermes에 있다고 주장하지 않습니다.
