# Third-party notices

Skills vendored into `.claude/skills/` from other projects, with their licenses.

Provenance also travels with each file, as an HTML comment at the top of its
`SKILL.md`, in one of two forms: `Vendored verbatim from ... @ <sha>`, or
`Vendored from ... ; adapted for this repo (<deltas>)`. See
[ADR 0002](./Decisions/0002-vendor-third-party-skills-as-plain-files.md).

---

## mattpocock/skills

Source: <https://github.com/mattpocock/skills>
Pinned at: `9c9f36ccd3995266cd675468af71639c8dde1ec5`

Vendored:

| Skill | Upstream path | Form |
|---|---|---|
| `grilling` | `skills/productivity/grilling/SKILL.md` | verbatim |
| `grill-me` | `skills/productivity/grill-me/SKILL.md` | verbatim |
| `wait-what` | `skills/productivity/wait-what/SKILL.md` | verbatim |
| `to-questionnaire` | `skills/productivity/to-questionnaire/SKILL.md` | verbatim |
| `writing-for-agents` | `skills/productivity/writing-for-agents/SKILL.md` | adapted |
| `handoff` | `skills/productivity/handoff/SKILL.md` | adapted, via an intermediate expansion |

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
`create-report`, `first-principles-investigation`, `wayfinder`, and
`setup-context-layers` are adapted from private repositories by the same author
as this template. They carry the same inline provenance convention so their
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
