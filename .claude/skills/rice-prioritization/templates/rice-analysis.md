---
date: <YYYY-MM-DD>
type: type/analysis
status: status/draft
project: <venture>
attendees: [<person/...>]
tags: [type/analysis, status/draft, venture/<venture>, topic/prioritization]
---

# RICE Prioritization - <subject>

## Round constants

- **Goal/metric:** <the single goal candidates are scored against>
- **Reach time window:** <one window for the whole round, e.g. per quarter>
- **Mode:** <Autonomous | Facilitated | Hybrid>
- **Candidates scored:** <n>
- **Date / participants:** <date>, <who scored>

## Calibration anchors

<The ~3 shipped features used to anchor the scales, with their agreed Impact and
Confidence. State them so the frame is auditable.>

| Anchor feature | Impact | Confidence | Note |
|---|---|---|---|
| <feature> | <3/2/1/0.5/0.25> | <100/80/50%> | <why> |

## Ranking

Scores are relative, not absolute. Treat anything in the same tie group as too
close to call on score alone. Computed by `rice_score.py`.

| Rank | Idea | Reach | Impact | Confidence | Effort | RICE | Tie | Evidence / source |
|---|---|---|---|---|---|---|---|---|
| 1 | <name> | <n> | <m> | <%> | <pm> | <score> | <-/group> | <reach data source; evidence flag; NEEDS-HUMAN markers> |

## Sensitivity and ties

<What would change the ranking. For each near-tie or fragile pair, state the
confidence (or other) change that would flip the order, from the script's
sensitivity output. Flag any order that is flippable by confidence alone as
"validate before committing.">

- <pair>: gap <x>; <lower item> overtakes at confidence <y> (currently <z>) -> <robust | fragile, validate>.

## Quick wins by effort

<Group candidates by effort so low-effort, decent-score items are visible.>

- **Quick wins (<= 1 person-month):** <names>
- **Medium (1-2):** <names>
- **Large (3+):** <names>

## Adversarial challenge record

<What the challenge pass disputed and what changed. Never bury unresolved
dissent.>

- **Reach Inflator:** <rows challenged, outcome>
- **Confidence Optimist:** <rows challenged, outcome>
- **Effort Underestimator:** <rows challenged, outcome>
- **Scores revised:** <yes/no; if yes, recomputed>

## Assumptions and open questions

- **Assumptions:** <key assumptions, especially behind low-confidence items>
- **NEEDS-HUMAN (autonomous mode):** <effort and strategic-impact numbers awaiting a human>
- **Open questions:** <what to validate before committing>

## Operator decision required

<Surface the ranking and a recommendation. Do not decide. Name the strategic
overrides, dependencies, and table-stakes that could reorder the top items.>

- **Recommended order:** <top 3-5, with the one-line why>
- **Where RICE and strategy diverge:** <any item the score ranks differently than strategy would>
- **Decision owed:** <what the operators need to choose>
