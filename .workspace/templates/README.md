# Templates

The files the engine renders from. Template-owned: they contain tokens and
sentinels by design, which is why `.workspace/` is excluded from the mutate
surface.

| File | Rendered as |
|---|---|
| `root.md` | the workspace root `CLAUDE.md` |
| `router.md` | a `CLAUDE.md` for a folder whose children carry their own |
| `leaf.md` | a `CLAUDE.md` for an area that carries full context |
| `parking-lot.md` | `<Area> - Parking Lot.md` |
| `links.md` | an area's external-link manifest |
| `decision-record.md` | `<scope>/decisions/NNNN-<slug>.md` |

## Slots

Three grammars. All of them must be filled before the workspace is done.

| Grammar | Filled by |
|---|---|
| `{{UPPER_SNAKE}}` | the engine, from `workspace.json` and the plan node |
| `__REPLACE_ME__` | the agent's authoring pass |
| `<!-- AGENT: ... -->` | the agent, which acts on it and then deletes it |

`{{REL_TO_ROOT}}` and `{{REL_TO_PARENT}}` are computed per node. Never write
them by hand: a leaf four levels deep needs four levels of `..`, and getting it
wrong produces a link that reads as correct and resolves nowhere.

## Managed blocks

`<!-- workspace:NAME:start -->` and `<!-- workspace:NAME:end -->` fence content
the engine owns. `./hq render` replaces what is between the fences and
preserves everything outside them byte for byte. That is what makes a re-run a
merge rather than a clobber, and it is why the folder map cannot drift: no human
and no agent ever writes it.
