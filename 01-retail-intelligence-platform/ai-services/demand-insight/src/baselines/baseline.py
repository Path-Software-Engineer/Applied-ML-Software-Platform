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

# DAY-14-BASELINE-MAE
import pandas as pd


def calculate_mae(y_true: pd.Series, y_pred: pd.Series) -> float:
    """Calculate mean absolute error between true and predicted values."""
    true_values = pd.to_numeric(y_true, errors="coerce")
    predicted_values = pd.to_numeric(y_pred, errors="coerce")

    if len(true_values) != len(predicted_values):
        raise ValueError("y_true and y_pred must have the same length.")

    valid = true_values.notna() & predicted_values.notna()
    if not valid.any():
        raise ValueError("No valid values available to calculate MAE.")

    return float((true_values[valid] - predicted_values[valid]).abs().mean())
