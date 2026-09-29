"""허용 입력을 검사하고 terminal 응답을 보존하는 단일 요청 처리기."""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Callable

try:
    from .filesystem_transport import read_json, write_json_atomic
    from .orchestrator import SAFE_ID, TERMINAL
except ImportError:  # 단위 테스트에서 모듈을 직접 불러오는 경우도 지원합니다.
    from filesystem_transport import read_json, write_json_atomic
    from orchestrator import SAFE_ID, TERMINAL


class InvalidRequest(ValueError):
    """요청이 잘못되었거나 선언된 입력 경계를 벗어났습니다."""


def resolve_inputs(root: Path, names: list[str]) -> list[Path]:
    root = Path(root).resolve(strict=True)
    resolved: list[Path] = []
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            raise InvalidRequest("input paths must stay beneath the allowlisted root")
        try:
            item = (root / relative).resolve(strict=True)
        except FileNotFoundError as exc:
            raise InvalidRequest(f"input does not exist: {name}") from exc
        if not item.is_relative_to(root) or not item.is_file():
            raise InvalidRequest(f"input is not an allowlisted regular file: {name}")
        resolved.append(item)
    return resolved


def process_one(
    request_path: Path,
    outbox: Path,
    allowed_root: Path,
    handler: Callable[[dict[str, Any], list[Path]], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """불변 요청 하나를 읽고 기존 terminal 응답을 덮어쓰지 않습니다."""
    raw = Path(request_path).read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    try:
        request = read_json(request_path)
        request_id = request.get("request_id")
        if not isinstance(request_id, str) or not SAFE_ID.fullmatch(request_id):
            raise InvalidRequest("request_id must be a safe filename token")
        if type(request.get("intent_revision")) is not int or request["intent_revision"] < 1:
            raise InvalidRequest("intent_revision must be a positive integer")
        if not isinstance(request.get("goal_id"), str) or not request["goal_id"].strip():
            raise InvalidRequest("goal_id is required")
        if not isinstance(request.get("acceptance"), str) or not request["acceptance"].strip():
            raise InvalidRequest("acceptance is required")
        if not isinstance(request.get("policy"), dict):
            raise InvalidRequest("policy must be an object")
        names = request.get("inputs")
        if not isinstance(names, list) or not all(isinstance(item, str) for item in names):
            raise InvalidRequest("inputs must be a list of relative paths")
        input_paths = resolve_inputs(allowed_root, names)
    except (InvalidRequest, ValueError) as exc:
        request = locals().get("request", {})
        request_id = request.get("request_id")
        if not isinstance(request_id, str) or not SAFE_ID.fullmatch(request_id):
            request_id = Path(request_path).stem
        response = _response(request_id, request, digest, "blocked", error=str(exc))
        return _publish(response, outbox)

    response_path = Path(outbox) / f"{request_id}.json"
    if response_path.exists():
        existing = read_json(response_path)
        if existing.get("request_sha256") != digest:
            raise ValueError("request_id already has a terminal response for different request bytes")
        return existing

    try:
        result = (handler or _default_handler)(request, input_paths)
        status = result.get("status")
        if status not in TERMINAL:
            raise ValueError("handler must return a terminal status")
        response = _response(request_id, request, digest, status,
                            artifacts=result.get("artifacts", []), result=result.get("result"))
    except Exception as exc:  # 처리 오류를 기록 가능한 terminal 상태로 변환합니다.
        artifacts = getattr(exc, "artifacts", [])
        status = "partial" if artifacts else "failed"
        response = _response(request_id, request, digest, status,
                            artifacts=artifacts, error=f"{type(exc).__name__}: {exc}")
    return _publish(response, outbox)


def _default_handler(request: dict[str, Any], inputs: list[Path]) -> dict[str, Any]:
    return {"status": "done", "artifacts": [], "result": {"checked_inputs": len(inputs)}}


def _response(request_id: str, request: dict[str, Any], digest: str, status: str,
              *, artifacts: list[str] | None = None, result: Any = None, error: str | None = None) -> dict[str, Any]:
    response: dict[str, Any] = {
        "request_id": request_id,
        "goal_id": request.get("goal_id"),
        "intent_revision": request.get("intent_revision"),
        "status": status,
        "request_sha256": digest,
        "artifacts": list(artifacts or []),
    }
    if result is not None:
        response["result"] = result
    if error is not None:
        response["error"] = error
    return response


def _publish(response: dict[str, Any], outbox: Path) -> dict[str, Any]:
    path = Path(outbox) / f"{response['request_id']}.json"
    try:
        write_json_atomic(path, response)
    except FileExistsError:
        existing = read_json(path)
        if existing != response:
            raise ValueError("terminal response already exists and is immutable")
        return existing
    return response
