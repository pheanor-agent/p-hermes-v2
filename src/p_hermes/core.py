"""Shared explicit data contracts. No network or import-time side effects."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


class ContractError(ValueError):
    """The requested operation does not satisfy the public reference contract."""


def identifier(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,79}", value):
        raise ContractError("identifier must use 1–80 ASCII letters, digits, dots, _ or -")
    return value


def require_text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label} must be nonempty text")
    return value


def canonical(value: object) -> str:
    """Reference canonical JSON v1; all fields participate, NaN is forbidden."""
    try:
        result = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
        result.encode("utf-8")
        return result
    except (ValueError, TypeError, UnicodeError) as exc:
        raise ContractError("value must be finite, UTF-8 encodable JSON") from exc


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def contained(root: Path, relative: str) -> Path:
    """Reject absolute, traversal and symlink paths, including parent components."""
    root = Path(root).resolve()
    if not isinstance(relative, str) or not relative or "\\" in relative or ":" in relative:
        raise ContractError("artifact path must be a portable relative path")
    path = Path(relative)
    if path.is_absolute() or any(part in {"..", "."} for part in relative.split("/")):
        raise ContractError("artifact path must stay below workspace")
    candidate = root
    for part in path.parts:
        candidate /= part
        if candidate.is_symlink():
            raise ContractError("symlink artifacts are not accepted")
    if not candidate.resolve().is_relative_to(root):
        raise ContractError("artifact path escapes workspace")
    return candidate


def file_digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()
