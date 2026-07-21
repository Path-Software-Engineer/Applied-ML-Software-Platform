"""Official Linear Regression candidate for Sprint 2."""

from __future__ import annotations

from pathlib import Path

from sklearn.linear_model import LinearRegression

from .candidate import run_candidate
from .results import CandidateResult


MODEL_ID = "linear_regression"
MODEL_NAME = "Linear Regression"
MODEL_FAMILY = "linear_model"
MODEL_PARAMETERS: dict[str, object] = {
    "fit_intercept": True,
    "positive": False,
}


def run_linear_regression(project_root: Path) -> CandidateResult:
    """Train, evaluate and persist the official linear candidate."""
    result, _ = run_candidate(
        project_root,
        model_id=MODEL_ID,
        model_name=MODEL_NAME,
        model_family=MODEL_FAMILY,
        estimator=LinearRegression(**MODEL_PARAMETERS),
        estimator_parameters=MODEL_PARAMETERS,
    )
    return result


def main() -> None:
    """Generate official Day 60 artifacts."""
    project_root = Path(__file__).resolve().parents[4]
    result = run_linear_regression(project_root)
    print("Linear Regression candidate generated")
    print(f"MAE: {result.metrics.mae:.4f} units")
    print(f"RMSE: {result.metrics.rmse:.4f} units")
    print(f"R²: {result.metrics.r2:.4f}")


if __name__ == "__main__":
    main()
