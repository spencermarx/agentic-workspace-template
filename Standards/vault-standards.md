# Vault standards

How notes are shaped, named, linked, and classified.

## Required frontmatter by note type

Every content note carries these five properties. No exceptions, and no empty
keys: if you do not have the value, you do not have the note yet.

```yaml
---
type: meeting/external
status: done
created: 2026-08-18
scope: clients/example-co
tags:
  - type/meeting/external
  - status/done
  - scope/clients/example-co
---
```

Conditional properties, added only when the note actually has the data:

| Property | Type | When |
|---|---|---|
| `updated` | date | any note edited after the day it was created |
| `date` | date | events: meetings, calls, decisions. Distinct from `created` |
| `people` | list of slugs | notes about or attended by people |
| `orgs` | list of slugs | notes about organizations |
| `stage` | closed vocabulary | pipeline notes only |
| `authors` | list of person slugs | any authored document |
| `related` | list of wikilinks | explicit cross-references |
| `canonical` | boolean | see `canonical-and-mirrors.md` |
| `canonical_source` | path | required when `canonical: false` |
| `canonical_ref` | string | git SHA or version, where one applies |
| `revised` | date | when a mirror was last re-synced |
| `supersedes` | wikilink | this note replaces another |

Anything not on these two lists is not a property. To add one, edit this section
in the same commit that introduces it.

`CLAUDE.md` files have no frontmatter and no tags. They are agent-instruction
documents, not notes.

## The closed vocabulary for type

The tag is `type/` plus the value, verbatim.

| Value | Note kind |
|---|---|
| `daily` | daily note |
| `weekly-review` | weekly retrospective |
| `weekly-goals` | weekly goal plan |
| `meeting/internal` | meeting, internal only |
| `meeting/external` | meeting with a party outside the workspace |
| `meeting/1-1` | one to one |
| `transcript` | raw or polished transcript |
| `person` | person note |
| `org` | organization note |
| `decision` | decision record |
| `note/prep` | preparation for a meeting or event |
| `note/analysis` | analysis or synthesis |
| `note/research` | a research receipt inside a dated bundle |
| `doc/spec` | specification or PRD |
| `doc/proposal` | proposal or statement of work |
| `doc/playbook` | how-to, runbook, service design |
| `doc/policy` | policy, charter, agreement |
| `moc` | map of content, index, folder README |
| `parking-lot` | an area's parking lot file |

Nineteen values. Closed. Adding one means editing this table.

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

## Property and tag mirroring

Every value of `type`, `status`, `scope`, and `stage` appears in `tags:` as
`<property>/<value>`, byte-identical, with no re-nesting and no reordering of
path segments.

`type: daily` gives `type/daily`. It does not give `type/note/daily`. Removing
the human judgment step is what keeps the two layers from drifting apart, and
it makes compliance checkable with one grep.

## Scope

`scope` is the lowercase-kebab, slash-joined path of the owning folder, relative
to the vault root, with no file extension.

| Folder | `scope` |
|---|---|
| `Clients/example-co/` | `clients/example-co` |
| `Products/thing/` | `products/thing` |
| `Business/` | `business` |
| workspace-level | `none` |

Because it is derived from the path it cannot drift into a second spelling.
`scope` is single-valued: a note that touches two areas picks its primary and
links to the other.

## File naming

Kebab-case when sequenced (`00-summary.md`, `01-findings.md`), descriptive
otherwise. Folders for instances are kebab-case; display names are Title Case
and live in the note, not the path. The separator in a filename is a hyphen
surrounded by spaces, never an em dash, which is both a voice violation and
hostile to shells.

## Links

`[[WikiLinks]]` for entities that resolve inside the vault: people,
organizations, meetings, decisions, areas. First mention per major section gets
a link; later mentions can be bare.

Markdown links with angle brackets for anything containing spaces and anything
outside the vault, so the link resolves outside Obsidian too:
`[the agreement](<../Legal/Master Agreement.pdf>)`.

## Tag namespaces

Nine, and the same taxonomy governs both frontmatter tags and body inline tags.

| Namespace | Purpose |
|---|---|
| `type/` | note kind, mirrors the `type` property |
| `status/` | note state, mirrors `status` |
| `scope/` | owning folder, mirrors `scope` |
| `stage/` | pipeline stage, mirrors `stage` |
| `area/` | ongoing responsibility |
| `topic/` | broad theme |
| `person/` | central person entities, mirrors `people` |
| `org/` | central organization entities, mirrors `orgs` |
| `relation/` | relationship type, on person and org notes |

All tags are namespaced, lowercase kebab, at least one level deep. There are no
flat tags: a flat tag breaks the tag pane's tree, which is the only reason the
taxonomy exists.

Add a namespace only when more than one note will use it, it does not fit an
existing one, and you can name the query you would run against it. Document it
in this table in the same commit.

## Tag list style

Block sequence only, one `- ` per line. Inline flow arrays are not permitted.

The reason is mechanical, not aesthetic: Obsidian's property editor rewrites an
inline array into a block sequence the next time anyone touches the note in the
GUI, producing a diff that looks like a content change. Pick the form the tool
writes.

## Inline tags in the body

Body `#tags` are for recurring concepts, never for entities. Entities are
wikilinks.

The bar: tag a concept only if it will appear in three or more unrelated notes
across the year, and you would want to find every note that mentions it. A
one-off reference stays bare.

## Ubiquitous language

Terms specific to this workspace live in `CONTEXT.md`, one definition each, with
the synonyms you are choosing against listed under `_Avoid_`. Define what a term
is, not what it does. A general concept that any workspace would share does not
belong there.

## Attachments and binaries

`Attachments/` holds only images the notes themselves produce: diagram exports,
screenshots, pasted images. Documents another system owns may live here or
stay in that system and be linked to. Neither is prescribed.
