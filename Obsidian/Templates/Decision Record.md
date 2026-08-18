<%*
// Offer the decision registers that already exist, rather than assuming one.
const dirs = app.vault.getAllLoadedFiles()
  .filter(f => f.children && f.path.endsWith("/decisions"))
  .map(f => f.path);
const choice = await tp.system.suggester(
  [...dirs, "New register (enter a scope path)"],
  [...dirs, "__new__"], false, "Which scope owns this decision?");
let dir = choice;
if (choice === "__new__") {
  const scope = await tp.system.prompt("Scope folder path, or . for workspace-wide");
  dir = (scope === "." ? "" : scope + "/") + "decisions";
}
const title = await tp.system.prompt("Decision title, stated as a claim");
const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const existing = app.vault.getFiles().filter(f => f.path.startsWith(dir + "/")).length;
const num = String(existing + 1).padStart(4, "0");
const scopeSlug = dir.replace(/\/decisions$/, "").toLowerCase() || "none";
await tp.file.move(`${dir}/${num}-${slug}`);
-%>
---
type: decision
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
date: <% tp.date.now("YYYY-MM-DD") %>
scope: <% scopeSlug %>
authors: []
tags:
  - type/decision
  - status/draft
  - scope/<% scopeSlug %>
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
