---
name: ceo-review
description: >
  Structured CEO-level strategic review of any initiative plan, proposal, or
  roadmap item. Requires an explicit mode selection upfront (EXPAND, CHERRY-PICK,
  HOLD, or CUT) then evaluates across 8 business dimensions. Produces a structured
  review document and a prioritized list of open questions. Invoke when evaluating
  quarterly roadmap priorities, significant new bets, or resourcing decisions above
  a meaningful threshold. Based on gstack's /plan-ceo-review.
---
<!-- Vendored from https://github.com/spencermarx/anthony-and-spencer-business-workspace (.claude/skills/ceo-review/SKILL.md @ 2e62970bb6cd); adapted for this repo (issue-tracker references generalised). See [vendoring provenance](../../../Standards/harness-standards.md#vendoring-provenance). -->


# CEO Review

A 4-mode structured CEO-level review for any initiative plan, proposal, or roadmap item.
Based on Garry Tan's [gstack `/plan-ceo-review`](https://github.com/garrytan/gstack).

**Core principle from gstack:** Before reviewing any plan, choose a mode. Trying to expand,
hold, and cut simultaneously in one session produces confused output. **Mode-first thinking**
forces an explicit strategic stance that governs every dimension of the review.

## When to Use

- When evaluating quarterly roadmap priorities
- When making resourcing decisions above ~2 days of agent effort
- When reviewing a new strategic bet, product pivot, or significant investment proposal
- When a plan has been presented and a rigorous, structured CEO-level response is needed

## When NOT to Use

- For tactical execution reviews (use tracker comments directly)
- For marketing asset review (use `brand-review`)
- For pre-commitment demand validation (use `strategic-brief` first, then `ceo-review`)
- For campaigns (use `campaign-brief`)

## Agents

**Primary:** CEO

---

## Procedure

### Step 1 - Select Mode

Before reading the plan in detail, explicitly select and declare one mode. The mode governs
the entire review - do not mix modes within a single session.

| Mode | Strategic context | What it means |
|---|---|---|
| **EXPAND** | We're in growth mode | What's the 10x version? What would we add with 3x resources? |
| **CHERRY-PICK** | Constrained resources | Which 20% of this delivers 80% of value? |
| **HOLD** | Execution rigor | Don't add anything - pressure-test everything already in scope. |
| **CUT** | Over-committed | What do we kill without losing the core bet? |

Declare the mode at the top of the review document:
> "Mode: HOLD - We are executing on the current roadmap without additions. This review
> pressure-tests execution quality, not scope."

---

### Step 2 - Review Across 8 Dimensions

Evaluate the initiative against each dimension. Write 2–5 sentences per dimension.
Be direct: state what's strong, what's weak, and what's missing.

**Dimension 1: Strategic Fit**
Does this advance our core bets? Is it central to what we're building, or adjacent/distraction?
Does the team agree this is a priority, or was it driven by recency bias or a single voice?

**Dimension 2: Market Timing**
Why now? What happens if we do this 6 months later? What's the window, and is there evidence
the window is real (competitor moves, customer pressure, regulatory change)?

**Dimension 3: Resource Requirement**
What is the realistic cost - agent time, human time, cash, and attention? Is the estimate
anchored to comparable past work, or is it optimistic? What are the hidden costs (maintenance,
iteration, dependencies)?

**Dimension 4: Competitive Moat**
Does this create a durable advantage, or is it easily copied? If a well-funded competitor
launched the same thing next quarter, what would we have that they wouldn't?

**Dimension 5: Reversibility**
Is this a two-way door or a one-way door? Two-way = can be undone cheaply.
One-way = hard to reverse (architectural decisions, public commitments, vendor lock-in).
One-way doors require more upfront rigor.

**Dimension 6: Measurability**
How do we know it worked? What's the specific metric and threshold at 30 days and 90 days?
If no metric exists, the initiative cannot be evaluated - this is a blocking concern.

**Dimension 7: Dependencies**
What else has to be true for this to succeed? List all external dependencies:
other teams, third-party tools, data availability, customer behavior changes, etc.
Which dependency is most likely to slip, and what happens to this initiative if it does?

**Dimension 8: Risk Concentration**
What's the single most likely failure mode? Not a laundry list - name the one thing.
If this initiative fails, what's the post-mortem going to say caused it?

---

### Step 3 - Mode-Specific Output

After the 8-dimension review, produce mode-specific findings:

**EXPAND mode output:**
- Top 3 additions that would 2–3x the value of this initiative
- Resources required for each addition
- Which additions are compatible with current timeline vs. next phase

**CHERRY-PICK mode output:**
- The highest-ROI 20% of scope (specific features/deliverables, not abstract categories)
- What to defer to v2 with rationale
- Estimated effort delta (what this saves vs. full scope)

**HOLD mode output:**
- The 3 highest-risk execution assumptions in the current scope
- Specific pressure-test questions the team must answer before proceeding
- Leading indicators to watch in the first 2 weeks of execution

**CUT mode output:**
- What to eliminate (specific, not vague - name the features/workstreams)
- What the initiative becomes after cuts (re-stated minimal scope)
- Confirmation that the core bet is preserved after cutting

---

### Step 4 - Prioritized Open Questions

Close with a list of open questions that must be resolved before proceeding. Max 5.
Rank by urgency. Each question must include: who needs to answer it, and by when.

```markdown
## Open Questions (prioritized)

1. [Question] - Owner: [name/role] - Needed by: [date or milestone]
2. [Question] - Owner: [name/role] - Needed by: [date or milestone]
...
```

---

### Step 5 - Publish Review

If working in a tracked work item: write the review as an issue document (key: `ceo-review`).
Post a comment with the mode selected, the top concern from each dimension, and the #1 open question.

If working on a freestanding proposal: write to the initiative's planning document.
Send a summary comment or Slack message to the relevant stakeholder(s).
