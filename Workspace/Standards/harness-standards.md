# Harness standards

How the agentic side of the workspace is built: skills, rules, agents,
commands, settings, and the context budget that governs all of them.

## The two-artifact invariant

A standard exists as two synchronized things.

1. **Statement.** One `##` section in a `Workspace/Standards/*.md` document. This is the
   single source of truth. It is stated here and nowhere else.
2. **Router.** One `.claude/rules/<domain>/<slug>.md` file: a `paths:` glob plus
   a deep link to the section above. It never restates the rule.

A doc section that no rule routes is dead. A rule whose link does not resolve is
broken.

The reason this is not a `CLAUDE.md` section: a `CLAUDE.md` governs a directory
subtree, not a file type, and it does not reliably reach subagents. A rule
governs a file type wherever it lives, and loads for subagents too.

Drift here is silent. Nothing reports at read time that a rule failed to load,
so a renamed heading or a glob that matches nothing simply stops routing, and
the system reads as healthy. Whoever renames a heading rewrites the pointers
that aim at it, in the same change.

## Rule authoring contract

A rule file has **exactly two frontmatter keys**, in this order: `description`
and `paths`. A third key means the rule is doing more than routing.

The body is a heading and one or two link lines. If a rule contains an
imperative outside a link line, it has stopped being a pointer and started being
a second copy of the standard.

Size cap: 1,200 bytes. `.claude/rules/writing/house-voice.md` is capped at 400,
because it fires on every markdown read. **If house voice needs more surface it
splits into narrower globs. It never grows.** This is the one place where the
mechanism built to solve the always-on budget problem could recreate it.

Keep glob syntax to `**`, `*`, `?`, and `[abc]`. No braces, no negation, no
extended globs. Claude Code does this matching, not anything in this repo, so a
pattern that reaches too far just matches nothing, which is indistinguishable
from a healthy system.

Globs use [the reserved folder vocabulary](vault-standards.md#the-reserved-folder-vocabulary)
and are written as `**/<Folder>/**/*.md`, so they match wherever the folder is
nested. Renaming a reserved folder obligates you to rewrite the affected globs
in the same change, because a glob that matches nothing stops routing without
saying so.

## Skill authoring contract

Layout, and only this layout:

```
.claude/skills/<name>/SKILL.md              the only registrable file
.claude/skills/<name>/sub-skills/<name>.md  flat, never a nested directory
.claude/skills/<name>/references/<name>.md  depth, loaded on demand
.claude/skills/<name>/scripts/<name>.{sh,mjs,py}
.claude/skills/_stubs/<name>.md             not a skill until promoted
```

Sub-skills are flat files. A nested `SKILL.md` risks auto-registration into the
always-resident description budget, which is the budget that decides whether any
skill fires at all.

**The description is the dispatch mechanism.** There is no router skill and
there will not be one. Therefore:

- Third person, at most 500 characters, target 350.
- Open with the capability, then the triggers in the words a person actually
  types, not the concept they are an instance of.
- **Be pushy.** Under-triggering is the dominant failure mode: a skill that
  never fires is worse than one that fires slightly too often. Write "Use
  whenever...", "Invoke before...", "Always use when...". Never "Can be used
  for...".
- **Negative routing is mandatory** where a sibling skill could plausibly
  capture the same trigger: "Do NOT use for X, use `sibling` instead."
- Every skill name mentioned anywhere is backticked and, where it is a real
  dependency, written as a markdown link to that skill's `SKILL.md`. Declaring
  dependencies as links is what makes a dependency on a skill that never
  existed visible as a dead link rather than as silence.

## Picking the primitive

| Need | Primitive |
|---|---|
| A fact agents should know when working in an area | a `CLAUDE.md` note in that folder |
| A convention that governs a file type | a `Workspace/Standards/` section plus a rule |
| A repeatable multi-step procedure | a skill |
| A procedure only a human should trigger | a skill with model invocation disabled |
| Context isolation or a restricted tool surface | a subagent |
| A deterministic action taking arguments | a command |

A subagent earns its place only when it needs a tool surface the main agent
cannot have, or a context window the main agent cannot afford to spend.

## Context budget

Three tiers of cost, and only the third is cheap.

1. **Always loaded:** every skill's name and description. This is the budget
   that decides whether a skill fires.
2. **Loaded on trigger:** a skill's whole `SKILL.md` body, for the rest of the
   session.
3. **Loaded on demand:** `sub-skills/`, `references/`, and files a rule points
   at. Depth belongs here.

| Artifact | Cap |
|---|---|
| One description | 500 chars |
| `SKILL.md` body | 8,000 B, target 5,000 |
| One rule | 1,200 B |

**There is no cap on the combined size of all descriptions.** There was one, at
14,000 B, and it was retired deliberately: it measured cost rather than quality,
nothing degrades at 14,001, and a library grows because its coverage is worth
having. A number nobody intends to honour is worse than no number, because every
session reads it as a constraint and proposes cuts against it.

The per-description cap stays, and it is the one that matters. A bloated
description dilutes its own triggers, so the skill fires less often -- which is
a real failure, not an estimated one.

`CLAUDE.md` sizes live in
[claude-md-contract § The three tiers](claude-md-contract.md#the-three-tiers),
which owns the tiers and therefore owns their budgets.

Nothing enforces any of these. They mark where an artifact has stopped paying
for the tokens it costs, and cue you to move depth behind a pointer.

A `## Standards` section is prohibited in every `CLAUDE.md` at every tier.
Standards arrive by glob; a Standards heading means paying the always-on price
for something conditional.

Estimate tokens as bytes divided by four, then multiply by requests per week,
never by sessions per week. At any real usage, a thousand always-loaded tokens
is millions of tokens a week.

## Plugins versus vendoring

A third-party skill is either installed as a plugin or vendored as files, never
both. Doing both gives you every skill twice, with two copies competing for the
same triggers.

This template vendors. `enabledPlugins` is therefore empty, and the marketplace
declaration exists only so a consumer has a one-word path to enabling something
later.

## Vendoring provenance

Vendored skills are plain files under `.claude/skills/<name>/`. No separate
agents directory, no symlinks, no lock manifest. Provenance is an inline HTML
comment at the top of the vendored `SKILL.md`, in one of exactly two forms:

```
<!-- Vendored verbatim from <url> (<path> @ <sha>). See [vendoring provenance](...). -->
<!-- Vendored from <url> (<path>); adapted for this repo (<enumerated deltas>). See [vendoring provenance](...). -->
```

The trailing link points back at this section. It used to point at the decision
record that set the policy, which put a link to the template's own construction
history into thirty shipped files; the rule a reader needs is here.

The distinction is load-bearing, because the verbatim string is read by code: a
skill directory whose `SKILL.md` contains it is excluded whole from the mutate
surface. That is marker-driven rather than a hardcoded list, so every future
vendoring is covered by the provenance line this standard already requires. An
adapted skill stays on the surface, which is correct: we already changed it, so
we own it.

The `@ <sha>` pin is mandatory on both forms. Without it there is no tractable
way to diff against upstream, and drift becomes undetectable.

Every upstream also gets a block in `THIRD-PARTY-NOTICES.md` carrying its
license and copyright. For a public repo this is a legal requirement, not a
courtesy.

## Settings split

`.claude/settings.json` is committed and holds what every clone should have:
a read-only permission allowlist, hooks, marketplace declarations, and env.

`.claude/settings.local.json` is git-ignored and holds what varies by machine or
operator: model preference, MCP servers, network allowlist, and any permission
naming a local path.

A committed settings file must never contain a machine-specific path.
