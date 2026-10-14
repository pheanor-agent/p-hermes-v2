# Supermemory — Memory and Context Engine for AI

- Source: https://github.com/supermemoryai/supermemory
- Alternate sources: https://app.supermemory.ai, https://supermemory.ai/install
- Topics: context-memory-knowledge, skills-tools, case-implementation
- Publication date: unknown / not independently verified
- User-provided: unknown; date: unknown
- Knowledge registration: True; evidence: knowledge/references/github/supermemoryai-supermemory.md
- Source confirmation: 기존 reference 파일 확인; 제공 시점은 미확정
- Utilization: 메모리·프로필·검색·connector의 제품 기록. 벤치마크/제품 기능은 원천의 주장이고 Hermes 도입 또는 성능 검증을 의미하지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.
- 정리 근거: 원문 일부 확인

## Independent summary and scope

메모리·프로필·검색·connector의 제품 기록. 벤치마크/제품 기능은 원천의 주장이고 Hermes 도입 또는 성능 검증을 의미하지 않음.

## 상세 정리

### 핵심 주장
1. AI가 대화 사이에 잊는 문제를 메모리 계층으로 해결한다고 주장한다. 사실을 추출하고, 사용자 프로필을 만들고, 모순과 만료를 처리한다.
2. 메모리와 RAG를 하나의 질의로 합쳐 개인화된 문맥과 지식 베이스 문서를 함께 제공한다.
3. 로컬 실행이 가능하다고 소개한다.

### 구조와 패턴
- 구성: 메모리(사실 추출, 시간 변화와 모순 처리, 자동 망각), 사용자 프로필, 하이브리드 검색, 커넥터(드라이브, 메일, 노션 등 웹훅 동기화), 멀티모달 추출(PDF, 이미지 OCR, 영상 전사, 코드 청킹).
- 벤치마크(LongMemEval, LoCoMo, ConvoMem) 1위를 주장한다.

### 적용 방법
- 사실 추출과 모순 처리 방식은 Hermes 메모리 설계의 비교 대상이 될 수 있다.
- 외부 커넥터로 개인 데이터를 동기화하면 권리와 개인정보 범위를 먼저 정한다.

### 근거와 한계
- 저장소 README 일부만 확인했다. 벤치마크 1위는 저장소의 주장이며 독립 재현은 확인하지 못했다.
- 내부 구현과 성능 수치는 확인하지 못했다.

### 연결
- [MemGPT context OS](memgpt-context-os.md) — 계층형 메모리의 원조 설계
- [Letta context repositories](letta-context-repositories.md) — 파일과 git 기반 기억 관리
- [Codebase memory MCP](codebase-memory-mcp.md) — 코드 지식 그래프를 MCP로 제공하는 사례
## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
