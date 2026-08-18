# the workspace Visual Design System

The single source of truth for the *look and feel* of every the workspace visual asset - infographics, slide decks, landing pages, email graphics, marketing cards, hero images, and any other piece of editorial creative.

This sub-skill defines the **aesthetic system** the workspace visuals must conform to. It is distinct from `color-palette.md` (which defines hex values), `typography.md` (which defines typefaces), and `logos.md` (which defines logo assets). This file defines how those building blocks are *composed*.

## The North Star

the workspace's visual aesthetic sits at the intersection of four reference design systems:

| Reference | What we borrow |
|---|---|
| **Anthropic** | Warm cream backgrounds with subtle dot/grid texture, single muted accent used sparingly, publication-quality breathing room, editorial magazine feel, hand-tuned typographic spacing |
| **shadcn/ui** | Card-based composition with crisp 1px borders and refined drop shadows, small pill badges for taxonomy ("RESULT", "POLL", "PROOF"), mono fonts for metadata captions, multi-weight typographic hierarchy, refined corner radii |
| **Linear** | Asymmetric editorial layouts, generous negative space, restrained iconography, subtle layered depth |
| **Stripe** | Premium publication-quality polish, editorial grid systems, sophisticated use of single accent color, data visualizations as graphic elements |

The aesthetic we are NOT going for: flat marketing-poster look, centered-text-on-solid-color slides, bright contrasting accent colors, decorative illustrations, clip art, gradients with multiple hues.

## Core Composition Rules

### 1. Background

- **Default background:** warm cream off-white `#FAF9F6` or `#F8F6F2` (see `color-palette.md`)
- **Texture:** every infographic background MUST include a very subtle dot grid pattern - tiny soft brand-primary dots, evenly spaced, no more than 5% opacity. This adds depth without distracting.
- **Soft radial gradient:** the center of the canvas should be very subtly brighter than the edges, creating a gentle vignette that focuses the eye on the central card.

### 2. Card-based composition

Every infographic, data viz, callout, or marketing card lives inside a **card container** sitting on the textured background:

- **Border:** crisp 1px in muted slate-gray `#C9D0DD`
- **Corner radius:** 16px (consistent with shadcn `rounded-2xl`)
- **Drop shadow:** soft layered, 0–30% opacity blur, NEVER hard or pure black
- **Background:** cream `#FAF9F6` or pure white inside the card (slightly brighter than the page background)
- **Padding:** generous internal padding - at least 8% of card width on every side
- **Floating effect:** the card should feel like it floats above the background, like a real shadcn UI card

### 3. Pill badges (taxonomy)

Every card has a small pill badge in its top-left corner that names what the card *is*:

- Badge style: rounded-pill shape, 1px border in `#C9D0DD`, white background
- Content: tiny uppercase mono-spaced text in the brand primary `#2F4858`, plus a small filled brand-primary dot to its left
- Examples: `● RESULT`, `● POLL`, `● PROOF`, `● BENCHMARK`, `● INSIGHT`, `● DATA`

This single element is the most important shadcn/Anthropic visual cue - it instantly signals "this is a refined editorial product card, not a marketing poster."

### 4. Typographic hierarchy (multi-weight)

Every card composition uses **at least three distinct type treatments** to avoid the flat-poster look:

| Element | Treatment |
|---|---|
| **Display number / hero stat** | Massive heavy display sans-serif (Geist Black, Inter Display Black) in the brand primary `#2F4858`. Serves as the visual anchor. |
| **Headline / question** | Medium-large weight, dark text `#17242C` (or charcoal `#1A1A1A`). Sans-serif (Inter Medium) or contemporary editorial serif. |
| **Body / supporting copy** | Clean medium-weight sans-serif `#17242C`. Generous line height. |
| **Caption / metadata** | Tiny uppercase **mono-spaced** text in `#8FA3AD`. Used for attribution, source citations, and microcopy. The mono font is critical - it's the second most important shadcn signal. |

A poster has one weight. A product card has three or four. Always do three or four.

### 5. Dividers and separators

Use thin horizontal divider lines to separate semantic regions inside a card:

- 1px solid line in `#E0E4EC` (a very light slate-gray)
- Used between hero number and headline, between headline and option list, between body and footer caption
- Never use bold or thick dividers - they break the refined feel

### 6. Visualization elements

Every numeric or comparative card SHOULD include a small visualization element to elevate it above pure typography:

- **Sparkline** for growth/trend stats (thin curve in the brand primary, single dot at the endpoint, optional faint shaded area below)
- **Mini bar chart** for comparison stats
- **Donut/ring** for percentages
- **Outline icon** (1.5–2px stroke, the brand primary) for conceptual cards
- **Chevron arrows** (`>`) on interactive-looking option buttons

These elements must be **minimal, line-based, brand-primary, single-stroke** - never filled-in colorful chart art.

### 7. Interactive-looking option buttons

For polls, lists of choices, or any "pick one" pattern:

- Each option is a clean rounded rectangle (8px radius, `rounded-lg`)
- 1px border `#C9D0DD`
- Subtle drop shadow
- White background
- Inside: small filled brand-primary dot on the left, option label in `#17242C`, thin gray chevron `>` on the right
- Even spacing between options
- All options identical in size

These should look indistinguishable from real shadcn `Button` components.

### 8. Spacing and grid

- Generous breathing room everywhere - at least 8% padding inside cards, 6% margin between card and canvas edge
- Asymmetric layouts encouraged (text-left + visualization-right) over centered slabs
- Consistent vertical rhythm: hero element → divider → headline → divider → body → footer caption
- Never let elements touch the card border

## Reference Prompt Snippet

When constructing an image prompt for any infographic / data card, paste this aesthetic block into the prompt:

```
Premium editorial infographic in landscape 16:9 format, designed in the visual style of Anthropic's product marketing combined with the shadcn/ui design system. Background: warm cream off-white #FAF9F6 with a VERY SUBTLE faint dot grid pattern (tiny soft slate dots at 5% opacity) plus a soft radial gradient brightening the center.

Centered: a single card-style composition with crisp 1px border #C9D0DD, soft layered drop shadow, 16px rounded corners, generous internal padding, slightly brighter cream background inside the card.

Inside the card top-left: a small pill-shaped badge with thin border, tiny uppercase mono text "[BADGE LABEL]" in #2F4858, with a small filled slate dot to its left.

[Hero element - display stat in heavy sans-serif #2F4858, OR editorial headline]
[Optional small sparkline/icon visualization in #2F4858, line-based]
[Thin horizontal divider in #E0E4EC]
[Headline or body copy in #17242C, clean medium sans-serif]
[Bottom caption in tiny uppercase mono #8FA3AD]

Strict monochromatic palette: cream #FAF9F6, the brand primary #2F4858, dark text #17242C, muted borders #C9D0DD and #E0E4EC, caption gray #8FA3AD. NO other accent colors.

Premium editorial design like Anthropic's blog illustrations, Linear's marketing pages, Vercel's product cards, or Stripe's annual report graphics. Sharp typographic precision, refined spacing, subtle layered depth.
```

## What to avoid

These patterns break the aesthetic and must be flagged + rebuilt:

- Centered text on a solid flat color background with no card or texture
- Single typographic weight throughout (everything looks like one big headline)
- Bright contrasting accent colors beyond the brand primary
- Pure white backgrounds (feels cold and corporate)
- Hard black drop shadows
- Filled colorful chart graphics (pie charts in rainbow colors, 3D bar charts, etc.)
- Decorative illustrations, clip art, or stock-style icon sets
- Centered "poster" compositions with no asymmetric editorial layout
- Missing pill badge taxonomy
- Missing mono-spaced caption metadata
- Sans-only with no editorial polish (boring corporate slide look)

## Examples of cards rendered to this spec

The the workspace content sprint has produced two reference cards in this style:

1. `<an example asset path>` - `● RESULT` card with massive `5x` stat + sparkline + headline + attribution caption
2. `<an example asset path> workspace-Facebook/images/post-image-final.png` - `● POLL` card with editorial headline + 5 shadcn-style option buttons + `PICK ONE` caption

Use these as visual anchors when designing future cards. New cards should look like they came from the same product family.
