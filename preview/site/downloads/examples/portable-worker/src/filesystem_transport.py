"""로컬 실습용 소형 원자적 JSON 파일 전달 모듈."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def encode_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def write_json_atomic(path: Path, value: Any, *, replace: bool = False) -> None:
    """같은 디렉터리에 완성된 JSON을 원자적으로 게시하며 덮어쓰기를 거부할 수 있습니다."""
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
            # 같은 파일시스템의 하드 링크 생성은 원자적으로 덮어쓰기를 막습니다.
            os.link(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value
