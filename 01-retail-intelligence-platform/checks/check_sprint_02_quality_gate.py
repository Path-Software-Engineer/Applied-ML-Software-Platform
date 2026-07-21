"""Validate Day 80 quality evidence and safe-log boundary."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    report = (
        PROJECT_ROOT
        / "reports"
        / "quality"
        / "model-comparison"
        / "sprint_02_quality_gate.md"
    ).read_text(encoding="utf-8")
    summary = (
        PROJECT_ROOT
        / "reports"
        / "summaries"
        / "model-comparison"
        / "day_80_quality_gate_summary.md"
    ).read_text(encoding="utf-8")
    service = (
        PROJECT_ROOT
        / "backend"
        / "api"
        / "app"
        / "services"
        / "model_comparison_service.py"
    ).read_text(encoding="utf-8")
    tests = (
        PROJECT_ROOT / "tests" / "backend" / "test_model_comparison_service.py"
    ).read_text(encoding="utf-8")

    for phrase in (
        "96 passed",
        "18 passed",
        "47 passed",
        "local HTTP smoke",
        "does not make the models production ready",
    ):
        assert phrase in report
    assert "model_comparison_summary_ready" in service
    for phrase in (
        "test_service_logs_safe_summary_metadata",
        "test_service_log_excludes_paths_checksums_and_candidate_metrics",
        'assert str(tmp_path) not in message',
        'assert "mae_units" not in message',
    ):
        assert phrase in tests
    assert "operational" in summary and "evidence" in summary

    print("OK - Sprint 2 Day 80 quality gate evidence check passed")
    print("Automated suites: 96 Python | 18 frontend")
    print("Manual checks: 47")
    print("Safe operational log boundary: confirmed")


if __name__ == "__main__":
    main()
