# The five stages, in full

Loaded on demand by the [`startup-idea-engine`](../SKILL.md) skill. Each stage
also has a sub-skill that carries its detail; this is the spine that sequences
them.

## Procedure

### Phase 0 - Setup (always runs)

1. **Mode selection** - if not specified, use `AskUserQuestion` with one question and three options (AUTOPILOT / COLLABORATE / STEP-BY-STEP). Declare the chosen mode in the session header.

2. **Output destination** - if not specified, use `AskUserQuestion` to ask where Raw Idea docs and the session summary should be written. Default options to offer:
   - The active retreat's Raw Ideas folder (e.g., `the workspace Company Files/Product/Design/Brainstorm/Exercises/{retreat-slug}/the operator/Raw Ideas/`)
   - The user's personal inbox (`the operator Personal Workspace/Inbox/Active/`)
   - A custom path the user specifies

   The skill writes ALL outputs (Raw Idea docs, session summary, optional Heretical Theses Pool update) under this destination unless the user specifies otherwise.

3. **Optional scope hint** - if the user has provided a problem-space hint (e.g., "ideas in the agentic-ops space," "ideas using the existing topology," "blank slate"), capture it. If not, default to "blank slate, generate from leading edges."

4. **Optional candidate count** - default 3–5 surviving candidates. The user can override.

5. **Optional Heretical Theses Pool update** - if the destination is the active retreat folder, ask whether surviving candidates should also be added as new theses to `02 Heretical Theses Pool.md`. Default yes.

6. **Session document** - create the session output doc immediately at `{destination}/{YYYY-MM-DD}-startup-idea-engine-session.md` with frontmatter (date, mode, scope hint, output destination). Update this doc at the end of each phase. This is the running journal of the session.

### Phase 1 - Context Build (always runs, parallel)

Launch **4 `Explore` sub-agents in parallel** in a single message. Each agent brief is self-contained (the sub-agent has no conversation history) and asks for ≤400-word reports.

**Agent 1 - Founder shape & principles.** Read the canonical operating frame for the user's company / project (e.g., `the workspace Company Files/Product/Design/Brainstorm/Exercises/{retreat}/the operator/01 the operator's Cabin Operating Frame.md`), the principles file (e.g., `Retreat Raw Notes` Deriving Principles section, or `the workspace Company Files/Business Dev/Core/Philosophies/`), and the team / role index (`the workspace Company Files/Operations/Team/00-team-index.md`). Report: the principles each candidate must survive, the founder shape constraints (revenue ambition, capital strategy, family-rooted team, etc.), and any explicit foreclosures (e.g., "no VC," "no acquisition by the incumbent vendor").

**Agent 2 - Topology & competence.** Read the architecture / RFC docs (e.g., `RFC-001a - Walking Skeleton.md`), the GTM plan, and any product-philosophy docs. Report: the platform primitives the user holds, the technical competencies, and what the topology can and cannot become without rewrite. Also identify the operator's "leading edge positions" (e.g., AI-augmented dev, agentic-web substrate thinking, the incumbent vendor API depth).

**Agent 3 - Prior candidate inventory.** Read all existing Raw Idea docs and the Heretical Theses Pool in the retreat folder (or the user-specified prior-ideas location). Report: every candidate already documented, its current status (active / parked / killed), and any cross-references between candidates. Goal: prevent the skill from re-generating ideas already explored.

**Agent 4 - Recent reality.** Read the latest weekly review and weekly plan, the most recent customer-call notes, and the last 7 days of daily notes. Report: the painful reality the user is operating against right now (failed sales motion, lost customers, broken assumptions, recently-validated buyer signals), and any specific named buyers / contacts who are real conduits for buyer-conversation validation.

After agents return, the skill reads only the *critical* files each agent flagged (not all of them), and synthesizes a single context summary into the session document under "Context."

### Phase 2 - Noticing (Generation)

Load `sub-skills/01-noticing.md` and follow it in full. The sub-skill applies Paul Graham's six generation procedures (start with own needs / live in the future / cross domains / single-user consultant / schlep-heavy / waves) to produce candidates.

**Mode behavior:**
- AUTOPILOT: run all six procedures, generate up to 8 raw candidates, advance to Phase 3.
- COLLABORATE: run all six procedures, present candidates, pause for user to indicate which to advance.
- STEP-BY-STEP: present each procedure result individually, pause for user reaction, refine before moving on.

### Phase 3 - Framework Tests

Load `sub-skills/02-framework-tests.md`. For each candidate from Phase 2, apply:
- PG's three-pillar test (founders want / build / few realize)
- Demand-shape test (Well not Broad)
- Founder-market-fit test (lineage-shape filter)
- Schlep-disabled test
- Wave-alignment test
- Tarpit check (against `references/dalton-michael-tarpits.md` and the operator's Q1 history)

Each test outputs PASS / PARTIAL / FAIL per candidate. Candidates with multiple FAILs are killed in this phase, not after Phase 4 research.

**Mode behavior:**
- AUTOPILOT: run tests, kill failures, advance with survivors.
- COLLABORATE: present test results, pause for user to override kill decisions.
- STEP-BY-STEP: walk through each candidate's tests one at a time.

### Phase 4 - Research Validation

Load `sub-skills/03-research-validation.md`. For each candidate that survived Phase 3, run targeted research designed to **kill, not justify**: documented pain evidence, incumbent landscape and reviews, buyer-process signal, wave-timing check, and tarpit-history check.

Update the test results from Phase 3 with research findings. Candidates whose tests degrade from PASS to FAIL after research are killed.

**Mode behavior:**
- AUTOPILOT: run research, update results, advance.
- COLLABORATE: present research findings + updated tests, pause for kill/keep decisions.
- STEP-BY-STEP: research one candidate at a time, present findings, refine, repeat.

### Phase 5 - Adversarial Review

Load `sub-skills/04-adversarial-review.md`. For each surviving candidate, spawn parallel critics:
- Hostile investor (5-min coffee chat verdict)
- Hostile incumbent (the obvious competitor's 90-day response)
- Principles auditor (against the founder's bedrock principles + founder shape)
- Tarpit auditor (against the canonical tarpit catalog)

Surface strongest objection from each. Refine candidate to address objections. Up to 2 refinement rounds. If a candidate cannot survive critics after 2 rounds, kill it. If a critic dissents irreconcilably, surface the dissent in the output (never bury it).

**Mode behavior:**
- AUTOPILOT: run critics, refine, kill or advance.
- COLLABORATE: present critic findings, pause for direction on refinement.
- STEP-BY-STEP: walk through each critic's verdict, refine collaboratively.

### Phase 6 - Output Write

Load `sub-skills/05-output-write.md`. For each surviving candidate:
- Write a Raw Idea doc to the user-specified destination using the template in `references/raw-idea-template.md` (matches the retreat's existing Raw Ideas pattern).
- If applicable (and user opted in during Phase 0), append a new thesis to the Heretical Theses Pool with full provenance.

Then write the **session synthesis** to the session document:
- Ranked surviving candidates with one-line case for each
- The single candidate the skill recommends with conviction (case + risks)
- Open questions per candidate
- The forcing question that determines the next step

**Mode behavior (always pauses here regardless of mode):** The user reviews the synthesis and provides direction. The skill never silently writes the final output without a moment of confirmation, even in AUTOPILOT.

### Phase 7 - Forcing Question

The session always closes with exactly one forcing question. Options follow PG's authentication signals:
- "Of the surviving candidates, which one would you most embarrass yourself by walking past?"
- "Which candidate's user can you name with a face by tomorrow at noon?"
- "Which candidate would you sell verbally to one buyer this week before building anything?"

Pick the question whose answer most disambiguates the user's next move. Write it to the session document. End the session.

---
