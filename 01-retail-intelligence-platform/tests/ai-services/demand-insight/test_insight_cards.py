"""Tests for structured Demand Insight Cards."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from src.insights.insight_cards import (
    EXPECTED_CARD_IDS,
    build_insight_cards,
    load_artifacts,
    save_insight_cards,
)


def sample_artifacts() -> dict[str, pd.DataFrame]:
    return {
        "sales_summary": pd.DataFrame(
            [
                {
                    "total_units_sold": 15,
                    "total_revenue": 90.0,
                    "start_date": "2026-01-01",
                    "end_date": "2026-01-02",
                }
            ]
        ),
        "product_ranking_by_units": pd.DataFrame(
            [
                {
                    "units_rank": 1,
                    "product_name": "Bread",
                    "total_units_sold": 10,
                },
                {
                    "units_rank": 2,
                    "product_name": "Rice",
                    "total_units_sold": 5,
                },
            ]
        ),
        "product_ranking_by_revenue": pd.DataFrame(
            [
                {
                    "revenue_rank": 1,
                    "product_name": "Rice",
                    "total_revenue": 60.0,
                },
                {
                    "revenue_rank": 2,
                    "product_name": "Bread",
                    "total_revenue": 30.0,
                },
            ]
        ),
        "daily_sales_summary": pd.DataFrame(
            [
                {
                    "date": "2026-01-01",
                    "total_units_sold": 10,
                    "total_revenue": 30.0,
                },
                {
                    "date": "2026-01-02",
                    "total_units_sold": 5,
                    "total_revenue": 60.0,
                },
            ]
        ),
    }


def test_load_artifacts_rejects_missing_columns(tmp_path: Path) -> None:
    input_path = tmp_path / "summary.csv"
    pd.DataFrame([{"total_units_sold": 15}]).to_csv(input_path, index=False)

    with pytest.raises(ValueError, match="missing columns"):
        load_artifacts(
            {
                input_path: {
                    "total_units_sold",
                    "total_revenue",
                }
            }
        )


def test_build_insight_cards_respects_contract() -> None:
    cards = build_insight_cards(sample_artifacts())
    cards_by_id = {card["card_id"]: card for card in cards}

    assert set(cards_by_id) == EXPECTED_CARD_IDS
    assert cards_by_id["top-product-units"]["metric"] == "Bread — 10 unidades"
    assert cards_by_id["top-product-revenue"]["metric"] == "Rice — 60.00"
    assert cards_by_id["top-day-units"]["metric"] == "2026-01-01 — 10 unidades"
    assert cards_by_id["top-day-revenue"]["metric"] == "2026-01-02 — 60.00"

    required_fields = {
        "card_id",
        "title",
        "metric",
        "insight",
        "recommendation",
        "limitation",
    }
    assert all(set(card) == required_fields for card in cards)
    assert all("no predice demanda futura" in card["limitation"] for card in cards)


def test_save_insight_cards_uses_requested_paths(tmp_path: Path) -> None:
    cards = build_insight_cards(sample_artifacts())
    json_path = tmp_path / "cards.json"
    markdown_path = tmp_path / "cards.md"

    save_insight_cards(cards, json_path, markdown_path)

    saved_cards = json.loads(json_path.read_text(encoding="utf-8"))
    markdown = markdown_path.read_text(encoding="utf-8")

    assert len(saved_cards) == 5
    assert saved_cards[0]["card_id"] == "observed-demand"
    assert "# Demand Insight Cards" in markdown
    assert "## Producto con mayor demanda" in markdown