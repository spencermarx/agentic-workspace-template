---
name: image-clean
description: >
  Strip AI metadata (EXIF, C2PA provenance) from generated images by rendering
  them through Playwright. Produces a clean PNG with no embedded metadata.
  Use for blog images only. Organic social posts use the image-overlay skill instead.
---
<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/image-clean/SKILL.md @ 496d37273aca); adapted for this repo (script colocated under scripts/; de-branded). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Image Clean Skill

Strip AI-generation metadata from images by rendering them through a Playwright screenshot pipeline. The output is a "born clean" PNG with no EXIF data, no C2PA provenance markers, and no embedded generation metadata.

## When to Use

- **Blog images:** Every blog image (hero, social share, in-article) must be cleaned before publishing to Sanity CMS. Blog images do NOT get overlays or logos.
- **Any image that needs metadata stripped** without adding text or logos

## When NOT to Use

- **Organic social posts (LinkedIn, Facebook).** ALL social posts use the `image-overlay` skill instead, which adds professional text + the workspace logo and also strips metadata in the process.
- When the image is a **product screenshot** (already clean, no AI metadata).
- For **generating** the base AI image itself. Use the `openai` skill for that.

## Prerequisites

- Playwright available via npx (`npx playwright screenshot`)
- Python 3 with Pillow (`from PIL import Image`)
- Base image already generated and saved to the content's `images/` directory

## Procedure

### Step 1: Identify the image to clean

Read the content post file. Locate the generated image(s) in the `images/` subdirectory:
- Social posts: `images/post-image.png`
- Blog hero: `images/hero.png`
- Blog social share: `images/social-share.png`
- Blog in-article: `images/inline-{N}.png`

### Step 2: Run the clean script

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/clean.sh \
  --image "{path-to-images}/post-image.png" \
  --output "{path-to-images}/post-image-clean.png"
```

### Parameters

| Parameter | Required | Default | Description |
|:----------|:---------|:--------|:------------|
| `--image` | Yes | -- | Path to the AI-generated source image |
| `--output` | No | `{basename}-clean.png` next to source | Output path for the clean PNG |
| `--width` | No | Read from source image | Override width in pixels |
| `--height` | No | Read from source image | Override height in pixels |

### Step 3: Verify the output

Confirm the output file exists and has the expected dimensions. The clean image should be visually identical to the source but with all metadata stripped.

### Step 4: Use the clean image as the final asset

- For social posts: `post-image-clean.png` becomes the image uploaded to Buffer
- For blog posts: `hero-clean.png`, `social-share-clean.png`, etc. become the images uploaded to Sanity

## How It Works

The script:
1. Reads the source image dimensions via Pillow
2. Generates a minimal HTML page containing only the image at full size (no text, no logo, no overlay)
3. Uses Playwright to screenshot the HTML page at the exact image dimensions
4. Crops to exact size via Pillow if needed
5. Saves as a fresh PNG with no inherited metadata

## Examples

**Clean a the operator LinkedIn post image:**
```bash
bash ${CLAUDE_SKILL_DIR}/scripts/clean.sh \
  --image "Initiatives/Q2/Sprints/Sprint-01_.../Days/07/the operator-LinkedIn/images/post-image.png"
```

**Clean all blog images:**
```bash
for img in hero.png social-share.png inline-1.png; do
  bash ${CLAUDE_SKILL_DIR}/scripts/clean.sh \
    --image "images/$img" \
    --output "images/${img%.png}-clean.png"
done
```

## Related Skills

| Skill | Relationship |
|:------|:------------|
| `image-overlay` | Use instead of image-clean when text overlay or the workspace logo is needed |
| `openai` (image generation sub-skill) | Use to generate the base image before cleaning |
| `content-sprint` | Calls image-clean during Phase 2 (social drafting) and Phase 3 (blog drafting) |
