---
type: decision
status: active
created: 2026-08-18
date: 2026-08-18
scope: none
---

# 0001 - Standards as rules routed to the files they govern

## Context

The two workspaces this template was built from both put conventions inside
`CLAUDE.md`. One reached 45 nested `CLAUDE.md` files totalling 315 KB, with a
single file at 33 KB; the other reached 11 files totalling 106 KB with a 35 KB
leaf. At roughly 8,750 tokens, a 35 KB file is paid on every request made
anywhere in that subtree.

No single edit was unreasonable. Nothing ever reported the total.

Two structural problems drove the growth. A `CLAUDE.md` governs a directory
subtree, not a file type, so a convention about one kind of file had to be
repeated in every subtree containing that kind. And a `CLAUDE.md` does not
reliably reach subagents, so anything a subagent needed had to be duplicated
into its prompt.

## Decision

A standard is stated **once**, in a `##` section of a document under
`Standards/`. That section is the single source of truth.

Standards are then **routed to the files they govern** by atomic
`.claude/rules/<domain>/<slug>.md` files. Each rule carries exactly two
frontmatter keys, `description` and `paths`, loads on demand when the main agent
or a subagent reads a matching file, and is a **pure pointer**: a glob plus a
deep link to the exact section. It never restates the rule.

Each standard also carries a row in `Standards/README.md`, the registry.

Nested `CLAUDE.md` files remain, and remain the mechanism for progressive
disclosure, but they no longer carry standards. A `## Standards` section is
prohibited at every tier.

`./workspace validate` enforces all of it, including a positive control that
every glob matches at least one real file.

## Alternatives considered

### Keep standards in nested CLAUDE.md and just be disciplined
- **Approach:** cap file sizes by convention and review.
- **Rejected because:** this is what both source repositories were already
  doing. Accretion is the default state of a file with no cheaper alternative,
  and no mechanism reported the total until someone measured it by hand.

### Ban nested CLAUDE.md entirely, root-only
- **Approach:** one `CLAUDE.md`, hard-capped, everything else in rules.
- **Rejected because:** it over-corrects. Progressive disclosure through nesting
  is a genuine requirement, and the failure mode was standards living in the
  file, not the file existing. Removing the pressure fixes the cause; removing
  the mechanism removes a feature.

### A single lint script with hardcoded checks, no rules layer
- **Approach:** encode conventions directly in the validator.
- **Rejected because:** the agent would never read them. A lint tells you after
  the fact; a rule loads into context before the agent writes.

## Consequences

**Makes easier:** finding where a convention is stated, because there is exactly
one place. Reaching subagents, because rules load for them too. Governing a file
type wherever it lives. Keeping `CLAUDE.md` small enough that nesting is cheap.

**Makes harder:** adding a convention, which now costs three artifacts instead
of one paragraph. This is intentional friction: it is the friction that keeps
the registry short enough to read.

**Explicitly deferred:** automatic detection of a pointer aimed at a live but
wrong section. The validator checks the anchor resolves and warns when the link
label disagrees with the heading, but a pointer to a plausible wrong section
still passes.
