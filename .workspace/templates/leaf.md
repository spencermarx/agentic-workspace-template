<!-- workspace:node {{NODE_PATH}} template=leaf tv={{TEMPLATE_VERSION}} -->
# {{NODE_TITLE}} - Workspace Context

<!-- AGENT: one paragraph. What this is, why it exists, and its relationship to
     the rest of the workspace. If the area is soft-parked, the status banner
     goes here as a bold second sentence, not as a folder move. Delete this
     comment. -->
__REPLACE_ME__

## TL;DR for picking up cold

<!-- AGENT: enough that an agent with zero prior context can hold a competent
     conversation. Keep the bold labels. Delete this comment. -->

**What it is:** __REPLACE_ME__

**Who's involved:**
- **__REPLACE_ME__**: what they own here

**Current state (as of {{TODAY}}):**
- __REPLACE_ME__

**The shape of the deal:** __REPLACE_ME__

## Where context lives (progressive disclosure)

Two buckets. `Documents/<Family>/` for durable artifacts,
`Activities/<YYYY-MM-DD> <activity name>/` for dated, time-stamped work. See
[document-patterns § Two buckets per area]({{REL_TO_ROOT}}/Standards/document-patterns.md#two-buckets-per-area).

<!-- workspace:context-table:start -->
| File | When to load |
|---|---|
<!-- workspace:context-table:end -->

## Working norms

These extend the workspace root and `{{PARENT_TITLE}}/CLAUDE.md` conventions.
Where they conflict, these win.

<!-- AGENT: only the DELTAS from the workspace defaults. If there are none,
     write "No local overrides." Do not restate anything in Standards/. Delete
     this comment. -->

### Ubiquitous language

| Term | Means | Does not mean |
|---|---|---|

### What not to do

-

## Open questions (load-bearing assumptions)

<!-- AGENT: each one states why it is load-bearing, which decision depends on
     it, and what would resolve it. An unknown that changes nothing is not an
     open question. Delete this comment. -->

-

## Anti-patterns specific to this area

-

## Recent activity

Reverse-chronological. Three lines maximum per entry; anything longer becomes a
dated note under `Activities/` that the entry links to.

- **{{TODAY}}:** area created.

## What's pending

Committed near-term actions only. Deferred items go to the Parking Lot,
strategic unknowns to Open questions above. See
[document-patterns § The three registers]({{REL_TO_ROOT}}/Standards/document-patterns.md#the-three-registers).

-

---

Parent context lives at the workspace root `CLAUDE.md` ({{REL_TO_ROOT}}/CLAUDE.md), `{{PARENT_TITLE}}` ({{REL_TO_PARENT}}/CLAUDE.md), and `Standards/`. This area inherits those conventions unless explicitly overridden above.
