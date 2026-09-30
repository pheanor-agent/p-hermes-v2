"""불변 요청을 시도별로 발행하고 terminal 응답을 수집합니다."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

try:
    from .filesystem_transport import read_json, write_json_atomic
except ImportError:  # 단위 테스트에서 모듈을 직접 불러오는 경우도 지원합니다.
    from filesystem_transport import read_json, write_json_atomic

TERMINAL = {"done", "partial", "failed", "blocked"}
SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


def request_digest(request: dict[str, Any]) -> str:
    import json
    payload = json.dumps(request, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def submit(request: dict[str, Any], inbox: Path) -> Path:
    """요청 파일을 만듭니다. 동일 내용 재요청은 멱등이며 변경 내용은 충돌로 처리합니다."""
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


def collect(request_id: str, outbox: Path) -> dict[str, Any] | None:
    path = Path(outbox) / f"{request_id}.json"
    if not path.exists():
        return None
    response = read_json(path)
    if response.get("request_id") != request_id:
        raise ValueError("response request_id does not match requested attempt")
    if response.get("status") not in TERMINAL:
        raise ValueError("response is not terminal")
    return response
