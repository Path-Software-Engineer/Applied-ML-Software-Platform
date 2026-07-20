"""Readable Day 72 check for the internal Model Comparison read service."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.api.app.services.model_comparison_service import (  # noqa: E402
    ModelComparisonService,
)


def main() -> None:
    summary = ModelComparisonService(PROJECT_ROOT).get_summary()

    assert summary["schema_version"] == "1.0"
    assert summary["module"] == "model_comparison"
    assert summary["report_status"] == "learning_evidence_only"
    assert len(summary["candidates"]) == 4
    assert len(summary["decision_cards"]) == 3
    assert summary["decision"]["measurement_leader"]["model_id"] == "gradient_boosting"
    assert summary["decision"]["selected_candidate"]["model_id"] == "random_forest"
    assert summary["decision"]["production_status"] == "not_production_ready"

    print("OK - Sprint 2 Day 72 Model Comparison service check passed")
    print("Schema version: 1.0")
    print("Candidates / Decision Cards: 4 / 3")
    print("Selected for next integration: Random Forest")
    print("HTTP behavior: not implemented on Day 72")


if __name__ == "__main__":
    main()
