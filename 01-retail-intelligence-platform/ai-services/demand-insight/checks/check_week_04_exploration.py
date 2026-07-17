"""Validate the Day 22 Week 4 exploration evidence."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
REQUIRED_DOCUMENTS = (
    "docs/api-contract.md",
    "docs/sprints/sprint-01-demand-insight/week-04/exploration.md",
    "docs/sprints/sprint-01-demand-insight/week-04/plan.md",
    "reports/summaries/demand-insight/week_04_exploration_summary.md",
)
REQUIRED_CONTRACT_TERMS = (
    "GET /api/v1/demand-insights/summary",
    '"schema_version": "1.0"',
    '"sales_summary"',
    '"baseline"',
    '"leaders"',
    '"insight_cards"',
    "503 Service Unavailable",
)


def main() -> None:
    missing = [
        relative_path
        for relative_path in REQUIRED_DOCUMENTS
        if not (PROJECT_ROOT / relative_path).is_file()
    ]
    if missing:
        raise AssertionError(f"Incomplete Week 4 exploration evidence: {missing}")

    contract = (PROJECT_ROOT / "docs/api-contract.md").read_text(encoding="utf-8")
    missing_terms = [term for term in REQUIRED_CONTRACT_TERMS if term not in contract]
    if missing_terms:
        raise AssertionError(f"Incomplete planned API contract: {missing_terms}")

    exploration = (
        PROJECT_ROOT
        / "docs/sprints/sprint-01-demand-insight/week-04/exploration.md"
    ).read_text(encoding="utf-8")
    if "No backend or frontend functionality was implemented" not in exploration:
        raise AssertionError("Day 22 scope boundary is not explicit.")
    if "Sprint 1 closure criteria" not in exploration:
        raise AssertionError("Sprint 1 closure criteria are missing.")

    print("OK - Day 22 Week 4 exploration check passed")
    print(f"Evidence documents: {len(REQUIRED_DOCUMENTS)}")
    print("Planned endpoint: GET /api/v1/demand-insights/summary")
    print("Schema version: 1.0")
    print("Backend and frontend runtime changes: none")


if __name__ == "__main__":
    main()
