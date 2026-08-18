---
name: excalidraw
description: >-
  Generate clean, editable Excalidraw diagrams for the vault from a small declarative spec
  of nodes, edges, and regions. Produces a native Obsidian .excalidraw.md with real bound
  arrows and bound text labels, compiled by a dependency-free script. Covers flowcharts,
  sequence diagrams, swimlanes, ERDs, architecture, and mindmaps. Use whenever a diagram
  belongs in a document or note.
---

# Excalidraw Diagram Skill

Produces an editable Obsidian Excalidraw diagram (`.excalidraw.md`) from a small JSON spec you author. You describe the diagram as nodes, edges, texts, and regions; a dependency-free compiler wires up the real Excalidraw elements — bound arrows, bound labels, auto-contrast text — and writes the Obsidian file.

This skill is deliberately small. It has one script, one spec format, and a set of per-type starter templates. There is no build toolchain, no headless renderer, and no browser. The tradeoff is that you verify the result by opening it in Obsidian, not by an automated render.

## When to use

- A doc, PRD, or note in the vault needs a diagram (flowchart, sequence, swimlane, ERD, class, architecture, data-flow, mindmap).
- You want the artifact to stay **editable** in Obsidian's Excalidraw plugin, with arrows that stay attached to their boxes.

## When NOT to use

- For Mermaid diagrams meant to render inline in Markdown (the Example Co PRD uses Mermaid for its canonical flows). Generate Mermaid directly there.
- For quantitative charts (bar / line / area). Excalidraw is for relational, hand-drawn diagrams.
- For marketing / editorial imagery. Use the image tooling instead.

## The output format

The compiler writes an **Obsidian Excalidraw plugin file** (`<name>.excalidraw.md`): YAML frontmatter (`excalidraw-plugin: parsed`), a `## Text Elements` index, and a `## Drawing` block holding the scene as **uncompressed JSON** (so it is diffable in git). Obsidian's plugin reads this directly and normalizes it (regenerates fractional indices and defaults) on open. Open it in the vault and switch to Excalidraw view to edit.

Pass `--plain` to also emit a standalone `.excalidraw` (for excalidraw.com or the VS Code extension).

## Workflow

1. **Pick the diagram type** and read its section in [`references/diagram-types.md`](references/diagram-types.md) for the shape conventions and layout guidance.
2. **Start from a template.** Copy the matching spec from [`references/examples/`](references/examples/) and adapt it. Author real content inline — labels, edge text, attributes are your job, not the script's.
3. **Lay it out with explicit coordinates.** You set `x`/`y`/`w`/`h`. The compiler does not auto-layout (that was the old skill's finicky part). The templates use sane grids and spacings; follow them. See [`references/spec-format.md`](references/spec-format.md) for every field.
4. **Compile:**
   ```bash
   node ${CLAUDE_SKILL_DIR}/scripts/build.mjs --spec /path/to/spec.json --out "/path/to/Diagram Name.excalidraw.md"
   ```
   The script fails fast on spec errors (unknown edge endpoints, duplicate ids, dangling bindings) and prints an element/node/edge summary on success.
5. **Self-review** against the checklist below and the per-type checklist in `references/diagram-types.md`.
6. **Open in Obsidian** to confirm it looks right. This is the visual check; there is no automated render.

## The spec in one glance

```json
{
  "title": "Onboarding Flow",
  "font": "hand",
  "texts": [
    { "x": 480, "y": 40, "text": "Onboarding Flow", "fontSize": 28, "align": "center", "w": 300 }
  ],
  "nodes": [
    { "id": "start",  "shape": "ellipse",   "x": 500, "y": 120, "w": 200, "h": 80,  "label": "Visitor" },
    { "id": "signup", "shape": "rectangle", "x": 500, "y": 260, "w": 200, "h": 90,  "label": "Sign Up", "bg": "#a5d8ff" },
    { "id": "verify", "shape": "diamond",   "x": 480, "y": 410, "w": 240, "h": 140, "label": "Email\nVerified?", "bg": "#ffd43b" }
  ],
  "edges": [
    { "from": "start",  "to": "signup" },
    { "from": "signup", "to": "verify" },
    { "from": "verify", "to": "onboard", "label": "Yes" }
  ]
}
```

- **`nodes`** are boxes (`rectangle` / `ellipse` / `diamond`) with a bound label. Edges bind to node `id`s.
- **`edges`** become real bound arrows. Drag a node in Obsidian and its arrows follow. `label` becomes a bound label at the midpoint.
- **`texts`** are free-floating strings (titles, annotations).
- **`regions`** are background rectangles with a corner/edge label (swimlanes, zones, tiers).

Full field reference: [`references/spec-format.md`](references/spec-format.md).

## What the compiler guarantees (so you don't have to)

- **Bound arrows.** Every edge emits `startBinding`/`endBinding` and registers on each node's `boundElements`. Arrows stay attached when you move boxes.
- **Bound labels.** Node and edge labels become `text` elements with `containerId`, `fontFamily: 5` (Excalifont), centered and contained.
- **Auto-contrast labels.** A label on a filled shape gets black or white text chosen by the fill's luminance. No invisible dark-on-dark text.
- **Correct arrow geometry.** Endpoints are clipped to each box's edge with a small gap, so arrows touch borders cleanly.
- **Structural gates.** The build aborts on duplicate ids, edges to unknown nodes, or any dangling binding.
- **Deterministic ids/seeds.** Reruns of the same spec produce stable output for clean git diffs.

## Self-review checklist (before you ship)

- Every node the user described is present; nothing invented.
- Every edge points the right way; decision branches are labeled (Yes/No, etc.).
- No boxes overlap; arrows do not cross more than necessary.
- Labels fit their boxes. If a label is long, widen the box or add `\n` line breaks — the compiler sizes text at ~0.5em/char, so give generous width.
- Diamonds are decisions, ellipses are start/end or stores, rectangles are steps/entities. Type conventions per `references/diagram-types.md`.
- The file opened and rendered correctly in Obsidian.

## Layout guidance (no auto-layout — you place things)

The compiler places elements exactly where your coordinates say. Keep it clean with these spacings (the templates already use them):

- **Vertical flow:** 140–160px between row tops. **Horizontal flow:** 260–320px between column origins.
- **Box sizes:** rectangles 200x90 for a short phrase; diamonds need ~1.4x the width of their text; ellipses square-ish for start/end.
- **Swimlanes:** stack full-width `regions` ~170px tall; place each step inside its lane's y-band.
- **Grids (ERD/architecture):** 250–300px horizontal pitch, 180–260px vertical.

If a diagram is large or dense, it is usually clearer to split it into two diagrams than to cram one.

## References

- [`references/spec-format.md`](references/spec-format.md) — every spec field, with defaults.
- [`references/diagram-types.md`](references/diagram-types.md) — per-type conventions, shape semantics, and a review checklist for each of: flowchart, sequence, swimlane, ERD, class, architecture, data-flow, mindmap.
- [`references/examples/`](references/examples/) — a ready-to-adapt starter spec for each type. These double as a smoke test: `for f in references/examples/*.json; do node scripts/build.mjs --spec "$f" --out "/tmp/$(basename $f .json).excalidraw.md"; done`

## Provenance

Rebuilt lean in 2026 from two sources: this workspace's prior compiler-based Excalidraw skill (which contributed the bound-arrow geometry and auto-contrast logic) and the open-source `github/awesome-copilot` `excalidraw-diagram-generator` skill (which contributed the breadth of diagram-type conventions — ERD, sequence, class, swimlane). The heavy compiler, headless renderer, visual-audit passes, and three-critic loop were removed in favor of direct authoring, because the vault's actual need is a handful of small, editable diagrams in Obsidian format, not data-driven auto-laid-out maps.
