"""Validate the frozen documentation-only Week 10 policy exploration."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    exploration = (
        PROJECT_ROOT
        / "docs"
        / "sprints"
        / "sprint-03-inventory-decision"
        / "week-10"
        / "exploration.md"
    ).read_text(encoding="utf-8")
    policy = (PROJECT_ROOT / "docs" / "inventory-decision-policy.md").read_text(
        encoding="utf-8"
    )

    for value in (
        "default lead time | 2 days",
        "safety horizon | 1 demand day",
        "review period | 3 days",
        "reorder_point = ceil",
        "deterministic priority index",
        "No policy function",
    ):
        assert value in exploration
    assert "inventory-review-policy/1.0" in policy
    assert "calibrated probability" in policy

    print("OK - Sprint 3 Day 120 policy exploration check passed")
    print("Policy: inventory-review-policy/1.0")
    print("Lead / safety / review days: 2 / 1 / 3")
    print("Runtime policy implementation: not started")


if __name__ == "__main__":
    main()
