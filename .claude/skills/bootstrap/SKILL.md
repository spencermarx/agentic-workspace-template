---
name: bootstrap
description: >-
  Turns a fresh template clone into this business's workspace: collects the identity the
  engine substitutes, sequences the skills that decide what to read, read it, and shape the
  vault, then runs the authoring pass and Obsidian setup. User-invoked, once per fork. Do
  NOT use to change the shape of a workspace that already exists (use `extend-architecture`)
  or to add one instance under an existing router (use `new-area`).
disable-model-invocation: true
argument-hint: '[what this workspace is for]'
---

<!-- workspace:no-mutate -->

# bootstrap

The first-run orchestrator, and nothing else. It owns the three things that
happen exactly once in a workspace's life -- the fresh-fork check, the identity
the engine substitutes everywhere, and the flip to `bootstrapped: true` -- and
it delegates everything else.

The substance lives in three skills, in this order:

1. [`investigation-brief`](../investigation-brief/SKILL.md) -- the conversation
   that decides what is worth reading
2. [`explore-context`](../explore-context/SKILL.md) -- the reading, and the
   playback that gets it confirmed
3. [`extend-architecture`](../extend-architecture/SKILL.md) -- the structural
   change itself

The order is the design. Reading before talking means probing blind, because
only the operator knows where the material is. Shaping before reading means
proposing a tree over a vault whose contents you have not seen.

Nothing here is special to day one except identity and the flag. The three
domains added during bootstrap and the fourth added three years later go through
the same skill, the same plan, and the same engine.

## Step 1: confirm this is a fresh fork

Read `.workspace/workspace.json`. If `bootstrapped` is true, stop. Say so, and
point at [`extend-architecture`](../extend-architecture/SKILL.md) for a shape
change or [`new-area`](../new-area/SKILL.md) for one instance. Do not offer to
re-run this skill.

**Done when:** you have read the file and `bootstrapped` is false.

## Step 2: collect identity, once

The engine substitutes identity into every file on the mutate surface at the
moment the plan is applied. Collect it before that happens, or the tokens go out
unreplaced and someone finds `{{WORKSPACE_NAME}}` in a note a year later.

Ask for, and write into `.workspace/workspace.json`:

- `workspaceName`, `slug`, `domain`, `primaryEmail`, `oneLiner`
- `people[]`, one entry per human: `key` (kebab), `display`, `emails[]`, and
  `default: true` on exactly one

`people[].emails` is what every path-coupled skill resolves the session email
against, so an operator with no email listed is invisible to the harness.

**Done when:** no `{{TOKEN}}` and no `__REPLACE_ME__` remains in
`.workspace/workspace.json`, and `people[]` has at least one entry carrying an
email and exactly one carrying `default: true`.

## Step 3: decide what to read

Invoke [`investigation-brief`](../investigation-brief/SKILL.md).

**Done when:** it returns a written brief and the operator has agreed to it.

## Step 4: read it

Invoke [`explore-context`](../explore-context/SKILL.md) with that brief.

**Done when:** it returns a digest the operator has confirmed in words. Not
"looks good" from you.

## Step 5: shape the vault

Invoke [`extend-architecture`](../extend-architecture/SKILL.md) with the digest.
On a fresh fork this is where `Business/` stops being empty and `Operators/`
gets one zone per person in `people[]`.

One thing is first-run and belongs here rather than in that skill: because the
workspace is not bootstrapped yet, the command that applies the plan is

```bash
./hq bootstrap --plan .workspace/plan.json --dry-run
./hq bootstrap --plan .workspace/plan.json
```

That run is what sets `bootstrapped: true`. Every application of the plan after
it, including every one in year three, is `./hq apply`.

**Done when:** `.workspace/workspace.json` has `bootstrapped: true` and every
folder the dry run listed exists on disk.

## Step 6: the authoring pass

The engine leaves `__REPLACE_ME__` sentinels and `<!-- AGENT: ... -->` comments
across the generated tree. Walk every one and replace it with real prose from
the brief and the digest, deleting each comment as you go.

This is where the workspace stops being a skeleton. Write for an agent that has
never seen it: if a sentence would be obvious from the artifacts, cut it. Do not
invent. Where nothing in Steps 3 and 4 answered something, the honest output is
an entry under Open questions naming what is unknown and what would resolve it.

**Done when:** a search of the tree for `__REPLACE_ME__`, `{{`, and
`<!-- AGENT:` returns only files the engine excludes by design (`.workspace/`,
`Workspace/Templates/`, `.credentials/`).

## Step 7: Obsidian

```bash
./hq obsidian-setup
```

Quit Obsidian first. It rewrites plugin config from memory on quit, so an edit
made while it is running is silently discarded.

Then tell the person, in this order: open the repo root as a vault, **trust the
plugins when prompted**, and install the store plugins the command listed. A
fresh clone with plugins disabled looks broken, and people conclude the template
is broken.

**Done when:** the command has run and you have relayed the plugin list it
printed, if any.

## Step 8: hand off

Run `./hq doctor`, then print `git status --short` and summarise what changed.

**Do not commit.** Print the command instead:

```
git add -A && git commit -m "chore: bootstrap this workspace"
```

The first commit of someone's workspace is theirs to make.

**Done when:** `doctor` reports clean and the operator has the commit command,
uncommitted.

## Guardrails

- **Never hand-roll a `{{TOKEN}}` or hand-edit what the engine owns**: the tree,
  the folder map, or any managed block. Change `plan.json` and re-apply.
- **Confirm before anything outward-facing or irreversible**, including a repo
  rename.
- If a secret is needed, have the person paste it and pipe it straight to the
  tool that consumes it. Never echo it, write it to a file, or put it in a
  command argument that gets logged.
