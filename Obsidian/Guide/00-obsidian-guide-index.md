---
type: moc
status: active
created: 2026-08-18
scope: none
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
| Find things | [Finding Things](Finding%20Things.md) |

## The two layers

Every note uses both, and each has one job.

1. **Frontmatter properties** are typed and queryable. The views filter on them,
   and there are only nine of them in total.
2. **The body** uses `[[wikilinks]]` for entities: people, organizations,
   meetings, decisions, areas. Linking rather than describing twice is what makes
   the backlink panel a complete record of where something came up.

## The views

[`Obsidian/Views/`](../Views) holds five saved views, and `Home.md` links each
one. They are ordinary vault files rather than config, so the file explorer
shows them and you can open one the way you open a note.

The one to check regularly is **inbox-triage**: it surfaces every note that
breaks the frontmatter contract. A note appearing there is a note that no other
view can find.

## Creating a note

Use a template. Command palette, "Templater: Open insert template modal", or
bind it to a key you like. Templates move the file to the right folder, write
correct frontmatter, and in the case of a meeting note, link themselves into the
right daily note.

Creating notes by hand is how a vault drifts: the frontmatter contract is easy to
satisfy with a template and easy to forget without one.

Templater is the only template engine here. Obsidian's own Templates and Daily
Notes core plugins are switched off in `core-plugins.json`, because they cannot
execute the `<%* %>` blocks these templates are built from and would paste the
script in as literal text. Create a daily note from the Daily Note template like
any other.
