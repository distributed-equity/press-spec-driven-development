#!/usr/bin/env python3
"""Build cover PNGs from SVG sources.

Injects build metadata (git hash/tag + date) into the front cover SVG
before rendering to PNG.

Usage:
  python scripts/build-cover.py [--git-hash HASH] [--build-date DATE]
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COVER_DIR = REPO_ROOT / "assets" / "cover"
OUTPUT_DIR = REPO_ROOT / "output"

# Cover definitions: (svg_name, output_name, width, height)
COVERS = [
    ("front-cover.svg", "front-cover.png", 1600, 2286),
    ("spine.svg", "spine.png", 228, 2286),
    ("back-cover.svg", "back-cover.png", 1600, 2286),
]


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


def build_ref(git_hash: str | None, build_date: str | None) -> str:
    """Build the reference string for cover injection.

    Tagged commit:  v1.0.0 · 2026.02.16
    Normal commit:  a3f8bcc · 2026.02.16
    No metadata:    empty string (token removed)
    """
    parts = []
    if git_hash:
        parts.append(git_hash)
    if build_date:
        parts.append(build_date)
    return " · ".join(parts)


def inject_metadata(svg_path: Path, ref: str) -> Path:
    """Replace {{BUILD_REF}} token in SVG, return path to processed file.

    If no token is found, returns the original path unchanged.
    """
    content = svg_path.read_text(encoding="utf-8")

    if "{{BUILD_REF}}" not in content:
        return svg_path

    content = content.replace("{{BUILD_REF}}", ref)

    # Write to a temp file alongside the original so rsvg-convert
    # can resolve any relative references
    tmp_path = svg_path.parent / f".{svg_path.stem}-build{svg_path.suffix}"
    tmp_path.write_text(content, encoding="utf-8")
    print(f"  Injected build ref: {ref}")
    return tmp_path


def build_cover(
    svg_name: str,
    png_name: str,
    width: int,
    height: int,
    git_hash: str | None = None,
    build_date: str | None = None,
):
    """Convert a single SVG to PNG, injecting metadata if applicable."""
    svg_path = COVER_DIR / svg_name
    png_path = OUTPUT_DIR / png_name

    if not svg_path.exists():
        print(f"  Skipping {svg_name} (not found)")
        return

    # Inject build metadata into front cover
    tmp_path = None
    if svg_name == "front-cover.svg" and (git_hash or build_date):
        ref = build_ref(git_hash, build_date)
        render_path = inject_metadata(svg_path, ref)
        if render_path != svg_path:
            tmp_path = render_path
    else:
        render_path = svg_path

    try:
        subprocess.run(
            [
                "rsvg-convert",
                "-w",
                str(width),
                "-h",
                str(height),
                str(render_path),
                "-o",
                str(png_path),
            ],
            check=True,
        )
        size_kb = png_path.stat().st_size / 1024
        print(f"  {svg_name} -> {png_name} ({size_kb:.0f} KB)")
    finally:
        # Clean up temp file
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()


def main():
    """Build all cover images."""
    print("Building cover images...\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for svg_name, png_name, width, height in COVERS:
        build_cover(svg_name, png_name, width, height, args.git_hash, args.build_date)

    print("\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build cover PNGs from SVG sources")
    parser.add_argument("--git-hash", help="Short git hash or version tag")
    parser.add_argument("--build-date", help="Build date (YYYY.MM.DD)")
    args = parser.parse_args()

    check_deps()
    main()
