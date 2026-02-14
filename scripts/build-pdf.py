#!/usr/bin/env python3
"""
SDD Book PDF Build Script

Assembles all content into a single markdown file with raw LaTeX
injections for structural control (frontmatter/mainmatter/parts),
then passes it to pandoc + XeLaTeX.

Usage:
  python scripts/build-pdf.py [--git-hash HASH] [--build-date DATE] [--variant screen|print|both]

Output:
  output/spec-driven-development.pdf       (screen: RGB, clickable links)
  output/spec-driven-development-print.pdf (print: CMYK-safe, black links)
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# === CONFIGURATION ===

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
METADATA_FILE = REPO_ROOT / "build" / "epub" / "metadata.yaml"
TEMPLATE_FILE = REPO_ROOT / "build" / "pdf" / "template.tex"
COVER_IMAGE = REPO_ROOT / "output" / "front-cover.png"
OUTPUT_DIR = REPO_ROOT / "output"
BOOK_TITLE = "spec-driven-development"

# Fonts
MAIN_FONT = "Source Serif 4"
SANS_FONT = "Inter"
MONO_FONT = "JetBrains Mono"
SLAB_FONT = "Alfa Slab One"
FONT_SIZE = "11pt"

# Content directories in book order
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

# These are handled by the LaTeX template, not content
TEMPLATE_HANDLED = {"01-title-page.md", "02-copyright.md"}


def check_deps():
    """Verify pandoc and xelatex are available."""
    for cmd, pkg in [("pandoc", "pandoc"), ("xelatex", "texlive-xetex")]:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
        except FileNotFoundError:
            print(f"Error: {cmd} not found. Install {pkg}.")
            sys.exit(1)


def get_sort_key(path: Path) -> tuple[int, str]:
    """Sort files by numeric prefix, then alphabetically."""
    match = re.match(r"^(\d+)", path.stem)
    return (int(match.group(1)) if match else 999, path.stem)


def get_markdown_files(directory: Path) -> list[Path]:
    """Get sorted markdown files from a directory."""
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"), key=get_sort_key)


def is_part_directory(dirname: str) -> bool:
    """Check if a directory name represents a book part."""
    return bool(re.match(r"^\d+-part-\d+", dirname))


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    for old, new in [
        ("\\", r"\textbackslash{}"),
        ("&", r"\&"),
        ("%", r"\%"),
        ("$", r"\$"),
        ("#", r"\#"),
        ("_", r"\_"),
        ("{", r"\{"),
        ("}", r"\}"),
        ("~", r"\textasciitilde{}"),
        ("^", r"\textasciicircum{}"),
    ]:
        text = text.replace(old, new)
    text = text.replace("\u2014", "---")
    text = text.replace("\u2013", "--")
    text = text.replace("\u2018", "`")
    text = text.replace("\u2019", "'")
    text = text.replace("\u201c", "``")
    text = text.replace("\u201d", "''")
    return text


def parse_part_intro(filepath: Path) -> str:
    """Extract title from a part intro file.

    Expected: # Part N: Title {.part}
    Returns the title string.
    """
    content = filepath.read_text(encoding="utf-8").strip()

    match = re.match(
        r"^#\s+Part\s+\d+:\s*(.+?)\s*(?:\{[^}]*\})?\s*$",
        content,
        flags=re.MULTILINE,
    )
    if not match:
        raise ValueError(f"Could not parse part intro: {filepath}")

    return match.group(1).strip()


def build_part_latex(title: str, part_number: int) -> str:
    """Build raw LaTeX for a part divider page."""
    return f"\\part{{{title}}}"


def raw_latex(code: str) -> str:
    """Wrap LaTeX code in a pandoc raw block."""
    return f"\n```{{=latex}}\n{code}\n```\n"


def assemble_markdown() -> str:
    """Assemble all content into a single markdown string.

    Structure:
      [preface markdown - stays in frontmatter]
      \\mainmatter  (injected before first part)
      \\part{Title}  (with intro text)
      [chapter markdown]
      ...
    """
    sections: list[str] = []
    mainmatter_injected = False
    part_number = 0

    for dirname in SECTION_ORDER:
        dirpath = CONTENT_DIR / dirname
        files = get_markdown_files(dirpath)

        if not files:
            print(f"  {dirname}/ (empty or missing)")
            continue

        print(f"  {dirname}/")

        for f in files:
            # Skip files handled by LaTeX template
            if f.name in TEMPLATE_HANDLED:
                print(f"    [skip] {f.name} (in template)")
                continue

            # Part intro file
            if f.name == "00-part-intro.md" and is_part_directory(dirname):
                title = parse_part_intro(f)
                part_number += 1

                latex = ""
                if not mainmatter_injected:
                    latex += "\\mainmatter\n"
                    mainmatter_injected = True

                latex += build_part_latex(title, part_number)
                sections.append(raw_latex(latex))
                print(f"    [part] {f.name} -> Part {part_number}: {title}")
                continue

            # Regular content file
            content = f.read_text(encoding="utf-8").strip()
            sections.append(content)
            print(f"    [ok]   {f.name}")

    return "\n\n".join(sections)


def build_pdf(variant: str, git_hash: str | None, build_date: str | None):
    """Build a single PDF variant."""
    is_print = variant == "print"
    suffix = "-print" if is_print else ""
    output_file = OUTPUT_DIR / f"{BOOK_TITLE}{suffix}.pdf"

    print(f"\n{'='*60}")
    print(f"  Building: {output_file.name} ({variant})")
    print(f"{'='*60}\n")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Assemble content
    print("Scanning content...")
    assembled = assemble_markdown()

    if not assembled.strip():
        print("ERROR: No content found.")
        sys.exit(1)

    # Write assembled markdown for pandoc (and debugging)
    assembled_path = OUTPUT_DIR / "assembled.md"
    assembled_path.write_text(assembled, encoding="utf-8")
    print(f"\nAssembled markdown: {assembled_path}")
    print(f"Length: {len(assembled)} chars, {assembled.count(chr(10))} lines")

    # Build pandoc command
    cmd = [
        "pandoc",
        str(assembled_path),
        "--pdf-engine=xelatex",
        "--top-level-division=chapter",
        "-o",
        str(output_file),
    ]

    if TEMPLATE_FILE.exists():
        cmd.append(f"--template={TEMPLATE_FILE}")
    if METADATA_FILE.exists():
        cmd.append(f"--metadata-file={METADATA_FILE}")

    # Fonts
    cmd.extend(
        [
            f"--variable=mainfont:{MAIN_FONT}",
            f"--variable=sansfont:{SANS_FONT}",
            f"--variable=monofont:{MONO_FONT}",
            f"--variable=slabfont:{SLAB_FONT}",
            f"--variable=fontsize:{FONT_SIZE}",
        ]
    )

    # Variant
    if is_print:
        cmd.append("--variable=print:true")
    else:
        if COVER_IMAGE.exists():
            cmd.extend(
                [
                    "--variable=include-cover:true",
                    f"--variable=cover-image:{COVER_IMAGE}",
                ]
            )

    # Build info
    if git_hash:
        cmd.append(f"--variable=git-hash:{git_hash}")
    if build_date:
        cmd.append(f"--variable=build-date:{build_date}")

    print(f"\nPandoc command:\n  {' '.join(cmd)}\n")
    print("Running pandoc + xelatex...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR:\n{result.stderr}")
        print(f"\nDEBUG: Check {assembled_path} for the assembled markdown")
        sys.exit(1)

    size_kb = output_file.stat().st_size / 1024
    print(f"Done: {output_file} ({size_kb:.1f} KB)")

    # Clean up assembled file on success
    assembled_path.unlink(missing_ok=True)

    return output_file


def main():
    parser = argparse.ArgumentParser(description="Build SDD Book PDFs")
    parser.add_argument("--git-hash", help="Short git commit hash")
    parser.add_argument("--build-date", help="Build date (YYYY-MM-DD)")
    parser.add_argument(
        "--variant",
        choices=["screen", "print", "both"],
        default="both",
        help="Which variant(s) to build (default: both)",
    )
    args = parser.parse_args()

    variants = ["screen", "print"] if args.variant == "both" else [args.variant]
    for v in variants:
        build_pdf(v, args.git_hash, args.build_date)

    print(f"\n{'='*60}")
    print("  All builds complete.")
    print(f"{'='*60}")


if __name__ == "__main__":
    check_deps()
    main()
