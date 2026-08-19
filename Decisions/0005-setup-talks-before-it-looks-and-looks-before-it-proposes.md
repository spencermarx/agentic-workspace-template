---
type: decision
status: active
created: 2026-08-19
date: 2026-08-19
scope: none
---

# 0005 - Setup talks before it looks, and looks before it proposes

## Context

`bootstrap` is the only path from a fresh clone to a populated workspace, so it
is the template's first impression and its highest-leverage skill. It opened
with a fifteen-question interview across four rounds, held in
`references/interview.md`, fired before anything had been read.

A `Step 0` probe ran first, but it was a fixed list of six shell commands. A
fixed list finds only what its author anticipated. It could not act on the
sentence that actually matters, which is a person saying *the real context is in
my other repo*, because nothing had asked them yet.

Counting the fifteen questions is what settled this. Eleven of them were
structural decisions that already carried a recommended default written beside
them: naming convention, lifecycle stages, the inside of one instance,
cross-cutting folders, which skills to keep, where work is tracked. The template
knew the answer and asked anyway. Only four needed a human at all: the name, the
one-liner, what they have many of, and who else touches the vault. Those four
were buried among the eleven.

So the interview spent the person's attention on the agent's half of the job,
asked in the template's vocabulary, before either party had looked at any
evidence. Then it proposed a tree against a vault whose contents it had not
read.

## Decision

**Three phases, and the order is the design: conversation, then exploration,
then playback. Each one feeds the next, and nothing is written until the person
signs off on the playback.**

**Phase 1, conversation. Read nothing.** Open with one question, not a numbered
round, and follow up like a colleague. Ask only what only a person can know:
what the work is, what recurs, who else touches it, and where things already
are. Capture their vocabulary verbatim; if they say "engagements", the workspace
does not say "clients". The most valuable output is the list of places to go and
look, because that list is what a fixed probe list can never produce.

**Phase 2, exploration. Write nothing.** Directed by Phase 1's pointers, with
the old `Step 0` probes demoted to a secondary standing list. One read-only
`researcher` subagent per pointer, in parallel. Every finding carries a source
path. If the vault already has content, record the shape that exists rather than
proposing one over it. A contradiction between what they said and what is on
disk is a finding, surfaced with a recommendation, never resolved silently.

**Phase 3, playback. Write nothing until approval.** Six sections: what I
understand you do, your vocabulary, what I found and where, what I could not
determine, what I propose and why, what I am assuming. Every line is labelled
**confirmed**, **found**, or **assumed**, and the assumed ones are gathered into
their own section so the person can see exactly which lines deserve scrutiny.

Every structural decision the old interview asked about becomes a recommendation
with its default, its one-line reason, and what evidence overturns it. They are
visible and refusable, which is what invariant 2 requires: present options, give
a recommendation, leave the decision where it belongs.

**The `grilling` numbered-round format moves from the opening to the
confirmation.** Numbered questions each carrying a one-word-acceptable
recommendation was the best property of the old interview, and it was in the
wrong place. It is the right shape for confirming a proposal and the wrong shape
for meeting someone.

`references/interview.md` is replaced by `conversation.md`, `exploration.md`,
and `playback.md`, one per phase, so `SKILL.md` carries the spine and each
phase's depth loads when that phase starts.

**No `disable-model-invocation` flag changes.** `to-questionnaire` and
`wait-what` stay user-invoked only, and `bootstrap` does not call them. Those
flags keep user-only triggers out of the always-on description budget, which
`harness-standards § Context budget` names as the budget deciding whether any
skill fires at all. Flipping two of them permanently, to serve a procedure that
runs once per workspace, is the wrong trade. `bootstrap` inlines the
conversational register it needs and points the person at `/clarify` as an
escape hatch, which costs nothing.

## Alternatives considered

### Reorder the existing interview, exploring before asking
- **Approach:** keep the fifteen questions and the four rounds, move `Step 0`'s
  probing in front of them and widen it.
- **Rejected because:** it fixes the smaller half. The order was wrong, but so
  was the content: eleven of the fifteen were questions the template could
  answer itself. Reordering them would have produced a better-informed
  questionnaire, and the objection was to the questionnaire.

### Cut to the four questions and decide the rest silently
- **Approach:** ask only what a human must answer, apply every default without
  showing it.
- **Rejected because:** it violates invariant 2. Deciding for the operator is
  not made acceptable by deciding well. Phase 3 exists so the eleven defaults
  are stated, attributed, and refusable in one word, which costs the person one
  review instead of eleven answers.

## Consequences

**Makes easier:** adoption. Someone meets the template by describing their work
in their own words, not by finding their business in a stranger's taxonomy.

**Makes easier:** bootstrapping a vault that already has content, or a person
whose real context lives in a sibling repo. Phase 2 can follow a pointer, and
the proposal now arrives after the evidence rather than before it.

**Makes harder:** predicting the run. It is longer in wall-clock than a form,
and Phase 2 spends subagent tokens that six shell commands did not. A person who
wanted a fast skeleton now gets a conversation first.

**Makes harder:** verification. Nothing checks that Phase 3 actually labelled
every line, or that Phase 1 truly read nothing. The bar is stated and not
enforced, which is consistent with 0004 and carries the same exposure.

**Explicitly deferred:** whether a multi-person setup should be able to reach
`to-questionnaire`, so one person can hand sections of the playback to a
colleague. The need is real and the flag change is not, until someone hits it.
