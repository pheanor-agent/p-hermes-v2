"""Rebuild site/assets/fonts/pretendard-subset.woff2 from the glyphs the site uses.

Optional maintenance tool (needs fontTools + brotli, not needed for make build/check):
    python3 tools/subset_font.py /path/to/PretendardVariable.woff2
Run after `make build` so docs/ holds the current text. Pretendard is SIL OFL 1.1.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "assets" / "fonts" / "pretendard-subset.woff2"


def used_text() -> str:
    chunks = []
    for p in list((ROOT / "docs").rglob("*.html")) + list((ROOT / "site" / "assets").glob("*.js")):
        chunks.append(p.read_text(encoding="utf-8", errors="ignore"))
    text = "".join(chunks)
    # Always include printable ASCII, common punctuation and the full Hangul syllable block
    # actually present in the text (keeps the file small).
    extra = "".join(chr(c) for c in range(0x20, 0x7F)) + "·…—–→←↑↓✓≠=“”‘’「」『』①②③④⑤"
    return "".join(sorted(set(re.sub(r"\s", "", text)) | set(extra)))


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    chars = ROOT / "build" / "font-chars.txt"
    chars.parent.mkdir(exist_ok=True)
    chars.write_text(used_text(), encoding="utf-8")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pyftsubset", sys.argv[1], f"--text-file={chars}", "--flavor=woff2",
                    f"--output-file={OUT}", "--layout-features=*", "--no-hinting"], check=True)
    print(OUT, OUT.stat().st_size, "bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
