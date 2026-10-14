# Apache Maka: Agent Graph and stream scheduling draft

- 원문 (영어): https://github.com/apache/maka/blob/main/docs/architecture/agent-graph-stream-scheduling-draft.md
- 원문 (중국어): https://github.com/apache/maka/blob/main/docs/architecture/agent-graph-stream-scheduling-draft.zh-CN.md
- 저장소: https://github.com/apache/maka (사용자가 저장소 링크로 처음 제공)
- 출처 시점: live draft; retrieved 2026-10-14. 원문 링크 제공 2026-10-13 (KST, 내부 증거).
- 주제: orchestration/workflow · evaluation/observability · case/implementation
- 상태: 사용자 제공 링크; 현행 knowledge registration/활용 확인되지 않음. 초안 문서로 기록.
- 권리: Apache project repository; file-level license/NOTICE applicability not checked. 내용 미복사.
- 정리 근거: 원문 일부 확인

## 자체 요약

Apache Maka의 agent graph와 stream scheduling architecture draft로, graph scheduling과 runtime events/child sessions 관계를 논한다. 문서 자체가 draft이므로 변경 가능성이 있으며, normative/stable contract로 해석하면 안 됩니다.

## 상세 정리

### 핵심 주장
- 여러 에이전트의 의존적이고 동적으로 늘어나는 작업을, 새 에이전트 런타임을 만들지 않고 그래프로 조정할 수 있다는 것이 문서의 주장이다. 그래프는 '두 번째 런타임'이 아니라 기존 실행 사실 위에 놓인 내구성 있는 스케줄이라고 정의한다.
- 자식 세션(child Session)은 operator의 컨테이너, 세션 안의 AgentRun은 한 번의 activation, 커밋된 RuntimeEvent는 불변 스트림 레코드로 취급한다. 부분 청크나 프로세스 내부 콜백은 내구성 있는 데이터 흐름 사실로 쓰지 않는다.
- 준비 상태(readiness)는 라우트와 정책에서 결정적으로 계산되는 투영(projection)이고, 실제 실행 허가는 SQLite의 claim 행으로 한 번만 부여한다. 그래서 같은 intent를 다시 계산해도 두 번 실행되지 않는다.
- 메인 에이전트는 데이터 경로 옆에서 감독자 역할만 한다. 관찰·스케줄 변경은 하지만 일반 레코드 전달이 승인을 기다리지는 않는다.
- '스케줄이 비었다'는 것과 '런타임이 정지했다'는 것을 구분한다. 실행 가능한 항목이 없다고 그래프 작업이 끝난 것은 아니라고 명시한다.

### 구조와 패턴
- 제어 평면(SQLite 기반 스케줄 리비전, 토폴로지, claim, supervisor wake)과 데이터 평면(기존 Session·Runtime 이벤트 로그)을 분리한다.
- 식별자 계층은 root Session → graph → operator → child Session → activation/AgentRun → RuntimeEvent로 이어지며, 후속 작업은 같은 Session을 재사용하고 매번 새 Turn과 Run을 받는다.
- 장 전체가 가정하는 범위 밖도 명시된다. 임의의 순환 워크플로, 분산 실행, 그래프 전체 자원 최적화, 시각적 워크플로 편집기는 다루지 않는다.

### 적용 방법
- 다중 에이전트 작업에서 '실행 사실'과 '조정 상태'를 다른 저장소·다른 식별자로 나누는 설계를 검토할 수 있다.
- 레코드 전달을 승인 대기와 분리하고, 감독 판단은 별도 턴으로 기록하는 방식이 참고할 만하다.
- 중복 실행 방지는 재계산 로직이 아니라 단일 원자적 claim 행으로 보장하는 식이 설계 기준으로 제시된다.

### 근거와 한계
- 원문 일부 확인: GitHub 문서 페이지의 앞부분(개요, 식별자 모델, 두 평면 구조)과 끝부분(참조 코드 경로, 결론)을 읽었다. 중간 장 대부분은 추출에서 생략되어 확인하지 못했다.
- 문서 상태는 draft이며 구현 상태는 current로 표시되어 있다. 문서는 변경될 수 있고, 표준이나 안정 계약으로 해석하면 안 된다.
- 문서가 말하는 검증 날짜(2026-08-23)와 이번 열람 시점 사이의 변경 여부는 확인하지 않았다.
- Apache 저장소의 라이선스 적용 범위는 확인하지 않았다. 내용을 복사하지 않고 요약만 기록한다.
- 이 문서의 구현 성능이나 운영 결과는 확인하지 못했다.

### 연결
- [langgraph-human-approval.md](langgraph-human-approval.md) — 그래프 상태와 사람 승인 지점을 다루는 다른 설계와 비교할 때 참고
- [graph-of-thoughts.md](graph-of-thoughts.md) — 그래프를 추론 구조로 쓰는 접근과 대비할 때 참고
- [multi-agent-orchestration-patterns.md](multi-agent-orchestration-patterns.md) — 조정 패턴 전반과 교차 확인용

## Hermes 관련성

그래프형 multi-agent workflow와 scheduling boundary의 현재 설계 논의 비교에 유용하다. 초안 상태의 제안이며 Hermes 구현·채택 또는 성능 검증 결과가 아닙니다.
