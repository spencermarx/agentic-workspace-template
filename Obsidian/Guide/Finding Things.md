---
type: moc
status: active
created: 2026-08-18
scope: none
---

# Finding things

Three ways, in the order worth trying.

## 1. The saved views

[`Obsidian/Views/`](../Views) answers the recurring questions without a search,
and every one is linked from `Home.md`:

| View | Answers |
|---|---|
| [inbox-triage](../Views/inbox-triage.base) | what is broken or unfinished |
| [meetings](../Views/meetings.base) | when did we last speak, and about what |
| [people](../Views/people.base) | who have I not touched in longest |
| [decisions](../Views/decisions.base) | what did we decide, and is it still current |
| [active-work](../Views/active-work.base) | what is actually live right now |

They live in the vault rather than in `.obsidian/`, because a view the file
explorer will not show you is a view nobody opens.

## 2. Backlinks

Open a person, an organization, or a decision and read its backlinks. Because
entities are wikilinked rather than described twice, the backlink panel is a
complete record of where that thing came up.

## 3. Search

Full text last, not first. If you are searching for something that a view or a
backlink should have surfaced, that is usually a sign the note is missing
frontmatter rather than a sign the search is bad. Check inbox-triage.
