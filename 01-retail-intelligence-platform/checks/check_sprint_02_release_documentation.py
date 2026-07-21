"""Validate Day 81 release documentation and story traceability."""

from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    contract = (PROJECT_ROOT / "docs/model-comparison-read-contract.md").read_text(
        encoding="utf-8"
    )
    model_cards = (
        PROJECT_ROOT / "reports/model-cards/model-comparison/README.md"
    ).read_text(encoding="utf-8")
    users = (PROJECT_ROOT / "docs/user-stories.md").read_text(encoding="utf-8")
    technical = (PROJECT_ROOT / "docs/technical-stories.md").read_text(
        encoding="utf-8"
    )
    scope = (PROJECT_ROOT / "docs/model-comparison-release-scope.md").read_text(
        encoding="utf-8"
    )

    assert "Finalized for Sprint 2" in contract
    assert "Proposed success resource" not in contract
    assert "Proposed unavailable response" not in contract
    assert "not deployment approval" in model_cards
    user_ids = set(re.findall(r"US-S2-\d{3}", users))
    technical_user_ids = set(re.findall(r"US-S2-\d{3}", technical))
    assert user_ids == {f"US-S2-{number:03d}" for number in range(1, 7)}
    assert technical_user_ids <= user_ids
    for technical_id in (f"TS-S2-{number:03d}" for number in range(1, 7)):
        assert technical_id in technical
    for phrase in (
        "18 synthetic rows",
        "six-row chronological holdout",
        "Sprint 3 implementation",
    ):
        assert phrase in scope

    print("OK - Sprint 2 Day 81 release documentation check passed")
    print("User Stories: 6 | Technical Stories: 6")
    print("Read contract: final schema 1.0")
    print("Limitations and Sprint 3 boundary: explicit")


if __name__ == "__main__":
    main()
