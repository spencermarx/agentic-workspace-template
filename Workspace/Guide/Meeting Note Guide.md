---
type: moc
status: active
created: 2026-08-18
scope: none
---

# Meeting notes

The template does three things for you: moves the file to `Meetings/<year>/`,
writes the frontmatter, and links the meeting into the chosen person's daily
note under its Meetings heading.

It asks which area owns the meeting, because that answer is what the meetings
view groups by. `.` means workspace-level and becomes `scope: none`.

This page is the shape of a meeting note. There is no separate standard to check
against: the template emits it and this explains it, and those are the only two
places it exists.

## The sections, and why they are in that order

**Context** and **Agenda** are written before. **Notes**, **Decisions**, and
**Action items** during. **Follow-up** and **References** after.

The order is chronological on purpose. A note whose first heading is "Notes" is
a note written after the fact, and it will read as a transcript rather than as a
record of a meeting that went somewhere.

Anything that turns out to be durable leaves: a decision becomes a decision
record, an unknown becomes an area's Open question, a deferred item becomes a
parking-lot row. What stays behind is the account of the conversation.

## Before, not after

Create the note before the meeting, with `status: prep`, and fill Context and
Agenda. A note written only afterwards records what was said; a note written
beforehand shapes what gets said.

## Action items

`- [ ] verb phrase - @owner - YYYY-MM-DD`

An item with no owner is not an action item, it is a note. An item with no date
is a wish. This is the single highest-value discipline on this page: unowned
action items are the most common reason a meeting produces nothing.

## One meeting, several artifacts

A meeting with a transcript, an analysis, and a follow-up message becomes a
folder named `YYYY-MM-DD <Title>/`, with the siblings sharing that prefix. A
meeting with one artifact stays one file.

## Attendees are entities

Everyone present goes in `people` as a slug and gets a wikilink on first mention.
That is what turns a person note into a record of every conversation you have
had with them, without anyone maintaining it.
