---
type: moc
status: active
created: 2026-08-18
scope: none
---

# Decision records

A decision record holds a choice you have settled **and the reasoning that got
you there**, so the same debate is not reopened in six months by someone who
only has the conclusion.

Write one when the choice is **precedent-setting**, **hard to reverse**, or
**surprising given its trade-off**. Two of three is a clear yes. The full test,
and everything else this page describes, is governed by
[decision-standards](../Standards/decision-standards.md); this page explains
it, that page rules on it.

The register itself is [Decisions](../../Decisions/README.md). The template
picks the register that owns the decision, numbers the record, and derives its
scope from the folder, so the only thing left to you is the thinking.

## You decide when one gets written

An agent working alongside you may notice that something looks worth recording
and say so. It will not create the record. You say yes first, every time.

This is deliberate, and it is the difference between a register you read and a
register you skim. An agent applying a significance test on its own initiative
is generous with it — every settled question starts to look precedent-setting —
and a register that grows on autopilot buries the four decisions that mattered
under forty that did not.

So if something you have decided deserves a record and nobody offered, ask for
one. Nothing is watching the conversation on your behalf, by design.

## The section people skip

**Alternatives considered.** Without it, a future reader has your answer but not
your reasoning, so the first person who disagrees reopens the whole debate. If
you cannot name a real alternative, you have not made a decision, you have
described the only path available.

## Naming

`decisions/NNNN-<slug>.md`, and the slug reads as a claim:
`0004-price-by-outcome-not-hours.md`, never `0004-pricing.md`. A topic name
forces a future reader to open the file to find out whether it is relevant.

## Superseding

Never edit a record to say something else. Its reasoning stays true of the moment
it was made. Set it to `superseded`, write a new one pointing back with
`supersedes`, and update the index.

Being able to see what was believed, and when, is most of the value of keeping a
register at all.

## Changing a standard is a strong signal

A standard that changes without a recorded reason gets changed back, so a change
to anything in `Workspace/Standards/` is usually worth a record.

Usually, not always. This used to be an automatic trigger, which meant a typo fix
in a standards file demanded a decision record. Treat it as a prompt to think,
not as a rule that has already decided.
