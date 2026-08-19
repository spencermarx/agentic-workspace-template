---
name: wayfinder
description: Plan a huge chunk of work - more than one agent session can hold - as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---

<!-- Vendored from https://github.com/spencermarx/bizkit (.claude/skills/wayfinder/SKILL.md @ ce32987bb267); adapted for this repo (renamed to match what it does here; tracker and config locations read from .workspace/workspace.json rather than assuming an issue tracker; engineering artifact types re-keyed to vault artifacts). Upstream lineage: https://github.com/mattpocock/skills. See [vendoring provenance](../../../Workspace/Standards/harness-standards.md#vendoring-provenance). -->

A loose idea has arrived - too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** - questions whose resolution is a decision, not slices of a build to execute - one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting - it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic - engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear - nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes** - carrying execution into the map itself - but absent that, produce decisions, not deliverables.

## Refer by name

Every map and ticket is an issue, so it has a **name** - its title. In everything the human reads - narration, the map's Decisions-so-far - refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish - a name wraps its link - but they ride _inside_ the name, never stand in for it.

The same instinct governs **vocabulary**: a name made of private jargon is no more legible than a number. Everything a human reads on the map or its tickets - bodies, titles, resolution comments, Decisions-so-far gists - obeys the [`conveying-clearly` skill](../conveying-clearly/SKILL.md): terms are plain words, `CONTEXT.md` ubiquitous language, or glossed inline at first use. Shorthand coined while working the map is private until translated; persisted ungrounded, it becomes the canonical text the next session inherits and re-offends with.

## The map document

Format, ticket types, and the fog-of-war test are in
[references/map-format.md](references/map-format.md). Load it before charting a
map or adding a ticket to one.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session** - with the exception of research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `/grilling` and `/domain-modeling` session to pin down what this map is finding its way to - the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** - the way to the destination is already clear, the whole journey small enough for one session - you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues of the map - then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog - the **Not yet specified** section.
5. **Fire the research subagents.** For each **unblocked** `research` ticket you just created, **claim it first** (assign it, the same claim rule every session follows - an in-progress ticket must not look takeable on the frontier), then spin up a background research subagent to resolve it in parallel - each resolves its own ticket per the Research lifecycle in [Ticket Types](references/map-format.md#ticket-types). Blocked research tickets wait for their blockers like any other ticket. Concurrent subagents editing the map body can collide: re-read the map immediately before appending to Decisions-so-far, and re-apply on conflict.
6. Stop - charting is one session's work; it hand-resolves nothing itself (the research subagents from step 5 resolve their own tickets).

### Work through the map

User invokes with a map (URL or number). A ticket is **optional** - without one, you pick the next decision, not the user.

1. Load the **map** - the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. **Claim it**: assign it to yourself before any work.
3. Resolve it - **zoom as needed**: fetch the full body of any related or closed ticket on demand; invoke the skills the `## Notes` block names. If in doubt, use `/grilling` and `/domain-modeling`.
4. Record the resolution: post the answer as a **resolution comment** written per the [`conveying-clearly`](../conveying-clearly/SKILL.md) contract and its [text-that-outlives-the-session](../conveying-clearly/references/persisted-artifacts.md) mechanics (the decision first, then the why as consequences, vocabulary grounded), **close** the issue, and **append a context pointer** to the map's Decisions-so-far. A resolution comment is the canonical text future sessions inherit, so it earns the contract's strictest reading. If the resolution leaned on a coined term that now recurs across tickets, add its one-line gloss to the map's [Working vocabulary](references/map-format.md#working-vocabulary).
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals a ticket - this one or another - sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.
