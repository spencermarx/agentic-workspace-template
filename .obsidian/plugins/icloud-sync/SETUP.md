<!-- workspace:no-mutate -->
# iCloud Sync

One-time setup, per machine.

> [!tip] `./workspace obsidian-setup` does the steps below for you.
> It refuses to run while Obsidian is open, substitutes your real paths, creates
> the destination, and rejects a path containing escaped spaces. Read on only if
> you want to know what it is doing, or to configure by hand.

The `icloud-sync` plugin pushes selected vault folders to your local iCloud Drive folder so they appear on the Obsidian mobile app via iCloud. The plugin's `data.json` is **gitignored** because it holds a per-machine absolute path (your iCloud Drive folder) plus per-machine sync state. Each machine configures it once.

## When to run this setup

- Fresh clone of the workspace.
- After `data.json` got corrupted or lost (rare).
- If your username changed (rare).

## Steps

1. **Make sure Obsidian is fully quit before editing data.json directly.** A running Obsidian will overwrite manual edits to this file from its in-memory state. `pkill -9 -f 'Obsidian.app/Contents/MacOS/Obsidian'` if needed.

2. **Copy the example:**
   ```bash
   cd ".obsidian/plugins/icloud-sync/"
   cp data.json.example data.json
   ```

3. **Edit `data.json`** and replace the `icloudBasePath` placeholder with your literal local path. On macOS this is almost always:
   ```
   /Users/<your-macOS-username>/Library/Mobile Documents/iCloud~md~obsidian/Documents/{{VAULT_NAME}}
   ```
   Use literal characters. **Do NOT escape spaces or tildes with backslashes.** The plugin passes this string directly to filesystem APIs; backslashes get treated as literal characters in the directory name and the plugin will silently sync to the wrong location (a directory called `Mobile\ Documents` next to the real `Mobile Documents`).

4. **Make sure that destination folder exists.** On a fresh macOS setup, iCloud Drive's Obsidian folder is created the first time you launch Obsidian on a phone with iCloud + Obsidian Mobile. Create the workspace subfolder manually if needed:
   ```bash
   mkdir -p "/Users/<your-username>/Library/Mobile Documents/iCloud~md~obsidian/Documents/{{VAULT_NAME}}"
   ```

5. **Open Obsidian.** The plugin loads, reads the marker on `Home.md` (`icloud-sync: true` with an exclude list for `.git/`, `.claude/`, `.obsidian/`, `.credentials/`, etc.), scans the vault, and starts syncing. With a 10-second interval, expect the destination folder to populate within a minute or two.

6. **Verify the sync is working:**
   ```bash
   find "/Users/<your-username>/Library/Mobile Documents/iCloud~md~obsidian/Documents/{{VAULT_NAME}}/" -type f | wc -l
   ```
   The number should climb from 0 toward the vault's content file count (~130 at the time of writing). It should match across founders since the marker config is in vault content (`Home.md` frontmatter).

7. **Check your phone.** Once iCloud Drive's `bird` daemon has uploaded the files to Apple's cloud (minutes to hours depending on the first sync), they appear in Obsidian Mobile.

## What's shared and what's local

| Lives in git (shared) | Lives only on your machine |
|---|---|
| `Home.md` `icloud-sync: true` marker + exclude list | `data.json` (your absolute `icloudBasePath` + your sync state) |
| The plugin itself (`main.js`, `manifest.json`, `styles.css`) | The iCloud Drive folder you sync to |
| `data.json.example` (this folder) | The plugin's per-machine `lastFullSync` timestamp |
| `SETUP.md` (this file) | Any local-only plugin debug toggles you flip |

The fact that the marker (`icloud-sync: true` + the exclude list) lives in `Home.md` means **both founders sync the same set of vault content** without coordinating, even though their destination paths differ.

## Two non-negotiable safety rules

1. **Never paste a shell-quoted path into the plugin's settings UI.** The plugin stores whatever you type verbatim — including backslash escapes. If you need to change the path, edit `data.json` directly with Obsidian closed.

2. **If anything looks wrong after a plugin update** (files moving into `.trash/`, destination going empty, sync log errors), **force-quit Obsidian immediately** (`pkill -9 -f 'Obsidian.app/Contents/MacOS/Obsidian'`) before the 10-second sync loop fires again. The plugin's `deleteStrategy: trash-on-delete` will mirror a destination-side deletion back to the source if state gets inconsistent. The full damage-and-recovery story is in this repo's git history if you need a precedent.

## Why this plugin is the exception to "track all plugin settings"

The repo's `.gitignore` deliberately tracks the rest of `.obsidian/plugins/*` (community plugins + their `data.json` files) so both founders run the same plugin set with the same config. The `icloud-sync` plugin is the only one whose `data.json` contains a per-machine absolute path — hence the explicit exception. If a future plugin gets installed that also stores machine-specific paths in its `data.json`, add it to the `.gitignore` the same way.
