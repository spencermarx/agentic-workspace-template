# Plugins

Two kinds live here, and the split is a licensing decision rather than a
preference.

## Vendored (committed, work on clone)

| Plugin | Why vendored |
|---|---|
| `agentic-copilot` | Not in the community store. MIT. It is the reason Claude Code is reachable from inside Obsidian. |
| `icloud-sync` | Not in the community store. Custom. |

Neither can be installed any other way, so a clone that did not carry them would
simply be missing them.

## Store-installed (declared, not committed)

Listed in `store-plugins.json` with their licenses. Four of the five are
**GPL-3.0 or AGPL-3.0**: committing their built `main.js` into a public,
MIT-licensed template would redistribute copyleft binaries under an incompatible
license.

They are two clicks each from Obsidian's plugin browser, so not vendoring them
costs a few minutes once. Vendoring them would cost a license violation.

Installing one puts it in a directory git would otherwise offer to stage, so
`.gitignore` ignores each store plugin by id, and `.obsidian/themes/` with them.
Without that, "not vendored" would last exactly until the first `git add -A`.
The ignore is by id rather than a blanket rule over `plugins/`, because the two
vendored plugins in the table above have to stay tracked. Both halves matter:
check `git check-ignore` before changing either.

`community-plugins.json` still lists every plugin, vendored or not, so the
**enable list travels with the clone**. That was one of the two reproducibility
gaps in the vault this template came from: a clone got the plugin code and
Obsidian enabled none of it. The other gap was `appearance.json`, so the theme
selection is committed too.

Run `./workspace obsidian-setup` to see what is missing on this machine.

## Per-machine config

A plugin whose `data.json` holds an absolute path or accumulating personal state
ships a `data.json.example` and a `SETUP.md`, and its `data.json` is
git-ignored. `./workspace obsidian-setup` writes the real file from the example.

This applies to `icloud-sync`, whose `data.json` holds an absolute path, and to
`agentic-copilot`, whose `editApprovalMode` decides whether an agent's edits land
without a prompt. That is a choice each machine should make rather than inherit
from a clone.

Excalidraw would belong here too, its `data.json` being more than half personal
stencil library and rewritten every session, a single-line 171 KB blob that git
cannot merge and a human cannot resolve. It needs no entry only because the whole
plugin is store-installed and therefore already ignored.
