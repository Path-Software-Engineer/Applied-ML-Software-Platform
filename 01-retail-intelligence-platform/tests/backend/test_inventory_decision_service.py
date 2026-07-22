"""Tests for the read-only Inventory Decision service."""

from __future__ import annotations

from datetime import date
import json
from pathlib import Path
import shutil

import pytest

from backend.api.app.services.inventory_decision_service import (
    InventoryDecisionError,
    InventoryDecisionService,
    REPORT_RELATIVE_PATH,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_REPORT = PROJECT_ROOT / REPORT_RELATIVE_PATH


def service_with_report(tmp_path: Path) -> tuple[InventoryDecisionService, Path]:
    target = tmp_path / REPORT_RELATIVE_PATH
    target.parent.mkdir(parents=True)
    shutil.copyfile(SOURCE_REPORT, target)
    return InventoryDecisionService(tmp_path), target


def test_service_maps_valid_report_and_current_freshness(tmp_path: Path) -> None:
    service, _ = service_with_report(tmp_path)

    resource = service.get_summary(today=date(2026, 1, 12))

    assert resource["schema_version"] == "1.0"
    assert resource["freshness"] == {
        "evidence_as_of_date": "2026-01-09",
        "age_days": 3,
        "stale_after_days": 7,
        "status": "current",
    }
    assert resource["summary"]["products"] == 6
    assert len(resource["recommendation_cards"]) == 6
    assert "inventory_sha256" not in resource["integration"]


def test_service_marks_old_evidence_stale(tmp_path: Path) -> None:
    service, _ = service_with_report(tmp_path)

    resource = service.get_summary(today=date(2026, 1, 20))

    assert resource["freshness"]["status"] == "stale"
    assert resource["freshness"]["age_days"] == 11


def test_service_rejects_missing_report(tmp_path: Path) -> None:
    with pytest.raises(InventoryDecisionError, match="missing"):
        InventoryDecisionService(tmp_path).get_summary()


def test_service_rejects_corrupt_json(tmp_path: Path) -> None:
    target = tmp_path / REPORT_RELATIVE_PATH
    target.parent.mkdir(parents=True)
    target.write_text("{broken", encoding="utf-8")

    with pytest.raises(InventoryDecisionError, match="cannot be read"):
        InventoryDecisionService(tmp_path).get_summary()


def test_service_rejects_inconsistent_card_order(tmp_path: Path) -> None:
    service, target = service_with_report(tmp_path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    payload["recommendation_cards"].reverse()
    target.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(InventoryDecisionError, match="identities are inconsistent"):
        service.get_summary()


def test_service_rejects_probability_claim(tmp_path: Path) -> None:
    service, target = service_with_report(tmp_path)
    payload = json.loads(target.read_text(encoding="utf-8"))
    payload["ranking"][0]["risk_score_meaning"] = "stockout_probability"
    target.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(InventoryDecisionError, match="risk meaning"):
        service.get_summary()
