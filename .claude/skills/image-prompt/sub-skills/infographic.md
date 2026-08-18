# Infographic Image Prompt Build + Review Sub-Skill

Build and validate an image prompt for an **infographic, chart, or data visualization** that will accompany a Proof Post, stat-first hook, or any post whose core payload is quantitative. Runs a three-critic review loop tuned for **typographic, data-driven imagery** that will receive a **logo-only stamp** (no text bridge) in post-processing — the infographic carries its own typography.

Use this sub-skill when the image's job is to communicate a stat, comparison, framework, or chart visually. For editorial photography on social posts, load `social.md` instead. For blog images, load `blog.md` instead.

## How infographic differs from social/blog

- **Typography is intentional, not banned.** Unlike editorial prompts (where "no text" is enforced), infographic prompts MUST request specific labels, numbers, axis text, etc. The third critic (Chart Accuracy Critic) verifies that every text element will be correct, accurate, spelled correctly, and cohesive — and that the chart visually makes sense as a coherent graphic.
- **No physics check.** Infographics aren't physical scenes, so the social/blog Physical Accuracy Critic doesn't apply. Instead, the third critic focuses on text accuracy and chart coherence — the failure modes that actually matter for data visualizations.
- **Logo-only post-processing.** The image will receive a the workspace logo stamp via `image-overlay --logo-only` — no text bridge. The composition must therefore be self-explanatory and scroll-stop on its own.
- **Generator preference: Gemini.** Gemini's typography rendering is significantly stronger than OpenAI's. If the generator override forces OpenAI, the Chart Accuracy Critic flags any meaningful text load as risky.
- **the workspace brand palette.** Load `.claude/skills/get-brand-kit/sub-skills/color-palette.md` for the current brand color values and palette rules. Use those exact values in the prompt — never hardcode hex values in this skill.

## Default Aesthetic (load before drafting)

**Mandatory first step:** before drafting any infographic prompt, load `.claude/skills/get-brand-kit/sub-skills/visual-design-system.md` and apply it as the default aesthetic. That file defines the the workspace visual language for all editorial cards — warm cream background with dot grid, card-based composition with crisp borders and soft shadows, pill badge taxonomy, multi-weight typographic hierarchy, sparkline visualizations, the Anthropic + shadcn + Linear + Stripe reference DNA. Every drafted prompt MUST embed the reference snippet from that file unless the caller explicitly overrides.

**Override:** the caller can pass an `aesthetic_override` field (see Inputs below) with a different design direction (e.g., "data-dense academic chart," "warm hand-drawn editorial," "dark mode product UI mockup"). If supplied, the override REPLACES the default visual-design-system aesthetic — do not blend the two. Otherwise, default applies.

## Inputs (What the Caller Must Provide)

1. **Post body** — the full text of the social or blog post the infographic accompanies. The Message Relevance Critic uses this to judge whether the visualized data matches the post's specific argument.
2. **Concept description** — a 1–3 sentence description of the chart/framework concept. Includes the chart type (bell curve, bar comparison, before/after split, horizontal ranking, stacked donut, callout) and the specific stat or relationship being visualized.
3. **The data** — the actual stats, percentages, comparisons, or framework elements to render in the chart. Be specific — "53.5% conversion lift" not "a conversion lift."
4. **Generator** — `gemini` (the default for infographics) or `openai`.
5. **Initial draft prompt** — a first-pass prompt the caller has written.
6. **Aesthetic override (optional)** — a different visual direction that replaces the default the workspace visual-design-system aesthetic. Omit to use the default.

## Outputs

After the loop completes, the caller receives one of two outcomes:

### Outcome A: Validated Prompt
A finalized prompt string that has passed all three critics in the same round. The caller proceeds to generate the image, then runs the result through `image-overlay --logo-only` (per `social-drafting` sub-skill, Logo-Only pipeline).

### Outcome B: Pivot Recommendation
After 3 failed iterations, the loop returns a structured pivot recommendation. For infographics, common pivots are: simpler chart type, fewer labels, switching from OpenAI to Gemini if text is the failing dimension, or rethinking which stat to lead with.

## Procedure

### Step 1 — Receive and parse inputs

Hold the post body, concept description, data points, generator, and initial draft prompt in working context. Initialize iteration count to 1.

### Step 2 — Spawn three critic sub-agents in parallel

Use the `Agent` tool with `subagent_type=general-purpose`, sending all three tool calls in a single message. Each critic receives the post body, the concept description, the data, the current prompt draft, the generator, and the critic's exact mandate from below.

### Step 3 — Synthesize feedback

Read all three critic responses. The prompt is ready to generate ONLY if all three return PASS in the same round.

### Step 4 — Iterate

Rewrite the prompt addressing every REVISE comment. Re-run Step 2 with the revised prompt. Increment iteration count.

### Step 5 — Cap and pivot

**Maximum 3 iterations.** If the prompt still fails any critic on the third iteration, return Outcome B (Pivot Recommendation).

### Step 6 — Return

When all three critics PASS in the same round, return Outcome A (the finalized prompt string).

## Critic Mandates

Send these EXACT prompts to the three sub-agents.

### Critic 1: Scroll-Stop Critic (Infographic Edition)

```
You are reviewing a draft prompt for an infographic, chart, or data visualization that will appear in a LinkedIn or Facebook feed. Your only job is to judge whether the visual described would stop someone scrolling.

Score the described visual 1–5 on visual interest:
- 5: Bold and arresting. Strong typographic hierarchy, single dominant insight, instantly readable at thumbnail size. The kind of chart someone would screenshot.
- 4: Clean and confident. Clearly designed, not template-y. Reader pauses on it.
- 3: Competent but generic. Looks like a standard B2B SaaS chart.
- 2: Cluttered, low-contrast, or template-flat.
- 1: Boring, hard to read, or visually inert.

Bias toward bold typographic hierarchy, single dominant data point, high contrast. Bias against cluttered multi-panel dashboards, faint pastel palettes, or "every metric on one chart" compositions. The bar for social infographic is "would stop scroll AND be readable in <1 second" — competence is not enough.

If the score is 4 or 5, return: `PASS — <one-line reason>`.
If the score is 1–3, return: `REVISE — <specific feedback on what's flat, generic, or hard to read, plus a concrete suggestion>`.

Do NOT comment on relevance to the post or rendering feasibility. Judge ONLY visual interest.

POST BODY:
{post_body}

CONCEPT DESCRIPTION:
{concept_description}

DATA:
{data}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

### Critic 2: Message Relevance Critic (Infographic Edition)

```
You are reviewing a draft prompt for an infographic against the post it's meant to support. Your only job is to judge whether the visualized data communicates the post's specific argument.

A few specific failure modes for infographics:
- The chart shows a stat that's tangentially related to the post but not the post's central claim
- The chart visualizes one number when the post's argument requires a comparison (or vice versa)
- The chart's framing contradicts the post's framing (e.g., post says "X is bad" but chart shows X neutrally)
- The chart includes more data points than the post discusses, distracting from the central argument
- The chart leaves out the data point that IS the post's hook

The image will receive a the workspace logo stamp in post-processing but NO text overlay. The chart must communicate the post's central data point on its own — the typography embedded in the chart IS the message.

If the chart will clearly communicate the post's central data point, return: `PASS — <one-line reason>`.
If there's a disconnect, return: `REVISE — <specific feedback on what doesn't connect and what would>`.

Do NOT comment on visual interest or rendering feasibility. Judge ONLY message relevance.

POST BODY:
{post_body}

CONCEPT DESCRIPTION:
{concept_description}

DATA:
{data}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

### Critic 3: Chart Accuracy Critic (Infographic Edition)

```
You are reviewing a draft prompt for an infographic. Your only job is to verify that (a) every piece of text the model is being asked to render will be correct, accurate, spelled correctly, and cohesive, AND (b) the chart will visually make sense as a coherent graphic.

Infographics intentionally include text (labels, numbers, axis titles, callouts) — that's the entire point. So the question is NOT "will the model render text" but "is every piece of text in this prompt correct, well-specified, and unlikely to garble."

Check for these failure modes:

**Text accuracy checks:**

1. **Every text element must be specified verbatim.** Does the prompt name the EXACT text strings to render, in quotes? Vague phrasing like "label the bars" is a recipe for the model inventing wrong text. Every label, number, percentage, axis title, and callout must appear in the prompt as quoted exact text. Flag any text element that's described but not quoted.

2. **Spelling and accuracy.** Read every quoted text string carefully. Are all words spelled correctly? Are numbers consistent with the source data provided? Are units (%, $, hours, etc.) correct and consistent? Flag any typo, inconsistency, or stat that doesn't match the source data.

3. **Cohesion across labels.** Do the text elements use consistent grammar, capitalization, terminology, and style across the chart? (e.g., don't mix "Industry median" with "Top quartile (top 25%)" — pick one labeling convention.) Flag any inconsistency.

4. **Text load reasonable for the generator.** Does the prompt request more than ~10–15 words of text total? Even Gemini's stronger typography starts garbling at high text counts. If the generator is OpenAI, the threshold is much lower (~3–5 words) since OpenAI handles infographic typography poorly. Flag overload and suggest reducing or splitting into multiple visuals.

5. **Numerical text risk.** AI models often subtly garble digits, especially in long numbers, decimals, and dates. Flag any image with critical numbers and recommend verifying every character after generation.

**Visual coherence checks:**

6. **Chart type matches the data.** Is the chosen chart type (bell curve, bar, donut, line, ranking, callout) appropriate for what's being shown? A bar chart for trends, a pie for ranked comparisons, a line for unrelated single values — all fail. Flag and suggest the right type.

7. **Single dominant insight.** Does the chart have one clear focal point that the viewer's eye lands on first? Multi-focal charts with no hierarchy fail at scroll speed. Flag if there's no clear "this is the number/insight that matters most."

8. **Clutter / multi-panel requests.** Does the prompt ask for multiple charts in one image, dashboards, side-by-side grids, or layered visualizations? AI models render these as garbled noise. Flag and suggest single-focal-point composition.

9. **Visual hierarchy specified.** Does the prompt name a clear hierarchy (largest element = the headline number; smaller elements = supporting labels)? If hierarchy is implicit, the model picks for you and usually picks wrong. Flag if hierarchy is unspecified.

10. **Color and contrast specified.** Does the prompt name accent colors that match the the workspace brand palette (defined in `.claude/skills/get-brand-kit/sub-skills/color-palette.md` — load it for current values), the background, and the contrast direction? Flag if colors are unspecified, low-contrast, or use hues outside the documented brand palette.

11. **Logo space.** Has the prompt requested negative space in the top-right corner for the logo stamp WITHOUT asking the model to draw the logo itself? Flag if missing.

12. **Spatial / typographic specificity vs intensity language.** Does the prompt rely on intensity adjectives ("very bold," "huge", "dramatic") instead of concrete typographic specs (font weight, point size relative, position on canvas)? Flag and suggest replacing.

If the prompt passes ALL accuracy AND coherence checks, return: `PASS — <one-line reason>`.
If any text accuracy or visual coherence issue is present, return: `REVISE — <specific feedback on what's wrong, with a suggested rewrite of the problematic phrasing>`.

Do NOT comment on visual interest or message relevance. Judge ONLY text accuracy and visual coherence.

POST BODY:
{post_body}

CONCEPT DESCRIPTION:
{concept_description}

DATA:
{data}

GENERATOR:
{generator}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

## Why Three Critics, Not One

A single generalist reviewer tends to give vague, balanced feedback. Three focused critics produce sharper, more actionable feedback because each is forced to commit on its lane and ignore everything else.

## Why Cap at 3 Iterations

A prompt that fails the same critic three times is signaling a structural concept problem (or, for infographics, often a generator-vs-text-load mismatch). Capping at 3 forces a structural fix rather than endless rewrites.

## Example Invocation

> Run the `image-prompt` skill's infographic sub-skill (`sub-skills/infographic.md`) on this prompt before generation:
>
> - Post body: [full text of the Proof Post]
> - Concept: "Bell curve chart showing distribution of contractor booking conversion rates with one outlier highlighted"
> - Data: "Industry median: 2.5%. Top quartile: 8.1%. Reeis post-the workspace: 13.4%."
> - Generator: gemini
> - Draft prompt: "Bold sans-serif bell curve chart on a clean off-white background. the workspace brand palette per .claude/skills/get-brand-kit/sub-skills/color-palette.md..."

The sub-skill runs the loop and returns either the validated prompt or a pivot recommendation.
