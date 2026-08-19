# Agentic Workspace Template

A GitHub template for knowledge workspaces that two interfaces share: **Obsidian is the human GUI, Claude Code is the agentic GUI**, both operating over the same Markdown files in one git repo.

Clone it, answer some questions, and you get a vault with a nested `CLAUDE.md` hierarchy, a standards layer that routes rules to the files they govern, a working Obsidian plugin set, and a skill library.

## Use it

1. **Use this template** on GitHub to create your repo, then clone it.
2. `./workspace bootstrap` -- a conversation, not a form. It interviews you, generates the folder tree and the `CLAUDE.md` hierarchy, and wires Obsidian.
3. `./workspace obsidian-setup` -- writes per-machine plugin config. Quit Obsidian first.
4. Open the repo root in Obsidian as a vault, trust the plugins when prompted, and start at `Home.md`.

Nothing to install. The engine is Python 3 standard library, and `/usr/bin/python3` ships with the same Xcode Command Line Tools that provide `git`.

## What is in here

| Path | What it is |
|---|---|
| `Standards/` | Every convention, stated exactly once. The single source of truth. |
| `.claude/rules/` | Pointers that route a standard to the files it governs, loaded on demand by path glob. |
| `.claude/skills/` | The skill library. `_stubs/` holds skills that need wiring before they work. |
| `.workspace/` | The engine, the templates it renders from, the plan grammar, and one worked example plan. Template-owned. |
| `Obsidian/` | Vault mechanics: guides and templates. Not content. |
| `Decisions/` | Architecture decision records. |

## The one rule that holds it together

`.workspace/`, `.claude/`, `.obsidian/`, `Obsidian/Templates/`, and `.credentials/` are **template-owned** and contain no workspace content. Everything else is **workspace-owned** and contains no template logic. No file is both.

That boundary is what lets `./workspace upgrade` replace harness files without touching your notes.

## Commands

```
./workspace bootstrap         turn this template into a workspace
./workspace add               scaffold one new client, venture, or area
./workspace obsidian-setup    write per-machine plugin config
./workspace doctor            report drift from the template and from vendored upstreams
./workspace upgrade --to REF  pull a newer template in
```

## License

MIT. Vendored third-party skills keep their own provenance and copyright; see `THIRD-PARTY-NOTICES.md`.
