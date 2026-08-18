---
name: openai
description: >
  Use when you need to call the OpenAI API for any purpose: generating text
  (chat completions), creating embeddings, transcribing audio, generating
  images, or making any other adhoc OpenAI API call. For image generation
  specifically, load sub-skills/image-generation.md for the full procedure.
  Uses the OpenAI REST API via curl — no SDK required.
---
<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/openai/SKILL.md @ 496d37273aca); adapted for this repo (no changes beyond this marker; the skill carried no brand references). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# OpenAI API

Call the OpenAI API for text generation, embeddings, image creation, audio
transcription, and other capabilities. All operations use `curl` against the
REST API — no extra dependencies beyond what macOS ships with.

## Authentication

Credentials are stored in `.credentials/openai/tokens.env` (gitignored).

```bash
source .credentials/openai/tokens.env
# exports: OPENAI_API_KEY (and optionally OPENAI_ORG_ID, OPENAI_PROJECT_ID)
```

### Auth priority order

1. `OPENAI_API_KEY` env var (if already set in shell)
2. `.credentials/openai/tokens.env` — source this file if env var is not set

### Setting up credentials (first time)

```bash
cp .credentials/openai/tokens.env.example .credentials/openai/tokens.env
# Fill in OPENAI_API_KEY, then:
source .credentials/openai/tokens.env
```

### Verify auth

```bash
source .credentials/openai/tokens.env
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print('OK —', len(d['data']), 'models')"
```

### When credentials are missing

If `OPENAI_API_KEY` is not set and `.credentials/openai/tokens.env` does not exist:

1. PATCH the issue to `blocked`
2. Post a comment:
   > Blocked: OpenAI credentials are missing. Please copy `.credentials/openai/tokens.env.example`
   > to `.credentials/openai/tokens.env`, fill in `OPENAI_API_KEY`, then re-assign this task.

---

## Sub-Skills (Domain-Specific Guides)

For specific capabilities, load the relevant sub-skill for exact payloads and gotchas.

| Domain | Sub-Skill | When to load |
|---|---|---|
| Image generation | [`sub-skills/image-generation.md`](sub-skills/image-generation.md) | Generating or editing images with OpenAI |

---

## Routing Guide

| Task | Use |
|---|---|
| Generate an image | Load `sub-skills/image-generation.md` |
| Generate or summarize text | Chat completions (below) |
| Classify or extract structured data from text | Chat completions with JSON mode (below) |
| Create vector embeddings | Embeddings (below) |
| Transcribe audio | Audio transcription (below) |

---

## Chat Completions

### Basic text generation

```bash
source .credentials/openai/tokens.env
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Summarize the key benefits of TypeScript in 3 bullets."}
    ]
  }' | python3 -c "import json,sys; r=json.load(sys.stdin); print(r['choices'][0]['message']['content'])"
```

### JSON mode (structured output)

```bash
source .credentials/openai/tokens.env
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "response_format": {"type": "json_object"},
    "messages": [
      {"role": "system", "content": "Return JSON only."},
      {"role": "user", "content": "List 3 programming languages with their main use cases as JSON."}
    ]
  }' | python3 -c "import json,sys; r=json.load(sys.stdin); print(r['choices'][0]['message']['content'])"
```

### Model selection

| Model | Best for |
|---|---|
| `gpt-4o` | Complex reasoning, multi-step tasks, vision |
| `gpt-4o-mini` | Fast, cost-effective tasks |
| `o1` | Advanced reasoning with chain-of-thought |
| `o3-mini` | Coding, math, science — fast reasoning |

---

## Embeddings

Generate vector embeddings for semantic search, clustering, or similarity:

```bash
source .credentials/openai/tokens.env
curl -s https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-3-large",
    "input": "The quick brown fox jumps over the lazy dog"
  }' | python3 -c "
import json, sys
r = json.load(sys.stdin)
emb = r['data'][0]['embedding']
print(f'Vector length: {len(emb)}, first 5 values: {emb[:5]}')
"
```

**Model options:**
- `text-embedding-3-large` — highest quality (3072 dims, reducible)
- `text-embedding-3-small` — fast and cost-effective (1536 dims)

---

## Audio Transcription (Whisper)

Transcribe an audio file to text:

```bash
source .credentials/openai/tokens.env
curl -s https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F file="@/path/to/audio.mp3" \
  -F model="whisper-1" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['text'])"
```

**Supported formats:** mp3, mp4, mpeg, mpga, m4a, wav, webm (max 25 MB).

---

## Error Handling

All OpenAI API errors return a non-2xx status with a JSON body:

```json
{
  "error": {
    "message": "...",
    "type": "invalid_request_error",
    "code": "..."
  }
}
```

| HTTP status | Meaning | Fix |
|---|---|---|
| 401 | Invalid or missing API key | Check `OPENAI_API_KEY` |
| 429 | Rate limit or quota exceeded | Wait and retry; check billing at platform.openai.com/usage |
| 400 | Bad request (invalid parameters) | Check payload shape and model name |
| 500 | OpenAI server error | Retry after a short wait |

Capture the full error for debugging:

```bash
curl -s -w "\nHTTP %{http_code}" https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "hi"}]}'
```

---

## Reference

- [OpenAI API docs](https://platform.openai.com/docs/api-reference)
- [Models overview](https://platform.openai.com/docs/models)
- [Usage dashboard](https://platform.openai.com/usage)
- [Rate limits](https://platform.openai.com/docs/guides/rate-limits)
