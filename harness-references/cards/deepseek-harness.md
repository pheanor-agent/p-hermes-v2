# DeepSeek Harness

- 원문: https://github.com/deepseek-ai/deepseek-harness
- 출처 시점: 사용자 링크 제공 확인 2026-08-12 (KST, 내부 증거); repository 직접 확인 2026-10-14.
- 주제: orchestration/workflow · skills/tools · 사례/구현
- 상태: 사용자 제공; `knowledge/references/github/deepseek-harness.md` 등록; 관련 JOB 조사·설계 산출물 확인. 채택·활성화와 무관.
- 권리: GitHub 페이지에 MIT license 표시 확인. 외부 원문·코드 미복사; 저장소 내 개별 third-party 조건은 별도.

## 자체 요약

DeepSeek가 공개한 dsh agent harness로 “Everything is a Plugin”을 설계 방향으로 내세우며, Cordis 기반 구성·도구·plugin 확장과 Web/Desktop 앱, 개발자 문서를 포함하는 대규모 구현 사례다. README는 developer preview 및 compatibility-breaking change 가능성을 알린다.

## Hermes 관련성

plugin 경계, capability 조립, 실제 프로젝트의 architecture 문서를 비교할 수 있다. Hermes 시스템 전반에 도입하거나 호환된다고 단정할 수 없으며, runtime 보안·라이선스·호스트 요구사항을 독립 검토해야 합니다.
