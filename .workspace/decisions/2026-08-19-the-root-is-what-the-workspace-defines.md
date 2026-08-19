---
type: decision
status: active
created: 2026-08-19
date: 2026-08-19
scope: none
---

# The root is what the workspace defines, not what a business does

## Context

The template shipped a root that named a business's activity: `Clients/`,
`Areas/`, an `Operations/` fan-out into Sales, Marketing, Legal, Finance. Every
one of those names was a guess about a company the template had never met.

The guess is not free. A folder in the shipped root is a claim that the template
knows something about what belongs inside it, and the rules layer is where that
claim gets cashed. A rule globbing `**/Sales/**` can only route to conventions
that already apply to every note in the vault, because there is no such thing as
sales frontmatter. So the folder shipped, matched a rule that told the agent
nothing it did not already know, and cost a name at the root that the business
might have wanted for something else.

The failure was quiet rather than loud. A business that partitions its work as
Practices and Engagements forked a vault that told it to think in Clients and
Areas, found no routing for its own words, and got silence -- not an error.

| Factor | Detail |
|---|---|
| Trigger | The structural rework of the shipped root, which forced the question "why is this folder here?" for every entry and produced no principled answer for most of them. |
| Constraint | The rules layer already exists and already decides what the agent is told about a file. Any ship rule that ignores it invents a second, weaker authority. |
| Goal | A ship-or-not decision that is mechanical, so it does not get relitigated per folder and per fork. |

## Decision

**A folder ships in the template if and only if the workspace itself defines the
shape of what goes inside it. Everything else is a domain, and domains belong to
setup.**

Three classes satisfy "the workspace defines the shape":

- **Record types.** The note has a schema this workspace owns -- a value in the
  closed `type` vocabulary plus the frontmatter that goes with it. `People/` and
  `Decisions/` ship because a person note and a decision record have the same
  required fields at any company on earth.
- **Ownership zones.** The folder exists to make single-writer isolation
  structural rather than a matter of etiquette. Its contents have no schema; its
  **path** is the point. `Operators/<key>/` ships for this reason alone.
- **Structural slots.** The name is fixed and the contents are defined
  elsewhere. `Workspace/` holds the substrate that survives a fork. `Business/`
  ships empty and holds whatever setup writes into it.

### The test

> **Can the template write a `.claude/rules/` pointer for this folder?**

A rule routes a folder to the `Workspace/Standards/` section that governs its
contents, so the question is really "does the template know anything true about
what lives here?"

`People/` passes: required frontmatter, the `relationship: internal|external`
split, naming. `Sales/` fails, and fails for a reason that will not change with
effort -- the only rule anyone could write for it is one that already applies
vault-wide.

This is what makes the decision not a matter of taste. It ties the ship decision
to the enforcement mechanism the template already has. A folder the rules layer
cannot say anything about is a folder the template has no business shipping.

### The shipped root, derived

```
Workspace/    Standards/ Guide/ Templates/ Views/   substrate, survives a fork
Business/     empty; setup fills it with domains
People/       person and org notes
Operators/    one private single-writer area per person
Decisions/    workspace-level decision records
Attachments/  Obsidian's attachment sink
```

Nothing else. No `Clients/`, no `Areas/`, no `Operations/`. Every domain router
is named in conversation with the operator and written by setup.

### Why `Business/` ships empty with a fixed name

An empty folder is an odd thing to ship, and it earns its place by being a
**stable glob target**. Rules that govern business notes glob `**/Business/**`.
A domain created inside it -- `Business/Sales/`, `Business/Client Delivery/`,
whatever the business actually calls its work -- is routed the moment it exists,
and **no rule is rewritten**.

The alternative is setup editing `.claude/rules/` frontmatter as it creates
folders, which means the enforcement layer is generated rather than authored,
and `./hq upgrade` can no longer tell a template rule from a local one. A fixed
name at a known depth buys the whole thing for the cost of one empty directory.

The consequence is worth stating plainly: a folder created at the vault **root**
matches no glob and gets no routing until someone writes one. That is the deal.

### The concurrency consequence

`Operators/<key>/` is single-writer. One person's meeting notes and daily notes
live under a path nobody else writes to, so two operators working the same week
produce zero conflicts in each other's material. The isolation is structural --
it holds whether or not anyone remembers the convention.

Shared artifacts get the opposite treatment on purpose. A standard, a decision
record, a `Business/` domain note **should** conflict when two people change it,
because a conflict there is two people changing an agreed thing, and that
deserves to be seen rather than merged away. Git already reports it correctly;
the design's job is to make sure the conflict lands where it is informative and
never where it is noise.

## Alternatives considered

### Ship a superset of business vocabularies and prune at bootstrap

- **Approach:** what the template did before. Ship `Clients/`, `Areas/`,
  `Operations/` and the rules that go with them; have bootstrap delete the
  folders the business does not need and drop rules whose globs match nothing.
- **Rejected because:** the superset is one person's vocabulary wearing a
  general-purpose label. A business whose words differ got no error, only
  silence -- unroutable folders and a root that read like someone else's
  company. Pruning also makes the rules layer partly generated, so a template
  rule and a local rule become indistinguishable and `./hq upgrade` loses the
  ability to reconcile them. And the pruning only ever ran at fork time; the
  business that added a legal function a year later was back to no routing.

### State the boundary in prose, or encode it in a naming convention

- **Approach:** keep the boundary documented -- a `Workspace/Standards/` section
  saying which folders are template-owned, or a prefix such as `_sales/` marking
  business folders -- and let people follow it.
- **Rejected because:** a documented boundary is enforced by memory, and the
  file it governs is edited by whoever is in a hurry. A prefix does slightly
  better, since a glob can match it, but it puts the load-bearing distinction in
  a character that any rename silently drops, and it makes every business folder
  ugly in the file explorer for the benefit of a machine. `Business/` as a real
  parent gets the same glob for free and survives renames of everything beneath
  it. This decision exists because the previous boundary **was** conventional and
  drifted.

### Johnny.Decimal numeric areas

- **Approach:** number the root as areas and categories -- `10-19 Business`,
  `20-29 Operations` -- so every folder has a stable identifier independent of
  its name, and notes can be addressed by number.
- **Rejected because:** it is genuinely better information architecture at
  scale, and that is exactly why it does not belong here. Adopting it changes
  every path, every rule glob, every template, every view, and the way people
  refer to things out loud. It is a larger commitment than the one being made
  today and deserves its own record with its own alternatives, not a rider on
  this one. Nothing in this decision forecloses it: the ship test is about which
  folders exist, and it would survive a renumbering unchanged.

## Consequences

**Makes easier:**

- Deciding whether a folder ships. The question is mechanical and has one
  answer, so it does not get argued per folder or re-argued per fork.
- Growing the business side. A new domain goes under `Business/`, is routed by
  the existing globs on creation, and requires no harness change.
- Multi-operator work. Personal material cannot conflict because the path
  forbids it, and shared material conflicts visibly, which is the correct
  outcome.
- Recognising the vault. A fork opens showing the business's own words, not the
  template author's.

**Makes harder:**

- This migration. Moving `Standards/`, `Obsidian/`, and the per-person folders
  into `Workspace/` and `Operators/` touched nearly every path in the repository
  -- rule globs, guide links, view definitions, skill references, the CLI itself,
  which was renamed from `./workspace` to `./hq` because a root file named
  `workspace` collides with `Workspace/` on a case-insensitive filesystem.
- Putting a domain at the vault root. It matches no shipped glob and gets no
  routing until someone writes a rule with the right `paths` frontmatter. The
  cheap path is `Business/<domain>/`; anything else is opt-in work.
- Adding a root folder at all, which now requires arguing that the workspace
  defines the shape of its contents -- usually meaning a new `type` in the closed
  vocabulary, which is a reviewed edit to a standard.

**Explicitly deferred:**

- Johnny.Decimal, per the alternative above. Its own decision, if ever.
- Whether `Business/` should be seeded with a single example domain so the empty
  folder explains itself. Doing so would ship a vocabulary guess by the back
  door, but an empty directory that git barely tracks is a real usability
  problem, and the current answer is documentation rather than structure.
- An explicit expansion mode for setup. Adding a top-level domain a year in is a
  `./hq bootstrap --force` reconciliation today, and nothing surfaces that
  outside an error message.
