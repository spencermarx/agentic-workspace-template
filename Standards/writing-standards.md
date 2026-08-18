# Writing standards

Everything a human will read. Each `##` below is a standard, stated once. The
`.claude/rules/writing/` pointers route these to the files they govern.

## House voice

Seven rules, applied to every note, document, message, and generated artifact.

1. **No em dashes.** Use a period, a comma, a colon, or a pair of hyphens. Em
   dashes are the single most reliable tell that text was machine-written.
2. **No emojis**, unless quoting a source verbatim. Where an emoji was carrying
   a visual affordance in a heading, use an Obsidian callout instead:
   `> [!tip]`, `> [!warning]`, `> [!note]`. The affordance survives; the
   character does not enter the file.
3. **No false precision.** Use a range when the underlying uncertainty is real.
   "Roughly 40 to 60 hours" beats "52 hours" when you do not know.
4. **Distinguish facts from observations from open questions.** A fact is
   something you can point at. An observation is your reading of it. An open
   question is neither. Label them when they appear together.
5. **Cite inline** for any numeric claim or named comparable, as a markdown
   link. A number without a source is a rumor.
6. **Tables for comparisons.** Three or more things compared across two or more
   dimensions is a table, not prose.
7. **Never decide for the principal.** Present the options, give a
   recommendation, and leave the decision where it belongs.

## Plain language for outbound text

Anything a client, prospect, or partner will read is written in short,
unambiguous sentences: one idea per sentence, concrete nouns, active voice, and
no term that has not been defined either in `CONTEXT.md` or in the document
itself.

The test is not whether it reads well to you. It is whether a reader who has
none of your context can act on it without asking a clarifying question.

## AI tells

Marketing and published copy is checked for the phrasings that mark machine
authorship and cost credibility:

- Openers that restate the prompt ("In today's fast-paced world...").
- Tricolon padding, where three adjectives do the work of one.
- "It's not just X, it's Y" and its variants.
- Hedged superlatives ("arguably one of the most...").
- Section headings that promise a payoff the section does not deliver.
- Uniform paragraph length across an entire piece.

The `seven-copy-critics` skill is the systematic version of this check.

## Completion criteria

Every instruction written for an agent ends on a condition that can be observed
to be true or false. "Review the document" cannot fail; "list every claim in the
document that has no inline citation" can.

This applies to skills, to `CLAUDE.md` sections, and to any task handed to a
subagent.
