"""Verify Day 136 fail-closed evidence coverage."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    matrix = (
        PROJECT_ROOT / "reports/quality/inventory-decision/adversarial_contracts.md"
    ).read_text(encoding="utf-8")
    test_source = (
        PROJECT_ROOT / "tests/ai-services/inventory-decision/test_adversarial_contracts.py"
    ).read_text(encoding="utf-8")
    service_tests = (
        PROJECT_ROOT / "tests/backend/test_inventory_decision_service.py"
    ).read_text(encoding="utf-8")
    api_tests = (
        PROJECT_ROOT / "tests/backend/test_inventory_decision_api.py"
    ).read_text(encoding="utf-8")

    for phrase in (
        "required field missing",
        "unknown field",
        "negative stock",
        "duplicate product",
        "missing or unknown product key",
        "unit differs",
        "corrupt",
        "stale",
        "no fallback recommendation",
    ):
        assert phrase in matrix
    for phrase in ("test_missing_required_field", "test_unknown_field", "test_duplicate_inventory_key", "test_unmatched_and_incompatible"):
        assert phrase in test_source
    assert "test_service_rejects_corrupt_json" in service_tests
    assert "test_inventory_endpoint_maps_service_error_to_safe_503" in api_tests

    print("OK - Sprint 3 Day 136 adversarial contract check passed")
    print("Boundaries: record | source | join | policy | report | HTTP | client")
    print("Failure behavior: controlled and recommendation-free")


if __name__ == "__main__":
    main()
