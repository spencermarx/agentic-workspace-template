# The bootstrap interview

Loaded on demand by the [`bootstrap`](../SKILL.md) skill. Four frontier rounds.

Format every question the way [`grilling`](../../grilling/SKILL.md) does: a
numbered question with a title, then a recommendation on its own line that can be
accepted in one word. Skip any question Step 0 already answered.

## Round 1: no prerequisites

**Q1, workspace name.** The display name in the root `CLAUDE.md`, `Home.md`, and
the Obsidian window title. Default from the repo name.

**Q2, one-liner.** One sentence telling a cold agent what this vault is for. It
becomes the first paragraph of the root `CLAUDE.md` and is the highest-leverage
sentence in the workspace.

**Q3, primary multiplicity.** *What do you have many of, where each one
accumulates its own context over time?* This determines the shape of everything.
Common answers: clients, ventures, products, properties, cases, portfolio
companies, campaigns.

**Q4, secondary multiplicity.** Is there a second, independent thing you have
many of that does not nest under the first? Usually the honest answer is that the
second thing is a small stable **catalog** rather than a growing set of
context-accumulating folders. A catalog is one note each, no folder, no
`CLAUDE.md`. Recommend that, and note it can be promoted later with `new-area`.

**Q5, people.** How many humans read and write this vault, and does each need a
private area?

Recommend the **plural container with a single occupant**: `Operators/<key>/`,
even for one person. The container costs nothing today, and renaming
`Operator/` to `Operators/<key>/` later breaks every wikilink and every pointer
into it. This is the one place where paying zero now avoids a migration.

**Q6, voice.** `Standards/writing-standards.md` carries only the two mechanical
rules, no em dashes and no emojis. Ask what else the house voice should say, and
write the answer into that file.

## Round 2: unblocked by the shape

**Q7, lifecycle.** Which stages get a **folder** with its own context, and which
get a **note**? Folders are expensive to create and cheap to grow; notes are the
reverse.

The usual right answer is two homes: a note per prospect in a pipeline, promoted
to a folder on signature. Recommend it.

**Q8, naming.** kebab-case folders, Title Case display in the leaf's H1, and an
Obsidian folder note carrying the human name. kebab survives shells, git, and
link syntax; the human name lives where humans read it.

**Q9, the inside of one instance.** The fixed sub-shape every instance is
scaffolded with. Recommend the two-bucket pattern: `Activities/<date> <name>/`
for dated work, `Documents/<Family>/` for durable artifacts, plus a parking lot.

Create these lazily, on first use, never pre-created empty. An empty folder
teaches an agent that the folder is unused.

**Q10, cross-cutting folders.** `People/` and `Meetings/` are ambient: flat, no
`CLAUDE.md` until either exceeds roughly fifty notes.

**Q11, business versus operator.** Does the enterprise get a folder distinct from
the person running it? The test: *would this content change if you replaced
yourself with someone else doing the same job?* Yes means it belongs to the
business, no means it belongs to the operator.

## Round 3: unblocked by the tree

**Q12, skills.** Which of the shipped skills stay? Everything unwired is already
a flat file under `_stubs/` costing nothing, so the real question is only whether
any active skill is irrelevant here.

**Q13, sync.** Only ask if Step 0 found an iCloud Obsidian directory. Otherwise
say plainly that git is the sync substrate and move on.

**Q14, tracking.** Where committed work is recorded. Recommend the three in-vault
registers, and add an external tracker only if a real need already exists.

**Q15, first real instances.** Name the two or three that exist today. Naming
them now is the difference between a useful workspace in ten minutes and an empty
one.

## Round 4: the frontier is empty

Render the proposed tree, with the byte count you expect for each `CLAUDE.md`.
Ask a single question with three options: approve, edit the tree, or start over
on the shape.

Write nothing until that returns.
