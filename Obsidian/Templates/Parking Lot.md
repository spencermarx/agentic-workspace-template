<%*
const scope = await tp.system.prompt("Scope path this parking lot belongs to, e.g. Clients/example-co");
const title = scope.split("/").pop().replace(/-/g, " ").replace(/\b\w/g, c => c.toUpperCase());
const slug = scope.toLowerCase();
await tp.file.move(`${scope}/${title} - Parking Lot`);
-%>
---
type: parking-lot
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
scope: <% slug %>
tags:
  - type/parking-lot
  - status/active
  - scope/<% slug %>
---

# <% title %> - Parking Lot

Anything surfaced mid-work that is out of scope right now and must not be lost.

One of three registers, and they do not overlap. A committed near-term action
goes in this area's `CLAUDE.md` under "What's pending". A load-bearing unknown
goes under "Open questions".

Nothing is ever deleted. A triaged row moves to Archive marked `promoted`,
`dropped`, or `resolved`.

## Open items

| ID | Raised | By | Area | Item | Next step |
|---|---|---|---|---|---|

## Archive

| ID | Raised | Closed | Outcome | Item | Where it went |
|---|---|---|---|---|---|
