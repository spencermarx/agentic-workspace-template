# Templater setup

Templater is AGPL-3.0, so it is store-installed rather than vendored and its
directory is git-ignored. Two files are the exception: this one and
`data.json.example`, because without them Templater arrives unconfigured and
every template in `Workspace/Templates/` fails.

## What breaks without this

Templater ships with no template folder and no user-scripts folder. Left at its
defaults it opens an empty template picker, and `tp.user.operators` is
undefined, which throws on the first line of the Daily Note and Meeting Note
templates. Both settings are what `data.json.example` supplies.

`user_scripts_folder` points at `Workspace/Templates/scripts`, which is where
`./hq render` writes `operators.js`. That file is the reason no template
contains a person's name.

## Install

1. Obsidian, Settings, Community plugins, Browse, install and enable
   **Templater**.
2. Run `./hq obsidian-setup` from the repo root. It writes `data.json`
   from `data.json.example` beside it. A `data.json` that already exists is left
   alone.
3. Reload Obsidian. Command palette, "Templater: Open insert template modal",
   should now list the templates.

## The settings this file cannot carry

Templater keeps three settings in the vault's local storage rather than in
`data.json`, deliberately, because each one lets a file execute code and that is
a decision a machine makes rather than inherits from a clone. None of them can
travel in `data.json.example`, and none is needed for the templates here to
work.

| Setting | Leave off unless |
|---|---|
| Trigger Templater on new file creation | you want folder or regex templates to fire automatically |
| Enable startup templates | you want a template to run when the vault opens |
| Enable system commands | you want templates to shell out |

## Verified against

Templater 2.25.0. The key names above are its own `DEFAULT_SETTINGS`, read out
of the built `main.js`, not inferred: `data_version`, `templates_folder`,
`user_scripts_folder`. Note that `trigger_on_file_creation` is **not** among
them; on `data_version: 2` Templater deletes that key from `data.json` on load
and reads the local-storage copy instead.
