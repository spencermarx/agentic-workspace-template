---
type: moc
status: active
created: 2026-08-18
scope: none
tags: [type/moc, status/active, scope/none]
---

# Meeting notes

The template does three things for you: moves the file to `Meetings/<year>/`,
writes the frontmatter, and links the meeting into the chosen person's daily
note under its Meetings heading.

Format and the action-item contract:
[meeting-standards](../../Standards/meeting-standards.md).

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
