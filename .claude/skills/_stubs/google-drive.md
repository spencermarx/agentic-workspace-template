> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/google-drive/SKILL.md`, and delete this banner. See
> [README](README.md).

# google-drive

Upload local files and directories to Google Drive, optionally converting them to native Google formats, mirroring local folder structure.

## Wiring

Same Google service-account setup as `google-calendar.md`:

- A Google Cloud service account with domain-wide delegation, or OAuth for one user.
- `.credentials/google/` holding the key. Domain-wide delegation can act as any
  user in the domain, so this is the highest blast-radius credential in the set.
- `GOOGLE_DWD_CLIENT_ID` and `GOOGLE_IMPERSONATE_EMAIL` as environment
  variables, with no defaults baked in.

All four Google skills share one auth module. Promote them together or not at all.

## What it does

Markdown to Google Doc conversion, and directory-tree mirroring. This is the
deliverable-handoff primitive: the vault holds the source of truth, and a client
gets a Doc they can comment on.

Treat every upload as sending outward. Apply
`Standards/confidentiality-standards.md` before uploading anything that names a
client.
