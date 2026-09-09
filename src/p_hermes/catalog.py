"""Pinned catalog resolution and explicit workflow input compilation.

This public contract is independent of operational YAML and workflow engines.
It accepts caller-provided catalogs, never discovers local models or secrets.
"""
from __future__ import annotations

from copy import deepcopy
from .core import ContractError, digest, identifier, require_text


def resolve(entries: list[dict], *, asset_id: str, version: str,
            operation: str, runtime: str, expected_digest: str | None = None) -> dict:
    if not isinstance(entries, list) or not all(isinstance(entry, dict) for entry in entries):
        raise ContractError("catalog must be a list of objects")
    matches = [entry for entry in entries if entry.get("id") == asset_id and entry.get("version") == version]
    if len(matches) != 1:
        raise ContractError("catalog pin must match exactly one entry")
    entry = matches[0]
    identifier(entry.get("id"))
    require_text(entry.get("version"), "catalog version")
    require_text(entry.get("license_ref"), "catalog license_ref")
    if entry.get("state") != "active" or entry.get("health") != "healthy":
        raise ContractError("catalog entry must be active and healthy")
    if entry.get("operation") != operation or entry.get("runtime") != runtime:
        raise ContractError("catalog operation/runtime mismatch")
    actual = digest(entry)
    if expected_digest is not None and actual != expected_digest:
        raise ContractError("catalog changed since pinning")
    return {"entry": deepcopy(entry), "digest": actual}


def compile_image(spec: dict, selection: dict, template: dict) -> dict:
    """Bind only declared slots; validate both inputs and compiled output.

    Every template node has an inputs mapping. Catalog bindings map public fields
    to [node_id, input_name]. No arbitrary graph insertion, hidden default or LLM.
    The caller receives a new graph; all inputs remain unchanged.
    """
    if not all(isinstance(value, dict) for value in (spec, selection, template)):
        raise ContractError("spec, selection and template must be objects")
    entry = selection.get("entry", {})
    if not isinstance(entry, dict):
        raise ContractError("selection entry must be an object")
    if digest(entry) != selection.get("digest"):
        raise ContractError("selection digest mismatch")
    if digest(template) != entry.get("template_digest"):
        raise ContractError("workflow template changed since catalog release")
    if entry.get("operation") != "image" or entry.get("state") != "active" or entry.get("health") != "healthy":
        raise ContractError("selection is not an available image operation")
    require_text(spec.get("prompt"), "prompt")
    for key in ("width", "height"):
        value = spec.get(key)
        if type(value) is not int or not 64 <= value <= 8192 or value % 8:
            raise ContractError(f"{key} must be an integer multiple of 8 in [64,8192]")
    if type(spec.get("seed")) is not int or not 0 <= spec["seed"] < 2**63:
        raise ContractError("seed must be a nonnegative 63-bit integer")
    required = {"prompt", "width", "height", "seed"}
    if set(spec) != required:
        raise ContractError("image spec accepts exactly prompt, width, height, seed")
    bindings = entry.get("bindings")
    if not isinstance(bindings, dict) or set(bindings) != required:
        raise ContractError("catalog must bind every image field exactly once")
    output = deepcopy(template)
    destinations = set()
    for field, slot in bindings.items():
        if not isinstance(slot, list) or len(slot) != 2 or not all(isinstance(v, str) for v in slot):
            raise ContractError("binding must be [node_id,input_name]")
        node, name = slot
        if (node, name) in destinations:
            raise ContractError("two public fields cannot overwrite one slot")
        destinations.add((node, name))
        if not isinstance(output.get(node), dict) or not isinstance(output[node].get("inputs"), dict):
            raise ContractError("binding node does not exist")
        if name not in output[node]["inputs"]:
            raise ContractError("binding input does not exist")
        output[node]["inputs"][name] = spec[field]
    # Postcondition is about compilation, not provider acceptance or pixel QA.
    for field, (node, name) in bindings.items():
        if output[node]["inputs"][name] != spec[field]:
            raise ContractError("compiled binding postcondition failed")
    return {"schema_version": 1, "operation": "image", "runtime": entry.get("runtime"),
            "catalog_id": entry["id"], "catalog_version": entry["version"],
            "catalog_digest": selection["digest"], "spec_digest": digest(spec),
            "workflow": output, "workflow_digest": digest(output), "validation": "bindings-checked"}
