---
type: moc
status: active
created: 2026-08-19
scope: none
---

# People

One note per entity this business deals with: people, and the organizations they
belong to. Contacts, collaborators, advisors, counterparts, and your own team.

This is the single source of truth for who someone is. A meeting mentions them,
a domain document assumes them, an agent needs their context -- all of it
resolves here rather than being restated in each place.

## Naming and association

The filename is the person's name, or the organization's name. Nothing else.

Association is carried in frontmatter, never in the filename or the folder:

- `orgs` links a person to the organizations they belong to.
- `relationship` is `internal` or `external`.
- `links` holds the CRM record and anything else vendor-specific, as a map, so
  the workspace never depends on which CRM this business uses.

Filenames used to carry the organization too, so a person sorted beside their
employer. People change jobs, and that rename broke every wikilink pointing at
them. `Workspace/Views/people.base` does the grouping now, which costs nothing
and survives the job change.

## Internal people have two homes, deliberately

A teammate's **profile** is here: their role, what they own, their goals. It is
shared, so two people editing it at once *should* conflict -- that is two people
changing something the organization agreed on.

Their **working area** is `Operators/<key>/`, which only they write to and which
therefore never conflicts.

Who they are is shared. Where they work is theirs.
