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
REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "summaries"
    / "demand-insight"
    / "product_ranking_summary.md"
)

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
    output_directory: Path = OUTPUT_DIRECTORY,
) -> tuple[Path, Path, Path]:
    output_directory.mkdir(parents=True, exist_ok=True)

    product_summary_path = output_directory / "product_summary.csv"
    units_ranking_path = output_directory / "product_ranking_by_units.csv"
    revenue_ranking_path = output_directory / "product_ranking_by_revenue.csv"

    product_summary.to_csv(product_summary_path, index=False)
    units_ranking.to_csv(units_ranking_path, index=False)
    revenue_ranking.to_csv(revenue_ranking_path, index=False)

    return (
        product_summary_path,
        units_ranking_path,
        revenue_ranking_path,
    )


def write_product_ranking_summary(
    product_summary: pd.DataFrame,
    units_ranking: pd.DataFrame,
    revenue_ranking: pd.DataFrame,
    report_path: Path = REPORT_PATH,
) -> Path:
    """Write product-ranking evidence from production results."""
    top_units = units_ranking.iloc[0]
    top_revenue = revenue_ranking.iloc[0]
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"""# Product Ranking Summary

## Results

| Metric | Result |
|---|---:|
| Products | {len(product_summary)} |
| Top product by units | {top_units['product_name']} |
| Top units | {int(top_units['total_units_sold'])} |
| Top product by revenue | {top_revenue['product_name']} |
| Top revenue | {float(top_revenue['total_revenue']):.2f} |

This report describes observed sales and does not predict future demand.
""",
        encoding="utf-8",
    )
    return report_path


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
    report_path = write_product_ranking_summary(
        product_summary, units_ranking, revenue_ranking
    )

    top_units_product = units_ranking.iloc[0]
    top_revenue_product = revenue_ranking.iloc[0]

    print("Product ranking generated")
    print(f"Input: {INPUT_PATH}")
    print(f"Product summary: {output_paths[0]}")
    print(f"Units ranking: {output_paths[1]}")
    print(f"Revenue ranking: {output_paths[2]}")
    print(f"Report: {report_path}")
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
