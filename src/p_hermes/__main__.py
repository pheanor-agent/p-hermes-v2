"""Local CLI. All writes go to explicitly chosen output paths."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .catalog import compile_image, resolve
from .core import ContractError, digest
from .media import compile_timeline, inspect_video, record_artifact, verify_artifact
from .store import Store


def read_json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContractError("input JSON must be an object")
    return value


def write_json(path, value):
    # Exclusive creation protects previous experiments from accidental overwrite.
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")


def demo(output: Path) -> dict:
    """Execute a synthetic, persistent integration scenario in a new directory."""
    output.mkdir(parents=True, exist_ok=False)
    knowledge = {"id": "composition-note", "title": "Lamp composition",
                 "body": "Place a teal lamp with warm light at left; reserve the right for text.",
                 "source_ref": "synthetic:studio-brief", "license_ref": "CC0-1.0", "public": True}
    entry = {"id": "layout-workflow", "version": "1.0", "operation": "image",
             "runtime": "example-graph-v1", "state": "active", "health": "healthy",
             "license_ref": "MIT", "bindings": {"prompt": ["text", "prompt"],
             "width": ["canvas", "width"], "height": ["canvas", "height"], "seed": ["noise", "seed"]}}
    spec = {"prompt": knowledge["body"], "width": 1280, "height": 720, "seed": 42}
    template = {"text": {"inputs": {"prompt": ""}}, "canvas": {"inputs": {"width": 0, "height": 0}},
                "noise": {"inputs": {"seed": 0}}}
    entry["template_digest"] = digest(template)
    selection = resolve([entry], asset_id=entry["id"], version=entry["version"],
                        operation="image", runtime="example-graph-v1")
    compiled = compile_image(spec, selection, template)
    plan = {"purpose": "Prepare a two-shot lamp storyboard", "knowledge_refs": [knowledge["id"]],
            "catalog_digest": selection["digest"], "image_spec": spec}
    with Store(output / "workspace.sqlite3") as store:
        store.register_knowledge(knowledge)
        job = store.create_job("studio-demo", plan)
        job = store.act(job["id"], job["revision"], "approve", approved_digest=job["plan_digest"])
        job = store.act(job["id"], job["revision"], "start")
        # A hand-authored SVG storyboard is a real file; it is not model output.
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720">'
               '<rect width="1280" height="720" fill="#172c2a"/>'
               '<path d="M180 400h360l100 270H80z" fill="#ffc982" opacity="0.12"/>'
               '<path d="M240 220h240l80 180H160z" fill="#286675"/>'
               '<path d="M360 400v180m-100 0h200" stroke="#eddbc3" stroke-width="18"/>'
               '<rect x="740" y="210" width="370" height="260" rx="16" fill="none" '
               'stroke="#9baaa2" stroke-width="3" stroke-dasharray="12 12"/></svg>')
        (output / "storyboard.svg").write_text(svg, encoding="utf-8")
        artifact = record_artifact(output, "storyboard.svg", artifact_id="lamp-frame", media_type="image/svg+xml",
                                   license_ref="CC0-1.0", input_refs=[job["plan_digest"], selection["digest"]])
        shots = [{"id": "establish", "duration_seconds": 2, "image_ref": artifact["id"], "purpose": "Establish composition"},
                 {"id": "hold", "duration_seconds": 3, "image_ref": artifact["id"], "purpose": "Hold for the message"}]
        timeline = compile_timeline(output, shots, [artifact])
        write_json(output / "image-plan.json", compiled)
        write_json(output / "artifact.json", artifact)
        write_json(output / "timeline.json", timeline)
        job = store.act(job["id"], job["revision"], "complete", evidence="Storyboard bytes and five-second timeline verified; no model or video encoding run.")
        report = {"job": job, "events": store.events(job["id"]), "knowledge_hits": store.search("lamp"),
                  "artifact": artifact, "timeline": timeline,
                  "execution": {"persistent_store": True, "image_binding_compile": True,
                                "storyboard_file": True, "reference_hashes": True,
                                "model_inference": False, "video_encoding": False}}
        write_json(output / "report.json", report)
    # Reopen, rather than treating in-memory returns as persistence evidence.
    with Store(output / "workspace.sqlite3") as reopened:
        if reopened.job("studio-demo")["state"] != "completed":
            raise ContractError("persistence verification failed")
    return {"status": "completed", "report": str(output / "report.json"), "model_inference": False, "video_encoding": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run = sub.add_parser("demo", help="run a synthetic integration with persistent outputs")
    run.add_argument("--output", type=Path, required=True, help="new directory, must not exist")
    image = sub.add_parser("compile-image", help="bind a pinned catalog to an image workflow")
    image.add_argument("input", type=Path, help="JSON with catalog, pin, spec and template")
    image.add_argument("output", type=Path, help="new JSON file")
    timeline = sub.add_parser("compile-timeline", help="verify image references and compile shot intervals")
    timeline.add_argument("input", type=Path, help="JSON with shots and artifacts")
    timeline.add_argument("--root", type=Path, required=True)
    timeline.add_argument("--output", type=Path, required=True)
    verify = sub.add_parser("verify-artifact", help="check recorded bytes and workspace containment")
    verify.add_argument("input", type=Path)
    verify.add_argument("--root", type=Path, required=True)
    probe = sub.add_parser("inspect-video", help="inspect a real video with installed ffprobe")
    probe.add_argument("file", type=Path)
    probe.add_argument("--duration", type=float)
    job = sub.add_parser("job", help="persist and inspect a local revisioned job")
    job.add_argument("--db", type=Path, required=True)
    job_commands = job.add_subparsers(dest="job_command", required=True)
    create = job_commands.add_parser("create")
    create.add_argument("id")
    create.add_argument("plan", type=Path)
    show = job_commands.add_parser("show")
    show.add_argument("id")
    act = job_commands.add_parser("act")
    act.add_argument("id")
    act.add_argument("revision", type=int)
    act.add_argument("action", choices=["revise", "approve", "start", "complete", "fail", "unknown", "reconcile_complete", "reconcile_fail"])
    act.add_argument("--plan", type=Path)
    act.add_argument("--approved-digest")
    act.add_argument("--evidence")
    knowledge = sub.add_parser("knowledge", help="register, search or retire local public knowledge")
    knowledge.add_argument("--db", type=Path, required=True)
    knowledge_commands = knowledge.add_subparsers(dest="knowledge_command", required=True)
    register = knowledge_commands.add_parser("register")
    register.add_argument("input", type=Path)
    search = knowledge_commands.add_parser("search")
    search.add_argument("query")
    retire = knowledge_commands.add_parser("retire")
    retire.add_argument("id")
    args = parser.parse_args(argv)
    try:
        if args.command == "demo":
            result = demo(args.output)
        elif args.command == "compile-image":
            data = read_json(args.input)
            selected = resolve(data["catalog"], **data["pin"])
            result = compile_image(data["spec"], selected, data["template"])
            write_json(args.output, result)
        elif args.command == "compile-timeline":
            data = read_json(args.input)
            result = compile_timeline(args.root, data["shots"], data["artifacts"])
            write_json(args.output, result)
        elif args.command == "verify-artifact":
            verify_artifact(args.root, read_json(args.input))
            result = {"validation": "bytes-checked"}
        elif args.command == "job":
            with Store(args.db) as store:
                if args.job_command == "create":
                    result = store.create_job(args.id, read_json(args.plan))
                elif args.job_command == "show":
                    result = {"job": store.job(args.id), "events": store.events(args.id)}
                else:
                    result = store.act(args.id, args.revision, args.action,
                                       plan=read_json(args.plan) if args.plan else None,
                                       approved_digest=args.approved_digest, evidence=args.evidence)
        elif args.command == "knowledge":
            with Store(args.db) as store:
                if args.knowledge_command == "register":
                    store.register_knowledge(read_json(args.input))
                    result = {"status": "registered"}
                elif args.knowledge_command == "search":
                    result = {"results": store.search(args.query)}
                else:
                    store.retire_knowledge(args.id)
                    result = {"status": "retired"}
        else:
            result = inspect_video(args.file, expected_duration=args.duration)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ContractError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
