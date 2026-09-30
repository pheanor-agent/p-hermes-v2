from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from contract_check import check


class ContractCheckTests(unittest.TestCase):
    def test_complete_fixture_passes(self):
        ok, missing = check(ROOT / "fixtures/pass/request.json", ROOT / "fixtures/pass/artifacts")
        self.assertTrue(ok)
        self.assertEqual(missing, [])

    def test_missing_required_artifact_fails_with_path(self):
        ok, missing = check(ROOT / "fixtures/missing/request.json", ROOT / "fixtures/missing/artifacts")
        self.assertFalse(ok)
        self.assertEqual(missing, ["verification.md"])


if __name__ == "__main__":
    unittest.main()
