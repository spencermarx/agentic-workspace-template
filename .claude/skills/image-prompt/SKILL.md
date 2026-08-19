---
name: image-prompt
description: >-
  Build and validate an AI image-generation prompt before sending it to any model. Runs a
  build-and-review loop with three parallel critics, and pulls brand values from `get-
  brand-kit` rather than inlining them. Use BEFORE calling any image model. Do NOT use to
  composite text or a logo onto a finished image (use `image-overlay`) or to strip
  metadata (use `image-clean`).
---
<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/image-prompt/SKILL.md @ 496d37273aca); adapted for this repo (brand references routed through get-brand-kit rather than inlined; scripts colocated). See [vendoring provenance](../../../Standards/harness-standards.md#vendoring-provenance). -->


# Image Prompt Build + Review Skill

A primitive skill that validates image generation prompts through a structured build + review loop with three focused critic sub-agents. Designed to be invoked by any workflow that produces AI-generated images so the build+review discipline lives in one place instead of being duplicated across docs.

This skill does NOT call any image generation API. It produces a finalized prompt string. The caller is responsible for then passing that string to the appropriate generator (`openai/sub-skills/image-generation.md` or `gemini/sub-skills/image-generation.md`).

## When to Use

- **Before any image generation API call** for marketing content (social posts, blog posts, ad creatives, landing page assets)
- When a draft prompt exists but hasn't been critically reviewed
- When iterating on a concept that has failed previous generations and needs structured critique
- When a workflow says "draft a prompt, then generate" - insert this skill between the two steps

## When NOT to Use

- For generating the image itself. Use the `openai` or `gemini` skills for that.
- For text overlay decisions on an existing image. Use the `image-overlay` skill.
- For metadata stripping. Use the `image-clean` skill.

## Sub-Skills (Load the One Matching Your Scenario)

The build + review loop is the same shape across scenarios, but the critic emphasis, prompt construction conventions, and downstream processing differ. Load the sub-skill that matches what you're producing.

| Scenario | Sub-Skill | When to load |
|---|---|---|
| Organic social post (LinkedIn, Facebook) - editorial photography that will be overlaid with text + the workspace logo | [`sub-skills/social.md`](sub-skills/social.md) | Producing an image for an Unfair Advantages, Builder's Journal, or Product Announcement social post |
| Blog post image (hero or inline) - editorial photography that will be image-cleaned (no overlay) | [`sub-skills/blog.md`](sub-skills/blog.md) | Producing a blog hero or any inline blog image |
| Infographic / data visualization - typographic chart or framework that will get a logo-only stamp (no text bridge) | [`sub-skills/infographic.md`](sub-skills/infographic.md) | Producing an image for a Proof Post, stat-first hook, or any infographic-style visual |

Each sub-skill is self-contained: it includes the full 5-step loop, the three critic mandates scoped to its scenario, and the input/output contract for that scenario. You only need to load one sub-skill per image you're prompting.

## Why Three Critics, Not One

A single generalist reviewer tends to give vague, balanced feedback ("the prompt is good but could be more specific"). Three focused critics each operating on one criterion produce sharper, more actionable feedback. Each critic is forced to commit on their lane and ignore everything else. This catches issues that a generalist would smooth over.

The three criteria are also genuinely independent:
- **Visual interest** has nothing to do with whether the image relates to the post.
- **Message relevance** has nothing to do with whether the image is renderable.
- **Physical accuracy** has nothing to do with whether the scene is interesting.

Mixing them produces tradeoffs and softening. Separating them produces clear PASS/REVISE signals on each axis.

## Why Cap at 3 Iterations

A prompt that fails the same critic three times is not a writing problem. It's a concept problem. The prompt language can be polished indefinitely without fixing a structural issue (e.g., asking the model to render a scale violation it has no training data for, or asking for a connection to a post that the chosen visual fundamentally cannot make). Capping at 3 forces the caller to recognize structural failure and pivot the concept rather than wasting tokens on more rewrites.

## Related Skills

| Skill | Relationship |
|:------|:------------|
| `openai` (image-generation sub-skill) | The generator the caller invokes after this skill returns a validated prompt (editorial path) |
| `gemini` (image-generation sub-skill) | The generator the caller invokes after this skill returns a validated prompt (infographic path) |
| `image-overlay` | Used after the generated image is produced (social), to add text + the workspace logo |
| `image-clean` | Used after the generated image is produced (blog), to strip metadata |
| `content-sprint` | A primary caller - invokes this skill during Phase 2 (social drafting) and Phase 3 (blog drafting) for every image |

## Reference

The full prompt construction guide (Section 8c) and concept development process (Sections 8, 8a, 8b) live in `the workspace Company Files/Marketing/Resources/Image Generation Guide.md`. This skill (and its sub-skills) is the operational implementation of the build+review discipline that the Guide describes.
