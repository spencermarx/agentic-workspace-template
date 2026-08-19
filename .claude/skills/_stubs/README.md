<!-- workspace:no-mutate -->
# Stubs

Skills that are shipped but not wired. Each points at a service this workspace
has no credentials for, or at infrastructure that does not exist yet.

They are flat `.md` files rather than `<name>/SKILL.md` directories, so Claude
Code does not register them. **A stub costs zero context.** That is the whole
reason they live here instead of being deleted: nothing is lost, and nothing
fires half-configured.

An unwired skill left in `.claude/skills/` is worse than no skill at all. It has
a live description, so it wins triggers it cannot fulfil, and it fails in the
middle of a task rather than at the start.

## Promoting one

1. Read its **Wiring** section and supply everything listed: credentials in
   `.credentials/<service>/tokens.env`, identifiers, any MCP server.
2. `mkdir .claude/skills/<name>` and move the file to
   `.claude/skills/<name>/SKILL.md`.
3. Delete the stub banner at the top.
4. Replace every `__REPLACE_ME__` with a real value.

## Demoting one

The reverse, and it is a legitimate move. If a skill's service goes away, move it
back here rather than deleting it. The procedure it encodes is usually still
correct; only the wiring is gone.
