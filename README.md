<!-- GENERATED FILE — DO NOT HAND-EDIT -->
<!-- Source: .specmcp/specs/devops/readme-update.md -->
<!-- Re-generate by executing the readme-update spec -->

> **Generated file** — do not edit directly. This README is produced by
> the [`readme-update`](.specmcp/specs/devops/readme-update.md) spec.
> To change it, update the spec and re-execute.

# Specification Driven Development: The Book

A practical guide to Specification Driven Development (SDD) for
professional developers working with AI coding agents.

**Website:** [sddbook.com](https://sddbook.com)

This repository contains the specifications, content, and build pipeline
for a book about Specification Driven Development — a methodology where
specifications become the primary artifact and code becomes a generated
side effect.

## Core Thesis

> The specification is the artifact. Code is a side effect.

## This Repository Proves the Methodology

This repository is itself specification-driven. The book about SDD is
written using SDD. Specifications in `.specmcp/specs/` drive content
generation, MCP servers provide structured access to project resources,
and even this README is a generated artifact produced by executing a
spec.

Every workflow in this repository follows the SDD two-loop process
described below. The provenance system records what happened during each
spec execution, creating an audit trail that complements the git history.

If you want to understand what Specification Driven Development looks
like in practice, explore this repository.

## The SDD Workflow

The SDD workflow has eight steps across two loops. The spec loop is
where the creative work happens. The execution loop is mechanical.

### The Spec Loop

1. **Brief** — Capture intent as bullet points or a problem statement.
   The brief is the spec for the spec — fast, loose, and incomplete by
   design.
2. **Spec draft** — An agent expands the brief into a full
   specification. The agent asks clarifying questions if the brief has
   gaps.
3. **Iterate spec** — The human reviews the draft. This is where the
   real intellectual work happens: missing requirements, implicit
   assumptions, verification gaps, scope creep.
4. **Commit spec to main** — The spec is the artifact. Committing it
   marks it as approved and ready for execution.

### The Execution Loop

5. **Plan** — An agent reads the committed spec and produces an
   execution plan in plan mode only — no files created, no changes made.
6. **Validate plan against spec** — Does the plan reveal deficiencies
   in the spec? If yes, fix the spec and discard the plan. If no,
   approve.
7. **Execute** — The agent executes the approved plan. The prompt
   should be minimal — if it needs to explain the work, the spec is
   deficient.
8. **Validate results** — Run every verification check listed in the
   spec. Every check is mandatory.

**Key principle:** The spec loop is where you spend your cognitive
budget. The execution loop should be boring. If execution is surprising,
the spec has holes.

For the full workflow reference, see [`AGENTS.md`](AGENTS.md).

## MCP Servers

This repository includes local MCP servers that provide AI agents with
structured access to project resources. All servers are registered in
[`.mcp.json`](.mcp.json).

### Spec Server (`.specmcp/server.py`)

Structured access to book specifications, provenance records, chapter
context, and content validation.

- **list_specs** — List available specifications, optionally filtered by category
- **get_spec** — Get the full content of a specification by name
- **list_provenance** — List all provenance records across specs
- **get_provenance** — Get the provenance (execution history) for a specific spec
- **get_chapter_context** — Get bundled specification context for writing a chapter
- **validate_content** — Validate content against SDD book specifications

### Skills Server (`.skillmcp/server.py`)

Reusable skills that guide agent workflows.

- **list_skills** — List available skills, optionally filtered by category
- **get_skill** — Get the full content of a skill by name

### Brand Server (`.brandmcp/server.py`)

Brand guidelines, design tokens, and brand validation.

- **list_brand** — List available brand guideline documents
- **get_brand** — Get the full content of a brand guideline by name
- **get_design_tokens** — Read and return the design tokens from tokens.json
- **validate_brand** — Validate content against the brand guidelines

## Specifications

| Spec | Category | Purpose |
|------|----------|---------|
| [`brandmcp-build`](.specmcp/specs/devops/brandmcp-build.md) | devops | Spec: brandmcp Build — Brand Guidelines Server |
| [`readme-update`](.specmcp/specs/devops/readme-update.md) | devops | Spec: readme-update — Generated README from Repository State |
| [`skillmcp-refactor`](.specmcp/specs/devops/skillmcp-refactor.md) | devops | Spec: skillmcp Refactor — Skill Convention Alignment |
| [`specmcp-refactor`](.specmcp/specs/devops/specmcp-refactor.md) | devops | Spec: specmcp Refactor — Provenance Separation |
| [`authors-note`](.specmcp/specs/editorial/authors-note.md) | editorial | Author's Note |
| [`book-brief`](.specmcp/specs/editorial/book-brief.md) | editorial | Book Brief: Specification Driven Development |
| [`chapter-outline`](.specmcp/specs/editorial/chapter-outline.md) | editorial | Chapter Outline: Specification Driven Development |
| [`continuity-tracker`](.specmcp/specs/editorial/continuity-tracker.md) | editorial | Continuity Tracker |
| [`diataxis-integration`](.specmcp/specs/editorial/diataxis-integration.md) | editorial | Diátaxis Framework Integration |
| [`glossary`](.specmcp/specs/editorial/glossary.md) | editorial | Glossary: SDD Terminology |
| [`licensing`](.specmcp/specs/editorial/licensing.md) | editorial | Licensing |
| [`prior-art`](.specmcp/specs/editorial/prior-art.md) | editorial | Prior Art: Related Concepts and How SDD Relates |
| [`writers-guide`](.specmcp/specs/editorial/writers-guide.md) | editorial | Writer's Guide for Specification Driven Development |
| [`author-spec-skill`](.specmcp/specs/methodology/author-spec-skill.md) | methodology | Spec: author-spec Skill — How to Write Specifications |
| [`provenance`](.specmcp/specs/workflow/provenance.md) | workflow | Provenance |
| [`workflow`](.specmcp/specs/workflow/workflow.md) | workflow | SDD Workflow: Authoring This Book |

## Skills

| Skill | Description |
|-------|-------------|
| [`author-spec`](.skillmcp/skills/author-spec/author-spec.md) | Write effective specifications for SDD workflows |
| [`mcp-builder`](.skillmcp/skills/mcp-builder/mcp-builder.md) | Build, refactor, and maintain MCP servers for the SDD book repository |

## Target Audience

Professional developers (3+ years experience) who:

- Use AI coding tools but find ad-hoc prompting frustrating
- Want systematic methods, not hacks
- Value engineering discipline over "vibe coding"

## Outputs

The build pipeline produces three book formats from the same markdown
source:

| Format | File | Purpose |
|--------|------|---------|
| **EPUB** | `spec-driven-development.epub` | E-readers and digital distribution |
| **Screen PDF** | `spec-driven-development.pdf` | Digital download with cover, RGB colours, clickable links |
| **Print PDF** | `spec-driven-development-print.pdf` | Print-ready interior (no cover, CMYK-safe, black links) |

All outputs are deployed to Azure Blob Storage on merge to `main`.
Each build embeds the short git hash and build date on the copyright
page for traceability.

## Repository Structure

```
.
├── .brandmcp/                          # Brand guidelines MCP server
│   ├── brand/                          # Brand design tokens and content
│   ├── requirements.txt
│   └── server.py
├── .devcontainer/                      # Development container configuration
│   └── devcontainer.json
├── .github/                            # GitHub configuration
│   └── workflows/
│       ├── build-book.yml
│       └── deploy-site.yml
├── .skillmcp/                          # Skills MCP server
│   ├── requirements.txt
│   ├── server.py
│   └── skills/
│       ├── author-spec/
│       └── mcp-builder/
├── .specmcp/                           # Specifications MCP server
│   ├── requirements.txt
│   ├── server.py
│   └── specs/
│       ├── devops/                     # Infrastructure and tooling specs
│       ├── editorial/                  # Content and style specs
│       ├── methodology/                # SDD methodology specs
│       ├── provenance/                 # Execution audit trail
│       └── workflow/                   # Authoring workflow specs
├── assets/
│   ├── cover/                          # Cover artwork (SVG sources)
│   │   ├── back-cover.svg
│   │   ├── front-cover.svg
│   │   └── spine.svg
│   └── fonts/                          # Bundled fonts for reproducible builds
├── build/
│   ├── epub/                           # EPUB metadata and styles
│   │   └── metadata.yaml
│   └── pdf/                            # LaTeX template for PDF generation
│       └── template.tex
├── content/                            # Book manuscript
│   ├── 00-front-matter/                # Title, copyright, preface
│   └── 01-part-1-foundation/           # Part 1 chapters
├── infra/                              # Azure Bicep infrastructure-as-code
│   ├── main.bicep
│   └── main.bicepparam.json
├── notes/                              # Research and lessons learned
│   ├── 2026-02-19-lessons-learned.md
│   ├── example-spec-brief-prompt.txt
│   └── links.md
├── scripts/                            # Build, deploy, and setup scripts
│   ├── build-cover.py
│   ├── build-epub.py
│   ├── build-pdf.py
│   ├── deploy-content.py
│   ├── deploy-infra.sh
│   ├── install-az-cli.sh
│   └── setup-deps.sh
├── site/                               # Landing page (GitHub Pages)
│   ├── CNAME
│   ├── index.html
│   └── sdd-book-mockup.png
├── .gitignore
├── .markdownlint.yaml
├── .mcp.json                           # MCP server registry
├── .pre-commit-config.yaml
├── AGENTS.md                           # Agent workflow conventions
├── CLAUDE.md
├── LICENSE-CC-BY-NC-ND
├── LICENSE-MIT
├── README.md                           # This file (generated)
├── requirements.txt
└── ruff.toml
```

## Provenance

Every spec execution leaves a trace. Provenance files record what was
done, why, and how — creating an audit trail that complements the git
history.

Provenance files are stored at
`.specmcp/specs/provenance/<category>/<spec-name>.provenance.md` and
are overwritten on each execution (git provides the history). See the
[provenance spec](.specmcp/specs/workflow/provenance.md) for the full
convention.

**Current provenance records:** 7 (discovered via `list_provenance`)

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

### PDF Typography

PDFs are typeset with XeLaTeX at 6 x 9 inch trim size using Google
Fonts:

- **Source Serif 4** — Body text (designed for long-form reading)
- **Alfa Slab One** — Part and chapter titles
- **Inter** — Section headings
- **JetBrains Mono** — Code blocks

All fonts are committed to `assets/fonts/` for reproducible builds.

## CI/CD

| Workflow | Trigger | What it does |
|----------|---------|--------------|
| `build-book.yml` | Push/PR to `main` | Builds cover, EPUB, and both PDFs. Deploys to Azure Blob Storage on merge. |
| `deploy-site.yml` | Push to `main` (`site/` changes) | Deploys landing page to GitHub Pages |

The build pipeline captures the git short hash and build date, passing
them to all build scripts. These are embedded on the copyright page of
every output so any copy can be traced back to the exact commit that
produced it.

## Development

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Install MCP server dependencies
pip install -r .specmcp/requirements.txt

# Run linting manually
pre-commit run --all-files
```

For agent workflow and project conventions, see
[`AGENTS.md`](AGENTS.md).

## Licence

This repository uses split licensing:

| Content | Licence |
|---------|---------|
| Book content, specifications, prose (`.specmcp/specs/`, `content/`) | [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) |
| Code, scripts, build tooling (`scripts/`, `build/`, config files) | [MIT](LICENSE-MIT) |

**Book content:** Free to share with attribution. No commercial use or
derivatives.

**Code:** Do whatever you want with attribution.
