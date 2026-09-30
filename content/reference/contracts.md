# File handoff contracts

This reference describes the portable teaching kit in `reference/`. It is a proposed, local contract; it is not a claim that every agent product implements these files or fields.

## Request object

Required JSON fields:

| Field | Type | Meaning |
|---|---|---|
| `request_id` | non-empty string | Unique immutable attempt identifier; do not reuse for a changed request. |
| `goal_id` | non-empty string | Stable outcome identity shared across attempts. |
| `intent_revision` | positive integer | Revision of the user's intent represented by this attempt. |
| `inputs` | array of relative path strings | Files the worker may read beneath its configured allowlist root. |
| `acceptance` | string | Observable condition for this attempt. |
| `policy` | object | Caller-defined constraints; the worker must enforce each constraint it relies on. A recorded label alone is not an access-control mechanism. |

A retry for the same goal uses a new `request_id`. The file is write-once: identical resubmission is idempotent; different content under the same ID is a conflict.

## Response object

Required fields:

| Field | Type | Meaning |
|---|---|---|
| `request_id` | string | Must exactly match the attempt being collected. |
| `goal_id` | string or null | Echo of the request goal when available. |
| `intent_revision` | integer or null | Echo of the request revision when available. |
| `status` | enum | One of `done`, `partial`, `failed`, `blocked`. |
| `request_sha256` | 64-character hex string | Digest of the original request bytes used by this worker. |
| `artifacts` | array of strings | Paths or identifiers for preserved outputs; empty when none. |
| `result` | optional JSON value | Small success details. |
| `error` | optional string | Failure/block reason; do not include secrets. |

`done` means the worker reports the acceptance condition met. `partial` means at least one artifact is preserved but the attempt did not fully complete. `failed` means the attempt ended without a preserved deliverable. `blocked` means validation or policy prevented execution. Consumers treat any other value as non-terminal and reject mismatched IDs.

## State and file movement

```text
created → inbox/request.json → worker reads immutable bytes
                               ├─ malformed / disallowed → outbox/response.json: blocked
                               ├─ execution error, no artifact → failed
                               ├─ execution error, artifact kept → partial
                               └─ acceptance met → done
```

The teaching kit leaves archival or movement of the original request to the caller. It does not delete a request after processing. The caller configures the worker's `allowed_root`; `policy` metadata does not itself grant or restrict operating-system permissions. The worker enforces the input-path boundary, but the surrounding application/operator remains responsible for process identity, filesystem permissions, and any additional policy checks. The terminal response is written atomically and is never overwritten. Existing response for the same request is returned only when it binds to the same request digest; a conflicting response is an error.

## Error cases and limits

- Missing or malformed request fields: `blocked` response.
- Absolute path, `..`, missing input, or symlink resolving outside the allowlist: `blocked` response.
- Handler raises without reporting artifacts: `failed` response.
- Handler raises after reporting preserved artifacts: `partial` response; keep the files.
- A response with a different request ID or a non-terminal status: collection fails closed.
- A request ID reused with changed content: submission fails; allocate a new ID.
- Atomic file publication is not a queue lock or multi-worker claim protocol. Add a lease/claim mechanism before concurrent production use.

## Directory contract

```text
inbox/   immutable request JSON, one file per attempt
outbox/  terminal response JSON, one file per attempt
inputs/  caller-owned fixture files beneath the worker allowlist
```

The example uses the Python standard library and temporary directories. It performs no network, credential, GPU, or product-specific operation.
