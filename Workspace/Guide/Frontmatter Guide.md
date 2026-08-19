---
type: moc
status: active
created: 2026-08-18
scope: none
---

# Frontmatter

Four properties on every content note, no exceptions, and no empty keys. If you
do not have the value, you do not have the note yet.

```yaml
type: meeting/external
status: done
created: 2026-08-18
scope: clients/example-co
```

Four more are conditional, added only when the note has the data: `date`,
`people`, `orgs`, `supersedes`. Anything not on one of those two lists is not a
property at all.

There is deliberately no `updated`. A hand-written date stamp goes stale the
first time someone edits without touching it, so the views read `file.mtime`
instead and get it right for free.

The normative tables, including every allowed value of `type` and `status`, are
in
[vault-standards](../Standards/vault-standards.md#required-frontmatter-by-note-type).
This page is the explanation, not the rule.

## The two that trip people up

**`status` has seven values and `completed` is not one of them.** Use `done`.
Two words for one state is how a taxonomy starts to rot, and the source vault
this template came from had both in circulation.

**`scope` is derived from the folder path**, lowercase and slash-joined. A note
in `Clients/example-co/` has `scope: clients/example-co`. Because it is derived
rather than chosen, it cannot drift into a second spelling of the same thing.

## `type` is nine values, and the templates cover all of them

`daily`, `meeting/internal`, `meeting/external`, `meeting/1-1`, `person`, `org`,
`decision`, `moc`, `parking-lot`.

Every one of those except `moc` is written by a template, so in practice you
only type a `type` by hand when you are writing an index page. If you find
yourself wanting a tenth value, that is a change to the table in vault-standards
and a decision record, not a judgment call at the top of one note.

## Why it matters

Every Bases view filters on these properties. A note without them is invisible to
every query in the vault: it exists, and nothing can find it.

The **inbox-triage** view exists to catch exactly that. Check it occasionally.
