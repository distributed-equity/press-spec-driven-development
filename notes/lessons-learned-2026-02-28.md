# Lessons Learned — kevinryan.io Refactoring

**Date:** 2026-02-28
**Project:** Kevin Ryan & Associates — kevinryan.io
**Phase:** Brand integration and component architecture

---

## Ease of Specification

During the brand guidelines integration and site refactoring exercise, a key architectural principle emerged: **ease of specification**.

### The Problem

The site's `page.tsx` is a single 597-line monolith containing 11 distinct sections: Hero, Ticker, About, Capabilities, Enterprise Delivery, Clients, Timeline, SpecMCP Showcase, Writing & Projects, Certifications, and Contact. Each section has its own data, layout logic, and presentation concerns — all interleaved in one file.

When specifying changes — whether to Claude, to a collaborator, or to a future version of yourself — you cannot point at a section in isolation. Every instruction requires context about where in the file the change applies, what data drives it, and what else might be affected. A request like "update the capabilities section" requires the reader to mentally parse 600 lines to find the boundaries, understand the data shape, and identify dependencies.

This is the opposite of ease of specification.

### The Principle

**A well-architected codebase is one where changes can be specified with minimal context.**

If you can say "update `CapabilitiesSection.tsx`" instead of "find the capabilities section starting around line 267 in page.tsx, the data is defined starting at line 12, and the styles are in the responsive block at line 584" — you have achieved ease of specification.

This matters more in the age of AI-assisted development than it ever did before. When your development partner is an LLM operating on a context window, the cost of ambiguity is not a confused junior developer who asks a clarifying question — it is a confidently wrong edit that silently breaks something three sections away.

### The Fix

Split `page.tsx` into discrete, self-contained components. Each component:

- Owns its data (or receives it via props with a clear interface)
- Owns its markup
- Can be specified, reviewed, and modified independently
- Has a filename that maps directly to the section it represents

### Current Sections in page.tsx

| # | Section | Lines (approx) | Data |
|---|---|---|---|
| — | Hero | 107–205 | Inline |
| — | Ticker | 207–215 | `TICKER_ITEMS` array |
| 01 | About | 217–265 | Inline text |
| 02 | Capabilities | 268–287 | `CAPABILITIES` array |
| 03 | Enterprise Delivery | 290–311 | `CASES` array |
| 04 | Clients | 314–329 | `CLIENTS` array |
| 05 | Timeline | 332–358 | `TIMELINE` array |
| 06 | SpecMCP Showcase | 362–432 | Inline |
| 07 | Writing & Projects | 435–463 | `WRITING` array |
| 08 | Certifications | 464–522 | `CERTS` array |
| 09 | Contact | 523–583 | Inline |
| — | Responsive styles | 584–597 | CSS-in-JSX |

### Broader Application

This lesson applies directly to the Spec Driven Development thesis. The argument is not just that specifications should drive development — it is that **architecture should be optimised for the act of specifying**. If a system is hard to specify changes to, no amount of specification discipline will save you from drift, ambiguity, and rework.

Ease of specification is a quality attribute of the codebase itself, alongside maintainability, testability, and performance. It should be designed for, not hoped for.

---

**Status:** Principle captured. Component extraction to follow as next step.
