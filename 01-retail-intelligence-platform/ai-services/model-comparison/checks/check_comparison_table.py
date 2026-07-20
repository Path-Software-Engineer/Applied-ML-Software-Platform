"""Readable Day 65 check for the formal comparison table."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_SRC = PROJECT_ROOT / "ai-services" / "model-comparison" / "src"
sys.path.insert(0, str(MODULE_SRC))

from model_comparison.comparison_table import run_comparison_table  # noqa: E402


def main() -> None:
    """Regenerate and validate formal metric evidence."""
    table = run_comparison_table(PROJECT_ROOT)
    output_root = PROJECT_ROOT / "reports" / "outputs" / "model-comparison"
    payload = json.loads(
        (output_root / "comparison_table.json").read_text(encoding="utf-8")
    )
    lab_output = (
        PROJECT_ROOT
        / "labs"
        / "tec-labs"
        / "tec-model-metrics-lab"
        / "outputs"
        / "mae_rmse_comparison.md"
    )

    assert table["mae_rank"].tolist() == [1, 2, 3, 4]
    assert table["mae_units"].is_monotonic_increasing
    assert table["within_practical_equivalence"].sum() == 2
    assert payload["primary_metric"]["id"] == "mae"
    assert payload["policy"]["practical_equivalence_units"] == 0.25
    assert payload["selection_status"] == "not_selected"
    assert lab_output.is_file() and lab_output.stat().st_size > 0

    print("OK - Sprint 2 Day 65 comparison table check passed")
    print("Comparable rows: 4")
    print(f"Observed MAE leader: {table.iloc[0]['model_name']}")
    print("Practically equivalent learned candidates: 2")
    print("Selection status: not selected")


if __name__ == "__main__":
    main()
