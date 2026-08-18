# Domain Docs

<!-- Seed template — the written instance for this repo lives at .workspace/config/domain.md. When fixing either copy, mirror it in the other; a setup re-run merges, never blind-overwrites. -->

How tracker-driven skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **The glossaries** — per-context `CONTEXT.md` files (in this repo family: `docs/contexts/<context>/CONTEXT.md`, optionally indexed by a root `CONTEXT-MAP.md`). A single-context repo has one `CONTEXT.md` at the root instead. Read each one relevant to the topic.
- **`docs/engineering/adr/`** — read ADRs that touch the area you're about to work in.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `context` and `adr` skills create them lazily when terms or decisions actually get resolved, and the `/domain-modeling` skill decides what's worth capturing.

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in the relevant `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts [ADR: event-sourced orders] — but worth reopening because…_
