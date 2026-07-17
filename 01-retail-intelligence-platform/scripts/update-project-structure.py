"""Generate or verify the deterministic repository structure inventory."""

from __future__ import annotations

import argparse
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "project-structure.txt"
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    ".runtime",
    ".pytest_cache",
    ".pytest-tmp",
    "__pycache__",
    "dist",
    "node_modules",
}


def build_inventory() -> str:
    paths = sorted(
        path.relative_to(PROJECT_ROOT).as_posix()
        for path in PROJECT_ROOT.rglob("*")
        if path.is_file()
        and path != OUTPUT_PATH
        and not EXCLUDED_PARTS.intersection(path.relative_to(PROJECT_ROOT).parts)
    )
    lines = [
        "# Project structure",
        "",
        "Current UTF-8 file paths relative to the repository root.",
        "Excluded: `.git`, `.venv`, `.runtime`, generated `dist`, Python caches and `node_modules`.",
        "",
        "```text",
        *paths,
        "project-structure.txt",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail when project-structure.txt does not match the repository.",
    )
    args = parser.parse_args()
    expected = build_inventory()

    if args.check:
        current = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if current != expected:
            raise SystemExit(
                "project-structure.txt is stale. Run "
                "`.venv\\Scripts\\python.exe scripts\\update-project-structure.py`."
            )
        print("Project structure inventory: current")
        return

    OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
    print(f"Project structure inventory updated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
