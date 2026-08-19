<%*
const name = await tp.system.prompt("Organization name");
await tp.file.move(`People/${name}`);
-%>
---
type: org
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
scope: none
---

# <% name %>

## What they do

## How we relate

What the relationship is, and what each side wants out of it.

## Who we deal with

## Open threads
