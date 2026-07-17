"""Tests for validated Demand Insight figure resolution."""

from pathlib import Path

import pytest

from backend.api.app.services.demand_figure_service import (
    FIGURE_PATHS,
    PNG_SIGNATURE,
    DemandFigureError,
    DemandFigureService,
    UnknownDemandFigureError,
)


def write_figure(project_root: Path, figure_id: str, content: bytes) -> Path:
    path = project_root / FIGURE_PATHS[figure_id]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def test_service_resolves_allowlisted_valid_png(tmp_path: Path) -> None:
    expected = write_figure(
        tmp_path,
        "daily-sales",
        PNG_SIGNATURE + b"controlled-png-content",
    )

    result = DemandFigureService(tmp_path).get_figure_path("daily-sales")

    assert result == expected


def test_service_rejects_unknown_figure_identifier(tmp_path: Path) -> None:
    with pytest.raises(UnknownDemandFigureError, match="Unknown"):
        DemandFigureService(tmp_path).get_figure_path("../../private")


def test_service_rejects_missing_known_figure(tmp_path: Path) -> None:
    with pytest.raises(DemandFigureError, match="missing"):
        DemandFigureService(tmp_path).get_figure_path("daily-sales")


def test_service_rejects_invalid_png_signature(tmp_path: Path) -> None:
    write_figure(tmp_path, "daily-sales", b"not-a-png")

    with pytest.raises(DemandFigureError, match="valid PNG"):
        DemandFigureService(tmp_path).get_figure_path("daily-sales")
