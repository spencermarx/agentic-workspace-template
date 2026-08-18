# Standards

Every convention in this workspace, stated exactly once, and the registry that
proves each one is actually reaching the files it governs.

## How a standard works

Three artifacts, always. Full contract in
[harness-standards § The three-artifact invariant](./harness-standards.md#the-three-artifact-invariant).

1. **Statement.** One `##` section in a document below. The single source of truth.
2. **Router.** One `.claude/rules/<domain>/<slug>.md` file: a `paths:` glob plus
   a deep link back to that section. It never restates the rule.
3. **Registry row.** One row in the table below. This table is the drift oracle.

A rule loads on demand, when the main agent or a subagent reads a file matching
its glob. That is why standards live here rather than in a `CLAUDE.md`: a
`CLAUDE.md` governs a directory subtree, a rule governs a file type wherever it
lives, and a rule reaches subagents.

Run `./workspace validate` to check the invariant. It resolves every link and
anchor, verifies every glob matches at least one real file, and fails on a rule
without a row or a row without a rule.

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
| [external-paths](./external-paths.md) | The link-out registry and how the boundary is enforced |
| [harness-standards](./harness-standards.md) | Skills, rules, budgets, vendoring, settings |

## The registry

| Standard | Statement | Router | Governs |
|---|---|---|---|
| House voice | [writing-standards § House voice](./writing-standards.md#house-voice) | `.claude/rules/writing/house-voice.md` | every `.md` |
| Plain language for outbound text | [writing-standards § Plain language for outbound text](./writing-standards.md#plain-language-for-outbound-text) | `.claude/rules/writing/plain-language.md` | client, pipeline, proposal, offering notes |
| AI tells | [writing-standards § AI tells](./writing-standards.md#ai-tells) | `.claude/rules/writing/no-ai-tells.md` | marketing, content, proposal, collateral notes |
| Required frontmatter by note type | [vault-standards § Required frontmatter by note type](./vault-standards.md#required-frontmatter-by-note-type) | `.claude/rules/vault/frontmatter.md` | typed note folders |
| File naming | [vault-standards § File naming](./vault-standards.md#file-naming) | `.claude/rules/vault/note-naming.md` | meetings, people, activities |
| Attachments and binaries | [vault-standards § Attachments and binaries](./vault-standards.md#attachments-and-binaries) | `.claude/rules/vault/attachments.md` | `Attachments/` |
| Ubiquitous language | [vault-standards § Ubiquitous language](./vault-standards.md#ubiquitous-language) | `.claude/rules/vault/glossary-terms.md` | `CONTEXT.md` |
| Canonical and mirrors | [canonical-and-mirrors § The rules](./canonical-and-mirrors.md#the-rules) | `.claude/rules/vault/canonical-mirrors.md` | `Documents/` trees |
| Meeting note format | [meeting-standards § Meeting note format](./meeting-standards.md#meeting-note-format) | `.claude/rules/meetings/note-format.md` | `Meetings/` |
| Action items carry an owner and a date | [meeting-standards § Action items carry an owner and a date](./meeting-standards.md#action-items-carry-an-owner-and-a-date) | `.claude/rules/meetings/action-items.md` | meetings and activities |
| Decision record format | [decision-standards § Decision record format](./decision-standards.md#decision-record-format) | `.claude/rules/decisions/record-format.md` | decision registers |
| The recording threshold | [decision-standards § The recording threshold](./decision-standards.md#the-recording-threshold) | `.claude/rules/decisions/threshold.md` | decision registers and `Standards/` |
| What never leaves the vault | [confidentiality-standards § What never leaves the vault](./confidentiality-standards.md#what-never-leaves-the-vault) | `.claude/rules/clients/confidentiality.md` | client, pipeline, proposal trees |
| PII minimisation | [confidentiality-standards § PII minimisation](./confidentiality-standards.md#pii-minimisation) | `.claude/rules/clients/pii.md` | `People/` |
| Skill authoring contract | [harness-standards § Skill authoring contract](./harness-standards.md#skill-authoring-contract) | `.claude/rules/harness/skill-authoring.md` | `.claude/skills/` |
| Rule authoring contract | [harness-standards § Rule authoring contract](./harness-standards.md#rule-authoring-contract) | `.claude/rules/harness/rule-authoring.md` | `.claude/rules/` and `Standards/` |
| Context budget | [harness-standards § Context budget](./harness-standards.md#context-budget) | `.claude/rules/harness/context-budget.md` | every `CLAUDE.md` and `SKILL.md` |

## Intentionally unrouted

Sections that state a convention no glob can usefully target. They are read by
humans and by the skills that name them, not routed automatically.

- [claude-md-contract § Assigning a tier](./claude-md-contract.md#assigning-a-tier) and its neighbours: consumed by the `bootstrap` and `new-area` skills at generation time.
- [document-patterns](./document-patterns.md): shapes rather than file-type rules. The relevant skills cite them directly.
- [external-paths](./external-paths.md): enforced by `.gitignore`, not by a rule.
- [harness-standards § Settings split](./harness-standards.md#settings-split) and [§ Plugins versus vendoring](./harness-standards.md#plugins-versus-vendoring): configuration decisions, checked by `./workspace validate` rather than routed.
