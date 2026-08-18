> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/sanity/SKILL.md`, delete this banner, and run
> `./workspace validate`. See [README](README.md).

# sanity

Read from and write to a Sanity CMS: query content, create and update documents, publish drafts, upload assets, and build Portable Text.

## Wiring

- A Sanity project. Record `projectId`, `dataset`, and organization in `.workspace/workspace.json`, never in the skill body.
- `.credentials/sanity/tokens.env` with `SANITY_AUTH_TOKEN` carrying write access.
- The Sanity MCP server configured, or the shell scripts under `scripts/` for asset upload and large document creates.

The source version hardcoded a project ID belonging to an unrelated
organization. Parameterize before promoting.

## What it does

Content operations for a marketing site. Portable Text is the part worth reading
before writing anything: a body field is a structured array, not markdown, and
building it by hand is the usual source of corrupt documents.
