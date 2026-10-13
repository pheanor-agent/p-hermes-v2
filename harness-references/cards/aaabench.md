# AAABench

- 원문: https://github.com/ukanwat/aaabench
- 출처 시점: 기존 reference에서 조사 commit `fb4eee22c45c72aa83b491b7018dc1db614acfad`, 2026-08-14 기록; 현재 upstream 재검증은 하지 않음.
- 주제: orchestration/workflow · evaluation · 사례/구현
- 상태: `knowledge/references/github/aaabench.md` 등록; 기존 검토는 조건부 reference, 미설치·미실행.
- 권리: 기존 카드에서 저장소 코드 MIT라 기록했으나 외부 asset·plugin·콘텐츠 권리는 개별 확인 필요. 이 자료집은 코드·원문 미복사.

## 자체 요약

Unreal Engine Editor를 MCP로 제어해 coding agent가 장기 open-world game 제작을 수행하는 benchmark/harness 사례다. agent runner, session resume, crash recovery, viewport 검사와 제작 단계 gate를 포함한다고 기존 source review가 기록한다.

## Hermes 관련성

agent의 장기 실행·도구 오류 복구·화면 기반 검증이 결합된 도메인별 사례다. Unreal 환경/호스트 호환성은 별도 검토 대상이며 일반 Hermes 사용자가 바로 실행 가능한 예제가 아닙니다.
