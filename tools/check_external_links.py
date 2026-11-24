"""Check that external links in the published site and repository references still resolve."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [*sorted((ROOT / "docs").rglob("*.html")), *sorted((ROOT / "harness-references").rglob("*.md")),
           ROOT / "README.md"]
URL = re.compile(r"https?://[^\s\"'<>)\]`|]+")
# Hosts that block automated requests; a refusal there says nothing about the link.
SOFT = {401, 403, 405, 429, 999}


def links() -> set[str]:
    found = set()
    for path in SOURCES:
        for url in URL.findall(path.read_text(encoding="utf-8", errors="ignore")):
            url = url.rstrip(".,;:")
            if "pheanor-agent.github.io/p-hermes-v2" not in url:
                found.add(url)
    return found


def status(url: str) -> tuple[str, int | str]:
    headers = {"User-Agent": "Mozilla/5.0 (p-hermes link check)"}
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(request, timeout=20) as response:
                return url, response.status
        except urllib.error.HTTPError as error:
            if method == "GET" or error.code not in (403, 405, 501):
                return url, error.code
        except Exception as error:  # DNS, TLS, timeout
            if method == "GET":
                return url, type(error).__name__
    return url, "unreachable"


def main() -> int:
    targets = sorted(links())
    with ThreadPoolExecutor(max_workers=12) as pool:
        results = list(pool.map(status, targets))
    broken = [(u, s) for u, s in results if not (isinstance(s, int) and (s < 400 or s in SOFT))]
    soft = [(u, s) for u, s in results if isinstance(s, int) and s in SOFT]
    for url, code in soft:
        print(f"warn {code} {url}")
    for url, code in broken:
        print(f"broken {code} {url}")
    print(f"checked={len(targets)} broken={len(broken)} soft={len(soft)}")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
