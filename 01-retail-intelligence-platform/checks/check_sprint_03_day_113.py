"""Validate the documentation-only Sprint 3 exploration boundary."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    required = (
        "docs/sprints/sprint-03-inventory-decision/README.md",
        "docs/sprints/sprint-03-inventory-decision/week-09/exploration.md",
        "docs/sprints/sprint-03-inventory-decision/week-09/plan.md",
        "docs/inventory-data-contract.md",
        "docs/demand-signal-contract.md",
        "docs/inventory-decision-policy.md",
        "reports/summaries/inventory-decision/day_113_exploration_summary.md",
    )
    for relative in required:
        path = PROJECT_ROOT / relative
        assert path.is_file(), f"Missing Day 113 evidence: {relative}"
        assert path.read_text(encoding="utf-8").strip(), f"Empty evidence: {relative}"

    stories = (PROJECT_ROOT / "docs/user-stories.md").read_text(encoding="utf-8")
    technical = (PROJECT_ROOT / "docs/technical-stories.md").read_text(
        encoding="utf-8"
    )
    for index in range(1, 7):
        assert f"US-S3-{index:03d}" in stories
        assert f"TS-S3-{index:03d}" in technical

    exploration = (PROJECT_ROOT / required[1]).read_text(encoding="utf-8")
    assert "not a production forecast" in exploration
    assert "No calculation, endpoint or React feature" in exploration

    print("OK - Sprint 3 Day 113 exploration check passed")
    print("User Stories / Technical Stories: 6 / 6")
    print("Runtime scope: not started")


if __name__ == "__main__":
    main()
