---
name: new-area
description: >-
  Scaffold one new client, venture, product, offering, or area into an existing workspace,
  with the correct CLAUDE.md tier, the standard sub-shape, a parking lot, and the parent's
  inventory re-rendered. Use whenever a new instance of something the workspace already has
  many of comes into being. Do NOT use for the first setup of a workspace (use `bootstrap`)
  or to create an ordinary note (use an Obsidian template).
argument-hint: '<name> [as a client|venture|product|offering]'
---

<!-- workspace:no-mutate -->

# new-area

Used far more often than [`bootstrap`](../bootstrap/SKILL.md), and it exists
because of a specific failure: six months in, a new client arrives and someone
hand-creates the folder. They get a `CLAUDE.md` with the wrong sections, the
wrong relative depth in its upward pointer, and no row in the parent's inventory.
It looks right and it is subtly wrong, and the next one is wrong differently.

This is `bootstrap` restricted to one node: same plan, same templates, same
renderer, same gate.

## Step 1: read, do not ask

Load `.workspace/workspace.json` and `.workspace/plan.json`. Refuse if
`bootstrapped` is false: there is no plan to append to, so run `bootstrap` first.

**Infer the parent from the name.** If exactly one node declares an
`instanceTemplate`, that is the parent and there is no question to ask. "Add Acme
as a client" resolves without a single prompt when only `Clients` takes
instances.

Ask only when it is genuinely ambiguous:

- Two or more candidate parents. Ask which, with a recommendation.
- A name that matches no container. Then the one question is: *is this a new
  instance of something that exists, or a new kind of thing?* The second answer
  means a new container, which is a bigger change and deserves saying so.

## Step 2: preview, then apply

```bash
./workspace add --parent Clients --name "Acme Corp" --dry-run
./workspace add --parent Clients --name "Acme Corp"
```

The engine appends a node to the plan, creates the folder with the parent's
declared sub-shape, writes the `CLAUDE.md` from the right template with computed
relative depth, creates the parking lot, and **re-renders the parent's inventory
and the root folder map**.

That last part is the point. The folder map cannot drift because nobody writes it.

## Step 3: author it

Fill every `__REPLACE_ME__` and act on every `<!-- AGENT: -->` comment, using
whatever the person just told you about this client, venture, or product.

The **TL;DR for picking up cold** section is the one worth spending time on. It
is what an agent reads six months from now with no other context.

Where you do not know something, write it as an Open question naming what is
unknown and what would resolve it. A leaf full of confident invention is worse
than a thin one that is honest.

## Step 4: gate, then hand off

```bash
./workspace validate
```

Then summarise and stop. **Do not commit.**

## Promoting rather than creating

Two cases worth recognising, because both look like "create a new area" and
neither is:

- **A pipeline note becoming a real engagement.** `git mv` the existing note into
  the new folder and use it to seed the leaf's TL;DR. The thinking that won the
  work is the best possible starting context, and recreating it from scratch
  loses it.
- **A catalog entry growing into an area.** A note that has outgrown one file
  becomes a folder. Same move: move the note in, do not rewrite it.
