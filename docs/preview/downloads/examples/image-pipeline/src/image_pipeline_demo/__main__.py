"""합성 fixture를 이용한 데모 진입점."""
import json
from pathlib import Path

from .pipeline import run


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    output = run(root / "fixtures/request.json", root / "fixtures/catalog.json")
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
