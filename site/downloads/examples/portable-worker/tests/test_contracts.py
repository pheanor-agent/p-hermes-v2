"""Contract tests use only temporary directories and synthetic inputs."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from filesystem_transport import read_json, write_json_atomic
from orchestrator import collect, submit
from worker import process_one


class ContractsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inbox = self.root / "inbox"
        self.outbox = self.root / "outbox"
        self.allowed = self.root / "allowed"
        self.allowed.mkdir()
        (self.allowed / "brief.txt").write_text("synthetic input", encoding="utf-8")
        self.request = {
            "request_id": "attempt-a",
            "goal_id": "goal-a",
            "intent_revision": 1,
            "inputs": ["brief.txt"],
            "acceptance": "produce a terminal receipt",
            "policy": {"allowed_root": "fixture"},
        }

    def tearDown(self):
        self.temp.cleanup()

    def test_submit_is_idempotent_only_for_identical_attempt(self):
        first = submit(self.request, self.inbox)
        self.assertEqual(first.read_text(), (self.inbox / "attempt-a.json").read_text())
        self.assertEqual(submit(self.request, self.inbox), first)
        changed = dict(self.request, acceptance="different intent")
        with self.assertRaisesRegex(ValueError, "immutable"):
            submit(changed, self.inbox)

    def test_request_id_cannot_escape_inbox_or_outbox(self):
        bad = dict(self.request, request_id="../escape")
        with self.assertRaisesRegex(ValueError, "safe filename"):
            submit(bad, self.inbox)

    def test_atomic_write_refuses_overwrite(self):
        target = self.root / "one.json"
        write_json_atomic(target, {"value": 1})
        with self.assertRaises(FileExistsError):
            write_json_atomic(target, {"value": 2})
        self.assertEqual(read_json(target), {"value": 1})
        self.assertEqual(list(self.root.glob(".one.json.*.tmp")), [])

    def test_worker_writes_done_and_collect_matches_attempt(self):
        request_path = submit(self.request, self.inbox)
        result = process_one(request_path, self.outbox, self.allowed)
        self.assertEqual(result["status"], "done")
        self.assertEqual(result["request_id"], "attempt-a")
        self.assertEqual(collect("attempt-a", self.outbox), result)

    def test_path_traversal_is_blocked(self):
        bad = dict(self.request, request_id="attempt-bad", inputs=["../secret.txt"])
        path = submit(bad, self.inbox)
        result = process_one(path, self.outbox, self.allowed)
        self.assertEqual(result["status"], "blocked")
        self.assertIn("allowlisted", result["error"])

    def test_missing_acceptance_is_blocked(self):
        request = dict(self.request, request_id="attempt-no-acceptance")
        del request["acceptance"]
        path = self.inbox / "attempt-no-acceptance.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(request), encoding="utf-8")
        result = process_one(path, self.outbox, self.allowed)
        self.assertEqual(result["status"], "blocked")

    def test_non_object_policy_is_blocked(self):
        request = dict(self.request, request_id="attempt-bad-policy", policy="allowed")
        path = self.inbox / "attempt-bad-policy.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(request), encoding="utf-8")
        result = process_one(path, self.outbox, self.allowed)
        self.assertEqual(result["status"], "blocked")

    def test_symlink_escape_is_blocked(self):
        outside = self.root / "outside.txt"
        outside.write_text("not allowed", encoding="utf-8")
        (self.allowed / "escape.txt").symlink_to(outside)
        bad = dict(self.request, request_id="attempt-link", inputs=["escape.txt"])
        result = process_one(submit(bad, self.inbox), self.outbox, self.allowed)
        self.assertEqual(result["status"], "blocked")

    def test_handler_exception_is_failed(self):
        def broken(_request, _inputs):
            raise RuntimeError("synthetic failure")
        result = process_one(submit(self.request, self.inbox), self.outbox, self.allowed, broken)
        self.assertEqual(result["status"], "failed")
        self.assertIn("RuntimeError", result["error"])

    def test_exception_with_artifact_is_partial_and_preserves_path(self):
        artifact = self.root / "partial.txt"
        artifact.write_text("kept", encoding="utf-8")
        def partially_done(_request, _inputs):
            error = RuntimeError("later stage failed")
            error.artifacts = [str(artifact)]
            raise error
        result = process_one(submit(self.request, self.inbox), self.outbox, self.allowed, partially_done)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["artifacts"], [str(artifact)])
        self.assertTrue(artifact.exists())

    def test_existing_terminal_response_is_not_reprocessed(self):
        path = submit(self.request, self.inbox)
        first = process_one(path, self.outbox, self.allowed)
        second = process_one(path, self.outbox, self.allowed, lambda *_: self.fail("reprocessed"))
        self.assertEqual(second, first)

    def test_collect_rejects_wrong_response_identity(self):
        self.outbox.mkdir()
        (self.outbox / "attempt-a.json").write_text(json.dumps({"request_id": "other", "status": "done"}))
        with self.assertRaisesRegex(ValueError, "does not match"):
            collect("attempt-a", self.outbox)


if __name__ == "__main__":
    unittest.main()
