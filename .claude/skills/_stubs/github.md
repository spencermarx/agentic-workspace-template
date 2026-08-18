> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/github/SKILL.md`, delete this banner, and run
> `./workspace validate`. See [README](README.md).

# github

Read, write, and manage GitHub: repositories, branches, releases, pull requests, issues, and comments. Uses the `gh` CLI, so there is no SDK or API client to install.

## Wiring

- `gh auth login` completed for the account this workspace should act as. Verify with `gh auth status`.
- Optionally `.credentials/github/tokens.env` with `GITHUB_TOKEN`, for raw API calls that bypass `gh`.
- Set the default account in the skill body. The source version hardcoded one account in seventy-six places; do not reintroduce that. Read it from `gh auth status` or from `.workspace/workspace.json`.

## What it does

Wraps the `gh` CLI with the calls a knowledge workspace actually makes: opening
an issue from a parking-lot row, reading a repository's docs without cloning it,
and creating a release. Most of the value is in knowing which `gh` subcommand
answers a question without a clone.
