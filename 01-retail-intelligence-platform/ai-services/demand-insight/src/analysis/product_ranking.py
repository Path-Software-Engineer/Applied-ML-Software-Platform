from __future__ import annotations

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[4]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "demand-insight"
    / "sales_feature_baseline_metric_pipeline.csv"
)

OUTPUT_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "demand-insight"
)

PRODUCT_SUMMARY_PATH = OUTPUT_DIRECTORY / "product_summary.csv"
UNITS_RANKING_PATH = OUTPUT_DIRECTORY / "product_ranking_by_units.csv"
REVENUE_RANKING_PATH = OUTPUT_DIRECTORY / "product_ranking_by_revenue.csv"

REQUIRED_COLUMNS = {
    "product_id",
    "product_name",
    "category",
    "units_sold",
    "revenue",
}


def load_sales_data(input_path: Path = INPUT_PATH) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    sales_df = pd.read_csv(input_path)

    missing_columns = REQUIRED_COLUMNS.difference(sales_df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return sales_df


def build_product_summary(sales_df: pd.DataFrame) -> pd.DataFrame:
    product_summary = (
        sales_df.groupby(
            ["product_id", "product_name", "category"],
            as_index=False,
        )
        .agg(
            total_units_sold=("units_sold", "sum"),
            total_revenue=("revenue", "sum"),
            sales_count=("product_id", "size"),
        )
    )

    product_summary["total_units_sold"] = (
        product_summary["total_units_sold"].astype(int)
    )
    product_summary["total_revenue"] = (
        product_summary["total_revenue"].round(2)
    )

    return product_summary


def build_units_ranking(product_summary: pd.DataFrame) -> pd.DataFrame:
    units_ranking = (
        product_summary.sort_values(
            by=["total_units_sold", "product_id"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
        .copy()
    )

    units_ranking.insert(
        0,
        "units_rank",
        range(1, len(units_ranking) + 1),
    )

    return units_ranking


def build_revenue_ranking(product_summary: pd.DataFrame) -> pd.DataFrame:
    revenue_ranking = (
        product_summary.sort_values(
            by=["total_revenue", "product_id"],
            ascending=[False, True],
        )
        .reset_index(drop=True)
        .copy()
    )

    revenue_ranking.insert(
        0,
        "revenue_rank",
        range(1, len(revenue_ranking) + 1),
    )

    return revenue_ranking


def save_product_outputs(
    product_summary: pd.DataFrame,
    units_ranking: pd.DataFrame,
    revenue_ranking: pd.DataFrame,
) -> tuple[Path, Path, Path]:
    OUTPUT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    product_summary.to_csv(PRODUCT_SUMMARY_PATH, index=False)
    units_ranking.to_csv(UNITS_RANKING_PATH, index=False)
    revenue_ranking.to_csv(REVENUE_RANKING_PATH, index=False)

    return (
        PRODUCT_SUMMARY_PATH,
        UNITS_RANKING_PATH,
        REVENUE_RANKING_PATH,
    )


def main() -> None:
    sales_df = load_sales_data()
    product_summary = build_product_summary(sales_df)
    units_ranking = build_units_ranking(product_summary)
    revenue_ranking = build_revenue_ranking(product_summary)

    output_paths = save_product_outputs(
        product_summary,
        units_ranking,
        revenue_ranking,
    )

    top_units_product = units_ranking.iloc[0]
    top_revenue_product = revenue_ranking.iloc[0]

    print("Product ranking generated")
    print(f"Input: {INPUT_PATH}")
    print(f"Product summary: {output_paths[0]}")
    print(f"Units ranking: {output_paths[1]}")
    print(f"Revenue ranking: {output_paths[2]}")
    print(
        "Top product by units sold: "
        f"{top_units_product['product_name']} "
        f"({top_units_product['total_units_sold']} units)"
    )
    print(
        "Top product by revenue: "
        f"{top_revenue_product['product_name']} "
        f"({top_revenue_product['total_revenue']:.2f})"
    )


if __name__ == "__main__":
    main()