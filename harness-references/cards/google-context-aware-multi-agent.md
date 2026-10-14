# Architecting efficient context-aware multi-agent framework for production

- 원문: https://developers.googleblog.com/architecting-efficient-context-aware-multi-agent-framework-for-production
- 출처 시점: 2025-12-04 (Google Developers Blog 검색 결과 표기); 사용자 제공 링크 확인 2026-06-02 (KST).
- 주제: orchestration/workflow · context/memory/knowledge · 사례/구현
- 상태: 사용자 제공 링크; 지식 references 등록 확인되지 않음. ADK 설계 사례, Hermes에서 미도입.
- 권리: 미확인. 자체 요약·링크만; 전문 미보존.
- 정리 근거: 원문 일부 확인

## 자체 요약

Google ADK에서 context engineering을 시스템·lifecycle·제약을 가진 first-class concern으로 다루며, session 저장 상태와 model에 제시하는 working context를 구분하는 구조를 설명한다. 검색 결과는 context processing과 효율적 multi-agent 운영을 강조한다.

## 상세 정리
### 핵심 주장
1. 긴 작업을 하는 에이전트에서 병목은 모델 성능보다 "문맥"이다. 기록·도구 출력·문서·중간 추론이 계속 쌓이기 때문이다.
2. 모든 내용을 한 프롬프트에 몰아넣는 방식은 세 가지로 무너진다. 비용과 지연이 커지고, 중요한 정보가 묻히며("lost in the middle"), 결국 창의 한계를 넘는다.
3. 큰 창을 쓰는 것만으로는 해결되지 않으므로, 문맥을 크기가 아니라 구조로 다뤄야 한다는 것이 핵심이다.

### 구조와 패턴
- 저자들은 문맥을 "가변 문자열 버퍼"가 아니라 "더 풍부한 상태 시스템에서 컴파일된 뷰"로 본다.
- 원천(source)은 세션, 메모리, 아티팩트(파일)다. 이것이 전체 상태다.
- 흐름과 프로세서는 컴파일러 파이프라인처럼 원천을 여러 단계로 변환한다.
- 작업 문맥(working context)은 이번 호출에 LLM으로 보내는 컴파일 결과다.
- 이 구조는 Google Agent Development Kit(ADK)의 문맥 계층으로 구현되었다고 소개된다.

### 적용 방법
- 문맥을 쌓기 전에 "무엇을 원천으로 보관하고, 무엇을 이번 호출에 보낼지"를 나눠 설계한다.
- 도구 출력이 길면 원천에는 남기고 작업 문맥에는 요약이나 참조만 넣는 식의 분리를 검토한다.
- 여러 에이전트가 같은 원천을 보더라도 각자의 작업 문맥을 따로 컴파일하는 방식이 가능하다.

### 근거와 한계
- 원문은 제품 팀의 설계 설명이다. 비용·지연 개선 수치는 이 정리 범위에서 확인하지 못했다.
- 원문이 길어 본 정리는 앞부분의 문제 제기와 설계 개념 위주로 확인했다. 세부 API와 구현 세부는 원문에서 확인해야 한다.
- ADK에 특화된 용어가 많으므로 Hermes에 옮길 때는 개념만 가져오는 것이 안전하다.

- 원문의 핵심 구분은 "원천 상태"와 "이번 호출에 보는 뷰"의 분리다. 긴 작업에서 원천은 계속 기록하고, 뷰만 호출마다 새로 만든다는 뜻이다.
- 실패 점검으로는 긴 이력을 넣은 경우와 뷰만 넣은 경우의 답을 같은 과제에서 비교하는 것이 확인 방법이 된다.

### 연결
- [Letta context repositories](letta-context-repositories.md) — 문맥을 파일과 git으로 관리하는 다른 접근
- [MemGPT context OS](memgpt-context-os.md) — 계층형 메모리로 문맥 한계를 넘는 원조 설계
- [Context engineering survey](context-engineering-survey.md) — 문맥 공학 전반의 정리

## Hermes 관련성

기록의 authority와 호출별 context view를 분리하는 설계 토론에 참고할 수 있다. ADK의 구현을 Hermes에 그대로 이식해야 한다는 의미는 아닙니다.
