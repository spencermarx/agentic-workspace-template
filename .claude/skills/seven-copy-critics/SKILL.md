---
name: seven-copy-critics
description: >-
  Adversarial copy review that stress-tests marketing copy through seven hostile reader
  personas across three failure layers, 21 checks. Catches weak hooks, generic phrasing,
  unsubstantiated claims, AI tells, and abstraction. Produces a failure report, a
  tightened rebuild, and a changelog. Use before sending cold email, publishing a page, or
  scheduling a post. Do NOT use to write copy from scratch; this reviews drafts only.
---
<!-- Vendored from https://github.com/spencermarx/anthony-and-spencer-business-workspace (.claude/skills/seven-copy-critics/SKILL.md @ 2e62970bb6cd); adapted for this repo (placeholder org name removed). See [vendoring provenance](../../../Standards/harness-standards.md#vendoring-provenance). -->


# Seven Copy Critics

An adversarial pre-publication review that runs marketing copy through 7 hostile
reader personas, each attacking the draft at 3 failure layers. The author of a
piece of copy is the worst person to review it: they know the context, they are
already bought in, and they cannot see what a cold reader sees. This skill
simulates 7 cold readers having 7 bad days.

Adapted from Simon Severino's [Seven Critics framework](https://github.com/SimonTheSalesBooster/sevencritics).

## When to Use

- Before sending any cold outbound email or sequence
- Before publishing a landing page, ad, or newsletter
- Before scheduling any organic social post that matters (especially the operator LinkedIn)
- Before publishing a blog post
- When copy "feels right" but is not converting
- When AI-assisted drafts read too polished or templated

## When NOT to Use

- To write copy from scratch - this is a review tool, not a writing tool
- On copy that is already converting - do not fix what is not broken
- For pre-launch strategic review of an entire campaign brief - use `campaign-brief` instead
- For visual or design review of marketing assets - use `brand-review` instead
- For one-off internal messages with no audience consequence

## Agents

**Primary:** CMO

---

## Procedure

### Step 1 - Gather Context

Before running the critics, collect:

1. **The draft copy** (full text, exactly as it would be sent)
2. **The target audience** (specific persona, role, situation - not "marketers" or "operators")
3. **The channel and format** (cold email, LinkedIn post, landing page hero, blog intro, etc.)
4. **The desired action** (reply, click, book a call, share, subscribe)

If any of these are missing, ask for them before proceeding. A review without
audience context produces generic feedback.

---

### Step 2: run all 7 critics across all 3 failure layers

The full matrix is in [references/critic-matrix.md](references/critic-matrix.md).
Load it now and work through it. Twenty-one checks: seven personas, each
applied at the hook, the body, and the close.

Run every check. A critic that finds nothing is a finding in itself, and
skipping one because the copy "obviously passes" is how the failure this
skill exists to catch survives review.

### Step 3 - Compile the Failure Report

Categorize every failure surfaced in Step 2 by severity. Use this exact format:

```markdown
## FAILURE REPORT

### CRITICAL - [n] failures
(blocks the desired action; copy cannot ship as-is)
- [Critic #] [Layer]: [one-line description]
- ...

### HIGH PRIORITY - [n] failures
(meaningfully weakens the copy; should be fixed before publishing)
- ...

### LOW - [n] failures
(minor polish; address if cheap, otherwise note and move on)
- ...
```

**Severity rules:**
- **CRITICAL:** Any First Impression failure on Critic 1 (Time-Crushed) or
  Critic 4 (AI-Allergic). Any Action layer failure on the dominant target
  persona. Any Trust failure on Critic 3 (Burned Skeptic) when the copy makes
  a quantitative claim.
- **HIGH PRIORITY:** Any failure on a layer that directly opposes the desired
  action (e.g., Visual Reader failures on a story-driven post).
- **LOW:** Cosmetic patterns, minor word choice, second-order trust dings.

---

### Step 4 - Rebuild

Rewrite the draft addressing every CRITICAL and HIGH PRIORITY failure. The
rebuild standard is **tighter, not bigger. Sharper, not different.**

If the rebuild reads like a different person wrote it, the review failed.
The rebuild must:

1. Preserve the author's voice and core message
2. Fix root causes, not just symptoms
3. Not introduce new failures across other critics (re-check mentally)
4. Be the same length or shorter than the original
5. Comply with house style: **no em dashes** (per CMO feedback memory), no
   recap-style follow-up phrasing, dream outcome leads, mechanism explains

Output the full rebuilt copy in a fenced block, ready to copy-paste.

---

### Step 5 - Validation Pass

Before declaring done, mentally walk all 7 critics through the rebuilt version
one more time. For each critic, write a single line:

```markdown
## VALIDATION PASS
1. Time-Crushed: PASS / FAIL - [one-line reason]
2. Self-Conscious: PASS / FAIL - [one-line reason]
3. Burned Skeptic: PASS / FAIL - [one-line reason]
4. AI-Allergic: PASS / FAIL - [one-line reason]
5. Lurker: PASS / FAIL - [one-line reason]
6. Visual Reader: PASS / FAIL - [one-line reason]
7. Inspiration Seeker: PASS / FAIL - [one-line reason]
8. Operator-Voice Detector: PASS / FAIL - [one-line reason]
```

If any critic still fails, return to Step 4 and rebuild again. **Do not ship
copy with any remaining CRITICAL failure.** A maximum of 2 rebuild rounds - if the third pass still fails, the underlying message itself is wrong and
the copy needs to be rethought from the audience or offer angle, not rewritten.

---

### Step 6 - Changelog

End the review with a "What Changed" section explaining each meaningful edit
and which critic's failure it addressed:

```markdown
## WHAT CHANGED
- [Original phrase] → [new phrase] - fixes Critic [#] [Layer]
- ...
```

This is non-negotiable. The author needs to see the fixes mapped to root causes
so the same patterns do not reappear in the next draft.

---

## Output template

In [references/output-template.md](references/output-template.md). Load it
before writing the report.

## House Style Constraints

The rebuilt copy MUST comply with the CMO feedback memory:

- **No em dashes anywhere.** Restructure with periods, commas, or colons.
- **No recapping the recipient's own business** in follow-up emails. Reference
  shared ideas or next steps instead.
- **No parroting call notes.** Focus on what is next, not what was said.
- **Dream outcome leads, mechanism explains.** Lead with what the customer
  gets (more bookings, less churn), not how the product works.
- **Literal-first imagery.** If the copy references visuals, they must depict
  specific moments from the post content, not abstract metaphors.
- **Author conviction required.** If the original draft is from the operator, the
  rebuilt copy must contain at least one sentence expressing a personal belief,
  opinion, or conviction. Information-only posts that never take a position fail
  the validation pass regardless of how the other critics score it.

A rebuild that violates any of these is an automatic FAIL on the validation
pass, regardless of how the critics score it.

---

## Key Principle

> If the rebuilt version reads like a different person wrote it, the review
> failed. Tighter, not bigger. Sharper, not different.

The goal is not a "better" version of the copy in the abstract. The goal is
the same author's same message, stripped of the failure modes a cold reader
would catch. Voice preservation is a hard constraint, not a nice-to-have.
