<%*
const name = await tp.system.prompt("Organization name");
const rel = await tp.system.suggester(
  ["Client", "Prospect", "Partner", "Vendor", "Competitor"],
  ["client", "prospect", "partner", "vendor", "competitor"],
  false, "Relationship?");
const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
await tp.file.move(`People/${name}`);
-%>
---
type: org
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
scope: none
tags:
  - type/org
  - status/active
  - scope/none
  - org/<% slug %>
  - relation/<% rel %>
---

# <% name %>

## What they do

## Why they matter to us

## Who we deal with

## Open threads
