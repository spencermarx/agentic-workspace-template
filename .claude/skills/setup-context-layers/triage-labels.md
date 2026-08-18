# Triage Labels

<!-- Seed template — the written instance for this repo lives at .workspace/config/triage-labels.md. When fixing either copy, mirror it in the other; a setup re-run merges, never blind-overwrites. -->

The skills speak in terms of canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

## State roles

| Canonical role    | Label in our tracker | Meaning                                  |
| ----------------- | -------------------- | ---------------------------------------- |
| `needs-triage`    | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`      | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent` | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human` | `ready-for-human`    | Requires human implementation            |
| `wontfix`         | `wontfix`            | Rejected — label genuine rejections only |

## Category roles

| Canonical role | Label in our tracker | Meaning                    |
| -------------- | -------------------- | -------------------------- |
| `bug`          | `bug`                | Something isn't working    |
| `enhancement`  | `enhancement`        | New feature or improvement |

If the tracker already types issues (e.g. `type: bug` / `type: feature`), map the category roles onto those existing labels instead of creating duplicates.

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from these tables. One carve-out (per the triage skill's outcome step): the `wontfix` label is applied to genuine rejections only — built/underway/deferred closures carry no state label, their close reason and comment holding the outcome.

Labels must exist on the tracker before a skill can apply them (`gh issue edit --add-label` fails on unknown labels) — create any missing ones: `gh label create <name> --description "..."`.

Edit the right-hand columns to match whatever vocabulary you actually use.
