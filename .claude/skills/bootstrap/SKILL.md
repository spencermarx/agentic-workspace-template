---
name: bootstrap
description: >-
  Turn a fresh template clone into this person's workspace. Talks first, then goes and reads
  what they pointed at, then plays back everything gathered for sign-off before writing a
  byte. Runs the deterministic engine and the authoring pass. User-invoked only, and only
  once per workspace. Do NOT use to add one client or venture to an existing workspace (use
  `new-area`) or to re-render managed blocks (run `./hq render`).
disable-model-invocation: true
argument-hint: '[what this workspace is for]'
---

<!-- workspace:no-mutate -->

# bootstrap

Three phases, in this order, and the order is the whole design:

1. **Conversation.** Understand their world in their words. Read nothing.
2. **Exploration.** Go and read what they pointed at. Write nothing.
3. **Playback.** Show everything gathered, get sign-off. Then write.

Each phase feeds the next. Exploring first means probing blind, because only the
conversation knows where to look. Proposing a tree before exploring means
proposing over a vault whose contents you have not seen.

You drive the conversation; deterministic scripts do every mutation. **Never
hand-edit what a script owns**: the tree, the folder map, or any managed block.

## Pre-flight

Read `.workspace/workspace.json`. If `bootstrapped` is true, stop and ask which
steps to re-run; the engine needs `--force` and you should confirm before using
it. This is the one read that precedes Phase 1, because it decides whether to
run at all.

## Phase 1: conversation

Full method: [references/conversation.md](references/conversation.md).

**Read nothing in this phase.** Reading makes you propose, and a proposal here
anchors the person to your vocabulary before they have shown you theirs.

Open with one question, not a numbered round:

> Before I look at anything: what is this workspace for, and what do you
> actually spend your time on?

Then follow up like a person, one thread at a time.

**Do not** propose a tree, name a folder, or ask about naming, lifecycle stages,
sub-shapes, or which skills to keep. Those are yours to decide and defend in
Phase 3. Asking them now spends the person's attention on your half of the job.

**Exit when** you can say back what they do in one sentence in their words, and
you hold at least one place to go and look.

## Phase 2: exploration

Full method: [references/exploration.md](references/exploration.md).

Say what you are about to read and roughly how long. Then go. **Write nothing in
this phase.** Dispatch parallel `researcher` subagents, one per pointer; they are
read-only by construction, which is what makes it safe to run this wide.

- **If the vault already has content, record the shape that exists.** Do not
  propose one over the top of it.
- **Every finding carries its source path.** A finding without one is an
  assumption, and Phase 3 labels it as such.
- **A contradiction is a finding, not an error.** If they said "clients" and the
  disk is organised by product, both go into the playback with a recommendation.
  Never resolve it silently.

**Exit when** every pointer is read or recorded as unreachable, and every
recommendation you intend to make has evidence or a stated assumption behind it.

## Phase 3: playback and sign-off

Full method, including the recommendation catalogue:
[references/playback.md](references/playback.md).

One document, formatted the way [`grilling`](../grilling/SKILL.md) formats a
round: numbered, each item carrying a recommendation acceptable in one word.
Six sections, in order: what I understand you do; your vocabulary; what I found
and where; what I could not determine; what I propose and why; what I am
assuming.

Label every line **confirmed** (they said it), **found** (evidence, with a
path), or **assumed** (neither). Three registers, no fourth.

Render the tree rather than describing it. Reviewing a concrete tree is ten
times cheaper than specifying one.

Close with a single question: approve, edit, or start over on the shape. If any
of it does not land, tell them `/clarify` will re-pitch it.

**Write nothing until that returns.**

## Phase 4: write the plan, then dry run

Write `.workspace/plan.json` from what was signed off. The schema is
`.workspace/schema/plan.schema.json`; `.workspace/fixtures/plan.example.json` is
a worked example of the grammar.

Always dry-run first and apply with the identical command:

```bash
./hq bootstrap --plan .workspace/plan.json --dry-run
./hq bootstrap --plan .workspace/plan.json
```

Show the dry run and get a yes before applying. If the engine prunes rules, say
which and why: it means those standards have no folder to govern here.

## Phase 5: the authoring pass

The engine leaves `__REPLACE_ME__` sentinels and `<!-- AGENT: ... -->` comments
in every generated file. Walk them and replace each with real prose from Phases
1 to 3, **deleting every comment as you go**.

This is where the workspace stops being a skeleton. Write for an agent that has
never seen it: if a sentence would be obvious from the artifacts, cut it.

Do not invent. Where nothing in the first three phases answered something, the
honest output is an entry under Open questions naming what is unknown and what
would resolve it.

## Phase 6: Obsidian

```bash
./hq obsidian-setup
```

Quit Obsidian first; it rewrites plugin config from memory on quit, so an edit
made while it is running is discarded.

Then tell the person, in this order: open the repo root as a vault, **trust the
plugins when prompted**, and install the store plugins the command listed. A
fresh clone with plugins disabled looks broken, and people conclude the template
is broken.

## Phase 7: hand off

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
