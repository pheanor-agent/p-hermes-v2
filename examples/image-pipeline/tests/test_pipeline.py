"""합성 fixture로 입력, 어댑터, fake runtime, 결과 계약을 검증한다."""
import json
from pathlib import Path
import tempfile
import unittest

from image_pipeline_demo import (
    CatalogEntry, FakeRuntime, GenericAdapter, GenerationResult, SceneIntent,
    compile_prompt, load_catalog, load_intent, run, validate_result,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


class PipelineContractTests(unittest.TestCase):
    def test_fixture_runs_without_creating_real_image(self):
        result = run(FIXTURES / "request.json", FIXTURES / "catalog.json")
        self.assertEqual(result["status"], "simulated")
        self.assertEqual(result["request_id"], "synthetic-request-01")
        self.assertEqual(result["output_marker"], "synthetic://synthetic-request-01.webp")
        self.assertEqual(result["aspect_ratio"], "16:9")
        self.assertIn("스타일: 선명한 평면 도해", result["prompt"])
        self.assertFalse((FIXTURES / "synthetic-request-01.webp").exists())

    def test_seven_segments_keep_order_and_optional_constraints(self):
        intent = SceneIntent("도형", "연결", "배경", "정면", "부드러운 빛", "", "")
        prompt = compile_prompt(intent, CatalogEntry("demo", "단순한 도해", "1:1"))
        self.assertEqual(prompt, "주제: 도형 / 행동: 연결 / 장소: 배경 / 카메라: 정면 / 조명: 부드러운 빛 / 스타일: 단순한 도해")
        self.assertNotIn("제약:", prompt)

    def test_missing_required_intent_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "request.json"
            path.write_text(json.dumps({"request_id": "r", "catalog": "soft-diagram", "intent": {"subject": "", "action": ""}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "주제와 행동"):
                load_intent(path)

    def test_unknown_catalog_is_rejected_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "request.json"
            path.write_text(json.dumps({"request_id": "r", "catalog": "unknown", "intent": {"subject": "도형", "action": "연결"}}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "카탈로그 항목을 찾을 수 없음"):
                run(path, FIXTURES / "catalog.json")

    def test_fake_runtime_result_matches_request_and_prompt(self):
        prompt = "주제: 도형 / 행동: 연결"
        runtime = FakeRuntime()
        result = runtime.generate("r-1", prompt, CatalogEntry("demo", "평면", "1:1"))
        validate_result(result, "r-1", prompt)
        with self.assertRaisesRegex(ValueError, "요청과 다름"):
            validate_result(result, "r-2", prompt)
        with self.assertRaisesRegex(ValueError, "지문이 다름"):
            validate_result(result, "r-1", prompt + " 변경")

    def test_duplicate_catalog_names_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "catalog.json"
            path.write_text(json.dumps({"schema": "synthetic-image-catalog/v1", "entries": [
                {"name": "same", "style": "a", "aspect_ratio": "1:1"},
                {"name": "same", "style": "b", "aspect_ratio": "16:9"},
            ]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "비어 있거나 이름이 중복"):
                load_catalog(path)

    def test_adapter_exposes_only_the_demo_string_contract(self):
        prompt = GenericAdapter().adapt(SceneIntent("도형", "이어짐"), CatalogEntry("demo", "선명한 평면", "16:9"))
        self.assertTrue(prompt.startswith("주제: 도형 / 행동: 이어짐"))
        self.assertLess(len(prompt), 500)


if __name__ == "__main__":
    unittest.main()
