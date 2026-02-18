# Author's Note

Specification for the Author's Note front matter page.

## Purpose

Provide a short, direct note to the reader establishing that the book is in
early beta, inviting participation, and setting expectations. This page appears
before the table of contents so every reader encounters it.

## Placement

File: `content/00-front-matter/05-authors-note.md`

Position: After epigraph (04), before TOC (06). Unnumbered — uses
`{.unnumbered}` Pandoc attribute. No page number in the rendered output.

This page is temporary. It should be removed or replaced when the book
reaches a stable release.

## Content Requirements

The Author's Note must contain the following elements in order:

### 1. Beta status

State clearly that this is an early beta. Content will change frequently.
Set the reader's expectations — they are reading a living document.

### 2. How this book is built

A single sentence noting that this book is written using the methodology it
describes. Do not explain SDD or the CI/CD pipeline in detail — the colophon
(back matter) is the place for that. The purpose here is to plant the meta
hook, not teach the methodology.

### 3. Call for involvement

The author is interested in:

- Case studies and real-world lessons learned
- Shared experiences practising specification-driven development
- Technical review and feedback on the book's content

### 4. How to contribute

Collaboration happens on GitHub — contributing to this book works the same way
as contributing to any open source project.

Provide:

- Email: kevin@kevinryan.io
- Website: kevinryan.io
- GitHub repository link

### 5. Contributor recognition

Anyone who contributes direct effort to this book will be credited as a
contributor.

## Tone

Direct, warm, brief. This is a personal note, not a marketing page. Write in
first person. Keep it to a single page in the rendered PDF — no more than
250 words.

## LaTeX Template Considerations

Because this page is unnumbered and appears before the TOC, it must be handled
in `build/pdf/template.tex` the same way as the copyright page — rendered from
the template, not from the markdown source. The build script should skip this
file during content assembly (like it skips title-page and copyright).

If the file does not exist, the template should silently omit the page. This
supports clean removal when the book exits beta.

## Implementation Notes

- Adding this page requires renumbering existing front matter files from
  `05-toc.md` onward (05 → 06, 06 → 07, etc. through to 09 → 10).
- The workflow spec's repo structure, front matter table, and file naming
  examples must be updated to reflect the new numbering.
- The build scripts (`build-epub.py`, `build-pdf.py`) must be checked to
  confirm they handle the new file correctly — either skipping it (if rendered
  from the template) or including it in assembly order.
