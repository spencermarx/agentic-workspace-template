# Agentic Copilot

Runs an agentic CLI (Claude Code, Gemini CLI, others) as a copilot inside
Obsidian, with streaming chat, vault-aware context, and edit diffs.

Source: <https://github.com/spencermarx/obsidian-ai>. MIT. Vendored here as
built files because it is not in the community store.

## Setup

There is no API key, and there is nothing to paste. The plugin **shells out to a
CLI you have already authenticated**, so it inherits your existing login. If
`claude` works in your terminal, it works here.

1. Confirm the CLI is on your PATH: `command -v claude`.
2. Copy the settings example if you want anything other than the defaults:
   `cp data.json.example data.json`.

## Settings that deserve a deliberate choice

| Setting | Default | Why it matters |
|---|---|---|
| `selectedAgent` | `claude-code` | Which CLI to spawn |
| `workingDirectory` | `vault` | The vault root becomes the agent's cwd, so `CLAUDE.md` and `.claude/skills` apply |
| `editApprovalMode` | `auto-accept` | Whether edits land without a prompt |
| `autoApplyEdits` | `false` | Whether they are written without you seeing the diff |

The last two are the pair worth thinking about. `auto-accept` with
`autoApplyEdits: false` means edits are approved automatically but still shown as
a diff before writing. That is the intended combination: fast, but nothing
changes in your vault without you having seen it.

## Updating

Replace `main.js`, `manifest.json`, and `styles.css` from a newer release of the
upstream repository, then restart Obsidian. `./workspace doctor` reports the
vendored version against upstream.
