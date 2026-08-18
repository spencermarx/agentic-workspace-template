<%*
const op = await tp.user.operators.pick(tp, "Whose daily note?");
const d = tp.date.now("YYYY-MM-DD");
const y = tp.date.now("YYYY");
const m = tp.date.now("MM");
await tp.file.move(`${tp.user.operators.home(op)}/Daily Notes/${y}/${m}/${d}`);
-%>
---
type: daily
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
date: <% tp.date.now("YYYY-MM-DD") %>
scope: operator/<% op.key %>
people:
  - <% op.key %>
tags:
  - type/daily
  - status/active
  - scope/operator/<% op.key %>
  - person/<% op.key %>
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
