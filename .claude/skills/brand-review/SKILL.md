---
name: brand-review
description: >-
  Structured design audit for any marketing or product asset: landing pages, social
  graphics, email templates, ad creatives. Rates each across 7 dimensions 0-10, separates
  mechanical fixes from design judgment calls, and produces a scorecard plus a prioritized
  fix list. Use before publishing any marketing creative. Do NOT use for copy quality (use
  `seven-copy-critics`) or for the strategic case (use `strategic-brief`).
---
<!-- Vendored from https://github.com/spencermarx/anthony-and-spencer-business-workspace (.claude/skills/brand-review/SKILL.md @ 2e62970bb6cd); adapted for this repo (no changes beyond this marker). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Brand Review

A structured design audit that produces dimension-based ratings and a prioritized fix list
for any marketing or product asset before it's published.
Based on Garry Tan's [gstack `/design-review` + `/plan-design-review`](https://github.com/garrytan/gstack).

**Core insight from gstack:** The common failure mode in design review is mixing
"this button is the wrong color" (mechanical fix) with "I'm not sure about the overall
aesthetic" (judgment call). Conflating these produces confused feedback that's hard to act on.
This skill separates them explicitly - mechanical fixes are non-negotiable; judgment calls
require discussion.

## When to Use

- Before publishing any social graphic, ad creative, or campaign visual
- Before launching or updating a landing page
- When reviewing email template designs
- When evaluating a new brand direction or asset set

## When NOT to Use

- For copy/messaging review - use `campaign-brief` for campaign messaging QA
- For strategic brand direction decisions - use `ceo-review`
- For rough drafts that aren't yet ready for critique - flag as draft and review when ready

## Agents

**Primary:** CMO, Producer

---

## Procedure

### Step 1 - Identify the Asset

Describe the asset being reviewed:
- Asset type (social graphic, landing page, email, ad, etc.)
- Platform/destination (LinkedIn, website, email client, etc.)
- Intended audience
- Campaign or context it belongs to

If reviewing multiple assets in a set (e.g., a 3-post LinkedIn carousel), review each
individually on the scorecard, then add a set-level coherence note.

---

### Step 2 - Score Across 7 Dimensions (0–10)

Rate each dimension with a score and a 2–4 sentence rationale. Be honest - a 7 is not a gift; a 4 is not a punishment. The score must reflect the actual quality.

**Scoring guide:**
- 9–10: Exceptional. Would use as a reference example.
- 7–8: Strong. Minor polish needed.
- 5–6: Acceptable. Clear room for improvement; specific fixes needed.
- 3–4: Weak. Significant issues that will hurt performance.
- 1–2: Broken. Fundamental problems that must be resolved before any use.

---

**Dimension 1: Visual Hierarchy (0–10)**

Is the eye drawn in the right sequence? Does the primary message land first?
Is the reading order: headline → supporting point → CTA? Or does the layout fight itself?

Questions to answer:
- What's the first thing a viewer's eye goes to? Should it be?
- Is the headline visually dominant, or is it competing with imagery?
- Does the layout guide the viewer to the CTA, or do they have to hunt for it?

---

**Dimension 2: Brand Consistency (0–10)**

Does this feel like us? Are font, color, voice, and imagery choices aligned with the brand guide?

Questions to answer:
- Are the correct brand fonts being used?
- Are the colors within the brand palette, or are there off-brand additions?
- Does the imagery style match our established aesthetic?
- Would someone familiar with our brand immediately recognize this as ours?

---

**Dimension 3: Message Clarity (0–10)**

Can you extract the core value proposition in under 5 seconds?

Questions to answer:
- Cover the logo - can you still tell what this is for?
- What does a first-time viewer take away in 5 seconds?
- Is the benefit stated explicitly, or does the viewer have to infer it?

---

**Dimension 4: Emotional Resonance (0–10)**

Does the asset evoke the right emotion - professional, trustworthy, bold, warm - whichever
is appropriate for this context?

Questions to answer:
- What feeling does the visual design communicate before any text is read?
- Is that the right feeling for this audience and message?
- Does the visual tone match the copy tone?

---

**Dimension 5: Call to Action (0–10)**

Is the CTA specific, visible, and compelling?

Questions to answer:
- Is there a clear CTA? (If not, score is 1–2 automatically.)
- Is the CTA specific ("Book a 20-min demo" vs. "Learn more")?
- Is it visually prominent - can a viewer identify it without searching?
- Does the CTA match the asset's goal (awareness vs. conversion vs. nurture)?

---

**Dimension 6: Platform Fit (0–10)**

Does the format, ratio, and length match where this asset will be seen?

Questions to answer:
- Is the aspect ratio correct for the platform (LinkedIn 1:1 or 1.91:1, Story 9:16, etc.)?
- Is text legible at the size it'll be rendered (mobile vs. desktop)?
- For email: is it designed for clients that block images by default?
- Would this look correct in a native feed scroll without cropping?

---

**Dimension 7: Distinctiveness (0–10)**

Does this stand out from generic competitors, or could any SaaS company's logo replace ours?

Questions to answer:
- What is the one distinctive element that makes this unmistakably ours?
- If we swapped our logo for a competitor's logo, would the asset still feel ours?
- Is there a design choice here that a competitor would not make? Should there be?

---

### Step 3 - Separate Mechanical Fixes from Judgment Calls

**Mechanical fixes** are objectively incorrect and must be resolved before publishing.
No discussion needed - fix them.

Examples:
- Wrong brand color used (#FF0000 instead of #CC2200)
- Off-brand font applied to headline
- Text is not legible at mobile size (fails accessibility or readability test)
- Aspect ratio is wrong for the platform
- CTA button is missing or hidden below the fold

**Design judgment calls** are subjective choices that may be correct depending on strategic
context. These require discussion before changing.

Examples:
- Layout feels dense vs. airy - is this intentional?
- Image choice feels bold - is that aligned with the tone goal for this campaign?
- Headline is unconventional - is this a calculated risk or an oversight?

List each category separately with specific items.

---

### Step 4 - Scorecard and Fix List

Produce a clean summary:

```markdown
## Brand Review Scorecard

| Dimension | Score | Notes |
|---|---|---|
| Visual hierarchy | X/10 | [one line] |
| Brand consistency | X/10 | [one line] |
| Message clarity | X/10 | [one line] |
| Emotional resonance | X/10 | [one line] |
| Call to action | X/10 | [one line] |
| Platform fit | X/10 | [one line] |
| Distinctiveness | X/10 | [one line] |
| **Overall** | X/10 | |

## Mechanical Fixes (must resolve before publishing)
1. [Fix]
2. [Fix]

## Design Judgment Calls (discuss before changing)
1. [Observation + question]
2. [Observation + question]

## Priority Fix List (top 3 highest-impact changes)
1. [Fix with expected impact]
2. [Fix with expected impact]
3. [Fix with expected impact]
```

An **overall score of 7+** is publishable with mechanical fixes resolved.
A **score of 5–6** requires at least the top-3 priority fixes before publishing.
A **score below 5** should go back to production for a significant rework.
