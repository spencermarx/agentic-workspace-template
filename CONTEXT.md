---
type: moc
status: active
created: 2026-08-19
scope: none
---

# Context

The ubiquitous language of this workspace: the terms that mean something
specific here, and the synonyms we are choosing against.

Owned by the [`context`](.claude/skills/context/SKILL.md) skill. Add a term when
it recurs and its meaning is not obvious; do not add general concepts any
workspace would share.

## Language

**Area**:
A top-level folder that carries its own context and its own `CLAUDE.md`. A
client, a venture, a product, an offering.
_Avoid_: project, workspace, space

**Leaf**:
An area whose `CLAUDE.md` carries full context, because it has no children that
carry their own.
_Avoid_: page, terminal node

**Router**:
A folder whose `CLAUDE.md` exists only to say what is beneath it and which child
to read next.
_Avoid_: index, hub

**Standard**:
A convention stated once in `Standards/`, and routed to the files it governs by
a rule. Both, or it is not a standard.
_Avoid_: guideline, policy, convention

**Rule**:
A file in `.claude/rules/` that routes a standard to a set of paths. A pointer,
never a statement.
_Avoid_: lint, check

## Relationships

- A **standard** has exactly one **rule** routing it.
- An **area** is either a **leaf** or a **router**, never both.

## Flagged ambiguities

<!-- AGENT: terms that are used loosely in this workspace and have not been
     pinned down yet. Each one is a question, not a definition. Delete this
     comment once you have added the first real entry, or delete the section if
     there are none. -->

- None recorded yet.
