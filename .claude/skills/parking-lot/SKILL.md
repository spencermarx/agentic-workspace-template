---
name: parking-lot
description: >-
  Capture, triage, and query parking-lot items: anything surfaced mid-work that is out of
  scope right now and must not be lost. Use on "park this", "note it for later", "out of
  scope for now", "what is parked", or "triage the parking lot". Works for any area. Do
  NOT use for a committed near-term action (that goes in the area's CLAUDE.md "What's
  pending") or a load-bearing unknown ("Open questions").
---

# Parking Lot

One repeatable job: keep a scope's deferred items in a single canonical Markdown file that both operators and both Claude harnesses read and write, so nothing surfaced mid-work is lost and everything is triaged the same way. Git is the sync layer. This skill enforces the file location, ID scheme, status vocabulary, and graduation routing so concurrent edits rarely collide and a sweep is uniform no matter who runs it.

A parking lot is a capture inbox, not a plan. The bar to add is low. The discipline is in the triage.

## Boundary (do not duplicate other registers)

| Register | Holds | Where |
|---|---|---|
| **Parking Lot** (this skill) | Anything deferred or out of scope now. Low bar to add. | `<Scope> - Parking Lot.md` |
| **What's pending** | Committed near-term actions. | the scope's `CLAUDE.md` |
| **Open questions** | Load-bearing strategic unknowns the scope must answer. | the scope's `CLAUDE.md` |
| **§7 tracked-but-uncommitted** | Product-feature optionality (Example Co). | the PRD |

A parked item graduates by moving into one of those registers on triage. It does not get copied into two places.

## Scope resolution

Resolve the scope from the active file or working directory, then map to a canonical file:

| Scope | Parking Lot file |
|---|---|
| A venture | `Clients/<venture>/<Venture Display Name> - Parking Lot.md` |
| Partnership-level | `Core/Core - Parking Lot.md` |
| A operator | `Operators/<current-operator>/<current-operator> - Parking Lot.md` |

If the scope is ambiguous, ask which one. Never guess between two ventures. The `<current-operator>` is resolved per the root `CLAUDE.md` rule (session user / git email).

## Procedure

Pick the verb from the request.

### Add (park an item)

1. Resolve the scope and its Parking Lot file. If the file does not exist, create it from `templates/parking-lot.md` (see Init).
2. Read the file. Find the highest existing item number for this scope's prefix; the new ID is that number + 1, zero-padded to three digits (`BIZ-PL-014`). Prefixes and the ID scheme are in `references/conventions.md`.
3. Append one row per new item to the **Open items** table (append at the end; never rewrite existing rows or renumber existing IDs):
   - **Raised**: today's date, `YYYY-MM-DD`.
   - **By**: the current operator (resolved per root `CLAUDE.md`), or `both` / an external name when stated.
   - **Area**: one short area tag (see the suggested set in `references/conventions.md`).
   - **Item**: the thing in one or two sentences. Facts, observations, and open questions stay distinguishable per workspace voice.
   - **Next step**: optional owner or immediate follow-up; leave blank if none.
4. Confirm back the IDs assigned. Do not also add the item to any other register (that is what triage does).

### Triage (sweep open items)

1. Load the Parking Lot file and the scope's `CLAUDE.md` (for its Open questions and What's pending sections).
2. Walk each **Open item**. For each, decide a disposition and, when it graduates, write it into the target register first, then update the parking-lot row. The routing table is in `references/conventions.md`.
3. Move triaged rows from **Open items** to the **Archive** table, setting **Status** (`promoted` / `dropped` / `resolved`) and a **Disposition** that points to where it went (for example `Promoted -> CLAUDE.md Open questions #14`).
4. Never delete a row. The archive keeps the thinking.
5. Do not decide for the operators. Where an item needs a operator call, surface it as a recommendation and leave it open, or promote it to Open questions.

### List (show what is parked)

Render the Open items table, optionally filtered by area, operator, or scope. Read-only.

### Init (create the file)

Copy `templates/parking-lot.md`, filling the placeholders (`{{SCOPE_NAME}}`, `{{PREFIX}}`, `{{PROJECT_TAG}}`, `{{TODAY}}`). Leave the Open items table empty. Then add the pointer to this file in the scope's `CLAUDE.md` (its file table or an equivalent index) so future sessions find it.

## Sync and merge

The file is canonical and committed; git is the only sync mechanism. New items append to the end of Open items, so two people parking different items produce non-overlapping additions in most cases. IDs are always read-then-max+1, so never reuse or renumber an existing ID. If git surfaces a conflict (two rows added at the same tail), keep both and renumber the later one. Both operators being part-time and async makes real concurrency rare.

## References

- `references/conventions.md`: ID prefixes and scheme, status vocabulary, area set, the graduation routing table, frontmatter, and merge guidance.
- `templates/parking-lot.md`: the canonical Parking Lot file template.
