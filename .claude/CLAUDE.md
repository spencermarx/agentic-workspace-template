# Harness

The agentic side of this workspace. Loads when working in `.claude/`.

## The layers, and which to reach for

| Layer | Loads | Use for |
|---|---|---|
| `rules/` | on demand, when a matching file is read | a convention that governs a file type |
| `skills/` | on trigger, from the description | a repeatable multi-step procedure |
| `agents/` | when dispatched | isolation, or a tool surface the main agent cannot have |
| `commands/` | when a person types `/name` | a deterministic action, especially one taking arguments |

Full contract: [harness-standards](../Workspace/Standards/harness-standards.md). Do not
restate it here.

## The two hard rules

**A rule is a pointer.** It carries exactly two frontmatter keys and links to
the `Workspace/Standards/` section that owns the wording. A rule that states the rule has
become a second source of truth, and the two will diverge.

**A description is the dispatch mechanism.** There is no router skill. A skill
fires because its description matched, so the description carries the triggers
in the words a person actually types, is pushy rather than tentative, and
carries negative routing where a sibling could plausibly capture the same
trigger.

## Layout

```
skills/<name>/SKILL.md               the only registrable file
skills/<name>/sub-skills/<name>.md   flat, never a nested directory
skills/<name>/references/<name>.md   depth, loaded on demand
skills/<name>/scripts/               deterministic helpers
skills/_stubs/<name>.md              not a skill until promoted
```

Helper scripts are colocated inside the skill that owns them, referenced through
`${CLAUDE_SKILL_DIR}`. There is no top-level tools directory.

**Skills invoke scripts; scripts never reference skills.** Always enter through
a `SKILL.md`, never by calling a script directly. The skill is the interface
layer and the script is the execution layer, and inverting that makes the
interface unmaintainable.

## Stubs

`skills/_stubs/` holds skills that are shipped but not wired: they point at
services this workspace does not have credentials for, or at infrastructure that
does not exist yet.

They are flat `.md` files, so they cannot register and cost nothing. Promoting
one means supplying the wiring its banner lists, moving it to
`skills/<name>/SKILL.md`, and deleting the banner.

## Credentials

Auth resolution order, in every skill and script, without exception:

1. environment variables
2. `.credentials/<service>/tokens.env`
3. error

Never a hardcoded value, never a fallback to someone's personal account.

## Settings

`settings.json` is committed and holds what every clone should have.
`settings.local.json` is git-ignored and holds anything machine- or
person-specific. A committed settings file must never contain a local path.

Changes to either go through the `update-config` skill rather than a hand edit.
