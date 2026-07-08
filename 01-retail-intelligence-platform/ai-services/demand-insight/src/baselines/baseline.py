"""Demand Insight Python module."""

# DAY-13-MEAN-BASELINE
import pandas as pd


def calculate_mean_baseline(target: pd.Series) -> float:
    """Calculate the mean baseline value for a numeric target."""
    numeric_target = pd.to_numeric(target, errors="coerce").dropna()

    if numeric_target.empty:
        raise ValueError("Target is empty after numeric conversion.")

    return float(numeric_target.mean())


def create_mean_baseline_predictions(target: pd.Series) -> pd.Series:
    """Create constant predictions using the mean baseline value."""
    baseline_value = calculate_mean_baseline(target)
    return pd.Series([baseline_value] * len(target), index=target.index, name="mean_baseline_prediction")
