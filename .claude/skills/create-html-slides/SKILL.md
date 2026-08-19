---
name: create-html-slides
description: >
  Generate branded HTML slide decks as single self-contained HTML files.
  Produces premium editorial presentations in the workspace visual style
  (Anthropic + shadcn/ui + Linear + Stripe aesthetic). Use for sales demos,
  internal presentations, marketing decks, and pitch materials. Animations
  included by default. Output is 16:9 widescreen, Google Slides compatible.
---
<!-- Vendored from https://github.com/spencermarx/anthony-and-spencer-business-workspace (.claude/skills/create-html-slides/SKILL.md @ 2e62970bb6cd); adapted for this repo (its two missing dependencies, get-brand-kit and the logo assets, now exist and are linked rather than named, so the gate can catch it if either disappears again; the palette inlined in viewport-base.css was another brand's and is replaced by the placeholder tokens, because a deck that renders in a stale brand looks correct and is wrong). See [vendoring provenance](../../../Standards/harness-standards.md#vendoring-provenance). -->


# Create HTML Slides

Generate a branded the workspace slide deck as a single self-contained HTML file. The LLM produces the complete HTML/CSS/JS. No build tools, no frameworks, no dependencies beyond Google Fonts.

## When to Use

- Sales demo decks (prospect-specific presentations)
- Internal team presentations
- Marketing decks and pitch materials
- Conference or workshop slides
- Any context where a polished, branded slide deck is needed

## When NOT to Use

- Quick text-only outlines (just write markdown)
- Interactive web applications (use a real framework)
- Print-only documents (use a document template)
- Infographics or single-image cards (use `image-prompt` + `openai`/`gemini`)

## Prerequisites

- Google Fonts CDN access (for Inter + Fira Code). System fonts work as fallback.
- Playwright via `npx` (PDF export only; HTML works without it)

---

## Procedure

### Phase 0: Detect Mode

- If the user provides a path to an existing `.html` slide deck, enter **enhance mode**: read the file, propose improvements, modify in place.
- Otherwise, enter **new deck mode** and proceed to Phase 1.

### Phase 1: Content Discovery

Gather these inputs. If the user has already provided enough context (e.g., a detailed outline doc), collapse this into a quick confirmation rather than an interrogation.

| Question | Why |
|---|---|
| Who is the audience? | Determines tone, density, jargon level |
| What is the one-sentence takeaway? | Anchors every slide's hierarchy |
| How many slides? (suggest 3-12) | Scopes the deck |
| What content exists already? | User may paste bullets, link a doc, or start from scratch |
| Any specific slide types needed? | Maps to types in `references/slide-types.md` |

### Phase 2: Generate Presentation

**Step 1: Load brand values.**

Load these [`get-brand-kit`](../get-brand-kit/SKILL.md) sub-skills and use the exact values:

| Sub-skill | What you need from it |
|---|---|
| [`color-palette`](../get-brand-kit/sub-skills/color-palette.md) | All CSS custom property hex values |
| [`typography`](../get-brand-kit/sub-skills/typography.md) | Font family direction and weight rules |
| [`visual-design-system`](../get-brand-kit/sub-skills/visual-design-system.md) | Card composition, pill badge, divider, and spacing rules |
| [`logos`](../get-brand-kit/sub-skills/logos.md) | Logo SVG file path for footer embedding |

**Step 2: Load reference docs.**

| Reference | Action |
|---|---|
| `references/viewport-base.css` | Read and inline verbatim into the `<style>` block |
| `references/html-template.md` | Follow for document structure, JS controller, and footer spec |
| `references/slide-types.md` | Use to select slide type for each slide and enforce density limits |
| `references/animation-patterns.md` | Include animations by default. Only omit if user explicitly requests a static deck. |

**Step 3: Embed the logo.**

Read the workspace logo SVG from the path documented in [`logos`](../get-brand-kit/sub-skills/logos.md). Inline the raw SVG markup into every slide's footer. Use the primary variant on light backgrounds, white variant on dark backgrounds.

**Step 4: Generate the HTML file.**

Produce a single self-contained HTML file following the architecture in `references/html-template.md`.

**Output location** (determined by deck purpose):

| Context | Output path |
|---|---|
| **For a specific person** | `People/{Name}/Presentations/{deck-name}/index.html` |
| **For a venture's customer (business)** | `Ventures/{venture}/Customers/{Customer}/Presentations/{deck-name}/index.html` |
| **Other / unclear** | Ask the user where to store it |

Person directories live under the top-level `People/` folder (for example `People/{Name}/`). Customer decks live under the relevant venture (for example `Ventures/hola-pip/Customers/{Name}/`). If neither context is clear from the request, ask before writing.

**Content density enforcement:** Each slide type has hard limits documented in `references/slide-types.md`. If the user's content exceeds a slide's capacity, split into multiple slides. Never cram. `overflow: hidden` clips anything that doesn't fit.

### Phase 3: Deliver and Refine

1. Open the HTML file in the default browser:
   ```bash
   open {path-to-html}
   ```

2. Ask the user for feedback. Iterate by editing the HTML file directly.

3. If PDF export is requested:
   ```bash
   bash ${CLAUDE_SKILL_DIR}/scripts/export-pdf.sh \
     --input {path-to-html} \
     --output {path-to-pdf}
   ```
   Default export: 1920x1080 (16:9, Google Slides compatible at 10" x 5.625").

---

## Reference Index

| File | Purpose | When to load |
|---|---|---|
| `references/viewport-base.css` | Responsive CSS foundation | Always (inline verbatim) |
| `references/html-template.md` | HTML/CSS/JS architecture spec | Always |
| `references/slide-types.md` | 12 slide types with density limits | Always |
| `references/animation-patterns.md` | Editorial CSS animations | Always (default on) |

## Related Skills

| Skill | Relationship |
|---|---|
| [`get-brand-kit`](../get-brand-kit/SKILL.md) | Source of truth for all brand values. Load sub-skills, never hardcode. |
| `image-prompt` | Use if the deck needs AI-generated images for image slides. |
| `seven-copy-critics` | Run deck copy through critics before a high-stakes presentation. |
| `brand-review` | Audit the finished deck against brand standards. |
