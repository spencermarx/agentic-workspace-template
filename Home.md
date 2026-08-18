---
icloud-sync: true
icloud-sync-exclude: [.git/, .claude/, .obsidian/, .credentials/, .workspace/, .trash/, Attachments/, node_modules/, .DS_Store]
---

# {{WORKSPACE_NAME}}

<!-- AGENT: one framing sentence. What a person opening this vault should know
     first. Delete this comment. -->
__REPLACE_ME__

<!-- workspace:nav:start -->
## Conventions

- [Standards](<Standards/README.md>) -- every convention, and the registry
- [Context](<CONTEXT.md>) -- the ubiquitous language
- [Decisions](<Decisions/README.md>) -- the decision register

## Shared

- [Meetings](<Meetings/README.md>)
- [People](<People/README.md>)

## How the vault works

- [Obsidian guide](<Obsidian/Guide/00-obsidian-guide-index.md>)
<!-- workspace:nav:end -->

Everything below the heading is generated from `.workspace/plan.json` by
`./workspace render`. The frontmatter above it is hand-owned: it carries the
sync marker and exclusion list, which are part of the file contract.

Markdown links with angle brackets are used for paths with spaces, so they
resolve outside Obsidian too. Wikilinks are used for notes Obsidian can find on
its own.
