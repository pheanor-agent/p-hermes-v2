# Applying the pattern in other environments

This is an adaptation map, not a claim that any agent product shares an API. The Python kit in this repository is the runnable, portable example; any other environment must be mapped from its own documentation.

| Environment | What maps | What remains environment-specific | Evidence status |
|---|---|---|---|
| A coding agent that reads repository instructions, plus an external worker | Keep the user's goal and approval boundary in project guidance; create a distinct immutable request for each attempt; dispatch the bounded request to a worker; read back a structured terminal result before reporting. | Instruction file names, request-registration helpers, dispatcher commands, outbox paths and identities differ per environment and are not portable interfaces. | Pattern description only; no product API is asserted. |
| Generic Python agent | The included modules implement request validation, immutable attempt IDs, file transport, allowlisted inputs, atomic terminal response, deduplication, and tests. | A real deployment still needs an environment-specific scheduler, process claim/lease strategy, authorization, logging, and recovery contract. | Executed locally with synthetic fixtures; see `tests/`. |

## Reading the pattern

Project guidance defines the coordinating agent's role and points to the canonical operating rules. A helper registers the request and updates the goal record; a separate dispatcher launches the worker with the request path. The caller then checks the dispatcher result, the structured response, and the actual artifacts instead of trusting a chat summary alone.

## Porting checklist

1. Identify which component owns the user goal and approval decision.
2. Identify the actual execution worker and its supported input/output interface from that environment's documentation.
3. Translate the request/response fields; keep attempt identity separate from goal identity.
4. Define what `done`, `partial`, `failed`, and `blocked` mean for that worker.
