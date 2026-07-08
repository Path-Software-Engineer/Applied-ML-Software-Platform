from pathlib import Path
import sys

MODULE_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = Path(__file__).resolve().parents[3]

sys.path.append(str(MODULE_ROOT))

from src.data.data_loader import (  # noqa: E402
    build_data_loading_summary,
    get_data_columns,
    get_data_shape,
    load_sales_data,
    validate_required_columns,
)

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "demand-insight" / "sales.csv"
SUMMARY_PATH = (
    PROJECT_ROOT
    / "reports"
    / "summaries"
    / "demand-insight"
    / "data_loading_summary.md"
)

REQUIRED_COLUMNS = [
    "date",
    "product_id",
    "product_name",
    "units_sold",
    "unit_price",
]


def main() -> None:
    sales_data = load_sales_data(RAW_DATA_PATH)

    rows, columns = get_data_shape(sales_data)
    data_columns = get_data_columns(sales_data)
    missing_columns = validate_required_columns(sales_data, REQUIRED_COLUMNS)

    if rows <= 0:
        raise AssertionError("The dataset must contain at least one row.")

    if columns <= 0:
        raise AssertionError("The dataset must contain at least one column.")

    if missing_columns:
        raise AssertionError(f"Missing required columns: {missing_columns}")

    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_PATH.write_text(
        build_data_loading_summary(
            data=sales_data,
            source_path=RAW_DATA_PATH,
            required_columns=REQUIRED_COLUMNS,
        ),
        encoding="utf-8",
    )

    print("Data loading check passed.")
    print(f"Rows: {rows}")
    print(f"Columns: {columns}")
    print(f"Column names: {data_columns}")
    print(f"Summary written to: {SUMMARY_PATH}")


if __name__ == "__main__":
    main()