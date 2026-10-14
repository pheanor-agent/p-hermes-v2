# Manifest field definitions

`manifest.json` is the machine-readable source of truth; `manifest.csv` is a UTF-8 convenience export generated from it. Unknown is represented as JSON `null`/CSV empty, never inferred as false.

| Field | Meaning |
|---|---|
| `id` | Stable local record identifier. It is not required to equal the card basename; use the separate `card` field for the path (for example `agentskills-standard` → `cards/agent-skills-standard.md`). |
| `canonical_url` | Preferred public source URL; not a claim that the page is currently reachable. |
| `alternate_urls` | Related canonical/localized/format URLs grouped with this record. |
| `topics` | One or more controlled categories from `CATALOG.md`. |
| `published` | Source publication status/date; use `unknown` when not confirmed. |
| `provided_by_user` | `true` only when a human-origin source message is evidenced; `false` means a reviewed non-user source; `null` means unresolved. |
| `provided_date` | Confirmed date of providing the source, distinct from source publication/capture dates. |
| `registered_in_knowledge` | `true` only when a knowledge reference file or derived knowledge document is verified; a JOB-only record is not counted as a knowledge registration. Does not imply index coverage or usage. |
| `registration_evidence` | Categorical evidence: `reference_file`, `reference_file_not_indexed`, `derived_document`, `job_registration_record_only`, `index_only`, `not_found_after_targeted_check`, `record_confirmed_location_unspecified`, or `unknown`. |
| `registration_indexed` | `true`/`false` only when index status is evidenced; otherwise `null`. Index-only presence is distinct from a reference file. |
| `registration_note` | Public-safe registration evidence description; private paths/messages are excluded. |
| `utilization` | Evidence-bounded description; do not treat registration/review as adoption. |
| `rights` | Rights check state and redistribution boundary. |
| `original_preserved` | Whether this library redistributes original full text (all current records are false). |
| `source_confirmation` | What was actually checked, including partial/title-only status. |
| `card` | Relative path to the standalone summary card. |
| `digest_basis` | What the card's 상세 정리 section was written from: `원문 전체 확인` (whole source read), `원문 일부 확인` (part of the source read, e.g. abstract/intro or a login-limited post), `지식 기록 대조 + 원문 일부 확인` (an earlier knowledge record checked against part of the source), `지식 기록 기준(원문 미열람)` (earlier record only). |

Dates use ISO `YYYY-MM-DD` when verified. Do not replace unknown with an assumed date. Provenance in the public library is intentionally anonymized; detailed source locators remain in the private audit records.

## Card structure

Each card has: metadata lines, `## 자체 요약` (one-paragraph summary), `## 상세 정리` (a working digest meant to be usable without opening the link), and a relevance/reading note.

`## 상세 정리` always has five subsections: `### 핵심 주장` (main claims), `### 구조와 패턴` (components, flow, patterns), `### 적용 방법` (how to apply), `### 근거와 한계` (evidence, conditions, what was not read), `### 연결` (related cards). The digest is written in our own words; numbers from papers or vendors are labeled as source claims together with their conditions. When `digest_basis` is partial, check the original before relying on details the digest does not cover.
