---
name: investigation-brief
description: >-
  Runs the conversation deciding what to read before anyone proposes a workspace structure,
  then writes an ordered brief of investigation points: paths, URLs, and what the operator
  will simply explain. Use whenever a business or vault must be understood before it is
  shaped. Do NOT use to do the reading (use `explore-context`), to create folders (use
  `extend-architecture`), for end-to-end first setup (use `bootstrap`), or to stress-test a
  plan they already have (use `grilling`).
---

# investigation-brief

Owns one thing: **the conversation that decides what is worth reading.** It ends
with a written, ordered brief of investigation points, and nothing else.

It does not do the reading. It does not propose a folder, a name, or a tree. The
moment you catch yourself sketching structure, you have left this skill.

The reason it is separate: reading before talking means probing blind, because
only the operator knows where the material is. And the single highest-value
source is usually not on disk at all. It is something they will explain in two
minutes if asked, and that an agent reliably forgets to ask for.

## What an investigation point is

A concrete thing to go and look at, in one of three forms:

- **A path on disk.** An existing vault, a folder of proposals, a sibling repo, a
  Notion or Drive export sitting in Downloads.
- **A URL.** The company site, a pricing page, a blog, public docs, a LinkedIn
  profile, a job posting they wrote.
- **An explanation from the operator.** Something no artifact records: why they
  fired a client segment, who actually decides, which of the four product names
  is the real one.

Each point carries three things or it is not a point: **its source**, **the
question it should answer**, and **its priority**.

## Step 1: open the conversation

One question, not a numbered round:

> Before I go and read anything: what does this business actually do, and what do
> you spend your week on?

Then follow up like a colleague, one thread at a time. Ask for the boring
operational truth rather than the pitch. "Walk me through the last one you
delivered" beats "what is your value proposition" every time.

Compose questions through [`conveying-clearly`](../conveying-clearly/SKILL.md):
one question at a time, in their words, answerable without having watched you
think.

**Done when:** you can say back in one sentence what the business does, in their
vocabulary, and they would recognise it.

## Step 2: cover the five things

Not a checklist to read out. Reach each as a follow-up, and note which ones the
conversation never touched.

1. **What they produce**, and what a finished unit of it looks like.
2. **Who buys it**, and how a buyer arrives.
3. **Who works in it**, and whether the work splits by person.
4. **What recurs**, meaning what they have many of where each accumulates its own
   context over time.
5. **Where the material already lives.** Every place they name goes on the list,
   even in passing.

Capture their vocabulary verbatim. If they say "engagements", do not write
"clients". Note the words they reject too.

**Done when:** each of the five is either answered in their words or written down
as an unanswered gap.

## Step 3: turn the conversation into points

For each place they named, and each gap you found, draft a point. Recommend an
answer wherever you can, so the operator can accept it in one word:

> 3. The old vault at `~/Documents/Practice Notes` -- I would read this first;
>    it is the only record of how the work was actually organised. Read it, or
>    is it stale?

Two failure modes to check for before you move on:

- **A brief with no operator-explanation points.** If everything on the list is a
  file or a URL, you did not ask what only they know. Go back.
- **A point with no question.** "Read the website" is not a point. "Read the
  website to find out which of the three service lines they still sell" is.

**Done when:** every point has a source, a question, and a priority, and at least
one point is an explanation only the operator can give.

## Step 4: write the brief

Create the entry through [`scratchpad`](../scratchpad/SKILL.md) and write the
brief inside it:

```bash
SP="$(git rev-parse --show-toplevel)/.claude/skills/scratchpad/scripts/scratchpad.sh"
dir="$(bash "$SP" new research 'investigation brief')"
```

Write `00-brief.md` in that directory. Use the absolute path the script printed;
never build a `.scratchpad/...` path by hand.

The brief is a numbered list, highest priority first. Each entry:

| Field | Content |
|---|---|
| Source | The path, the URL, or the person to ask |
| Question | What reading it should answer |
| Priority | high, medium, or low, with the reason for high |
| Reachable | whether it exists and you can get to it |

Close with two short sections: **what the conversation settled** and **what is
still unknown**.

**Done when:** the file exists at a reported absolute path and every point in it
carries all four fields.

## Step 5: hand off

Show the operator the brief and ask one question: approve, edit, or add a source.
Then hand the absolute path to [`explore-context`](../explore-context/SKILL.md),
which does the reading.

**Done when:** the operator has approved the list and you have named the file
path in your handoff.

## Guardrails

- **Read nothing while this skill is running.** One `ls` to confirm a path exists
  is fine. Opening the files is the next skill's job, and reading here makes you
  propose structure before the operator has shown you their vocabulary.
- **Never decide for the operator.** Recommend, then let them accept or reject.
- **Do not resolve a contradiction silently.** If they said "clients" and the
  disk says products, that is a point to investigate, not an error to fix.
- **An unreachable source stays in the brief**, marked unreachable. Deleting it
  loses the fact that it was worth reading.
