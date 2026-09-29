"""Small atomic JSON transport for a local, portable worker demo."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def encode_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write_json_atomic(path: Path, value: Any, *, replace: bool = False) -> None:
    """Publish complete JSON by same-directory replace; optionally refuse overwrite."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not replace:
        raise FileExistsError(path)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(encode_json(value))
            stream.flush()
            os.fsync(stream.fileno())
        if replace:
            os.replace(temp, path)
        else:
            # Hard-link creation is an atomic no-clobber publish on one filesystem.
            os.link(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value
