#!/usr/bin/env python3
"""Upload build artifacts to Azure Blob Storage."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "output"

# Files to upload
ARTIFACTS = [
    "spec-driven-development.epub",
]


def check_deps():
    """Verify az CLI is available."""
    try:
        subprocess.run(
            ["az", "version"],
            capture_output=True,
            check=True,
        )
    except FileNotFoundError:
        print("Error: az CLI not found.")
        sys.exit(1)


def upload(storage_account: str, container: str):
    """Upload artifacts to blob storage."""
    for filename in ARTIFACTS:
        filepath = OUTPUT_DIR / filename
        if not filepath.exists():
            print(f"  Skipping {filename} (not found)")
            continue

        print(f"  Uploading {filename}...")
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

    print("\nFiles available at:")
    print(f"  https://{storage_account}.blob.core.windows.net/{container}/")


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <storage-account-name> [container]")
        sys.exit(1)

    storage_account = sys.argv[1]
    container = sys.argv[2] if len(sys.argv) > 2 else "downloads"

    print(f"Uploading to {storage_account}/{container}...\n")

    upload(storage_account, container)
    print("\nDone.")


if __name__ == "__main__":
    check_deps()
    main()
