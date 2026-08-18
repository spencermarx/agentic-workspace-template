# Color palette

The single source of truth for every color value. Any image prompt, infographic,
overlay, slide, or chart using a brand color references these exact tokens.

> [!warning] Placeholder values.
> This is a neutral slate chosen so the pipeline runs and looks composed out of
> the box. Replace the hex values below with your own. Keep the token names: the
> whole system references tokens, not hexes.

## Primary

| Token | Hex | Use |
|---|---|---|
| `brand-primary` | `#2F4858` | The single primary accent. Headlines, hero numbers, primary buttons, key chart elements, the logo. |

## The monochromatic scale

Built from `brand-primary`. The palette is deliberately monochromatic: one hue,
five values. A second hue is a decision to make once, in this file, not an
improvisation inside an asset.

| Token | Hex | Use |
|---|---|---|
| `brand-primary` | `#2F4858` | Primary accent |
| `brand-primary-dark` | `#17242C` | Body text and headings on light grounds, deep contrast |
| `brand-primary-mid` | `#4A6B7C` | Secondary accents, hover states, a second chart series |
| `brand-primary-light` | `#8FA3AD` | Captions, source attributions, metadata, gridlines |
| `brand-primary-tint` | `#E7EDF0` | Backgrounds, callout fills, subtle blocks |

## Neutrals

| Token | Hex | Use |
|---|---|---|
| `neutral-bg-warm` | `#F8F6F2` | Default background for editorial layouts, infographics, slides. Preferred over pure white. |
| `neutral-bg-cool` | `#F5F7FA` | Background for technical or product contexts |
| `neutral-ink` | `#1A1A1A` | Body text when `brand-primary-dark` reads too tinted |
| `neutral-border` | `#C9D0DD` | Card borders, table rules |
| `neutral-divider` | `#E0E4EC` | Thin dividers inside a card |
| `pure-white` | `#FFFFFF` | Product UI mockups and screen content only |
| `pure-black` | `#000000` | High-contrast logo lockups only |

## Hard rules

1. **Monochromatic only.** Every asset uses values from this file. If a chart
   needs a second series, use `brand-primary-mid` or `brand-primary-light`, never
   a contrasting hue.
2. **The primary appears in every asset.** It is what makes a set look like a
   set.
3. **Never write a hex inline in another skill.** Reference this file. A consumer
   that needs the value loads this sub-skill at the moment of need.
4. **The default background is `neutral-bg-warm`, not pure white.** Pure white
   reads cold in print and in social, and is reserved for product UI.
5. **When you replace these values, replace them here only.** Then run
   `grep -rn '#' .claude/skills --include='*.md' | grep -v get-brand-kit` and fix
   anything that turns up. Nothing outside this directory should hold a hex.
