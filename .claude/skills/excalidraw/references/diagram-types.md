# Diagram types

Conventions, shape semantics, layout, and a review checklist for each common type. All of these are expressed with the same four primitives (`nodes`, `edges`, `texts`, `regions`) — only the conventions differ. Each type has a ready starter in [`examples/`](examples/).

Shape semantics are shared across types: **rectangle** = step / entity / component; **diamond** = decision; **ellipse** = start/end terminal or data store. Honor these — a diamond that isn't a decision, or an ellipse that isn't a terminal/store, misleads the reader.

---

## Flowchart / decision tree — `examples/flowchart.json`

Process flows with sequential steps and conditional branches.

- Rectangles for steps, diamonds for decisions, ellipses for start/end.
- **Label every decision branch** (`Yes`/`No`, `Approve`/`Reject`) on the outbound edges, and make them mutually exclusive.
- Top-down (`vertical`) is the default; use left-right for a time axis.
- Give every path a terminal (end node) or a loop back into the flow. No dead ends.
- If there is a retry loop, draw the back-edge explicitly (dashed reads well) and make sure the loop has an exit.

Checklist: every diamond has ≥2 labeled outbound edges; every path terminates; no dangling nodes; loops have an exit; shapes match semantics.

---

## Sequence diagram — `examples/sequence.json`

Interactions between participants over time. Time flows top to bottom.

- **Participants** are a row of rectangles across the top (`nodes`, one per actor).
- **Lifelines** are long thin vertical `regions` (e.g. `w: 2`, tall) dropping from each participant, or a dashed thin rectangle. Keep them light gray.
- **Activation bars** are narrow rectangles (`w: ~14`) sitting on a lifeline for the span an actor is active.
- **Messages** are horizontal edges between activation bars (or between the small message-anchor nodes you place on each lifeline at each time step). Label every message with the call. Solid arrow = synchronous call; dashed (`style: "dashed"`) = async or return.
- Because edges bind to nodes, model each message endpoint as a small node on the lifeline at the right y (time) — see the example. Order messages by increasing y.

Checklist: participants across the top; time increases downward; each message labeled; sync vs async/return distinguished by arrow style; returns drawn after their triggering call.

---

## Swimlane (cross-functional flow) — `examples/swimlane.json`

A process where steps belong to different actors/roles.

- One full-width `region` per lane (actor), stacked vertically, each ~150–180px tall, with the actor name as the lane label.
- Place each step `node` inside its lane's y-band. Handoffs are edges that cross between lanes.
- Keep the left-to-right order of steps consistent with time; cross-lane edges show responsibility handoff.
- For this vault's Example Co work: remember the architectural invariant that Example Co never messages customers — a swimlane must not show a Example Co→customer arrow.

Checklist: every step sits fully inside one lane; lanes are labeled; handoffs cross lanes explicitly; step order reads as time; no step straddles two lanes ambiguously.

---

## ERD (entity-relationship) — `examples/erd.json`

Database entities and their relationships.

- Each **entity** is a rectangle `node` with a **left-aligned, top-aligned** multi-line label: the entity name on line 1, a divider line (`──────────`), then one attribute per line.
- Mark keys inline: `id  (PK)`, `customer_id  (FK)`. Keep alignment readable with two spaces before the marker.
- **Relationships** are edges. Use `"end": null` (no arrowhead) and put **cardinality** in the label: `1 : 1`, `1 : N`, `N : M`. Point from the "one" side to the "many" side, or label both ends.
- For an N:M relationship, add a **junction entity** (its own rectangle, often with a dashed border) between the two, with two `1 : N` edges.
- Lay entities on a grid with 280–320px horizontal pitch so relationship edges have room.

Checklist: every entity has a name + attributes with a divider; PKs and FKs marked; every relationship carries cardinality; N:M modeled via a junction entity; FKs correspond to a drawn relationship.

---

## UML class diagram — `examples/class.json`

Object-oriented structure.

- Each **class** is a rectangle `node` with a left/top-aligned label in three visual compartments separated by divider lines: **name** (line 1), **attributes** (with visibility markers `+` public, `-` private, `#` protected), then **methods** (`+ save(): void`). Approximate the compartments with `──────────` divider lines inside the single label.
- **Relationships** are edges with conventional ends (this skill draws the line + label; note the relationship type in the edge label since custom UML arrowheads aren't primitives):
  - Inheritance / implementation: label `extends` / `implements` (implementation dashed).
  - Association: plain solid edge.
  - Aggregation / composition: label `has` / `owns`; note diamond ownership in the label.
  - Dependency: dashed edge, label `uses`.
- Add multiplicity in the label where it matters (`1`, `0..1`, `1..*`, `*`).

Checklist: each class shows name/attributes/methods with visibility markers; relationships labeled with their UML type; inheritance direction points to the parent; multiplicity present where relevant.

---

## System architecture — `examples/architecture.json`

Components and their dependencies.

- Rectangles for services/apps; ellipses for stores (DB, cache, queue); diamonds for routers/load balancers.
- Group by tier using `regions` (edge / app / data) or `group` ids; layered systems read top-down.
- **Arrow direction = call direction** (caller → callee), not data flow. Label edges with the protocol/operation (`REST`, `gRPC`, `SQL`, `publishes`) when it varies.
- Distinguish **external/third-party** systems with a dashed stroke.

Checklist: dependency arrows point caller→callee; protocols labeled where they vary; tiers coherent; external systems visually distinct; no invented components.

---

## Data flow / pipeline — `examples/dataflow.json`

How data moves and transforms: source → transform → sink. Left-to-right.

- Ellipses for stores (sources/sinks: DB, queue, warehouse); rectangles for transforms/operations.
- **Label every edge with the operation** (`produce`, `consume`, `enrich`, `aggregate`, `load`, `query`).
- Keep one direction of flow; a response/ack that goes backward must be labeled as such.
- Draw fan-out/fan-in explicitly with multiple edges, not one ambiguous arrow.

Checklist: consistent source→sink direction; every transform edge labeled with its operation; stores vs operations visually distinct; fan-out/in explicit.

---

## Mindmap / concept map — `examples/mindmap.json`

A central concept radiating into related ideas.

- One prominent **root** (ellipse, larger) in the center or at top-left; children radiate out (rectangles or ellipses).
- Balance branches around the root; keep siblings at the same level of abstraction.
- 3–7 branches per node is the sweet spot. For depth, let a child be the parent of its own sub-branch.
- Every leaf connects back to its parent with an edge (arrowheads optional; `"end": null` for a cleaner map).

Checklist: exactly one clear root, visually distinct; branches balanced; siblings same abstraction level; every node connected; coverage matches the user's dimensions.
