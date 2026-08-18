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
Excalidraw, whose `data.json` is more than half personal stencil library and is
rewritten every session. Committing that one guarantees conflicts on a
single-line 171 KB blob that git cannot merge and a human cannot resolve.
