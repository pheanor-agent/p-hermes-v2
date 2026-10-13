# 하네스 과거 등록 참고 자료 재고표 (legacy-index inventory)

이 폴더는 과거 참고 색인(`references/index.md`)에는 등록되어 있었지만 현재 카드 목록에서 빠진 하네스 관련 자료를 한 곳에 모은 독립 재고표다.

- 대상: 색인 항목 88개 중 하네스 관련으로 표시된 42개 + 같은 원천 URL을 공유하는 항목 + 검토 후 포함한 항목 4개 → 원천 기준 병합 후 39개 항목
- 제외: 일반 모델 카드·범용 라이브러리 등 하네스와 무관한 7개 (사유는 내부 감사 기록에만 있음)
- 기준 시점: 2026-10-14. 주 manifest 스냅샷: 47개 record, SHA-256 `714a98736e92…`(inventory.json에 전체 값 기록). 작성 중 주 manifest가 병렬 갱신되어 최종 스냅샷 기준으로 다시 대조했다. 이후 주 manifest에는 두 record(`typesafe-ai-skills`, `apache-maka-agent-graph`)의 대체 출처 URL만 추가되어 현재 해시는 이 값과 다르며, record 수와 id는 같다.

## 파일

- `inventory.json`: 항목별 전체 필드 (기계 판독용)
- `inventory.csv`: 같은 내용의 표 형식 (JSON 값은 문자열로 인코딩)

## 항목 필드

| 필드 | 뜻 |
|---|---|
| title | 원천 페이지 또는 색인에서 확인한 제목 |
| public_source_url | 공개 원천 URL. 기록에서 확인되지 않으면 null |
| topics | 주 manifest의 주제 태그 (주 manifest에 없으면 `unclassified-legacy`) |
| self_summary | 원천 기록을 바탕으로 한 짧은 자체 요약 (원문 복사 아님) |
| state | `file-present` / `derived-only` / `indexed-only` |
| registration_check | 색인·참고 파일·파생 문서 중 무엇이 확인되었는지 |
| provision_check | 사용자 제공 여부 (주 manifest 기준, 미확정이면 unknown) |
| utilization_check | 활용 확인 수준. 원천 기록의 주장이며 운영 채택 증거가 아님 |
| source_date | 원천 기록에서 확인된 날짜 (없으면 빈 값) |
| rights | 원문 미배포. 권리 상태는 확인하지 않았으므로 미확인 |
| manifest_record_id | 주 manifest에서 같은 URL을 가진 record id (없으면 null) |
| merged_index_entries | 같은 원천으로 병합된 색인 항목 수 |

## 읽는 법

- `state`가 `derived-only`이면 색인 항목은 있으나 참고 파일이 없고, 가공된 위키 페이지에서 원천을 찾았다는 뜻이다.
- `indexed-only`는 색인 항목만 있고 원천 페이지를 찾지 못한 항목이다.
- 이 재고표는 과거 등록 흔적을 찾아보기 위한 목록이다. 여기에 있다고 해서 현재 운영에 채택되었다는 뜻은 아니다.
- 메인 카드와 주 manifest는 이 재고표가 수정하지 않는다. 주 manifest에 없는 항목은 `manifest_record_id`가 null이다.

## 확인 범위와 한계

- 원천 확인은 색인 줄, 가공된 위키 페이지, 참고 파일의 머리말과 본문 일부에 한정했다. 원문 전체와 링크 최신성은 확인하지 않았다.
- 권리·라이선스는 확인하지 않았다. 원문은 배포하지 않고 링크와 자체 요약만 둔다.
- 일부 X(트위터) 링크는 공개 게시물 주소이며, 원천 로그인 게이트로 본문을 확인하지 못했다.
