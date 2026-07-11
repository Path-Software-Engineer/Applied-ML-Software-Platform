from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT))

from src.analysis.product_ranking import (  # noqa: E402
    INPUT_PATH,
    PRODUCT_SUMMARY_PATH,
    REVENUE_RANKING_PATH,
    UNITS_RANKING_PATH,
    build_product_summary,
    build_revenue_ranking,
    build_units_ranking,
    load_sales_data,
    save_product_outputs,
)


def validate_product_summary(
    sales_df: pd.DataFrame,
    product_summary: pd.DataFrame,
) -> None:
    expected_products = sales_df["product_id"].nunique()

    if len(product_summary) != expected_products:
        raise AssertionError(
            "Product summary does not contain one row per product."
        )

    if product_summary["product_id"].duplicated().any():
        raise AssertionError(
            "Product summary contains duplicated product identifiers."
        )

    if product_summary["total_units_sold"].sum() != sales_df["units_sold"].sum():
        raise AssertionError(
            "Product summary does not preserve total units sold."
        )

    summary_revenue = round(float(product_summary["total_revenue"].sum()), 2)
    source_revenue = round(float(sales_df["revenue"].sum()), 2)

    if summary_revenue != source_revenue:
        raise AssertionError(
            "Product summary does not preserve total revenue."
        )


def validate_rankings(
    units_ranking: pd.DataFrame,
    revenue_ranking: pd.DataFrame,
) -> None:
    if not units_ranking["total_units_sold"].is_monotonic_decreasing:
        raise AssertionError(
            "Units ranking is not ordered from highest to lowest."
        )

    if not revenue_ranking["total_revenue"].is_monotonic_decreasing:
        raise AssertionError(
            "Revenue ranking is not ordered from highest to lowest."
        )

    expected_units_ranks = list(range(1, len(units_ranking) + 1))
    expected_revenue_ranks = list(range(1, len(revenue_ranking) + 1))

    if units_ranking["units_rank"].tolist() != expected_units_ranks:
        raise AssertionError("Units ranking positions are invalid.")

    if revenue_ranking["revenue_rank"].tolist() != expected_revenue_ranks:
        raise AssertionError("Revenue ranking positions are invalid.")


def dataframe_to_markdown(data: pd.DataFrame) -> str:
    headers = [str(column) for column in data.columns]
    rows = [
        [str(value) for value in row]
        for row in data.itertuples(index=False, name=None)
    ]

    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join("---" for _ in headers) + " |"
    row_lines = [
        "| " + " | ".join(row) + " |"
        for row in rows
    ]

    return "\n".join([header_line, separator_line, *row_lines])

def write_summary(
    product_summary: pd.DataFrame,
    units_ranking: pd.DataFrame,
    revenue_ranking: pd.DataFrame,
) -> Path:
    top_units_product = units_ranking.iloc[0]
    top_revenue_product = revenue_ranking.iloc[0]

    summary_path = (
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "demand-insight"
        / "product_ranking_summary.md"
    )
    summary_path.parent.mkdir(parents=True, exist_ok=True)

    units_table = dataframe_to_markdown(
        units_ranking[
            [
                "units_rank",
                "product_id",
                "product_name",
                "total_units_sold",
            ]
        ]
    )

    revenue_table = dataframe_to_markdown(
        revenue_ranking[
            [
                "revenue_rank",
                "product_id",
                "product_name",
                "total_revenue",
            ]
        ]
    )

    summary_path.write_text(
        f"""# Product Ranking Summary

## Day

Sprint 1 - Week 3 - Day 17

## Objective

Build a product-level summary and rank observed products by units sold and revenue.

## Input

`data/processed/demand-insight/sales_feature_baseline_metric_pipeline.csv`

## Outputs

- `data/processed/demand-insight/product_summary.csv`
- `data/processed/demand-insight/product_ranking_by_units.csv`
- `data/processed/demand-insight/product_ranking_by_revenue.csv`

## Main results

| Metric | Result |
|---|---|
| Unique products | {len(product_summary)} |
| Top product by units sold | {top_units_product["product_name"]} |
| Top units sold | {int(top_units_product["total_units_sold"])} |
| Top product by revenue | {top_revenue_product["product_name"]} |
| Top revenue | {float(top_revenue_product["total_revenue"]):.2f} |

## Ranking by units sold

{units_table}

## Ranking by revenue

{revenue_table}

## Interpretation

The units ranking measures accumulated observed demand per product.

The revenue ranking measures accumulated observed economic value per product.

The leading product can differ between rankings because revenue depends on both units sold and unit price.

## Limitations

These rankings describe only the current observed dataset.

They do not predict future demand and do not measure profit because product costs are unavailable.
""",
        encoding="utf-8",
    )

    return summary_path


def main() -> None:
    sales_df = load_sales_data(INPUT_PATH)
    product_summary = build_product_summary(sales_df)
    units_ranking = build_units_ranking(product_summary)
    revenue_ranking = build_revenue_ranking(product_summary)

    validate_product_summary(sales_df, product_summary)
    validate_rankings(units_ranking, revenue_ranking)

    save_product_outputs(
        product_summary,
        units_ranking,
        revenue_ranking,
    )
    summary_path = write_summary(
        product_summary,
        units_ranking,
        revenue_ranking,
    )

    top_units_product = units_ranking.iloc[0]
    top_revenue_product = revenue_ranking.iloc[0]

    print("OK - Day 17 product ranking check passed")
    print(f"Products: {len(product_summary)}")
    print(
        "Top product by units sold: "
        f"{top_units_product['product_name']} "
        f"({int(top_units_product['total_units_sold'])})"
    )
    print(
        "Top product by revenue: "
        f"{top_revenue_product['product_name']} "
        f"({float(top_revenue_product['total_revenue']):.2f})"
    )
    print(f"Product summary: {PRODUCT_SUMMARY_PATH}")
    print(f"Units ranking: {UNITS_RANKING_PATH}")
    print(f"Revenue ranking: {REVENUE_RANKING_PATH}")
    print(f"Report: {summary_path}")


if __name__ == "__main__":
    main()