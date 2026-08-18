# Issue tracker: GitHub

<!-- Seed template - the written instance for this repo lives at .workspace/config/issue-tracker.md. When fixing a command or protocol block in either copy, mirror it in the other; a setup re-run merges, never blind-overwrites. -->

Issues for this repo live as GitHub issues. Use the `gh` CLI for all operations. [Record where PRDs/specs live - in many repos they are files in the repo (e.g. `docs/product/prds/`), not tracker issues.]

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments` for a human-readable read, or `gh issue view <number> --json body,comments,labels` when filtering with `jq`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`. Pick the close reason deliberately - `--reason completed` for work that exists or is underway, `--reason "not planned"` for rejections and deferrals. The triage skill's dedup pass relies on the **label + reason pairing**: the `wontfix` label marks genuine rejections only (a deferral shares the "not planned" reason but carries no label, its roadmap-link comment telling them apart).

Infer the repo from `git remote -v` - `gh` does this automatically when run inside a clone.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(Set to `yes` if this repo treats external PRs as feature requests; `/triage` reads this flag.)_

When set to `yes`, PRs run through the same labels and states as issues, using the `gh pr` equivalents:

- **Read a PR**: `gh pr view <number> --comments` and `gh pr diff <number>` for the diff.
- **List external PRs for triage**: the author association is only on the REST surface (`gh pr list --json` does not expose it) - `gh api 'repos/{owner}/{repo}/pulls?state=open' --paginate --jq '.[] | select(.author_association | IN("CONTRIBUTOR","FIRST_TIME_CONTRIBUTOR","FIRST_TIMER","MANNEQUIN","NONE")) | {number, title, author_association}'` (one JSON object per external PR - this drops `OWNER`/`MEMBER`/`COLLABORATOR`; a bracketed filter would emit one array per page under `--paginate`), then fetch bodies/labels/comments per candidate with `gh pr view <number>`.
- **Comment / label / close**: `gh pr comment`, `gh pr edit --add-label`/`--remove-label`, `gh pr close`.

GitHub shares one number space across issues and PRs, so a bare `#42` may be either - resolve with `gh pr view 42` and fall back to `gh issue view 42`.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets.

- **Labels**: the map and its tickets use the `wayfinder:*` labels - `wayfinder:map` plus one `wayfinder:<type>` per ticket (`research`/`prototype`/`grilling`/`task`). `gh issue create --label` fails on labels that don't exist, so create any missing ones first: `gh label create "wayfinder:<name>" --description "..."`.
- **Map**: a single issue labelled `wayfinder:map`, holding the Destination / Notes / Decisions-so-far / Not-yet-specified / Out-of-scope body (see the wayfinder skill's map template). `gh issue create --label wayfinder:map`.
- **Child ticket**: an issue linked to the map as a GitHub sub-issue: `gh api --method POST repos/<owner>/<repo>/issues/<map>/sub_issues -F sub_issue_id=<child-db-id>`, where `<child-db-id>` is the child's numeric **database id** (`gh api repos/<owner>/<repo>/issues/<n> --jq .id`, _not_ the `#number` or `node_id` - the same trap as the blocking edge below). Where sub-issues aren't enabled, add the child to a task list in the map body and put `Part of #<map>` at the top of the child body. Labels: `wayfinder:<type>`. Once claimed, the ticket is assigned to the driving dev.
- **Blocking**: GitHub's **native issue dependencies** - the canonical, UI-visible representation. Add an edge with `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>`, where `<blocker-db-id>` is the blocker's numeric **database id**. GitHub reports `issue_dependencies_summary.blocked_by` (open blockers only - the live gate) on single-issue GETs. Where dependencies aren't available, fall back to a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Frontier query**: two REST steps - `issue_dependencies_summary` is **not** available via `gh issue list`. (1) Enumerate the map's children in map order: `gh api repos/<owner>/<repo>/issues/<map>/sub_issues --paginate` (unpaginated, the list truncates at 30 children). (2) Keep the children that are open, unblocked, and unclaimed: `state == "open"`, `.issue_dependencies_summary.blocked_by == 0` (fetch per child via `gh api repos/<owner>/<repo>/issues/<n>` if the list payload omits the field), and `(.assignees | length) == 0`; first in map order wins.
- **Claim**: `gh issue edit <n> --add-assignee @me` - the session's first write.
- **Resolve**: `gh issue comment <n> --body "<answer>"`, then `gh issue close <n>`, then append a context pointer (gist + link) to the map's Decisions-so-far.

## Work-ticket operations

Used by `/work-ticket` (the post-triage front-door) to drive one `ready-for-agent` issue to shipped. State lives on the issue and is derived every run; no new labels are minted.

- **Read state**: `gh issue view <n> --json number,title,body,labels,comments,assignees,state`. The phase is derived from the labels + live facts (below) + the latest handoff comment - never a stored field.
- **Latest handoff comment**: `/work-ticket` posts a `## work-ticket handoff` comment at transitions; the most recent one wins. Read the newest comment whose body starts with `## work-ticket handoff` (comments are returned in creation order); it carries the prior owner's judgment (decisions + why, gotchas, intended next step), never stale mechanical state.
- **Live native facts** (always current, primary over the handoff): a linked PR - `gh pr list --head work/<n>-<slug> --state all` / `gh pr view`; CI - `gh run view --json conclusion` (watch to green via the `watch-ci` skill, never a sleep-poll); merge/closed - the PR/issue state.
- **Deterministic branch**: `work/<issue-number>-<short-slug>` (slug from the title, lowercased, non-alphanum → dashes). Recomputable by any agent, so it doubles as the idempotency key - match the **stable `work/<issue-number>-` prefix** (`gh pr list --head "work/<issue-number>-*" --state all`), not the drift-prone slug, before opening a PR; GitHub's one-open-PR-per-head rule guards a duplicate.
- **Label transitions**: reuse the triage labels only - `needs-info` for a parked human gate (with a question comment), `ready-for-human` when work genuinely needs a person. On a genuine state contradiction the skill reconciles loudly (park to `needs-info` + a comment) rather than guessing.
- **Kanban projection**: a board's In-progress / In-review columns may be set to reflect progress, but are a write-only human projection - never read back to decide the phase.
- **Working content**: ephemeral notes go to the scratchpad `work-items` domain (git-ignored, local to one machine - shared across its worktrees, but never durable), never the resume authority.
