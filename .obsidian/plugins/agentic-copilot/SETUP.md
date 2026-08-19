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
| `editApprovalMode` | `approve` | Whether edits land without a prompt |
| `autoApplyEdits` | `false` | Whether they are written without you seeing the diff |

The last two are the pair worth thinking about, and the example ships the
cautious end of both: every edit is shown and waits for you. Switching
`editApprovalMode` to `auto-accept` while leaving `autoApplyEdits: false` is the
fast combination, where edits are approved automatically but still rendered as a
diff before they are written.

That is a choice each machine makes rather than one that arrives from a clone,
which is the whole reason `data.json` is git-ignored and this file exists. The
in-panel shield toggle flips the same setting.

## Updating

Replace `main.js`, `manifest.json`, and `styles.css` from a newer release of the
upstream repository, then restart Obsidian. `./workspace doctor` reports the
vendored version against upstream.
