<%*
const name = await tp.system.prompt("Organization name");
const relationship = await tp.system.suggester(
  ["External -- a company we deal with", "Internal -- part of this business"],
  ["external", "internal"], false, "Which side of the house?");
// Conditional block, so the key disappears rather than shipping an empty value.
// This is the account-level record, so the URL here is the company in the CRM,
// not any one contact.
const crm = await tp.system.prompt("CRM record URL (blank if none)", "");
const linksBlock = crm ? `\nlinks:\n  crm: ${crm}` : "";
await tp.file.move(`People/${name}`);
-%>
---
type: org
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
scope: none
relationship: <% relationship %><% linksBlock %>
---

# <% name %>

## What they do

## How we relate

What the relationship is, and what each side wants out of it.

## Who we deal with

## Open threads
