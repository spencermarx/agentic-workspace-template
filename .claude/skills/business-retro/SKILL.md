---
name: business-retro
description: >
  Weekly business health synthesis pulled from real work output - the task
  history - rather than manual summaries. Computes delivery rate, blocker patterns,
  agent-specific highlights anchored to specific tasks, slip analysis, and a focus
  score. Produces a formatted weekly review document written to
  the workspace/the operator Personal Workspace/Weekly Reviews/. Run every Friday. Based on
  gstack's /retro, adapted from git-history to task history.
---
<!-- Vendored from https://github.com/spencermarx/wrkbelt-agent-team (.claude/skills/business-retro/SKILL.md @ 496d37273aca); adapted for this repo (the four hardcoded task-source REST endpoints replaced by a pluggable task source read from .workspace/workspace.json). See [ADR 0002](../../../Decisions/0002-vendor-third-party-skills-as-plain-files.md). -->


# Business Retro

A weekly retrospective synthesized from real task data - not a manual summary.
Based on Garry Tan's [gstack `/retro`](https://github.com/garrytan/gstack), adapted from
git-commit history to task history as the source of truth.

**Core principle from gstack:** Specificity over generality. "CMO shipped 3 LinkedIn posts
this week, including the attribution one that drove 4 inbound replies" beats "great week
everyone." Work recognition must be anchored to actual work artifacts.

## When to Use

- Every Friday as a standing ritual (CEO triggers)
- When a weekly summary is needed for board review
- After a sprint or milestone to synthesize what shipped and what slipped

## When NOT to Use

- Mid-week - this is a weekly synthesis, not a daily standup
- For individual task post-mortems - handle those at the issue level
- As a planning tool - this is backward-looking; use `ceo-review` for forward planning

## Agents

**Primary:** CEO (triggers)
**Secondary:** Any agent assisting with data pull

---

## Procedure

### Step 1: pull the task data

Use the configured task source to pull the past 7 days of task activity. The reporting week runs
Friday-to-Friday. Collect:

**Completed tasks (status = done, completedAt in past 7 days):**
```bash
```

**New tasks created this week:**
```bash
```

For each task, record: title, assignee agent, project/goal, completion date, and (for
blocked tasks) the blocker reason from the most recent comment.

---

### Step 2 - Compute Metrics

**Delivery Rate:**
`Tasks completed this week / Tasks created this week × 100`

A delivery rate above 80% is healthy. Below 60% indicates either over-commitment or
execution friction.

**Blocker Pattern Analysis:**
Group blocked tasks by root cause. Common categories:
- Waiting on human input (board decision, approval, credentials)
- Waiting on another agent (dependency)
- Technical/tooling blocker
- Unclear scope or missing spec

If more than 2 tasks are blocked for the same reason, that's a systemic issue, not a
one-off.

**Focus Score:**
`Tasks on high/critical priority / Total tasks worked × 100`

A score above 70% means the team spent most of their capacity on priority work.
Below 50% means low-priority tasks absorbed disproportionate attention - investigate why.

---

### Step 3 - Agent-Specific Highlights

For each agent that completed work this week, write **one specific, work-anchored highlight.**
The highlight must reference a specific task by name or identifier - not a generic summary.

Format:
> "[Agent name] - [specific accomplishment tied to a named task or deliverable]. [Impact if measurable.]"

Examples of the right specificity level:
- "CMO - Launched the 3-post LinkedIn attribution series (WRK-44, WRK-45, WRK-46); the March 18 post drove 4 inbound connection requests in 48 hours."
- "Founding Engineer - Shipped the Slack skill (WRK-38) and the Google Sheets integration (WRK-39); both are now available to all agents."
- "CEO - Completed the gstack integration proposal (WRK-56) and green-lit 5 new skills for engineering."

Do not write generic highlights ("had a productive week," "made good progress").
If an agent completed no tasks, note that explicitly - don't omit them.

---

### Step 4 - Slip Analysis

For each slipped task (in_progress or todo for >5 days), diagnose the root cause:

| Cause | Definition |
|---|---|
| **Scope creep** | Task grew beyond original spec mid-execution |
| **Dependency** | Blocked on another task, agent, or external input |
| **Execution** | Task was picked up but not completed - agent capacity or priority issue |
| **Stale** | Task was created but never started - backlog hygiene issue |

For each slipped task, write one sentence: what it is, how long it's been open, and the
diagnosed root cause. Flag tasks open >10 days for explicit board attention.

---

### Step 5 - Write the Weekly Review Document

Write the output to:
`the workspace/the operator Personal Workspace/Weekly Reviews/[YYYY-MM-DD]-weekly-review.md`

Use this format:

```markdown
# Weekly Business Review - [Week ending YYYY-MM-DD]

**Generated:** [date]
**Data window:** [start date] → [end date]

---

## At a Glance

| Metric | This Week |
|---|---|
| Tasks completed | X |
| Tasks created | X |
| Delivery rate | X% |
| Tasks blocked | X |
| Focus score | X% |

---

## Agent Highlights

- **CEO:** [specific work-anchored highlight]
- **CMO:** [specific work-anchored highlight]
- **Founding Engineer:** [specific work-anchored highlight]
- *(add others as applicable)*

---

## What Shipped

[Bulleted list of completed tasks, grouped by project/goal if applicable.
Include task identifier and one-line description for each.]

---

## What Slipped

[Bulleted list of slipped tasks with root cause diagnosis.
Flag >10-day items explicitly.]

---

## Blocker Patterns

[Summary of blocked tasks grouped by root cause. Flag systemic patterns.
Include who needs to act to unblock each.]

---

## Focus Analysis

[Delivery rate commentary: was the team focused on priority work?
If focus score is low, identify what pulled attention away.]

---

## Open Question for Next Week

[Single most important unresolved question heading into the following week.
Not a laundry list - the one question that most determines whether next week
is a good week or not.]
```

---

### Step 6 - Notify

After writing the document:
- Post a Slack message to the team channel (or DM the operator) with the at-a-glance table
  and the open question for next week. Use the `slack` skill.
- If a retro item in the tracker exists for the week, post a comment with a link to the document.

---

## Key Principle: Work-Anchored Specificity

Every item in this retro must be traceable to a specific the task by title or identifier.
If it can't be traced to actual work, it doesn't belong in the retro. Vague summaries
("the team made good progress on marketing") are not acceptable.
