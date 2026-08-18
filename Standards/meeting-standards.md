# Meeting standards

## Meeting note format

A fixed spine, so an agent reading any meeting note knows where to look:

```markdown
## Context
## Agenda
## Notes
## Decisions
## Action items
## Follow-up
## References
```

Headings carry no emoji. Where one was providing a visual affordance, use a
callout inside the section instead.

A meeting with more than one artifact becomes a folder named
`YYYY-MM-DD <Meeting Name>/`, with the note and its siblings sharing that
prefix: `... - Transcript.md`, `... - Analysis.md`, `... - Follow-up.md`. A
meeting with one artifact stays a single file.

## Action items carry an owner and a date

Every action item is `- [ ] <verb phrase> - @<owner> - <YYYY-MM-DD>`.

An item with no owner is not an action item, it is a note. File it under
Decisions if it was settled, or under the area's Open questions if it was not.
An item with no date is a wish.

## Attendees are entities

Every attendee appears in the `people` property as a slug and as a
`person/<slug>` tag, and is wikilinked on first mention in the body. An external
meeting also carries the counterpart organization in `orgs`.

This is what makes the meetings and people views queryable, and what turns a
person note into a record of every conversation you have had with them.
