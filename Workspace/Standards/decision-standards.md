# Decision standards

What earns a decision record, who is allowed to create one, and the shape it
takes. The register is only worth keeping if it stays short enough to read end
to end, so most of this document is about restraint.

## Capture is human-confirmed

**An agent may propose a decision record. An agent may not create one without an
explicit yes from the operator in the same session.**

This is the load-bearing rule and it has no exceptions worth the name. A record
written because a heuristic fired is a record nobody chose to keep, and a
register full of those is worse than no register: it buries the four decisions
that mattered under forty that did not.

Proposing looks like one line. State the claim the record would make, and stop:

> That's a decision — "vendored skills are plain files, not plugins". Record it?

Then wait. No draft, no file, no number reserved. Silence is not consent, and
neither is the operator moving on to something else.

The reverse case needs saying too, because the rule is not "agents are
untrusted": an operator who says "write that up" has confirmed, and the agent
should not ask twice.

### The one exception, and why it is one

A skill whose **stated purpose** is document creation, invoked by a human who
read that description, has consent. `grill-with-docs` announces that it "creates
docs (ADR's and glossary) as we go", and a person typing it has asked for
exactly that.

The exception is narrow on purpose. It does not extend to a skill that creates
records incidentally while doing something else, and it does not extend to any
skill an agent can invoke on its own initiative. If those two conditions are not
both met, the rule above applies.

## The significance test

Write one when the choice is:

- **Precedent-setting.** It sets a pattern others will follow.
- **Hard to reverse.** Undoing it means unwinding work, or a conversation with
  someone outside the workspace.
- **Surprising given its trade-off.** A reader who knows the constraints would
  guess differently.

Two of three is a clear yes. One is a judgment call, and a judgment call is a
thing to raise with a person rather than resolve alone.

Changing a document in `Workspace/Standards/` is a strong signal, because a standard that
changes without a recorded reason gets changed back. It is a reason to
**propose** a record. It is not a trigger that writes one, and it never was a
good one: the rule fired on every typo fix to a standards file.

Do not write one for a preference nobody will relitigate.

## Where records go

`<scope>/decisions/NNNN-<kebab-slug>.md`

- **Scope-local.** A decision about one area lives in that area's `decisions/`
  folder. A workspace-wide decision lives in `Decisions/` at the root.
- **Numbered per scope**, four digits, zero-padded. Two areas never collide, and
  numbering per scope keeps the sequence meaningful within the thing it governs.
- **The slug reads as a claim**, not a topic:
  `0004-price-by-outcome-not-hours.md`, never `0004-pricing.md`. A topic name
  forces a future reader to open the file to learn whether it is relevant.

Decisions about **the template itself** are not workspace decisions and do not
belong in any of these. They live in `.workspace/decisions/`, which is
template-owned and carried by `./hq upgrade`. A consumer never adds to
that register.

## The four sections

Every record carries **Context**, **Decision**, **Alternatives considered**, and
**Consequences**. The reasoning is the point; a record that states what was
decided without saying what was rejected and why is a note, not a record, and it
will not survive contact with the first person who disagrees.

**Alternatives considered** is the section people skip and the one that earns
the file. If you cannot name a real alternative, you have not made a decision,
you have described the only path available.

## Superseding

Never edit a record to say something else. Its reasoning stays true of the
moment it was made. Set it to `superseded`, write a new one pointing back with
`supersedes`, and update the register.

Being able to see what was believed, and when, is most of the value of keeping a
register at all.
