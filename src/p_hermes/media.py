"""Artifact byte verification, video timeline compilation and ffprobe QA."""
from __future__ import annotations

import json
import math
from pathlib import Path
import subprocess

from .core import ContractError, contained, digest, file_digest, identifier, require_text


def record_artifact(root: Path, relative: str, *, artifact_id: str, media_type: str,
                    license_ref: str, input_refs: list[str]) -> dict:
    identifier(artifact_id)
    require_text(license_ref, "license_ref")
    require_text(media_type, "media_type")
    if not isinstance(input_refs, list) or not all(isinstance(v, str) and v.strip() for v in input_refs):
        raise ContractError("input_refs must be a list of nonempty references")
    path = contained(root, relative)
    if not path.is_file():
        raise ContractError("artifact must be a regular file")
    return {"schema_version": 1, "id": artifact_id, "relative_uri": relative,
            "media_type": media_type, "license_ref": license_ref,
            "input_refs": list(input_refs), "sha256": file_digest(path),
            "size_bytes": path.stat().st_size}


def verify_artifact(root: Path, artifact: dict) -> Path:
    if not isinstance(artifact, dict):
        raise ContractError("artifact must be an object")
    path = contained(root, artifact.get("relative_uri"))
    if not path.is_file() or path.stat().st_size != artifact.get("size_bytes") or file_digest(path) != artifact.get("sha256"):
        raise ContractError("artifact bytes differ from the recorded hash/size")
    return path


def compile_timeline(root: Path, shots: list[dict], artifacts: list[dict]) -> dict:
    """Create consecutive cut intervals, verifying every referenced image file."""
    if not isinstance(shots, list) or not shots:
        raise ContractError("timeline needs at least one shot")
    if not isinstance(artifacts, list) or not all(isinstance(a, dict) for a in artifacts):
        raise ContractError("artifacts must be a list of objects")
    lookup = {}
    for artifact in artifacts:
        key = identifier(artifact.get("id"))
        if key in lookup:
            raise ContractError("duplicate artifact identifier")
        lookup[key] = artifact
    timeline, seen, cursor = [], set(), 0.0
    for shot in shots:
        if not isinstance(shot, dict):
            raise ContractError("shot must be an object")
        shot_id = identifier(shot.get("id"))
        if shot_id in seen:
            raise ContractError("duplicate shot identifier")
        seen.add(shot_id)
        duration = shot.get("duration_seconds")
        if type(duration) not in (int, float) or not math.isfinite(duration) or duration <= 0:
            raise ContractError("shot duration must be finite and positive")
        ref = shot.get("image_ref")
        if ref not in lookup or not lookup[ref].get("media_type", "").startswith("image/"):
            raise ContractError("shot must reference a registered image")
        verify_artifact(root, lookup[ref])
        require_text(shot.get("purpose"), "shot purpose")
        timeline.append({"id": shot_id, "start_seconds": cursor,
                         "end_seconds": cursor + duration, "image_ref": ref,
                         "image_sha256": lookup[ref]["sha256"], "purpose": shot["purpose"]})
        cursor += duration
        if not math.isfinite(cursor):
            raise ContractError("timeline duration overflow")
    result = {"schema_version": 1, "shots": timeline, "duration_seconds": cursor,
              "validation": "reference-bytes-checked"}
    return result | {"timeline_digest": digest(result)}


def inspect_video(path: Path, *, expected_duration: float | None = None,
                  tolerance: float = 0.1, ffprobe: str = "ffprobe") -> dict:
    """Probe an actual local file; no encoder, upload or provider call.

    ffprobe must already be installed. Parsing metadata cannot judge aesthetics,
    identity, continuity, factual correctness, or successful model generation.
    """
    path = Path(path).resolve(strict=True)
    if not path.is_file():
        raise ContractError("video must be a regular file")
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ContractError("duration tolerance must be nonnegative and finite")
    if expected_duration is not None and (not math.isfinite(expected_duration) or expected_duration <= 0):
        raise ContractError("expected duration must be finite and positive")
    try:
        response = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                                   "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate",
                                   "-of", "json", str(path)], capture_output=True, text=True,
                                  check=True, timeout=30)
        data = json.loads(response.stdout)
    except (subprocess.SubprocessError, OSError, json.JSONDecodeError) as exc:
        raise ContractError("ffprobe could not inspect this file") from exc
    video = [s for s in data.get("streams", []) if s.get("codec_type") == "video"]
    if not video or any(type(s.get("width")) is not int or s["width"] <= 0 or
                        type(s.get("height")) is not int or s["height"] <= 0 for s in video):
        raise ContractError("no valid video dimensions found")
    try:
        duration = float(data["format"]["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ContractError("video duration unavailable") from exc
    if not math.isfinite(duration) or duration <= 0:
        raise ContractError("invalid video duration")
    if expected_duration is not None and abs(duration - expected_duration) > tolerance:
        raise ContractError("encoded duration does not match timeline")
    return {"validation": "container-metadata-checked", "sha256": file_digest(path),
            "duration_seconds": duration, "video_streams": video,
            "audio_stream_count": sum(s.get("codec_type") == "audio" for s in data.get("streams", []))}
