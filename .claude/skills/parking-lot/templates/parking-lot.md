---
type: note
status: active
project: {{PROJECT_TAG}}
tags:
  - type/note/parking-lot
  - venture/{{PROJECT_TAG}}
  - status/active
---

# {{SCOPE_NAME}} — Parking Lot

Capture inbox for anything surfaced during work on {{SCOPE_NAME}} that is out of scope right now and must not be lost. Both operators and both Claude harnesses read and write this file; git keeps it in sync. Managed by the `parking-lot` skill.

The bar to add is low. The discipline is the triage. This is not a plan. When an item becomes committed work, a strategic unknown, a product-feature idea, or a decision to make, it graduates into the matching register (see the boundary table below) and its row moves to the Archive marked `promoted`. Nothing is ever deleted.

## Boundary

| This item is... | It belongs in... |
|---|---|
| Deferred / out of scope now | this file (Open items) |
| A committed near-term action | `CLAUDE.md` "What's pending" |
| A load-bearing strategic unknown | `CLAUDE.md` "Open questions" |
| A product-feature idea | the PRD's tracked-but-uncommitted register |

## Open items

| ID | Raised | By | Area | Item | Next step |
|---|---|---|---|---|---|
| | | | | | |

<!--
Row format (copy into the table above, delete this comment block once the first real row exists):
| {{PREFIX}}-PL-001 | {{TODAY}} | Spencer | gtm | One or two sentences describing the parked item. | Optional owner or immediate follow-up. |
Area set: product, gtm, legal, infra, ops, research, brand, finance, partnership.
-->

## Archive

Triaged items. Status is one of `promoted`, `dropped`, `resolved`. Disposition points to where a promoted item went.

| ID | Raised | By | Area | Item | Status | Disposition |
|---|---|---|---|---|---|---|
| | | | | | | |
