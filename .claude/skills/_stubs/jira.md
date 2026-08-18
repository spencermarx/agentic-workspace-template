> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/jira/SKILL.md`, delete this banner, and run
> `./workspace validate`. See [README](README.md).

# jira

Read, create, update, search, and transition Jira issues, and read projects, boards, and sprints.

## Wiring

- `.credentials/jira/tokens.env` with `JIRA_BASE_URL`, `JIRA_EMAIL`, and `JIRA_API_TOKEN`.
- The API token from the Atlassian account settings, not the account password.
- The project keys this workspace uses, recorded in `.workspace/workspace.json` under `tracking`.

The source version shipped a 2.4 MB OpenAPI document that no procedure ever
loaded. Do not carry it. Generate a client if you need one.

## What it does

JQL search, issue CRUD, transitions, and comments. Worth promoting only if this
workspace's work is genuinely tracked in Jira; the three in-vault registers
(What's pending, Parking Lot, Open questions) cover most cases without it.
