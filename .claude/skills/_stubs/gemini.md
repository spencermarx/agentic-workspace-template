> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/gemini/SKILL.md`, delete this banner, and run
> `./workspace validate`. See [README](README.md).

# gemini

Call the Google Gemini API for text and image generation.

## Wiring

- `.credentials/gemini/tokens.env` with `GEMINI_API_KEY`.
- Uses the REST API over `curl`. No SDK.

## What it does

Its image-generation sub-skill reaches into `get-brand-kit` for brand values.
Promote `get-brand-kit` alongside it, or the generated images will carry no brand
at all, which is the failure mode the brand kit exists to prevent.
