
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
