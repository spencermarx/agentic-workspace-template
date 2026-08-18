# the workspace Typography

The single source of truth for the workspace typography choices.

> **Status: partially defined.** The brand currently uses generic guidance ("bold sans-serif"), not a specific licensed typeface. Update this file when a primary typeface is selected and licensed.

## Current direction

| Use | Current rule |
|---|---|
| **Headlines / hero numbers** | Heavy bold sans-serif. Reference faces: Inter Black, Söhne Heavy, Söhne Breit Halbfett. Final selection TBD. |
| **Body / subheads** | Medium-weight sans-serif. Reference: Inter, Söhne Buch, or system-ui as fallback. |
| **Captions / metadata** | Same family as body, smaller size, desaturated color from `color-palette.md` (`brand-blue-light`). |
| **Overlay text on social images** | Heavy bold sans-serif loaded via Google Fonts in the overlay rendering script. Currently the overlay script uses an Inter-class face — verify the actual loaded font in `tools/scripts/sh/image-overlay/`. |

## Hard rules

1. **Sans-serif only.** No serif faces in marketing or product creative.
2. **Bold weight for hero elements.** A massive headline or stat must be in the heaviest available weight of the chosen face.
3. **Two weights maximum per asset.** A heavy weight for emphasis and a medium weight for body. No display, no thin, no italic unless intentional and rare.
4. **Never specify a typeface in another skill.** Reference this file. When the canonical face is locked in, this is the only place it changes.

## Open questions

- Which licensed face becomes the primary headline face?
- Which face becomes the body face? (Same family or contrasting?)
- What is the canonical type scale (h1 → caption sizes)?

Resolve these and update this file before they get hardcoded elsewhere.
