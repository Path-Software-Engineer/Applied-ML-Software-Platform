"""Official Gradient Boosting candidate for Sprint 2."""

from __future__ import annotations

from pathlib import Path

from sklearn.ensemble import GradientBoostingRegressor

from .candidate import run_candidate
from .contract import EXPERIMENT_CONTRACT
from .results import CandidateResult


MODEL_ID = "gradient_boosting"
MODEL_NAME = "Gradient Boosting"
MODEL_FAMILY = "boosted_tree_ensemble"
MODEL_PARAMETERS: dict[str, object] = {
    "n_estimators": 100,
    "learning_rate": 0.05,
    "max_depth": 2,
    "min_samples_leaf": 2,
    "loss": "squared_error",
    "random_state": EXPERIMENT_CONTRACT.random_seed,
}


def run_gradient_boosting(project_root: Path) -> CandidateResult:
    """Train, evaluate and persist the official boosting candidate."""
    result, _ = run_candidate(
        project_root,
        model_id=MODEL_ID,
        model_name=MODEL_NAME,
        model_family=MODEL_FAMILY,
        estimator=GradientBoostingRegressor(**MODEL_PARAMETERS),
        estimator_parameters=MODEL_PARAMETERS,
    )
    return result


def main() -> None:
    """Generate official Day 62 artifacts."""
    project_root = Path(__file__).resolve().parents[4]
    result = run_gradient_boosting(project_root)
    print("Gradient Boosting candidate generated")
    print(f"MAE: {result.metrics.mae:.4f} units")
    print(f"RMSE: {result.metrics.rmse:.4f} units")
    print(f"R²: {result.metrics.r2:.4f}")


if __name__ == "__main__":
    main()
