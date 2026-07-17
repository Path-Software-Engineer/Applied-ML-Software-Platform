"""Tests for the internal Demand Summary service."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from backend.api.app.services.demand_summary_service import (
    CARD_FIELDS,
    DemandSummaryError,
    DemandSummaryService,
)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sample_cards() -> list[dict[str, str]]:
    cards = []
    for card_id in (
        "observed-demand",
        "top-product-units",
        "top-product-revenue",
        "top-day-units",
        "top-day-revenue",
    ):
        cards.append(
            {
                "card_id": card_id,
                "title": f"Title {card_id}",
                "metric": "Metric",
                "insight": "Insight",
                "recommendation": "Recommendation",
                "limitation": "Observed period only.",
            }
        )
    return cards


def create_artifacts(project_root: Path) -> None:
    processed = project_root / "data/processed/demand-insight"
    write_csv(
        processed / "sales_summary.csv",
        [
            {
                "total_units_sold": 30,
                "total_revenue": 75.5,
                "sales_count": 2,
                "unique_products": 2,
                "unique_categories": 1,
                "start_date": "2026-02-01",
                "end_date": "2026-02-02",
            }
        ],
    )
    write_csv(
        processed / "sales_feature_baseline_metric_pipeline.csv",
        [
            {"mean_baseline_prediction": 15, "baseline_absolute_error": 3},
            {"mean_baseline_prediction": 15, "baseline_absolute_error": 5},
        ],
    )
    write_csv(
        processed / "product_ranking_by_units.csv",
        [
            {"units_rank": 1, "product_name": "Bread", "total_units_sold": 20},
            {"units_rank": 2, "product_name": "Milk", "total_units_sold": 10},
        ],
    )
    write_csv(
        processed / "product_ranking_by_revenue.csv",
        [
            {"revenue_rank": 1, "product_name": "Milk", "total_revenue": 45.5},
            {"revenue_rank": 2, "product_name": "Bread", "total_revenue": 30},
        ],
    )
    write_csv(
        processed / "daily_sales_summary.csv",
        [
            {"date": "2026-02-01", "total_units_sold": 12, "total_revenue": 33},
            {"date": "2026-02-02", "total_units_sold": 18, "total_revenue": 42.5},
        ],
    )
    cards_path = project_root / "reports/insight-cards/demand_insight_cards.json"
    cards_path.parent.mkdir(parents=True, exist_ok=True)
    cards_path.write_text(json.dumps(sample_cards()), encoding="utf-8")


def test_get_summary_assembles_versioned_contract(tmp_path: Path) -> None:
    create_artifacts(tmp_path)

    summary = DemandSummaryService(tmp_path).get_summary()

    assert summary["schema_version"] == "1.0"
    assert summary["period"] == {
        "start_date": "2026-02-01",
        "end_date": "2026-02-02",
        "observed_days": 2,
    }
    assert summary["sales_summary"]["total_units_sold"] == 30
    assert summary["baseline"] == {"mean_units_prediction": 15.0, "mae": 4.0}
    assert summary["leaders"]["product_by_units"]["name"] == "Bread"
    assert summary["leaders"]["date_by_revenue"]["value"] == 42.5
    assert len(summary["insight_cards"]) == 5


def test_get_summary_rejects_missing_artifact(tmp_path: Path) -> None:
    create_artifacts(tmp_path)
    (tmp_path / "data/processed/demand-insight/sales_summary.csv").unlink()

    with pytest.raises(DemandSummaryError, match="Required artifact is missing"):
        DemandSummaryService(tmp_path).get_summary()


def test_get_summary_rejects_inconsistent_baseline(tmp_path: Path) -> None:
    create_artifacts(tmp_path)
    write_csv(
        tmp_path
        / "data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv",
        [
            {"mean_baseline_prediction": 10, "baseline_absolute_error": 1},
            {"mean_baseline_prediction": 11, "baseline_absolute_error": 2},
        ],
    )

    with pytest.raises(DemandSummaryError, match="one mean baseline prediction"):
        DemandSummaryService(tmp_path).get_summary()


def test_get_summary_rejects_invalid_card_contract(tmp_path: Path) -> None:
    create_artifacts(tmp_path)
    cards_path = tmp_path / "reports/insight-cards/demand_insight_cards.json"
    cards = sample_cards()
    cards[0].pop("limitation")
    cards_path.write_text(json.dumps(cards), encoding="utf-8")

    with pytest.raises(DemandSummaryError, match="field contract"):
        DemandSummaryService(tmp_path).get_summary()


def test_save_summary_uses_requested_output_path(tmp_path: Path) -> None:
    create_artifacts(tmp_path)
    service = DemandSummaryService(tmp_path)
    output_path = tmp_path / "isolated/output/demand_summary.json"

    saved_path = service.save_summary(output_path=output_path)

    assert saved_path == output_path
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0"
    assert set(payload["insight_cards"][0]) == CARD_FIELDS
