# Plugins

Two kinds live here, and the split is a licensing decision rather than a
preference.

## Vendored (committed, works on clone)

`agentic-copilot` is MIT, is not in the community store, and is the reason Claude
Code is reachable from inside Obsidian. A clone that did not carry it would
simply be missing it, because there is no other way to install it.

## Store-installed (declared, not committed)

Listed in `store-plugins.json` with their licenses. Both are **AGPL-3.0**:
committing their built `main.js` into a public, MIT-licensed template would
redistribute copyleft binaries under an incompatible license.

| Plugin | Why it is expected |
|---|---|
| Templater | The template engine. Every file in `Workspace/Templates/` is Templater syntax. |
| Excalidraw | The runtime for the `excalidraw` skill in `.claude/skills/`. |

They are two clicks each from Obsidian's plugin browser, so not vendoring them
costs a few minutes once. Vendoring them would cost a license violation.

Installing one puts it in a directory git would otherwise offer to stage, so
`.gitignore` ignores **every** subdirectory of `plugins/` and names back only
what has to travel. A blanket rule rather than a list of ids, because a list
only protects the plugins someone remembered to add to it, and "not vendored"
would otherwise last exactly until the first `git add -A`.

`community-plugins.json` still lists every plugin, vendored or not, so the
**enable list travels with the clone**. That was one of the reproducibility gaps
in the vault this template came from: a clone got the plugin code and Obsidian
enabled none of it.

Run `./hq obsidian-setup` to see what is missing on this machine.

## Per-machine config

A plugin whose `data.json` holds machine-specific state, or a setting a machine
should decide rather than inherit, ships a `data.json.example` and a `SETUP.md`.
`./hq obsidian-setup` writes the real file from the example and leaves an
existing one alone.

| Plugin | What the example carries |
|---|---|
| `agentic-copilot` | `editApprovalMode` decides whether an agent's edits land without a prompt, which is a security choice each machine makes. |
| `templater-obsidian` | The template folder and the user-scripts folder. Without them Templater opens an empty picker and `tp.user.operators` is undefined. |

Templater is the one store-installed plugin with files inside its ignored
directory, which is why `.gitignore` names those two paths individually. Its
built `main.js` stays ignored, so the AGPL obligation is intact.

Excalidraw needs no entry. Its `data.json` would qualify twice over, being more
than half personal stencil library and rewritten every session as a single-line
171 KB blob git cannot merge, but the whole plugin directory is already ignored.
