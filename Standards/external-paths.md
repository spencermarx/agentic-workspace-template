# External paths

This vault is a knowledge layer. Code, binaries, and legal originals live
outside it and are referenced by relative path, never copied in.

## The registry

Named anchors, with paths relative to the vault root so the whole tree stays
movable. Bootstrap fills this table from the interview; `workspace.json` holds
the machine-readable copy under `externalRoots`.

| Anchor | Path | Holds | The vault may |
|---|---|---|---|
| (none yet) | | | |

## The rule

Never copy an external artifact into the vault.

If you need its content, write a summary note that links to it and records the
date you read it. If text genuinely must be quoted at length, the note becomes a
mirror: `canonical: false` with `canonical_source` set to the external path. See
`canonical-and-mirrors.md`.

## How the boundary is enforced

Three layers, so absorption fails loudly rather than depending on discipline.

1. **This registry**, so an agent knows what exists outside and what it may do
   with each thing.
2. **`links.md` in any leaf with external dependencies**, a small manifest so an
   agent does not have to guess which of many repositories matters here.
3. **`.gitignore`**, which refuses to stage `*.pdf`, `*.docx`, `*.xlsx`,
   `*.pptx`, and `*.sketch` anywhere in the vault. Copying a signed agreement in
   does not produce a quiet multi-megabyte commit. It produces an error.

## Link syntax

Markdown with angle brackets, so the link resolves outside Obsidian too:

```markdown
The signed agreement is [the Master Agreement](<../Legal/Master Agreement.pdf>)
(read 2026-08-18).
```
