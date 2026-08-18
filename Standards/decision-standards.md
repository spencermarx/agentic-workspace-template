# Decision standards

## The recording threshold

Write a decision record when the choice is **precedent-setting**, **hard to
reverse**, or **surprising given its trade-off**. Two of the three is a clear
yes; one is a judgment call.

Do not write one for a choice you could undo in an afternoon, or for a
preference nobody will relitigate. The register earns its keep by being short
enough to read.

Changing anything in `Standards/` always meets the threshold, because a standard
that changes without a recorded reason will be changed back.

## Decision record format

Path: `<scope>/decisions/NNNN-<kebab-slug>.md`. Four digits, zero-padded,
numbered per scope rather than globally, so two areas never collide.

Frontmatter is mandatory. A decision record without it is invisible to every
query, which defeats the point of having a register.

Four sections, in this order:

```markdown
## Context
## Decision
## Alternatives considered
## Consequences
```

**Alternatives considered** is the section that earns the document. Without it,
a future reader has the answer but not the reasoning, and reopens the same
debate. Each alternative gets what it was and why it lost.

**Consequences** splits three ways: what this makes easier, what it makes
harder, and what it explicitly defers.

## Superseding rather than editing

A decision that no longer holds is not edited. Its `status` becomes
`superseded`, and the new record carries `supersedes` pointing at it. The
thinking stays useful even when the conclusion does not.
