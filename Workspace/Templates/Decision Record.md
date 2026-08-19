<%*
// Offer the decision registers that already exist, rather than assuming one.
// Matched on the folder's own name so the workspace-level `Decisions/` is
// offered alongside the lowercase `decisions/` an area scaffold creates.
const dirs = app.vault.getAllLoadedFiles()
  .filter(f => f.children && f.path.split("/").pop().toLowerCase() === "decisions")
  .map(f => f.path)
  .sort();
const choice = await tp.system.suggester(
  [...dirs, "New register (enter a scope path)"],
  [...dirs, "__new__"], false, "Which scope owns this decision?");
let dir = choice;
if (choice === "__new__") {
  const scope = await tp.system.prompt("Scope folder path, or . for workspace-wide");
  dir = (!scope || scope === ".") ? "Decisions" : scope + "/decisions";
}
const title = await tp.system.prompt("Decision title, stated as a claim");
const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
// Highest number already used, not a file count: a register holds a README and
// may have had a record moved out of it, and both make a count skip a number.
const used = app.vault.getFiles()
  .filter(f => f.parent && f.parent.path === dir && /^\d{4}-/.test(f.name))
  .map(f => parseInt(f.name.slice(0, 4), 10));
const num = String((used.length ? Math.max(...used) : 0) + 1).padStart(4, "0");
// Strips the register segment whether or not a scope precedes it, so a
// workspace-level record gets `none` rather than `decisions`.
const scopeSlug = dir.replace(/(^|\/)decisions$/i, "").toLowerCase() || "none";
const d = tp.date.now("YYYY-MM-DD");
await tp.file.move(`${dir}/${num}-${slug}`);
-%>
---
type: decision
status: draft
created: <% d %>
date: <% d %>
scope: <% scopeSlug %>
---

# <% num %> - <% title %>

## Context

Why now? What deadline, constraint, or trade-off forced this? A reader should
feel the pressure before they see the answer.

| Factor | Detail |
|---|---|
| Trigger | |
| Constraint | |
| Goal | |

## Decision

One sentence, then the specifics. What does this mean concretely, and how would
you verify it held?

## Alternatives considered

The section that earns the document. If you cannot name a real alternative, you
have described the only available path rather than made a decision.

### Option A: name
- **Approach:**
- **Rejected because:**

### Option B: name
- **Approach:**
- **Rejected because:**

## Consequences

**Makes easier:**

**Makes harder:**

**Explicitly deferred:**
