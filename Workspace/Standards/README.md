# Standards

Every convention in this workspace, stated exactly once. Full contract in
[harness-standards § The two-artifact invariant](harness-standards.md#the-two-artifact-invariant).

A rule loads on demand, when the main agent or a subagent reads a file matching
its glob. That is why standards live here rather than in a `CLAUDE.md`: a
`CLAUDE.md` governs a directory subtree, a rule governs a file type wherever it
lives, and a rule reaches subagents.

## The documents

| Document | Covers |
|---|---|
| [writing-standards](writing-standards.md) | House voice |
| [vault-standards](vault-standards.md) | Note types, frontmatter, vocabularies, naming, links |
| [confidentiality-standards](confidentiality-standards.md) | What never leaves the vault, credentials |
| [claude-md-contract](claude-md-contract.md) | The three tiers, budgets, the reusable boilerplate |
| [document-patterns](document-patterns.md) | Two buckets, dated bundles, the three registers |
| [decision-standards](decision-standards.md) | What earns a record, who may create one, numbering, supersession |
| [harness-standards](harness-standards.md) | Skills, rules, budgets, vendoring, settings |

## Intentionally unrouted

Sections that state a convention no glob can usefully target. They are read by
humans and by the skills that name them, not routed automatically.

- [claude-md-contract § Assigning a tier](claude-md-contract.md#assigning-a-tier) and its neighbours: consumed by the `bootstrap` and `new-area` skills at generation time.
- [document-patterns](document-patterns.md): shapes rather than file-type rules. The relevant skills cite them directly.
- [harness-standards § Settings split](harness-standards.md#settings-split) and [§ Plugins versus vendoring](harness-standards.md#plugins-versus-vendoring): configuration decisions rather than file-type rules.
