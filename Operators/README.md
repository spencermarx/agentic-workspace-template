---
type: moc
status: active
created: 2026-08-19
scope: none
---

# Operators

One folder per person who works in this workspace, and the only place in the
vault with a single writer.

```
Operators/<key>/
  Meetings/          notes from meetings this person attended
  Daily Notes/       their dailies
  <Name> - Parking Lot.md
```

`<key>` is resolved from the session email against `people[].emails` in
`.workspace/workspace.json`, never hardcoded. `./hq add` creates the folder.

## Why this folder exists

Git expresses ownership through paths. Because exactly one person writes under
`Operators/<key>/`, nothing in it can produce a merge conflict -- not by
convention or good manners, but structurally. Personal notes, half-formed
thinking, and daily logs stay out of everyone else's way.

The inverse is deliberate. Shared notes -- a domain document, a person's
profile, a decision -- **should** conflict when two people edit them at once,
because that is two people changing the same agreed thing and it deserves to be
seen. A conflict here would be noise; a conflict there is the signal.

## Meetings belong to the note-taker

Two people in one meeting produce two sets of notes, because that is what
actually happened. Neither overwrites the other, and neither has to wait.

What needs to outlive the meeting gets promoted: a decision into `Decisions/`,
an action into the relevant parking lot, a fact about someone into their note in
`People/`. Consolidating two accounts into one summary is a thing a person may
choose to do, not something the structure demands.

## What does not go here

A person's **profile** -- their role, responsibilities, and goals -- is shared
information about them, so it lives in `People/` where the rest of the
organization can read and edit it. This folder is where they work, not who they
are.
