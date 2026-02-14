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
├── assets/                  # Cover artwork and bundled fonts
├── build/epub/              # Pandoc metadata and styles
├── content/                 # Book content (front matter, chapters)
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

- **EPUB** — Primary distribution format
- **Audiobook** — Generated from markdown via ElevenLabs

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

Requires [pandoc](https://pandoc.org/installing.html) for EPUB generation.

```bash
# Install pandoc (Ubuntu/Debian)
sudo apt-get install pandoc

# macOS
brew install pandoc

# Build the EPUB
python scripts/build-epub.py
```

Output: `output/spec-driven-development.epub` (gitignored)

## CI/CD

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `build-book.yml` | Push/PR to `main` | Builds cover and EPUB, deploys to Azure on merge |
| `deploy-site.yml` | Push to `main` (`site/` changes) | Deploys landing page to GitHub Pages |

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
