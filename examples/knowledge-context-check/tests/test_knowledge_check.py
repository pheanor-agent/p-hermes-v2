from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from knowledge_check import inspect


class KnowledgeCheckTests(unittest.TestCase):
    def test_candidates_preserve_pending_and_do_not_verify_claims(self):
        result = inspect(ROOT / "fixtures/request.json", ROOT / "fixtures/lessons.json")
        self.assertEqual(result["status"], "candidates_found")
        self.assertEqual(result["scope"], "fixtures_only")
        self.assertEqual(len(result["items"]), 2)
        self.assertTrue(all(item["review_status"] == "pending" for item in result["items"]))
        self.assertTrue(all(item["claim_verified"] is False for item in result["items"]))
        self.assertTrue(all(item["promotion_performed"] is False for item in result["items"]))

    def test_missing_source_date_and_validation_remain_unknown(self):
        item = inspect(ROOT / "fixtures/request.json", ROOT / "fixtures/lessons.json")["items"][1]
        self.assertEqual(item["source"], "unknown")
        self.assertEqual(item["updated_at"], "unknown")
        self.assertEqual(item["validation_status"], "unknown")

    def test_no_match_is_fixture_scoped(self):
        result = inspect(ROOT / "fixtures/no-match-request.json", ROOT / "fixtures/lessons.json")
        self.assertEqual(result, {"status": "no_candidate", "scope": "fixtures_only", "items": []})

    def test_invalid_request_fails_closed(self):
        with self.assertRaises(ValueError):
            inspect(ROOT / "fixtures/invalid-request.json", ROOT / "fixtures/lessons.json")


if __name__ == "__main__":
    unittest.main()
