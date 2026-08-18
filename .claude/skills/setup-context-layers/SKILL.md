---
name: setup-context-layers
description: Configure this repo's tracking, triage, and context layers for the agent skills that consume them (e.g. wayfinder) - where issues live, the triage label vocabulary, and the domain-doc layout. Run once before first use of those skills.
disable-model-invocation: true
---

<!-- Vendored from https://github.com/spencermarx/bizkit (.claude/skills/setup-tracking-triage-and-context-layers/SKILL.md @ ce32987bb267); adapted for this repo (renamed to match what it does here; tracker and config locations read from .workspace/workspace.json rather than assuming an issue tracker; engineering artifact types re-keyed to vault artifacts). Upstream lineage: https://github.com/mattpocock/skills. See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->

# Setup: Tracking, Triage, and Context Layers

Scaffold the per-repo configuration that the tracker-driven skills (like `wayfinder`) assume:

- **Issue tracker** - where issues live (GitHub Issues)
- **Triage labels** - the strings used for the canonical triage roles (five state + two category)
- **Domain docs** - where the glossaries (`CONTEXT.md`) and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` - is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root - does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root, and per-context glossaries under `docs/contexts/<context>/CONTEXT.md`
- `docs/engineering/adr/` (where the `adr` skill writes decision records)
- `.workspace/config/` - does this skill's prior output already exist?
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals - a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order - one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when exploration already found the layout).

**Section A - Issue tracker.** This repo tracks work on **GitHub Issues** (skills like `wayfinder` - and `triage`, if installed - read from and write to it via the `gh` CLI). Confirm the `git remote` points at the GitHub repo the user expects, then record it in `.workspace/config/issue-tracker.md` - including where PRDs/specs live (the seed carries a bracketed placeholder; exploration usually answers it, e.g. `docs/product/prds/`). The template carries a "PRs as a request surface" flag, defaulted **off** - leave it off and don't raise it; a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B - Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you) - an uninstalled skill needs no labels.

If it is installed, the vocabulary has two parts - five **state** roles and two **category** roles (`bug`, `enhancement`) - and both get recorded. Ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The state defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. The category defaults are likewise `bug` and `enhancement` - but check the tracker's existing labels first: if the repo already types issues (e.g. `type: bug` / `type: feature`), map the category roles onto those existing labels rather than creating duplicates, and fold that into the recommendation. On **yes**, write both tables accordingly. Only if the user says no - usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`) - collect the overrides so `triage` applies existing labels instead of creating duplicates.

Whatever vocabulary is chosen, the labels must exist on the tracker before triage can apply them - create any missing ones as part of this section (`gh label create <name> --description "..."`), mirroring how the repo's other label families are provisioned.

**Section C - Domain docs.** This repo family's domain-doc conventions are owned by the `context` skill (glossary format and placement, `CONTEXT-MAP.md`) and the `adr` skill (decision records under `docs/engineering/adr/`); the `domain-modeling` skill decides what's worth capturing. Don't scaffold a layout - **record the one that exists**. Exploration tells you which shape the repo is in:

- **Multi-context** - per-context glossaries (e.g. `docs/contexts/<context>/CONTEXT.md`), optionally indexed by a root `CONTEXT-MAP.md`
- **Single-context** - one `CONTEXT.md` at the repo root

Write what you found into `.workspace/config/domain.md` (seeded from [domain.md](./domain.md)). If no glossary exists yet, still write the file - it records where one would go, and the `context` skill creates it lazily.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules)
- The contents of `.workspace/config/issue-tracker.md`, `.workspace/config/domain.md`, and `.workspace/config/triage-labels.md` (the last only when `triage` is installed)

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create - don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) - always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

**Re-runs merge, never blind-overwrite.** When a `.workspace/config/*.md` file already exists, treat the seed as a starting point only: update the sections being reconfigured and preserve hand-maintained additions (extra tables, repo-specific notes). The seeds and their written instances carry sync markers - when a fix lands in one copy's command or protocol blocks, mirror it in the other.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `.workspace/config/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `.workspace/config/triage-labels.md`.

### Domain docs

[one-line summary of layout - "single-context" or "multi-context"]. See `.workspace/config/domain.md`.
```

Include the `### Triage labels` sub-block, and write `.workspace/config/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md) - GitHub issue tracker
- [triage-labels.md](./triage-labels.md) - label mapping (only if `triage` is installed)
- [domain.md](./domain.md) - domain doc consumer rules + layout

### 5. Done

Tell the user the setup is complete and which skills will now read from these files. Mention they can edit `.workspace/config/*.md` directly later - re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.
