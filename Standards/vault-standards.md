# Vault standards

How notes are shaped, named, linked, and classified.

## Required frontmatter by note type

Every content note carries these four properties. No exceptions, and no empty
keys: if you do not have the value, you do not have the note yet.

```yaml
---
type: meeting/external
status: done
created: 2026-08-18
scope: areas/example-area
---
```

Tagging is free-form and optional. Nothing queries `tags`, so use them however
they help you navigate, or not at all.

Conditional properties, added only when the note actually has the data:

| Property | Type | When |
|---|---|---|
| `date` | date | events: meetings, calls, decisions. Distinct from `created` |
| `people` | list of slugs | notes about or attended by people |
| `orgs` | list of slugs | notes about organizations |
| `supersedes` | wikilink | this note replaces another |

Anything not on these two lists is not a property. To add one, edit this section
in the same commit that introduces it.

`CLAUDE.md` files have no frontmatter. They are agent-instruction documents, not
notes.

## The closed vocabulary for type

| Value | Note kind |
|---|---|
| `daily` | daily note |
| `meeting/internal` | meeting, internal only |
| `meeting/external` | meeting with a party outside the workspace |
| `meeting/1-1` | one to one |
| `person` | person note |
| `org` | organization note |
| `decision` | decision record |
| `moc` | map of content, index, folder README |
| `parking-lot` | an area's parking lot file |

Closed. Adding a value means editing this table.

## The closed vocabulary for status

| Value | Means |
|---|---|
| `draft` | being written, not usable yet |
| `prep` | scaffolded ahead of an event that has not happened |
| `active` | live and in use |
| `blocked` | cannot progress, with the blocker named in the body |
| `done` | finished |
| `superseded` | replaced, with `supersedes` on the replacement pointing here |
| `archived` | kept for provenance, no longer consulted |

`completed` is not a value. Use `done`. Two words for one state is how a
taxonomy starts to rot.

## The reserved folder vocabulary

These folder names carry meaning: rules route by them, skills resolve paths
through them, and `scope` is derived from them. Treat them as reserved.

| Folder | Holds | Created by |
|---|---|---|
| `Standards/` | Conventions, stated once | ships |
| `Obsidian/` | Vault mechanics: guides, templates, views | ships |
| `Decisions/` | Workspace-level decision records | ships |
| `Meetings/` | Meeting notes | ships |
| `People/` | Person and organization notes | ships |
| `Attachments/` | Binaries. No notes, so no frontmatter | ships |
| `Areas/` | The router over whatever this business does many of | bootstrap |
| `Operators/` | One working area per person | bootstrap |
| `Activities/`, `Documents/` | An area's working notes and artifacts | `./workspace add` |
| `Daily Notes/` | An operator's dailies | `./workspace add` |
| `decisions/` | An area's own decision records | `./workspace add` |

`Areas/` and `Operators/` are the two a business renames: a firm may call them
`Clients/` and `Partners/`, a fund `Portfolio/` and `Principals/`. Renaming one
is a supported choice, made once at bootstrap, and it obligates the glob rewrite
that [harness-standards § Rule authoring contract](./harness-standards.md#rule-authoring-contract)
describes.

The vocabulary is not yours to extend mid-flight. A new top-level folder is a
bootstrap-time or `./workspace add` decision, never something a note-writing
session invents.

## Scope

`scope` is the lowercase-kebab, slash-joined path of the owning folder, relative
to the vault root, with no file extension.

| Folder | `scope` |
|---|---|
| `Areas/example-area/` | `areas/example-area` |
| `Operators/operator/` | `operators/operator` |
| `Meetings/` | `meetings` |
| workspace-level | `none` |

Because it is derived from the path it cannot drift into a second spelling.
`scope` is single-valued: a note that touches two areas picks its primary and
links to the other.

## File naming

Kebab-case when sequenced (`00-summary.md`, `01-findings.md`), descriptive
otherwise. The separator in a filename is a hyphen surrounded by spaces, never
an em dash, which is both a voice violation and hostile to shells.

## Links

`[[WikiLinks]]` for entities that resolve inside the vault: people,
organizations, meetings, decisions, areas.

Markdown links with angle brackets for anything containing spaces and anything
outside the vault, so the link resolves outside Obsidian too:
`[the agreement](<../Legal/Master Agreement.pdf>)`.
