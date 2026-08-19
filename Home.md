---
type: moc
status: active
created: {{TODAY}}
scope: none
---

# {{WORKSPACE_NAME}}

<!-- AGENT: one framing sentence. What a person opening this vault should know
     first. Delete this comment. -->
__REPLACE_ME__

<!-- workspace:nav:start -->
## Conventions

- [Standards](<Standards/README.md>) -- every convention, stated once
- [Context](<CONTEXT.md>) -- the ubiquitous language
- [Decisions](<Decisions/README.md>) -- the decision register

## Shared

- [Meetings](<Meetings/README.md>)
- [People](<People/README.md>)

## How the vault works

- [Obsidian guide](<Obsidian/Guide/00-obsidian-guide-index.md>)
<!-- workspace:nav:end -->

## Views

Saved queries that answer the recurring questions without a search.

- [Inbox triage](<Obsidian/Views/inbox-triage.base>) -- what is broken or stale
- [Active work](<Obsidian/Views/active-work.base>) -- what is live right now
- [Meetings](<Obsidian/Views/meetings.base>) -- when did we last speak, and about what
- [People](<Obsidian/Views/people.base>) -- who have I not touched in longest
- [Decisions](<Obsidian/Views/decisions.base>) -- what did we decide, and is it still current

Everything between the nav markers is generated from `.workspace/plan.json` by
`./workspace render`. Everything outside them, including this section, is
hand-owned and survives a re-render.

Markdown links with angle brackets are used for paths with spaces, so they
resolve outside Obsidian too. Wikilinks are used for notes Obsidian can find on
its own.
