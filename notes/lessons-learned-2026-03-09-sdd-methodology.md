# Lessons Learned — 2026-03-09

## Session: Defining Spec Driven Development — The Provenance Method

**Date:** 9 March 2026
**Context:** Extended working session with Claude (Opus 4.6) developing the SDD methodology, templates, slide deck, and session brief. Started with a question about scenario-based testing with agentic AI and ended with a complete methodology definition, three templates, a 22-slide presentation, and a session brief page.
**Purpose:** Research content for *Spec Driven Development: AI-Native Software Engineering* (sddbook.com)

---

## 1. The Core Distinction: Testing Software, Not Testing Agents

The entire industry conversation around agentic AI testing is focused on evaluating the agent — does it reason well, pick the right tools, stay aligned? LLM-as-judge, Agent-as-a-judge, Bloom, eval-driven development. Billions of research dollars.

SDD asks a different question: **how does my agent test what it builds?** The output is deterministic software. It either handles the edge case or it doesn't. The API either returns the right status code or it doesn't. You're back in the world of testable artefacts.

This is a fundamental reframing that nobody else is articulating. Anthropic talks about eval-driven development but from the testing side. SDD argues it from the specification side, which inverts the whole thing.

**Book implication:** This distinction should be established early — possibly in the introduction or chapter one. It sets up everything that follows.

---

## 2. The Spec-Scenario-Test Collapse

In traditional development, three separate artefacts exist: the specification (what we want), the implementation (what we built), and the tests (did we build what we wanted). They're written independently, often by different people, and they drift.

With agentic AI, the spec you hand the agent *is* the implementation instruction. The agent reads the spec and builds the software. If the spec is structured well enough, it also defines the test scenarios — not as a side effect, but inherently.

**The insight:** A well-structured specification contains the scenario, the acceptance criteria, and the evaluation rubric. This isn't a nice-to-have — it's a necessary consequence of how agentic development works. You go from three artefacts to one. The spec is the scenario is the test definition. The only additional thing you need is the evaluation mechanism.

**Constraint:** This only works if the spec is written in a way that's evaluable. Vague specs produce vague scenarios produce unjudgeable outcomes. The quality of the spec isn't just about making it easy for the agent to do the work — it's about making it possible to verify the work was done right.

**Book implication:** This is potentially a central argument — the spec-scenario-test collapse as an architectural principle of AI-native development.

---

## 3. The Builder-Tester Separation

The same agent cannot build the software and verify it, for the same reason a developer shouldn't be the sole reviewer of their own code. If the builder misunderstood the spec, it will write code that reflects the misunderstanding *and* tests that confirm the misunderstanding. Everything passes. Everything's wrong.

**The architecture:**

- **Builder agent** reads the spec, writes code, produces provenance (assumptions, ambiguities, decisions). Does not write tests.
- **Testing agent** reads the spec and the provenance, finds the daylight between them, writes prose scenarios, then implements executable tests. Updates the provenance with findings.
- **They never communicate directly.** They communicate through the provenance document, with the spec as the authority both defer to.

This is agent coordination through documentation rather than orchestration. No supervisor agent. No LangGraph. No message bus. The workflow emerges from the documents.

**Book implication:** This is the process chapter. The separation of concerns is the architectural principle; the provenance document is the mechanism that makes it work.

---

## 4. Provenance as the Core Innovation

This is the idea that doesn't exist anywhere else.

**What provenance is:** A layered document where agents record their reasoning as they work. The builder writes what it did and why — every assumption, every ambiguity, every decision. The tester appends what it found — gaps, challenges to assumptions, ambiguity assessments, silences. Neither modifies the other's sections.

**What provenance is NOT:** A map of the codebase. Code is self-describing — any agent can read it and understand *what* exists. Provenance answers the questions code can't answer about itself: *why* is it this way? Why is the timeout 30 minutes? Why this library and not that one? Why does this module exist at all?

**The key distinction:**
- **Code = the what.** Self-describing canonical context. The reality of the system.
- **Provenance = the why.** The reasoning record. Decisions, assumptions, the questions the code can't answer about itself.

An agent entering a codebase does two things: reads the code to understand what exists, reads the provenance to understand why it exists. One gives you the territory. The other gives you the decisions that shaped the territory.

**Provenance as communication protocol:** The builder writes to it. The tester reads from it and writes to it. The builder reads back and acts on it. The provenance is the interface between agents. The spec is the authority they both defer to.

**Provenance as institutional memory:** Code and tests are regenerated every cycle. Provenance is what persists and grows. It accumulates understanding about the software across agents and across time.

**Book implication:** This is the chapter that makes the book matter. The provenance concept, its properties, its role in the SDD loop, and its implications for compliance and audit.

---

## 5. Prose Scenarios Before Test Code

The testing agent writes a markdown scenario — plain language explaining what's being tested and why — before it writes a single line of test code. The code is derived from the prose, not the other way around.

**Why this matters:**
- A product owner can read the scenario.
- A regulator can read it.
- A client who knows nothing about code can say "yes, that's the right question to ask" or "actually, don't test for that — update the spec."
- If the prose scenario is wrong or irrelevant, you catch it before anyone writes a test.
- If the code doesn't match the prose, that's itself a verifiable problem.

**The provenance chain:** Why does this test exist? Because of this scenario. Why does this scenario exist? Because the provenance revealed this assumption against this part of the spec. Complete lineage from business intent to running test.

**Book implication:** This is a subsection of the testing chapter but deserves emphasis — it's what makes SDD auditable by non-technical stakeholders.

---

## 6. The Spec Defines Everything

The spec in SDD is not just a requirements document. It defines:

- **The product:** Requirements, architecture, interfaces, constraints, assumptions.
- **The process:** What happens, in what order, where artefacts are stored.
- **The roles:** Builder and tester role definitions, what each reads, what each produces, where each writes.

At prompt time, you say: "You are the builder. Here is the spec. Do your job." The agent reads its role definition from the same document that describes the software. **The spec is the orchestrator.**

This means the roles are auditable and changeable. Want to add a security review step? Add a role to the spec. Want to change what the tester is responsible for? Edit the spec. The workflow *is* the spec.

**Book implication:** This is a design principle that should be stated explicitly — the spec specifies everything, including the process that produces the product.

---

## 7. Failing Tests as Work Orders

A failing test without context is a stack trace. A failing test with provenance is a diagnosis.

The builder doesn't get "line 47 assertion failed." It gets: the prose scenario explaining why this test exists, the specific gap between spec and provenance that generated it, and the testing agent's recommendation for what to fix.

The fix cycle: fail → builder reads updated provenance → fixes code → updates provenance → tester re-runs → pass or new cycle.

No human touched the code. No human wrote a test. No human triaged a bug. A human wrote a spec. Everything else is derived.

**Book implication:** This is the loop chapter — how the infinity loop actually operates in practice.

---

## 8. Five Artefacts, Five Purposes

| Artefact | Purpose | Audience |
|----------|---------|----------|
| **Spec** | Intent — what should exist and why | Stakeholders |
| **Code** | Reality — self-describing canonical context | Agents, developers |
| **Provenance** | Reasoning — why the code is the way it is | Technical reviewers, auditors |
| **Scenarios** | Challenge — what's being verified and why | Anyone |
| **Tests** | Execution — derived from scenarios, pass or fail | Machines |

Code and tests are outputs (white borders in the deck). Spec, provenance, and scenarios are the document chain (lime borders).

**Book implication:** This taxonomy should be a reference table early in the book and referenced throughout.

---

## 9. The Compliance Angle

SDD's provenance chain maps directly to regulatory and audit requirements:

**SOC 2** — Change management controls require evidence that changes are authorised, documented, and traceable. The provenance chain is that evidence.

**ISO 27001** — Annex A requires documented development procedures, separation of duties, and design review records. SDD's builder-tester separation and layered provenance satisfy this structurally.

**EU AI Act (full force August 2026):**
- **Article 11** — Technical documentation: comprehensive records of design decisions, kept updated.
- **Article 12** — Record-keeping: systems must automatically record events so actions can be traced back.
- **Article 19** — Automatically generated logs: retained for six months minimum.

**The key argument:** The Act was written assuming humans build software. When a human makes a decision, the reasoning exists in their head, in Slack threads, in PR comments. When an agent builds software, the reasoning exists in the context window — and evaporates when the session ends. Unless you capture it. Provenance captures it.

**Nuance:** The EU AI Act applies directly when the software being built is itself an AI system (high-risk classification). When the output software is not an AI system, the Act doesn't formally apply to it just because an AI wrote it. But the documentation and traceability discipline is increasingly expected across SOC 2, ISO 27001, and regulated procurement regardless.

**The line:** "You cannot retrospectively create provenance for decisions that were never documented. SDD means you never have to."

**Book implication:** This is a dedicated chapter — possibly the chapter that sells the book to enterprise buyers. Compliance as a byproduct, not a project.

---

## 10. What SDD Does Not Give You

SDD is deliberately simple. There are real problems it doesn't address:

- **Multi-agent orchestration** — SDD uses two roles talking through documents. LangGraph, CrewAI, AutoGen solve the dynamic coordination problem.
- **Real-time agent monitoring** — SDD tests the software, not the agent. Arize, Braintrust, Bloom solve production agent monitoring.
- **Dynamic tool discovery** — SDD specs are static documents. MCP servers and tool registries handle runtime tool composition.
- **Long-term agent memory** — SDD uses provenance as persistent context but doesn't provide vector stores, RAG, or cross-session memory.

**The framing:** "These technologies solve real problems. But they solve advanced problems. SDD sharpens the thinking that makes every other tool more effective. Start with the spec. Graduate to complexity when the problem demands it."

**Book implication:** A chapter or section that positions SDD in the landscape — honest about scope, not defensive about limitations.

---

## 11. Industry State of Practice (as of March 2026)

Research conducted during this session on who's doing what:

- **Anthropic** recommends "eval-driven development" — building evals before agents can fulfil them. Close to the spec-as-scenario insight but framed from the testing side. Key finding: checking agents followed specific steps was too rigid; outcome-oriented evaluation is best practice.
- **Meta** built Just-in-Time Tests — generated on the fly by LLMs for each code change, not stored in the codebase. Interesting because it dissolves the test artefact entirely, but tests are generated from code, not from a specification of intent.
- **Anthropic's Bloom** takes a single behaviour specification and generates a targeted evaluation suite. Literally a spec generating scenarios — but designed for safety alignment, not product development.
- **Tessl** observed that Anthropic's SKILL.md files are heading toward a future where a description of what a skill should accomplish is the skill itself. "Evals already describe the 'what.' Eventually, that description may be the skill itself." Almost exactly the spec-scenario-test collapse, stated as a future direction.
- **LLM-as-judge** is mature and accelerating, with researchers framing "Evaluation-driven Development" as an ongoing part of the pipeline. But evaluation criteria are written separately from specifications.

**The gap SDD fills:** Nobody is articulating the full loop — that a well-structured specification inherently contains the scenario, the acceptance criteria, and the evaluation rubric, and that provenance is the mechanism that makes this traceable.

**Book implication:** Literature review / state of practice chapter. Position SDD as filling a specific gap that the industry is circling but hasn't landed on.

---

## 12. The Maturity Model Connection

SDD is positioned as the practical method to move from L0–2 (spicy autocomplete, coding intern, junior developer) to L3–4 (developer as manager, developer as product owner) on Dan Shapiro's Five Levels of Vibe Coding.

Level 5 (dark factory) is a different problem set — fully autonomous, digital twins, thousand-dollar daily compute budgets. SDD doesn't claim to get you there. But it gets you off the bottom rung today, with tools you already have.

**Book implication:** The maturity model frames the "who is this for" question. SDD is for the 90% stuck at L0–2 who know there's a higher level but don't have a method.

---

## 13. Presentation Structure

The SDD presentation (22 slides) was developed as a companion to the Dark Factory deck:

- **Dark Factory** = the strategy (for CTOs and engineering leaders)
- **SDD** = the execution (for engineers and tech leads)

The Dark Factory asks "what's happening and where do you sit?" SDD answers "OK, how do I actually do this?"

**Slide arc:**
1. Title
2. What is SDD (sets expectations, intellectual honesty)
3. Maturity model (the problem)
4. SDD gets you to L3–4 (the opportunity)
5. It's all about the spec (the insight)
6. The infinity loop (architecture)
7. The spec contents
8. Builder agent
9. Testing agent
10. Provenance (reasoning record, not a map)
11. The cross-examination (what the tester targets)
12. Prose first, code second
13. The loop (failing tests as work orders)
14. The provenance chain (five artefacts)
15. Why it's different (markdown and a process)
16. The value (six cards)
17. What SDD does not give you
18. Live demo
19. Close
20–22. Bonus: compliance (SOC 2, ISO 27001, EU AI Act)

**Book implication:** The slide structure maps almost directly to a book outline.

---

## 14. Templates Produced

Three markdown templates were created during this session:

### Spec Template (`sdd-spec-template.md`)
- Agent Roles section at the top (builder and tester with full instructions for first and subsequent cycles)
- Task, Prerequisites, Context, Implementation sections
- Constraints and Assumptions section (testing agent targets these)
- Out of Scope section (prevents agents from over-building)
- Provenance and Validation sections

### Provenance Template (`sdd-provenance-template.md`)
- Two-layer document: Builder Agent Record and Testing Agent Record
- Builder layer: actions, decisions, assumptions (table with spec reference and rationale), ambiguities (table with interpretation and alternative reading), deviations, artefacts, build status, validation results
- Tester layer: findings (gaps, assumption challenges, ambiguity assessments, silences), scenario results, recommendations (each naming who should act: builder, human, or spec author)

### Scenario Template (`sdd-scenario-template.md`)
- Summary with counts by trigger type (gaps, assumptions, ambiguities, silences, requirements)
- Each scenario: triggered by, spec reference, provenance reference, context (plain language), expects, fails if, test implementation reference
- "Scenarios Not Generated" section for audit — shows coverage reasoning

### Directory structure:
```
.sdd/
  specification/   ← specs (canonical, immutable once saved)
  provenance/      ← provenance (layered, both agents write)
  scenarios/       ← prose scenarios (testing agent writes)
tests/             ← executable test code (testing agent writes)
```

**Book implication:** These templates are appendix material and potentially downloadable resources from sddbook.com.

---

## 15. Key Quotes and Lines

Lines that emerged during the session worth preserving:

- "The spec is the single source of truth for what the software does, how it gets built, and how it gets verified."
- "Provenance is the communication protocol between agents."
- "The builder shows its working. The tester cross-examines the working. They never talk to each other."
- "Prose first. Code second."
- "Failing tests are work orders, not bug reports."
- "Code is the what. Provenance is the why."
- "The spec is the orchestrator."
- "Compliance as a byproduct. Not a project."
- "You cannot retrospectively create provenance for decisions that were never documented."
- "Your auditor's AI is going to ask how this was built."
- "Start with the spec. Graduate to complexity when the problem demands it."
- "The spec specifies everything."

---

## 16. What Comes Next

- [ ] Polish the three templates and commit to the kevin-ryan-platform repo under `.sdd/`
- [ ] Deploy the slide deck to a URL (alongside the Dark Factory deck)
- [ ] Deploy the session brief page
- [ ] Write the SDD book chapter on provenance — this is the chapter that makes the book unique
- [ ] Build the live demo: a real spec → builder → provenance → tester → scenarios → tests flow, executable in front of an audience
- [ ] Reach out to Fredrik Hagstroem at Emergn — SDD maps directly to their "Closing the AI Execution Gap" positioning
- [ ] Consider a LinkedIn post on the provenance concept — test the idea in public before the book chapter ships
- [ ] Update sddbook.com with the methodology overview

---

*Session duration: ~4 hours. Output: methodology definition, 3 templates, 22-slide deck, session brief page, this lessons learned document.*
