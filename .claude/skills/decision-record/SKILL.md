---
name: decision-record
description: >-
  Record a settled choice, and its reasoning, so nobody relitigates it. Use whenever a
  decision is made that is precedent-setting, hard to reverse, or surprising given its
  trade-off, and on any change to Standards. Trigger on "write this down", "document this
  decision", "supersede that decision", "why did we choose". Do NOT use for a choice you
  could undo in an afternoon, to park an open item (use `parking-lot`), or to plan work
  that is not yet decided (use `wayfinder`).
---

<!-- Vendored from https://github.com/spencermarx/example-co (.claude/skills/adr/SKILL.md @ ce32987bb267); adapted for this repo (rewritten around a plain file write: the generator, ULID identity, and derived ledger are gone, replaced by per-scope NNNN numbering and the Decisions README index; the significance test, the section discipline, the supersession protocol, and the anti-patterns are carried over). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->

# Decision record

A decision record holds a settled choice **and its reasoning**, so the same
debate is not reopened in six months by someone who only has the conclusion.

The reasoning is the point. A record that states what was decided without saying
what was rejected and why is a note, not a record, and it will not survive
contact with the first person who disagrees.

## The significance test

Write one when the choice is:

- **Precedent-setting.** It sets a pattern others will follow.
- **Hard to reverse.** Undoing it means unwinding work, or a conversation with
  someone outside the workspace.
- **Surprising given its trade-off.** A reader who knows the constraints would
  guess differently.

Two of three is a clear yes. One is a judgment call.

**Any change to `Standards/` always qualifies**, because a standard that changes
without a recorded reason gets changed back.

Do not write one for a preference nobody will relitigate. The register earns its
keep by staying short enough to read end to end.

## Where it goes

`<scope>/decisions/NNNN-<kebab-slug>.md`

- **Scope-local.** A decision about one client lives in that client's
  `decisions/` folder. A workspace-wide decision lives in `Decisions/` at the
  root.
- **Numbered per scope**, four digits, zero-padded. Two areas never collide, and
  numbering per scope keeps the sequence meaningful within the thing it governs.
- **Slug is kebab-case** and reads as a claim, not a topic:
  `0004-price-by-outcome-not-hours.md`, never `0004-pricing.md`.

Find the next number by counting what is already there:

```bash
scope="Clients/example-co"          # or "." for workspace-wide
mkdir -p "$scope/decisions"
n=$(printf "%04d" $(( $(ls "$scope/decisions" 2>/dev/null | grep -c '^[0-9]') + 1 )))
echo "$scope/decisions/$n-<slug>.md"
```

There is no generator and no minted identity. The filename is the identity, it
sorts correctly in Obsidian's file list, and a human can read it.

## Writing it

Start from [the template](../../../.workspace/templates/decision-record.md).
Frontmatter is **mandatory**: a record without it is invisible to every query,
which defeats having a register at all.

Four sections, in order.

**Context.** Why now? What deadline, constraint, or trade-off forced this? A
reader should understand the pressure before they see the answer.

**Decision.** One sentence, then the specifics. What does this mean concretely,
what is the definition of done, and how would you verify it held?

**Alternatives considered.** The section that earns the document. Each option
gets what it was and why it lost. If you cannot name a real alternative, you
probably have not made a decision, you have described the only available path.

**Consequences.** Three ways: what this makes easier, what it makes harder, and
what it explicitly defers. The middle one is the one people skip and the one
that is read most often later.

## Superseding

A decision that no longer holds is **never edited to say something else**. Its
reasoning stays true of the moment it was made.

1. Set the old record's `status` to `superseded`.
2. Write the new record, with `supersedes` in its frontmatter pointing at the
   old one as a wikilink.
3. Update the index table in that scope's `decisions/README.md`.

The old record stays readable. Being able to see what was believed, and when, is
most of the value of keeping a register.

## Citing one

Link a record wherever its conclusion is being relied on, so a reader who
disagrees finds the reasoning rather than arguing with the result:

```markdown
Rationale: [0004 Price by outcome not hours](decisions/0004-price-by-outcome-not-hours.md).
```

Cross-reference related records inline. They are a web, not a list.

## Anti-patterns

- **Recording the outcome without the alternatives.** The most common failure,
  and it makes the record worthless for its one purpose.
- **Writing a record for a reversible choice.** It dilutes the register until
  nobody reads it.
- **Editing a superseded record** so it agrees with current practice. That
  destroys the history the register exists to hold.
- **A slug that names a topic rather than a claim.** `0004-pricing.md` tells a
  future reader nothing; they have to open it to know whether it is relevant.
- **Deferring the record until the work is done.** Write it when the decision is
  made, while the alternatives are still in your head.
