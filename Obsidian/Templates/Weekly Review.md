<%*
const op = await tp.user.operators.pick(tp, "Whose review?");
const wk = tp.date.now("GGGG-[W]WW");
await tp.file.move(`${tp.user.operators.home(op)}/Weekly Reviews/${wk}`);
-%>
---
type: weekly-review
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
date: <% tp.date.now("YYYY-MM-DD") %>
scope: operator/<% op.key %>
people:
  - <% op.key %>
tags:
  - type/weekly-review
  - status/active
  - scope/operator/<% op.key %>
  - person/<% op.key %>
---

# Week <% wk %>

## What actually happened

Facts before interpretation. What shipped, what did not, what changed.

## What I learned

Distinguish what you now know from what you now suspect.

## What I got wrong

The section that makes the rest worth writing.

## Next week

Three things. Carry forward what genuinely matters, drop the rest rather than
letting it accumulate.

- [ ]
- [ ]
- [ ]
