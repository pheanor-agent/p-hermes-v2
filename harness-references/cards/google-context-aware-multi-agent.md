# Architecting efficient context-aware multi-agent framework for production

- 원문: https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production
- 출처 시점: 2025-12-04 (Google Developers Blog 검색 결과 표기); 사용자 제공 링크 확인 2026-06-02 (KST).
- 주제: orchestration/workflow · context/memory/knowledge · 사례/구현
- 상태: 사용자 제공 링크; 지식 references 등록 확인되지 않음. ADK 설계 사례, Hermes에서 미도입.
- 권리: 미확인. 자체 요약·링크만; 전문 미보존.

## 자체 요약

Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working context를 구분하는 구조를 설명한다. 검색 결과는 context processing과 효율적 multi-agent 운영을 강조한다.

## Hermes 관련성

기록의 authority와 호출별 context view를 분리하는 설계 토론에 참고할 수 있다. ADK의 구현을 Hermes에 그대로 이식해야 한다는 의미는 아닙니다.
