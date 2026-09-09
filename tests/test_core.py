"""Failure-oriented tests for the reusable public runtime."""
from copy import deepcopy
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

from p_hermes.__main__ import demo, main
from p_hermes.catalog import compile_image, resolve
from p_hermes.core import ContractError, digest
from p_hermes.media import compile_timeline, inspect_video, record_artifact, verify_artifact
from p_hermes.store import Store


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = Store(self.root / "workspace.sqlite3")

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def job(self):
        return self.store.create_job("job-1", {"purpose": "Test independent workflow"})

    def test_competing_client_rejects_stale_revision(self):
        job = self.job()
        with Store(self.root / "workspace.sqlite3") as other:
            snapshot = other.job(job["id"])
            self.store.act(job["id"], 0, "approve", approved_digest=job["plan_digest"])
            with self.assertRaisesRegex(ContractError, "stale revision"):
                other.act(job["id"], snapshot["revision"], "revise", plan={"purpose": "new"})
        self.assertEqual(len(self.store.events(job["id"])), 2)

    def test_revision_type_and_invalid_json_are_rejected(self):
        job = self.job()
        for revision in (False, True, 0.0, -1):
            with self.assertRaises(ContractError):
                self.store.act(job["id"], revision, "approve", approved_digest=job["plan_digest"])
        for invalid in (float("nan"), object(), "\ud800"):
            with self.assertRaises(ContractError):
                self.store.create_job("invalid", {"purpose": "invalid input", "value": invalid})
        self.assertEqual(self.store.job(job["id"])["revision"], 0)

    def test_event_failure_rolls_back_state_change(self):
        job = self.job()
        with patch.object(self.store, "_event", side_effect=sqlite3.OperationalError("injected disk failure")):
            with self.assertRaises(sqlite3.OperationalError):
                self.store.act(job["id"], 0, "approve", approved_digest=job["plan_digest"])
        self.assertEqual(self.store.job(job["id"])["state"], "draft")
        self.assertEqual(len(self.store.events(job["id"])), 1)

    def test_revised_plan_clears_approval(self):
        job = self.job()
        self.store.act(job["id"], 0, "approve", approved_digest=job["plan_digest"])
        revised = self.store.act(job["id"], 1, "revise", plan={"purpose": "changed"})
        self.assertIsNone(revised["approved_digest"])
        with self.assertRaises(ContractError):
            self.store.act(job["id"], 2, "start")
        with self.assertRaises(ContractError):
            self.store.act(job["id"], 2, "approve", approved_digest=job["plan_digest"])

    def test_unknown_outcome_requires_reconciliation(self):
        job = self.job()
        self.store.act(job["id"], 0, "approve", approved_digest=job["plan_digest"])
        self.store.act(job["id"], 1, "start")
        self.store.act(job["id"], 2, "unknown", evidence="Provider request timed out")
        with self.assertRaises(ContractError):
            self.store.act(job["id"], 3, "start")
        with self.assertRaises(ContractError):
            self.store.act(job["id"], 3, "reconcile_complete", evidence="")
        done = self.store.act(job["id"], 3, "reconcile_complete", evidence="Provider result verified by receipt")
        self.assertEqual(done["state"], "completed")

    def test_knowledge_unique_public_and_retirement(self):
        item = {"id": "note", "title": "Lamp", "body": "Warm light", "source_ref": "synthetic:brief", "license_ref": "CC0", "public": True}
        with self.assertRaises(ContractError):
            self.store.register_knowledge(item | {"id": "../../escape"})
        with self.assertRaises(ContractError):
            self.store.register_knowledge(item | {"public": False})
        self.store.register_knowledge(item)
        with self.assertRaises(ContractError):
            self.store.register_knowledge(item)
        self.assertEqual(len(self.store.search("LAMP")), 1)
        self.assertEqual(self.store.search("%"), [])
        self.store.retire_knowledge("note")
        self.assertEqual(self.store.search("lamp"), [])

    def image_input(self):
        return json.loads((Path(__file__).parents[1] / "examples/image-request.json").read_text())

    def test_catalog_ambiguity_compatibility_and_drift(self):
        data = self.image_input()
        catalog, pin = data["catalog"], data["pin"]
        selected = resolve(catalog, **pin)
        with self.assertRaises(ContractError):
            resolve(catalog * 2, **pin)
        with self.assertRaises(ContractError):
            resolve(catalog, **(pin | {"runtime": "unavailable"}))
        changed = deepcopy(catalog)
        changed[0]["license_ref"] = "different"
        with self.assertRaises(ContractError):
            resolve(changed, **pin, expected_digest=selected["digest"])

    def test_compiler_preserves_inputs_and_binds_all_fields(self):
        data = self.image_input()
        before = deepcopy(data)
        selected = resolve(data["catalog"], **data["pin"])
        output = compile_image(data["spec"], selected, data["template"])
        self.assertEqual(data, before)
        self.assertEqual(output["workflow"]["noise"]["inputs"]["seed"], 42)
        self.assertEqual(output["workflow_digest"], digest(output["workflow"]))
        for field in data["spec"]:
            malformed = dict(data["spec"])
            del malformed[field]
            with self.assertRaises(ContractError):
                compile_image(malformed, selected, data["template"])

    def test_compiler_rejects_missing_and_overlapping_slots(self):
        data = self.image_input()
        for replacement in (["missing", "width"], ["canvas", "height"]):
            entry = deepcopy(data["catalog"][0])
            entry["bindings"]["width"] = replacement
            selected = resolve([entry], **data["pin"])
            with self.assertRaises(ContractError):
                compile_image(data["spec"], selected, data["template"])

    def test_template_drift_blocked_even_outside_bound_slots(self):
        data = self.image_input()
        selected = resolve(data["catalog"], **data["pin"])
        altered = deepcopy(data["template"])
        altered["extra-node"] = {"inputs": {"unreviewed": True}}
        with self.assertRaisesRegex(ContractError, "template changed"):
            compile_image(data["spec"], selected, altered)

    def artifact(self):
        (self.root / "frame.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        return record_artifact(self.root, "frame.svg", artifact_id="frame", media_type="image/svg+xml", license_ref="CC0", input_refs=[])

    def test_artifact_tampering_and_escape(self):
        artifact = self.artifact()
        verify_artifact(self.root, artifact)
        for path in ("../frame.svg", "C:/private.txt", "dir/../../private.txt", "dir\\private.txt"):
            with self.assertRaises(ContractError):
                verify_artifact(self.root, artifact | {"relative_uri": path})
        (self.root / "frame.svg").write_text("tampered")
        with self.assertRaises(ContractError):
            verify_artifact(self.root, artifact)

    def test_symlink_artifact_rejected(self):
        artifact = self.artifact()
        try:
            (self.root / "link.svg").symlink_to(self.root / "frame.svg")
        except OSError:
            self.skipTest("OS does not permit unprivileged symlink creation")
        with self.assertRaises(ContractError):
            verify_artifact(self.root, artifact | {"relative_uri": "link.svg"})

    def test_timeline_reference_bytes_and_duration(self):
        artifact = self.artifact()
        shot = {"id": "one", "image_ref": "frame", "duration_seconds": 2.5, "purpose": "Introduce"}
        result = compile_timeline(self.root, [shot, shot | {"id": "two"}], [artifact])
        self.assertEqual(result["duration_seconds"], 5)
        self.assertEqual(result["shots"][1]["start_seconds"], 2.5)
        for duration in (True, 0, -1, float("nan"), float("inf")):
            with self.assertRaises(ContractError):
                compile_timeline(self.root, [shot | {"duration_seconds": duration}], [artifact])
        with self.assertRaises(ContractError):
            compile_timeline(self.root, [shot, shot], [artifact])
        (self.root / "frame.svg").write_text("changed")
        with self.assertRaises(ContractError):
            compile_timeline(self.root, [shot], [artifact])

    def test_probe_rejects_invalid_stream_and_duration(self):
        path = self.root / "video.mp4"
        path.write_bytes(b"fake only for mocked ffprobe failure paths")
        class Response:
            stdout = json.dumps({"streams": [{"codec_type": "video", "width": 1280, "height": 720}], "format": {"duration": "2.0"}})
        with patch("p_hermes.media.subprocess.run", return_value=Response()):
            self.assertEqual(inspect_video(path, expected_duration=2)["duration_seconds"], 2)
            with self.assertRaises(ContractError):
                inspect_video(path, expected_duration=5)
        Response.stdout = '{"streams":[],"format":{"duration":"2"}}'
        with patch("p_hermes.media.subprocess.run", return_value=Response()):
            with self.assertRaises(ContractError):
                inspect_video(path)

    def test_demo_persists_and_does_not_overwrite(self):
        output = self.root / "demo"
        result = demo(output)
        self.assertEqual(result["status"], "completed")
        with Store(output / "workspace.sqlite3") as store:
            self.assertEqual(store.job("studio-demo")["state"], "completed")
            self.assertEqual(len(store.events("studio-demo")), 4)
        report = json.loads((output / "report.json").read_text())
        verify_artifact(output, report["artifact"])
        self.assertFalse(report["execution"]["model_inference"])
        with self.assertRaises(FileExistsError):
            demo(output)

    def test_cli_malformed_input_exits_nonzero(self):
        file = self.root / "bad.json"
        file.write_text('{"catalog":[]}')
        self.assertEqual(main(["compile-image", str(file), str(self.root / "output.json")]), 2)
        self.assertFalse((self.root / "output.json").exists())
        file.write_text("[]")
        self.assertEqual(main(["compile-image", str(file), str(self.root / "output.json")]), 2)


if __name__ == "__main__":
    unittest.main()
