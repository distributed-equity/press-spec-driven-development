# Specification Driven Development: The Book

A practical guide to Specification Driven Development (SDD) for professional developers working with AI coding agents.

## What is this?

This repository contains the specifications, content, and build pipeline for a book about Specification Driven Development—a methodology where specifications become the primary artifact and code becomes a generated side effect.

The book is being written using SDD. The specifications in this repo drive the content generation.

## Core Thesis

> The specification is the artifact. Code is a side effect.

## Repository Structure

```
.
├── .github/workflows/       # CI/CD (build book, deploy site)
├── .specmcp/
│   ├── server.py            # MCP server for spec delivery
│   └── specs/
│       ├── editorial/       # What to write (brief, outline, guide, glossary...)
│       └── workflow/        # How to write it
├── assets/
│   ├── cover/               # Cover artwork (SVG sources)
│   └── fonts/               # Bundled fonts (Source Serif 4, Inter, JetBrains Mono, Alfa Slab One)
├── build/
│   ├── epub/                # EPUB metadata and styles
│   └── pdf/                 # LaTeX template for PDF generation
├── content/                 # Book content (front matter, parts, chapters)
├── infra/                   # Azure Bicep IaC
├── scripts/                 # Build, deploy, and setup scripts
├── site/                    # Landing page (GitHub Pages)
└── notes/                   # Research links
```

## Specifications

| Document | Purpose |
|----------|---------|
| `book-brief.md` | Scope, thesis, audience, boundaries |
| `chapter-outline.md` | 26 chapters across 5 parts |
| `writers-guide.md` | Voice, tone, style rules |
| `glossary.md` | 27 canonical term definitions |
| `prior-art.md` | Related practices and positioning |
| `diataxis-integration.md` | Content type framework (Tutorial/How-to/Reference/Explanation) |
| `continuity-tracker.md` | Cross-reference and consistency tracking |
| `workflow.md` | Authoring workflow and CI/CD pipeline |

## Target Audience

Professional developers (3+ years experience) who:

- Use AI coding tools but find ad-hoc prompting frustrating
- Want systematic methods, not hacks
- Value engineering discipline over "vibe coding"

## Outputs

The build pipeline produces three book formats from the same markdown source:

| Format | File | Purpose |
|--------|------|---------|
| **EPUB** | `spec-driven-development.epub` | E-readers and digital distribution |
| **Screen PDF** | `spec-driven-development.pdf` | Digital download with cover, RGB colours, clickable links |
| **Print PDF** | `spec-driven-development-print.pdf` | Print-ready interior (no cover, CMYK-safe, black links) |

All outputs are deployed to Azure Blob Storage on merge to `main`:

```
https://sddbook.blob.core.windows.net/downloads/spec-driven-development.epub
https://sddbook.blob.core.windows.net/downloads/spec-driven-development.pdf
https://sddbook.blob.core.windows.net/downloads/spec-driven-development-print.pdf
```

Each build embeds the short git hash and build date on the copyright page for traceability.

### PDF Typography

PDFs are typeset with XeLaTeX at 6×9 inch trim size using Google Fonts:

- **Source Serif 4** — Body text (designed for long-form reading)
- **Alfa Slab One** — Part and chapter titles
- **Inter** — Section headings
- **JetBrains Mono** — Code blocks

All fonts are committed to `assets/fonts/` for reproducible builds.

## Development

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Install MCP server dependencies (for spec-driven authoring)
pip install -r .specmcp/requirements.txt

# Run linting manually
pre-commit run --all-files
```

The `.specmcp/` directory provides a local MCP server that gives Claude
structured access to book specifications. See `CLAUDE.md` for usage.

## Build

### Prerequisites

```bash
# Install system dependencies (pandoc, texlive, fonts)
chmod +x scripts/setup-deps.sh
./scripts/setup-deps.sh
```

### Building locally

```bash
# Build cover images from SVG sources
python3 scripts/build-cover.py

# Build EPUB
python3 scripts/build-epub.py

# Build both PDF variants (screen + print)
python3 scripts/build-pdf.py

# Build a single variant
python3 scripts/build-pdf.py --variant screen
python3 scripts/build-pdf.py --variant print

# Include git hash and build date
python3 scripts/build-pdf.py \
  --git-hash "$(git rev-parse --short HEAD)" \
  --build-date "$(date +%Y-%m-%d)"
```

Output goes to `output/` (gitignored).

### How the PDF build works

The PDF build assembles all markdown content into a single file with raw LaTeX injections at structural boundaries. The key design decisions:

1. **Title, copyright, and TOC** are handled by the LaTeX template (`build/pdf/template.tex`), not markdown — this gives precise typographic control over the front matter.

2. **Preface** stays in LaTeX `\frontmatter` context (roman page numbers, no chapter numbering).

3. **Part dividers** are detected by filename convention (`00-part-intro.md` in a `*-part-*` directory). The build script extracts the title and injects a `\part{}` command with a `\mainmatter` switch before the first part.

4. **Chapters** are regular markdown files processed as pandoc chapters.

5. **Screen vs print** variants differ in colour profile (RGB vs CMYK), link styling, and whether the cover image is included as page one.

## CI/CD

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `build-book.yml` | Push/PR to `main` | Builds cover, EPUB, and both PDFs. Deploys to Azure Blob Storage on merge. |
| `deploy-site.yml` | Push to `main` (`site/` changes) | Deploys landing page to GitHub Pages |

The build pipeline captures the git short hash and build date, passing them to all build scripts. These are embedded on the copyright page of every output so any copy can be traced back to the exact commit that produced it.

## Progress

- **Front matter** — Title page, copyright, preface
- **Part 1: Foundation** — Chapter 1: The Fifth Generation

## License

This repository uses split licensing:

| Content | License |
|---------|---------|
| Book content, specifications, prose (`.specmcp/specs/`, `content/`) | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) |
| Code, scripts, build tooling (`scripts/`, `build/`, config files) | [MIT](LICENSE-MIT) |

**Book content:** Free to share with attribution. No commercial use or derivatives.

**Code:** Do whatever you want with attribution.
