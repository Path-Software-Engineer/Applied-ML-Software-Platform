"""Verify that installed backend packages match the Day 24 lock file."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOCK_PATH = PROJECT_ROOT / "backend/api/requirements-lock.txt"


def main() -> None:
    if not LOCK_PATH.is_file():
        raise AssertionError(f"Backend dependency lock is missing: {LOCK_PATH}")

    expected = {}
    for line in LOCK_PATH.read_text(encoding="utf-8").splitlines():
        candidate = line.strip()
        if not candidate or candidate.startswith("#"):
            continue
        if candidate.count("==") != 1:
            raise AssertionError(f"Dependency is not exactly pinned: {candidate}")
        package, expected_version = candidate.split("==", maxsplit=1)
        expected[package] = expected_version

    mismatches = []
    for package, expected_version in expected.items():
        try:
            installed_version = version(package)
        except PackageNotFoundError:
            mismatches.append(f"{package}: missing")
            continue
        if installed_version != expected_version:
            mismatches.append(
                f"{package}: expected {expected_version}, installed {installed_version}"
            )
    if mismatches:
        raise AssertionError(f"Backend dependency mismatch: {mismatches}")

    print("OK - Day 24 backend dependency lock check passed")
    print(f"Pinned packages: {len(expected)}")
    print("FastAPI: 0.136.3")
    print("Uvicorn: 0.49.0")
    print("HTTPX: 0.28.1")
    print("Pydantic: 2.13.4")


if __name__ == "__main__":
    main()
