#!/usr/bin/env python3
"""Build cover PNG from SVG source."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COVER_SVG = REPO_ROOT / "assets" / "cover" / "cover.svg"
OUTPUT_DIR = REPO_ROOT / "output"
OUTPUT_PNG = OUTPUT_DIR / "cover.png"

# Cover dimensions
WIDTH = 1600
HEIGHT = 2286


def check_deps():
    """Verify rsvg-convert is available."""
    try:
        subprocess.run(
            ["rsvg-convert", "--version"],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        print("Error: rsvg-convert not found. Run scripts/setup-deps.sh first.")
        sys.exit(1)


def build_cover():
    """Convert SVG to PNG."""
    if not COVER_SVG.exists():
        print(f"Error: {COVER_SVG} not found.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Building cover: {COVER_SVG} -> {OUTPUT_PNG}")
    subprocess.run(
        [
            "rsvg-convert",
            "-w",
            str(WIDTH),
            "-h",
            str(HEIGHT),
            str(COVER_SVG),
            "-o",
            str(OUTPUT_PNG),
        ],
        check=True,
    )
    print(f"Done: {OUTPUT_PNG} ({OUTPUT_PNG.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    check_deps()
    build_cover()
