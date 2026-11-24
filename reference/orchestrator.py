"""Submit immutable goals as versioned attempts, collect terminal responses, and record decisions."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

try:
    from .filesystem_transport import read_json, write_json_atomic
except ImportError:  # Also supports direct-module use in the unittest harness.
    from filesystem_transport import read_json, write_json_atomic

TERMINAL = {"done", "partial", "failed", "blocked"}
DECISIONS = {"accepted", "needs_work"}
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


def request_file_digest(path: Path) -> str:
    """Return the SHA-256 of the request file's original bytes (the value workers record)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def submit(request: dict[str, Any], inbox: Path) -> Path:
    """Create one request file. Repeating identical bytes is idempotent; changed bytes conflict."""
    required = {"request_id", "goal_id", "intent_revision", "inputs", "acceptance", "policy"}
    if required - request.keys():
        raise ValueError(f"missing request fields: {sorted(required - request.keys())}")
    if not all(isinstance(request[k], str) and request[k].strip() for k in ("request_id", "goal_id")):
        raise ValueError("request_id and goal_id must be non-empty strings")
    if not SAFE_ID.fullmatch(request["request_id"]):
        raise ValueError("request_id must be a safe filename token")
    if type(request["intent_revision"]) is not int or request["intent_revision"] < 1:
        raise ValueError("intent_revision must be a positive integer")
    if not isinstance(request["inputs"], list) or not all(isinstance(x, str) for x in request["inputs"]):
        raise ValueError("inputs must be a list of relative path strings")
    if not isinstance(request["acceptance"], str) or not isinstance(request["policy"], dict):
        raise ValueError("acceptance must be text and policy must be an object")
    path = Path(inbox) / f"{request['request_id']}.json"
    try:
        write_json_atomic(path, request)
    except FileExistsError:
        if read_json(path) != request:
            raise ValueError("request_id is immutable; use a new ID for changed intent")
    return path


def revise_request(previous: dict[str, Any], new_request_id: str, **changes: Any) -> dict[str, Any]:
    """Build the next attempt for the same goal: new request_id, intent_revision + 1.

    Use this after a `needs_work` decision. The previous request_id is never edited.
    """
    revised = dict(previous)
    revised.update(changes)
    revised["request_id"] = new_request_id
    revised["intent_revision"] = previous["intent_revision"] + 1
    return revised


def collect(request_id: str, outbox: Path, request_path: Path | None = None) -> dict[str, Any] | None:
    """Return the terminal response for one attempt, or None if none exists yet.

    When `request_path` is given, the response's `request_sha256` must equal the SHA-256 of
    that file's original bytes; otherwise the response is not bound to this request.
    """
    path = Path(outbox) / f"{request_id}.json"
    if not path.exists():
        return None
    response = read_json(path)
    if response.get("request_id") != request_id:
        raise ValueError("response request_id does not match requested attempt")
    if response.get("status") not in TERMINAL:
        raise ValueError("response is not terminal")
    if request_path is not None and response.get("request_sha256") != request_file_digest(request_path):
        raise ValueError("response request_sha256 does not match the request file bytes")
    return response


def accept(request_id: str, outbox: Path, reviews: Path, decision: str, note: str = "") -> dict[str, Any]:
    """Record the manager's decision on a terminal response, separate from the worker's status.

    `decision` is `accepted` or `needs_work`. The record is written once to
    `<reviews>/<request_id>.json`; the same decision again returns the existing record, and a
    different decision raises ValueError. A `needs_work` outcome means: submit a new attempt with
    `revise_request(...)` (same goal_id, higher intent_revision, new request_id). Do not edit the old one.
    """
    if not isinstance(request_id, str) or not SAFE_ID.fullmatch(request_id):
        raise ValueError("request_id must be a safe filename token")
    if decision not in DECISIONS:
        raise ValueError(f"decision must be one of {sorted(DECISIONS)}")
    if not isinstance(note, str):
        raise ValueError("note must be text")
    response = collect(request_id, outbox)
    if response is None:
        raise ValueError("no terminal response yet; the decision cannot be recorded")
    record = {
        "request_id": request_id,
        "goal_id": response.get("goal_id"),
        "intent_revision": response.get("intent_revision"),
        "response_status": response["status"],
        "request_sha256": response.get("request_sha256"),
        "decision": decision,
        "note": note,
    }
    path = Path(reviews) / f"{request_id}.json"
    try:
        write_json_atomic(path, record)
    except FileExistsError:
        existing = read_json(path)
        if existing != record:
            raise ValueError("review decision is immutable; record a new attempt instead")
        return existing
    return record


def check_duplicate(request: dict[str, Any], inbox: Path, outbox: Path) -> list[str]:
    """Soft warning: request_ids of other requests for the same goal that have no response yet.

    This never blocks submission. It does not provide a lease or lock; two workers can still run
    the same request at the same time (see the concurrency test).
    """
    goal_id = request.get("goal_id")
    own_id = request.get("request_id")
    open_ids: list[str] = []
    for path in sorted(Path(inbox).glob("*.json")):
        try:
            other = read_json(path)
        except (OSError, ValueError):
            continue
        other_id = other.get("request_id")
        if other.get("goal_id") != goal_id or other_id == own_id or not isinstance(other_id, str):
            continue
        if not (Path(outbox) / f"{other_id}.json").exists():
            open_ids.append(other_id)
    return open_ids
