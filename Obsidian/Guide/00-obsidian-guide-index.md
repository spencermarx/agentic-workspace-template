---
type: moc
status: active
created: 2026-08-18
scope: none
tags:
  - type/moc
  - status/active
  - scope/none
---

# How this vault works

Two interfaces over the same files. **Obsidian is the human GUI**, **Claude Code
is the agentic GUI**, and both read and write the same Markdown in one git repo.

Nothing here is a rule. The rules live in
[Standards](../../Standards/README.md); these pages explain how to follow them.

## Start here

| If you want to | Read |
|---|---|
| Understand the folder layout | the root [CLAUDE.md](../../CLAUDE.md) |
| Know what a note must carry | [Frontmatter Guide](Frontmatter%20Guide.md) |
| Capture the day | [Daily Note Guide](Daily%20Note%20Guide.md) |
| Write up a meeting | [Meeting Note Guide](Meeting%20Note%20Guide.md) |
| Record a person or organization | [Person and Org Guide](Person%20and%20Org%20Guide.md) |
| Write down a decision | [Decision Record Guide](Decision%20Record%20Guide.md) |
| Park something for later | [Parking Lot Guide](Parking%20Lot%20Guide.md) |
| Run a research burst | [Research Bundle Guide](Research%20Bundle%20Guide.md) |
| Do a weekly cycle | [Weekly Cycle Guide](Weekly%20Cycle%20Guide.md) |
| Find things | [Finding Things](Finding%20Things.md) |

## The three layers

Every note uses all three, and each has one job.

1. **Frontmatter properties** are typed and queryable. The Bases views filter on
   them.
2. **Frontmatter tags** classify, and mirror the properties byte-identically.
3. **The body** uses `[[wikilinks]]` for entities and `#namespaced/tags` for
   recurring concepts. Entities are linked, concepts are tagged. Not the reverse.

## The views

`.obsidian/bases/` holds five saved views. The one to check regularly is
**inbox-triage**: it surfaces every note that breaks the frontmatter contract,
plus mirrors that have gone stale. If it is empty, the vault is clean.

## Creating a note

Use a template. `Ctrl/Cmd+T` inserts one. Templates move the file to the right
folder, write correct frontmatter, and in the case of a meeting note, link
themselves into the right daily note.

Creating notes by hand is how a vault drifts: the frontmatter contract is easy to
satisfy with a template and easy to forget without one.
