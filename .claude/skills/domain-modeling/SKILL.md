---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record a significant architectural decision, or when another skill needs to maintain the domain model.
---
<!-- Vendored from https://github.com/spencermarx/example-co (.claude/skills/domain-modeling/SKILL.md @ ce32987bb267); adapted for this repo (decision handoff re-pointed at the decision-record skill, and its prose re-grounded on that skill's actual contract: scope-local NNNN records under <scope>/decisions/, no generator and no ULID; file-structure examples re-keyed from an engineering repo to this vault; the glossary challenge extended to the agent's own coined terms via the conveying-clearly skill). Upstream lineage: https://github.com/mattpocock/skills (skills/engineering/domain-modeling/SKILL.md). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the _active_ discipline - challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down the moment they crystallize. (Merely _reading_ `CONTEXT.md` for vocabulary is not this skill - that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

This workspace has one glossary at the root, and decision records that live
beside the thing they are about:

```
/
├── CONTEXT.md                     ← the workspace glossary
├── Decisions/                     ← workspace-level, via the `decision-record` skill
│   ├── 0001-standards-as-rules-routed-to-files.md
│   └── 0002-vendor-third-party-skills-as-plain-files.md
└── <Area>/
    └── decisions/                 ← area-level, same skill, its own NNNN sequence
        └── 0001-<kebab-slug>.md
```

If a `CONTEXT-MAP.md` exists at the root, the workspace has several contexts and
the map points to where each glossary lives.

**Decision records are scope-local, never centralized.** A decision about one
area lives in that area's own `decisions/` folder and gets its own numbering;
only workspace-level decisions go in the root `Decisions/`. Glossaries may split
per context in the same way.

Create files lazily - only when you have something to write. If no `CONTEXT.md` exists, scaffold it with the [`context` skill](../context/SKILL.md) when the first term is resolved. **Decision records are never created by hand here** - when one is warranted, hand off to the [`decision-record` skill](../decision-record/SKILL.md), which owns the significance test, the per-scope `NNNN-<kebab-slug>` numbering, the location, and the index row in the register's `README.md`.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `CONTEXT.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y - which is it?"

Challenge your **own** terms the same way. Vocabulary you coined this session is not ubiquitous language, however settled it feels from inside: before it reaches a question, an answer, or an artifact a human reads, hold it to the [`conveying-clearly` skill](../conveying-clearly/SKILL.md)'s three-bucket rule - expand it to plain words, gloss it inline, or (rarely, for a genuine domain concept the humans themselves speak) propose promoting it into `CONTEXT.md` here. Never add session shorthand to the glossary to dodge glossing.

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account' - do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible - which is right?"

### Update CONTEXT.md inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up - capture them as they happen. The [`context` skill](../context/SKILL.md) owns the format and the generator that scaffolds the file.

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

### Record decisions as they crystallize

When a **significant** design decision settles during the session - a boundary, a pattern, a key standard, a chosen approach and the alternative you rejected - record it via the [`decision-record` skill](../decision-record/SKILL.md). Use that skill's gauge, not a separate bar: record what sets a precedent, is hard to reverse, or is surprising given its trade-off. Two of the three is a clear yes; one is a judgment call. Any change to `Standards/` always qualifies. Leave one-off or obvious choices unrecorded.

Don't author decision records by hand or invent a format. The `decision-record` skill owns the significance test, the per-scope `NNNN-<kebab-slug>` numbering, the location, the register index, the supersession protocol, and the Context/Decision/Alternatives/Consequences shape.
