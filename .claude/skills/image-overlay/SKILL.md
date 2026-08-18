---
name: image-overlay
description: >-
  Add styled text and a logo to a generated marketing image. Measures WCAG contrast against
  the actual destination regions, picks the readable logo variant, escalates to a text
  shadow when contrast is marginal, and composites through a headless browser render. Use
  whenever an image needs a headline or brand mark burned in. Do NOT use to generate the
  image (use `image-prompt` first) or to strip metadata afterwards (use `image-clean`).
---

<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/image-overlay/SKILL.md and tools/scripts/sh/image-overlay/overlay.sh @ 496d37273aca); adapted for this repo (script colocated under scripts/; logo paths and per-variant luminance parameterised, the latter now computed from the SVG fills so replacing the brand cannot silently invert variant selection; the "purple" variant renamed "primary"; logo assets moved to get-brand-kit, which claimed to own them; the venv escape hatch moved out of a fixed temp path; and the --logo-variant contradiction resolved in favour of the code). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->

# image-overlay

Composites a headline and a logo onto an image, choosing the logo variant by
**measured contrast** rather than by intent.

The measurement is the whole point. A logo placed by eye on a generated image is
unreadable roughly as often as it is readable, because generated images have no
stable ground: the top-right corner is dark in one render and washed out in the
next.

## Before you run it

Load [`get-brand-kit`](../get-brand-kit/SKILL.md) sub-skills `logos` and
`color-palette`. This skill reads logo assets from the brand kit; it does not
carry its own copies.

## Usage

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/overlay.sh" \
  --image path/to/base.png \
  --text "The headline" \
  --position bottom-left \
  --output path/to/final.png
```

| Flag | Meaning |
|---|---|
| `--image` | the base image |
| `--text` | the headline. Omit with `--logo-only` |
| `--position` | where the text sits. Drives the region sampled for text contrast |
| `--logo-only` | logo, no text. For assets that already carry their own typography |
| `--output` | destination |

Environment overrides, all optional:

| Variable | Effect |
|---|---|
| `BRAND_LOGOS_DIR` | look for logos somewhere other than the brand kit |
| `BRAND_LOGO_WHITE`, `BRAND_LOGO_PRIMARY` | point at specific files |
| `BRAND_LOGO_WHITE_LUMINANCE`, `BRAND_LOGO_PRIMARY_LUMINANCE` | override the computed luminance, for a mark whose dominant fill is not its first |
| `IMGTOOLS_VENV` | where to find a Pillow-bearing interpreter |

## How the variant is chosen

1. Crop the region the logo will actually occupy, not the whole image.
2. Compute mean WCAG relative luminance over that crop.
3. Compute each variant's luminance from the fills in its own SVG.
4. Composite whichever gives the higher contrast ratio.

**There is no `--logo-variant` flag, and passing one would not help.** The
measured choice is authoritative.

The source version documented such a flag and told callers to set it explicitly,
while the script overrode it unconditionally two hundred lines later. Callers
believed they were in control and were not. The behaviour was right and the
documentation was wrong, so the documentation is what changed.

If a specific variant is genuinely required, point `BRAND_LOGO_WHITE` and
`BRAND_LOGO_PRIMARY` at the same file. That makes the intent explicit rather
than hiding it behind a flag the algorithm ignores.

## Text handling

Font size is derived from text length, in five bands, so a short headline is
large and a long one still fits. Where white text falls below a 3:1 contrast
ratio against its own region, a triple-layer shadow is applied rather than
changing the color, which keeps the type reading as designed.

## Requirements

- **Pillow**, for cropping and luminance. The script names the venv command if
  it is missing.
- **A headless browser renderer**, for the composite. Fonts are loaded at render
  time, so a font not on the machine falls back silently: check the output.

## Anti-patterns

- **Overriding the measured variant.** It is measured because guessing failed.
- **Sampling the whole image** instead of the destination region. An image can be
  bright on average and black exactly where the logo lands.
- **Storing a logo next to this skill.** Read it from the brand kit, so a rebrand
  is one change.
- **Running it before the image is final.** It composites; it does not edit.
