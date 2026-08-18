---
name: context
description: >-
  Create or maintain CONTEXT.md, the glossary of a workspace's ubiquitous language, or
  CONTEXT-MAP.md indexing several bounded contexts. Use whenever scaffolding a glossary,
  pinning down or sharpening a term, or when another skill needs the domain vocabulary
  maintained. Do NOT use to decide which terms matter (use `domain-modeling`) or to record
  a decision (use `decision-record`).
argument-hint: '[the context name, e.g. "Ordering"]'
---
<!-- Vendored from https://github.com/spencermarx/example-co (.claude/skills/context/SKILL.md @ ce32987bb267); adapted for this repo (the monorepo generator invocation replaced with a plain file write). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Context

A `CONTEXT.md` is the glossary of a bounded context's **ubiquitous language** - the canonical term for each domain concept and the words to avoid. It is a
glossary and **nothing else**: keep it totally devoid of implementation detail.
It is not a spec, a scratch pad, or a home for decisions - decisions are ADRs
(the [`adr` skill](../decision-record/SKILL.md)).

This skill owns the **format** and the **generator**. It does not decide _which_
terms are worth pinning down, or when the language is wrong - that active
discipline is the [`domain-modeling` skill](../domain-modeling/SKILL.md), which
calls this one to write the glossary down.

## Generate the file

Run the generator - don't hand-create the file. It scaffolds a `CONTEXT.md` at
the repo root (the single-context default) and never clobbers an existing one
(if the target already exists it skips and says so, so you edit it in place):

```bash
Write the file directly. There is no generator: a CONTEXT.md is a
markdown file with two or three headings.
```

For a context that lives in a subtree, pass `--directory`:

```bash
# A context scoped to one area: Clients/example-co/CONTEXT.md
```

For a multi-context repo, scaffold the root index with `--map` (the map is always
a repo-root index - don't combine it with `--directory`):

```bash
# The multi-context index: CONTEXT-MAP.md at the vault root
```

## Format

### CONTEXT.md - the glossary

```md
# {Context name}

{One or two sentences: what this context is and why it exists.}

## Language

**Order**:
A customer's request to buy, once submitted and accepted.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request
```

Rules:

- **Be opinionated.** When several words exist for one concept, pick the best and
  list the rest under `_Avoid_`.
- **Keep definitions tight.** One or two sentences. Define what it IS, not what it
  does.
- **Only terms specific to this context.** General programming concepts (timeouts,
  error types, utility patterns) don't belong, however much the code uses them.
  Ask: is this unique to the domain, or a general programming concept? Only the
  former belongs.
- **Group terms under subheadings** when natural clusters emerge; a flat list is
  fine when they all belong to one cohesive area.

### CONTEXT-MAP.md - the multi-context index

A single context (most repos) is one `CONTEXT.md` at the root. When a repo has
multiple bounded contexts, a root `CONTEXT-MAP.md` lists them, where each lives,
and how they relate:

```md
# Platform - Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) - receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) - generates invoices and processes payments

## Relationships

- **Ordering → Billing**: Ordering emits `OrderPlaced`; Billing consumes it to invoice
- **Ordering ↔ Billing**: shared types for `CustomerId` and `Money`
```

Inferring which structure applies:

- If `CONTEXT-MAP.md` exists, read it to find the contexts.
- If only a root `CONTEXT.md` exists, it's a single context.
- If neither exists, scaffold a root `CONTEXT.md` when the first term is resolved.

When multiple contexts exist, infer which one the current topic belongs to; if
it's unclear, ask.
