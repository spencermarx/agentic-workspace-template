# Parking Lot Conventions

The deep reference behind the `parking-lot` SKILL.md. The verbs and the boundary live in the SKILL.md; this file is the detail it links to.

## Scope prefixes

Every item ID carries a scope prefix so IDs stay unique if items are ever cross-referenced across scopes. The prefix is the first three or four letters of the scope name, uppercased, kept unique.

| Scope | Prefix | Parking Lot file |
|---|---|---|
| Example Co | `BIZ` | `Clients/example-co/Example Co - Parking Lot.md` |
| Example Two | `Example Two` | `Clients/example-two/Example Two - Parking Lot.md` |
| Example Three | `ROD` | `Clients/example-three/Example Three - Parking Lot.md` |
| Example Four | `PIP` | `Clients/example-four/Example Four - Parking Lot.md` |
| Core (partnership) | `CORE` | `Core/Core - Parking Lot.md` |
| Spencer (personal) | `SM` | `Operators/Spencer/Spencer - Parking Lot.md` |
| Anthony (personal) | `AC` | `Operators/Anthony/Anthony - Parking Lot.md` |

A new scope picks a prefix by the same rule and records it here.

## ID scheme

`<PREFIX>-PL-NNN`, `NNN` zero-padded to three digits, monotonic per scope. Examples: `BIZ-PL-001`, `Example Two-PL-012`. Read the file and take the highest existing number for the prefix, add one. Never reuse a retired ID and never renumber an existing one; the archive references depend on IDs being stable.

## Status vocabulary

| Status | Meaning | Lives in |
|---|---|---|
| `open` | Parked, not yet triaged or acted on. | Open items table |
| `promoted` | Graduated into another register (see routing). | Archive table |
| `dropped` | Decided not to pursue. | Archive table |
| `resolved` | Question answered or item handled with no further work. | Archive table |

Only `open` items sit in the Open items table. The three terminal states sit in the Archive. Rows are never deleted.

## Area set (suggested, not enforced)

Pick one short tag per item. Align to the workspace taxonomy where a namespace exists.

`product` (build / PRD scope), `gtm` (positioning, channel, pricing), `legal` (compliance, counsel, entity), `infra` (harness, tooling, APIs), `ops` (partnership operations, cadence), `research` (market / customer evidence), `brand` (naming, voice, design), `finance`, `partnership` (equity, structure, roles).

## Graduation routing

When a parked item stops being just-a-capture, write it into the target register first, then mark the parking-lot row `promoted` with a Disposition that points to where it went. This keeps a single source of truth per item.

| A parked item becomes... | Route it to | Parking-lot status |
|---|---|---|
| a committed near-term action | the scope's `CLAUDE.md` "What's pending" | `promoted` |
| a load-bearing strategic unknown | the scope's `CLAUDE.md` "Open questions" | `promoted` |
| a product-feature idea (Example Co) | the PRD's tracked-but-uncommitted register (§7) | `promoted` |
| a decision that needs a working session | an `Activities/<YYYY-MM-DD> <name>/` decision note | `promoted` |
| something we will not do | stays in the Archive only | `dropped` |
| a question with a clear answer and no follow-on work | stays in the Archive only | `resolved` |

Do not decide for the operators. Where a call is theirs, either leave the item `open` with a recommendation noted, or promote it to Open questions so it is tracked as a decision to make.

## Frontmatter

The Parking Lot file carries workspace-standard frontmatter. `type/note/parking-lot` is a leaf under the existing `type/note/` namespace, so no new namespace is introduced.

```yaml
---
type: note
status: active
project: <project-tag>        # e.g. example-co; omit for Core / operator scopes
tags:
  - type/note/parking-lot
  - venture/<project-tag>      # or area/... for Core / operator scopes
  - status/active
---
```

## Merge and sync guidance

The file is canonical and committed to git; git is the only sync mechanism between the two operators and their harnesses. Append new Open items at the tail so independent additions do not overlap. IDs are read-then-max+1, so never renumber. If git flags a conflict from two tail additions made in parallel, keep both rows and bump the later ID to the next free number. Real concurrency is rare because both operators are part-time and asynchronous.
