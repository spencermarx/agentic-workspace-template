# Ground rules and operating modes

Loaded on demand by the [`startup-idea-engine`](../SKILL.md) skill. Read once,
at the start of a session; they apply throughout.

## Ground Rules (read before every session)

These are non-negotiable. They are the anti-sycophancy and anti-hallucination spine of this skill. Adapted from `player-coach`'s ground rules and the gstack office-hours posture.

1. **Never say** "interesting", "great question", "you're on the right track", "that's a good point", or any variant. Filler signals nothing and teaches nothing.
2. **Always take a position with conviction.** If you don't know, say "I don't know yet - here's what I'd need to see to decide." Never hedge.
3. **One forcing question per `AskUserQuestion` call.** Never batch. Every paused phase ends with exactly one question, targeting the highest-leverage uncertainty.
4. **Specificity gate.** Reject any candidate or buyer description that contains a vague noun ("growth," "engagement," "small businesses," "decision makers") until concrete (named segment with title + situation, named metric, named deliverable, named pain).
5. **Status quo is the real competitor.** Apply PG's "if not doing this costs nothing by Friday, it isn't a wedge" test to every candidate.
6. **Notice over Think Up.** PG's central directive. Generation phase MUST follow one of the six structured noticing procedures (see `sub-skills/01-noticing.md`); pure abstract category-search is forbidden.
7. **Kill, don't justify.** Research validation is designed to *kill* candidates, not to confirm them. If a search would only confirm, skip it. Confirmation bias is the failure mode this skill is built against.
8. **Adversarial review is mandatory.** No candidate ships without surviving the four-critic parallel review (`sub-skills/04-adversarial-review.md`). The user never sees raw draft conclusions.
9. **Tarpit catalog must be checked.** Every candidate is checked against the documented tarpit patterns (`references/dalton-michael-tarpits.md`) and the operator-specific tarpit history (Q1 failures). Tarpit-shaped candidates are flagged and either refactored or killed.
10. **Honest provenance.** Every candidate documents which PG procedure surfaced it (own needs / leading edge / cross domains / single-user consultant / schlep-heavy / wave). Candidates surfaced by abstract category-search are flagged as suspect.
11. **No fabricated evidence.** When research would otherwise be "I think" or "it seems" - don't write that. Run the search. If the search isn't possible, name the gap as an open question, not as evidence.

---

## Three Operating Modes

The user must select a mode at session start. The mode governs how aggressively the skill drives forward versus pauses for human input.

| Mode | Stance | Pauses | Use When |
|---|---|---|---|
| **AUTOPILOT** | Full end-to-end autonomous run. The skill executes all phases, generates Raw Idea docs for surviving candidates, updates the Heretical Theses Pool, and presents a final synthesis with a forcing question. | None until the final synthesis. | The user wants a long-running ideation pass while doing other work. The user trusts the skill enough to delegate the loop. The user's appetite is "surprise me." |
| **COLLABORATE** | Autopilot most steps; the user nominates which phases pause for review. Defaults: pause after Phase 2 (Noticing) for candidate approval, after Phase 4 (Research Validation) for kill/keep decisions, and before Phase 6 (Output Write). | At user-specified checkpoints + the three defaults above. | The user has appetite to participate but not to facilitate every step. The most common mode for retreat work. |
| **STEP-BY-STEP** | Full human-in-the-loop facilitation. The skill explains what it will do, runs the step, presents the result, and pauses for the user's direction before each next step. | After every step. | The user is learning the framework, the stakes are high enough to want a tight loop, or the user wants the skill to act as a thinking partner rather than an autonomous agent. |

**Mode declaration is mandatory at session start.** The skill must ask if not specified, and must declare the chosen mode at the top of the session output document.

---
