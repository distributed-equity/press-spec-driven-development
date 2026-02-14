#!/usr/bin/env python3
"""Upload build artifacts to Azure Blob Storage."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"

ARTIFACTS = [
    "spec-driven-development.epub",
    "spec-driven-development.pdf",
    "spec-driven-development-print.pdf",
]


def check_deps():
    """Verify az CLI is available."""
    try:
        subprocess.run(["az", "version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: az CLI not found.")
        sys.exit(1)


def upload(storage_account: str, container: str):
    """Upload artifacts to blob storage."""
    uploaded = 0
    for filename in ARTIFACTS:
        filepath = OUTPUT_DIR / filename
        if not filepath.exists():
            print(f"  Skip {filename} (not found)")
            continue

        size_kb = filepath.stat().st_size / 1024
        print(f"  Uploading {filename} ({size_kb:.1f} KB)...")
        subprocess.run(
            [
                "az",
                "storage",
                "blob",
                "upload",
                "--account-name",
                storage_account,
                "--container-name",
                container,
                "--name",
                filename,
                "--file",
                str(filepath),
                "--overwrite",
            ],
            check=True,
        )
        uploaded += 1

    print(f"\n{uploaded}/{len(ARTIFACTS)} uploaded.")
    print(f"https://{storage_account}.blob.core.windows.net/{container}/")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <storage-account> [container]")
        sys.exit(1)

    storage_account = sys.argv[1]
    container = sys.argv[2] if len(sys.argv) > 2 else "downloads"

    print(f"Uploading to {storage_account}/{container}...\n")
    upload(storage_account, container)


if __name__ == "__main__":
    check_deps()
    main()
