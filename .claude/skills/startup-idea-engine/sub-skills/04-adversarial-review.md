# Sub-skill: Adversarial Review

**Parent skill:** `startup-idea-engine`

For every candidate that survived Phase 4 (Research Validation), spawn parallel hostile critics. Surface the strongest objection from each. Refine candidates against the objections. Up to 2 refinement rounds. Candidates that cannot survive critics after 2 rounds are killed. Critic dissent that cannot be resolved is **never buried** — it is surfaced in the final output.

**Before starting this sub-skill**, the surviving candidates from Phase 4 are in the session document with their updated test matrices and research findings.

**Critical framing rule:** Adversarial review is a *gate*, not a formality. The user does not see raw conclusions until the critics have run. Inspired by the parallel-critic patterns in `seven-copy-critics`, `player-coach`, and the gstack `/office-hours` Phase 3.5 cross-model second opinion.

---

## The Four Critics

Each critic is a separate `general-purpose` sub-agent dispatch with a focused brief. Critics run in parallel — one message, four tool calls. Each critic returns a ≤300-word verdict.

### Critic 1 — The Hostile Investor

**Brief:**
> You are a senior partner at a Tier-1 venture firm (Sequoia / Benchmark / a16z shape). A founder pitches you the candidate below in a 5-minute coffee chat. You are skeptical by default, busy, pattern-matched against years of failed bets in adjacent spaces.
>
> Your job: surface the *strongest single objection* a hostile investor would raise. Not all objections — the one that would most immediately collapse the pitch.
>
> Specifically test:
> - Is the market large enough to matter at venture scale? (Note: the founder may be explicitly *not* venture-shaped; if so, the test is whether the business is large enough to matter at the founder's chosen scale.)
> - Is the moat real, or is this a feature that any well-funded incumbent ships in 6 months?
> - Is the team uniquely positioned to win this, or could anyone with capital execute it?
> - What is the obvious "why hasn't this been built?" answer, and is the candidate's answer compelling?
>
> Return:
> 1. The single strongest objection (one paragraph)
> 2. What evidence would change your mind (specific, falsifiable)
> 3. A verdict: PASS (objection addressable) / FAIL (objection structural) / DEFER (need data)
>
> Under 300 words. Direct. No hedging.

### Critic 2 — The Hostile Incumbent

**Brief:**
> You are the head of strategy or product at the most obvious incumbent in this candidate's space — name them explicitly based on the candidate's market. (For the operator's candidates: this is often the incumbent vendor, Workato, BetterCloud, Mindbody, or whichever incumbent is the named threat.)
>
> Your job: predict your company's 90-day response to this candidate launching, and assess whether your response would crush the candidate.
>
> Specifically test:
> - Could you ship a competing feature in your existing product in 6 months?
> - Could you acquire the leader in this category for $20–50M and absorb the threat?
> - Could you cut off the candidate's distribution channel (e.g., API access, marketplace listing)?
> - Could you simply outwait them — let them prove the category, then enter with scale?
>
> Return:
> 1. Your most likely 90-day response (specific tactical move)
> 2. The candidate's structural counter (if any)
> 3. A verdict: PASS (candidate has structural defense) / FAIL (incumbent crushes inside 12 months) / DEFER (depends on timing)
>
> Under 300 words. Speak as the incumbent's voice. Specific, ruthless, no flattery.

### Critic 3 — The Principles Auditor

**Brief:**
> You are an external auditor whose only job is to ensure the candidate survives the founder's stated principles AND founder shape, under sustained scale pressure. The founder's principles are loaded into the session document; read them before assessing.
>
> Your job: audit the candidate against the principles and founder-shape constraints, focusing on *gradient drift* — what does the candidate become at $10M ARR, at $100M ARR, under acquisition pressure, under VC pressure?
>
> Specifically test (for the operator):
> - **Anti-Exploitation:** Does the candidate remain anti-extractive at scale, or does the gradient lead toward a take-rate / dark-pattern / data-extraction model?
> - **Craftsmanship-as-Moral-Act:** Does the candidate require sustained craft, or does it incentivize quantity-over-quality?
> - **Always Strive for Good:** Is the candidate actively striving for good, or merely "not doing bad"?
> - **Cognitive Sovereignty:** Does the candidate respect users' capacity to think, choose, and live, or does it depend on engagement-maximization or attention-capture?
> - **Founder shape:** Does the candidate work at $100M+ revenue with no VC, family-rooted team, no Patagonia-shaped CEO yet?
> - **Acquisition foreclosures:** What acquirers are foreclosed by the principles? Does the candidate's natural exit-shape violate them?
>
> Return:
> 1. The single principle or founder-shape constraint most at risk under sustained scale
> 2. The structural commitment (corporate form, governance, license, capital strategy) that would prevent drift
> 3. A verdict: PASS (no structural risk OR risk is addressable with stated commitment) / FAIL (gradient drift unavoidable) / DEFER (depends on chosen corporate form)
>
> Under 300 words. Specific. Cite which principle clause is at risk.

### Critic 4 — The Tarpit Auditor

**Brief:**
> You are Dalton Caldwell or Michael Seibel reviewing the candidate against the tarpit-ideas catalog. Tarpit ideas are patterns that first-time founders cluster on, that look attractive, and that a generation of failed attempts has established do not work for structural reasons.
>
> Your job: identify whether the candidate sits in any documented tarpit shape. Reference the tarpit catalog at `references/dalton-michael-tarpits.md`.
>
> Specifically test:
> - Is this a "better X" idea where X is an incumbent category leader? (Most "better CRM," "better email tool," "better calendar" candidates are tarpit.)
> - Is this an "X for Y" idea where Y is a notoriously hard-to-sell-to vertical? (E.g., "AI for restaurants," "software for nonprofits.")
> - Is this a marketplace where neither side is structurally captive?
> - Is this a "social network for X profession" idea?
> - Is this an attention-economy or engagement-maximization play?
> - Has the founder cited prior generations' failure modes in this space, and does the candidate's structural difference address them?
>
> Also consider founder-specific tarpit history. For the operator: Q1 produced 7-8 trades-agency interest with 0 conversions, 0/15 HCP discovery conversations, and 0/15 law-firm conversations. Cold outbound to SMB owners was a shape-failure. Re-running that shape with a different pitch is tarpit-shaped repetition.
>
> Return:
> 1. The tarpit shape (if any) the candidate fits, with the canonical name
> 2. The structural difference the candidate must demonstrate to escape the tarpit
> 3. A verdict: PASS (no tarpit shape OR clear structural difference) / FAIL (canonical tarpit shape with no escape) / DEFER (adjacent to tarpit, may escape with refactor)
>
> Under 300 words. Cite the tarpit pattern name. No hedging.

---

## Refinement Loop

After all four critics return, for each candidate:

1. **Synthesize the four objections** into a single one-paragraph "what we must address." If the four critics agree on the same objection, it is the gate. If they raise different objections, prioritize the FAIL > DEFER > PASS hierarchy and address the FAIL first.

2. **Refine the candidate.** Refinement options:
   - **Narrow the wedge** to address an investor objection (e.g., "pivot from broad the incumbent vendor sanitization to specifically the PE-acquisition integration moment")
   - **Add a structural defense** to address an incumbent objection (e.g., "customer-owned portable spec format makes vendor capture less valuable")
   - **Commit to a corporate-form constraint** to address a principles objection (e.g., "commit to steward-ownership before scale pressure arrives")
   - **Demonstrate the structural difference** to address a tarpit objection (e.g., "this is not 'better CRM' because the buyer is the substrate operator, not the seller")

3. **Re-run the affected critics** on the refined candidate. Up to 2 refinement rounds total.

4. **Verdict after refinement:**
   - SHIP = all four critics PASS or DEFER (with the DEFER explicitly noted as future-resolvable)
   - KILL = any critic returns FAIL after 2 refinement rounds
   - SHIP-WITH-DISSENT = three critics PASS, one critic dissents irreconcilably. The dissent is **named in the final output** under "Reviewer Concerns" per the gstack pattern. Never bury.

---

## Mode Behavior

| Mode | Behavior |
|---|---|
| AUTOPILOT | Run all four critics in parallel. Refine. Run again if needed. Apply verdicts. Advance to Phase 6. |
| COLLABORATE | Run critics in parallel. Present synthesis. Pause: "Direction on refinement?" User can choose narrow / structural / commitment / difference / kill. Then refine. |
| STEP-BY-STEP | Run critics in parallel (this is faster than serial and more honest). Present each critic's verdict separately. Pause for user reaction per critic before refinement. |

---

## Anti-Patterns

- **Letting the founder rebut the critic to themselves.** The critic's voice is the gate. The founder's "but actually…" without changing the candidate is denial, not refutation.
- **Refining away the criticism rather than the candidate.** "We'll just say it differently" is not refinement. The candidate must structurally change.
- **Burying dissent.** If the principles auditor or the tarpit auditor refuses to PASS after refinement, that dissent is named in the output. Do not silently downgrade dissent to PASS.
- **Skipping refinement and shipping anyway.** A KILL verdict from any critic, after 2 rounds, is binding. The user can override only with an explicit reason logged in the session document AND a corresponding "Reviewer Concerns" section in the Raw Idea doc.

---

## Output to Session Document

Append the full critic verdicts and refinement rounds to the session document under "Phase 5 — Adversarial Review." For each candidate:

```markdown
### Candidate: {name}

**Round 1 — Critics:**
- Hostile Investor: {verdict} — {one-line objection}
- Hostile Incumbent: {verdict} — {one-line objection}
- Principles Auditor: {verdict} — {one-line objection}
- Tarpit Auditor: {verdict} — {one-line objection}

**Refinement: {what changed}**

**Round 2 (if needed):**
- {Critics re-verdicts}

**Final verdict:** SHIP / KILL / SHIP-WITH-DISSENT

**Unresolved dissent (if any):** {named, never buried}
```

Advance SHIP and SHIP-WITH-DISSENT candidates to Phase 6 (Output Write).
