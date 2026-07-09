from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[4]

INPUT_PATH = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_feature_baseline_metric_pipeline.csv"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "demand-insight" / "sales_summary.csv"

REQUIRED_COLUMNS = {
    "sale_id",
    "date",
    "product_id",
    "product_name",
    "category",
    "units_sold",
    "unit_price",
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


def build_sales_summary(sales_df: pd.DataFrame) -> pd.DataFrame:
    summary = {
        "total_units_sold": int(sales_df["units_sold"].sum()),
        "total_revenue": round(float(sales_df["revenue"].sum()), 2),
        "sales_count": int(len(sales_df)),
        "unique_products": int(sales_df["product_id"].nunique()),
        "unique_categories": int(sales_df["category"].nunique()),
        "start_date": sales_df["date"].min().date().isoformat(),
        "end_date": sales_df["date"].max().date().isoformat(),
        "average_units_per_sale": round(float(sales_df["units_sold"].mean()), 2),
        "average_revenue_per_sale": round(float(sales_df["revenue"].mean()), 2),
        "average_unit_price": round(float(sales_df["unit_price"].mean()), 2),
    }

    return pd.DataFrame([summary])


def save_sales_summary(summary_df: pd.DataFrame, output_path: Path = OUTPUT_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    sales_df = load_sales_data()
    summary_df = build_sales_summary(sales_df)
    output_path = save_sales_summary(summary_df)

    print("Sales summary generated")
    print(f"Input: {INPUT_PATH}")
    print(f"Output: {output_path}")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
