
# DAY-09-TEMPORAL-FEATURES
import pandas as pd


def add_date_features(data: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """Add temporal features from a date column.

    Created for Sprint 1 Day 9 of the Demand Insight Module.
    """
    if date_column not in data.columns:
        raise ValueError(f"Missing required date column: {date_column}")

    enriched = data.copy()
    parsed_dates = pd.to_datetime(enriched[date_column], errors="coerce")

    if parsed_dates.isna().any():
        raise ValueError("Date column contains invalid dates.")

    enriched[date_column] = parsed_dates.dt.strftime("%Y-%m-%d")
    enriched["day_of_week"] = parsed_dates.dt.dayofweek
    enriched["month"] = parsed_dates.dt.month
    enriched["year"] = parsed_dates.dt.year
    enriched["is_weekend"] = enriched["day_of_week"].isin([5, 6])

    return enriched

# DAY-10-REVENUE-PROCESSED-DATASET
import pandas as pd


def add_revenue_column(
    data: pd.DataFrame,
    units_column: str = "units_sold",
    price_column: str = "unit_price",
    revenue_column: str = "revenue",
) -> pd.DataFrame:
    """Add revenue as units sold multiplied by unit price.

    Created for Sprint 1 Day 10 of the Demand Insight Module.
    """
    required_columns = [units_column, price_column]
    missing_columns = [column for column in required_columns if column not in data.columns]

    if missing_columns:
        raise ValueError(f"Missing required revenue columns: {missing_columns}")

    enriched = data.copy()
    enriched[units_column] = pd.to_numeric(enriched[units_column], errors="coerce")
    enriched[price_column] = pd.to_numeric(enriched[price_column], errors="coerce")

    if enriched[[units_column, price_column]].isna().any().any():
        raise ValueError("Units or price columns contain invalid numeric values.")

    enriched[revenue_column] = enriched[units_column] * enriched[price_column]

    return enriched
