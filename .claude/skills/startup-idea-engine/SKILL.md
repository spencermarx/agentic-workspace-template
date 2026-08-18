---
name: startup-idea-engine
description: >-
  Generate, test, validate, and document startup ideas using Paul Graham's framework plus
  a tarpit-idea warning lens. Five stages: noticing, framework tests, research validation,
  adversarial review, and a written output. Runs autonomously, collaboratively, or step by
  step. Use whenever a new business idea needs stress-testing before anyone commits time
  to it.
---
<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/startup-idea-engine/SKILL.md @ 496d37273aca); adapted for this repo (de-branded throughout; the incumbent-vendor examples generalised; the task-source dependency removed). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Startup Idea Engine

A structured ideation engine that applies Paul Graham's canonical "How to Get Startup Ideas" framework - augmented by Dalton Caldwell + Michael Seibel's tarpit-ideas warning lens - to generate, test, research-validate, and document startup ideas. Inspired by Garry Tan's [gstack `/office-hours`](https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md) skill (the multi-phase diagnostic with adversarial review pattern).

**Core insight from PG's framework:** good startup ideas are *noticed* from the leading edge, not *thought up* in the abstract. Plausible-sounding ideas are statistically more likely to fail than implausible-sounding ones. The most dangerous failure mode is the "sitcom idea" - invented through abstract category-search, validated by friends saying "maybe I'd use that," failing in real adoption.

**Core insight from Dalton/Michael:** first-time founders cluster on tarpit ideas - patterns that look attractive and that a generation of failed attempts has already established do not work. The framework must explicitly catch these.

This skill is designed against those failure modes specifically.

## When to Use

- Retreat-style ideation sessions where the goal is 3–5 well-formed candidate ideas
- Wedge generation for an existing platform topology / founder shape
- Long-arc vision exploration paired with near-term wedge selection
- Pivot evaluation when an existing product is failing to find product-market fit
- Any structured "I need to find a real startup idea" session
- After a customer loss / category death / strategic reset that demands a new direction

## When NOT to Use

- For idea *evaluation* of a single existing idea → use `strategic-brief` (pre-commitment demand validation) or `ceo-review` (structured plan review)
- For *content* idea generation → use `content-idea-capture`
- For tactical execution planning of a chosen idea → use `strategic-brief` then a the task source issue
- For brand / creative review → use `brand-review` or `seven-copy-critics`
- When the user already knows the idea and wants implementation help → file a the task source issue

## Agents

**Primary:** Founder, CEO, CTO, or any operator running an ideation cycle.

**Delegates to:** `Explore` sub-agents for parallel context build; `general-purpose` sub-agents for adversarial critic review and per-candidate research; `WebSearch` and `WebFetch` for landscape research.

---

## Ground rules and modes

In [references/ground-rules.md](references/ground-rules.md), together with the
three operating modes (autonomous, collaborative, step by step). Read it at the
start of a session. The rules apply throughout and are not repeated per stage.

## Procedure

Five stages, in [references/procedure.md](references/procedure.md). Each has a
sub-skill carrying its detail:

| Stage | Sub-skill |
|---|---|
| 1. Noticing | [`01-noticing`](sub-skills/01-noticing.md) |
| 2. Framework tests | [`02-framework-tests`](sub-skills/02-framework-tests.md) |
| 3. Research validation | [`03-research-validation`](sub-skills/03-research-validation.md) |
| 4. Adversarial review | [`04-adversarial-review`](sub-skills/04-adversarial-review.md) |
| 5. Output | [`05-output-write`](sub-skills/05-output-write.md) |

Load the spine first, then each sub-skill as you reach its stage. Do not skip
stage 4: an idea that has not been attacked has not been tested.

## Output convention

Where the written idea lands, and the voice it is written in, are in
[references/output-convention.md](references/output-convention.md). Load it at
stage 5, not before.

## Extending This Skill

To add a new sub-skill or specialized scenario:

1. Create `sub-skills/{NN-scenario}.md` following the same phase structure: Inputs → Procedure → Outputs → Mode Behavior.
2. Update the SKILL.md procedure to reference it from the appropriate phase.
3. The adversarial review phase is **required** - do not bypass it for shortcut scenarios.
4. New tarpit patterns observed in production go into `references/dalton-michael-tarpits.md` with date and observed-failure context.
5. New procedures for noticing (e.g., a domain-specific generation lens) go into `sub-skills/01-noticing.md` as additional procedures, not as separate sub-skills.

---

## Sources

- Paul Graham, "How to Get Startup Ideas" (2012) - `https://www.paulgraham.com/startupideas.html`
- Y Combinator Startup Library entry - `https://www.ycombinator.com/library/8z-how-to-get-startup-ideas`
- Dalton Caldwell + Michael Seibel, "Where do great startup ideas come from?" - `https://www.ycombinator.com/library/DU-dalton-michael-where-do-great-startup-ideas-come-from`
- Garry Tan, gstack `/office-hours` SKILL.md - `https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md`
- Y Combinator Requests for Startups (current) - `https://www.ycombinator.com/rfs`
