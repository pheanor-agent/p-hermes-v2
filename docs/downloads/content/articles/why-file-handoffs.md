# Why pass work as files?

A handoff is not a chat message that happens to mention a task. It is a small, inspectable agreement between the part that decides what should happen and the part that performs it. The agreement needs a stable identity, a bounded input set, a way to report the result, and a rule for what happens when work stops midway.

## The problem: one goal can have several attempts

Suppose an orchestrator wants one outcome: prepare a short explanation. The first attempt may fail because an input is missing. The next attempt may use a corrected input. The goal has not changed, but the attempts are different events. If the same identifier is reused, a late response from the first attempt can be mistaken for the second.

Keep two identities:

- A **goal ID** names the continuing outcome.
- A **request ID** names one immutable attempt at that outcome.

A retry keeps the goal ID and gets a new request ID. The request records its intent revision and acceptance condition so a worker can tell what this particular attempt is expected to do.

## What the file boundary buys you

A request file can be read before work starts. It makes the inputs, constraints, and expected result visible together. A worker can reject a malformed request before it touches anything. The same file can be used to reproduce the attempt later, while a response file records what actually happened.

The boundary also makes delivery clear. A response is not “done” because a process stopped. It is terminal only when it says whether the attempt finished, partially finished, failed, or was blocked—and names any artifacts that were produced.

## A small lifecycle

```text
same goal
  ├─ attempt A: request → worker → failed (input unavailable)
  └─ attempt B: new request ID → worker → partial (draft preserved)
                                      └→ later attempt may finish
```

The request is immutable after submission. A correction creates another attempt rather than rewriting history. The worker reads only inputs beneath an explicitly allowed root. It writes a response to a temporary file first and publishes the complete file atomically, so a reader does not see half a JSON document.

## Why partial is a real result

Imagine the worker has already saved a draft, then a later step fails. Deleting the draft or reporting only “failed” loses useful work and hides what remains. A `partial` response names the saved artifact and explains the failure. A `failed` response means the attempt produced no preserved deliverable; `blocked` means the request or its permissions prevent safe execution. These labels describe outcomes, not quality grades.

## What this does not solve

Files do not provide a scheduler, a process lock, a distributed transaction, or authorization by themselves. Atomic replacement prevents torn publication; it does not make a multi-process queue safe without a separate claim/lease protocol. An allowlist is useful only if the worker resolves paths and refuses traversal or symlink escapes. The code kit below is a local, single-worker teaching example—not a production dispatcher.

## Use the result as evidence

A consumer should match the response's request ID to the attempt it asked about, accept only terminal statuses, and inspect the artifact list. If a response is missing, the attempt is still pending from the consumer's point of view. If it belongs to another request, reject it rather than guessing.

The companion contract reference defines the fields and transitions. The tutorial runs the same pattern with a temporary inbox, outbox, and synthetic input; it sends nothing outside that directory.
