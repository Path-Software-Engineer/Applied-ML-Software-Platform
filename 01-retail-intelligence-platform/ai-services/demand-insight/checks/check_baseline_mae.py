"""Manual end-to-end validation for an existing Demand Insight artifact."""

from artifact_checks import check_baseline


if __name__ == "__main__":
    check_baseline(True)
