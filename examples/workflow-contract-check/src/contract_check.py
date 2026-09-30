from __future__ import annotations

import json
from pathlib import Path


def check(request_file: Path, artifact_dir: Path) -> tuple[bool, list[str]]:
    """Return pass status and paths of required artifacts that are missing."""
    request = json.loads(request_file.read_text(encoding="utf-8"))
    if request.get("tier") != "light":
        raise ValueError("지원하는 계약은 light뿐입니다")
    required = request.get("required_artifacts")
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        raise ValueError("required_artifacts는 문자열 배열이어야 합니다")
    missing = [name for name in required if not (artifact_dir / name).is_file()]
    return not missing, missing
