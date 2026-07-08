from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "date",
    "product_id",
    "product_name",
    "units_sold",
    "unit_price",
]


def validate_required_columns(data: pd.DataFrame) -> None:
    """Validate that the sales dataset contains the required columns."""
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")


def clean_sales_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean a raw sales dataset and return a clean DataFrame."""
    validate_required_columns(data)

    clean_data = data.copy()

    clean_data["date"] = pd.to_datetime(clean_data["date"], errors="coerce")
    clean_data["product_id"] = clean_data["product_id"].astype(str).str.strip()
    clean_data["product_name"] = clean_data["product_name"].astype(str).str.strip()
    clean_data["units_sold"] = pd.to_numeric(clean_data["units_sold"], errors="coerce")
    clean_data["unit_price"] = pd.to_numeric(clean_data["unit_price"], errors="coerce")

    clean_data = clean_data.dropna(subset=REQUIRED_COLUMNS)
    clean_data = clean_data[clean_data["units_sold"] >= 0]
    clean_data = clean_data[clean_data["unit_price"] >= 0]
    clean_data = clean_data.drop_duplicates()
    clean_data = clean_data.sort_values(by=["date", "product_id"]).reset_index(drop=True)

    return clean_data


def save_clean_sales_data(data: pd.DataFrame, output_path: Path) -> None:
    """Save the clean sales dataset as a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)


def build_clean_sales_dataset(raw_path: Path, output_path: Path) -> pd.DataFrame:
    """Load raw data, clean it, save it and return the clean dataset."""
    raw_data = pd.read_csv(raw_path)
    clean_data = clean_sales_data(raw_data)
    save_clean_sales_data(clean_data, output_path)

    return clean_data