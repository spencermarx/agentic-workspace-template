# Phase 2: the exploration

Loaded on demand by the [`bootstrap`](../SKILL.md) skill. Write nothing while
this phase is running.

Tell the person what you are about to read and roughly how long it will take,
then go quiet and do it. This is the phase where the agent earns the questions
it did not ask.

## Two sources, in priority order

### 1. The pointers from Phase 1

The places they named. These are the point of the exercise: a fixed probe list
can only find what someone anticipated, while a pointer is the person telling
you where their real context lives.

Dispatch one `researcher` subagent per pointer, in parallel. That agent is
read-only by construction (`Read, Grep, Glob, WebSearch, WebFetch`), which is
what makes it safe to run this wide without a confirmation per read.

Ask each one a single answerable question, not "have a look at this". Good:
*what does this repo's README say the business does, and which client or product
names appear in it?*

If a pointer is unreachable, outside the machine, or needs a credential, record
it as unreachable and move on. Never ask for a credential to satisfy curiosity.

### 2. The standing probes

Cheap, always worth running, and each one removes a question from Phase 3:

```bash
gh repo view --json name,owner,description 2>/dev/null   # repo identity
git config user.name; git config user.email              # the operator
gh auth status 2>&1 | head -3                            # is the GitHub step possible
ls -d /Applications/Obsidian.app 2>/dev/null             # is Obsidian installed
ls -d ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents 2>/dev/null
find . -name '*.md' -not -path './.claude/*' -not -path './.workspace/*' \
       -not -path './Standards/*' -not -path './Obsidian/*' | head -50
```

That last one matters most.

## If the vault already has content

**Record the shape that exists. Do not propose one over the top of it.**

Read what is there and derive: what the top-level plural folder already is, how
instances are named, whether frontmatter is already in use and in what form,
and which of [the reserved folder names](../../../../Standards/vault-standards.md#the-reserved-folder-vocabulary)
are already taken. A bootstrap that renames someone's existing folders is a
migration they did not ask for.

If the shape you record renames `Areas/` or `Operators/`, the rule globs that
route by those names must be rewritten to match in the same change. A glob that
matches nothing stops routing without saying so.

## Three rules

**Every finding carries its source path.** `Clients/beantown/CLAUDE.md` names
two contacts, not "there seem to be some contacts". A finding without a path is
an assumption, and Phase 3 puts it in a different section.

**A contradiction is a finding, not an error.** If they said "clients" and the
disk is organised by product, that is the single most useful thing you will
learn all session. Both go into the playback, with a recommendation and the
reason. Never resolve it silently, and never assume the disk is right: the disk
is often the thing they are trying to escape.

**Follow the evidence past the list.** A README naming three clients has just
answered "which instances exist today" without costing a question. A folder of
proposals with consistent filenames has answered the naming convention. Chase
those; they are why this phase comes before the proposal and not after.

## Exit condition

- Every pointer is either read or recorded as unreachable.
- Every recommendation you intend to make in Phase 3 has either evidence with a
  path, or an assumption you are prepared to label as one.
- You have not written a single byte.
