"""Tests for factual inventory snapshot summaries."""

from __future__ import annotations

import pandas as pd

from inventory_decision.reporting.snapshot_summary import (
    build_snapshot_summary,
    render_snapshot_summary,
)


def joined_snapshot() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "snapshot_id": ["S1", "S1"],
            "snapshot_as_of_date": ["2026-01-09", "2026-01-09"],
            "observed_at": ["2026-01-09", "2026-01-07"],
            "freshness_days": [0, 2],
            "product_id": ["P001", "P002"],
            "stock_on_hand": [0, 9],
            "stock_unit": ["units", "units"],
            "lead_time_days": [None, None],
            "signal_type": ["observed_daily_average"] * 2,
            "signal_value": [3.0, 4.0],
            "signal_unit": ["units_per_day"] * 2,
            "period_start": ["2026-01-01"] * 2,
            "period_end": ["2026-01-09"] * 2,
        }
    )


def test_summary_separates_facts_from_decisions() -> None:
    summary = build_snapshot_summary(joined_snapshot())

    assert summary["snapshot"]["products"] == 2
    assert summary["snapshot"]["stock_on_hand_units"] == 9
    assert summary["snapshot"]["zero_stock_products"] == 1
    assert summary["decision_status"] == "not_calculated"
    assert "risk" not in summary


def test_summary_markdown_states_evidence_boundary() -> None:
    markdown = render_snapshot_summary(build_snapshot_summary(joined_snapshot()))

    assert "validated snapshot facts" in markdown
    assert "recommendations have not been calculated" in markdown
