---
name: set-credential
description: Put a credential where this workspace resolves it, at .credentials/<service>/tokens.env. Use whenever a token is missing or expired, a key needs rotating, a service needs connecting, or a stub's Wiring asks for credentials. Builds a guided setup script through `wizard` when the value must be fetched from a dashboard. Do NOT use to edit settings.json (use `update-config`).
---

# set-credential

One job: get a real credential into `.credentials/<service>/tokens.env` without
it ever landing anywhere else.

Everything that reads credentials in this workspace resolves them in one order,
stated in [the harness CLAUDE.md](../../CLAUDE.md#credentials):

1. environment variables
2. `.credentials/<service>/tokens.env`
3. error

You are writing step 2. Never a hardcoded value, never a fallback to someone's
personal account.

## The one hard rule

**The credential goes in the file and nowhere else** -- not a note, not a
`CLAUDE.md`, not `settings.json`, not a commit message, and never echoed back
into the transcript. What a note may record instead, and why, is
[confidentiality-standards § Credentials never enter a note](../../../Workspace/Standards/confidentiality-standards.md#credentials-never-enter-a-note).

`.credentials/` is git-ignored. Confirm that before writing, because the failure
is silent and permanent: a token committed once is in history forever.

## Process

### 1. Establish what is actually needed

Name the service, and the exact variable names the consumer reads. Get these
from the consumer, not from memory:

- A stub in `.claude/skills/_stubs/` states them in its **Wiring** section.
- An active skill or script states them where it reads the env var.

Do not invent a variable name. A credential written under the wrong key is
indistinguishable from a missing one at the point it fails.

**Done when:** every variable name is known and traced to the line that reads it.

### 2. Decide whether this needs a wizard

| Situation | Do this |
|---|---|
| The human already has the value | Ask for it, write it, stop. No wizard. |
| The value must be generated, or found by navigating a dashboard | Build a wizard. |
| Several values, or several services at once | Build a wizard. |

Most single tokens do not need a wizard. Reach for one when the acquisition path
is the tedious part -- the clicking, the finding, the "which of these four keys
is it" -- because that is the part nobody wants to re-explain next time.

### 3. Build it, if it needs building

Hand off to [`wizard`](../wizard/SKILL.md), which owns the script's shape and UX
entirely. Give it the service, the ordered stages, and for each value where the
human obtains it and which variable it fills.

Two adjustments for this workspace, which `wizard` does not assume:

- Set `ENV_FILE=".credentials/<service>/tokens.env"`. `wizard` defaults to
  `.env`, which is the wrong destination here.
- Skip `set_secret` / `set_var` unless this workspace genuinely has CI needing
  the value. Those stages target GitHub Actions, and most vault work has none.

Save the script as `.credentials/<service>/setup-wizard.sh`, beside what it
writes. `.credentials/**` is git-ignored, so it stays local by default, which is
the right default for something that touches secrets.

To share the procedure with everyone who clones this workspace, save it as
`setup-wizard.sh.example` instead: `.gitignore` un-ignores `*.example` under
`.credentials/`, which is the same mechanism `tokens.env.example` already uses.
Only ever commit the `.example`, and only after reading it top to bottom to
confirm it carries the steps and not a single value.

### 4. Verify without printing

Confirm the file exists, has the expected keys, and is ignored by git. Check the
key names, never the values: `grep -o '^[A-Z_]*=' <file>` shows the keys with
nothing after the `=`.

Then confirm the thing that was broken now works -- run the skill or script that
reported the missing credential. That is the only real proof.

**Done when:** the consumer succeeds, `git status` is clean of the credentials
path, and no value has appeared in the transcript.
