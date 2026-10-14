# codebase-memory-mcp — external read-only reference

- Source: https://github.com/DeusData/codebase-memory-mcp
- Alternate sources: none recorded
- Topics: context-memory-knowledge, skills-tools, evaluation-observability-security, case-implementation
- Publication date: unknown / not independently verified
- User-provided: unknown; date: unknown
- Knowledge registration: True; evidence: knowledge/references/github/codebase-memory-mcp.md
- Source confirmation: 지식 문서 확인; 사용자 제공 여부 및 활용 시점은 미확정
- Utilization: 코드베이스 그래프·MCP·증거 기반 배포에 관한 read-only 비교 자료. upstream 보안/성능 주장은 별도 검증 대상으로 남김.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 원문 일부 확인

## Independent summary and scope

코드베이스 그래프·MCP·증거 기반 배포에 관한 read-only 비교 자료. upstream 보안/성능 주장은 별도 검증 대상으로 남김.

## 상세 정리
### 핵심 주장
- 코드베이스를 지속 저장되는 지식 그래프로 색인하고, 에이전트가 MCP 도구로 그 그래프를 질의하게 하는 도구로 소개된다. 로컬에서 실행하는 것을 기본 모델로 한다.
- 저장소 소개는 빠른 색인과 토큰 사용 절감을 강조한다. 이는 업스트림의 주장이며 조건이 확인되지 않아 별도 검증이 필요하다.
- 참고 가치의 초점은 기능보다 배포 방식에 있다고 본다. 단일 네이티브 실행 파일, 릴리스 검증 체인, 설치·업데이트 수명주기, 공유 그래프 아티팩트가 그 대상이다.

### 구조와 패턴
- 구성 요소는 tree-sitter 기반 파싱(158개 언어), 일부 언어의 LSP 기반 의미 해석, SQLite 그래프 저장소, Cypher 유사 질의 계층, MCP stdio 서버, CLI, 로컬 시각화 UI, 파일 감시기, 계정 단위 조정 데몬으로 기록되어 있다.
- 팀 공유 아티팩트는 그래프 DB를 정리·압축해 저장소에 넣는 방식이다. 가져올 때 무결성을 검사하는 절차가 함께 설명된다.
- 릴리스는 플랫폼별 바이너리에 체크섬, 출처(provenance) 증명, SBOM, 서명, 보안 스캔 결과를 붙이는 형태로 설명된다.
- 보안 문서는 파일 읽기, 에이전트 설정 파일 쓰기, 백그라운드 프로세스 생성, 초기화 후의 릴리스 확인 네트워크 요청, 설치·업데이트 시의 네트워크 활동을 명시한다.

### 적용 방법
- 런타임 의존성이 무거운 환경에서는 단일 실행 파일과 소규모 자산 집합으로 배포하는 방식을 검토할 수 있다.
- 릴리스 매니페스트에 OS, 아키텍처, libc, 빌드 정체성을 명시하고, 설치(활성화)와 실행 바이너리를 분리해 롤백 경계를 둔다.
- 공유 그래프는 스냅샷 식별자, 스키마 버전, 소스 잠금, 증거 호환성 검사를 갖춘 경우에만 쓴다.
- 데몬형 세션 조정은 인덱스 작업의 소유권, 잠금 충돌, 취소와 재개에 참고가 된다. 같은 빌드와 캐시 루트인지 엄격히 확인해야 한다.
- 자동 설정 쓰기, 백그라운드 업데이트 확인, 검증 없는 바이너리, 업스트림 성능 주장은 기본 도입 대상에서 제외하는 것이 정리된 원칙이다.

### 근거와 한계
- 저장소 페이지의 앞부분과 끝부분 위주로 확인했다. 파일 목록, 라이선스(MIT), 릴리스 보안 표시 일부를 확인했고 중간 구간과 벤치마크 세부는 열람하지 않았다.
- 릴리스 보안 주장(출처 증명 수준, 서명, 바이러스 스캔 결과 등)은 업스트림 주장이며 독립적으로 검증하지 않았다.
- "밀리초 단위 색인", "토큰 99% 감소" 같은 수치는 저장소 소개 문구이며 실험 조건이 확인되지 않았다.
- 지식 reference 파일에 기록된 내용을 함께 대조했으나, 사용자 제공 여부와 활용 시점은 미확정이다. 이 정리는 외부 참고 기록이며 채택 결정을 포함하지 않는다.

### 연결
- [agent-skills-standard.md](agent-skills-standard.md) — MCP와 스킬을 도구 표면으로 묶는 표준 관점과 대조할 수 있다.
- [context-engineering-survey.md](context-engineering-survey.md) — 코드 그래프를 컨텍스트 공급 수단으로 볼 때의 위치를 잡는 개관이다.

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
