---
name: conveying-clearly
description: >-
  The contract for anything a human will read — a statement of what you found or did, a
  question or option set, a recommendation or verdict, a ticket or PR comment, a
  handoff, a status update. Use BEFORE composing any surface a person must read and act
  on; the grilling, wayfinder, arch-board, and work-ticket flows load it automatically.
  Also trigger the moment a reply comes back "I don't understand the question / the
  options / where you've got to".
---
<!-- Vendored from https://github.com/spencermarx/bizkit (.claude/skills/conveying-clearly/SKILL.md @ ce32987bb267); adapted for this repo (engineering artifact examples re-keyed to vault artifacts). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


<!-- Original skill authored for this repo; rationale in Surface questions
     and answers to humans through the conveying-clearly skill contract.
     The plain-language spine borrows from the "wait-what" skill in
     github.com/mattpocock/skills (skills/productivity/wait-what): give a little
     context, write ASD-STE100 Simplified Technical English, speak the ubiquitous
     language from CONTEXT.md. Retrofitted here — upstream is a one-line re-pitch
     prompt a human fires after a message lands badly, so that becomes one move
     inside this standing contract ("When it lands badly"), and two of STE's rules
     are deliberately not carried over: its ~900-word approved dictionary (the
     three vocabulary buckets are this repo's equivalent, and they admit our own
     domain language) and its blanket ban on the passive. The glossary pointer
     resolves through the root CONTEXT-MAP.md rather than a single CONTEXT.md. -->

# Conveying clearly

A statement, a question, an option set, a verdict, a resolution comment, a PR
description, a handoff, a map gist — one act: **surfacing something to a reader
who did not watch this session.** The shorthand you coined while reading code,
issues, and memory feels canonical to you and means nothing to them. That
asymmetry is invisible from the inside — a surface is always clear to its author
— so the fix is never to dumb the content down. Ground the vocabulary, write
plainly, lead with the point.

## The reader test

Compose for a teammate who stepped away before this session started and reads
only what you are sending now. If acting on it — or trusting it — takes having
watched your exploration, the surface fails. Rewrite it before sending; do not
wait for "please clarify."

## Lead with the point

One shape serves every surface:

1. **A line or two of shared context** — what the reader needs, in their
   vocabulary. Not a replay of your reasoning; they are deciding, not auditing.
2. **The point** — the ask, the decision, the finding, the state — in one plain
   sentence, ahead of any elaboration. A point buried under recited findings has
   already failed the reader test.
3. **The why, as consequences** — what taking it gets them, what it trades away.
4. **What follows** — what it unblocks, invalidates, or commits to.

## Ground every term

Every load-bearing term belongs to one of three buckets:

1. **Everyday technical vocabulary** — read without a glossary by any working
   engineer (schema, migration, endpoint, rate limit).
2. **Ubiquitous language** — defined in the relevant `CONTEXT.md` (indexed by the
   root `CONTEXT-MAP.md`). Use these freely and by preference, and never
   re-define them inline: **define the private, assume the shared.**
3. **Glossed right here** — at first use, in the surface the reader sees: "the
   claim short-circuit (the check that skips permission resolution while an org
   is unclaimed)".

Shorthand coined this session — by you, an inherited map gist, a ticket, a memory
file — is **never automatically bucket 1**, however settled it feels. Gloss it,
expand it, or drop it. A term that fits no bucket means you do not yet understand
the thing well enough to surface it; translate first.

**No bare issue numbers as nouns.** The citation rides in parentheses, never as a
subject or object: "the rule that agents can never provision organizations
(#69)" passes; "#93 tracks the resets" fails, because the number is doing a
noun's job.

## Write plainly

Sentence craft, in the spirit of **ASD-STE100 Simplified Technical English**:

- One idea per sentence; roughly 20 words for an instruction, 25 for a
  description.
- Active voice, simple present: "the migration drops the column". (The passive
  is fine where the actor is genuinely unknown or irrelevant.)
- One term per meaning. A synonym reads as a second, different thing.
- No orphan "it" / "this" / "that" — name the thing again.
- No noun stacks: "agent permission grant scope resolver" is not a phrase.

## Give reasons, not authority

"Board unanimous 4-0", "per the ratified ruling", "as decided" justify nothing to
a reader who was not there. Say what happens if the recommendation is taken, and
what is given up.

Reasons do not replace **marking** your lean. Where the surface has a mark, use
it: in an `AskUserQuestion` the recommended option goes first and its label ends
with `(Recommended)`. A lean argued only in prose renders as no recommendation at
all. Holding no real lean, say so out loud — an unmarked list reads as either "no
recommendation" or "the marker got dropped". Never manufacture a lean you do not
hold.

## When it lands badly

"I don't understand the question." "I'm not following where you've got to." The
answer is to **re-pitch, not repeat** — shortening the same jargon is the classic
wrong move, because vocabulary rather than length is usually what broke. Name
which terms were private, then rebuild: a little shared context, the point in one
plain sentence, grounded words. A human can invoke this skill
(`/conveying-clearly`) to demand exactly that of the last message.

## Load when composing

- **[Option pickers](references/ask-user-question.md)** — `AskUserQuestion`
  headers, labels, descriptions, previews, the recommendation marker, and a
  worked rewrite.
- **[Text that outlives the session](references/persisted-artifacts.md)** —
  resolution comments, map gists, handoffs, ticket bodies, ADRs, memory files:
  glossing, promote-or-drop, and the wayfinder map's Working vocabulary.

## Before you send

- Every noun understandable to a teammate who missed this session?
- Every load-bearing term plain, in `CONTEXT.md`, or glossed right here?
- The point in one plain sentence, behind at most a line or two of context?
- Short active sentences, one idea each, one term per meaning, no orphan "this"?
- Every _why_ a consequence rather than an authority — and a real lean actually
  marked, or its absence stated out loud?
- Any bare `#NNN` doing a noun's job?
