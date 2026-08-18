# Reference: Raw Idea Document Template

This template matches the canonical pattern used in the retreat's Raw Ideas folder (`the workspace Company Files/Product/Design/Brainstorm/Exercises/2026-04-26 Week Retreat/the operator/Raw Ideas/`). Use it exactly when writing new Raw Idea documents from `sub-skills/05-output-write.md`. The structural and visual consistency with the existing corpus (Fluid Websites, Mesh Substrate, Cooperative Substrate, Agentic SaaS Operations Substrate, Evolutionary Goal-Pursuit Engine, Agent-Facing Operator Surface) is required.

---

## Filename convention

```
{Candidate Short Name} - Problem and Solution Space.md
```

Examples that exist in the corpus:
- `Fluid Websites - Problem and Solution Space.md`
- `Mesh Substrate - Biological Frame.md`
- `Cooperative Substrate for Professionals Navigating AI Displacement - Problem and Solution Space.md`
- `Agentic SaaS Operations Substrate - Problem and Solution Space.md`

Use a multi-word descriptive short name. Don't use a vague single word ("Substrate," "Engine"). The short name should let a future reader recognize the candidate from filename alone.

---

## Frontmatter template (copy this verbatim, then fill in)

```yaml
---
date: {YYYY-MM-DD}
type: raw-idea
status: raw, contestable, unrefined, ready to be questioned and reworked
audience: {primary audience - typically "the operator and the cabin"}
related:
  - "[[../02 Heretical Theses Pool#T{N} - {thesis name}]]"
  - "[[../01 the operator's Cabin Operating Frame]]"
  - "[[{relevant adjacent Raw Idea filename without extension}]]"
  - "[[../Retreat Raw Notes]]"
tags:
  - retreat
  - raw-idea
  - {domain-specific tag, e.g., agentic-ai, mesh, cooperative, fluid-websites}
  - {business-shape tag, e.g., business-model, long-arc-vision, wedge}
---
```

---

## Body template (copy this structure exactly)

```markdown
> [!warning] Raw idea, ready to be questioned, ripped apart, reworked, refined, redesigned, redirected
> This document captures an exploration in progress, not a recommendation. Surfaced through {brief provenance - "a working session on YYYY-MM-DD between the operator and the cabin co-pilot, building on {key insight or trigger}"}. Treat every claim as a hypothesis. The cabin will stress-test, sharpen, kill, or evolve any of this Tuesday through Saturday.

# What this is

This is the problem and solution space underneath {T{N} - Thesis Name} in the [[../02 Heretical Theses Pool|Heretical Theses Pool]]. {Short paragraph describing the candidate's central claim.}

{If applicable: a horizon table - wedge / midterm / long-arc - like the one in Agentic SaaS Operations Substrate. This grounds the candidate as a three-horizon stack.}

| Horizon | Shape |
|---|---|
| **90-day wedge** | {one-paragraph wedge description} |
| **1-3 year midterm bridge** | {one-paragraph bridge description} |
| **5-10 year long-arc vision** | {one-paragraph vision description} |

Each layer ladders to the next without architectural rewrites. Each layer respects the founder shape. Each layer survives the four principles.

# The problem, stated specifically

{4–7 numbered sub-points. Each one names a structural failure mode in the world today. Each one is grounded in evidence - research, customer-call signal, prior-project lineage, or documented pattern. Avoid speculation; if a claim is speculative, mark it so.}

**1. {First failure mode.}** {Specific evidence + implication.}

**2. {Second failure mode.}** {Specific evidence + implication.}

...

The cumulative effect is {synthesis sentence - the meta-pain that makes this candidate worth pursuing}.

# The solution: {candidate name}

{Description of how the candidate works, in operational steps. The operator does X. The substrate / product / engine does Y. The result is Z. Use "the substrate" or "the engine" or "the product" depending on candidate shape.}

**The {candidate} works as follows:**

{Step-by-step operational description. Each step is a real capability, not a vision statement.}

# Why now: structural forces converging (optional but strong)

{Subsections grounding the candidate's timing in real waves:}

**Carlota Perez timing.** {Where in the AI / tech cycle this lives.}

**Bret Victor principle.** {Inherited assumption being violated.}

**{Other relevant lens - Ted Chiang on agents, Marc Levinson on primitives, Ben Thompson aggregation theory inversion, etc.}**

**{Specific 2026 wave + why it matters now.}**

# Properties the {substrate / product / engine} needs

{Numbered list, 8–12 items. Each is a property the candidate must have to succeed. Mark which are hard / soft / non-negotiable.}

1. **Operator-aligned incentives.** {How.}
2. **Anti-exploitation against {users / participants / operators}.** {How.}
...

# Concrete first wedges

{For each candidate wedge shape - typically 3–5:}

**{Wedge name.}** {1-3 sentences on shape.}

**Buyer.** {Specific persona, title, segment, situation. Named example helps.}

**Pain.** {This-quarter, budget-line-attached, concretely articulated.}

**Mechanism.** {What we sell that solves it.}

**Pricing.** {Range, packaging, who signs.}

**90-day proof point.** {One falsifiable result that confirms or kills.}

# Business model considerations

{Multiple admissible shapes; assess each against the founder principles.}

1. **{Shape 1.}** {Description + principle assessment.}
2. **{Shape 2.}** {Description + principle assessment.}
...

The candidate must NOT {explicit principle violation to avoid - typically "take a cut on operator-to-customer transactions" for the operator's principles}.

# Strategic questions this exposes

{Numbered list, 6–10 questions the cabin should resolve before commitment.}

# Open questions for the cabin

{Numbered list, 4–8 questions with deadlines or resolution conditions.}

# What this idea conflicts with or pressures

{Bulleted list of relationships to:}

- **Principles {1-4}.** {How candidate aligns or strains.}
- **Founder shape.** {Compatibility, with caveats.}
- **{Each related thesis T{N}.}** {Coupling, conflict, or supersession.}
- **The Walking Skeleton.** {Architectural fit.}
- **Current the workspace customers.** {What happens to them.}
- **Q1 GTM plan.** {Supersession or coexistence.}

# Heretical thesis pool entry (if applicable)

{If the candidate produced a new thesis in the pool, restate the thesis here for inline reference. Format:}

> **T{N} - {Thesis Name}**
>
> **Claim.** {Two sentences.}
>
> **Implication.** {Implication paragraph.}

# Reviewer Concerns (if any unresolved adversarial-review dissent)

{Per the gstack pattern: never bury dissent. If any of the four critics returned a FAIL or DEFER that was not resolved through refinement, name it here:}

> **{Critic name}'s unresolved concern:** {The concern, in their voice, with the specific evidence or commitment that would resolve it.}

# How to use this doc

Read it cold. Notice what makes you flinch and what makes you nod. The flinches are signal: either the idea is wrong somewhere, or it is right somewhere uncomfortable.

{Specific suggestions for next steps: which Devil's-Advocate prompt to apply, which Principles-Auditor angle to test, which buyer to probe, which research to run.}

If this raw idea survives, evolve it in place. If it does not, archive it but keep the framing: {what about this thinking is reusable for future directions}.

---

## Provenance footer

**Surfaced.** {YYYY-MM-DD} via `startup-idea-engine` skill, session {session-doc-filename}. Procedure: {A/B/C/D/E/F per noticing taxonomy}. Anchor: {the specific lived-experience or leading-edge position that produced it}.

**Framework tests.** {N PASS / N PARTIAL / N FAIL - link to session doc for full matrix.}

**Research validation.** {One-line summary of what survived vs. what degraded. Link to session doc.}

**Adversarial review.** Critics: {SHIP / KILL / SHIP-WITH-DISSENT}. {If SHIP-WITH-DISSENT, name the dissent.}

**Status.** {Strongest signal in this session, or "one of N surviving candidates." Honest read.}
```

---

## Style notes

Match the existing corpus exactly:
- No em dashes in the body (use commas, periods, parentheses).
- No filler ("interesting," "comprehensive," "robust").
- Specificity over generality. Named segments. Named pains. Named numbers.
- Wikilinks `[[...]]` for cross-references to other Raw Ideas, the operating frame, and theses.
- Voice: direct, declarative, willing to take a position. Where the candidate has a weak point, name it - don't bury.
- Length: existing Raw Ideas range 200-500 lines. Aim for the upper end if the candidate is the recommended one; lower if the candidate is a parking-lot direction.

---

## What NOT to include

- Do not include the session document's full Phase 3 / 4 / 5 record in the Raw Idea doc. The Raw Idea doc is the *artifact*; the session doc is the *journal*. Reference the session doc for full provenance, but keep the Raw Idea doc focused on the candidate itself.
- Do not include the rejected candidates from the same session in the Raw Idea doc. Each surviving candidate gets its own file. Killed candidates appear only in the session doc.
- Do not use the words "interesting," "comprehensive," "robust," "novel" (without specific evidence), or "unique" (without specific evidence). These are AI tells.
