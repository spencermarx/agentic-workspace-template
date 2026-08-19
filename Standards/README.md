# Standards

Every convention in this workspace, stated exactly once.

## How a standard works

Two artifacts, always. Full contract in
[harness-standards § The three-artifact invariant](./harness-standards.md#the-three-artifact-invariant).

1. **Statement.** One `##` section in a document below. The single source of truth.
2. **Router.** One `.claude/rules/<domain>/<slug>.md` file: a `paths:` glob plus
   a deep link back to that section. It never restates the rule.

A rule loads on demand, when the main agent or a subagent reads a file matching
its glob. That is why standards live here rather than in a `CLAUDE.md`: a
`CLAUDE.md` governs a directory subtree, a rule governs a file type wherever it
lives, and a rule reaches subagents.

## The documents

| Document | Covers |
|---|---|
| [writing-standards](./writing-standards.md) | House voice, plain language, AI tells, completion criteria |
| [vault-standards](./vault-standards.md) | Note types, frontmatter, vocabularies, tags, naming, links |
| [meeting-standards](./meeting-standards.md) | Meeting note format, action items, attendees as entities |
| [decision-standards](./decision-standards.md) | The recording threshold, record format, superseding |
| [confidentiality-standards](./confidentiality-standards.md) | What never leaves the vault, credentials, PII |
| [claude-md-contract](./claude-md-contract.md) | The three tiers, budgets, the reusable boilerplate |
| [document-patterns](./document-patterns.md) | Two buckets, summaries, dated bundles, the three registers |
| [canonical-and-mirrors](./canonical-and-mirrors.md) | Canonical, mirror, and summary documents |
| [harness-standards](./harness-standards.md) | Skills, rules, budgets, vendoring, settings |

## Intentionally unrouted

Sections that state a convention no glob can usefully target. They are read by
humans and by the skills that name them, not routed automatically.

- [claude-md-contract § Assigning a tier](./claude-md-contract.md#assigning-a-tier) and its neighbours: consumed by the `bootstrap` and `new-area` skills at generation time.
- [document-patterns](./document-patterns.md): shapes rather than file-type rules. The relevant skills cite them directly.
- [harness-standards § Settings split](./harness-standards.md#settings-split) and [§ Plugins versus vendoring](./harness-standards.md#plugins-versus-vendoring): configuration decisions rather than file-type rules.
