"""Build a daily sales summary for the Demand Insight module."""

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

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "demand-insight"
    / "daily_sales_summary.csv"
)
REPORT_PATH = (
    PROJECT_ROOT
    / "reports"
    / "summaries"
    / "demand-insight"
    / "temporal_sales_analysis_summary.md"
)

REQUIRED_COLUMNS = {
    "date",
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

    sales_df["date"] = pd.to_datetime(sales_df["date"])

    return sales_df

def build_daily_sales_summary(sales_df: pd.DataFrame) -> pd.DataFrame:
    daily_summary = (
        sales_df.groupby("date", as_index=False)
        .agg(
            total_units_sold=("units_sold", "sum"),
            total_revenue=("revenue", "sum"),
            sales_count=("date", "size"),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    daily_summary["total_units_sold"] = (
        daily_summary["total_units_sold"].astype(int)
    )
    daily_summary["total_revenue"] = (
        daily_summary["total_revenue"].round(2)
    )

    return daily_summary

def build_temporal_results(
    daily_summary: pd.DataFrame,
) -> dict[str, object]:
    top_units_row = daily_summary.loc[
        daily_summary["total_units_sold"].idxmax()
    ]
    top_revenue_row = daily_summary.loc[
        daily_summary["total_revenue"].idxmax()
    ]

    total_units = int(daily_summary["total_units_sold"].sum())
    total_revenue = round(
        float(daily_summary["total_revenue"].sum()),
        2,
    )

    return {
        "observed_days": int(len(daily_summary)),
        "top_units_date": top_units_row["date"].date().isoformat(),
        "top_units_sold": int(top_units_row["total_units_sold"]),
        "top_units_share": round(
            float(top_units_row["total_units_sold"]) / total_units * 100,
            2,
        ),
        "top_revenue_date": top_revenue_row["date"].date().isoformat(),
        "top_revenue": round(
            float(top_revenue_row["total_revenue"]),
            2,
        ),
        "top_revenue_share": round(
            float(top_revenue_row["total_revenue"])
            / total_revenue
            * 100,
            2,
        ),
    }
    
def save_daily_sales_summary(
    daily_summary: pd.DataFrame,
    output_path: Path = OUTPUT_PATH,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = daily_summary.copy()
    output_data["date"] = (
        output_data["date"].dt.date.astype(str)
    )
    output_data.to_csv(output_path, index=False)

    return output_path


def write_temporal_summary(
    daily_summary: pd.DataFrame,
    results: dict[str, object],
    report_path: Path = REPORT_PATH,
) -> Path:
    """Write temporal-analysis evidence from production results."""
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        f"""# Temporal Sales Analysis Summary

## Results

| Metric | Result |
|---|---:|
| Observed dates | {results['observed_days']} |
| Total units | {int(daily_summary['total_units_sold'].sum())} |
| Total revenue | {float(daily_summary['total_revenue'].sum()):.2f} |
| Top date by units | {results['top_units_date']} |
| Top units | {results['top_units_sold']} |
| Top date by revenue | {results['top_revenue_date']} |
| Top revenue | {results['top_revenue']:.2f} |

This report describes the observed period and does not establish seasonality or forecast demand.
""",
        encoding="utf-8",
    )
    return report_path


def main() -> None:
    sales_df = load_sales_data()
    daily_summary = build_daily_sales_summary(sales_df)
    temporal_results = build_temporal_results(daily_summary)
    output_path = save_daily_sales_summary(daily_summary)
    report_path = write_temporal_summary(daily_summary, temporal_results)

    print("Temporal sales analysis generated")
    print(f"Input: {INPUT_PATH}")
    print(f"Output: {output_path}")
    print(f"Report: {report_path}")
    print(
        "Top date by units sold: "
        f"{temporal_results['top_units_date']} "
        f"({temporal_results['top_units_sold']} units)"
    )
    print(
        "Top date by revenue: "
        f"{temporal_results['top_revenue_date']} "
        f"({temporal_results['top_revenue']:.2f})"
    )


if __name__ == "__main__":
    main()
