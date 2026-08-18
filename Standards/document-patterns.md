# Document patterns

The recurring shapes. Each one exists because the alternative was tried and rotted.

## Two buckets per area

Every area folder splits exactly two ways:

- `Activities/<YYYY-MM-DD> <activity name>/` for dated, time-stamped work:
  meetings, research bursts, working sessions, decision sessions.
- `Documents/<Family>/` for durable artifacts that persist independent of any
  single activity, subfoldered by artifact family.

If you cannot tell which bucket something belongs in, ask whether it will still
be read a year from now without its date attached. If yes, it is a Document.

## Summary and receipts

A folder of related outputs gets a `00-summary.md` that synthesizes, plus
`01-`, `02-` receipts that hold the evidence. The summary is explicitly a
pointer document: it states the conclusions and links to the receipts that
support them. It is not a place to put new material.

## Dated research bundles

Research lands as `Documents/Research/<topic>-<YYYY-MM-DD>/`, with its own
`README.md` index table.

New research lands as a new dated bundle. It never overwrites an existing one.
Supersession is noted in the index, so the older bundle stays readable and you
can see what you believed and when.

## Lifecycle as sibling directories

Where a thing passes through states, the states are sibling directories and
movement between them is `git mv`, never a delete. The thinking stays useful
even when the conclusion does not.

Soft-parking is a status banner at the top of the area's `CLAUDE.md`, not a
folder move. Folder location expresses a decision; it does not express the
passage of time.

Corollary: **never encode a lifecycle in folder names when a query can answer
it.** A `Recent/` and `Archive/` split is a manual chore that nobody performs,
and it goes stale within weeks. Sort by date in a view instead.

## The three registers

Three places for things that are not done, and they do not overlap.

| The item is | It belongs in |
|---|---|
| Deferred, or out of scope right now | the area's Parking Lot |
| A committed near-term action | `CLAUDE.md`, "What's pending" |
| A load-bearing strategic unknown | `CLAUDE.md`, "Open questions" |

A parking lot is two tables, Open items and Archive, with columns
`ID | Raised | By | Area | Item | Next step`. Nothing is ever deleted: a triaged
row moves to Archive marked `promoted`, `dropped`, or `resolved`.

## Canonical and mirror

See `canonical-and-mirrors.md`. Every document that copies something the vault
does not own declares that fact in frontmatter.

## The deliberately unfilled scaffold

A document you know you need but have not agreed yet ships as a scaffold:
`status: draft`, a prompt paragraph per section, and `- TBD`. This is better
than an absent document because it records the shape of the question, and better
than an invented document because it does not pretend to an answer.

## Per-machine plugin config

When a plugin's `data.json` holds an absolute path or accumulating personal
state:

1. Ignore `data.json` by explicit path in `.gitignore`, with a comment saying why.
2. Commit `data.json.example` beside it, with every machine-specific value
   replaced by a token.
3. Commit `SETUP.md` in the plugin folder: what the plugin does, the one-time
   copy step, what each setting means, and the safety rules.
4. Add a line to the workspace README's setup section.

`./workspace obsidian-setup` performs step 1 through 3 mechanically.

## Reconciling a second convention

When a second convention for an existing thing appears, reconciling it is part
of the change that introduced it, not a follow-up.

Two unreconciled conventions for one thing is the most expensive kind of debt in
a knowledge base, because both look correct in isolation and an agent will
propagate whichever it read most recently.
