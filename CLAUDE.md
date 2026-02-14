# SDD Book Repository

This repository uses Specification Driven Development to author a book about SDD.

## MCP Server

This repo includes a local MCP server (`.specmcp/server.py`) that provides
structured access to book specifications. Use these tools:

- **list_specs** — Discover available specifications
- **get_spec** — Read a specific specification by name
- **get_chapter_context** — Get bundled context for writing a chapter
- **validate_content** — Check content against spec rules

## Key Specifications

Start with `list_specs` to see all available specs. The most important are:

- **book-brief** — Scope, thesis, audience
- **writers-guide** — Voice, tone, style rules (read this before writing any content)
- **glossary** — Canonical term definitions (use terms exactly as defined)
- **chapter-outline** — 26 chapters across 5 parts

## Writing Workflow

When writing a chapter:

1. Call `get_chapter_context` with the chapter number
2. Follow the writers guide strictly
3. Use glossary terms exactly as defined
4. After writing, call `validate_content` to check for issues

## Code Quality

Python code uses ruff (linting + formatting) and mypy (type checking).
Run `pre-commit run --all-files` before committing.
