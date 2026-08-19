---
type: decision
status: active
created: 2026-08-19
date: 2026-08-19
scope: none
supersedes: "[[0003-cap-the-always-resident-context-budget]]"
---

# 0004 - Standards are enforced by rules, not by a validator

## Context

The template shipped a 1,995-line engine of which roughly 890 lines were a
`validate` command: twelve checks emitting 47 distinct finding codes, wired to a
`.githooks/pre-commit` gate and a `PostToolUse` hook.

An audit of the whole template measured what that layer actually did. On a fresh
clone, 45 of the 47 codes never fired. The two that did were `rule-glob-dead`,
warning four times because pre-bootstrap folders do not exist yet, and
`skill-body-size`, warning 21 times against the template's own skills. The
template shipped violating its own soft target.

The checks that never fired split cleanly. Some were correctness: a rule whose
pointer does not resolve, a skill that cannot register, a link that dangles on a
case-sensitive filesystem. Others were taste: em dashes, emoji, byte counts,
whether a rule's link label matched its anchor slug. The taste checks were the
ones that would fire first and most often on a new team's own writing, which
made the template restrictive at exactly the moment it should be inviting.

Underneath that, the layer had accreted without a decision. Every finding code
except two arrived in `fd8d419`, the initial standards commit, alongside a
knowledge-layer requirement that was removed once it emerged nobody had chosen
it. Provenance turned out to be the useful signal: what arrived unratified was
mostly what nobody wanted.

## Decision

**A standard is enforced through a `.claude/rules/` pointer, routed by glob and
loaded when a governed file is read, or through progressive disclosure via
nested `CLAUDE.md` files. Nothing is enforced by a script.**

The `validate` command and all twelve checks are removed, along with the
pre-commit hook, the `claude-md-budget` `PostToolUse` hook, the `budgets` object
in `workspace.json`, and the registry table in `Workspace/Standards/README.md` whose only
consumer was `check_registry`.

The engine keeps the jobs only a script can do: `bootstrap`, `add`, `render`,
`obsidian-setup`, `doctor`, `upgrade`. Generating structure is mechanical.
Judging prose is not.

**This supersedes 0003 in mechanism, not in measurement.** The byte budgets that
record established are sound and the numbers survive as guidance in
`Workspace/Standards/claude-md-contract.md` and `harness-standards § Context budget`,
routed by `.claude/rules/harness/context-budget.md`. What is withdrawn is the
claim that they should be hard failures. A cap that the template itself breaks
21 times is evidence that the number wants judgment, not a gate.

**It also amends 0001.** The three-artifact invariant becomes two: a statement in
`Workspace/Standards/`, and a rule that routes it. The registry row was the third artifact
and existed only so a check could parse it.

## Alternatives considered

### Demote every check to a warning
- **Approach:** keep all twelve checks, make none of them fail, so the commit
  hook never blocks.
- **Rejected because:** it keeps 890 lines and the maintenance they carry in
  exchange for output nobody is obliged to read. A warning that never blocks and
  fires 25 times on a clean clone is noise that trains people to ignore the tool.

### Keep the correctness checks, cut the taste checks
- **Approach:** retain `link-dead`, `rule-anchor-dead`, `skill-frontmatter` and
  their kind; remove house style and the budgets.
- **Rejected because:** it is the defensible half-measure, and it was rejected
  deliberately rather than overlooked. It preserves the framing that a script is
  the authority on whether the vault is correct, which is the thing being
  withdrawn. It also leaves a gate whose surface a new team must learn before
  their first commit lands.

## Consequences

**Makes easier:** adopting the template. A new team's first commit cannot be
blocked by a convention they have not read, and their own house voice is theirs
to set rather than inherited from whoever wrote `check_house_style`.

**Makes harder:** catching mechanical defects. Nothing now detects a dead link, a
rule pointing at a renamed heading, or a link that resolves on macOS and dangles
on Linux. With CI already removed, there is no automated pass at all. The
`vault-critic` agent is the remaining check and it is a reviewer, not a gate.

Two losses are worth naming because they were not standards enforcement and went
anyway. `check_identity` was meant to stop a consumer's name shipping in a public
template, and `check_template_purity` to keep client material out of it. Both are
restorable from git history if the trade proves wrong.

How well `check_identity` did that job is worth recording, because it argues
against rebuilding it the same way. Its term list was five hardcoded strings:
`spencermarx`, `aclarify`, `bizkit`, `wrkbelt`, `donostia`. Removing it exposed an
example row in `.workspace/templates/parking-lot.md` reading
`| 001 | 2026-08-18 | spencer | pricing |`, which had been there since the file
was written. That path was scanned and passed, because `spencer` is not
`spencermarx`. A denylist reports success on everything it was not told about,
and the confidence it buys is worth less than it appears.

**Explicitly deferred:** whether anything replaces the mechanical pass. A
link-checker run on demand rather than as a gate would recover most of the value
at none of the cost, but no such thing is being built now.
