<%*
const title = await tp.system.prompt("Document title");
const scope = await tp.system.prompt("Scope path, or . for workspace-wide", ".");
const slug = scope === "." ? "none" : scope.toLowerCase();
-%>
---
type: doc/policy
status: draft
created: <% tp.date.now("YYYY-MM-DD") %>
scope: <% slug %>
tags:
  - type/doc/policy
  - status/draft
  - scope/<% slug %>
---

# <% title %>

> [!note] Draft, unfilled.
> This records the shape of a question that has not been answered yet. It is
> deliberately not invented. Fill a section when the answer is real.

## Section

The question this section answers, stated as a prompt rather than an assertion.

- TBD
