# Sub-skill: Research Validation

**Parent skill:** `startup-idea-engine`

For every candidate that survived Phase 3 (Framework Tests), run targeted research designed to **kill, not justify**. Update the Phase 3 test matrix with research findings. Candidates whose tests degrade to FAIL after research are killed before Phase 5 (Adversarial Review).

**Before starting this sub-skill**, the surviving candidates from Phase 3 are in the session document with their test matrices.

**Critical framing rule:** Confirmation bias is the single largest threat to ideation quality. The skill is built against it. Every research query must be framed in a way that *would kill the candidate if the answer is bad*. If a query can only confirm, do not run it. If the user's instinct in COLLABORATE mode is to run only confirming queries, push back hard.

---

## The Five Research Queries (per candidate)

Run all five queries per candidate. Each query has an explicit "kill criterion" - what answer would degrade a test verdict.

### Query 1 - Documented Pain Evidence

**Goal:** Verify the pain claimed by the candidate is documented in real third-party sources, not just in the user's intuition.

**Search shape:** `WebSearch` for industry reports, recent research, customer-survey data, professional publications, or recent posts on the specific pain point.

**Kill criterion:** If the pain is *only* documented in vendor marketing pages (i.e., only by people selling solutions), it may be manufactured. PARTIAL becomes acceptable; absence of independent documentation is FAIL on Test 1 (PG Three-Pillar - "few realize" becomes "many vendors realize and are selling against it").

**Operational template:**
```
WebSearch query: "{specific pain} {target buyer} 2025 2026 statistics" or "{specific pain} {industry} survey report"
WebSearch query: "{target buyer} biggest challenges 2026" - to surface what they actually complain about, not what vendors think they should
WebSearch (forum-shape): "site:reddit.com OR site:hackernews {target buyer} {pain area}" - to find direct buyer voice
```

### Query 2 - Incumbent Landscape and Reviews

**Goal:** Map the existing competitive landscape. Crowded ≠ bad. Tarpit + saturated = bad. The check is whether incumbents are weak in the specific dimension the candidate exploits.

**Search shape:** `WebSearch` for the top 5–10 existing tools in this category. Then `WebFetch` reviews, complaints, or G2/Capterra-tier feedback for the leading 2–3.

**Kill criterion:**
- If 3+ well-funded incumbents are clearly addressing the *exact* pain with the *exact* mechanism the candidate proposes, FAIL on Test 6 (tarpit) unless the candidate has a structural difference.
- If reviews of incumbents show the pain is being solved adequately, the wedge is closed.
- If a category leader is shipping a competing feature in the next 6 months (e.g., "the incumbent vendor launches AR automation summer 2026"), this is a near-fatal signal.

**Operational template:**
```
WebSearch: "best {category} software 2026" - surface incumbents
WebSearch: "{category leader} reviews complaints 2026" - find weakness
WebSearch: "{category leader} roadmap 2026" - find collision risk
WebFetch on review sites: "What are users complaining about? What do they say is missing?"
```

### Query 3 - Buyer Process and Sales Cycle

**Goal:** Verify the buyer described in Test 2 (Demand-Shape) is actually buyable on the timeline the candidate assumes. A 90-day wedge cannot survive a 9-month sales cycle.

**Search shape:** `WebSearch` for the buyer's procurement process, typical purchase cycle length, decision authority, common purchase triggers.

**Kill criterion:**
- If the buyer's documented procurement cycle exceeds the candidate's wedge timeline by 2x, FAIL on Test 2 unless the wedge is structurally reframed for a faster path.
- If the buyer described doesn't have purchasing authority for this category (e.g., marketing director cannot buy AR software - that's a finance buyer), FAIL on founder-market fit because the user's network does not reach the actual buyer.

**Operational template:**
```
WebSearch: "{buyer title} purchasing authority {category}" - surface who actually signs
WebSearch: "{buyer title} {company shape} how do they buy software"
WebSearch: "average sales cycle {category} {company size}"
```

### Query 4 - Wave Verification

**Goal:** Verify the wave the candidate rides (Test 5) is real, dated, and not already saturated. Confirm the timing.

**Search shape:** `WebSearch` for recent (last 90 days) news, funding announcements, product launches, or category-formation signals in the wave area. Cross-check against current YC RFS.

**Kill criterion:**
- If the wave was real but is now saturated (10+ funded competitors in the past 18 months), FAIL on Test 5.
- If the wave is real but the user's specific position on it is downwind of better-positioned players, PARTIAL on Test 5 with explicit acknowledgment.
- If the candidate doesn't actually depend on the wave (would have been shippable 5 years ago), demote to PARTIAL on Test 5 anyway.

**Operational template:**
```
WebSearch: "{wave keyword} startups 2026" - surface recent activity
WebSearch: "{wave keyword} funding 2025 2026" - surface capital intensity
WebFetch YC RFS: "https://www.ycombinator.com/rfs" - verify YC's current wave bets
```

### Query 5 - Tarpit History

**Goal:** Check whether prior generations of founders have already tried this candidate shape and failed. If they have, find out why; refactor or kill.

**Search shape:** `WebSearch` for failed startups in the candidate's space, post-mortems, "why X failed" articles, or category-decline signals.

**Kill criterion:**
- If 5+ funded attempts at the candidate shape have failed in the past 5 years for the *same* reason, FAIL on Test 6 (tarpit) unless the candidate's structural difference addresses the documented failure mode.
- If failed attempts are recent (last 24 months) and the failure mode is the user's exact wedge, this is near-fatal.

**Operational template:**
```
WebSearch: "{candidate category} startup failed post-mortem"
WebSearch: "why {category} startups die"
WebSearch: "site:news.ycombinator.com {category}" - Hacker News commentary often surfaces tarpit recognition
```

---

## Update Rules After Research

For each candidate, after all five queries:

1. **Re-run the affected Test verdicts** with the research findings. Most commonly:
   - Query 1 affects Test 1 ("few realize" pillar) and Test 2 (demand reality)
   - Query 2 affects Test 6 (tarpit) and Test 4 (schlep - if incumbents are deep, schlep moat may be illusory)
   - Query 3 affects Test 2 (demand-shape - buyer reachability)
   - Query 4 affects Test 5 (wave alignment)
   - Query 5 affects Test 6 (tarpit) hard

2. **Promote or demote the candidate's verdict.** ADVANCE candidates whose Test verdicts degrade may become REFACTOR or KILL. KILL is binding once both Phase 3 and Phase 4 have run; the user can override only in COLLABORATE / STEP-BY-STEP modes with an explicit reason logged in the session document.

3. **Document research findings** in the session document under "Phase 4 - Research Findings." Each candidate gets a short subsection:

```markdown
### Candidate: {name}

**Q1 - Pain evidence:** {1-2 lines, with sources}
**Q2 - Incumbents:** {1-2 lines, top 3 named, weakness or strength}
**Q3 - Buyer process:** {1-2 lines, cycle length, authority, friction}
**Q4 - Wave:** {1-2 lines, dated and verified or demoted}
**Q5 - Tarpit history:** {1-2 lines, failed attempts found or not}

**Test matrix updates:**
- Test {N}: {OLD} → {NEW}, reason: {one line}

**New verdict:** ADVANCE / REFACTOR / KILL
```

---

## Mode Behavior

| Mode | Behavior |
|---|---|
| AUTOPILOT | Run all 5 queries × all surviving candidates. Update verdicts silently. Advance ADVANCE candidates to Phase 5. |
| COLLABORATE | Run all queries. Present findings + updated verdicts. Pause: "Override any KILL/REFACTOR decisions?" Confirm advances. |
| STEP-BY-STEP | Run one query at a time per candidate. Present findings, pause for reaction, refine the candidate or update tests collaboratively, then move to the next query. |

---

## Anti-Patterns

- **Confirming the founder's intuition.** Queries that frame the search around evidence the candidate is right are the failure mode. Frame queries to surface evidence the candidate is *wrong*.
- **Source quality drift.** Vendor marketing pages, AI-generated SEO articles, and decade-old strategy posts are low-signal. Weight: Hacker News threads, Reddit communities of practitioners, recent Stratechery / a16z / First Round posts, recent funding announcements, professional / trade publication reports, customer-review sites (G2, Capterra).
- **Search saturation.** If 5 queries don't move the verdict, stop. Returning to the same well looking for confirming evidence is the failure mode the skill is designed against.
- **Skipping Query 5 (tarpit history).** This is the single most-skipped query and the single most-fatal one. Tarpit history must always run.

---

## Output to Session Document

Append the full Phase 4 findings under "Phase 4 - Research Validation." Update the Phase 3 test matrix in place (do not delete the old verdicts; show the updates as `OLD → NEW`).

Append a one-paragraph synthesis: which candidates survived research, which were killed by which queries, and the strongest objections that surfaced across all candidates (these will inform Phase 5 adversarial review).

Advance survivors to Phase 5 (Adversarial Review).
