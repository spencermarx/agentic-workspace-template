# Credentials

One folder per service. Real secrets never enter git.

## How this works

`.gitignore` ignores everything under `.credentials/` and then un-ignores the
directories, the READMEs, the `*.example` templates, and the `.gitkeep` files.
A fresh clone therefore arrives with a ready-to-fill scaffold and no secret.

## Setup

For each service you actually use:

```
cp .credentials/<service>/tokens.env.example .credentials/<service>/tokens.env
```

Then fill in the real values. The `__REPLACE_ME__` sentinels in `.example` files
are permanent by design; the validator excludes this directory from its
placeholder check for exactly that reason.

## The contract every skill follows

Auth resolution order, in every skill and script, without exception:

1. environment variables
2. `.credentials/<service>/tokens.env`
3. error

Never a hardcoded value, never a prompt, never a fallback to someone's personal
account.

## Adding a service

1. `mkdir .credentials/<service>` and add a `.gitkeep`.
2. Write `tokens.env.example` with every variable the skill reads, each set to
   `__REPLACE_ME__` plus a comment saying where to obtain it.
3. Reference it from the skill's Wiring section.
