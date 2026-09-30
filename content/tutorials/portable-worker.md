# Run a portable file worker

This exercise uses Python 3.11 or newer and the standard library only. It creates a temporary inbox and outbox, reads one synthetic text fixture, and records a terminal response. It does not contact a service or modify a real agent installation.

## 1. Inspect the kit

The `reference/` directory contains three modules:

- `orchestrator.py` validates and submits one immutable request, then collects a terminal response.
- `worker.py` reads a request, resolves inputs beneath an allowlisted root, runs a handler, and records `done`, `partial`, `failed`, or `blocked`.
- `filesystem_transport.py` publishes complete JSON files atomically.

The fixture is `examples/inputs/brief.txt`. It is intentionally synthetic.

## 2. Submit and process an attempt

Run the following from the pilot root: the directory that directly contains both `reference/` and `examples/`. For example, after `cd /path/to/output/pilot`, `Path.cwd() / "examples"` resolves to the fixture allowlist root `output/pilot/examples/`; the request's `inputs` entry `inputs/brief.txt` is relative to that root, so it resolves to `output/pilot/examples/inputs/brief.txt`.

```sh
python3 - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory
from reference.orchestrator import collect, submit
from reference.worker import process_one

pilot = Path.cwd()
with TemporaryDirectory(prefix="portable-worker-") as temp:
    root = Path(temp)
    request = {
        "request_id": "attempt-demo-001",
        "goal_id": "goal-demo-001",
        "intent_revision": 1,
        "inputs": ["inputs/brief.txt"],
        "acceptance": "read the fixture and return a terminal response",
        "policy": {"allowed_root": "examples"},
    }
    request_path = submit(request, root / "inbox")
    response = process_one(request_path, root / "outbox", pilot / "examples")
    assert response["status"] == "done"
    assert collect(request["request_id"], root / "outbox") == response
    print(response["status"], response["request_id"], response["result"])
PY
```

Expected shape: a `done` status, the matching attempt ID, and a small result reporting one checked input. The temporary directory is removed when the block exits.

## 3. Try a safe failure

Change `inputs` to `["../outside.txt"]` in the request and use a new request ID. The worker should return `blocked` because the path escapes the configured root. It should not open that file.

Do not edit a request after submission. If its meaning changes, keep the same `goal_id`, increment the intent revision if appropriate, and create a new request ID.

## 4. Run the contract tests

From the pilot root:

```sh
python3 -m unittest discover -s tests -v
```

The tests use fresh temporary folders and synthetic files. They cover idempotent submission, immutable IDs, required-field/type validation, atomic write/no-overwrite, ID matching, allowlist traversal and symlink escape, terminal errors, partial artifact preservation, and duplicate response handling.

## 5. Read the result carefully

A successful process exit is not itself proof that useful work completed. Check the response ID and terminal status, then inspect any named artifact. `partial` is not success and is not equivalent to `failed`: it says some output was preserved. This teaching worker is single-process; use a separate claim/lease contract before allowing concurrent workers to compete for the same inbox.
