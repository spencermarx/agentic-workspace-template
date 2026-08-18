<%*
const name = await tp.system.prompt("Person's name");
const org = await tp.system.prompt("Organization (blank if none)", "");
const rel = await tp.system.suggester(
  ["Client", "Prospect", "Partner", "Vendor", "Advisor", "Contact"],
  ["client", "prospect", "partner", "vendor", "advisor", "contact"],
  false, "Relationship?");
const slug = name.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
  .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const fname = org ? `${name} - ${org}` : name;
await tp.file.move(`People/${fname}`);
-%>
---
type: person
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
scope: none
orgs: [<% org ? org.toLowerCase().replace(/[^a-z0-9]+/g, "-") : "" %>]
tags:
  - type/person
  - status/active
  - scope/none
  - person/<% slug %>
  - relation/<% rel %>
---

# <% fname %>

## Who they are

What they do, what they are trying to achieve, and what they are trying to prove
to whoever they answer to. That last one predicts their behaviour better than
their job title.

## How to work with them

How they prefer to communicate, how they decide, what they respond to, and what
loses them.

## History

<!-- Meetings that name this person link back here automatically. -->

## Notes

Working context only. No home addresses, identification numbers, financial or
health details. The test: would this be a normal thing for a colleague to have
written?
