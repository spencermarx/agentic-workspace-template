> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/linkedin/SKILL.md`, and delete this banner. See
> [README](README.md).

# linkedin

Automate LinkedIn through a real browser session, with mandatory human confirmation before any write.

## Wiring

- The [`agent-browser`](../agent-browser/SKILL.md) CLI installed: this builds on it.
- A saved, authenticated browser session. Treat it as a credential.

Its six safety rules are the reason to promote it rather than script LinkedIn
yourself: confirmation before every write, domain locking, velocity limits, and
no bulk automation.

## What it does

Reading a profile or a company page to prepare for a conversation is the safe,
useful nine-tenths of this. The write path exists but should stay
confirmation-gated: automated posting is how accounts get restricted.
