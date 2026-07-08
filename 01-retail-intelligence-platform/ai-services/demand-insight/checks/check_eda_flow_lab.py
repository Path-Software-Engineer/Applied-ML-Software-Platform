"""Check Day 12 EDA flow lab."""

from __future__ import annotations

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
LAB_SCRIPT = PROJECT_ROOT / "labs" / "tec-labs" / "tec-sales-eda-lab" / "src" / "compare_eda_flows.py"
OUTPUT = PROJECT_ROOT / "labs" / "tec-labs" / "tec-sales-eda-lab" / "outputs" / "eda_flow_comparison.md"


def main() -> None:
    if not LAB_SCRIPT.exists():
        raise AssertionError(f"Missing lab script: {LAB_SCRIPT}")

    runpy.run_path(str(LAB_SCRIPT), run_name="__main__")

    if not OUTPUT.exists():
        raise AssertionError(f"Expected EDA comparison output was not created: {OUTPUT}")

    content = OUTPUT.read_text(encoding="utf-8")
    required_terms = ["raw", "clean", "processed"]
    missing_terms = [term for term in required_terms if term not in content.lower()]
    if missing_terms:
        raise AssertionError(f"EDA report is missing terms: {missing_terms}")

    print("OK - Day 12 EDA flow lab check passed")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
