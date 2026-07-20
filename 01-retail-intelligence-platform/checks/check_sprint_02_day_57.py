"""Validate the documentation-only opening of Sprint 2."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = (
    "docs/model-comparison-experiment-contract.md",
    "docs/sprints/sprint-02-model-comparison/README.md",
    "docs/sprints/sprint-02-model-comparison/week-05/exploration.md",
    "docs/sprints/sprint-02-model-comparison/week-05/plan.md",
    "reports/summaries/model-comparison/day_57_exploration_summary.md",
)
REQUIRED_CONTRACT_TERMS = (
    "units_sold",
    "chronological",
    "Linear Regression",
    "Random Forest",
    "Gradient Boosting",
    "MAE",
    "RMSE",
    "R²",
    "18",
    "production-ready model",
)


def main() -> None:
    """Fail when the Sprint 2 exploration boundary becomes incomplete."""
    documents: dict[str, str] = {}
    for relative_path in EVIDENCE:
        path = PROJECT_ROOT / relative_path
        if not path.is_file():
            raise AssertionError(f"Missing Day 57 evidence: {relative_path}")
        documents[relative_path] = path.read_text(encoding="utf-8")

    contract = documents["docs/model-comparison-experiment-contract.md"]
    missing = [term for term in REQUIRED_CONTRACT_TERMS if term not in contract]
    if missing:
        raise AssertionError(f"Experiment contract is incomplete: {missing}")

    exploration = documents[
        "docs/sprints/sprint-02-model-comparison/week-05/exploration.md"
    ]
    if "Cloud report labs remain unassigned" not in exploration:
        raise AssertionError("Cloud lab boundary is not explicit.")

    user_stories = (PROJECT_ROOT / "docs/user-stories.md").read_text(encoding="utf-8")
    technical_stories = (PROJECT_ROOT / "docs/technical-stories.md").read_text(
        encoding="utf-8"
    )
    decisions = (PROJECT_ROOT / "docs/decisions.md").read_text(encoding="utf-8")
    for story_id in ("US-S2-001", "US-S2-002", "US-S2-003", "US-S2-004"):
        if story_id not in user_stories:
            raise AssertionError(f"Missing Sprint 2 user story: {story_id}")
    for story_id in ("TS-S2-001", "TS-S2-002", "TS-S2-003", "TS-S2-004"):
        if story_id not in technical_stories:
            raise AssertionError(f"Missing Sprint 2 technical story: {story_id}")
    if "Decision 029" not in decisions:
        raise AssertionError("Sprint 2 architecture decision is missing.")

    print("OK - Sprint 2 Day 57 exploration check passed")
    print(f"Evidence documents: {len(EVIDENCE)}")
    print("User stories / technical stories: 4 / 4")
    print("Model training and dependency installation: deferred")


if __name__ == "__main__":
    main()
