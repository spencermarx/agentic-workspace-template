---
name: get-brand-kit
description: >-
  The single source of truth for this workspace's brand: colors, typography, logos, the
  visual design system, and voice. Load the relevant sub-skill BEFORE constructing any
  image prompt, infographic, social asset, slide, landing page, or other marketing
  creative that must conform to brand. Never hardcode a brand value in another skill or
  document; always reference this one. Do NOT use for copy review (use
  `seven-copy-critics`) or for auditing a finished asset (use `brand-review`).
---

<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/get-brand-kit/SKILL.md @ 496d37273aca); adapted for this repo (fully de-branded: tokens renamed from brand-purple* to brand-primary*, which also removes the source's own note apologising that its "purple" reads as blue; a neutral placeholder palette and two generated placeholder wordmarks ship so the image and slide chain runs end to end from a fresh clone; the logo assets now live here rather than in image-overlay, correcting an inverted dependency). See [vendoring provenance](../../../Workspace/Standards/harness-standards.md#vendoring-provenance). -->

# get-brand-kit

The canonical source of truth for this workspace's brand. Every other skill,
document, prompt, and template that needs a brand value loads the relevant
sub-skill from here rather than hardcoding it.

> [!warning] This ships with a **placeholder** brand.
> The palette is a neutral slate and the wordmarks say the workspace name in
> plain type. That is deliberate: a fresh clone should look intentional rather
> than broken, and it must never ship someone else's brand. Replace the values
> in the sub-skills with your own; nothing else has to change, because nothing
> else holds a brand value.

## Why this exists

Brand values change. When they do, one file changes and every consumer picks up
the new value.

The failure this prevents is specific and has already happened once in this
lineage: a retired hex survived a rebrand, because it had been copied into image
prompts, guidelines, and templates "for convenience". Each copy looked correct in
isolation. Finding them all took longer than the rebrand.

## How to use it

1. Identify which dimension you need: color, logo, typography, layout, or voice.
2. Load only that sub-skill.
3. Use the values exactly. Do not paraphrase, derive, or interpolate.
4. If a value is not documented, **stop and ask**. Do not guess. Add it here
   first, then use it.

## Sub-skills

| Sub-skill | Load when you need |
|---|---|
| [color-palette](sub-skills/color-palette.md) | any color value: prompts, accents, overlay text, slide design, CSS, charts |
| [logos](sub-skills/logos.md) | a logo asset path, or a variant choice between light and dark grounds |
| [typography](sub-skills/typography.md) | a typeface, weight, or text hierarchy |
| [visual-design-system](sub-skills/visual-design-system.md) | to compose an asset: cards, badges, backgrounds, hierarchy, data marks |
| [voice-and-tone](sub-skills/voice-and-tone.md) | to align copy or messaging to brand voice |

## Hard rules for every consumer

1. **Never hardcode a brand value in another skill.** Reference the sub-skill.
2. **Never invent one.** If it is not documented here, the answer is "not yet
   defined". Raise it rather than fabricating.
3. **Update this skill, not your local copy.** When the brand evolves, it evolves
   here. Copying a value into a consumer "for convenience" is how the drift above
   happened.
4. **Renaming or removing a value is a brand-level change.** Update every
   consumer in the same change.
