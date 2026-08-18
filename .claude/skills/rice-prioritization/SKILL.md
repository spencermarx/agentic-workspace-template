---
name: rice-prioritization
description: >-
  Score and rank a backlog with the RICE model (Reach x Impact x Confidence / Effort). Use
  whenever there is a shortlist to prioritize quantitatively, a roadmap-ordering debate,
  or a request to compare initiatives on impact per effort. Produces a ranked,
  sensitivity-checked artifact ending in a decision block. Do NOT use for a single go/no-
  go (use `strategic-brief`) or to make the call itself.
---

# RICE Prioritization

Scores and ranks a candidate list with RICE: `(Reach x Impact x Confidence) /
Effort`. One repeatable task. The output is a relative ranking plus a sensitivity
read and a operator decision block, never a committed roadmap.

**The governing principle: RICE produces better numbers to argue about, it does
not remove the argument.** The skill surfaces a defensible ranking; the operators
decide. A high score never auto-greenlights a project that fails the strategy.

**Agent boundary (load-bearing in autonomous mode).** An agent may draft Reach
from real data and structure a Confidence evidence tier. It must NOT invent Reach
when no data exists, and it must NOT self-assign Effort or strategic Impact:
those depend on the codebase, team, and goals the model cannot see. Mark them
`NEEDS-HUMAN` and proceed with a clearly-flagged draft. Full boundary table in
`references/rice-methodology.md`.

## When to use

- A backlog or shortlist of features/initiatives needs ranking against one goal.
- A roadmap-ordering debate where "impact per effort" is the right lens.
- Comparing candidates that differ in how many users they reach (RICE's edge over ICE).

## When NOT to use

- A single initiative go/no-go with no list to rank -> `strategic-brief`.
- CEO-level review of one initiative across many dimensions -> `ceo-review`.
- A operator's personal weekly priorities -> `player-coach`.
- Foundational/tech-debt/market-timing work that always scores low -> carve a strategic lane instead (see methodology "When RICE is NOT the right tool").
- The final build commitment -> that is always a human call.

## Procedure

### Step 1 - Frame the round

Establish, and write down, the four constants before any scoring:

- **Goal/metric.** The single goal candidates are scored against (e.g. activation, retention, revenue).
- **Candidate list.** The items to rank. If the user has not supplied one, ask. Do not invent candidates.
- **Reach time window.** One window for the entire round (e.g. per quarter). Locked here, used for every item.
- **Context/venture.** Which venture this serves, for the output path.

Then pick the **mode**:

| Mode | Use when | What the agent does |
|---|---|---|
| **Autonomous** | Fast draft wanted; some data exists; human will review later | Drafts all four factors with an evidence flag per number; marks Effort and strategic Impact `NEEDS-HUMAN`; never invents Reach |
| **Facilitated** | A human or group is scoring live | Runs the session from `references/facilitation-guide.md`; elicits and records human scores |
| **Hybrid** | A human is available but wants a head start | Pre-fills an autonomous draft, then walks the human through confirm/adjust per factor |

Default to Hybrid when a human is in the loop; Autonomous when asked to produce a draft alone.

### Step 2 - Calibrate the scales

Before scoring, anchor Impact and Confidence against ~3 already-shipped features
the team knows. This is the single highest-leverage move against scale drift.

- Facilitated/Hybrid: do this with the human, using the calibration section of `references/facilitation-guide.md`.
- Autonomous: state the anchors explicitly in the output ("I am treating [known feature] as Impact 2 / Confidence 80%") so the human can correct the frame.

### Step 3 - Score each candidate

Score every candidate on all four factors, sourced not guessed, using the exact
scales in `references/rice-methodology.md` (Impact `3/2/1/0.5/0.25`; Confidence
`100/80/50%`; Effort in person-months across ALL disciplines; Reach an absolute
count in the locked window).

Per mode:
- **Autonomous** - draft each number with an evidence flag (`data` / `some-data` / `assumption`). Mark Effort and strategic Impact `NEEDS-HUMAN`. Attach a `reach_source` note to every Reach number. If no data supports a Reach figure, say so; do not fabricate one.
- **Facilitated** - elicit scores via the per-factor question bank in the facilitation guide; record who supplied each.
- **Hybrid** - present the draft, then confirm/adjust each factor with the human via the question bank.

Carry provenance (evidence flag, reach source, NEEDS-HUMAN markers, notes)
alongside each candidate; the calculator passes these through untouched.

### Step 4 - Compute

Write the scored candidates to a JSON list and run the deterministic calculator.
Do not hand-compute scores or ranks.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/rice_score.py /path/to/candidates.json
# add --format table for a quick read
```

Input shape and output fields are documented in `scripts/README.md`. The script
returns each candidate's `rice_score` and `rank`, the near-tie groups
(`tie_group`, default within 15%), and `sensitivity` for adjacent pairs (what
confidence would flip the order). The script errors loudly on a bad scale value;
fix the input rather than working around it.

### Step 5 - Adversarial challenge pass

Before presenting, pressure-test the scores against the three known gaming
vectors. Spawn three critics in parallel (one focused prompt each); pattern
borrowed from `player-coach/sub-skills/priority-check`:

- **Reach Inflator** - challenges Reach numbers: cherry-picked analytics view, wrong window, counting affected-not-active, unqualified segments.
- **Confidence Optimist** - challenges Confidence: any 80-100% riding on a gut estimate, confidence not tied to evidence.
- **Effort Underestimator** - challenges Effort: dev-only counts, missing disciplines, no buffer, linear-headcount assumptions.

Each returns the specific rows it disputes and why. Record what was challenged
and what changed. If any score moves, re-run Step 4. Keep the challenge record
for the artifact; never bury unresolved dissent.

For a small or low-stakes list, a single inline self-challenge against the three
vectors is acceptable instead of three subagents. Scale the rigor to the stakes.

### Step 6 - Present and write the artifact

Fill `templates/rice-analysis.md` and write it to the venture's activities
folder:

`Clients/<venture>/Activities/<YYYY-MM-DD> RICE Prioritization - <subject>/00-summary.md`

Default to `Clients/example-co/...` given current workspace state; ask
for venture/subject if not obvious. Never hardcode a single path.

The artifact includes: the round's constants, the mode and calibration anchors,
the ranked scoring table (with evidence/source per Reach), near-ties and
sensitivity, quick-wins grouped by effort, the adversarial challenge record, the
assumptions/open-questions log, and a **Operator decision required** block that
surfaces the ranking and a recommendation but does not decide. Workspace voice
applies: no em dashes, no emojis, ranges over false precision, `[[wikilinks]]`
for entities, namespaced inline tags.

## Extending this skill

- `sub-skills/drice-deep-dive` - after RICE produces a top 3-5, refine those with detailed `$X annualized revenue` estimates (Lenny Rachitsky's DRICE). Use when the top candidates are high-stakes enough to warrant a 30-minute estimate over a 30-second one.

## Composition

- Feeds `strategic-brief` for a deep go/no-go on the top-ranked item.
- The ranking can be an input to `ceo-review` when one initiative needs fuller scrutiny.
- `player-coach` can absorb the ranking when a operator's weekly priorities need to reflect it.

## See also

- `references/rice-methodology.md` - exact scales, formula, worked examples, pitfalls, when-not-to-use, variants, agent boundaries.
- `references/facilitation-guide.md` - workshop flow, per-factor question bank, calibration, disagreement handling.
- `scripts/rice_score.py` and `scripts/README.md` - the deterministic calculator and its I/O contract.
- `templates/rice-analysis.md` - the output artifact skeleton.
