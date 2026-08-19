# Template decisions

Decisions about **how this template is built**. They are not workspace content,
and a workspace forked from this template does not inherit them as its own.

They live here, under `.workspace/`, because that is the zone the template owns
and `./hq upgrade` carries. The consumer's register is `Decisions/` at
the repository root, and it starts empty.

Full contract: [decision-standards](../../Workspace/Standards/decision-standards.md).

| Record | Status |
|---|---|
| [Standards as rules routed to the files they govern](2026-08-18-standards-as-rules-routed-to-files.md) | active, amended |
| [Vendor third-party skills as plain files with inline provenance](2026-08-18-vendor-third-party-skills-as-plain-files.md) | active |
| [Cap the always-resident context budget](2026-08-18-cap-the-always-resident-context-budget.md) | superseded |
| [Standards are enforced by rules, not by a validator](2026-08-19-standards-are-enforced-by-rules-not-by-a-validator.md) | active, amended |
| [Setup talks before it looks, and looks before it proposes](2026-08-19-setup-talks-before-it-looks-and-looks-before-it-proposes.md) | active, amended |
| [The root is what the workspace defines, not what a business does](2026-08-19-the-root-is-what-the-workspace-defines.md) | active |

An amended record still holds. What changed since it was written is stated in a
note directly under its title, so a reader learns it before reading the body
rather than after acting on it.

## Why this split exists

The template shipped these records in `Decisions/`, so every fork opened with a
register of decisions about vendoring policy and bootstrap phase order presented
as the new workspace's own. That is the decision bloat the register is supposed
to prevent, shipped as a feature.

## Why the filenames are dated

They were numbered `0001` through `0005` until 2026-08-19. A sequence has to be
allocated, and allocation needs a single writer: two operators each taking
`0006` produce two differently named files that git merges cleanly and silently.
A date needs no allocation, and two records on the same day collide by filename
only when two people recorded the same decision twice, which is a conflict worth
having. The reasoning in full:
[decision-standards § Why dated rather than numbered](../../Workspace/Standards/decision-standards.md#why-dated-rather-than-numbered).
