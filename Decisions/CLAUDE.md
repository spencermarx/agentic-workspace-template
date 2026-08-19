# Decisions

The workspace-level decision register. Area-level decisions live in that area's
own `decisions/` folder, never here.

## Before you write anything here

**You may propose a record. You may not create one without an explicit yes from
the operator in this session.**

Full rule (SSOT): [decision-standards § Capture is human-confirmed](../Workspace/Standards/decision-standards.md#capture-is-human-confirmed)

Proposing is one line: state the claim the record would make, then stop. Do not
draft the file, do not reserve a number, do not create it and offer to delete it
afterwards. Absence of an answer is not an answer.

## Layout

- `README.md`: the register, written for a person. Add the row when a record
  lands.
- `NNNN-<kebab-slug>.md`: one record. Four digits, zero-padded, numbered within
  this folder only.

Decisions about **the template itself** do not belong here. Those live in
`.workspace/decisions/`, which is template-owned and carried by
`./hq upgrade`.

## Rule

The register earns its keep by staying short enough to read end to end. Every
record you add spends that budget, which is why the operator decides what enters
it and you do not.

The [`decision-record`](../.claude/skills/decision-record/SKILL.md) skill owns
the procedure: the significance test, numbering, the four sections, and the
supersession protocol. Do not invent a format or write a record by hand.
