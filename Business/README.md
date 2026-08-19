---
type: moc
status: active
created: 2026-08-19
scope: none
---

# Business

Everything this business does, one folder per functional domain: `Sales/`,
`Marketing/`, `Finance/`, `Legal/`, `Operations/`, or whatever this business
actually has.

It ships empty on purpose. The template cannot know which domains you have, and
guessing produces someone else's org chart. `./hq bootstrap` names them with
you, and adds more later as the business grows.

## Why the folder exists when it holds nothing

The name is fixed so the rules layer has something stable to point at. Every
rule that governs business notes globs `**/Business/**`, so a domain added here
inherits frontmatter, naming, and confidentiality routing the moment it is
created, with no rule rewritten.

A top-level folder added anywhere else matches none of those globs and gets no
routing at all, silently. That is the whole reason to put a domain here rather
than at the vault root.

## Inside a domain

`Activities/` for dated work, `Documents/` for durable artifacts, a parking lot
for what surfaced but is out of scope, and `decisions/` for choices that bind
only this domain. Workspace-wide decisions belong in `Decisions/` at the root.

Meetings do not live here. They belong to whoever took the notes, under
`Operators/<key>/Meetings/`, and reach a domain through `scope` rather than
through their folder.
