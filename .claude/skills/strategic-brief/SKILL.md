---
name: strategic-brief
description: >-
  Pre-commitment demand validation for a product feature, strategic initiative, or
  significant marketing investment. Runs a 6-question demand diagnostic, writes an
  initiative brief, then applies adversarial review to challenge demand evidence, scope
  creep, and feasibility before a go/no-go. Use before committing more than about two days
  of work. Do NOT use to rank a backlog (use `rice-prioritization`).
---
<!-- Vendored from https://github.com/spencermarx/anthony-and-spencer-business-workspace (.claude/skills/strategic-brief/SKILL.md @ 2e62970bb6cd); adapted for this repo (issue-tracker references generalised; the two-day-of-agent-work trigger restated without naming a tracker). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Strategic Brief

A pre-commitment ritual that forces demand validation before resources are committed.
Based on Garry Tan's [gstack `/office-hours`](https://github.com/garrytan/gstack) - specifically the Startup mode interrogation and adversarial spec reviewer pattern.

**Core insight from gstack:** The adversarial pre-commitment review closes the gap between
"this sounds like a good idea" and "this has real demand evidence." The default human
instinct is to execute on the first plausible idea. This skill forces the question:
what's missing, what's the strongest counterargument, and which assumption is most
likely wrong?

## When to Use

- Before creating any tracked work item expected to consume >2 days of agent work
- Before green-lighting a new product feature, strategic initiative, or significant marketing investment
- When a request arrives without clear demand evidence or success criteria
- When scope feels fuzzy or the problem definition shifts across conversations

## When NOT to Use

- For tactical execution tasks with clear specs (use the issue directly)
- For work explicitly delegated by the board with scope already locked
- For sub-2-day tasks where the overhead isn't warranted

## Agents

**Primary:** CEO, CPO
**Secondary:** Any agent receiving a large scope request from the board

---

## Procedure

### Step 1 - Demand Diagnostic (6 Questions)

Ask the initiator (or yourself, reasoning from available context) these six questions
in sequence. Do not move to the next question until the current one is answered with
specificity. Generic answers ("our users", "improve engagement") are not acceptable - push for named segments, concrete evidence, and measurable definitions.

**Q1 - Who specifically experiences this problem?**
Not "users" or "customers." Name the segment: a job title + company type + situation.
Example: "Head of RevOps at a 50–150 person B2B SaaS company managing a team of 3."

**Q2 - What's the evidence of demand?**
Options: direct customer conversations (quote them), observed workarounds, support tickets,
prior campaign data, competitive gap analysis. "We think" or "it seems" are not evidence.

**Q3 - What does success look like in 90 days?**
Must be measurable and specific. Not "improve retention." Instead: "Reduce 30-day churn
from 8% to 5% among the Head of RevOps segment."

**Q4 - What's the minimal viable version?**
What would you cut if you had half the time? This defines the true core bet and reveals
scope creep in the original description.

**Q5 - What are you explicitly NOT building?**
Force a scope boundary. If nothing is excluded, scope is undefined.

**Q6 - Why now?**
Why is this the right thing to work on today vs. the next best alternative? What is the
opportunity cost of delay, and what's the opportunity cost of doing this instead of X?

---

### Step 2 - Write the Initiative Brief

After the 6 questions, synthesize answers into a structured brief. If working within a
tracked work item, write this as an issue document with key `brief`. Otherwise write to a
markdown file.

**Brief format:**

```markdown
# Initiative Brief: [Initiative Name]

**Date:** [YYYY-MM-DD]
**Initiated by:** [Agent or person]
**Estimated scope:** [days of agent work]

## Problem
[Who has the problem, in specific terms. 2–3 sentences max.]

## Demand Evidence
[Concrete evidence: quotes, data, observed behavior. No speculation.]

## Success Criteria (90 days)
[Measurable outcome. One sentence.]

## Minimal Viable Scope
[What we're building. Bulleted list.]

## Explicit Non-Scope
[What we are NOT building. Bulleted list.]

## Why Now
[Opportunity cost reasoning. 2–3 sentences.]
```

---

### Step 3 - Adversarial Review (up to 2 rounds)

After the brief is written, perform a self-adversarial pass (or prompt a second AI
sub-agent if the context supports it). The adversary's job is to find weaknesses in
the brief across four dimensions:

1. **Demand evidence gaps** - Is the evidence real, or inferred? Would a skeptic accept it?
2. **Scope creep** - Does the minimal scope still contain aspirational additions?
3. **Feasibility holes** - Are there hidden dependencies, missing data, or technical assumptions
   that haven't been validated?
4. **Unclear success criteria** - Would two people reading the success criteria disagree on
   whether it was achieved?

For each weakness found, write a challenge in this form:
> "Claim: [what the brief asserts]. Challenge: [why this is weak or unverified]. Required fix: [what would close this gap]."

If the brief addresses all challenges well, skip round 2. If challenges remain unresolved
after 2 rounds, escalate to the board - do not proceed without resolution.

---

### Step 4 - Go/No-Go Recommendation

After the adversarial review, issue a clear recommendation:

```markdown
## Go/No-Go Recommendation

**Verdict:** GO / NO-GO / CONDITIONAL GO

**Conditions (if applicable):**
- [Specific condition that must be resolved before proceeding]
- [Second condition if needed]

**The 1–2 concerns that most need resolution:**
1. [Highest-risk open question]
2. [Second-highest if applicable]
```

A **GO** means demand evidence is strong, scope is clear, success criteria are measurable.
A **NO-GO** means demand evidence is weak or missing - do not proceed until evidence is gathered.
A **CONDITIONAL GO** means proceed only after resolving the listed conditions.

---

### Step 5 - Publish and Link

- If in a tracker context: write the brief to the issue document, post a comment with
  the verdict, and update the issue status accordingly.
- If creating a new initiative: include the brief as the first document on the new issue
  before any implementation subtasks are created.

---

## Key Principle: Specificity Over Generality

Borrowed directly from gstack: **named customers, specific examples, concrete data points - always.**
"Three customers in our target segment told us they spend 4 hours/week on this manually" beats
"customers find this valuable." The brief should be quotable in a board meeting.
