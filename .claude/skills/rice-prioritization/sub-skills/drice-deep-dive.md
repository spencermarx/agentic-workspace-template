---
name: drice-deep-dive
description: >
  Refine a shortlist of 3-5 top RICE candidates from rough relative scores into
  detailed, defensible estimates: expected annualized revenue (or the round's
  goal in absolute units), an explicit hypothesis per item, and a refined effort
  breakdown. This is DRICE (Detailed RICE), Lenny Rachitsky's two-stage method:
  turn a 30-second estimate into a 30-minute one. Use AFTER rice-prioritization
  has produced a top 3-5, when those candidates are high-stakes enough to warrant
  deeper modeling before committing. Do NOT use to score a fresh or long backlog
  (run rice-prioritization first), and do NOT use for a single go/no-go (use
  strategic-brief).
---

# DRICE Deep Dive

The second stage of a two-stage prioritization. Plain RICE ranks the whole
backlog with rough relative scores (S/M/L thinking). DRICE takes only the top
3-5 that survived and replaces the rough numbers with detailed estimates worth
defending. Teams applying this reported moving their key metric roughly twice as
much as with standard RICE alone ([Lenny Rachitsky](https://www.lennysnewsletter.com/p/introducing-drice-a-modern-prioritization)).

Run this only on a shortlist. The whole point is that the detailed estimate is
expensive, so you spend it only where the ranking is close or the stakes are
high. If there is no shortlist yet, run `rice-prioritization` first.

## When to use

- `rice-prioritization` produced a top 3-5 and the order matters enough to model deeper.
- Two or more top candidates are a near-tie and the cheap scores cannot separate them.
- A high-stakes bet needs a number a operator can defend, not a relative score.

## When NOT to use

- No ranked shortlist exists yet -> run `rice-prioritization`.
- A long or fresh backlog needs a first pass -> run `rice-prioritization`.
- A single initiative go/no-go -> `strategic-brief`.

## Procedure

### Step 1 - Take the shortlist

Start from the `rice-prioritization` output. Take the top 3-5 items and their
existing rough scores. Confirm the round's goal and time window carry over
unchanged, so the detailed numbers stay comparable to the first pass.

### Step 2 - Replace Reach x Impact with an absolute outcome

For each item, move from relative scoring to an absolute expected outcome in the
goal's units, usually expected annualized revenue or the round metric ([Lenny](https://www.lennysnewsletter.com/p/introducing-drice-a-modern-prioritization)):

- State the **hypothesis** explicitly: "we believe X will change Y by Z because ...".
- Build the number bottom-up: reach in the window x expected per-user effect x value. Show the arithmetic.
- Keep the same basis (segment, weighting) across all shortlisted items.

This collapses the rough Reach and Impact tiers into one modeled expected value
per item. Confidence still discounts it; Effort still divides it.

### Step 3 - Refine Confidence and Effort with the owners

- **Confidence** - re-derive from the strength of the hypothesis and the evidence behind the expected value, not from the first-pass tier. Tie it to specific evidence.
- **Effort** - get a refined breakdown from the people who will build it, across all disciplines, with the known unknowns named. This is a NEEDS-HUMAN input in autonomous use; do not self-assign it.

### Step 4 - Recompute and compare to the rough pass

Run the refined numbers through the calculator (DRICE keeps the RICE arithmetic;
only the inputs got more detailed):

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/rice_score.py /path/to/shortlist.json
```

Note the expected outcome (absolute units) as a passthrough field alongside the
score. Then compare the detailed ranking to the rough one: if the order changed,
say why; the change is the value of running DRICE.

### Step 5 - Write the artifact

Append to or sit beside the original RICE artifact in the same activities folder:

`Clients/<venture>/Activities/<YYYY-MM-DD> RICE Prioritization - <subject>/01-drice-deep-dive.md`

Include per item: the hypothesis, the bottom-up expected outcome with arithmetic,
the refined Confidence (with evidence) and Effort (with breakdown), the recomputed
score, and how the detailed ranking differs from the rough pass. End with a
**Operator decision required** block: the detailed recommendation and the decision
owed. Workspace voice applies (no em dashes, no emojis, ranges over false
precision, cite sources inline).

## See also

- `../../SKILL.md` - the core RICE skill that produces the shortlist.
- `../../references/rice-methodology.md` - scales, formula, and the DRICE row in the variants table.
- `../../scripts/README.md` - calculator I/O (DRICE uses the same arithmetic with more detailed inputs; invoke it via `${CLAUDE_SKILL_DIR}/scripts/rice_score.py`).
