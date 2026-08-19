---
type: decision
status: superseded
created: 2026-08-18
date: 2026-08-18
scope: none
---

# 0003 - Cap the always-resident context budget

## Context

Two costs are paid on every request rather than once per session: the body of
every `CLAUDE.md` on the path being worked in, and the name and description of
every skill in the library.

Measured in the source repositories: 315,777 bytes across 45 `CLAUDE.md` files
in one, 106,186 across 11 in the other. Skill descriptions ran to 28,144 bytes
across 67 skills in one and 9,879 across 17 in the other, an average of 581
bytes per description in the smaller library.

Estimating tokens as bytes over four, and multiplying by requests per week
rather than sessions per week, a thousand always-loaded tokens costs millions of
tokens a week at any real usage.

Neither repository had a mechanism that reported the total.

## Decision

Hard byte caps, enforced by `./workspace validate` as failures, with the
remediation stated in the error message.

| Artifact | Cap | Target |
|---|---|---|
| Root `CLAUDE.md` | 8,000 | 5,000 |
| Router `CLAUDE.md` | 3,500 | -- |
| Leaf `CLAUDE.md` | 20,000 | 14,000 |
| All skill descriptions combined | 14,000 | -- |
| One description | 500 chars | 350 |
| `SKILL.md` body | 8,000 | 5,000 |
| One rule | 1,200 | 750 |
| The one universal rule | 400 | 400 |

Tier is inferred structurally: a folder whose subtree contains another
`CLAUDE.md` is a router, and its only job is to point down.

## Alternatives considered

### Guidance without enforcement
- **Approach:** state the budgets in the standards and trust review.
- **Rejected because:** both source repositories already had size guidance in
  their skill-authoring docs and exceeded it by a factor of four.

### Enforce only at commit time
- **Approach:** a pre-commit check and nothing else.
- **Rejected because:** feedback speed is what prevents accretion. A `PostToolUse`
  hook that reports the overage in the same turn the agent wrote it is what
  stops the growth; the commit hook is a backstop.

## Consequences

**Makes easier:** keeping nesting cheap, which is what lets progressive
disclosure stay a usable feature rather than a liability.

**Makes harder:** writing a leaf that carries genuine depth. The intended
response is the `| File | When to load |` table: push the depth into linked
documents and let the leaf route to them. A leaf over budget is a signal that
table is not doing enough work.

**Explicitly deferred:** a token-accurate measurement. Bytes over four is a
coarse estimate, and a real tokenizer would need a dependency this engine
deliberately does not have.
