# Confidentiality standards

## What never leaves the vault

Material here is written on the assumption that it stays here. An agent does not
send outward on its own judgment. Publishing is a human act.

## Credentials never enter a note

Access notes record the system, the account identifier, the owner, and where the
credential lives: a password manager item name, or a path under `.credentials/`.
They never record the credential itself.

A token pasted into a note is in git history permanently, and git history is
what the whole workspace is built to preserve.
