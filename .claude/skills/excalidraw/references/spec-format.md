# Spec format

The input to `scripts/build.mjs`. A single JSON object with four optional arrays: `nodes`, `edges`, `texts`, `regions`, plus top-level options. Coordinates are absolute canvas pixels; you place everything (there is no auto-layout).

## Top level

| Field | Type | Default | Notes |
|---|---|---|---|
| `title` | string | — | Only used to seed deterministic ids. Put the visible title in `texts`. |
| `font` | `"hand"` \| `"normal"` \| `"code"` | `"hand"` | Excalidraw fontFamily: hand=Excalifont (5), normal=Helvetica (2), code=Cascadia (3). |
| `background` | hex string | `"#ffffff"` | Canvas background color. |
| `nodes` | array | `[]` | Boxes that edges can bind to. |
| `edges` | array | `[]` | Bound arrows between nodes. |
| `texts` | array | `[]` | Free-floating text (titles, annotations). |
| `regions` | array | `[]` | Background zones with a label (swimlanes, tiers). Drawn behind nodes. |

## `nodes[]`

A shape with an optional bound label. Edges reference nodes by `id`.

| Field | Type | Default | Notes |
|---|---|---|---|
| `id` | string | **required** | Unique. Referenced by `edges`. |
| `shape` | `"rectangle"` \| `"ellipse"` \| `"diamond"` | `"rectangle"` | |
| `x`, `y` | number | **required** | Top-left corner. |
| `w`, `h` | number | **required** | Width and height. |
| `label` | string | — | Bound, centered by default. Use `\n` for line breaks. |
| `align` | `"left"` \| `"center"` \| `"right"` | `"center"` | Label horizontal align (use `left` for ERD/class attribute lists). |
| `valign` | `"top"` \| `"middle"` \| `"bottom"` | `"middle"` | Label vertical align (use `top` for attribute lists). |
| `fontSize` | number | `16` | |
| `bg` | hex | `"transparent"` | Fill color. Label color auto-contrasts against it. |
| `stroke` | hex | `"#1e1e1e"` | Border color. |
| `labelColor` | hex | auto | Overrides auto-contrast. |
| `strokeStyle` | `"solid"` \| `"dashed"` \| `"dotted"` | `"solid"` | Dashed = external/optional by convention. |
| `fillStyle` | `"solid"` \| `"hachure"` \| `"cross-hatch"` | `"solid"` | |
| `roughness` | `0` \| `1` \| `2` | `1` | 0 = clean lines, 2 = very sketchy. |
| `group` | string | — | Shared groupId; elements move/select together in the editor. |

## `edges[]`

Becomes a real Excalidraw arrow bound to both endpoints (drag-follows in the editor). Geometry is computed by clipping to each box edge.

| Field | Type | Default | Notes |
|---|---|---|---|
| `from`, `to` | node id | **required** | Must exist in `nodes`. |
| `label` | string | — | Bound to the arrow at its midpoint (white background for legibility). |
| `style` | `"solid"` \| `"dashed"` \| `"dotted"` | `"solid"` | |
| `end` | arrowhead \| `null` | `"arrow"` | `"arrow"`, `"triangle"`, `"dot"`, `"bar"`, or `null` for none (ERD relationship lines). |
| `start` | arrowhead \| `null` | `null` | Set for bidirectional edges. |
| `stroke` | hex | `"#1e1e1e"` | |
| `curved` | boolean | `true` | `false` = straight segments. |
| `fontSize` | number | `14` | Label size. |

## `texts[]`

Free-floating text. Use for titles, notes, and annotations that are not bound to a shape.

| Field | Type | Default | Notes |
|---|---|---|---|
| `text` | string | **required** | Use `\n` for line breaks. |
| `x`, `y` | number | **required** | Top-left. |
| `fontSize` | number | `20` | Titles 28–36, headers 22–26, annotations 12–16. |
| `align` | `"left"` \| `"center"` \| `"right"` | `"left"` | |
| `w` | number | auto | Fixed width (helps center a title over a region). |
| `stroke` | hex | `"#1e1e1e"` | |

## `regions[]`

A background rectangle with an optional corner label. Drawn first (behind nodes). Use for swimlanes, architecture tiers, or grouping zones. Regions are decorative — edges cannot bind to them, so put the flow in `nodes` on top.

| Field | Type | Default | Notes |
|---|---|---|---|
| `x`, `y`, `w`, `h` | number | **required** | |
| `label` | string | — | Zone name. |
| `labelAlign` | `"top-left"` \| `"top-center"` | `"top-left"` | |
| `bg` | hex | `"#f1f3f5"` | Keep light; nodes sit on top. |
| `stroke` | hex | `"#adb5bd"` | |
| `fontSize` | number | `20` | |
| `labelColor` | hex | `"#495057"` | |

## A reasonable palette

Excalidraw's built-in accents read well and are conventional:

| Use | Hex |
|---|---|
| Primary / process | `#a5d8ff` (blue) |
| Success / positive path | `#b2f2bb` (green) |
| Decision / attention | `#ffd43b` (yellow) |
| Alert / negative path | `#ffc9c9` (red) |
| Secondary / accent | `#d0bfff` (violet), `#ffd8a8` (orange) |
| Zone backgrounds | `#e7f5ff`, `#fff9db`, `#f3f0ff`, `#f1f3f5` (light tints) |

## Text sizing note

The compiler estimates text at ~0.5em per character and 1.25 line height. It does not measure real font metrics (that needs a browser). Consequence: give boxes generous width, and prefer explicit `\n` line breaks over relying on wrapping. If a label looks tight in Obsidian, widen the box or break the line.
