---
name: writing-for-agents
description: >-
  The craft of writing documents agents read: skill descriptions, CLAUDE.md files, rules,
  and reference material. Covers context pointers, the two loads, progressive disclosure,
  completion criteria, leading words, and pruning. Use WHENEVER creating or editing a
  skill, a rule, or any CLAUDE.md, and before deciding what belongs in context versus
  behind a pointer. Do NOT use for prose a human will read (use `conveying-clearly`) or
  for marketing copy (use `seven-copy-critics`).
---

<!-- Vendored from https://github.com/mattpocock/skills (skills/productivity/writing-for-agents/SKILL.md @ 9c9f36ccd399); adapted for this repo (the 11 KB upstream body exceeds this workspace's skill-body budget, so it is kept verbatim in references/theory.md and this file is a lean router into it; SKILL-MECHANICS.md kept verbatim as references/skill-mechanics.md; a section added mapping the concepts onto this workspace's own layers). MIT, Copyright (c) 2026 Matt Pocock; see THIRD-PARTY-NOTICES.md. See [vendoring provenance](../../../Standards/harness-standards.md#vendoring-provenance). -->

# Writing for agents

A skill description, a line in a `CLAUDE.md`, and a rule's `paths:` glob are the
same object: a **context pointer**. Each names material that is out of context
and states the condition for reaching it. The pointer's wording, not its target,
decides whether it is reached.

That single idea is why this workspace spends so much care on descriptions and so
little on routers.

## Read this before

- Writing or editing any `SKILL.md`, especially its `description`.
- Writing or editing a `CLAUDE.md` at any tier.
- Adding a `Standards/` section or a `.claude/rules/` pointer.
- Deciding whether something belongs inline or behind a link.

## The material

- **[references/theory.md](references/theory.md)** is the full treatment:
  context pointers, the two loads, the information hierarchy, completion
  criteria, leading words, negation, and pruning. Read it in full the first time.
- **[references/skill-mechanics.md](references/skill-mechanics.md)** covers the
  skill-specific branch: model-invoked versus user-invoked, splitting by
  invocation, and router skills.

## How it maps onto this workspace

The upstream is tool-agnostic. Here the concepts land on specific layers:

| Concept | Where it lives here |
|---|---|
| Context pointer | a skill `description`, a rule's `paths:` glob, a `\| File \| When to load \|` row |
| Context load | the always-resident budget: descriptions, plus every `CLAUDE.md` on the path |
| Cognitive load | the `Standards/README.md` registry, which a human has to know exists |
| Progressive disclosure | `sub-skills/`, `references/`, and rules that load on demand |
| Co-location | scripts colocated in the skill that owns them |
| Sediment | a `CLAUDE.md` section nobody has pruned; see the "What's pending" rule |
| No-ops | instructions the model already follows by default. Delete the sentence |

The budgets that make this concrete are in
[harness-standards § Context budget](../../../Standards/harness-standards.md#context-budget).

## The one rule to carry away

**Prompt the positive, never the prohibition.** "Write the owner and the date on
every action item" works. "Don't forget the owner" does not, and reliably
produces the thing it names. Negation is the most common failure in this
workspace's own history of writing rules.
