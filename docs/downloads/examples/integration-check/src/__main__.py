from __future__ import annotations

import argparse
import json
from pathlib import Path

from .integration_check import run


def main() -> int:
    parser = argparse.ArgumentParser(description="합성 입력 기반 통합 계약 점검")
    parser.add_argument("--fixture", default="fixtures/pass", help="fixture 디렉터리")
    parser.add_argument("--output", default="build/integration-check", help="임시 산출물 디렉터리")
    args = parser.parse_args()
    result = run(Path(args.fixture), Path(args.output))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["status"] == "done" else 1


if __name__ == "__main__":
    raise SystemExit(main())
