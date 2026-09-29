# Applying the pattern in three environments

This is an adaptation map, not a claim that the products share an API. The concrete product-specific case below is the current Claude Code harness inspected for this pilot. The Python kit is the runnable, portable example. Codex is a target for future mapping; no product API behavior is asserted here.

| Environment | What maps | What remains environment-specific | Evidence status |
|---|---|---|---|
| Claude Code + an external worker | Keep the user's goal and approval boundary in project guidance; create a distinct immutable request for each attempt; dispatch the bounded request to a worker; read back a structured terminal result before reporting. | The inspected harness uses a project instruction file, a request-registration helper, a dispatcher command, and an outbox/report path. Those names, commands, identity, and local paths are not portable interfaces. | Current local example inspected; summarized, not published as a reusable product API. |
| Codex | The same role separation, stated acceptance conditions, scoped inputs, and terminal response can be expressed as instructions and tool permissions. | No Codex-specific wiring, command, hook, or runtime API is specified here because this pilot did not verify one. | Proposal only. |
| Generic Python agent | The included modules implement request validation, immutable attempt IDs, file transport, allowlisted inputs, atomic terminal response, deduplication, and tests. | A real deployment still needs an environment-specific scheduler, process claim/lease strategy, authorization, logging, and recovery contract. | Executed locally with synthetic fixtures; see `tests/` and the smoke evaluation. |

## Reading the Claude Code case

In the inspected setup, project guidance defines the top-level agent's role and points to the canonical operating rules. A helper registers the request and updates the goal record; a separate dispatcher launches the worker with the request path. The caller then checks the dispatcher result, structured outbox response, and actual artifacts instead of trusting a chat summary alone. This is a description of one local integration, not a recommendation to copy its paths or command names.

## Porting checklist

1. Identify which component owns the user goal and approval decision.
2. Identify the actual execution worker and its supported input/output interface from that environment's documentation.
3. Translate the request/response fields; keep attempt identity separate from goal identity.
4. Define what `done`, `partial`, `failed`, and `blocked` mean for that worker.
5. Add input allowlisting, artifact preservation, and response read-back.
6. Test retries, duplicate delivery, malformed input, and interruption before enabling real side effects.

Until steps 2–6 are checked in the target environment, call the mapping a proposal—not a working adapter.
