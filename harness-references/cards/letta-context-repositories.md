# Introducing Context Repositories: Git-based Memory for Coding Agents

- 원문: https://www.letta.com/blog/context-repositories
- 출처 시점: 2026-02-12 (내부 reference 카드의 원문 표기); 사용자 제공 링크 확인 2026-06-09 (KST).
- 주제: context/memory/knowledge · skills/tools · 사례
- 상태: 사용자 제공; `knowledge/references/memory/letta-context-repositories.md` 등록; 설계 비교 참고, Hermes memory 시스템 도입 아님.
- 권리: 미확인. 자체 요약·링크만; 원문 미보존.

## 자체 요약

Letta Code의 agent context를 로컬 파일시스템과 Git으로 version 관리하고, context 정리·검색·재구성에 terminal과 subagent를 이용하는 접근을 설명한다. 디렉터리 구조와 frontmatter를 내비게이션/점진 공개에 활용한다.

## Hermes 관련성

파일 기반 장기 기억의 변경 이력·동시성·progressive disclosure를 비교할 수 있다. 이것은 Letta 구현의 설계 소개이며 Hermes knowledge authority, 개인정보 경계, 운영 승인에 대한 대체 근거는 아닙니다.
