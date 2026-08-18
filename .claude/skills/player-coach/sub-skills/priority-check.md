# Sub-skill: Priority Check

**Parent skill:** `player-coach`

This is the priority coaching scenario: the user wants to know whether what they're
planning to focus on (today / this week / this month) is actually the right thing to
focus on, given the company's current bets and the bar for their role.

**Before starting this sub-skill**, you must have already completed Steps 1–2 of the
parent `SKILL.md`: role detected, coaching mode declared. The ground rules from the
parent apply throughout.

---

## Phase A - Parallel Context Build

Launch **3 `Explore` sub-agents in parallel** in a single message. Do not read any files
serially before this step - the agents do the reading. After they return, read only the
*critical* files they identify.

Each agent brief should be self-contained (the agent has no conversation history) and
should ask for a ≤400-word report.

### Agent 1 - Strategic Context

Brief:
> Read these files and report back the top 3 active company bets, the bar for a
> world-class {role} right now, and any explicit constraints (merge freezes, deadlines,
> stakeholder commitments) that would affect what the user should prioritize this
> {timeframe}.
>
> Files to read:
> - The active venture's strategy and go-to-market docs under `Clients/<active venture>/` (for example `Clients/example-four/Activities/.../00-summary.md` and `06-the-wedge.md`). GTM is venture-specific and lives in the venture, not in Core.
> - `Core/philosophies.md`
> - Any role-specific canonical doc (for CMO: Brand Brief; for CEO: Revenue Metrics &
>   Pipeline Framework, Market Sizing, Competitive Intelligence; for Founding Engineer:
>   active architecture / sprint docs).
>
> Report structure:
> 1. Top 3 active company bets (one line each, with the source doc line cited)
> 2. What a world-class {role} would be prioritizing this {timeframe}
> 3. Explicit constraints: deadlines, commitments, freezes, stakeholder asks
> 4. Any strategic context the coach would be reckless to ignore
>
> Under 400 words. Cite file paths.

### Agent 2 - User's Stated Priorities & Carryover Pattern

Brief:
> Read the last 5 Daily Notes under `Operators/{current-operator}/Daily Notes/{year}/{MM}/` (resolve `{current-operator}` per the root `CLAUDE.md` rule)
> (walk back from today). For each day extract: the stated top 3 priorities, what was
> marked complete, what carried over, and any end-of-day notes.
>
> Then synthesize:
> 1. Today's stated top 3 priorities (verbatim)
> 2. Carryover pattern: what has been carrying over for 2+ days, and what's been dropped
>    silently
> 3. What the user's *actual* pattern of focus has been this week (from completions, not
>    stated intent)
> 4. Any signal that the user is drifting, stuck, or misaligned with their own stated
>    priorities
>
> Under 400 words. Cite specific daily note dates.

### Agent 3 - Active Initiatives (what's actually moving)

Brief:
> Report on what is actually moving in the repo right now. Run `git log --oneline -30`
> and inspect the 20 most recently modified files under the workspace. Report:
>
> 1. What work is shipping (recent commits grouped by theme)
> 2. What's slipping (files touched repeatedly without resolution, or topics mentioned in
>    daily notes but absent from commits)
> 3. What's been silent (themes in strategic docs that are getting no execution time)
> 4. Any active client commitments with dates (a comparable vendor etc.) found in recent notes, issues,
>    or commits
>
> Under 400 words. Cite commits and file paths.

After the 3 agents return, the coach reads only the 2–3 *critical* files each agent
flagged - not all of them. Synthesize the 3 reports into a single context summary that
will become the "Context" section of the output doc.

---

## Phase B - Optional Landscape Research

Skip this phase for purely internal-tactical TACTICAL mode sessions. For STRATEGIC or
STRETCH mode, or when the role bar is unclear, run **one** targeted `WebSearch` query to
surface external best-practice context.

Query template:
> "What does a world-class {role} in a {stage} {type-of-company} focus on in {timeframe}?"

Use the result to sharpen the Role-Bar check in Phase C. One query only. Do not
rabbit-hole.

---

## Phase C - Apply Frameworks

Run the user's stated priorities (or, if none are stated, the coach's proposed top 3)
through each of these seven gates. Each gate produces a short judgment that will feed
Phase D.

1. **Strategic Fit.** Does each priority directly advance one of the top 3 active company
   bets from Agent 1? If not, name what it does advance, or flag it as drift.
2. **Specificity.** Is each priority specific enough that at end-of-day you'd know
   whether it was done? Vague priorities get rewritten as concrete deliverables with a
   definition-of-done.
3. **Reversibility / Blast radius.** Is this a one-way door (needs more rigor) or
   two-way (move fast)? One-way doors on the priority list today need extra scrutiny.
4. **Status quo as competitor.** What does *not* doing this priority cost by end of the
   timeframe? If the answer is "nothing meaningful," it's not a top-3 priority.
5. **Role-bar check.** Would a world-class {role} spend today on this, or would they
   delegate / refuse / sequence it differently? Name the alternative explicitly.
6. **Sequencing.** Are dependencies in the right order? Anything blocked by something
   not on the list? Anything on the list that should wait until something else lands?
7. **Carryover pattern check.** From Agent 2: is this priority something that's been
   carrying over for N days? If yes, the real coaching question is *why* - scoping,
   focus, will, or blockage. Name which.

Each gate output is ≤2 sentences, work-anchored (cite the specific priority line).

---

## Phase D - Draft Verdict

For each stated priority, issue exactly one verdict:

- **KEEP** - advances a top bet, specific, sequenced correctly
- **RESHAPE** - right intent, wrong shape (provide the rewrite)
- **DROP** - drift / nice-to-have / wrong sequence
- **PROMOTE** - was buried elsewhere in the day, should be top-3
- **ADD** - missing from the list and should be on it

If the user did not state priorities, propose a top 3 with rationale anchored to the
strategic context from Phase A.

**This is a draft.** It does NOT go to the user yet. It must survive adversarial review
in Phase E first. Do not write to the output doc in this phase.

---

## Phase E - Adversarial Review + Refine Loop

This is the rigor step. Without it, the coach is one voice. With it, the coach is
accountable to three hostile readers before anything reaches the user. This phase is
mandatory - do not skip it, even if the draft feels strong.

### E.1 - Launch 3 Parallel Critics

Launch **3 `general-purpose` sub-agents in parallel** in a single message. Each critic
gets:
- The full Phase A context summary
- The full Phase D draft verdict
- Their specific hostile lens (below)

| Critic | Lens | Must answer |
|---|---|---|
| **The Skeptic** | "This coaching is generic / could apply to anyone / isn't grounded in the user's real context." | Name the 3 weakest specificity failures in the draft. For each, quote the exact line and cite what evidence from the Phase A context is missing. |
| **The Bet-Fitter** | "None of these priorities actually move a top-3 company bet - the coach is rationalizing drift." | For each KEEP verdict, trace the causal chain: priority → concrete business outcome → one of the top-3 bets from Agent 1. If any link is broken or hand-waved, flag it. |
| **The Role-Bar Auditor** | "A world-class {role} wouldn't spend a day on any of this. The coach is grading on a curve." | For each priority, propose what a world-class {role} would do *instead*, and explain where the draft let the user off easy. Cite the Phase B landscape research if it was run. |

Each critic returns:
1. **PASS** or **FAIL** verdict
2. Specific failures found (quoted lines, specific gaps)
3. A concrete rewrite suggestion for each failure

### E.2 - Refine the Draft

For every critic that returned FAIL with a legitimate failure, rewrite the affected
section of the draft verdict. Document what changed and which critic triggered each
refinement - this feeds the "Adversarial review" section of the output doc.

If a critic returned FAIL but the coach disagrees with the critique (e.g., the critic
misread the context), record the disagreement and the reasoning. Do not silently ignore
critic feedback.

### E.3 - Re-run if Needed

If **≥2 critics returned FAIL** on the first pass, re-run the same 3 critics on the
refined draft. This is the review-refine *loop*.

**Hard cap: 2 refinement iterations total.** If critics still disagree after 2
iterations, the coach picks the position they're most confident defending and flags the
unresolved dissent in the output doc. Do not iterate indefinitely - polishing has
diminishing returns after 2 passes.

### E.4 - Surface, Don't Bury

If any critic dissent is unresolved after the loop, surface it explicitly in the output
doc. Never bury it. The user must see exactly where the coach's confidence is limited.

---

## Phase F - One Forcing Question

Ask exactly **one** forcing question via `AskUserQuestion`. Never batch. One decision
per turn.

The question should target the highest-leverage uncertainty exposed by the session. In
order of preference:

1. **Unresolved critic dissent from Phase E** - if the adversarial loop flagged something
   and the user's answer would resolve it, that's the question.
2. **The least-confident KEEP verdict** - the priority the coach kept with the most
   hedging.
3. **A missing constraint** - something the coach would need to know (a deadline, a
   stakeholder commitment, a hidden dependency) to lock down the recommendation.

The question must be concrete and answerable in one sentence. Vague questions
("how do you feel about this?") violate the specificity gate.

---

## Phase G - Write Output Doc

Write to `Operators/{current-operator}/Coaching/YYYY-MM-DD-priority-check.md`.
Create the `Coaching/` folder if it doesn't exist.

Use this exact structure:

```markdown
---
date: YYYY-MM-DD
role: {role}
mode: {TACTICAL|STRATEGIC|STRETCH|UNBLOCK}
scenario: priority-check
---

# Priority Coaching - {Role}, {Date}

**Mode:** {mode} - {one-line rationale for why this mode}

## Context (from scouting agents)
- Top 3 active company bets: …
- World-class {role} bar this {timeframe}: …
- User's stated priorities (today): …
- Carryover pattern (last 5 days): …
- Active commitments / deadlines: …

## Verdict per priority (post-adversarial-review)
1. **[KEEP|RESHAPE|DROP|PROMOTE|ADD]** - {priority} - {2–3 sentence rationale, work-anchored}
2. …
3. …

## Recommended top 3 (post-coaching)
1. …
2. …
3. …

## Adversarial review
- **Skeptic:** {PASS/FAIL} - {failures found → refinements made}
- **Bet-Fitter:** {PASS/FAIL} - {failures found → refinements made}
- **Role-Bar Auditor:** {PASS/FAIL} - {failures found → refinements made}
- **Iterations:** {1 or 2}
- **Unresolved dissent (if any):** {explicit note - never buried}

## Forcing question
{the one question asked via AskUserQuestion}

## Signal observations
{1–3 bullets of what the coach noticed about the user's pattern this session. Examples:
"Same a comparable vendor architecture task carried over 3 days - scoping issue, not will issue."
"User's stated priorities have drifted away from GTM top-bet #2 for 4 days in a row."
"First time the user has stated a priority with a concrete definition-of-done."
These accumulate across sessions and let future sessions detect arcs.}
```

After writing the doc, tell the user where it was saved and surface the top 1–2
findings in the chat. Do not paste the whole doc back into chat - the user will open the
file. Then ask the Phase F forcing question.
