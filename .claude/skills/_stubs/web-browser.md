> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/web-browser/SKILL.md`, delete this banner, and run
> `./workspace validate`. See [README](README.md).

# web-browser

Automate a real browser: navigate, click, fill forms, screenshot, read page content, manage cookies, and run JavaScript.

## Wiring

- A browser automation MCP server configured, or a local Playwright install.
- `.credentials/web-browser/` for any saved session state. Saved sessions are credentials: never commit one.

Declare which backend you are using in the skill body. Do not assume one is present.

## What it does

A low-level primitive other skills build on. Promote it when something concrete
needs it, not speculatively: it is the skill most likely to be invoked for tasks
better served by a plain HTTP fetch.
