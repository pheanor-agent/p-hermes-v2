# browser-harness (browser-use)

- 원문: https://github.com/browser-use/browser-harness
- 출처 시점: 사용자 링크 제공 확인 2026-07-04 (KST); 기존 knowledge 카드 검토 2026-07-04.
- 주제: skills/tools · security · 사례/구현
- 상태: `knowledge/references/github/browser-harness.md` 등록; 기존 평가는 미도입·참고. 현재 upstream 상태 재검증은 하지 않음.
- 권리: 기존 카드에 MIT라고 기록됐으나 이번 원문 재검증은 안 됨. 코드·원문 미복사.

## 자체 요약

Chrome DevTools Protocol을 통해 agent가 브라우저를 다루고, 실행 중 helper를 작성하거나 도메인 skill을 축적하는 구현 사례다. 기존 검토는 Alpha maturity, optional cloud/OAuth, PostHog telemetry를 위험으로 기록했다.

## Hermes 관련성

DOM/CDP 기반 브라우저 자동화와 고정 도구 표면의 trade-off를 비교할 수 있다. 현재 Hermes browser/computer-use 기능과 겹치는 범위가 있어 설치·활성화 후보로 해석하지 않습니다.
