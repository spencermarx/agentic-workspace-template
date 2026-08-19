---
name: extend-architecture
description: >-
  Change the workspace's shape: add business domains, add an operator, add a top-level
  router. Edits `.workspace/plan.json`, applies it with `./hq`, registers rule globs for
  any new root folder, then re-renders and verifies. Use whenever someone says add a
  department, a team area, a new person, or restructure the vault. Do NOT use to gather
  context first (use `investigation-brief` then `explore-context`), or for one new
  instance under a router that already exists (use `new-area`).
argument-hint: '<what to add>'
---

<!-- workspace:no-mutate -->

# extend-architecture

The one skill that changes the workspace's **shape**. There is no separate
"initial setup" path: adding the first three business domains during bootstrap
and adding a fourth three years later are the same operation, through the same
plan and the same engine. That is what makes expansion first-class here instead
of a `--force` flag bolted onto setup.

You never hand-create a folder. You edit `.workspace/plan.json` and let the
engine build from it. A folder made by hand gets no `CLAUDE.md`, no row in the
folder map, and no parking lot, and nothing reports any of it.

Working notes for a large change belong in a
[`scratchpad`](../scratchpad/SKILL.md) entry, not in the vault.

## Step 1: validate the change against the ship rule

A new folder must be one of three things: a record type, an ownership zone, or a
domain. The test and the reasoning:
[vault-standards § Why exactly these ship](../../../Workspace/Standards/vault-standards.md#why-exactly-these-ship).

A **domain** belongs inside `Business/`. That is the whole reason `Business/`
ships empty: anything under it already matches `**/Business/**`, so it inherits
frontmatter, naming, and confidentiality routing the moment it exists, and no
rule has to be rewritten.

An **operator** goes under `Operators/`, which is the vault's only single-writer
zone.

A domain router at the vault **root** (`Clients/`, `Products/`) is allowed, and
it is the common legitimate case: the business partitions its own activity that
way and it is genuinely not a sub-part of one function. Take it, say out loud
that it costs Step 4, and then actually do Step 4.

If the change satisfies none of the three, say so and stop. Say what it should
be instead: usually a folder under an existing domain, or a note type rather
than a folder at all.

**Done when:** you can name which of the three classes this change is, and
whether it lands inside `Business/`, inside `Operators/`, or at the root.

## Step 2: edit .workspace/plan.json

Grammar: `.workspace/schema/plan.schema.json`. Worked example:
`.workspace/fixtures/plan.example.json`.

A **router** node, one that instances get added under later, carries the shape
its future instances will get. The engine reads these keys at `add` time and
nothing else supplies them:

- `instanceRole`, normally `leaf`
- `instanceTemplate: true`, so `new-area` can infer the parent from a name
- `instanceScaffold`: `["Activities", "Documents"]` for a business domain,
  `["Meetings", "Daily Notes"]` for an operator
- `instanceChildren`: `["decisions"]` for a business domain

Getting `instanceScaffold` wrong fails quietly. An operator added a year later
gets built with `Activities/` and `Documents/`, which is a domain's shape, and
nothing complains.

**Done when:** every new node has `path`, `role`, `title`, and `holds`, every
router node also carries the instance keys above, and the file still parses as
JSON.

## Step 3: apply it with the engine

One new instance under a router that already exists:

```bash
./hq add --parent Business --name "Sales" --dry-run
./hq add --parent Business --name "Sales"
```

`add` appends that node to the plan itself, so do not also hand-write it in Step
2. Step 2 is for the router and for anything `add` cannot express.

A change that adds or renames a **top-level** node is applied by reconciling the
whole plan instead:

```bash
./hq apply --dry-run
./hq apply
```

`apply` is idempotent and does not care whether the workspace was bootstrapped
this morning or three years ago, which is the point: growing a workspace is its
own operation, not a flag on first-time setup. Read the dry run before applying,
every time, and show it to the operator when the change touches anything already
authored.

**Done when:** the dry run and the applied run were the identical command, and
every folder the dry run listed exists on disk.

## Step 4: register rule globs for every new top-level folder

Do this in the **same operation**. Never leave it as a later cleanup.

Anything under `Business/` or `Operators/` needs nothing; it already matches. A
folder at the vault root matches nothing, so notes inside it get no frontmatter
rule, no naming rule, and no confidentiality rule. Nothing errors. The vault
simply stops being governed in that one corner, and reads as healthy.

Add `'**/<Folder>/**/*.md'` to the `paths:` list of each rule in
`.claude/rules/vault/` that should govern the folder, and `'**/<Folder>/**'` in
`confidentiality.md`, which governs binaries too. Match the syntax already
there: `**`, `*`, `?`, `[abc]`, nothing else.

**Done when:** every rule file in `.claude/rules/vault/` that ought to govern
the new folder names it in `paths:`, and each of those rules still carries
exactly two frontmatter keys.

## Step 5: re-render and verify

```bash
./hq render
./hq doctor
```

Then look rather than assume: open the root `CLAUDE.md` folder map and `Home.md`
and confirm the new structure is there. Fill any `__REPLACE_ME__` the engine
left, and act on every `<!-- AGENT: -->` comment.

**Done when:** `doctor` reports clean, the folder map and the Home nav both show
the new structure, and a note created in the new folder is governed by the rules
you expect -- open one and name which rules fired.

## Then stop

Do not commit. Print `git status --short`, summarise what changed, and leave the
commit to the operator.

A new root-level router is usually precedent-setting and awkward to reverse.
When it is, propose a [`decision-record`](../decision-record/SKILL.md) and let
the operator decide whether to write one.
