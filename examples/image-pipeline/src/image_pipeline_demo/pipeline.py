"""합성 입력으로 이미지 생성 파이프라인의 데이터 계약을 보여준다."""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CatalogEntry:
    name: str
    style: str
    aspect_ratio: str


@dataclass(frozen=True)
class SceneIntent:
    subject: str
    action: str
    location: str = ""
    camera: str = ""
    lighting: str = ""
    style: str = ""
    constraints: str = ""


@dataclass(frozen=True)
class GenerationResult:
    request_id: str
    status: str
    prompt_sha256: str
    output_marker: str


SEGMENTS = ("subject", "action", "location", "camera", "lighting", "style", "constraints")


def load_catalog(path: Path) -> dict[str, CatalogEntry]:
    """합성 카탈로그를 읽고 고유 이름과 필수 기본값을 검사한다."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "synthetic-image-catalog/v1":
        raise ValueError("지원하지 않는 카탈로그 형식")
    entries: dict[str, CatalogEntry] = {}
    for row in payload.get("entries", []):
        name = str(row.get("name", "")).strip()
        style = str(row.get("style", "")).strip()
        ratio = str(row.get("aspect_ratio", "")).strip()
        if not name or not style or not ratio or name in entries:
            raise ValueError("카탈로그 항목이 비어 있거나 이름이 중복됨")
        entries[name] = CatalogEntry(name, style, ratio)
    if not entries:
        raise ValueError("카탈로그 항목이 없음")
    return entries


def load_intent(path: Path) -> tuple[str, SceneIntent]:
    """요청에서 식별자, 카탈로그 선택, 일곱 관점의 의도를 읽는다."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    request_id = str(payload.get("request_id", "")).strip()
    catalog_name = str(payload.get("catalog", "")).strip()
    raw = payload.get("intent")
    if not request_id or not catalog_name or not isinstance(raw, dict):
        raise ValueError("요청 식별자, 카탈로그 또는 의도가 누락됨")
    values = {key: str(raw.get(key, "")).strip() for key in SEGMENTS}
    if not values["subject"] or not values["action"]:
        raise ValueError("주제와 행동은 필수")
    return request_id, SceneIntent(**values)


def compile_prompt(intent: SceneIntent, entry: CatalogEntry) -> str:
    """고정된 일곱 관점 순서로 장면 의도를 컴파일한다."""
    effective = asdict(intent)
    effective["style"] = effective["style"] or entry.style
    labels = {
        "subject": "주제", "action": "행동", "location": "장소",
        "camera": "카메라", "lighting": "조명", "style": "스타일",
        "constraints": "제약",
    }
    parts = [f"{labels[key]}: {effective[key]}" for key in SEGMENTS if effective[key]]
    return " / ".join(parts)


class GenericAdapter:
    """데모용 백엔드 중립 문자열 어댑터. 모델 API payload는 만들지 않는다."""

    def adapt(self, intent: SceneIntent, entry: CatalogEntry) -> str:
        prompt = compile_prompt(intent, entry)
        if not prompt or "주제:" not in prompt or "행동:" not in prompt:
            raise ValueError("어댑터 출력 계약 위반")
        return prompt


class FakeRuntime:
    """네트워크·GPU 없이 결정론적 합성 결과 메타데이터를 반환한다."""

    def generate(self, request_id: str, prompt: str, entry: CatalogEntry) -> GenerationResult:
        if not request_id.strip() or not prompt.strip():
            raise ValueError("식별자와 프롬프트가 필요함")
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        return GenerationResult(request_id, "simulated", digest, f"synthetic://{request_id}.webp")


def validate_result(result: GenerationResult, request_id: str, prompt: str) -> None:
    """실제 이미지 대신 합성 실행의 식별자·상태·지문 계약을 확인한다."""
    expected = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    if result.request_id != request_id:
        raise ValueError("응답 식별자가 요청과 다름")
    if result.status != "simulated" or result.output_marker != f"synthetic://{request_id}.webp":
        raise ValueError("합성 결과 상태 또는 표식이 잘못됨")
    if result.prompt_sha256 != expected:
        raise ValueError("프롬프트 지문이 다름")


def run(request_path: Path, catalog_path: Path) -> dict[str, Any]:
    request_id, intent = load_intent(request_path)
    catalog = load_catalog(catalog_path)
    name = json.loads(request_path.read_text(encoding="utf-8"))["catalog"]
    if name not in catalog:
        raise ValueError(f"카탈로그 항목을 찾을 수 없음: {name}")
    entry = catalog[name]
    prompt = GenericAdapter().adapt(intent, entry)
    result = FakeRuntime().generate(request_id, prompt, entry)
    validate_result(result, request_id, prompt)
    return {"request_id": result.request_id, "status": result.status,
            "prompt": prompt, "prompt_sha256": result.prompt_sha256,
            "output_marker": result.output_marker,
            "aspect_ratio": entry.aspect_ratio,
            "note": "합성 예제 결과이며 실제 이미지 생성·게시를 수행하지 않음"}
