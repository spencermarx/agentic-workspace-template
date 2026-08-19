<%*
const op = await tp.user.operators.pick(tp, "Whose daily note?");
const d = tp.date.now("YYYY-MM-DD");
const y = tp.date.now("YYYY");
const m = tp.date.now("MM");
// scope is derived from the folder the file actually lands in, so the two
// cannot drift apart the way a hardcoded string did.
const home = tp.user.operators.home(op);
const scope = home.toLowerCase();
await tp.file.move(`${home}/Daily Notes/${y}/${m}/${d}`);
-%>
---
type: daily
status: active
created: <% d %>
date: <% d %>
scope: <% scope %>
people:
  - <% op.key %>
---

# <% tp.date.now("dddd, MMMM D, YYYY") %>

## Top three

Three, not five. If everything is a priority, nothing is.

- [ ]
- [ ]
- [ ]

## Notes

## Meetings

## End of day

**Landed:**

**Carried:**

**Worth remembering:**
