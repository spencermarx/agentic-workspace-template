---
name: create-report
description: >-
  Assemble a rich visual HTML report - planned from a markdown record, rendered on this
  skill's shared presentation foundation, delivered as a self-contained local file with an
  optional claude.ai artifact publish. Reach for it WHENEVER work deserves a report,
  briefing, or visual write-up rather than chat prose, and whenever another skill needs its
  results rendered and published. For a document someone reads, not an interactive page or
  app - those go to the Artifact tool with `artifact-design`.
---

# Create report

A report here is one self-contained page, rendered from a markdown record and built on a shared
presentation foundation, so two reports from two different callers read as the same publication.

Subject, vocabulary, ordering and emphasis stay with the caller - a consumer skill knows its
material, and a human asking inline knows theirs. This skill supplies the form.

The units this skill speaks in: **report** (the deliverable) · **record** (its markdown source) ·
**page** (the rendered HTML) · **section** · **entry** (the repeating unit inside a section) ·
**component** · **diagram**.

## Process

### 1. Establish what the report covers and who reads it

A consumer skill arrives holding this already. A human asking inline usually has not said it, so
settle three things in one exchange before planning:

- what the report covers,
- who reads it and what they will do with it,
- where the record and the page go. A consumer skill hands you the directory it opened for its run.
  Otherwise open one and use the absolute path it prints - a hand-built `.scratchpad/…` path
  resolves against whatever the cwd happens to be, and fails silently:

  ```bash
  bash "$(git rev-parse --show-toplevel)/.claude/skills/scratchpad/scripts/scratchpad.sh" new reports '<slug>'
  ```

When nobody is there to answer - a background run, an unattended consumer - take what the caller
gave you, open the destination yourself, and record the assumptions you made rather than stopping.

### 2. Plan the report

Sketch the shape before writing any of it: the sections and their order, the entries in each, the
diagram each entry carries, and what the closing section should leave the reader with. Order and
emphasis follow whatever the caller says matters.

The plan is worth the minute because of the discipline the page holds to - diagrams carry the
weight and prose is sparse. An entry that reaches this stage with no diagram beside it is usually
an entry whose point has not been made visual yet.

### 3. Write the record

Write `record.md` at the destination first, in markdown. The page renders from it, and every claim
on the page traces back to it - that is what makes a report checkable, because a reviewer reads
the record rather than the markup.

Head it with what the report covers, who it is for, the date, and, once the report has been
published, its artifact URL and the favicon it went out under. An unattended run heads it with the
assumptions it had to make, so the reader can overturn them.

### 4. Generate the page

Read [`references/report-format.md`](references/report-format.md) for the page's shape, its
patterns and its tone, and [`references/components.md`](references/components.md) for the markup of
every standard component. [`assets/sample/`](assets/sample) is a worked report - read it to see
the standard end to end, or when a pattern reads better as an example than as a rule.

Write `content.html` at the destination: page content only, the elements that live inside `<body>`.
Both delivered files are derived from it.

### 5. Assemble and deliver

```bash
bash "$(git rev-parse --show-toplevel)/.claude/skills/create-report/scripts/assemble-report.sh" \
  <destination>/content.html <destination>
```

The path comes from git rather than being typed relative to the repo, because a consumer skill's
agent often runs with its working directory pinned somewhere else entirely.

It writes two files and prints both paths: `report.html`, the standalone local document to open and
to hand a human by absolute path, and `report.page.html`, the publish source. It also flags any
subresource that loads from another host, since those render locally and go missing once published.

Then put the publish question to the human: a published artifact is a link they can open anywhere
and pass to someone else, while a local-only report is already a finished report. When nobody is
there to answer - a background run, an unattended consumer - deliver the local report and note in
the record that publishing was not offered.

To publish, pass `report.page.html` to the Artifact tool with a one-sentence description and a
favicon; the file already carries its `<title>`. The page's design arrives from this foundation, so
skip `artifact-design` - publishing here is a delivery step, not a design step. Record the returned
URL **and the favicon** in `record.md`: a reader finds the page by its tab icon, so a revision that
picks a fresh emoji reads to them as a different page.

### 6. Revise

Update the record, regenerate `content.html`, and re-run the script. Republishing from the same
session with the same `file_path` lands on the same URL; from a later session, pass the URL
recorded in `record.md` to the Artifact tool as `url`, together with the favicon recorded beside
it, so the link a reader already holds keeps working and the tab icon they find it by does not
change.

## Reference files

| File                                                                           | Read it when                                                                       |
| ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| [`references/report-format.md`](references/report-format.md)                   | generating a page - scaffold, layout and diagram patterns, style and tone          |
| [`references/components.md`](references/components.md)                         | writing markup - the catalogue of standard components and their accessibility      |
| [`references/integrating-a-consumer.md`](references/integrating-a-consumer.md) | wiring a new consumer skill to call this one, or giving it components of its own   |
| [`assets/report-base.css`](assets/report-base.css)                             | a component needs a token, or a consumer's own CSS has to match the foundation     |
| [`assets/sample/`](assets/sample)                                             | the standard is easier to see than to describe - a record and its page, end to end |
