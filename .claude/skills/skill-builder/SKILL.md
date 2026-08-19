---
name: skill-builder
description: >-
  Author, refactor, or split a skill so it is atomic, composable, auto-invocable, and
  progressively disclosed. Use whenever creating a new skill, reviewing or refactoring an
  existing one, deciding whether something should be a skill versus a CLAUDE.md note, a
  rule, a subagent, or a command, or when a skill is not firing when it should. Do NOT use
  for harness config such as settings.json (use `update-config`) or for the theory of
  writing agent-facing prose (use `writing-for-agents`).
---

<!-- Vendored from https://github.com/spencermarx/anthony-and-spencer-business-workspace (.claude/skills/skill-builder/SKILL.md @ 2e62970bb6cd); adapted for this repo (merged with the description-optimisation loop and anti-undertriggering guidance from Anthropic's skill-creator, and with the rules layer added to the primitive decision table; the deep reference now defers to the vendored writing-for-agents rather than restating it). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->

# skill-builder

## The five rules

1. **Atomic.** One skill does one thing. A skill that does five is reusable by
   none.
2. **Composable.** If logic already lives in another skill, call it rather than
   reimplementing it. Declare the dependency as a markdown link to that skill's
   `SKILL.md`, so a reference to a skill that does not exist reads as a dead
   link rather than as prose.
3. **Auto-invocable.** The description is the whole dispatch mechanism. There is
   no router skill. See below.
4. **Progressively disclosed.** `SKILL.md` stays lean. Depth goes in
   `references/` and `sub-skills/`, which load only when linked and read.
5. **Colocated and deterministic.** Scripts live inside the skill that owns them,
   invoked through `${CLAUDE_SKILL_DIR}`. Use a script for anything mechanical and
   reserve the model for judgment.

## First, is this a skill at all?

The highest-leverage question, and the one most often skipped.

| Need | Primitive |
|---|---|
| A fact agents should know when working in an area | a `CLAUDE.md` note in that folder |
| A convention that governs a file type | a `Standards/` section plus a `.claude/rules/` pointer |
| A repeatable multi-step procedure | a skill |
| A procedure only a person should trigger | a skill with `disable-model-invocation: true` |
| Context isolation, or a tool surface the main agent must not have | a subagent |
| A deterministic action, especially one taking arguments | a command |

The row people miss is the second. If what you are writing is "always do X when
touching Y", it is a standard with a rule, not a skill, and putting it in a skill
means it fires only when something else remembered to invoke it.

## Writing the description

Under-triggering is the dominant failure mode. A skill that never fires is worse
than one that fires slightly too often, because its absence is silent.

- Third person, at most 500 characters, target 350.
- Open with the capability, then the triggers **in the words a person actually
  types**, not the concept those words are an instance of.
- **Be pushy.** "Use whenever...", "Invoke before...", "Always use when...".
  Never "Can be used for...".
- **Negative routing is mandatory** where a sibling could plausibly capture the
  same trigger: "Do NOT use for X, use `sibling` instead." This is what makes a
  library of thirty skills dispatch correctly without a router.
- Backtick every skill name you mention, so a reader can resolve it.

If a skill is not firing, the description is nearly always the cause, not the
body. Rewrite the triggers before touching anything else.

## Structure

```
skills/<name>/SKILL.md              the only registrable file
skills/<name>/sub-skills/<name>.md  flat, never a nested directory
skills/<name>/references/<name>.md  depth, loaded on demand
skills/<name>/scripts/              deterministic helpers
```

Sub-skills are flat files. A nested `SKILL.md` risks registering as a top-level
skill, which spends the always-resident budget on something that should be
invisible until needed.

## Procedure

1. **Check the table above.** If it is not a skill, stop and build the right
   thing instead.
2. **Check for an existing skill** that already covers it, or that this should
   extend. Two skills competing for one trigger is worse than either alone.
3. **Write the description first.** It is the hardest part and it determines
   whether anything else you write is ever read.
4. **Write the procedure**, with each step ending on a condition that can be
   observed to be true or false. "Review the document" cannot fail; "list every
   claim with no inline citation" can.
5. **Push depth out.** Anything long, reference-heavy, or needed in only one
   scenario goes to `references/` or `sub-skills/` with a link.
6. **Re-read the layout, the budgets, and every skill reference you made**
   against [harness-standards](../../../Standards/harness-standards.md).
7. **Self-review against the five rules**, then against the anti-patterns below.

## Anti-patterns

- **A description that describes the skill instead of its triggers.** The reader
  is a dispatcher, not a browser.
- **Restating a standard inside a skill.** Link the `Standards/` section. Two
  copies diverge.
- **A skill that is really a rule**, so it only fires when someone remembers it.
- **Prohibitions instead of instructions.** Prompt the positive: "write the owner
  on every action item", not "don't forget the owner". See
  [`writing-for-agents`](../writing-for-agents/SKILL.md), which covers the
  underlying theory and is worth reading in full once.
- **A 500-line SKILL.md.** If triggering the skill is expensive, it will be
  avoided.

## Going deeper

[`writing-for-agents`](../writing-for-agents/SKILL.md) holds the theory this
skill applies: context pointers, the two loads, the information hierarchy,
completion criteria, and pruning. The budgets are in
[harness-standards § Context budget](../../../Standards/harness-standards.md#context-budget).
