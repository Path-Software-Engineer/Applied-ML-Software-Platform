"""Official Random Forest candidate for Sprint 2."""

from __future__ import annotations

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor

from .candidate import run_candidate
from .contract import EXPERIMENT_CONTRACT
from .results import CandidateResult


MODEL_ID = "random_forest"
MODEL_NAME = "Random Forest"
MODEL_FAMILY = "tree_ensemble"
MODEL_PARAMETERS: dict[str, object] = {
    "n_estimators": 200,
    "max_depth": 4,
    "min_samples_leaf": 2,
    "random_state": EXPERIMENT_CONTRACT.random_seed,
    "n_jobs": 1,
}


def run_random_forest(project_root: Path) -> CandidateResult:
    """Train, evaluate and persist the official forest candidate."""
    result, _ = run_candidate(
        project_root,
        model_id=MODEL_ID,
        model_name=MODEL_NAME,
        model_family=MODEL_FAMILY,
        estimator=RandomForestRegressor(**MODEL_PARAMETERS),
        estimator_parameters=MODEL_PARAMETERS,
    )
    return result


def main() -> None:
    """Generate official Day 61 artifacts."""
    project_root = Path(__file__).resolve().parents[4]
    result = run_random_forest(project_root)
    print("Random Forest candidate generated")
    print(f"MAE: {result.metrics.mae:.4f} units")
    print(f"RMSE: {result.metrics.rmse:.4f} units")
    print(f"R²: {result.metrics.r2:.4f}")


if __name__ == "__main__":
    main()
