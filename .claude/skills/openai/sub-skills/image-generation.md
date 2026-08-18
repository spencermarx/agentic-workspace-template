# Image Generation Sub-Skill

Generate and edit images using OpenAI's image models.

> **Source of truth.** This file is the single source of truth for which OpenAI image model to use and which sizes are supported. Other docs (Image Generation Guide, content-sprint skill, drafting sub-skills) must reference this file rather than hardcoding a specific model name or size. When OpenAI releases a new image model, update this file only.

## Current Default

| Setting | Value |
|---|---|
| **Default model** | `gpt-image-1.5` |
| **Default landscape size** | `1536x1024` |
| **Default square size** | `1024x1024` |
| **URL-output fallback** | `dall-e-3` (only when base64 handling is undesirable) |

Use `gpt-image-1.5` (highest quality, best instruction-following) unless you have a specific reason to fall back to `dall-e-3`.

## Prerequisites

- OpenAI credentials loaded: `source .credentials/openai/tokens.env`
- For saving images: `base64` (pre-installed on macOS), standard shell tools

---

## Model Selection

| Model | Quality | Output format | Best for |
|---|---|---|---|
| `gpt-image-1.5` | Highest | Base64 (b64_json) | Complex scenes, fine detail, instruction accuracy |
| `dall-e-3` | High | URL or base64 | Quick generation, URL-only workflows |
| `dall-e-2` | Standard | URL or base64 | Simple images, inpainting/editing |

**Default to `gpt-image-1.5`** for all new image generation tasks unless the task
specifically requires URL output or cost is a concern.

---

## Generate an Image

### With gpt-image-1.5 (recommended)

`gpt-image-1.5` always returns base64-encoded PNG. Save it to a file:

```bash
source .credentials/openai/tokens.env

OUTPUT_FILE="output.png"
PROMPT="A photorealistic aerial view of San Francisco at golden hour, detailed city streets"

curl -s https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"gpt-image-1.5\",
    \"prompt\": \"$PROMPT\",
    \"n\": 1,
    \"size\": \"1024x1024\"
  }" | python3 -c "
import json, sys, base64
r = json.load(sys.stdin)
b64 = r['data'][0]['b64_json']
with open('$OUTPUT_FILE', 'wb') as f:
    f.write(base64.b64decode(b64))
print('Saved to $OUTPUT_FILE')
"
```

### With dall-e-3 (URL output)

```bash
source .credentials/openai/tokens.env

curl -s https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A minimalist logo for a tech startup, clean geometric shapes, blue and white",
    "n": 1,
    "size": "1024x1024",
    "quality": "hd",
    "response_format": "url"
  }' | python3 -c "
import json, sys
r = json.load(sys.stdin)
print(r['data'][0]['url'])
print('Revised prompt:', r['data'][0].get('revised_prompt', '(none)'))
"
```

> **Note:** dall-e-3 URLs expire after ~1 hour. Download the image promptly if
> you need to persist it.

---

## Size Options

| Size | Aspect | Available on |
|---|---|---|
| `1024x1024` | Square | gpt-image-1.5, dall-e-3, dall-e-2 |
| `1792x1024` | Landscape | gpt-image-1.5, dall-e-3 |
| `1024x1792` | Portrait | gpt-image-1.5, dall-e-3 |
| `512x512` | Square | dall-e-2 only |
| `256x256` | Square | dall-e-2 only |

---

## Quality Options (dall-e-3 only)

| Quality | Description |
|---|---|
| `standard` | Default — faster, lower cost |
| `hd` | Higher detail and consistency |

`gpt-image-1.5` does not use a `quality` parameter — it always renders at maximum quality.

---

## Generate Multiple Images

```bash
source .credentials/openai/tokens.env

# dall-e-2 supports up to 10 images per request
# gpt-image-1.5 and dall-e-3 support n=1 only
curl -s https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-2",
    "prompt": "A cute robot waving hello",
    "n": 3,
    "size": "512x512",
    "response_format": "url"
  }' | python3 -c "
import json, sys
r = json.load(sys.stdin)
for i, img in enumerate(r['data']):
    print(f'Image {i+1}: {img[\"url\"]}')
"
```

---

## Edit an Existing Image (Inpainting) — dall-e-2

Replace a masked region of an image with AI-generated content.
Both `image` and `mask` must be square PNG files of identical size (max 4 MB each).
The mask uses transparency (alpha=0) to mark the area to regenerate.

```bash
source .credentials/openai/tokens.env

curl -s https://api.openai.com/v1/images/edits \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F image="@original.png" \
  -F mask="@mask.png" \
  -F prompt="A sunlit garden with flowers" \
  -F n=1 \
  -F size="1024x1024" \
  -F model="dall-e-2" \
  | python3 -c "
import json, sys
r = json.load(sys.stdin)
print(r['data'][0]['url'])
"
```

---

## Create a Variation — dall-e-2

Generate variations of an existing image without a prompt:

```bash
source .credentials/openai/tokens.env

curl -s https://api.openai.com/v1/images/variations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F image="@original.png" \
  -F n=2 \
  -F size="1024x1024" \
  -F model="dall-e-2" \
  | python3 -c "
import json, sys
r = json.load(sys.stdin)
for i, img in enumerate(r['data']):
    print(f'Variation {i+1}: {img[\"url\"]}')
"
```

---

## Download a URL Image to File

After getting a URL from dall-e-3, save it locally:

```bash
IMAGE_URL="https://..."
curl -s -o output.png "$IMAGE_URL"
echo "Saved to output.png"
```

---

## Prompt Tips

- Be specific about subject, style, lighting, and composition.
- For logos/icons: "flat design", "vector style", "white background", "minimal"
- For photos: "photorealistic", specific lighting ("golden hour", "studio lighting"), camera details
- For illustrations: name the art style ("watercolor", "line art", "cel-shaded")
- dall-e-3 rewrites your prompt internally — check `revised_prompt` to see what it used.
- gpt-image-1.5 follows your prompt more literally; use precise language.

---

## Error Handling

| Error | Cause | Fix |
|---|---|---|
| `billing_hard_limit_reached` | Usage cap hit | Check billing at platform.openai.com/usage |
| `content_policy_violation` | Prompt rejected | Rewrite prompt to remove disallowed content |
| `invalid_size` | Size not supported by model | Check the size table above |
| `rate_limit_exceeded` | Too many requests | Wait 60s and retry |

---

## Reference

- [Images API reference](https://platform.openai.com/docs/api-reference/images)
- [gpt-image-1.5 guide](https://platform.openai.com/docs/guides/image-generation)
- [DALL·E pricing](https://openai.com/api/pricing)
