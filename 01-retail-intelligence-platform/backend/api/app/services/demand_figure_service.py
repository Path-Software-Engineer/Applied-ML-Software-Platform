"""Resolve validated Demand Insight figures for HTTP delivery."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[4]
FIGURE_PATHS = {
    "daily-sales": "reports/figures/demand-insight/daily_sales.png",
    "product-units-ranking": (
        "reports/figures/demand-insight/product_units_ranking.png"
    ),
    "product-revenue-ranking": (
        "reports/figures/demand-insight/product_revenue_ranking.png"
    ),
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_FIGURE_BYTES = 10 * 1024 * 1024


class DemandFigureError(RuntimeError):
    """Raised when a known figure is unavailable or invalid."""


class UnknownDemandFigureError(DemandFigureError):
    """Raised when a figure identifier is not part of the public contract."""


class DemandFigureService:
    """Resolve only allowlisted, valid PNG artifacts."""

    def __init__(self, project_root: Path = PROJECT_ROOT) -> None:
        self.project_root = Path(project_root)

    def get_figure_path(self, figure_id: str) -> Path:
        relative_path = FIGURE_PATHS.get(figure_id)
        if relative_path is None:
            raise UnknownDemandFigureError(
                f"Unknown Demand Insight figure: {figure_id}"
            )

        path = self.project_root / relative_path
        if not path.is_file():
            raise DemandFigureError(f"Required figure is missing: {path}")

        try:
            size = path.stat().st_size
            with path.open("rb") as figure:
                signature = figure.read(len(PNG_SIGNATURE))
        except OSError as error:
            raise DemandFigureError(f"Cannot read figure: {path}") from error

        if size < len(PNG_SIGNATURE) or size > MAX_FIGURE_BYTES:
            raise DemandFigureError(
                f"Figure size is outside the accepted boundary: {path}"
            )
        if signature != PNG_SIGNATURE:
            raise DemandFigureError(f"Figure is not a valid PNG: {path}")
        return path
