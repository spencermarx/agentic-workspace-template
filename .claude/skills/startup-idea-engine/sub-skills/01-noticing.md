# Sub-skill: Noticing (Generation)

**Parent skill:** `startup-idea-engine`

The generation phase. Implements Paul Graham's six structured noticing procedures so candidate ideas are *noticed from the leading edge* rather than *thought up in the abstract*.

**Before starting this sub-skill**, you must have completed Phase 0 (Setup) and Phase 1 (Context Build) of the parent SKILL.md. The context summary, founder shape, principles, topology, prior candidates, and recent reality are loaded into the session document.

**Critical framing rule:** Pure abstract category-search ("let's brainstorm ideas in healthcare") is forbidden. Every candidate must come from one of the six procedures below, which are PG's actual prescriptions. Candidates that cannot be tagged with a procedure are flagged as suspect and treated as sitcom-shaped until proven otherwise.

---

## The Six Procedures (PG, "How to Get Startup Ideas," 2012)

Each procedure surfaces candidates from a different angle of the user's lived experience and leading-edge positions. Run procedures in order; each pass produces 1–3 candidates. Total expected candidates after all six: 5–10. Cull to the strongest before Phase 3.

### Procedure A — Start with Your Own Needs

**The PG question:** "What do you find yourself saying 'why doesn't someone make X?' about? People don't make such complaints about impossible things."

**Operational steps:**
1. From the context summary, surface 3–5 friction points the user has named in recent daily notes, weekly reviews, prior projects, or conversations.
2. For each friction point, ask: is this a tool the user wishes existed? Has the user already started building a hacky workaround?
3. If yes, propose it as a candidate, tagged `procedure-A`.

**Example signals (the operator-specific):**
- "Reeis stalled because Cindy could not self-serve past the first booking flow" → candidate: SMB-tier no-code FSM-aware experience-composition tool.
- "a collaborator's gate fired; founder-led sales doesn't scale" → candidate: AI-augmented founder-replacement sales motion for principle-aligned founders.
- The Intent Architecture RFC itself is a "this should exist but doesn't" signal — candidates in that adjacent space are procedure-A.

**Anti-pattern:** Friction points that the user *has not personally felt* are NOT procedure-A. If the user is gesturing at a third-party's pain ("trades shops have AR problems"), that's procedure-B or procedure-D, not procedure-A.

---

### Procedure B — Live in the Future and Build What's Missing

**The PG question:** "Get yourself to the leading edge of a field that's changing fast — either as a practitioner pushing forward, or as an early adopter living with emerging technology. Then look around and notice what's missing."

**Operational steps:**
1. Enumerate the user's leading-edge positions (loaded by Agent 2 in Phase 1). For the operator, current canonical leading edges include:
   - AI-augmented dev / Intent Architecture RFC
   - Agentic-web substrate thinking (T1, T2, T12)
   - the incumbent vendor / FSM data-model literacy
   - Multi-tenant hierarchical architecture (Walking Skeleton)
   - Doxy.me / professional-services lineage
2. For each leading-edge position, ask: "What is missing from this future that would be obvious to anyone living here?"
3. Flag candidates as `procedure-B`. Each candidate must name the leading-edge position it came from.

**Anti-pattern:** "Leading edge" must be real — the user actually lives in this future, has scar tissue, has shipped in this space. Reading about a space ≠ living in it. AI agent tooling at the level of "I read about Operator" is not a leading edge for the user.

---

### Procedure C — Cross Domains

**The PG question:** "Apply expertise from one field to another. New domain experts don't take the status quo for granted — that ignorance is advantageous."

**Operational steps:**
1. Take each leading-edge position from procedure B and pair it with each adjacent domain the user has touched (from prior projects, lineage docs, current customer conversations).
2. For each pair, ask: "What does the leading-edge competence reveal about the adjacent domain that domain-natives can't see?"
3. Candidates tagged `procedure-C`.

**Examples (the operator-specific):**
- AI-augmented dev × FSM operations → AI-driven the incumbent vendor sanitization (T12 was generated this way).
- Agentic-web substrate × Doxy.me lineage → operator-controlled patient/customer agent representation in healthcare.
- Multi-tenant arch × PE rollup integration → portfolio operations substrate.

**Anti-pattern:** Crossing into a domain the user has zero touch with ("apply your software skills to genomics") produces sitcom ideas, not procedure-C. The adjacent domain must have been touched, however lightly.

---

### Procedure D — Become a Consultant to a Single User

**The PG question:** "When you find unmet needs in others, act like you were retained to solve them. Build for one user; most becomes reusable."

**Operational steps:**
1. From Agent 4's "recent reality" report, list the named real humans the user is currently in conversation with (e.g., Andrew Bontz, the marketing-agency woman, Quo contacts, recently-churned customers).
2. For each, surface the most acute pain they've named in real conversations — not what the user assumes they want, but what they have actually said.
3. Ask: "If you were retained as a consultant to solve this person's most acute pain, what would you build?"
4. Candidate tagged `procedure-D` with the named human attached.

**Examples (the operator-specific):**
- Andrew Bontz × his stated post-estimate-to-scheduled-job gap → if (and only if) Airship doesn't beat us there.
- Andrew Bontz × his men's-health agency clients × pre-booking patient confidence → procedure-D.
- The marketing-agency woman × her stated the incumbent vendor setup chaos → procedure-D (this is what generated T12).

**Anti-pattern:** "If I were a consultant to a hypothetical user…" — this is procedure-A (own needs) wearing procedure-D's clothes. Procedure-D requires a *named* human you can call this week.

---

### Procedure E — Schlep-Heavy Problems

**The PG question:** "Move toward messy, tedious, annoying problems. Programming space is stripped pretty clean of convenient ideas. The valuable ones are sitting there in plain sight; founders flinch from the work, and that's why they stay open."

**Operational steps:**
1. Enumerate problem spaces where the user has already disabled their schlep filter (i.e., done the boring grinding work most founders avoid). For the operator:
   - the incumbent vendor API integration depth
   - FSM data-model literacy across customer instances
   - Intent Architecture / spec-driven AI codegen
   - Multi-tenant authorization with downward inheritance
2. For each, ask: "What painful, tedious problem could only be solved by someone with this schlep-disabled position?"
3. Candidates tagged `procedure-E`.

**Examples:**
- Schlep-disabled on the incumbent vendor API → ST sanitization, ST migration tooling, ST audit-as-a-service.
- Schlep-disabled on multi-tenant arch → portfolio ops for PE rollups, white-label substrate for agencies.
- Schlep-disabled on spec-driven codegen → enterprise governance for AI-assisted dev (the IA RFC commercialized).

**Anti-pattern:** "We could disable our schlep filter" — too aspirational. The schlep must already be done; the candidate exploits *existing* schlep-disabled positions, not future ones.

---

### Procedure F — Ride Waves

**The PG question:** "Look for technological declines (Moore's law for gene sequencing, 3D printing, etc.). What becomes possible in 3–5 years that we currently rule out? What companies might profit from the decline of incumbents?"

**Operational steps:**
1. Load `references/yc-rfs-current.md` (current YC Requests for Startups, used as a wave catalog) and any user-specific wave intuitions from the context summary.
2. For each documented wave, ask: "Given the user's topology and competence, what business does this wave make possible that wasn't possible 18 months ago?"
3. Candidates tagged `procedure-F` with the wave name attached.

**Current 2026 waves to consider (verify with WebSearch on YC RFS if older than 90 days):**
- Agentic-web maturity (Computer Use, Operator, MCP) — agents operating on operators' behalf
- AI-receptionist deployment crisis at SMB (knowledge-base hallucination)
- PE-rolled vertical SaaS consolidation (every SMB-dense vertical now has a PE platform)
- AI-native hedge funds, AI-powered agencies (per Spring 2026 RFS)
- Hard-tech pivot (per Summer 2026 RFS — agriculture robotics, counter-drone, lunar manufacturing — most of these are NOT founder-shape compatible for the operator)
- Cognitive-sovereignty backlash (privacy-first, attention-respecting tooling)
- GLP-1 / elective-medical operational boom

**Anti-pattern:** Waves the user is not equipped to ride (e.g., agriculture robotics for a software founder) are not procedure-F candidates. The wave must intersect with the user's topology / competence / lineage.

---

## After the Six Procedures

Aggregate all candidates surfaced. Each candidate is now a one-paragraph description with:
- Procedure tag (A through F)
- The lived-experience or leading-edge anchor that produced it
- One-sentence pain statement
- One-sentence mechanism

This list goes into the session document under "Phase 2 Noticing Output" before advancing to Phase 3 (Framework Tests).

**Cull rule:** If two candidates are essentially the same idea surfaced from two procedures, merge them and keep the strongest provenance. If a candidate fails to articulate a specific pain ("would help small businesses do X better"), kill it before it enters Phase 3 — that candidate is sitcom-shaped already.

**Expected output count:** 5–10 candidates after culling, depending on how many procedures yielded results. If fewer than 3 candidates survive, the leading-edge positions or named-human pool is too thin — flag this in the session doc and prompt the user (in COLLABORATE / STEP-BY-STEP modes) for additional inputs.

---

## Mode Behavior

| Mode | Behavior in this sub-skill |
|---|---|
| AUTOPILOT | Run all six procedures silently. Output the aggregated list to the session doc. Advance to Phase 3 without pause. |
| COLLABORATE | Run all six procedures. Present the aggregated list. Pause via `AskUserQuestion`: "Which candidates advance to Phase 3 framework tests? (Recommend keeping {N})". User can prune, add, or override. |
| STEP-BY-STEP | Run procedures one at a time. After each, present that procedure's candidates. Pause via `AskUserQuestion` with one question at a time. User can refine, add context, kill, or move on. |

---

## Output to Session Document

```markdown
## Phase 2 — Noticing Output

| Candidate | Procedure | Anchor | One-line Pain | One-line Mechanism |
|---|---|---|---|---|
| {name} | A–F | {lived experience or leading edge} | {pain} | {mechanism} |
| ... | ... | ... | ... | ... |

**Procedures that yielded:** A {count}, B {count}, C {count}, D {count}, E {count}, F {count}

**Culled (and why):**
- {candidate} — {reason: sitcom-shaped, duplicate, no named pain, etc.}
```

Advance to Phase 3 (Framework Tests).
