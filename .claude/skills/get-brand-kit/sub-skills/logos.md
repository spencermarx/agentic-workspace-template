# Logos

## The assets

| File | Use on |
|---|---|
| `../assets/logos/logo-primary.svg` | light grounds |
| `../assets/logos/logo-white.svg` | dark grounds and photography |

Both are the same artwork; only the fills differ. They live here, in the brand
kit, because the brand kit is the source of truth for brand assets. A consumer
that needs a logo reads this file for the path and never stores its own copy.

> [!warning] Placeholder marks.
> Both are generated wordmarks carrying the workspace name. Replace them with
> your own and **keep the filenames**, so nothing that references them changes.

## Picking the variant

Pick by measured contrast against the region the logo will sit on, not by eye
and not by intent.

The [`image-overlay`](../../image-overlay/SKILL.md) skill does this
automatically: it samples the destination region, computes WCAG relative
luminance, and selects the variant with the higher contrast ratio. **Its
selection is authoritative and overrides any variant you pass it.** That is
deliberate: a caller guessing from the filename was the source of most wrong
selections.

When choosing by hand, the rule is the same one the script encodes: if the
region's relative luminance is above roughly 0.5, use `logo-primary`; below,
use `logo-white`.

## Hard rules

1. **Never store a copy of a logo elsewhere.** Reference the path.
2. **Never recolor a logo inline.** If you need a fill that does not exist, it is
   a brand decision: add a variant here.
3. **Never place a logo on a busy region** without measuring contrast against the
   region it actually covers, not the image average.
4. **Keep the clear space.** No other element within half the mark's height.
