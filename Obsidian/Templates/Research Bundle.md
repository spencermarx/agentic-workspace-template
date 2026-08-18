<%*
const scope = await tp.system.prompt("Scope path, e.g. Clients/example-co");
const topic = await tp.system.prompt("Research topic");
const slug = topic.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const d = tp.date.now("YYYY-MM-DD");
await tp.file.move(`${scope}/Documents/Research/${slug}-${d}/00-summary`);
-%>
---
type: note/analysis
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
scope: <% scope.toLowerCase() %>
tags:
  - type/note/analysis
  - status/draft
  - scope/<% scope.toLowerCase() %>
---

# <% topic %>

Pointer document. The numbered files beside it are the receipts.

State conclusions here and link the evidence. Do not put new material in a
summary: a finding that exists only here has no receipt.

New research lands as a new dated bundle. It never overwrites this one.

## What we concluded

-

## The receipts

| File | Covers |
|---|---|

## What we did not establish

-
