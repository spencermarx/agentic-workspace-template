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
scope: operators/spencer
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
| `relationship` | `internal` or `external` | person and org notes: which side of the house |
| `links` | map of label to URL | person and org notes: CRM record, profile, site |
| `supersedes` | wikilink | this note replaces another |

`relationship` is a property rather than a folder because people cross the line:
a contractor becomes an employee, an employee becomes an advisor. As folders
that is a rename, a broken wikilink, and a merge conflict; as a property it is a
one-line edit, and a saved view still presents the two groups separately.

`links` is deliberately a map rather than one property per vendor, so adding a
second CRM never reopens this table:

```yaml
links:
  crm: https://app.example.com/contacts/1234
  site: https://acme.example
```

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
| `Workspace/` | How the workspace works: standards, guide, templates, views | ships |
| `Business/` | This business's own functional domains | ships empty |
| `People/` | Person and organization notes | ships |
| `Decisions/` | Workspace-level decision records | ships |
| `Operators/` | One private working area per person | ships |
| `Attachments/` | Binaries. No notes, so no frontmatter | ships |
| `Meetings/` | Meeting notes, inside an operator's area | `./hq add` |
| `Daily Notes/` | An operator's dailies | `./hq add` |
| `Activities/`, `Documents/` | A domain's working notes and artifacts | `./hq add` |
| `decisions/` | A domain's own decision records | `./hq add` |

### Why exactly these ship

A folder ships if and only if this workspace defines the shape of what goes
inside it. Three things satisfy that, and nothing else does:

**Record types.** The note has a schema stated above: a value in the closed
`type` vocabulary plus its required frontmatter. `People/` and `Decisions/`
are these. A meeting note is a meeting note at any company, which is why the
template can carry a rule for it and a business never has to invent one.

**Ownership zones.** `Operators/` exists so single-writer isolation is
structural rather than a matter of etiquette. Its contents have no schema; its
path is the point. One person writes under `Operators/<key>/`, so nothing there
can ever produce a merge conflict.

**Structural slots.** `Workspace/` and `Business/` are fixed names whose
children are defined elsewhere -- by the template and by the business
respectively. `Business/` ships empty on purpose: the fixed name gives the rules
layer a stable glob target, so bootstrap fills it with `Sales/`, `Legal/`, or
whatever this business actually has **without ever rewriting a rule**.

Everything else is a **domain** -- the business's own partition of its own
activity -- and the template never guesses at one. There is no `type: client`,
so no `Clients/` folder ships.

The test, when it is ever unclear: *can the template write a `.claude/rules/`
pointer for this folder?* If the answer is no, the template knows nothing true
about what lives there, and it has no business shipping it.

A top-level folder added outside `Business/` matches no existing glob, so it
gets no routing until one is written. Registering that glob is part of creating
the folder, never a later cleanup.

## Scope

`scope` is the lowercase-kebab, slash-joined path of the owning folder, relative
to the vault root, with no file extension.

| Folder | `scope` |
|---|---|
| `Business/sales/` | `business/sales` |
| `Operators/operator/` | `operators/operator` |
| `People/` | `people` |
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
`[the agreement](<../../Legal/Master Agreement.pdf>)`.
