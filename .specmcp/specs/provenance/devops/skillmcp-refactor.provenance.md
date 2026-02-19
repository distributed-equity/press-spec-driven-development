# Provenance: skillmcp-refactor

## 2026-02-19 — Align skillmcp server with mcp-builder skill conventions

**Prompt:** Execute spec skillmcp-refactor

**Branch:** claude/skillmcp-refactor-P9jDM
**Commit(s):** (included in this commit)

### Actions taken

1. Read the skillmcp-refactor spec, provenance convention, and mcp-builder skill.
2. Read `.skillmcp/server.py` and performed line-by-line audit against every
   convention in the mcp-builder skill (`SKILL.md`).
3. Compared against `.specmcp/server.py` as the reference implementation that
   already passed its own convention-alignment refactor.
4. Found two deviations — both related to missing `.provenance.md` file filtering
   (future-proofing). All other conventions already matched.
5. Added `if md_file.stem.endswith(".provenance"): continue` to `discover_skills()`
   to skip provenance files during discovery.
6. Added `if md_file.stem.endswith(".provenance"): continue` to `load_skill()`
   to prevent loading provenance files as skills.
7. Verified `requirements.txt` contains `mcp>=1.2.0` — satisfies the minimum
   `mcp` dependency requirement.
8. Verified `.mcp.json` contains the `sdd-book-skills` entry with stdio transport
   pointing to `.skillmcp/server.py`.
9. Verified tool names match the expected `list_skills` and `get_skill`.
10. Ran `ruff check`, `ruff format --check`, and `pre-commit run --all-files`.
11. Created this provenance file.

### Decisions

- **No provenance tools added.** The spec explicitly lists "Adding new tools beyond
  `list_skills` and `get_skill`" as out of scope. The provenance filtering is
  future-proofing only — if provenance files are later added under `skills/`, they
  will be correctly excluded from skill discovery.
- **Kept `SkillInfo` name unchanged.** The mcp-builder skill template uses
  `ResourceInfo` as a generic placeholder; `SkillInfo` is the domain-specific
  equivalent, consistent with `SpecInfo` in the specmcp server.

### MCP calls

1. `get_spec("skillmcp-refactor")`
2. `get_spec("provenance")`
3. `get_skill("SKILL")` (mcp-builder skill)

### Deviations

- **Branch name:** Used `claude/skillmcp-refactor-P9jDM` instead of the
  spec-mandated `spec/skillmcp-refactor/convention-alignment`. The `claude/`
  prefix is a system-enforced requirement for push access in this environment.
