"""Isolated tests for the Day 20 Demand Insight visual report."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from src.visualization.sales_visual_report import (
    build_daily_sales_figure,
    build_ranking_figure,
    load_insight_cards,
    load_visual_data,
    render_visual_report,
)


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _write_visual_inputs(tmp_path: Path) -> dict[Path, set[str]]:
    daily_path = tmp_path / "daily_sales_summary.csv"
    units_path = tmp_path / "product_ranking_by_units.csv"
    revenue_path = tmp_path / "product_ranking_by_revenue.csv"

    pd.DataFrame(
        {
            "date": ["2026-01-01", "2026-01-02"],
            "total_units_sold": [10, 15],
            "total_revenue": [25.0, 42.5],
            "sales_count": [1, 2],
        }
    ).to_csv(daily_path, index=False)

    pd.DataFrame(
        {
            "units_rank": [1, 2],
            "product_name": ["Bread", "Rice 1kg"],
            "total_units_sold": [15, 10],
        }
    ).to_csv(units_path, index=False)

    pd.DataFrame(
        {
            "revenue_rank": [1, 2],
            "product_name": ["Rice 1kg", "Bread"],
            "total_revenue": [42.5, 25.0],
        }
    ).to_csv(revenue_path, index=False)

    return {
        daily_path: {"date", "total_units_sold", "total_revenue"},
        units_path: {"units_rank", "product_name", "total_units_sold"},
        revenue_path: {"revenue_rank", "product_name", "total_revenue"},
    }


def _cards() -> list[dict[str, str]]:
    limitation = (
        "Describe únicamente las ventas observadas entre 2026-01-01 y "
        "2026-01-02; no predice demanda futura."
    )
    return [
        {
            "card_id": "observed-demand",
            "title": "Demanda observada",
            "metric": "25 unidades | 67.50 de revenue",
            "insight": "El periodo analizado va de 2026-01-01 a 2026-01-02.",
            "recommendation": "Usar estos totales como contexto general.",
            "limitation": limitation,
        },
        {
            "card_id": "top-product-units",
            "title": "Producto con mayor demanda",
            "metric": "Bread — 15 unidades",
            "insight": "Bread concentró el mayor volumen observado.",
            "recommendation": "Vigilar su disponibilidad.",
            "limitation": limitation,
        },
        {
            "card_id": "top-product-revenue",
            "title": "Producto con mayor revenue",
            "metric": "Rice 1kg — 42.50",
            "insight": "Rice 1kg generó el mayor valor económico observado.",
            "recommendation": "Comparar su aporte en periodos posteriores.",
            "limitation": limitation,
        },
        {
            "card_id": "top-day-units",
            "title": "Día con mayor movimiento",
            "metric": "2026-01-02 — 15 unidades",
            "insight": "Fue el día con más unidades vendidas.",
            "recommendation": "Revisar qué impulsó el volumen.",
            "limitation": limitation,
        },
        {
            "card_id": "top-day-revenue",
            "title": "Día con mayor revenue",
            "metric": "2026-01-02 — 42.50",
            "insight": "Fue el día con mayor revenue observado.",
            "recommendation": "Comparar su composición de ventas.",
            "limitation": limitation,
        },
    ]


def _assert_png(path: Path) -> None:
    assert path.exists()
    assert path.stat().st_size > len(PNG_SIGNATURE)
    assert path.read_bytes().startswith(PNG_SIGNATURE)


def test_load_visual_data_rejects_missing_columns(tmp_path: Path) -> None:
    contracts = _write_visual_inputs(tmp_path)
    daily_path = tmp_path / "daily_sales_summary.csv"
    pd.DataFrame({"date": ["2026-01-01"]}).to_csv(daily_path, index=False)

    with pytest.raises(ValueError, match="total_units_sold|total_revenue"):
        load_visual_data(contracts)


def test_load_visual_data_converts_date_to_datetime(tmp_path: Path) -> None:
    data = load_visual_data(_write_visual_inputs(tmp_path))

    assert pd.api.types.is_datetime64_any_dtype(data["daily_sales_summary"]["date"])


def test_build_daily_sales_figure_creates_valid_png(tmp_path: Path) -> None:
    data = load_visual_data(_write_visual_inputs(tmp_path))
    output_path = tmp_path / "daily_sales.png"

    result = build_daily_sales_figure(
        data["daily_sales_summary"], output_path=output_path
    )

    assert result == output_path
    _assert_png(output_path)


@pytest.mark.parametrize(
    ("dataset_name", "value_column", "title", "axis_label", "color", "fmt"),
    [
        (
            "product_ranking_by_units",
            "total_units_sold",
            "Product ranking by units sold",
            "Units sold",
            "#2563EB",
            ".0f",
        ),
        (
            "product_ranking_by_revenue",
            "total_revenue",
            "Product ranking by revenue",
            "Revenue",
            "#D97706",
            ".2f",
        ),
    ],
)
def test_build_ranking_figure_creates_valid_png(
    tmp_path: Path,
    dataset_name: str,
    value_column: str,
    title: str,
    axis_label: str,
    color: str,
    fmt: str,
) -> None:
    data = load_visual_data(_write_visual_inputs(tmp_path))
    output_path = tmp_path / f"{dataset_name}.png"

    result = build_ranking_figure(
        data[dataset_name],
        value_column,
        title,
        axis_label,
        color,
        output_path,
        fmt,
    )

    assert result == output_path
    _assert_png(output_path)


def test_load_insight_cards_rejects_invalid_field_contract(tmp_path: Path) -> None:
    cards_path = tmp_path / "cards.json"
    invalid_card = _cards()[0]
    invalid_card.pop("limitation")
    cards_path.write_text(
        json.dumps([invalid_card], ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="contract|fields|limitation"):
        load_insight_cards(cards_path)


def test_render_visual_report_uses_cards_and_relative_figure_paths() -> None:
    report = render_visual_report(_cards())

    assert "2026-01-02 — 15 unidades" in report
    assert "2026-01-02 — 42.50" in report
    assert "Bread — 15 unidades" in report
    assert "Rice 1kg — 42.50" in report
    assert "../../figures/demand-insight/daily_sales.png" in report
    assert "../../figures/demand-insight/product_units_ranking.png" in report
    assert "../../figures/demand-insight/product_revenue_ranking.png" in report
    assert "Units sold represent demand volume." in report
    assert "Revenue represents observed economic value." in report
    assert "no predice demanda futura" in report