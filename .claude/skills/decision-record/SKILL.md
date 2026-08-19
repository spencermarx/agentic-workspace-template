---
name: decision-record
description: >-
  Record a settled choice, and its reasoning, so nobody relitigates it. PROPOSE one whenever
  a decision is precedent-setting, hard to reverse, or surprising given its trade-off, then
  stop: a record is only ever created after the operator says yes. Trigger on "write this
  down", "document this decision", "supersede that decision", "why did we choose". Do NOT
  use for a choice you could undo in an afternoon, to park an open item (use `parking-lot`),
  or for work not yet decided (use `wayfinder`).
---

<!-- Vendored from https://github.com/spencermarx/example-co (.claude/skills/adr/SKILL.md @ ce32987bb267); adapted for this repo (rewritten around a plain file write: the generator, ULID identity, and derived ledger are gone, replaced by per-scope NNNN numbering and the Decisions README index; the significance test, the section discipline, the supersession protocol, and the anti-patterns are carried over). See [vendoring provenance](../../../Workspace/Standards/harness-standards.md#vendoring-provenance). -->

# Decision record

A decision record holds a settled choice **and its reasoning**, so the same
debate is not reopened in six months by someone who only has the conclusion.

The reasoning is the point. A record that states what was decided without saying
what was rejected and why is a note, not a record, and it will not survive
contact with the first person who disagrees.

## Stop: you need a yes first

**You may propose a record. You may not create one without an explicit yes from
the operator in this session.**

Full rule (SSOT): [decision-standards § Capture is human-confirmed](../../../Workspace/Standards/decision-standards.md#capture-is-human-confirmed)

Proposing is one line. State the claim the record would make, and stop:

> That's a decision — "vendored skills are plain files, not plugins". Record it?

Then wait. Do not draft the file, do not reserve a number, do not write it and
offer to remove it afterwards. The operator moving on to something else is not a
yes, and neither is silence.

Everything below this section is what to do **after** you have one.

## Does it qualify?

The significance test — precedent-setting, hard to reverse, or surprising given
its trade-off, two of three being a clear yes — is stated once in
[decision-standards § The significance test](../../../Workspace/Standards/decision-standards.md#the-significance-test).
Read it there rather than working from memory.

A change to `Workspace/Standards/` is a strong signal and a good reason to **propose** a
record. It is not a trigger that writes one.

## Where it goes

`<scope>/decisions/NNNN-<kebab-slug>.md`

- **Scope-local.** A decision about one area lives in that area's `decisions/`
  folder. A workspace-wide decision lives in `Decisions/` at the root.
- **Not for template decisions.** A choice about how the template itself is
  built belongs in `.workspace/decisions/`, which a consumer never adds to.
- **Numbered per scope**, four digits, zero-padded. Two areas never collide, and
  numbering per scope keeps the sequence meaningful within the thing it governs.
- **Slug is kebab-case** and reads as a claim, not a topic:
  `0004-price-by-outcome-not-hours.md`, never `0004-pricing.md`.

Find the next number by counting what is already there:

```bash
scope="Areas/example-area"          # or "." for workspace-wide
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

- **Writing one without being asked.** The failure this skill guards hardest
  against. Creating the file and offering to delete it is the same defect with
  an extra step, and so is drafting it "so it's ready if you want it".
- **Recording the outcome without the alternatives.** The most common failure,
  and it makes the record worthless for its one purpose.
- **Writing a record for a reversible choice.** It dilutes the register until
  nobody reads it.
- **Editing a superseded record** so it agrees with current practice. That
  destroys the history the register exists to hold.
- **A slug that names a topic rather than a claim.** `0004-pricing.md` tells a
  future reader nothing; they have to open it to know whether it is relevant.
- **Deferring the record until the work is done.** Raise it when the decision is
  made, while the alternatives are still in someone's head. Waiting for the yes
  is the rule; waiting a fortnight to ask is not.
