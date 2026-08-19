# Obsidian

This folder holds the mechanics of the vault, not content. Guides for humans,
templates for note creation, saved views. Nothing here is knowledge about the
business.

## Layout

- `Guide/`: one page per note type, plus the index. Written for a person.
- `Templates/`: Templater templates. Templater is configured from
  `.obsidian/plugins/templater-obsidian/data.json.example`; see the `SETUP.md`
  beside it.
- `Templates/scripts/`: generated helpers. `operators.js` is written by
  `./workspace render` from `.workspace/workspace.json`; do not hand-edit it.
- `Views/`: the `.base` files. Ordinary vault files, so the file explorer shows
  them and `Home.md` can link them. They were under `.obsidian/bases/`, where
  nothing could reach them and, across months of use, nothing did.

## Rule

Guides **explain**, `Standards/` **governs**. A guide links to the standard it
describes and never restates the rule, because two statements of one rule
diverge and the reader cannot tell which is current.

Templates are bound by the same house voice as everything else. Nothing checks
this; read [writing-standards](../Standards/writing-standards.md) and hold the
line yourself.

## Two things that look wrong and are not

**Obsidian's own Templates and Daily Notes core plugins are off** in
`core-plugins.json`. Both use the core template engine, which cannot execute the
`<%* %>` blocks every file in `Templates/` is built from; pointed at this folder
they paste the script in as literal text. Templater is the only engine here.

**A `.base` column must have a writer.** Before adding one, find the template
that writes the property. A column nothing writes renders empty for every
adopter forever, and nothing in the repo will tell you. Prefer a `file.` builtin
such as `file.mtime` over a hand-maintained property that nothing refreshes.
