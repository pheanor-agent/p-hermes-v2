"""Fixture-only knowledge provenance checks with no search side effects."""
from __future__ import annotations

import json
from pathlib import Path

ALLOWED_VALIDATION = {"validated", "unverified", "rejected", "unknown"}
ALLOWED_REVIEW = {"pending", "accepted", "rejected", "promoted", "unknown"}


def _known(value: object, allowed: set[str]) -> str:
    return value if isinstance(value, str) and value in allowed else "unknown"


def inspect(request_path: Path, lessons_path: Path) -> dict:
    """Inspect provided synthetic fixtures; never assert truth or promote."""
    request = json.loads(request_path.read_text(encoding="utf-8"))
    lessons = json.loads(lessons_path.read_text(encoding="utf-8"))
    query = request.get("query")
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be a non-empty string")
    if not isinstance(lessons, list):
        raise ValueError("lessons fixture must be a list")
    hits = [item for item in lessons if isinstance(item, dict) and query.casefold() in str(item.get("topic", "")).casefold()]
    if not hits:
        return {"status": "no_candidate", "scope": "fixtures_only", "items": []}
    items = []
    for item in hits:
        source, updated = item.get("source"), item.get("updated_at")
        items.append({
            "topic": item.get("topic", "unknown"),
            "source": source.strip() if isinstance(source, str) and source.strip() else "unknown",
            "updated_at": updated.strip() if isinstance(updated, str) and updated.strip() else "unknown",
            "validation_status": _known(item.get("validation_status"), ALLOWED_VALIDATION),
            "review_status": _known(item.get("review_status"), ALLOWED_REVIEW),
            "claim_verified": False,
            "promotion_performed": False,
        })
    return {"status": "candidates_found", "scope": "fixtures_only", "items": items}
