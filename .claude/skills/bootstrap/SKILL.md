---
name: bootstrap
description: >-
  Turn a fresh template clone into this person's workspace. Interviews for identity, the
  domain shape, and the people, writes a plan, then runs the deterministic engine and the
  authoring pass. User-invoked only, and only once per workspace. Do NOT use to add one
  client or venture to an existing workspace (use `new-area`) or to re-render managed
  blocks (run `./workspace render`).
disable-model-invocation: true
argument-hint: '[what this workspace is for]'
---

<!-- workspace:no-mutate -->

# bootstrap

You drive the conversation; deterministic scripts do every mutation. Gather what
only a human can decide, then call the engine. **Never hand-edit what a script
owns**: the tree, the folder map, or any managed block.

## Step 0: pre-flight, and do not ask what you can find out

Read `.workspace/workspace.json`. If `bootstrapped` is true, stop and ask which
steps to re-run; the engine needs `--force` and you should confirm before using it.

Then dispatch parallel `researcher` subagents and print one block of what you
already know, so the person can see you are not about to waste their time:

```bash
gh repo view --json name,owner,description 2>/dev/null   # repo identity
git config user.name; git config user.email              # the operator
gh auth status 2>&1 | head -3                            # is the GitHub step even possible
ls -d /Applications/Obsidian.app 2>/dev/null             # is Obsidian installed
ls -d ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents 2>/dev/null
find . -name '*.md' -not -path './.claude/*' -not -path './.workspace/*' \
       -not -path './Standards/*' -not -path './Obsidian/*' | head
```

That last one matters most. If the vault already has content, **record the shape
that exists** rather than proposing one.

## Step 1: the interview

Use the [`grilling`](../grilling/SKILL.md) frontier method. Ask every question
whose prerequisites are settled in one numbered round, each carrying a
recommendation the person can accept in a word. Recompute, ask the next round.

Full question set: [references/interview.md](references/interview.md).

The load-bearing question is the third one, and everything else falls out of it:

> **What do you have many of, where each one accumulates its own context over time?**

Clients, ventures, products, properties, cases, campaigns. That answer becomes a
top-level plural folder with one sub-folder and one leaf `CLAUDE.md` per
instance. It is why this template ships no domain profiles: a profile forces
someone to recognise their business in a stranger's taxonomy, while this question
is answerable in four seconds.

Always render a concrete proposed tree with the recommendation. Reviewing a tree
is ten times cheaper than specifying one.

## Step 2: write the plan, then dry run

Write `.workspace/plan.json` from the answers. The schema is
`.workspace/schema/plan.schema.json`; the three fixtures under
`.workspace/fixtures/` are worked examples of the three common shapes.

Then, always dry-run first and apply with the identical command:

```bash
./workspace bootstrap --plan .workspace/plan.json --dry-run
./workspace bootstrap --plan .workspace/plan.json
```

Show the dry run and get a yes before applying. If the engine prunes rules, say
which and why: it means those standards have no folder to govern here.

## Step 3: the authoring pass

The engine leaves `__REPLACE_ME__` sentinels and `<!-- AGENT: ... -->` comments
in every generated file. Walk them and replace each with real prose from the
interview, **deleting every comment as you go**.

This is where the workspace stops being a skeleton. Write for an agent that has
never seen it: if a sentence would be obvious from the artifacts, cut it.

Do not invent. Where the person did not tell you something, the honest output is
an entry under Open questions naming what is unknown and what would resolve it.

## Step 4: Obsidian

```bash
./workspace obsidian-setup
```

Quit Obsidian first; it rewrites plugin config from memory on quit, so an edit
made while it is running is discarded.

Then tell the person, in this order: open the repo root as a vault, **trust the
plugins when prompted**, and install the store plugins the command listed. A
fresh clone with plugins disabled looks broken, and people conclude the template
is broken.

## Step 5: hand off

Sweep the tree for a surviving `__REPLACE_ME__`, an unreplaced `{{TOKEN}}`, or
an unresolved `<!-- AGENT: -->` comment, and resolve every one before handing
off.

Then print `git status --short`, summarise what changed, and **do not commit**.
Print the command instead:

```
git add -A && git commit -m "chore: bootstrap this workspace"
```

The first commit of someone's workspace is theirs to make.

## Guardrails

- **Never hand-roll a `{{TOKEN}}`.** The engine owns them.
- **Confirm before anything outward-facing or irreversible**, including a repo
  rename.
- If a secret is needed, have the person paste it and pipe it straight to the
  tool that consumes it. Never echo it, write it to a file, or put it in a
  command argument that gets logged.
