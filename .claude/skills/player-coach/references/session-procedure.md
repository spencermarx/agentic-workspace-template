# Coaching session procedure

Loaded on demand by the [`player-coach`](../SKILL.md) skill once a session
actually begins. The ground rules in the SKILL.md apply throughout.

## Procedure

### Step 1 - Role Detection

Determine which role hat the user is wearing for this session.

**Mandatory first action - read the team index.** Before inferring or asking anything, read the canonical team index at:

```
Core/team-index.md
```

That file is the authoritative source for: who is on the team, what role each person holds, what their scope covers, and the role-default rules for AI agents. Do NOT hardcode role assumptions into this skill or into the output doc - always read the team index and let it define the defaults. If the team index is missing or out of date, ask the user before proceeding.

1. **Read the team index** (above). Apply the default-role rules it specifies for the current user.
2. **If ambiguous after the team index**, infer from the request topic, today's Daily Note (`Operators/{current-operator}/Daily Notes/{year}/{MM}/YYYY-MM-DD.md`, where `{current-operator}` is resolved per the root `CLAUDE.md` rule), and the last 5 commits.
3. **Ask only if still ambiguous** after steps 1–2. If the request spans multiple roles or clearly requires a different hat than the team index's default, use `AskUserQuestion` with a single question: "Which role are we coaching today?" - options pulled from the team index's role list plus "Initiative-specific."
4. **Declare the role** at the top of the output doc. From this moment the coach speaks as a world-class operator in that role and grades the user against that bar - not against where they actually are.

**Critical framing rule:** The coach must hold the user to the bar of their *actual* role as defined in the team index. A world-class CTO is judged on scoping discipline, DoD, architecture quality, team throughput, and technical-customer outcomes - NOT on "should you be writing code" (for a CTO the answer is yes). Do not apply a CEO lens to a CTO session: it produces wrong verdicts like "delegate the architecture work" when the user's actual job *is* the architecture work.

**Cross-functional scope rule:** The team index may describe cross-functional scopes (e.g., "Spencer performs all CEO tasks that are not sales-demo-related"). Respect those boundaries. When coaching a cross-functional task, identify which role owns the decision and which role provides support - do not let the user silently override another person's primary scope via a unilateral directive.

### Step 2 - Coaching Mode Selection

Explicitly select and declare one mode. The mode governs the stance of the whole session.
Do not mix modes.

| Mode | When | Stance |
|---|---|---|
| **TACTICAL** | Today / this week | What to do *now*. Short horizon, execution-grade. |
| **STRATEGIC** | This month / quarter | What bets to be making. Horizon >= 30 days. |
| **STRETCH** | "Am I performing at a world-class level?" | Grade hard against the best operators in the field, not against the user's current habits. |
| **UNBLOCK** | User is stuck | Diagnose root cause of stuckness. Prescribe the smallest next action. |

Declare the mode in the output doc header. Do not mix modes within a single session.

### Step 3 - Scenario Routing

Match the request to a sub-skill and load it. Each sub-skill owns its own phased
procedure (context build → framework application → draft → adversarial review + refine →
forcing question → output doc).

| Trigger phrases | Sub-skill |
|---|---|
| "What should I focus on…" / "Are these my priorities…" / "Review my Daily Note top 3" / "Check my top 3" / "Am I working on the right things" | **`sub-skills/priority-check.md`** ← built |
| *(future)* "Help me decide between X and Y" / "Which of these should I do first?" | `sub-skills/decision-coaching.md` - not yet built |
| *(future)* "I'm stuck on X - why?" / "Diagnose why this isn't moving" | `sub-skills/unblock.md` - not yet built |
| *(future)* "Stretch review my role" / "Am I performing like a world-class {role}?" | `sub-skills/role-stretch.md` - not yet built |

If the request does not match any existing sub-skill, fall back to the `priority-check`
sub-skill framework (it is the most general). Do not invent ad-hoc coaching without a
sub-skill procedure - the adversarial review loop is only guaranteed inside a sub-skill.

After routing, **read the sub-skill file in full** and follow its phased procedure
exactly.

### Step 4 - Output Convention

Every coaching session writes a document to:

```
Operators/{current-operator}/Coaching/YYYY-MM-DD-{scenario}.md
```

Create the `Coaching/` folder on first run if it does not exist. The sub-skill specifies
the exact output structure. Every output doc must contain:

- Frontmatter: `date`, `role`, `mode`, `scenario`
- Context summary (≤5 bullets, work-anchored)
- Verdict / recommendation (post-adversarial-review)
- Adversarial review record (which critics ran, what failed, what was refined, any
  unresolved dissent - never buried)
- Recommended next actions with deadlines
- The one forcing question
- Signal observations (what the coach noticed about the user's pattern this session - accumulates across sessions so future sessions can detect arcs of improvement,
  regression, or stuck patterns)

---
