> **STUB, not an active skill.** This file is a flat `.md` under `_stubs/`, so it
> is not registered and costs no context. To activate: supply the wiring below,
> move it to `.claude/skills/process-meeting/SKILL.md`, and delete this banner. See
> [README](README.md).

# process-meeting

Turn a meeting recording into a speaker-labeled transcript, a structured summary, and a strategic analysis.

## Wiring

Heavier than any other stub here, and machine-specific:

- Apple Silicon, for `mlx-whisper`.
- A Python environment with `pyannote` for diarization and `mlx-whisper` for transcription. This is roughly 1.3 GB of models and is why the source repository's harness was 1.4 GB.
- `.credentials/huggingface/tokens.env` with `HF_TOKEN`, and the pyannote model licenses accepted on Hugging Face.
- A recording source.

**The scripts are deliberately not vendored here.** A template must not carry a
gigabyte. Port them from the source repository when you promote this.

## What it does

Word-level merge of diarization and transcription, which is what makes speaker
attribution accurate rather than approximate. Produces vault-shaped output with a
human confirmation step for speaker names.

Its output lands in the note-taker's `Operators/<key>/Meetings/` and follows
`Workspace/Templates/Meeting Note.md`.
