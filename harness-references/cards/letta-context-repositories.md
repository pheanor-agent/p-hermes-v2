# Introducing Context Repositories: Git-based Memory for Coding Agents

- 원문: https://www.letta.com/blog/context-repositories
- 출처 시점: 2026-02-12 (내부 reference 카드의 원문 표기); 사용자 제공 링크 확인 2026-06-09 (KST).
- 주제: context/memory/knowledge · skills/tools · 사례
- 상태: 사용자 제공; `knowledge/references/memory/letta-context-repositories.md` 등록; 설계 비교 참고, Hermes memory 시스템 도입 아님.
- 권리: 미확인. 자체 요약·링크만; 원문 미보존.
- 정리 근거: 원문 일부 확인

## 자체 요약

Letta Code의 agent context를 로컬 파일시스템과 Git으로 version 관리하고, context 정리·검색·재구성에 terminal과 subagent를 이용하는 접근을 설명한다. 디렉터리 구조와 frontmatter를 내비게이션/점진 공개에 활용한다.

## 상세 정리

### 핵심 주장
1. 에이전트 기억을 도구 호출로만 다루던 방식(MemGPT식 메모리 도구, 가상 파일 시스템)을 넘어, 에이전트가 자기 문맥을 프로그램으로 직접 관리하게 한다.
2. 문맥을 git 저장소로 두면 모든 기억 변경이 커밋 메시지와 함께 버전 관리된다.
3. 파일은 사람과 에이전트가 함께 다루는 단위이므로, 셸 명령과 스크립트로 기억을 일괄 처리할 수 있다.

### 구조와 패턴
- Letta Code 에이전트는 서버의 기억을 로컬 파일시스템에 복제해 쓴다. 로컬 사본은 서버와 동기화된다.
- 파일 트리와 frontmatter로 점진적 공개(progressive disclosure)를 구현한다. 먼저 구조를 보고 필요한 파일만 연다.
- 여러 하위 에이전트가 같은 저장소에서 작업하고, 충돌은 표준 git 연산으로 정리한다. 원문은 이를 분할 정복식 학습으로 설명한다.

### 적용 방법
- 기억 변경을 커밋 단위로 남기면 잘못 학습된 내용을 되돌리는 절차가 명확해진다.
- 파일 트리로 구조를 먼저 보여 주는 방식은 Hermes의 메모리와 스킬 설계 비교에 쓸 수 있다.
- 여러 에이전트가 같은 기억을 고치면 충돌 해결 규칙이 없을 때 혼란이 커진다.

### 근거와 한계
- 제품 블로그 글이며 기억 품질이나 작업 성공률의 정량 비교는 없다.
- 원문 앞부분의 구조 설명 위주로 확인했다. 실제 저장소 형식과 명령은 공식 문서에서 다시 확인해야 한다.
- "에이전트가 기억을 스스로 재작성한다"는 주장은 사람 검토와 함께 읽어야 한다.
- Letta 제품의 설계 소개이며 Hermes의 메모리 도입 근거가 아니다.

### 연결
- [Google context-aware multi-agent](google-context-aware-multi-agent.md) — 문맥을 원천과 뷰로 나누는 설계
- [MemGPT context OS](memgpt-context-os.md) — 계층형 메모리의 원조 설계
- [Hermes official docs](hermes-official-docs.md) — 메모리와 스킬의 역할 분담

## Hermes 관련성

파일 기반 장기 기억의 변경 이력·동시성·progressive disclosure를 비교할 수 있다. 이것은 Letta 구현의 설계 소개이며 Hermes knowledge authority, 개인정보 경계, 운영 승인에 대한 대체 근거는 아닙니다.
