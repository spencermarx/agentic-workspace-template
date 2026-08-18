---
name: handoff
description: >-
  Compact the current session into a handoff document -- every load-bearing reference,
  decision, gotcha, and resume coordinate, and none of the transcript noise -- so a fresh
  agent in a new session picks the work up and carries it on. Writes into the git-ignored
  scratch area via `scratchpad`, never into the vault. User-invoked only. Do NOT use to
  record a settled decision (use `decision-record`) or to park an out-of-scope item (use
  `parking-lot`).
argument-hint: '[what the next session will focus on]'
disable-model-invocation: true
---

<!-- Vendored from https://github.com/spencermarx/example-co (.claude/skills/handoff/SKILL.md @ 8bd0dc9); adapted for this repo (artifact types re-keyed from Issues/OpenSpec/nx to vault artifacts: decision records, area CLAUDE.md registers, parking lots, activities, external paths; the document template moved to references/ to fit the skill-body budget; build-gate done-bar replaced with the validation gate). Upstream lineage: https://github.com/mattpocock/skills (skills/productivity/handoff/SKILL.md). Its core ideas are preserved: compact rather than copy, reference artifacts by path, redact secrets, suggest skills, save outside the tracked workspace. See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->

A session is about to end and the work is not done. What you were doing, the
three things you already ruled out, the exact file you stopped in, the gotcha
that cost you an hour: all of it lives only in this conversation. The next agent
boots cold. It gets the vault, the `CLAUDE.md` tree, and `Standards/`, and none
of your live thread.

The whole job is compaction: squeeze the session down to its resumable core, so
the next agent inherits the momentum and not the noise. There are two ways to
fail:

- **Too much.** You paste the transcript, or re-explain what a decision record
  already says. The next agent drowns and re-reads everything anyway.
- **Too little.** You write a tidy summary that quietly drops the load-bearing
  specifics: the exact next action, the dead end not to retry, the file you
  stopped in. The next agent looks confident and rebuilds the wrong thing.

Most durable context already lives in artifacts. Your handoff **points** at
those, never copies them. What it must carry itself is only the live thread that
is not written down anywhere yet, plus the mechanical coordinates to reconstitute
the workspace. Everything else is a link.

Write for a smart stranger who has your tools and your vault but zero memory of
this conversation. If a sentence would be obvious to them from the artifacts, cut
it and link the artifact. If it would not be recoverable without you in the room,
it belongs in the handoff.

## Step 1: recon the mechanical state

Before writing prose, capture the facts a summary loses. Run what is relevant.

```bash
git branch --show-current     # the branch to resume on
git status --short            # uncommitted work: the live edit surface
git log --oneline -8          # recent commits, for narrative anchor
git stash list                # anything parked
./workspace validate          # is the gate green right now, or did you leave it red?
```

Then take stock of what git will not show you:

- **Background processes** you started, and what each is watching.
- **State outside the vault**: a document shared, a message sent, an external
  system touched. Anything that will not be obvious from the files.
- **Registers this work already touched.** Check the relevant area's
  `CLAUDE.md` for "What's pending" and "Open questions", and its Parking Lot. If
  an item belongs in one of those registers rather than in a handoff, **put it
  there instead**. A register survives; a handoff is swept in fourteen days.

That last point is the most common mistake. A handoff is for the live thread, not
for anything that has a durable home.

## Step 2: write the document

Save into the git-ignored scratch area through the
[`scratchpad`](../scratchpad/SKILL.md) primitive. Never into the vault: a handoff
in the vault becomes a tracked artifact that shows up in Obsidian search and the
graph forever, competing with real knowledge.

```bash
SP="$(git rev-parse --show-toplevel)/.claude/skills/scratchpad/scripts/scratchpad.sh"
dir="$(bash "$SP" new handoffs '<short-slug>')"
```

Write `HANDOFF.md` inside that directory, at the absolute path the script
printed. Never at a hand-written `.scratchpad/...` path, which resolves against
your current directory and strands the file. The next session finds the latest
with `bash "$SP" list handoffs`.

The structure is in
[references/document-template.md](references/document-template.md). Load it now.
**Omit any section that is empty**: a padded handoff is noise wearing a template.

Two things that trip up the compaction:

- **A fact that fits two sections** belongs in one. The classic case is a dead
  end that is also the reasoning for where the work should go instead. Put it
  where the reader needs it most, usually Landmines, and let the other section
  point at it in a clause. One crisp pointer beats two near-duplicates.
- **An artifact that is also a live edit** gets linked, and you carry only the
  delta: what is done, what is in flight, where you stopped. Do not transcribe a
  list the artifact already holds.

## Step 3: redact before you save

The document may be pasted into a fresh session or shared. Strip API keys, secret
values, tokens, connection strings, and personal data on the way in. Reference
where a secret lives rather than its value.

Apply
[confidentiality-standards](../../../Standards/confidentiality-standards.md#what-never-leaves-the-vault)
in full. A handoff carrying client commercial terms is exactly the artifact that
gets pasted somewhere it should not be.

## Step 4: deliver it

Report back with:

1. The **absolute path** the script printed. Never a relative one.
2. A copy-pasteable **seed instruction** for the next session, for example:
   `Read <absolute path> and continue the work; start with the first item under "Next steps".`

Then stop. Do not launch the next session yourself unless asked. The default
deliverable is the document plus the seed line, so the person chooses when and
where to resume.

## If the user passed an argument

Treat it as the focus of the next session and tailor the whole document to it. A
handoff aimed at "finish the proposal and send it" foregrounds the done-bar and
the open questions; one aimed at "work out why the numbers disagree" foregrounds
the landmines and what has already been ruled out. Same session, different lens.

## Gut-check

Read the draft once as the stranger who will receive it and ask: could I resume
from this alone, without the transcript? If the answer is "not without knowing
what you already tried", or "not without the specific next action", fix that and
only that.

The bar is resumability. Nothing more, nothing less.
