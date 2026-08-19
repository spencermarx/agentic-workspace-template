<%*
// This picks the owner, not just a backlink target. A meeting note lives in the
// note-taker's own area, which is the only place in the vault with a single
// writer, so two people in one meeting keep two accounts and neither can
// conflict with the other.
const op = await tp.user.operators.pick(tp, "Whose notes are these?");
const title = await tp.system.prompt("Meeting title");
const kind = await tp.system.suggester(
  ["External", "Internal", "One to one"],
  ["meeting/external", "meeting/internal", "meeting/1-1"],
  false, "What kind of meeting?");
// The meetings view groups by scope. Hardcoding it collapsed every meeting into
// a single group called "none", so it is asked for.
const rawScope = await tp.system.prompt(
  "Owning area folder, e.g. Business/sales, or . for workspace-level", ".");
const scope = (!rawScope || rawScope === ".")
  ? "none"
  : rawScope.toLowerCase().replace(/^\/+|\/+$/g, "");
const d = tp.date.now("YYYY-MM-DD");
const name = `${d} ${title}`;
await tp.file.move(`${tp.user.operators.home(op)}/Meetings/${tp.date.now("YYYY")}/${name}`);
-%>
---
type: <% kind %>
status: prep
created: <% d %>
date: <% d %>
scope: <% scope %>
people:
  - <% op.key %>
---

# <% name %>

<%*
// Backlink into the operator's daily note, so the day's record is complete
// without anyone maintaining it by hand.
const dailyPath = `${tp.user.operators.home(op)}/Daily Notes/${tp.date.now("YYYY")}/${tp.date.now("MM")}/${d}.md`;
const daily = app.vault.getAbstractFileByPath(dailyPath);
if (daily) {
  const body = await app.vault.read(daily);
  const link = `- [[${name}]]`;
  if (!body.includes(link)) {
    await app.vault.modify(daily, body.replace(/^## Meetings\s*$/m, `## Meetings\n\n${link}`));
  }
}
-%>

## Context

Why this meeting is happening, and what a good outcome looks like.

## Agenda

## Notes

## Decisions

## Action items

Every item carries an owner and a date. An item with no owner is a note, not an
action; file it under Decisions or in the area's Open questions instead.

- [ ] verb phrase - @owner - YYYY-MM-DD

## Follow-up

## References
