from __future__ import annotations

import json
from pathlib import Path

# light JOB 게이트가 단계마다 읽는 필수 파일 (요청 → 실행 → 검증 → 완료).
LIGHT_FILES = {
    "request": ["request.md"],
    "execution": ["approval.md", "execution.md"],
    "verification": ["verification.md"],
    "done": ["result.md"],
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run(fixture_dir: Path, output_dir: Path) -> dict:
    request = read_json(fixture_dir / "request.json")
    contract = read_json(fixture_dir / "contract.json")
    context = read_json(fixture_dir / "context.json")
    job = read_json(fixture_dir / "job.json")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 작업 산출은 검증보다 먼저 남긴다. 검증이 실패해도 지우지 않는다.
    artifact = output_dir / "synthetic-result.md"
    artifact.write_text("# 합성 산출물\n교육용 표식 파일입니다.\n", encoding="utf-8")
    missing = [name for name in request["required_conditions"] if name not in contract["satisfied_conditions"]]
    if not context.get("source_verified", False):
        missing.append("context.source_verified")
    files = set(job.get("files", []))
    for stage in job.get("stages", []):
        missing += [f"job.{stage}.{name}" for name in LIGHT_FILES.get(stage, []) if name not in files]
    approval = job.get("approval", {})
    if not (approval.get("approved_by") and approval.get("evidence")):
        missing.append("job.approval.evidence")
    status = "done" if not missing and artifact.is_file() else "partial"
    response = {
        "request_id": request["request_id"],
        "status": status,
        "artifact": artifact.name,
        "missing_conditions": missing,
    }
    (output_dir / "response.json").write_text(json.dumps(response, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return response
