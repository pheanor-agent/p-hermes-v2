# 5 design patterns for long-horizon agent harness

- Source: https://x.com/GoogleCloudTech/status/2090248297214525569
- Alternate sources: none recorded
- Topics: orchestration-workflow, context-memory-knowledge, evaluation-observability-security, case-implementation
- Publication date: 2026-08-20 (내부 참조 기록(익명))
- User-provided: True; date: 2026-08-26
- Knowledge registration: false; a 내부 참조 기록(익명) exists, but this check did not confirm a separate knowledge/reference card or index entry
- Source confirmation: 내부 참조 기록(익명) 등록 기록은 2026-08-26 capture, user-provided Notes 전사, URL 및 reference snapshot SHA-256을 기록. 현재 첨부 cache 파일은 지정 경로에서 찾지 못했으며 공개본에 재배포하지 않음.
- Utilization: 내부 참조 기록(익명)은 reference-only/design-only scope로 승인되어 다섯 개 no-network/no-native-write contract fixture를 실행했고 모두 PASS; production/runtime 적용은 하지 않음.
- Rights: not verified; no full text, code, images, or private attachments are redistributed here.

## Independent summary and scope

Google Cloud Tech의 장기 에이전트 하네스 패턴 글. 내부 참조 기록(익명)는 게시일을 2026-08-20으로 기록하며, 캡처일은 2026-08-26입니다. 주요 패턴은 (1) stable prefix와 prompt-cache 측정, (2) 안전장치가 있는 background learning/write-behind, (3) persistent workspace와 lifecycle-aware liveness, (4) 명시적 typed failure와 bounded loop termination, (5) normalized guard chain 및 credential/sandbox 분리입니다.

내부 참조 기록(익명)의 contract fixtures는 stable prefix digest, background-learning lifecycle, persistent-workspace state, explicit-failure envelope, normalized guard-chain 다섯 항목에서 PASS했습니다. 이는 JOB-local 설계 fixture 검증이며 Hermes production/runtime 적용이나 외부 성능 검증이 아닙니다. 원문이 제시한 cache/latency/limit 수치도 source-stated이며 Hermes 측정값으로 옮기지 않습니다.

## Reading note

Treat the source's statements and benchmarks as source claims unless independently reproduced. Inclusion is for discoverability only: it is not an operational instruction, policy, safety endorsement, or adoption decision.
