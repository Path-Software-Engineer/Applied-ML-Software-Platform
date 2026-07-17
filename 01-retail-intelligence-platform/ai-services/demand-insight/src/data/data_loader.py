from pathlib import Path

import pandas as pd


def load_sales_data(file_path: str | Path) -> pd.DataFrame:
    """Load the raw sales dataset from a CSV file."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Sales data file not found: {path}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a CSV file, got: {path.suffix}")

    data = pd.read_csv(path)

    if data.empty:
        raise ValueError("Sales dataset is empty.")

    return data


def get_data_shape(data: pd.DataFrame) -> tuple[int, int]:
    """Return the number of rows and columns in the dataset."""
    return data.shape


def get_data_columns(data: pd.DataFrame) -> list[str]:
    """Return dataset column names."""
    return list(data.columns)


def validate_required_columns(
    data: pd.DataFrame,
    required_columns: list[str],
) -> list[str]:
    """Return missing required columns from the dataset."""
    current_columns = set(data.columns)
    return [column for column in required_columns if column not in current_columns]


def build_data_loading_summary(
    data: pd.DataFrame,
    source_path: str | Path,
    required_columns: list[str],
) -> str:
    """Build a Markdown summary for the data loading step."""
    rows, columns = get_data_shape(data)
    data_columns = get_data_columns(data)
    missing_columns = validate_required_columns(data, required_columns)

    missing_text = "None" if not missing_columns else ", ".join(missing_columns)

    return f"""# Data Loading Summary — Demand Insight Module

## Source

```txt
{source_path}
```

## Shape

```txt
rows: {rows}
columns: {columns}
```

## Columns

```txt
{', '.join(data_columns)}
```

## Required columns

```txt
{', '.join(required_columns)}
```

## Missing required columns

```txt
{missing_text}
```

## Result

The raw sales dataset was loaded successfully.

This step confirms that the Demand Insight Module can read the raw input before cleaning, feature engineering, baseline calculation or metric evaluation.
"""