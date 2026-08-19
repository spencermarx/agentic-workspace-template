# Template decisions

Decisions about **how this template is built**. They are not workspace content,
and a workspace forked from this template does not inherit them as its own.

They live here, under `.workspace/`, because that is the zone the template owns
and `./hq upgrade` carries. The consumer's register is `Decisions/` at
the repository root, and it starts empty.

Full contract: [decision-standards](../../Workspace/Standards/decision-standards.md).

| Record | Status |
|---|---|
| [0001 Standards as rules routed to files](0001-standards-as-rules-routed-to-files.md) | active |
| [0002 Vendor third-party skills as plain files](0002-vendor-third-party-skills-as-plain-files.md) | active |
| [0003 Cap the always-resident context budget](0003-cap-the-always-resident-context-budget.md) | superseded by 0004 |
| [0004 Standards are enforced by rules, not by a validator](0004-standards-are-enforced-by-rules-not-by-a-validator.md) | active |
| [0005 Setup talks before it looks, and looks before it proposes](0005-setup-talks-before-it-looks-and-looks-before-it-proposes.md) | active |

## Why this split exists

The template shipped these five records in `Decisions/`, so every fork opened
with five decisions about vendoring policy and bootstrap phase order presented
as the new workspace's own. That is the decision bloat the register is supposed
to prevent, shipped as a feature.
