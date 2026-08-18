<%*
const op = await tp.user.operators.pick(tp, "Whose goals?");
const wk = tp.date.now("GGGG-[W]WW");
await tp.file.move(`${tp.user.operators.home(op)}/Weekly Goals/${wk}`);
-%>
---
type: weekly-goals
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
date: <% tp.date.now("YYYY-MM-DD") %>
scope: operator/<% op.key %>
people:
  - <% op.key %>
tags:
  - type/weekly-goals
  - status/active
  - scope/operator/<% op.key %>
  - person/<% op.key %>
---

# Goals, week <% wk %>

## The one thing

If only one thing happens this week, this is it.

## Also

- [ ]
- [ ]

## Explicitly not this week

Naming what you are not doing is what makes the list above true.

-
