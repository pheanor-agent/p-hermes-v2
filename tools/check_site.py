"""Check published-site navigation, slide coverage, and known privacy patterns."""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCS = Path(os.environ.get("DOCS_PATH", ROOT / "docs"))
TEXT_SUFFIXES = {".html", ".md", ".txt", ".py", ".json", ".toml", ".css", ".js", ".svg", ".yaml", ".yml"}
TEXT_FILENAMES = {".nojekyll", "LICENSE", "NOTICE", "COPYING"}
CACHE_SUFFIXES = {".pyc", ".pyo", ".pyd"}
PRIVATE_RULES = {
    "unix-home-path": re.compile(r"/(?:home|Users)/[A-Za-z0-9_.-]+(?:/|$)"),
    "windows-home-path": re.compile(r"[A-Z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+", re.I),
    "private-job-id": re.compile(r"\bJOB-\d{4,}\b"),
    "private-key-header": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "credential-token": re.compile(r"\b(?:sk-proj-|ghp_|gho_)[A-Za-z0-9_-]{20,}"),
    "tailnet-address": re.compile(r"\b100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7])\.\d+\.\d+\b"),
    "credential-assignment": re.compile(r"\b(?:api[_-]?key|secret|token)\s*[:=]\s*[\"']?[^\s\"'<>]{8,}", re.I),
}


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.refs: list[str] = []
        self.classes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if values.get("class"):
            self.classes.extend((values["class"] or "").split())
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.refs.append(value)


def privacy_hits(path_label: str, text: str) -> list[str]:
    return [name for name, pattern in PRIVATE_RULES.items() if pattern.search(path_label) or pattern.search(text)]


def scan_public_tree(errors: list[str]) -> tuple[int, int]:
    scanned_text = 0
    scanned_zip_members = 0
    for path in sorted(p for p in DOCS.rglob("*") if p.is_dir() and "__pycache__" in p.relative_to(DOCS).parts):
        errors.append(f"public Python cache directory: {path.relative_to(DOCS).as_posix()}")
    for path in sorted(p for p in DOCS.rglob("*") if p.is_file()):
        rel = path.relative_to(DOCS).as_posix()
        if "__pycache__" in path.relative_to(DOCS).parts or path.suffix.lower() in CACHE_SUFFIXES:
            errors.append(f"public Python cache/bytecode artifact: {rel}")
        path_hits = privacy_hits(rel, "")
        if path_hits:
            errors.append(f"public path privacy rule {','.join(path_hits)}: {rel}")
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES:
            try:
                text = path.read_text(encoding="utf-8-sig")
            except (UnicodeDecodeError, OSError):
                errors.append(f"text asset is not readable as UTF-8: {rel}")
                continue
            scanned_text += 1
            hits = privacy_hits(rel, text)
            if hits:
                errors.append(f"public text privacy rule {','.join(hits)}: {rel}")
        elif path.suffix.lower() == ".zip":
            try:
                with zipfile.ZipFile(path) as archive:
                    for member in archive.infolist():
                        member_path = Path(member.filename)
                        if "__pycache__" in member_path.parts or member_path.suffix.lower() in CACHE_SUFFIXES:
                            errors.append(f"public ZIP Python cache/bytecode artifact: {rel}!{member.filename}")
                        if member.is_dir():
                            continue
                        scanned_zip_members += 1
                        hits = privacy_hits(member.filename, "")
                        if member_path.suffix.lower() in TEXT_SUFFIXES or member_path.name in TEXT_FILENAMES:
                            try:
                                text = archive.read(member).decode("utf-8-sig")
                            except (UnicodeDecodeError, OSError, RuntimeError):
                                errors.append(f"ZIP text member is not readable as UTF-8: {rel}!{member.filename}")
                                continue
                            hits.extend(privacy_hits(member.filename, text))
                        if hits:
                            errors.append(f"ZIP privacy rule {','.join(sorted(set(hits)))}: {rel}!{member.filename}")
            except (OSError, zipfile.BadZipFile):
                errors.append(f"invalid public ZIP archive: {rel}")
    return scanned_text, scanned_zip_members


def check_content_alignment(errors: list[str]) -> None:
    """Check public scope and operational contract markers without freezing prose."""
    classes = ("permanent_deletion", "external_publication", "credential_security", "policy_amendment")
    required = {
        "index.html": ("Hermes 엔진", "로컬 운영", "wiki/reference/contracts.html#scope"),
        "lectures/00-overview.html": ("세션 기록", "로컬 운영"),
        "lectures/04-integration.html": ("참조 구현",),
        "wiki/knowledge-context.html": ("write-lesson.py", "--id", "--body-file", "validation_status: candidate", "contracts.html#scope"),
        "wiki/reference/workflow.html": classes + ("simple", "JOB", "contracts.html#scope"),
        "wiki/reference/terms.html": classes + ("request_id", "status", "contracts.html#scope"),
        "wiki/reference/contracts.html": ('id="scope"', "Hermes 엔진", "JSON", "Markdown", "intent_revision", "request_sha256", "hermes-agent.nousresearch.com"),
    }
    forbidden = {
        "lectures/00-overview.html": ("Hermes의 모든 약속은",),
        "lectures/04-integration.html": ("원본 코드", "원본 구현과 테스트는"),
        "wiki/knowledge-context.html": ("index.md</code>에 한 행을 추가합니다",),
    }
    for relative, markers in required.items():
        for tree in (ROOT / "site", DOCS):
            path = tree / relative
            if not path.is_file():
                errors.append(f"content contract page missing: {relative}")
                continue
            content = path.read_text(encoding="utf-8")
            for marker in markers:
                if marker not in content:
                    errors.append(f"content contract marker missing in {path.name}: {marker}")
            for marker in forbidden.get(relative, ()):
                if marker in content:
                    errors.append(f"obsolete content contract in {path.name}: {marker}")


def main() -> int:
    errors: list[str] = []
    check_content_alignment(errors)
    source_home = ROOT / "site" / "index.html"
    published_home = DOCS / "index.html"
    if not source_home.is_file() or not published_home.is_file():
        errors.append("required home source or published home is missing")
    elif source_home.read_bytes() != published_home.read_bytes():
        errors.append("site/index.html and docs/index.html are not byte-identical")

    forbidden_paths = (
        "examples", "code", "downloads", "articles", "vendor",
        "wiki/examples", "wiki/environment",
    )
    for relative in forbidden_paths:
        if (DOCS / relative).exists():
            errors.append(f"retired public page tree remains: {relative}")

    html_paths = sorted(DOCS.rglob("*.html"))
    pages: dict[Path, Page] = {}
    for path in html_paths:
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = page
        duplicates = sorted(value for value, count in Counter(page.ids).items() if count > 1)
        if duplicates:
            errors.append(f"duplicate HTML id in {path.relative_to(DOCS)}: {','.join(duplicates)}")

    for path, page in pages.items():
        for reference in page.refs:
            url = urlsplit(reference)
            if url.scheme or url.netloc:
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"missing local link in {path.relative_to(DOCS)}: {reference}")
                continue
            if url.fragment and target.suffix.lower() == ".html":
                destination = pages.get(target.resolve())
                if destination is None:
                    errors.append(f"fragment target is outside parsed public HTML: {reference}")
                elif unquote(url.fragment) not in destination.ids:
                    errors.append(f"missing local fragment in {path.relative_to(DOCS)}: {reference}")

    sys.path.insert(0, str(ROOT / "tools"))
    import deckify

    source_counts: list[int] = []
    rail_count = 0
    for filename, number, _ in deckify.LECTURES:
        source = ROOT / "site" / "lectures" / filename
        if not source.is_file():
            errors.append(f"missing lecture source: {filename}")
            continue
        slides = deckify.parse(source.read_text(encoding="utf-8"), number)
        source_counts.append(len(slides))
        rail_count += sum(bool(slides[k - 1]["next"]) and bool(slides[k]["next"]) for k in range(1, len(slides)))
        if any(not slide.get("title") for slide in slides):
            errors.append(f"lecture slide title missing: {filename}")
        keys = [slide.get("key") for slide in slides]
        if not all(keys) or len(keys) != len(set(keys)):
            errors.append(f"lecture stable slide keys missing or duplicated: {filename}")
    expected_total = sum(source_counts)

    generated_counts: list[int] = []
    for filename, _, _ in deckify.LECTURES:
        generated = DOCS / "lectures" / filename
        if not generated.is_file():
            errors.append(f"missing generated lecture: {filename}")
            continue
        page = Page()
        page.feed(generated.read_text(encoding="utf-8"))
        count = page.classes.count("dk-slide")
        generated_counts.append(count)
        if count == 0:
            errors.append(f"generated lecture has no slides: {filename}")
    if generated_counts != source_counts:
        errors.append(f"generated/source lecture counts differ: {generated_counts} vs {source_counts}")
    mapping = DOCS / "lecture-slide-mapping.csv"
    if not mapping.is_file():
        errors.append("missing generated lecture slide mapping")
    elif len(mapping.read_text(encoding="utf-8").splitlines()) != expected_total + 1:
        errors.append("lecture slide mapping row count does not match authored/generated slides")

    text_count, zip_member_count = scan_public_tree(errors)
    if errors:
        print("\n".join(f"FAIL {error}" for error in errors))
        return 1
    print(json.dumps({
        "result": "PASS",
        "html_files": len(html_paths),
        "source_lecture_slides": source_counts,
        "generated_lecture_slides": generated_counts,
        "total_slides": sum(source_counts),
        "stable_slide_keys": "PASS",
        "mapping_rows": expected_total,
        "actual_question_rails": rail_count,
        "local_href_src_fragments": "checked (including same-page fragments)",
        "public_text_assets_scanned": text_count,
        "zip_members_scanned": zip_member_count,
        "private_pattern_hits": 0,
        "home_source": "site/index.html",
        "home_byte_identity": "PASS",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
