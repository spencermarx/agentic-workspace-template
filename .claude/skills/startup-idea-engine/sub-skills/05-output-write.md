# Sub-skill: Output Write

**Parent skill:** `startup-idea-engine`

For every candidate that survived Phase 5 (Adversarial Review) — including SHIP-WITH-DISSENT candidates — write a Raw Idea document to the user-specified destination using the canonical template. If the destination is an active retreat folder and the user opted in during Phase 0, append a new thesis to the Heretical Theses Pool. Then write the session synthesis with the recommended candidate and forcing question.

**Before starting this sub-skill**, the surviving candidates from Phase 5 are in the session document with full provenance: noticing procedure, framework test matrix, research findings, critic verdicts, refinements, and any unresolved dissent.

---

## Step 1 — Write Raw Idea Doc Per Surviving Candidate

For each candidate, write a file named:

```
{output-destination}/{Candidate Name} — Problem and Solution Space.md
```

Use the template at `references/raw-idea-template.md` exactly. The template matches the existing retreat Raw Ideas pattern (Fluid Websites, Mesh Substrate, Cooperative Substrate, Agentic SaaS Operations Substrate, etc.) so new docs are structurally and visually consistent with the corpus.

**Required sections (per template):**
- Frontmatter with: `date`, `type: raw-idea`, `status: raw, contestable, unrefined, ready to be questioned and reworked`, `audience`, `related` (cross-links to relevant theses, prior raw ideas, the operating frame), `tags`
- "Raw idea" warning callout at the top
- `# What this is`
- `# The problem, stated specifically`
- `# The solution`
- `# Why now: structural forces converging` (optional but strong)
- `# Properties the substrate / product needs`
- `# Concrete first wedges` (with named buyer, named pain, mechanism, price, 90-day proof)
- `# Business model considerations`
- `# Strategic questions this exposes`
- `# Open questions for the cabin`
- `# What this idea conflicts with or pressures`
- `# Heretical thesis pool entry` (if applicable — TXX claim + implication, drafted from candidate)
- `# How to use this doc`
- Provenance footer: which session generated this, which procedure surfaced it, which critics signed off, what dissent (if any) survived

**Critical: do not flatter or hedge in the Raw Idea doc.** Write it in the candidate's strongest voice with the unresolved dissent named clearly. The reader (the user, future cabin sessions, or another agent) must be able to see the candidate's strengths and the surviving objections in the same document.

**Cross-references:** Add `[[wikilinks]]` to:
- The thesis in the Heretical Theses Pool (if added)
- The operating frame doc (founder shape, principles)
- Adjacent Raw Idea docs (other surviving candidates from this session, or relevant prior candidates)

---

## Step 2 — Update Heretical Theses Pool (if opted in)

If the user opted in during Phase 0 AND the destination is an active retreat folder:

1. Open the Heretical Theses Pool file (typically `{retreat}/the operator/02 Heretical Theses Pool.md`).
2. Determine the next available thesis number (find the highest TN in the file and use TN+1).
3. Append a new thesis section under the appropriate domain header (or create a new domain section if needed).
4. Format strictly per the existing pattern in the pool:

```markdown
### T{N} — {Thesis Name}

**Claim.** {Two sentences: specific year, specific claim, specific implication setup.}

**Implication.** {What follows if the claim is true. What this implies for any business operating in that world.}

- **Drafted:** {YYYY-MM-DD} ({brief provenance: noticing procedure, key insight that surfaced it, who drafted})
- **Status:** [seed]
- **the workspace relevance:** {1–2 paragraph synthesis: how this connects to the candidate's wedge, founder shape fit, principle alignment, topology coupling, relationships to other Theses in the pool. Cross-reference the Raw Idea doc with `[[wikilink]]`.}
```

5. **Do not modify existing theses.** Append only.

---

## Step 3 — Session Synthesis

Append the final synthesis to the session document at:

```
{output-destination}/{YYYY-MM-DD}-startup-idea-engine-session.md
```

Required sections:

```markdown
## Phase 6 — Synthesis

### Surviving Candidates

| # | Candidate | Procedure | Strongest Case (1 line) | Strongest Objection (1 line) |
|---|---|---|---|---|
| 1 | {name} | {A–F} | {one-line case} | {one-line surviving objection or "none unresolved"} |
| 2 | ... | ... | ... | ... |

### Raw Idea Documents Written
- `{path/to/Candidate Name — Problem and Solution Space.md}`
- ... (one per surviving candidate)

### Heretical Theses Pool Updated (if applicable)
- T{N}: {Thesis Name} appended to `{path/to/02 Heretical Theses Pool.md}`
- ... (one per surviving candidate)

### Recommended Candidate (with conviction)

**The skill recommends:** {Candidate name}

**Why:**
1. {Reason 1, with specific evidence from research and critic review}
2. {Reason 2}
3. {Reason 3}

**Key risks:**
1. {Risk 1, with mitigation if any}
2. {Risk 2, with mitigation if any}

**Next concrete step:** {Specific action the user can take this week — e.g., "probe candidate X with named buyer Y by Friday"}

### Open Questions
- {Question 1: what would resolve it}
- {Question 2: what would resolve it}
- {Question 3: what would resolve it}
```

**The recommendation is mandatory.** The skill picks ONE candidate and presents the case with conviction. The user can override (the user is sovereign), but the skill must take a position. "All candidates are valid options" is failure.

---

## Step 4 — The Forcing Question

End the session with exactly one forcing question, written to the session document and presented to the user. The question must:
- Be answerable by the user (no research required)
- Determine the next concrete step
- Pressure the recommended candidate at its weakest point

**Choose from this template menu:**

| Question shape | When to use |
|---|---|
| "Of the surviving candidates, which one would you most embarrass yourself by walking past in 2027?" | When the user has been hedging between candidates and needs to commit |
| "Which candidate's named buyer can you have on a call by {Friday/in 7 days}?" | When buyer-validation reachability is the bottleneck |
| "Which candidate would you sell verbally to one buyer this week before building anything?" | When the user needs to apply Buchheit's "sell before build" |
| "If a hostile investor read all surviving candidates cold tomorrow, which one would survive their first three questions?" | When investor-grade defensibility is the open question |
| "Which surviving candidate, if it succeeded for a year, would in hindsight have wasted your founder shape?" | When founder-fit drift is the highest-risk failure mode |

Pick the question whose answer most disambiguates the user's next move. Write it to the session document and present it as the closing of the session.

---

## Mode Behavior

| Mode | Behavior |
|---|---|
| AUTOPILOT | Write all Raw Idea docs. Update Theses Pool if opted in. Write session synthesis. Present synthesis to user with the forcing question. **The skill always pauses here regardless of mode** — silent shipping of the final output without user awareness is forbidden. |
| COLLABORATE | Same as AUTOPILOT but additionally pause before each Raw Idea doc is written: "Approve writing {Candidate} as Raw Idea doc? Edits before write?" Allows user to refine the doc content. |
| STEP-BY-STEP | Walk through each Raw Idea doc section by section. The user reviews each section before the next is written. Slow but precise. |

---

## Anti-Patterns

- **Skipping the recommendation.** The skill must pick. Presenting candidates without a recommended pick is the sycophancy failure mode.
- **Burying dissent.** Unresolved critic dissent must appear in the Raw Idea doc under a "Reviewer Concerns" section AND in the session synthesis.
- **Mismatching the template.** New Raw Idea docs that don't match the existing retreat pattern erode the corpus's coherence. Use the template exactly.
- **Forgetting the cross-references.** Each Raw Idea doc must wikilink to the operating frame, the relevant thesis, and adjacent Raw Idea docs. Orphaned docs are weaker than connected ones.
- **Writing the forcing question generically.** "What's next?" is failure. The forcing question must pressure the recommended candidate's specific weakest point, surfaced from the critic review.

---

## Closing Convention

After the session document is complete and the user has seen the forcing question, the session ends. Do not loop back into ideation in the same session unless the user explicitly requests it (e.g., "kill all candidates and start over"). The next ideation cycle is a new session.

If the user requests an immediate next-step action (e.g., "draft the outreach to the named buyer"), that is a different skill's job (e.g., `loom-prep`, `slack`, etc.) — hand off, do not extend.
