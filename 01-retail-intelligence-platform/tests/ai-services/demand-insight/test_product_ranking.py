from pathlib import Path

import pandas as pd

from src.analysis.product_ranking import (
    build_product_summary,
    build_revenue_ranking,
    build_units_ranking,
    save_product_outputs,
)


def sales_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "product_id": ["P2", "P1", "P2", "P3"],
            "product_name": ["B", "A", "B", "C"],
            "category": ["X", "X", "X", "Y"],
            "units_sold": [2, 4, 2, 4],
            "revenue": [20.0, 10.0, 20.0, 50.0],
        }
    )


def test_summary_has_one_row_per_product_and_preserves_totals() -> None:
    summary = build_product_summary(sales_data())
    assert len(summary) == 3
    assert not summary["product_id"].duplicated().any()
    assert summary["total_units_sold"].sum() == 12
    assert summary["total_revenue"].sum() == 100.0


def test_rankings_are_descending_with_deterministic_tie_break() -> None:
    summary = build_product_summary(sales_data())
    units = build_units_ranking(summary)
    revenue = build_revenue_ranking(summary)
    assert units["product_id"].tolist() == ["P1", "P2", "P3"]
    assert revenue["product_id"].tolist() == ["P3", "P2", "P1"]
    assert units["units_rank"].tolist() == [1, 2, 3]


def test_product_outputs_use_tmp_path(tmp_path: Path) -> None:
    summary = build_product_summary(sales_data())
    paths = save_product_outputs(
        summary,
        build_units_ranking(summary),
        build_revenue_ranking(summary),
        tmp_path,
    )
    assert all(path.exists() and path.parent == tmp_path for path in paths)
