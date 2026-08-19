# The CLAUDE.md contract

Nested `CLAUDE.md` files are how context is progressively disclosed: the root
establishes identity and conventions, intermediate files route, and leaves carry
the depth. This document defines the tiers and what belongs in each.

## The three tiers

| Tier | Target | Getting heavy | Job |
|---|---|---|---|
| Root | 4 KB | 8 KB | Identity, folder map, always-on invariants, person resolution |
| Router | 0.5 to 2.5 KB | 3.5 KB | What is here, which child to read next. Inventory only |
| Leaf | 8 to 14 KB | 20 KB | Everything needed to work in this area cold |

Nothing enforces those sizes. They are the point at which a file has stopped
paying for the tokens it costs on every request into its subtree, and the cue to
move depth behind the context router table below.

Folders that carry neither, such as `Meetings/`, `People/`, and `Attachments/`,
get a five-line `README.md` if they need any explanation at all.

## Assigning a tier

Apply in order.

1. **Does this folder contain another folder that will get its own
   `CLAUDE.md`?** Then it is a **router**. A router's only job is to point down.
2. Otherwise apply the **engagement test**: can you hand an agent this folder
   path plus a task, and have it complete the task correctly after reading only
   the root `CLAUDE.md`, `Standards/`, and this file? If yes, it is a **leaf**.
3. Neither? No `CLAUDE.md`.

Depth limit: three `CLAUDE.md` levels below root. Needing a fourth means the
tree is wrong.

## Promotion and demotion

A section inside a leaf that outgrows the rest of the file gets promoted into
its own subfolder with its own leaf. A router whose children are all thin gets
demoted, collapsing them back into one leaf.

## The always-on paragraph

Every root carries this, verbatim:

> This is the root context. Each major folder has its own `CLAUDE.md` that
> extends or overrides what is here (progressive disclosure). Read the one for
> the area you are working in.
>
> Conventions that apply everywhere (voice, frontmatter, document patterns)
> live in `Standards/`. Read `Standards/README.md` before writing or
> restructuring any note. Do not restate those rules here or in any other
> `CLAUDE.md`; point at them.

## The inheritance sentence

Every leaf carries this under its Working norms heading, verbatim:

> These extend the workspace root and `<Parent>/CLAUDE.md` conventions. Where
> they conflict, these win.

## The upward pointer

Every leaf ends with a horizontal rule and this paragraph:

> Parent context lives at the workspace root `CLAUDE.md` (N directories up),
> `<Parent>/CLAUDE.md` (one up), and `Standards/`. This workspace inherits those
> conventions unless explicitly overridden above.

Relative depth is computed by the engine, never written by hand. A leaf four
levels deep needs four levels of `..`, and getting it wrong produces a dangling
link that reads as correct.

## The context router table

The highest-value artifact in a leaf. It tells an agent what to load and when,
so the leaf itself can stay small.

| File | When to load |
|---|---|
| `path` | **Always load** for any X task. What it contains, in enough detail to decide without opening it. State the read cost. |
| `path` | Load for any Y task. |
| `path` | EXTERNAL (read-only, not in vault). What it is and why you would open it. |

Rows may point outside the vault. The router covers the whole surface an agent
needs, not only the part that happens to live here.
