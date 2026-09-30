import json
import tempfile
import unittest
from pathlib import Path

from integration_check import run

ROOT = Path(__file__).resolve().parents[1]


class IntegrationCheckTests(unittest.TestCase):
    def test_complete_flow_returns_matching_done_response(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(ROOT / "fixtures/pass", Path(tmp))
            self.assertEqual(result["request_id"], "synthetic-integration-001")
            self.assertEqual(result["status"], "done")
            self.assertEqual(result["missing_conditions"], [])
            self.assertTrue((Path(tmp) / result["artifact"]).is_file())

    def test_unconfirmed_input_returns_partial_and_keeps_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run(ROOT / "fixtures/missing", Path(tmp))
            self.assertEqual(result["request_id"], "synthetic-integration-002")
            self.assertEqual(result["status"], "partial")
            self.assertIn("context.source_verified", result["missing_conditions"])
            self.assertTrue((Path(tmp) / result["artifact"]).is_file())
            saved = json.loads((Path(tmp) / "response.json").read_text(encoding="utf-8"))
            self.assertEqual(saved, result)


if __name__ == "__main__":
    unittest.main()
