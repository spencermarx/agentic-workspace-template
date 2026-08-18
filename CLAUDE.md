# {{WORKSPACE_NAME}}

<!-- AGENT: replace this paragraph with two or three sentences saying what this
     workspace is, who operates it, and what it holds. Written for an agent that
     has never seen it before. Delete this comment. -->
__REPLACE_ME__

This is the root context. Each major folder has its own `CLAUDE.md` that extends
or overrides what is here (progressive disclosure). Read the one for the area
you are working in.

Conventions that apply everywhere (voice, frontmatter, tags, document patterns)
live in `Standards/`. Read `Standards/README.md` before writing or restructuring
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
| `Standards/` | Every convention, stated once. Business-agnostic. | `Standards/README.md` |
| `Obsidian/` | Vault mechanics: guides and templates. Not content. | `Obsidian/CLAUDE.md` |
| `Decisions/` | Workspace-level decision records. | `Decisions/README.md` |
| `Meetings/`, `People/` | Shared operational notes. | `Meetings/README.md` |
| `.claude/` | The agentic harness: rules, skills, agents, commands. | `.claude/CLAUDE.md` |
<!-- workspace:map:end -->

This table is generated from `.workspace/plan.json`. Do not edit it by hand; run
`./workspace render` instead. That is why it cannot drift.

## Always-on invariants

Only rules with no useful glob belong here. Everything else is a `Standards/`
section routed by a `.claude/rules/` pointer that loads when a governed file is
read.

1. **Standards are stated once.** If you find yourself writing a convention into
   a `CLAUDE.md`, it belongs in `Standards/` with a rule routing it. A
   `## Standards` section in any `CLAUDE.md` is a defect.
2. **Never decide for the operator.** Present options, give a recommendation,
   leave the decision where it belongs.
3. **The canonical source wins on divergence.** A mirror that disagrees with its
   source is wrong by definition.
4. **Nothing is deleted, things are moved.** `git mv` to an archive location.
   The thinking stays useful even when the conclusion does not.
5. **Credentials never enter a note**, and client material never leaves the
   vault without a human deciding to send it.
6. **The vault is a knowledge layer.** Code, binaries, and legal originals live
   outside it and are referenced by relative path. See
   `Standards/external-paths.md`.
7. **Never fix the harness here.** `.workspace/`, `.claude/skills/`, and
   `Obsidian/Templates/` are owned by the template this workspace came from. Fix
   them upstream and run `./workspace upgrade`. `./workspace doctor` reports
   drift.

## Person resolution

Some skills need to know which person is running the session, to find the right
personal workspace.

Resolve the session email against `people[].emails` in
`.workspace/workspace.json`. If it does not match, fall back to
`git config user.email`. If that does not match either and exactly one person is
configured, use that one.

Path-coupled skills build their paths from the resolved key. **Never hardcode a
person's name or path in a skill, a template, or a view.** That single line is
what lets a second person be added later without a migration.

## What's pending

<!-- AGENT: the short-lived working set. Committed near-term actions only.
     Deferred items go to the relevant Parking Lot; strategic unknowns go to
     that area's Open questions. Prune this section every session rather than
     appending to it. Delete this comment. -->

- Nothing yet. This workspace was just bootstrapped.
