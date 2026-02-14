#!/usr/bin/env python3
"""
SDD Book EPUB Build Script

Usage: python scripts/build-epub.py [--git-hash HASH] [--build-date DATE]

Assembles front matter, parts, chapters, and back matter into EPUB
using pandoc. Scans content/ directory and includes files in order.

Dependencies:
  - pandoc
  - Run scripts/build-cover.py first for cover image
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
COVER_IMAGE = REPO_ROOT / "output" / "front-cover.png"
METADATA_FILE = REPO_ROOT / "build" / "epub" / "metadata.yaml"
CSS_FILE = REPO_ROOT / "build" / "epub" / "styles.css"
OUTPUT_DIR = REPO_ROOT / "output"
BOOK_TITLE = "spec-driven-development"

SECTION_ORDER = [
    "00-front-matter",
    "01-part-1-foundation",
    "02-part-2-writing-specifications",
    "03-part-3-the-workflow",
    "04-part-4-practice",
    "05-part-5-governance-and-evolution",
    "06-closing",
    "07-back-matter",
]


def check_deps():
    """Verify pandoc is available."""
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: pandoc not found. Install with: sudo apt-get install pandoc")
        sys.exit(1)


def get_sort_key(path: Path) -> tuple[int, str]:
    """Sort files by numeric prefix, then alphabetically."""
    match = re.match(r"^(\d+)", path.stem)
    return (int(match.group(1)) if match else 999, path.stem)


def scan_content() -> list[Path]:
    """Scan content directories and return files in book order."""
    all_files = []

    for dirname in SECTION_ORDER:
        dirpath = CONTENT_DIR / dirname
        if not dirpath.exists():
            print(f"  {dirname}/ (empty or missing)")
            continue

        files = sorted(dirpath.glob("*.md"), key=get_sort_key)
        if files:
            print(f"  {dirname}/")
            for f in files:
                print(f"    [ok] {f.name}")
                all_files.append(f)
        else:
            print(f"  {dirname}/ (empty)")

    return all_files


def build_epub(git_hash: str | None = None, build_date: str | None = None):
    """Build the EPUB."""
    output_file = OUTPUT_DIR / f"{BOOK_TITLE}.epub"

    print(f"Building: {output_file.name}\n")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Scanning content...")
    all_files = scan_content()

    if not all_files:
        print("\nERROR: No content files found.")
        sys.exit(1)

    print(f"\nTotal: {len(all_files)} files")

    # Build pandoc command
    cmd = [
        "pandoc",
        "--toc",
        "--toc-depth=2",
        "--epub-chapter-level=1",
        "--epub-title-page=false",
        "-o",
        str(output_file),
    ]

    if METADATA_FILE.exists():
        cmd.append(f"--metadata-file={METADATA_FILE}")
    if COVER_IMAGE.exists():
        cmd.append(f"--epub-cover-image={COVER_IMAGE}")
    if CSS_FILE.exists():
        cmd.append(f"--css={CSS_FILE}")
    if git_hash:
        cmd.append(f"--variable=git-hash:{git_hash}")
    if build_date:
        cmd.append(f"--variable=build-date:{build_date}")

    cmd.extend(str(f) for f in all_files)

    print("Running pandoc...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR:\n{result.stderr}")
        sys.exit(1)

    size_kb = output_file.stat().st_size / 1024
    print(f"Done: {output_file} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build SDD Book EPUB")
    parser.add_argument("--git-hash", help="Short git commit hash")
    parser.add_argument("--build-date", help="Build date (YYYY-MM-DD)")
    args = parser.parse_args()

    check_deps()
    build_epub(git_hash=args.git_hash, build_date=args.build_date)
