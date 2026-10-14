# 조사 범위와 한계

조사 기준일: 2026-10-14. 목적은 에이전트 harness engineering 관련 링크와 공개 문서를 사람이 직접 탐색할 수 있는 독립 라이브러리로 제공하는 것입니다. 이 문서는 기존 79-URL/31-card 제한 조사와 후속 무필터 후보 감사의 분모를 구분합니다. 원천 메시지·내부 파일 연결·원문 첨부는 비공개 조사 JOB artifacts에만 보관합니다. [과거 참고 색인 39건 주제별 재고표](legacy-index-inventory/README.md)도 함께 제공합니다.

## 최종 공개 집계

- 공개 manifest 및 카드: 47개 자료 레코드 / 47개 카드. 초기 제한조사 산출은 33개 카드에서 시작해 기존 보완 12건을 더한 45개였고, 2026-10-14 후속으로 Claude Code memory와 Codex AGENTS.md 2건을 추가해 최종 47개가 되었습니다. 단일 카드에 원천 URL 여러 개를 묶은 자료가 있습니다.
- 지식 등록 구분(manifest 기준): 17 reference files, 2 derived knowledge documents, 1 JOB registration record only, 1 reference file confirmed but not indexed, 26건은 제한 검색에서 exact knowledge registration 미확인. 합계는 최종 47건이며 별도 index-only 등록은 확인되지 않았습니다. '미확인'은 절대적 부재 보장이 아닙니다.
- 사용자 제공 상태(manifest 기준, 최종 47건): 33 true, 8 false, 6 unknown. 제공 날짜와 원문 발행일은 별도이며, unknown을 false로 합산하지 않았습니다.
- 기존 제한 조사(수치 원기록 유지): 155개 Hermes 사용자 메시지 후보에서 79개 URL을 추렸고, 공개 자료 30개 URL과 대응시켰으며 49개 URL은 비관련·자기참조·runtime/API endpoint 등 근거에 따라 제외했습니다. 이는 전수 URL 감사 수치가 아닙니다.
- 조사 버전 이력: 초기 제한조사 33개 + 그때 반영한 보완 12개 = 45개. 이후 2026-10-14 후속 카드 2개(Claude Code memory, Codex AGENTS.md)를 추가해 현재 47개입니다. 초기 33개 중 일부는 후보 탐색이 아닌 지정 핵심 출처/보충자료입니다.
- 후속 unfiltered-audit ledger: 10,333개 URL 추출 occurrence, 2,059행 unique-url-ledger, 645행 missing-unregistered context 후보(정규화 613 URL)가 기록되어 있습니다. 이들은 원시 발견/후보 분모이며 관련 문서 수나 누락 자료 수가 아닙니다. 중복 메시지, 자동화/worker 문맥, localhost/API, 문서 삽입, 서식 오류 URL 등이 포함되어 수동 맥락 판정이 필요합니다.
- 별도 missing-context-related 후보 파일은 7,127 rows, link-only review는 1,008 rows, registered source ledger는 15,537 rows, 첨부 포인터는 8 rows, 첨부 cache inventory는 5 rows입니다. 이 파일들의 행은 고유 자료 수와 같지 않습니다.
- 명시적 보완: graph engineering, 20-step loop engineering, MemGPT, Google Cloud self-improving evaluation loop, multi-agent orchestration, Supermemory, codebase-memory-mcp, OpenAI skills 문서 2종, Google Cloud Tech long-horizon 5 patterns 및 첨부 Notes provenance, Harnessing AI, typesafe-ai/skills.
- 미등재 후보 645행(613 URL) 판정: 이미 manifest 3, 내부·API endpoint 91, 맥락 신호 없음 468, 관련 후보 51(출처 확인 대기). 관련 후보 51건은 2차 수동 판정에서 새 카드로 올리지 않았습니다. 내역: typesafe 문서 사이트 23건은 사용자 첨부 스킬 문서 안의 링크라 typesafe-ai/skills 카드의 대체 출처로 묶음; apache/maka 저장소 루트는 기존 Apache Maka 카드의 대체 출처로 묶음; Claude Code memory·Codex AGENTS.md 문서는 이미 카드화; 나머지는 자체 공개 사이트 미리보기·자체 저장소·대화 공유 링크·예시 도메인·서식이 깨진 URL(약 12건), CUDA·NVIDIA·날씨·이미지 사이트·사용량 안내 등 하네스와 무관한 링크(약 8건), 하네스와 무관한 글쓰기 스킬 저장소 1건, 자동 뉴스 초안 작업 문맥에서만 나온 기사 1건이라 제외. 판정 원장은 비공개 조사 기록에 보관. 단, Google Cloud Tech Notes 원문 cache 경로는 이번 실행 시 현재 존재하지 않았고, JOB 원천 메시지 안의 첨부 전사/후속 분석 기록으로만 확인했습니다.

## 조사한 자료군과 분모

1. Hermes default 및 GLM/Astra/Kimi 세션 DB: 사용자 role 메시지 기반 후보 추출. 이전 조사 통계는 default 12,910 sessions / 2,056,939 messages / 96,174 user messages; Astra 737 / 41,195 / 2,191; Kimi 34 / 433 / 48; GLM 2,348 / 126,671 / 5,530입니다. 원시 DB 통계와 추출 후보는 서로 다른 분모입니다.
2. Hermes session/request logs: default 2,257 files 및 22,656 user records; 지정 profile files GLM 105 / 1,474 records, Astra 103 / 141, Kimi 22 / 21. 기존 키워드 탐색에서 추가 후보 0건으로 보고되었습니다.
3. Codex sessions: 152 JSONL / 188,909 lines / 856 user events; Claude projects: 82 JSONL / 29,943 lines / 6,447 user events. 기존 키워드/URL 기반 관련 후보는 0건. Codex `archived_sessions` 경로는 확인 당시 없었습니다.
4. 지식 references: 당시 4,723개 파일 인벤토리 후 harness/agent/workflow/memory/skills/evaluation 등 관련 검색·색인 및 식별 카드 대조. 전체 4,723개 파일 전문을 모두 읽은 것은 아닙니다.
5. JOB·orchestration·프로젝트 자료 및 지정 첨부 포인터: 관련 사례/요청 단위로 탐색. 전체 과거 JOB의 모든 첨부를 전문 검토한 것은 아닙니다.
6. 공개 원문: 관련 핵심 자료는 원문 페이지/서지와 기존 검토 기록을 대조했으나 접근 제한·미현행 확인 등은 개별 카드에 표시했습니다. 전체 전문을 복사하지 않았습니다.

## 제공·등록·활용 구분

- `provided_by_user`: 사람이 제공한 URL/자료 원천이 근거로 확인되면 `true`; 검토된 비사용자 출처면 `false`; 출처/메시지 판정이 안 되면 `null`입니다. 제공 시점은 원문 게시일과 별도 필드입니다.
- `registered_in_knowledge`: 실제 knowledge reference file/derived document가 확인된 경우만 `true`; JOB-only registration은 false이며 `registration_evidence=job_registration_record_only`로 구분합니다. `registration_evidence`는 reference file, derived document, index-only, JOB-only, not-found-after-targeted-check 등의 증거 유형을 따로 나타내고, `registration_indexed`는 근거 있는 경우만 boolean입니다.
- `utilization`: 등록·언급·설계 검토·JOB 분석·운영 채택을 구분합니다. 설계 검토는 production 적용 증거가 아니며 증거를 찾지 못한 경우 `unknown` 또는 제한된 문구를 사용합니다.
- `source_confirmation`: 전문, 첨부 전사, 등록 요약, 제목/URL만 확인한 수준을 표시합니다. 제목만으로 의미를 추정하지 않습니다.
- Google Cloud Tech long-horizon 첨부 Notes는 제공 사건과 내부 참조 기록(익명) 연계가 확인되지만 지정 cache 원본은 이번 재검사에서 찾지 못했습니다. 라이브러리에는 원문 전문 대신 공개 URL·자체 요약·확인 한계만 남겼습니다.
- `typesafe-ai/skills`는 GLM 메시지 2420/2998/4391의 동일 timestamp `1789879693.213`(KST 2026-09-20)으로 한 제공 사건을 확인했으며, 동일 본문 hash의 반복 rows는 별도 제공 사건으로 세지 않았습니다. 지식 파일은 존재하나 주 인덱스 등재는 확인되지 않았습니다.
- `Harnessing AI`는 보존된 원문 추출본에서 게시일과 결론까지 확인해 독립 카드를 보완했습니다. 같은 URL의 과거 색인·파생 위키 등록도 확인했으며, 실제 운영 활용은 별도 증거가 없습니다.

## 포함·제외 분류

- 포함: 사용자 직접 링크/첨부, 지식에 이미 등록된 harness 인접 자료, 필수 핵심 참고자료, 독립적인 보충 연구·구현. 카드에는 관련 주제 태그와 확인 수준을 표시합니다.
- 중복 병합: 번역·abstract/html·같은 문서의 alternate URL은 하나의 자료 레코드 아래 두며, 서로 다른 문서/산출은 별도 카드로 둡니다.
- 제외: 내부 localhost/API, 작업 대상 제품 endpoint, 자기참조·중복, harness와 직접 관계 없는 artifact/URL, 자동 worker나 quoted source의 링크를 사용자 제공 링크로 오인할 수 있는 레코드. 개별 판정과 원천 locator는 private candidate-decision/unfiltered audit artifacts를 참조합니다.
- 충분한 근거가 없는 후보는 없는 것처럼 삭제하지 않습니다. 감사 ledger에 후보로 남겨 검토 상태를 보존합니다. 다만 모든 원시 후보가 공개 자료 카드로 승격되는 것은 아닙니다.

## 메타데이터·라이선스·갱신

필드 정의는 [METADATA.md](METADATA.md), 독립 라이선스·제3자 권리 안내는 [LICENSE](LICENSE) 및 THIRD_PARTY_NOTICES.md(repo 루트, 독립 복사 시 별도 확인), 업데이트 절차는 [MAINTENANCE.md](MAINTENANCE.md)를 참조하세요. 공개본은 원문 전문·코드·이미지·사용자 메시지·로컬 파일 경로를 포함하지 않으며, 불명확한 권리에는 자체 요약과 링크만 둡니다.

## 남은 한계

무필터 URL 후보 조사는 검색 전처리/역할 추정/JSONL 구조에 영향을 받으며 2,059 unique-url-ledger 행은 정규화 결과이며 human-provided 확정 수가 아닙니다. `unfiltered-audit/summary.md`는 지정된 JOB 산출 폴더에서 발견되지 않았습니다. 서로 연결된 관련 후보별 증거는 `known-case-checks.json`, `missing-context-related-candidates.jsonl`, `missing-unregistered-context-candidates.jsonl`, `registered-reference-sources.jsonl`, `job-attachment-pointers.jsonl` 등 기존 로컬 원천 파일에 분산되어 있습니다. 본 공개본에서 제공 여부·등록·실사용을 완전 판정할 수 없는 경우 `unknown`으로 표시합니다.

이 라이브러리는 관련 문서의 재현 가능한 전수 목록이나 Hermes 운용 승인서가 아닙니다. 원문 출처의 변경, 문서 소실, 조사 범위 밖 자료, 비정형 첨부는 남은 누락 가능성으로 명시합니다.
