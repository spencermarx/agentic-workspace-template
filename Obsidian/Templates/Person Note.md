<%*
const name = await tp.system.prompt("Person's name");
const org = await tp.system.prompt("Organization (blank if none)", "");
const fname = org ? `${name} - ${org}` : name;
// Block sequence rather than an inline flow array, because Obsidian's property
// editor rewrites the inline form on first touch and that shows up as a content
// diff nobody made. The leading newline lives inside the string so the key
// disappears entirely when there is no org, rather than shipping an empty list.
const orgSlug = org
  ? org.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")
  : "";
const orgsBlock = orgSlug ? `\norgs:\n  - ${orgSlug}` : "";
await tp.file.move(`People/${fname}`);
-%>
---
type: person
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
scope: none<% orgsBlock %>
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
