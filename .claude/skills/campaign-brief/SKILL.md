---
name: campaign-brief
description: >-
  Adversarial pre-launch review for a marketing campaign. Challenges the brief across six
  dimensions (audience specificity, dream outcome, demand evidence, differentiation,
  measurability, message-audience fit) and issues a go/no-go with specific copy edits. Use
  before any campaign ships. Do NOT use to review the copy itself (use `seven-copy-
  critics`) or to audit finished creative (use `brand-review`).
---
<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/campaign-brief/SKILL.md @ 496d37273aca); adapted for this repo (de-branded; no other change, the six dimensions are domain-neutral). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Campaign Brief

An adversarial pre-launch review that challenges a marketing campaign brief before
any execution begins. Based on the adversarial spec reviewer pattern from Garry Tan's
[gstack `/office-hours`](https://github.com/garrytan/gstack), adapted for marketing.

**Core insight from gstack:** The default failure mode in marketing is shipping campaigns
that are technically complete but strategically weak — vague audience, mechanism-first
messaging, no success threshold. The adversarial reviewer catches these before launch,
not after.

## When to Use

- Before finalizing any outbound email or LinkedIn sequence
- Before launching a paid ad experiment
- Before publishing a content push (blog post series, LinkedIn campaign, newsletter)
- Before committing to a partnership or co-marketing arrangement

## When NOT to Use

- For single social posts or one-off tactical content — use `brand-review` for design QA
- For strategic planning upstream of campaigns — use `strategic-brief` or `ceo-review`
- After launch — this is a pre-commitment tool, not a post-mortem

## Agents

**Primary:** CMO

---

## Procedure

### Step 1 — Read the Campaign Brief

Obtain or write out the current campaign brief. A minimal brief must include:
- Target audience
- Core message / value proposition
- Channel and format
- Timeline and budget (if applicable)
- Success metric

If the brief doesn't include all of these, note the gaps and fill them in with explicit
assumptions before proceeding. Assumptions must be labeled clearly.

---

### Step 2 — Adversarial Challenge Across 6 Dimensions

For each dimension, write a challenge in this format:
> "**Claim:** [what the brief says or implies] / **Challenge:** [why this is weak] /
> **Required fix:** [what would close this gap]"

Only write "PASS" if the dimension is genuinely strong. No false credit.

**Dimension 1: Audience Specificity**

Is the target audience a named segment with a real person archetype?

- Weak: "HR managers at mid-market SaaS"
- Strong: "Head of RevOps at a 50–150 person B2B SaaS company who manages a 3-person team
  and is evaluated on pipeline quality, not just volume"

Generic segments do not produce resonant copy. Every word of the campaign must be written
to a specific person. If the audience is too broad, the message will be too broad.

**Dimension 2: Dream Outcome Clarity**

Is the primary promise the **dream outcome** (more bookings, more revenue, less churn,
less manual work), or is it the **mechanism** (AI-powered, automated attribution, real-time)?

- Weak hook: "the workspace gives your agents real-time attribution intelligence"
- Strong hook: "the workspace helped [Company X] book 40% more meetings without adding headcount"

The mechanism is the explanation, not the hook. Lead with what the customer gets, not how it works.

**Dimension 3: Demand Evidence**

Is there evidence this specific message resonates with this specific audience?

Acceptable evidence: direct conversation quotes, past campaign open/reply data, ICP interviews,
competitive research showing this framing works in adjacent markets.

Not acceptable: "we believe," "we think," "it makes sense that."

If no evidence exists, the campaign is a hypothesis, not a campaign. Label it as a test,
not a launch.

**Dimension 4: Differentiation**

What makes this campaign different from 10 other messages in the target's inbox this week?

If you removed the the workspace logo and replaced it with a competitor's, would the message still
sound the same? If yes, the campaign fails on differentiation.

Identify the one thing only we can say. That's the hook.

**Dimension 5: Measurability**

What is the specific success metric and threshold?

- Weak: "improve engagement"
- Strong: "≥15% open rate and ≥3% reply rate in the first 2 weeks; if neither, pause and
  rework before continuing"

What outcome in 2 weeks tells us this worked? What outcome tells us it failed?
Both must be stated in the brief before launch.

**Dimension 6: Message-Audience Fit**

Does the personal win framing match this specific audience's primary motivation?

Different roles have different win conditions even for the same product:
- Head of RevOps: cares about efficiency, process reliability, team scalability
- Founder/CEO: cares about growth rate, not burning cash, competitive positioning
- Sales Manager: cares about rep performance, pipeline conversion, quota attainment

The same product message pitched with a founder lens to a RevOps audience will underperform.
Check that the framing matches the audience's actual day-to-day stakes.

---

### Step 3 — Revised Brief

After identifying weaknesses, rewrite the campaign brief incorporating required fixes.
Produce:

1. **Revised audience definition** (if audience was too generic)
2. **Revised primary message / hook** (if dream outcome wasn't leading)
3. **Evidence note** (explicitly label what's validated vs. hypothesized)
4. **Differentiator statement** (the one thing only we can say)
5. **Success metric and threshold** (specific numbers, specific timeline)
6. **Suggested copy edits** (1–3 specific headline or subject line rewrites, if applicable)

---

### Step 4 — Go/No-Go Recommendation

```markdown
## Go/No-Go Recommendation

**Verdict:** GO / NO-GO / CONDITIONAL GO

**Conditions (if applicable):**
- [What must be resolved before launch]

**Strongest dimension:** [Which of the 6 dimensions is best]
**Weakest dimension:** [Which of the 6 dimensions needs the most work]
```

A **GO** means all 6 dimensions pass or near-pass and the revised brief is ready to execute.
A **NO-GO** means demand evidence is missing or audience specificity is fatally weak.
A **CONDITIONAL GO** means proceed with the revised brief, but treat as a test with
tight feedback loops — don't commit full budget until early signals confirm.

---

## Key Principle: Audience-Specific Personal Wins

From the gstack adversarial reviewer pattern: the same product delivers different personal
wins to different roles. The campaign brief must specify not just what the product does,
but what winning looks like from this specific person's perspective in their job — and
that framing must appear explicitly in the copy.
