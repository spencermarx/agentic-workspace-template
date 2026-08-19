---
name: scratchpad
description: >-
  Create, find, and reclaim ephemeral, git-ignored working artifacts under
  `.scratchpad/` -- this workspace's one home for session scratch (handoffs, research
  dumps, generated reports, debug output). Reach for it WHENEVER you are about to write
  a temporary file that must not be committed, instead of an ad-hoc `tmp/` or a stray
  `notes.md`. Also to list prior entries or clean up old ones. Do NOT use for durable
  tracked artifacts (notes, decision records, documents) -- those belong in the vault.
argument-hint: '[new|list|clean|root] <domain> [slug]'
---

<!-- Vendored from https://github.com/spencermarx/example-co (.claude/skills/scratchpad/SKILL.md @ ce32987bb267); adapted for this repo (worktree rationale compressed, since a knowledge vault rarely uses linked worktrees; examples re-keyed to vault domains; the script itself is byte-identical because it is already repo-agnostic). See [vendoring provenance](../../../Standards/harness-standards.md#vendoring-provenance). -->

# scratchpad

A domain-opaque primitive that owns one thing: where ephemeral, git-ignored
working artifacts live. It answers *where* a piece of scratch goes, *how* it is
named, and *when* it is reclaimed. It knows nothing about what any artifact
means.

It exists because sessions constantly produce working files, and left to habit
those scatter into `tmp/`, stray notes at the vault root, and half-remembered
paths. Anything that lands in the vault root also lands in Obsidian's search and
graph, which is worse here than in a code repo: scratch becomes indistinguishable
from knowledge.

## The one rule: it returns a directory, you write the file

`scratchpad new` creates and prints a **directory**. The caller writes its own
files inside.

The primitive never writes the document, so it can never drift as document
formats evolve, and each caller pins its own discoverable filename. The
[`handoff`](../handoff/SKILL.md) skill writes `HANDOFF.md`; a research burst
writes `00-summary.md` and its receipts.

`<domain>` is an opaque label you choose: `handoffs`, `research`, `reports`,
`debug`. Keep it `[a-z0-9][a-z0-9-]*`.

## One root

There is exactly one `.scratchpad/`, at the top of the main checkout. Calling
from a linked worktree writes to that same root rather than a worktree-local
copy, for two reasons learned the hard way: `git worktree remove` deletes ignored
files without complaint, so worktree-local scratch dies when its branch merges;
and per-worktree roots partition `list`, which defeats the one job this exists to
do.

## Usage

Invoke by absolute path. No build step and no dependencies.

```bash
SP="$(git rev-parse --show-toplevel)/.claude/skills/scratchpad/scripts/scratchpad.sh"

# Create an entry; capture the printed directory and write into it.
dir="$(bash "$SP" new research 'competitor pricing sweep')"
#   -> <root>/.scratchpad/research/20260818-143512-competitor-pricing-sweep/
echo "..." > "$dir/00-summary.md"

bash "$SP" list research      # prior entries in one domain, newest-first
bash "$SP" list               # across all domains
bash "$SP" root               # name the root without creating anything

bash "$SP" clean research --older-than 14d          # shows what it would remove
bash "$SP" clean research --older-than 14d --force  # actually deletes
```

- **`new <domain> <slug>`** creates `<root>/.scratchpad/<domain>/<UTC-YYYYMMDD-HHMMSS>-<slug>/`
  and prints its absolute path. The slug is slugified and capped around 50
  characters; exact collisions get a numeric suffix. Guarantees `.scratchpad/`
  is ignored.
- **`list [<domain>]`** prints entry directories newest-first, one absolute path
  per line. The timestamp prefix makes this a plain reverse sort.
- **`root`** prints the root. It names, it never creates. Use it to tell a human
  or a subagent where scratch lives. Entries still come from `new`, which owns
  the timestamp, the slug, and collision handling. Do not hand-build a path from
  `root`.
- **`clean [<domain>] --older-than <age> [--force]`** reclaims entries older than
  `14d`, `12h`, `30m`, or `0d` for everything. Dry-run unless `--force`. Never
  runs automatically.

## Use the path the script printed

Every verb prints absolute paths, and that is the only path to build on. Three
rules, each of which has already produced a wrong-place write somewhere:

1. **Never write a bare `.scratchpad/...` path.** It resolves against the current
   directory, so from any subdirectory it silently creates a second orphaned
   pile. Always capture the output of `new`.
2. **Report the absolute path back**, not a relative one. The reader may not be
   standing where you were.
3. **Pass the absolute path to subagents.** A subagent's working directory may be
   pinned somewhere else entirely.

This matters more here than in a typical repo: a vault path usually contains
spaces. The script is written for that, and entry names are slug-safe so
newline-delimited pipelines stay correct.

## What belongs here

Local, disposable, never committed: handoffs, research dumps, generated reports,
debug output. Because it is git-ignored it is also the right place for working
material carrying sensitive context.

Local also means local to this machine. Scratch survives reboots but never
reaches a teammate or another checkout, so it can hold working content but never
the authority for resuming work. Anything durable belongs in the vault, under
version control.

## Composed by other skills

This is a substrate. `handoff` calls `scratchpad new handoffs` and owns the file
it writes inside. When you build a flow that emits working artifacts, compose
this rather than inventing another location.

## Maintaining it

`scripts/scratchpad.sh` is bash: pure filesystem plumbing, portable across BSD
and GNU userlands, zero dependencies. After editing, run the colocated smoke test
`bash scripts/scratchpad.smoke.sh`, a create-list-clean roundtrip plus the
rooting guarantees. Keep both shellcheck-clean.

When you add a check, mutate the code to prove it fails before trusting it. The
bug that suite was extended for survived eighteen green checks, because none of
them could see it.
