---
type: decision
status: active
created: 2026-08-18
date: 2026-08-18
scope: none
---

# 0002 - Vendor third-party skills as plain files with inline provenance

## Context

Third-party skills enter a workspace by several routes. Installer tooling
scatters artifacts across a separate agents directory, cross-tool symlinks, and
a root lock manifest recording a source repository and content hash per skill.
Plugin marketplaces offer a managed, read-only, auto-updating bundle instead.

We want skills under `.claude/skills/` and nowhere else, and we want to adapt
them, which a managed read-only bundle does not allow.

There is also a hazard specific to a template repo: upstream documentation
legitimately contains double-braced uppercase template syntax, which the
identity gate would otherwise read as an unreplaced placeholder.

## Decision

Vendor third-party skills as **plain files under `.claude/skills/<name>/`**. No
separate agents directory, no symlinks, no lock manifest.

Record provenance **inline**, as an HTML comment at the top of the vendored
`SKILL.md`, in one of exactly two forms:

```
<!-- Vendored verbatim from <url> (<path> @ <sha>). See [ADR](...). -->
<!-- Vendored from <url> (<path>); adapted for this repo (<deltas>). See [ADR](...). -->
```

The `@ <sha>` pin is mandatory on both.

The verbatim string is **read by code**: a skill directory whose `SKILL.md`
contains it is excluded whole from the bootstrap mutate surface. Marker-driven
rather than a hardcoded directory list, so every future vendoring is covered by
the provenance line this decision already requires. An adapted skill stays on
the surface, which is correct, because we already changed it.

A skill is either vendored or installed as a plugin, never both.

Every upstream gets a block in `THIRD-PARTY-NOTICES.md`.

## Alternatives considered

### Keep a lock manifest with content hashes
- **Approach:** a root JSON file recording source and hash per skill.
- **Rejected because:** it puts skill metadata outside `.claude/`, against the
  standing rule, and in the repository this pattern came from it tracked nothing
  any tooling actually read.

### A central PROVENANCE.md index
- **Approach:** one file listing every vendored skill and its origin.
- **Rejected because:** it is a second index to keep in sync, drift-prone, and
  detached from the skill it describes. An inline comment travels with the file.

### Install the upstream plugin instead of vendoring
- **Approach:** subscribe to the marketplace bundle.
- **Rejected because:** we adapt several of these skills, and the upstream's own
  documentation warns that installing the plugin alongside copied files gives
  you every skill twice.

## Consequences

**Makes easier:** adapting a vendored skill, since it is an ordinary file.
Excluding upstream template syntax from the identity gate, by marker. Auditing
provenance, since it travels with the skill.

**Makes harder:** detecting upstream drift, which has no integrity hash and is
now a manual diff. The mandatory `@ <sha>` pin is what keeps that tractable, and
`./hq doctor --vendored` automates the comparison.

**Explicitly deferred:** any automatic re-vendoring. Pulling an upstream change
in is a human decision, because adapted skills have local deltas that a
mechanical update would silently discard.
