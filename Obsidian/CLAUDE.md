# Obsidian

This folder holds the mechanics of the vault, not content. Guides for humans,
templates for note creation. Nothing here is knowledge about the business.

## Layout

- `Guide/`: one page per note type, plus the index. Written for a person.
- `Templates/`: Templater templates, wired via `.obsidian/templates.json`.
- `Templates/scripts/`: generated helpers. `operators.js` is written by
  `./workspace render` from `.workspace/workspace.json`; do not hand-edit it.

## Rule

Guides **explain**, `Standards/` **governs**. A guide links to the standard it
describes and never restates the rule, because two statements of one rule
diverge and the reader cannot tell which is current.

Templates are bound by the same house voice as everything else. No emoji
headings: use a callout where one was carrying a visual affordance. No em
dashes, including in filenames a template generates.
