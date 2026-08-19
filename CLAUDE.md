# {{WORKSPACE_NAME}}

<!-- AGENT: replace this paragraph with two or three sentences saying what this
     workspace is, who operates it, and what it holds. Written for an agent that
     has never seen it before. Delete this comment. -->
__REPLACE_ME__

This is the root context. A folder that carries agent-specific context has its
own `CLAUDE.md`, which extends or overrides what is here (progressive
disclosure); a folder that only needs orienting has a `README.md` instead. Read
whichever the folder you are working in has, and both where both exist. They are
split by audience, never duplicated: [claude-md-contract § CLAUDE.md and
README.md are split by audience](Workspace/Standards/claude-md-contract.md#claudemd-and-readmemd-are-split-by-audience).

Conventions that apply everywhere (voice, frontmatter, document patterns)
live in `Workspace/Standards/`. Read `Workspace/Standards/README.md` before writing or restructuring
any note. Do not restate those rules here or in any other `CLAUDE.md`; point at
them.

## What this workspace is

Two interfaces over the same Markdown files in one git repository. Obsidian is
the human GUI: open the repo root as a vault and start at `Home.md`. Claude Code
is the agentic GUI: it reads this file, the nested `CLAUDE.md` files, and the
skills in `.claude/`.

<!-- AGENT: add two or three lines of specifics: the kind of work this workspace
     carries, and anything a reader would otherwise guess wrong about. Delete
     this comment. -->

## Where things live

<!-- workspace:map:start -->
| Folder | What it holds | Start here |
|---|---|---|
| `Workspace/` | How the workspace works: standards, guide, templates, views. Not content. | `Workspace/CLAUDE.md` |
| `Decisions/` | Workspace-level decision records. | `Decisions/CLAUDE.md` |
| `Meetings/`, `People/` | Shared operational notes. | `Meetings/README.md` |
| `.claude/` | The agentic harness: rules, skills, agents, commands. | `.claude/CLAUDE.md` |
<!-- workspace:map:end -->

This table is generated from `.workspace/plan.json`. Do not edit it by hand; run
`./hq render` instead. That is why it cannot drift.

## Always-on invariants

Only rules with no useful glob belong here. Everything else is a `Workspace/Standards/`
section routed by a `.claude/rules/` pointer that loads when a governed file is
read.

1. **Standards are stated once.** If you find yourself writing a convention into
   a `CLAUDE.md`, it belongs in `Workspace/Standards/` with a rule routing it. A
   `## Standards` section in any `CLAUDE.md` is a defect.
2. **Never decide for the operator.** Present options, give a recommendation,
   leave the decision where it belongs.
3. **Credentials never enter a note.**
4. **Never fix the harness here.** `.workspace/`, `.claude/skills/`, and
   `Workspace/Templates/` are owned by the template this workspace came from. Fix
   them upstream and run `./hq upgrade`. `./hq doctor` reports
   drift.

## Person resolution

Skills that need to know who is running the session resolve the session email
against `people[].emails` in `.workspace/workspace.json`. Path-coupled skills
build their paths from the resolved key; never hardcode a person's name or path
in a skill, a template, or a view.

## What's pending

<!-- AGENT: the short-lived working set. Committed near-term actions only.
     Deferred items go to the relevant Parking Lot; strategic unknowns go to
     that area's Open questions. Prune this section every session rather than
     appending to it. Delete this comment. -->

- Nothing yet. This workspace was just bootstrapped.
