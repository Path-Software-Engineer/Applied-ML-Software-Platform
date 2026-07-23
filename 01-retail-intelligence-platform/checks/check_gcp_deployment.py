"""Validate the reproducible GCP deployment package without deploying it."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    target = PROJECT_ROOT / path
    assert target.is_file(), f"Missing deployment file: {path}"
    return target.read_text(encoding="utf-8")


def main() -> None:
    backend = read("deployment/docker/backend.Dockerfile")
    frontend = read("deployment/docker/frontend.Dockerfile")
    server = read("deployment/docker/serve-frontend.mjs")
    deploy = read("deployment/gcp/deploy.ps1")
    backend_build = read("deployment/gcp/cloudbuild-backend.yaml")
    frontend_build = read("deployment/gcp/cloudbuild-frontend.yaml")
    guide = read("deployment/gcp/README.md")
    settings = read("backend/api/app/settings.py")

    assert "python:3.12.11-slim-bookworm" in backend
    assert "USER 10001:10001" in backend
    assert "PORT=8080" in backend
    assert "node:24.15.0-alpine" in frontend
    assert "USER node" in frontend
    assert "VITE_API_BASE_URL" in frontend
    assert "frame-ancestors 'none'" in server
    assert 'server.listen(port, "0.0.0.0"' in server
    assert "healthz" in server

    for build in (backend_build, frontend_build):
        assert "$PROJECT_ID" in build
        assert "${_REGION}-docker.pkg.dev" in build
        assert ":latest" not in build
    assert "_API_BASE_URL" in frontend_build

    for phrase in (
        "Artifact Registry",
        "Cloud Build",
        "Cloud Run",
        "CORS_ALLOWED_ORIGINS",
        "--allow-unauthenticated",
        "--service-account",
        "Invoke-RestMethod",
        "git status --porcelain",
    ):
        assert phrase in deploy
    for endpoint in (
        "/health",
        "/healthz",
        "/api/v1/demand-insights/summary",
        "/api/v1/model-comparisons/summary",
        "/api/v1/inventory-decisions/summary",
    ):
        assert endpoint in deploy

    assert deploy.count('"--min=0"') == 2
    assert deploy.count('"--max=1"') == 2
    assert '"--max=3"' not in deploy

    assert 'origin == "*"' in settings
    assert "exact HTTP(S) origins" in settings
    assert "No wildcard CORS policy" in guide
    assert "No service-account key" in guide

    combined = "\n".join((backend, frontend, server, deploy, backend_build, frontend_build, guide))
    for forbidden in ("PRIVATE KEY", "api_key=", "password=", "Bearer "):
        assert forbidden not in combined

    print("OK - GCP Cloud Run deployment package check passed")
    print("Images: FastAPI | React static server")
    print("Delivery: Cloud Build -> Artifact Registry -> Cloud Run")
    print("Remote deployment: intentionally not executed")


if __name__ == "__main__":
    main()
