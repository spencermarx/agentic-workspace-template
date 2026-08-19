> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/slack/SKILL.md`, and delete this banner. See
> [README](README.md).

# slack

Read and write Slack: post to channels, read history, reply in threads, send direct messages, and search.

## Wiring

- A Slack app with a bot token, installed into the target workspace.
- `.credentials/slack/tokens.env` with `SLACK_BOT_TOKEN`.
- The bot invited to every channel it must read or post in. This is the step that is always missed.
- Scopes: `channels:history`, `channels:read`, `chat:write`, `users:read`. Add `groups:*` for private channels.

## What it does

Uses the Slack Web API directly over HTTP. No CLI required.

Note the confidentiality boundary: posting to Slack is sending outward. Apply
`Standards/confidentiality-standards.md` before any message that quotes client
material.
