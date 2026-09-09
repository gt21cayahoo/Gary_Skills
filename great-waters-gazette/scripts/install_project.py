#!/usr/bin/env python3
"""Install the Gazette project seed and site template into a new directory."""

from pathlib import Path
import shutil
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: install_project.py DESTINATION")
        return 2
    destination = Path(sys.argv[1]).expanduser().resolve()
    if destination.exists() and any(destination.iterdir()):
        print(f"Refusing to overwrite non-empty destination: {destination}")
        return 1
    destination.mkdir(parents=True, exist_ok=True)
    skill_root = Path(__file__).resolve().parent.parent
    shutil.copytree(skill_root / "assets" / "project-seed" / "great-waters-gazette", destination / "great-waters-gazette")
    shutil.copytree(skill_root / "assets" / "site-template", destination / "great-waters-gazette-site")
    (destination / "great-waters-gazette" / "archive").mkdir(exist_ok=True)
    (destination / "great-waters-gazette" / "assets").mkdir(exist_ok=True)
    (destination / "output" / "pdf").mkdir(parents=True)
    print(f"Installed Great Waters Gazette workspace at {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
