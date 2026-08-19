# Phase 3: playback and sign-off

Loaded on demand by the [`bootstrap`](../SKILL.md) skill. Write nothing until
the person approves.

Format the whole thing the way [`grilling`](../../grilling/SKILL.md) formats a
round: numbered, each item carrying the recommended answer on its own line so it
can be accepted in one word. That format was the best property of the interview
this replaced. It belongs here, at the confirmation, rather than at the opening
where it turned a conversation into a form.

## The three registers

Label every line as exactly one of:

- **confirmed**: they said it in Phase 1.
- **found**: Phase 2 has evidence, and the line carries the source path.
- **assumed**: neither. You are recommending it from the defaults below.

No fourth register, and never leave a line unlabelled. The whole value of the
playback is that the person can see instantly which lines deserve their
attention, and the assumed ones are the ones that deserve it.

## The six sections, in order

**1. What I understand you do.** One sentence, in their words. It becomes the
first paragraph of the root `CLAUDE.md` and is the highest-leverage sentence in
the workspace. Get this wrong and every later reader inherits the error.

**2. Your vocabulary.** The terms captured verbatim in Phase 1, and the synonyms
being chosen against. Seeds `CONTEXT.md`.

**3. What I found, and where.** The evidence table. Every row has a source path.
Include what was already on disk, and include the pointers that turned out to be
unreachable.

**4. What I could not determine.** Explicit, and never quietly filled in. These
become entries under Open questions, each naming what is unknown and what would
resolve it.

**5. What I propose, and why.** The rendered tree, then the recommendations
below, each with its one-line reason. Render the tree concretely rather than
describing it: reviewing a tree is ten times cheaper than specifying one.

**6. What I am assuming.** Every line that came out as *assumed*, gathered in
one place. Kept separate from 3 and 5 on purpose. Scrutiny is cheap when the
things needing it are in one list, and expensive when they are scattered through
a proposal that otherwise reads as settled.

Close with one question: **approve**, **edit**, or **start over on the shape**.
Offer `/clarify` if any of it did not land.

## The recommendation catalogue

Each is a default you propose, not a question you ask. Skip any that Phase 1 or
2 already settled, and say which phase settled it.

| Decision | Recommend | Because | Overturned by |
|---|---|---|---|
| Workspace name | The repo name, title-cased | Already correct, already theirs | They name it differently in Phase 1 |
| Second thing they have many of | A flat catalog of one note each, no folder, no `CLAUDE.md` | A catalog that grows into an area can be promoted with `new-area`; an area that should have been a catalog is a migration | Evidence that each one already accumulates its own documents |
| People | The plural container with one occupant: `Operators/<key>/`, even for one person | Renaming `Operator/` to `Operators/<key>/` later breaks every wikilink and pointer into it. Paying zero now avoids a migration | Nothing. Take this one even for a solo operator |
| House voice | Keep the two mechanical rules, no em dashes and no emojis, and ask what else | Two rules that can be checked beat ten that cannot | Anything they add, which goes into `Standards/writing-standards.md` |
| Lifecycle stages | Two homes: a note per prospect, promoted to a folder on signature | Folders are expensive to create and cheap to grow; notes are the reverse | A stage that already has its own documents on disk |
| Naming | kebab-case folders, Title Case in the leaf's H1 | kebab survives shells, git, and link syntax; the human name lives where humans read it | An existing convention found in Phase 2. Match it |
| Inside one instance | The two buckets: `Activities/<date> <name>/` for dated work, `Documents/<Family>/` for durable artifacts, plus a parking lot | See `Standards/document-patterns.md` | An existing sub-shape found in Phase 2 |
| When to create those | Lazily, on first use, never pre-created empty | An empty folder teaches an agent the folder is unused | Nothing |
| Cross-cutting folders | `People/` and `Meetings/` flat, no `CLAUDE.md` until either passes roughly fifty notes | A router over ten notes costs more than it routes | A count found in Phase 2 that is already past it |
| Business versus operator | Separate them only if the test says so: *would this content change if you replaced yourself with someone else doing the same job?* Yes means business, no means operator | The test is answerable per-item, so the split stops being a matter of taste | Their answer, which is theirs to give |
| Skills | Keep all of them. Everything unwired is already a flat file under `_stubs/` costing nothing | The real question is only whether an active skill is irrelevant here | They name one to drop |
| Sync | git is the substrate. Only raise iCloud if the Phase 2 probe found an iCloud Obsidian directory | Two sync mechanisms over one vault is a conflict generator | The probe found one |
| Tracking | The three in-vault registers, per `Standards/document-patterns.md` | An external tracker earns its place only against a need that already exists | A tracker already in use, found in Phase 2 |
| First real instances | The ones Phase 2 found, named | Naming them is the difference between a useful workspace in ten minutes and an empty one | Phase 2 found none, in which case ask for two or three |

## The bar

**Write nothing until the person approves.** Not the plan, not a folder, not a
placeholder. The engine's dry run in Phase 4 is the first thing that touches
disk, and it is reversible by definition.
