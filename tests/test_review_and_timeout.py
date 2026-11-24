"""Tests for request-bound collection, manager review decisions, timeouts, and duplicate warnings.

Only temporary directories and synthetic inputs are used.
"""
import json
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "reference"))
from filesystem_transport import read_json
from orchestrator import accept, check_duplicate, collect, request_file_digest, revise_request, submit
from worker import process_one, record_timeout


class ReviewAndTimeoutTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.inbox = self.root / "inbox"
        self.outbox = self.root / "outbox"
        self.reviews = self.root / "reviews"
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

    # 1. request-result binding
    def test_collect_binds_response_to_request_file_bytes(self):
        path = submit(self.request, self.inbox)
        result = process_one(path, self.outbox, self.allowed)
        self.assertEqual(result["request_sha256"], request_file_digest(path))
        self.assertEqual(collect("attempt-a", self.outbox, request_path=path), result)

    def test_collect_rejects_same_object_with_different_file_bytes(self):
        path = submit(self.request, self.inbox)
        process_one(path, self.outbox, self.allowed)
        # Same JSON object, different bytes (compact form): the digest is over file bytes, not the object.
        other = self.root / "compact.json"
        other.write_text(json.dumps(self.request, separators=(",", ":")), encoding="utf-8")
        self.assertEqual(read_json(other), read_json(path))
        with self.assertRaisesRegex(ValueError, "request_sha256"):
            collect("attempt-a", self.outbox, request_path=other)

    # 2. review decision separate from worker status
    def test_accept_records_decision_once(self):
        process_one(submit(self.request, self.inbox), self.outbox, self.allowed)
        record = accept("attempt-a", self.outbox, self.reviews, "accepted", note="checked")
        self.assertEqual(record["decision"], "accepted")
        self.assertEqual(record["response_status"], "done")
        self.assertEqual(read_json(self.reviews / "attempt-a.json"), record)
        self.assertEqual(accept("attempt-a", self.outbox, self.reviews, "accepted", note="checked"), record)
        with self.assertRaisesRegex(ValueError, "immutable"):
            accept("attempt-a", self.outbox, self.reviews, "needs_work", note="changed mind")
        self.assertEqual(read_json(self.reviews / "attempt-a.json")["decision"], "accepted")

    def test_done_is_not_acceptance_until_manager_decides(self):
        process_one(submit(self.request, self.inbox), self.outbox, self.allowed)
        self.assertFalse((self.reviews / "attempt-a.json").exists())

    def test_accept_refuses_without_terminal_response(self):
        with self.assertRaisesRegex(ValueError, "no terminal response"):
            accept("attempt-a", self.outbox, self.reviews, "accepted")
        self.outbox.mkdir(parents=True)
        (self.outbox / "attempt-a.json").write_text(
            json.dumps({"request_id": "attempt-a", "status": "running"}), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "not terminal"):
            accept("attempt-a", self.outbox, self.reviews, "accepted")

    def test_accept_refuses_unsafe_request_id(self):
        with self.assertRaisesRegex(ValueError, "safe filename"):
            accept("../escape", self.outbox, self.reviews, "accepted")
        self.assertFalse((self.root / "escape.json").exists())

    def test_accept_rejects_unknown_decision(self):
        process_one(submit(self.request, self.inbox), self.outbox, self.allowed)
        with self.assertRaisesRegex(ValueError, "decision must be"):
            accept("attempt-a", self.outbox, self.reviews, "done")

    def test_needs_work_requires_a_new_revision_not_an_edit(self):
        process_one(submit(self.request, self.inbox), self.outbox, self.allowed)
        accept("attempt-a", self.outbox, self.reviews, "needs_work", note="add a check")
        # Editing the same request_id with new intent is refused.
        edited = dict(self.request, acceptance="add a check")
        with self.assertRaisesRegex(ValueError, "immutable"):
            submit(edited, self.inbox)
        # The next attempt keeps goal_id, raises intent_revision, and gets a new request_id.
        second = revise_request(self.request, "attempt-a-r2", acceptance="add a check")
        self.assertEqual(second["goal_id"], "goal-a")
        self.assertEqual(second["intent_revision"], 2)
        path = submit(second, self.inbox)
        self.assertTrue(path.exists())
        self.assertIsNone(collect("attempt-a-r2", self.outbox))
        result = process_one(path, self.outbox, self.allowed)
        self.assertEqual(result["intent_revision"], 2)
        self.assertEqual(read_json(self.reviews / "attempt-a.json")["decision"], "needs_work")

    # 3. timeout record
    def test_record_timeout_publishes_failed_when_no_response(self):
        path = submit(self.request, self.inbox)
        record = record_timeout(path, self.outbox, 30)
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["error"], "timeout after 30s")
        self.assertEqual(record["request_sha256"], request_file_digest(path))
        self.assertEqual(collect("attempt-a", self.outbox, request_path=path), record)
        self.assertEqual(record_timeout(path, self.outbox, 30), record)

    def test_record_timeout_keeps_existing_response(self):
        path = submit(self.request, self.inbox)
        done = process_one(path, self.outbox, self.allowed)
        self.assertEqual(record_timeout(path, self.outbox, 30), done)
        self.assertEqual(read_json(self.outbox / "attempt-a.json"), done)

    def test_record_timeout_rejects_bad_seconds(self):
        path = submit(self.request, self.inbox)
        for bad in (0, -1, True, "30"):
            with self.assertRaisesRegex(ValueError, "positive number"):
                record_timeout(path, self.outbox, bad)

    # 4a. concurrency: documented limitation
    def test_limitation_two_workers_can_run_the_same_handler(self):
        """Known limit: there is no lease or lock, so two concurrent workers both run the handler.

        This test passes when the duplicate execution is observed. Both workers are forced into the
        handler at the same time with a barrier, so the overlap is deterministic.
        """
        path = submit(self.request, self.inbox)
        calls = []
        lock = threading.Lock()
        barrier = threading.Barrier(2, timeout=5)

        def handler(_request, _inputs):
            with lock:
                calls.append(threading.get_ident())
            barrier.wait()  # both workers are inside the handler at once
            return {"status": "done", "result": {"checked": True}}

        errors: list[BaseException] = []
        results: list[dict] = []

        def run():
            try:
                results.append(process_one(path, self.outbox, self.allowed, handler))
            except BaseException as exc:  # noqa: BLE001 - recorded and asserted below
                errors.append(exc)

        threads = [threading.Thread(target=run) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=20)
        self.assertEqual(errors, [])
        self.assertEqual(len(calls), 2, "duplicate execution is the documented limit")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], results[1])
        self.assertEqual(collect("attempt-a", self.outbox)["status"], "done")

    # 4b. duplicate warning
    def test_check_duplicate_lists_open_requests_for_same_goal(self):
        submit(self.request, self.inbox)  # attempt-a (the one being checked)
        submit(dict(self.request, request_id="attempt-b"), self.inbox)  # same goal, open
        closed = dict(self.request, request_id="attempt-c")
        submit(closed, self.inbox)
        process_one(self.inbox / "attempt-c.json", self.outbox, self.allowed)  # same goal, closed
        submit(dict(self.request, request_id="attempt-d", goal_id="goal-b"), self.inbox)  # other goal
        self.assertEqual(check_duplicate(self.request, self.inbox, self.outbox), ["attempt-b"])

    def test_check_duplicate_is_empty_for_new_goal(self):
        submit(self.request, self.inbox)
        self.assertEqual(check_duplicate(dict(self.request, goal_id="goal-new"), self.inbox, self.outbox), [])


if __name__ == "__main__":
    unittest.main()
