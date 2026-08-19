> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/google-calendar/SKILL.md`, and delete this banner. See
> [README](README.md).

# google-calendar

Read, create, update, and delete Google Calendar events.

## Wiring

- A Google Cloud service account with domain-wide delegation, or OAuth for a single user.
- `.credentials/google/` with the service account key. This is the highest blast-radius credential in the set: domain-wide delegation can act as any user in the domain.
- `GOOGLE_DWD_CLIENT_ID` and `GOOGLE_IMPERSONATE_EMAIL` as environment variables, with no defaults.

Check first whether a Calendar MCP server covers your need. It usually does, with
far less setup and no service-account key on disk.

## What it does

Event CRUD and RSVP handling. The scripts live in the source repository under a
shared Google auth module that all four Google skills use.
