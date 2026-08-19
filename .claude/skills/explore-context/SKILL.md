---
name: explore-context
description: >-
  Runs the research an investigation brief asks for: dispatches parallel `researcher`
  subagents at its points, aggregates cited findings into one digest, and plays it back
  until the operator confirms. Use when a brief is ready, or on "go look into this". Do
  NOT use to decide what to research (use `investigation-brief`), to create folders (use
  `extend-architecture`), or to answer one known question (dispatch `researcher`).
---

<!-- workspace:no-mutate -->

# explore-context

You own the research, and nothing else. A brief arrives naming what is unknown;
you go and find out, and you do not stop until the operator has said, in words,
that the digest matches their world.

Three properties make this skill worth invoking rather than improvising:

- **Parallel and narrow.** One `researcher` per investigation point, each asked a
  single answerable question. A single agent given six questions returns six
  shallow answers.
- **Every finding carries its source.** A path or a URL, on the line itself. A
  finding without one is an assumption, and it lives in a section that says so.
- **A contradiction is a finding.** Two sources that disagree is the most useful
  thing you will learn. Surface both and ask. Never resolve it silently.

## Step 1: take the brief and open a scratchpad entry

Read the brief. It must give you a list of investigation points; if it gives you
a topic instead, stop and route to `investigation-brief`, because guessing the
points here wastes an entire research round.

Create the working directory through [`scratchpad`](../scratchpad/SKILL.md)
(`new research '<brief slug>'`) and write the digest inside it as
`00-digest.md`. Capture the absolute path the script prints; pass that same
absolute path to every subagent, because a subagent's working directory may be
pinned elsewhere.

**Done when:** you can list the investigation points as numbered questions, and
you hold an absolute scratchpad path.

## Step 2: dispatch one researcher per point

Dispatch the [`researcher`](../../agents/researcher.md) subagent once per point,
all in the same block so they run in parallel. That agent is read-only by
construction, which is what makes it safe to run this wide with no confirmation
per read.

Give each one a question that can come back true, false, or with a specific
value. Good: *which folders under `Business/` already hold pricing material, and
what is in them?* Bad: *have a look at pricing.*

Tell the operator what you are about to read and roughly how long, then go quiet.

If a pointer is unreachable, outside this machine, or needs a credential, record
it as unreachable and move on. Never ask for a credential to satisfy curiosity.

**Done when:** every point has either a returned digest or a written
unreachable line naming what blocked it.

## Step 3: aggregate into one digest

Write `00-digest.md` with these sections, in this order:

1. **What I went looking for.** The points, restated.
2. **What I found.** Grouped by the operator's own vocabulary, not by which
   subagent returned it. Every line ends with its source path or URL.
3. **Contradictions.** Each one states both claims, both sources, which is more
   recent, and your recommendation. Never a resolved single line.
4. **What I could not determine.** The unreachable pointers and the questions
   that came back empty, each with what would answer it.
5. **What I am assuming.** Everything with no source. Labelled as assumption,
   never merged upward into "What I found".

Deduplicate across subagents: two agents reporting the same file is one finding
with one source, not two.

**Done when:** you can point at the source on every line of section 2, and
section 5 holds every line that has none.

## Step 4: play it back

The playback is the product, not a formality. Load
[`conveying-clearly`](../conveying-clearly/SKILL.md) before composing it.

Present the digest in the operator's vocabulary, grouped so a whole group can be
confirmed or corrected in one word. Number the groups. Keep the assumption
section visibly separate, because that is the section they are most likely to
correct.

Close by naming the three moves available, in these words:

> **Confirm** any group and I will freeze it. **Correct** anything and I will
> edit the digest. Or tell me to **go look at this too**, and I will add it and
> run another round.

**Done when:** the operator has seen every group and every assumption, and knows
which three responses are open to them.

## Step 5: loop until confirmed

- **Confirm:** mark those groups frozen in the digest. Frozen groups are not
  re-researched in a later round.
- **Correct:** edit the digest to what they said, and relabel the line
  confirmed rather than found. Their correction outranks the source.
- **Go look at this too:** append the new points and return to Step 2. Only the
  new points get dispatched.

**Silence is not confirmation.** Neither is "looks fine" on a group they never
saw, nor an operator answering a different question. Loop until every group is
either confirmed or explicitly dropped.

**Done when:** every group in the digest is frozen, and the operator has said so
in a message you can quote.

## Step 6: hand off

Hand the confirmed digest to
[`extend-architecture`](../extend-architecture/SKILL.md), which turns confirmed
findings into actual folders. Pass the absolute scratchpad path, not the
contents.

**You create nothing.** No folder, no note, no `CLAUDE.md`, no plan edit. If the
research made an obvious folder obvious, that is exactly the input the next
skill wants, and taking the shortcut here means it gets created without the
checks that skill owns.

**Done when:** `extend-architecture` has the path, and the only file this skill
wrote is under `.scratchpad/`.
