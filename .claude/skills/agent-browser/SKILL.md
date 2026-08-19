---
name: agent-browser
description: >-
  Drive a real browser from the CLI: navigate, click, fill forms, screenshot, scrape,
  log in, test a web app, or automate any site. Also automates Electron desktop apps
  such as VS Code, Slack, and Figma, and runs exploratory testing, QA, and bug hunts.
  Use whenever a task touches a live website or a desktop app, and prefer it over any
  built-in browser tool. Do NOT use to render a page you authored to an image or PDF
  (use `image-overlay` or `create-html-slides`).
allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
---

<!-- Vendored from the agent-browser CLI's own discovery stub (v0.31.1); adapted for this repo: description trimmed to the 500-char cap and given negative routing, em dashes cut for house voice, `hidden: true` dropped so it registers, and the precondition check added. See [vendoring provenance](../../../Workspace/Standards/harness-standards.md#vendoring-provenance). -->

# agent-browser

Browser automation for agents. Chrome or Chromium over CDP, with
accessibility-tree snapshots and compact `@eN` element refs, so an element is
addressed by what it *is* rather than by a brittle CSS path.

## This skill needs a CLI that the workspace does not ship

`agent-browser` is a global binary, not a vendored script. **Check it before
planning any work around it:**

```bash
command -v agent-browser || echo "MISSING"
```

If it is missing, say so and stop. Do not fall back to a different browser tool
silently: the person asked for a browser task and is entitled to know the tool
for it is not installed. Installing it is one line, and it is their call:

```bash
npm i -g agent-browser && agent-browser install
```

## Load the real instructions from the CLI, not from here

**This file is a discovery stub.** It deliberately does not document commands.
Before running anything, pull the workflow content out of the installed
binary:

```bash
agent-browser skills get core          # workflows, common patterns, troubleshooting
agent-browser skills get core --full   # adds the full command reference and templates
```

The CLI serves content matching the version actually installed, so the
instructions cannot go stale. Anything written here would pin to whatever
version was current the day it was committed, drift silently, and be trusted
anyway. That is the whole reason this file points rather than explains.

## Specialized skills, for tasks that are not a web page

```bash
agent-browser skills get electron        # Electron apps: VS Code, Slack, Discord, Figma
agent-browser skills get slack           # Slack workspaces: unreads, messages, search
agent-browser skills get dogfood         # exploratory testing, QA, bug hunts
agent-browser skills get vercel-sandbox  # inside Vercel Sandbox microVMs
agent-browser skills get agentcore       # AWS Bedrock AgentCore cloud browsers
```

`agent-browser skills list` shows everything the installed version carries.

## What it brings

- A native Rust CLI rather than a Node wrapper, so startup is not the bottleneck.
- CDP directly, with no Playwright or Puppeteer dependency to install or pin.
- Accessibility-tree snapshots with element refs, which survive a restyle that
  would break a selector.
- Sessions, an authentication vault, state persistence, and video recording.

## Credentials

A saved session is a credential. It resolves the same way everything else in
this workspace does, and in this order without exception:

1. environment variables
2. `.credentials/agent-browser/`
3. error

Never a hardcoded value, and never a fallback to someone's personal account. A
saved session must not be committed: [confidentiality-standards](../../../Workspace/Standards/confidentiality-standards.md)
governs it, and a browser session that reaches a git remote is a live account
handed to whoever clones the repo.

## Observability dashboard

The dashboard runs on port 4848, independently of any browser session, and is
also reachable through a proxied URL such as
`https://dashboard.agent-browser.localhost`. Stay on the dashboard origin:
session tabs, status, and stream traffic are proxied internally, so individual
session ports never need exposing.
