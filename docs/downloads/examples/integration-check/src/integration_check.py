from __future__ import annotations

import json
from pathlib import Path


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(fixture_dir: Path, output_dir: Path) -> dict:
    request = read_json(fixture_dir / "request.json")
    contract = read_json(fixture_dir / "contract.json")
    context = read_json(fixture_dir / "context.json")
    catalog = read_json(fixture_dir / "catalog.json")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 가짜 실행은 합성 표식 파일을 남기며, 실제 이미지 런타임을 호출하지 않는다.
    artifact = output_dir / "synthetic-image.txt"
    artifact.write_text("SYNTHETIC_IMAGE_ARTIFACT\n", encoding="utf-8")
    missing = [name for name in request["required_conditions"] if name not in contract["satisfied_conditions"]]
    if not context.get("source_verified", False):
        missing.append("context.source_verified")
    if catalog.get("runtime") != "fake":
        missing.append("catalog.runtime=fake")
    status = "done" if not missing and artifact.is_file() else "partial"
    response = {
        "request_id": request["request_id"],
        "status": status,
        "artifact": artifact.name,
        "missing_conditions": missing,
    }
    (output_dir / "response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return response
