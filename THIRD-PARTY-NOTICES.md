# Third-party notices

Skills vendored into `.claude/skills/` from other projects, with their licenses.

Provenance also travels with each file, as an HTML comment at the top of its
`SKILL.md`, in one of two forms: `Vendored verbatim from ... @ <sha>`, or
`Vendored from ... ; adapted for this repo (<deltas>)`. See
[vendoring provenance](./Standards/harness-standards.md#vendoring-provenance).

---

## mattpocock/skills

Source: <https://github.com/mattpocock/skills>
Pinned at: `9c9f36ccd3995266cd675468af71639c8dde1ec5`

Vendored:

| Skill | Upstream path | Form |
|---|---|---|
| `grilling` | `skills/productivity/grilling/SKILL.md` | verbatim |
| `grill-me` | `skills/productivity/grill-me/SKILL.md` | verbatim |
| `grill-with-docs` | `skills/engineering/grill-with-docs/SKILL.md` | verbatim |
| `clarify` | `skills/productivity/wait-what/SKILL.md` | adapted, renamed from `wait-what` |
| `to-questionnaire` | `skills/productivity/to-questionnaire/SKILL.md` | verbatim |
| `teach` | `skills/productivity/teach/SKILL.md` | adapted |
| `writing-for-agents` | `skills/productivity/writing-for-agents/SKILL.md` | adapted |
| `handoff` | `skills/productivity/handoff/SKILL.md` | adapted, via an intermediate expansion |
| `wizard` | `skills/engineering/wizard/SKILL.md` | verbatim, pinned at `1bb95954ef0d` |

`wizard` was vendored later than the rest and carries its own pin, recorded in
the row above and in its provenance marker. The block pin is where everything
else came from; a per-skill pin overrides it. `wizard` also vendors
`template.sh` unmodified, and like `grill-with-docs` leaves upstream's
`agents/openai.yaml` behind.

`clarify` is the local name; the upstream path is where it came from and stays
recorded as such, so a future diff against upstream still resolves.

`grill-with-docs` upstream also carries `agents/openai.yaml`, which is interface
metadata for a different runtime and has no meaning in this harness or home in
the skill layout. It is deliberately not vendored. The `SKILL.md` is verbatim.

`teach` upstream keeps its four `*-FORMAT.md` files beside `SKILL.md`; here they
are under `references/`, per the skill layout standard.

```
MIT License

Copyright (c) 2026 Matt Pocock

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## spencermarx/wrkbelt-agent-team

Pinned at: `496d37273aca`. A private repository by the same author, and the
ancestor of this lineage.

Recovered from it: `get-brand-kit`, `image-overlay` (with `overlay.sh`),
`image-prompt`, `image-clean`, `startup-idea-engine`, `campaign-brief`,
`business-retro`, `openai`, and the four Google stubs.

`get-brand-kit` and `image-overlay` are the two dependencies that
`create-html-slides` had been referencing without them existing anywhere in its
own repository. Recovering them is what repaired that skill.

Every one of these was de-branded on the way in: the palette is now a neutral
placeholder, the logo assets are generated wordmarks, and the per-variant
luminance constants are computed from the SVGs rather than hardcoded to one
brand's hexes.

---

## Skills adapted from the author's own earlier work

`scratchpad`, `handoff`, `conveying-clearly`, `context`, `domain-modeling`,
`create-report`, `first-principles-investigation`, and `wayfinder` are adapted
from private repositories by the same author as this template. They carry the same inline provenance convention so their
lineage stays legible, and several of them are themselves downstream of
`mattpocock/skills`, which the marker records.

---

## Frameworks credited in skill bodies

Some skills implement a published framework and credit it in the skill itself
rather than here, because the skill is an original implementation rather than
vendored code:

- `seven-copy-critics` adapts Simon Severino's Seven Critics framework.
- `ceo-review`, `strategic-brief`, and `brand-review` adapt patterns from gstack.
- `rice-prioritization` implements the RICE model originated by Sean McBride at
  Intercom.

---

## Obsidian plugins

Two are vendored, because they cannot be installed any other way:

| Plugin | License | Source |
|---|---|---|
| `agentic-copilot` | MIT | <https://github.com/spencermarx/obsidian-ai> |

Five more are **declared but deliberately not vendored**, in
`.obsidian/plugins/store-plugins.json`:

| Plugin | License |
|---|---|
| Templater | AGPL-3.0 |
| Excalidraw | AGPL-3.0 |
| Notebook Navigator | GPL-3.0 |
| Advanced Tables | GPL-3.0 |
| Tag Wrangler | ISC |
| Things (theme) | MIT |

Four of those are copyleft. Committing their built `main.js` into this
MIT-licensed template would redistribute GPL and AGPL binaries under an
incompatible license, so they are installed from Obsidian's own plugin browser
instead. `community-plugins.json` still lists them, so the enable-list travels
with a clone and they switch on the moment they are installed.
