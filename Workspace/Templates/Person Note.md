<%*
const name = await tp.system.prompt("Person's name");
const org = await tp.system.prompt("Organization (blank if none)", "");
const internal = await tp.system.suggester(
  ["External -- someone we deal with", "Internal -- on our team"],
  ["external", "internal"], false, "Which side of the house?");
// Block sequence rather than an inline flow array, because Obsidian's property
// editor rewrites the inline form on first touch and that shows up as a content
// diff nobody made. The leading newline lives inside the string so the key
// disappears entirely when there is no org, rather than shipping an empty list.
const orgSlug = org
  ? org.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")
  : "";
const orgsBlock = orgSlug ? `\norgs:\n  - ${orgSlug}` : "";
// Same conditional-block trick: the key disappears entirely when there is no
// URL, rather than shipping `links:` with an empty `crm:` under it. A property
// with no value is exactly what the frontmatter contract forbids, and an empty
// column is what a saved view renders forever.
const crm = await tp.system.prompt("CRM record URL (blank if none)", "");
const linksBlock = crm ? `\nlinks:\n  crm: ${crm}` : "";
// The filename is the person's name and nothing else. It used to carry the
// organization too, to make a person sort next to their employer -- but people
// change jobs, and that rename broke every wikilink pointing at them. `orgs`
// carries the association now, and a view does the grouping.
await tp.file.move(`People/${name}`);
-%>
---
type: person
status: active
created: <% tp.date.now("YYYY-MM-DD") %>
scope: none
relationship: <% internal %><% orgsBlock %><% linksBlock %>
---

# <% name %>

## Who they are

What they do, what they are trying to achieve, and what they are trying to prove
to whoever they answer to. That last one predicts their behaviour better than
their job title.

<!-- For someone internal, this is also where their role, the outcomes they own,
     and their current goals belong. That is shared information about them, and
     it lives here rather than in their own Operators/ folder, so the rest of the
     organization can read and edit it. -->

## How to work with them

How they prefer to communicate, how they decide, what they respond to, and what
loses them.

## History

<!-- Meetings that name this person link back here automatically. -->

## Notes

Working context only. No home addresses, identification numbers, financial or
health details. The test: would this be a normal thing for a colleague to have
written?
