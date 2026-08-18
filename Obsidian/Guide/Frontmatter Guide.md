---
type: moc
status: active
created: 2026-08-18
scope: none
tags: [type/moc, status/active, scope/none]
---

# Frontmatter

Five properties on every content note, no exceptions, and no empty keys. If you
do not have the value, you do not have the note yet.

```yaml
type: meeting/external
status: done
created: 2026-08-18
scope: clients/example-co
tags:
  - type/meeting/external
  - status/done
  - scope/clients/example-co
```

The normative tables, including every allowed value of `type` and `status` and
the conditional properties, are in
[vault-standards](../../Standards/vault-standards.md#required-frontmatter-by-note-type).
This page is the explanation, not the rule.

## The three that trip people up

**`status` has seven values and `completed` is not one of them.** Use `done`.
Two words for one state is how a taxonomy starts to rot, and the source vault
this template came from had both in circulation.

**Tags mirror properties byte for byte.** `type: daily` gives `type/daily`. It
does not give `type/note/daily`. There is no re-nesting and no judgment call,
which is exactly the point: the judgment call is where the drift entered.

**`scope` is derived from the folder path**, lowercase and slash-joined. A note
in `Clients/example-co/` has `scope: clients/example-co`. Because it is derived
rather than chosen, it cannot drift into a second spelling of the same thing.

## Why it matters

Every Bases view filters on these properties. A note without them is invisible to
every query in the vault: it exists, and nothing can find it.

The **inbox-triage** view exists to catch exactly that. Check it occasionally.
