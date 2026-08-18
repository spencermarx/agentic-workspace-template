# Sub-skill: Framework Tests

**Parent skill:** `startup-idea-engine`

Apply Paul Graham's tests + Dalton/Michael's tarpit screen + the user's principle/founder-shape filters to every candidate from Phase 2. Each test produces PASS / PARTIAL / FAIL. Candidates with multiple FAILs are killed before research validation.

**Before starting this sub-skill**, the candidate list from Phase 2 (Noticing) is in the session document. The context summary, principles, founder shape, and topology are loaded.

**Loaded references:**
- `references/pg-framework.md` — full PG framework distilled (faster than re-reading the original essay)
- `references/dalton-michael-tarpits.md` — tarpit catalog with the operator-specific examples

---

## The Seven Tests

For each candidate, run all seven tests. Each test produces a verdict + a one-line reason.

### Test 1 — PG Three-Pillar (Founders Want / Build / Few Realize)

> "The very best startup ideas tend to have three things in common: they're something the founders themselves want, that they themselves can build, and that few others realize are worth doing." (PG)

**Three checks:**
- **Want:** Does the founder personally want this? Skin in the game? Has experienced the pain?
- **Build:** Does the founder's competence + topology cover this without rewrite or new core competence?
- **Few realize:** Is this non-obvious to the average competing founder? (Crowded ≠ tarpit; obvious ≠ wrong; the test is whether the *insight* is widely held.)

**Verdict rule:**
- PASS = all three pillars cleanly satisfied
- PARTIAL = one pillar weak but recoverable
- FAIL = two or more pillars missing or aspirational

### Test 2 — Demand-Shape (Well, not Broad)

> "Microsoft's Altair Basic had thousands of users programming in machine language without it. Pet-owner social network: millions might use it someday, but zero use it urgently." (PG)

**The check:** Who urgently needs this *right now*, so badly they would use a crappy v1? Name them with a face — title, company size, situation, the specific moment of pain.

**Verdict rule:**
- PASS = a named, narrow well exists; the user can describe the buyer in one specific sentence with all four (title, company shape, situation, moment)
- PARTIAL = the well exists but is described in generic terms (push for specificity in research validation)
- FAIL = no narrow well; the only honest answer is "many people might find this useful eventually"

### Test 3 — Founder-Market Fit (Lineage Shape)

**The check (user-specific):** Does this candidate fit the user's principle-aligned lineage? For the operator, the lineage is: tools that give an individual operator agency in a domain dominated by larger institutions (food, healthcare, telehealth, SMB services, AI dev tools). Every prior project fits this shape. The next idea must fit too — or have an explicit reason for departing.

**Operational check:**
- Does the candidate empower the small operator / individual / craftsperson?
- Does it oppose or route around an extractive larger institution?
- Does it pass all four principles (Anti-Exploitation, Craftsmanship-as-Moral-Act, Always Strive for Good, Cognitive Sovereignty)?

**Verdict rule:**
- PASS = lineage fit clean, all four principles pass cleanly
- PARTIAL = lineage fit partial OR one principle creates tension that needs deliberate design to resolve
- FAIL = candidate violates a principle OR fits the *opposite* lineage (powering the extractive institution)

### Test 4 — Schlep-Disabled

> "Stripe benefited from disabled schlep filter; thousands saw the pain but flinched. Schlep blindness is the most dangerous filter to leave on." (PG)

**The check:** Does the candidate exploit a schlep-disabled position the user already holds? The schlep must be *already done*, not aspirational. The candidate is strongest when most founders would flinch from the tedious work and the user has already done it.

**Examples (the operator-specific schlep-disabled positions):**
- the incumbent vendor API depth (months of integration work most founders would refuse)
- Multi-tenant hierarchical authorization (Walking Skeleton)
- Spec-driven AI codegen (Intent Architecture RFC)
- Telehealth UX patterns (Doxy.me-shaped simplicity at scale)

**Verdict rule:**
- PASS = the candidate exploits a clear schlep-disabled position
- PARTIAL = the candidate could exploit one with a 30-90 day investment
- FAIL = the candidate has no schlep moat; any well-funded team could ship it in 90 days

### Test 5 — Wave Alignment

> "What becomes possible in 3–5 years that we currently rule out? What companies might profit from the decline of incumbents?" (PG)

**The check:** Is the candidate riding a real, dated, structurally-changing wave? "AI is exciting" is not a wave. "Computer Use launched October 2024 making cross-app browser-agent operations affordable for SMB" is a wave.

**Verdict rule:**
- PASS = candidate rides a specific, dated wave with structural change behind it
- PARTIAL = candidate touches a wave but isn't built on the wave's structural change
- FAIL = candidate doesn't depend on any recent wave; could have been shipped 5 years ago

### Test 6 — Tarpit Check (Dalton/Michael)

**Reference:** Load `references/dalton-michael-tarpits.md`. Candidates are checked against:
- The general tarpit catalog (well-documented YC patterns)
- the operator's Q1 history (channel-shapes that already failed)

**Examples of tarpit shapes to flag:**
- "Better SMB CRM"
- "AI-powered scheduling for X vertical"
- "Social network for X profession"
- "Marketplace for X" (most marketplace ideas are tarpit unless one side is structurally captive)
- "Attention-economy or engagement-maximization tooling"
- Founder-led cold outbound to SMB owners (the operator's Q1 shape that failed)

**Verdict rule:**
- PASS = candidate is not in any documented tarpit shape
- PARTIAL = candidate is adjacent to a tarpit but has a structural reason to differ (state what)
- FAIL = candidate fits a documented tarpit cleanly with no structural difference

### Test 7 — Plausibility-Trap Check

> "The set of plausible-sounding startup ideas is many times larger than the set of good ones." (PG)

**The check:** This is the *meta* test. After running tests 1–6, ask: does this candidate sound very plausible on first reading? PG's warning is that plausible-sounding ideas are statistically more likely to be bad. Plausible ≠ wrong, but plausible-with-no-friction-or-edge usually = wrong.

**Operational signal:** If the candidate description reads like a generic SMB-software pitch deck — "we help X solve Y by leveraging Z" — and contains no surprising or counterintuitive specificity, the candidate is plausibility-trap-shaped.

**Verdict rule:**
- PASS = candidate has a non-obvious specific edge that makes it sound at-first slightly weird or surprising
- PARTIAL = candidate is plausible but defensible because of a specific anchor
- FAIL = candidate is too plausible; reads like a category-search output

---

## Test Matrix Output

For each candidate, produce:

```markdown
### Candidate: {name} (procedure {A–F})

| Test | Verdict | Reason |
|---|---|---|
| 1. PG Three-Pillar | PASS / PARTIAL / FAIL | one-line reason |
| 2. Demand-Shape (Well) | PASS / PARTIAL / FAIL | one-line reason |
| 3. Founder-Market Fit | PASS / PARTIAL / FAIL | one-line reason |
| 4. Schlep-Disabled | PASS / PARTIAL / FAIL | one-line reason |
| 5. Wave Alignment | PASS / PARTIAL / FAIL | one-line reason |
| 6. Tarpit Check | PASS / PARTIAL / FAIL | one-line reason |
| 7. Plausibility Trap | PASS / PARTIAL / FAIL | one-line reason |

**Score:** {N PASS} / {N PARTIAL} / {N FAIL}
**Verdict:** ADVANCE / KILL / REFACTOR
```

**Verdict rules:**
- ADVANCE = ≥5 PASS and 0 FAIL
- REFACTOR = exactly 1 FAIL but the candidate has a structural reason to refactor (e.g., narrowing the buyer, swapping the wedge shape). Refactor in place; re-run tests; if it can't reach ADVANCE in one refactor pass, kill.
- KILL = ≥2 FAIL or "few realize" + "tarpit" both FAIL (tarpit-shaped obvious idea — not the bet)

---

## Mode Behavior

| Mode | Behavior |
|---|---|
| AUTOPILOT | Run all tests on all candidates. Apply verdict rules. Advance survivors to Phase 4 without pause. |
| COLLABORATE | Run all tests. Present full matrix. Pause: "Override any KILL or REFACTOR decisions?" User can override before advancing. |
| STEP-BY-STEP | Walk through one candidate's tests at a time. Pause for reaction, refinement, or kill at each candidate. |

---

## Output to Session Document

Write the full test matrix to the session doc under "Phase 3 — Framework Tests." Append a one-paragraph synthesis: which candidates advanced, which were killed, which were refactored, and the strongest theme that emerged across the tests.

Advance survivors to Phase 4 (Research Validation).
