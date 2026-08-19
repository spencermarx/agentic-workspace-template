> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/google-slides/SKILL.md`, and delete this banner. See
> [README](README.md).

# google-slides

Read, create, and modify Google Slides presentations, including images, shapes, tables, and charts.

## Wiring

Same Google service-account wiring as `google-calendar`.

Weigh it against `create-html-slides`, which needs no authentication at all and
produces a self-contained file. Promote this only when the deliverable must be a
native Google deck someone else will edit.

## What it does

Full `batchUpdate` access for advanced operations, plus higher-level helpers for
the common create-a-deck-from-an-outline case.
