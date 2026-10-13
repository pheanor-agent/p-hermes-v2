# Effective harnesses for long-running agents

- 원문: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 출처 시점: 원문 추출본에서 게시일을 확인하지 못함; 직접 확인 2026-10-14.
- 주제: 개요 · orchestration/workflow · context/memory · 사례
- 상태: 요청 필수 핵심 자료; 제공 여부와 references 등록 여부는 이번 원천 검토에서 확인되지 않음. 패턴 참고, 도입 아님.
- 권리: 확인되지 않음. 자체 요약·링크만; 전문 미보존.

## 자체 요약

긴 작업이 여러 context window와 session을 넘을 때 compaction만으로는 부족할 수 있다고 설명한다. 첫 session은 요구사항·초기 환경·실행 스크립트를 준비하는 initializer로, 후속은 한 번에 작은 단위의 기능을 구현하고 구조화된 progress artifact와 깨끗한 작업 상태를 남기는 coding agent로 나눈다. feature list와 git history를 함께 handoff 자료로 사용한다.

## Hermes 관련성

세션 간 상태 전달, 점진적 요구사항 충족, clean handoff를 설계할 때 참고할 수 있다. Anthropic의 Claude Agent SDK 및 웹앱 개발 조건의 사례이며 Hermes worker/JOB 절차와 동등하거나 운영 적용되었다는 뜻은 아닙니다.
