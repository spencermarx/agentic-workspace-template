# Sub-agent: hypothesis-tester

Use this when the investigation warrants a swarm (SKILL.md → "When to fan out"):
you have two or more _independent_ hypotheses, each needing non-trivial digging in
a separate part of the system. Spawn **one sub-agent per hypothesis** so they run
in parallel, then converge their evidence yourself.

## How to spawn

Use the `Agent` tool. Pick the agent type by what the hypothesis needs:

- **`Explore`** - read-only tracing: reading source, following a value's origin,
  scanning logs/config. Fastest and safest; it returns findings, not edits.
- **`general-purpose`** - when the sub-agent must _run_ something (execute a repro,
  run a query, invoke a target) to get the evidence.

Fill the template below into the `prompt`, one hypothesis per agent. Launch all of
them in a single turn so they run concurrently.

## The prompt template

```
You are testing ONE hypothesis in a larger first-principles investigation. Your
job is to gather EVIDENCE, not to reach a verdict I have to trust - I will judge
the evidence myself. Do not try to make your hypothesis true; the most useful
thing you can return is the observation that KILLS it.

## The overall symptom
<the observed failure, verbatim - error text, actual vs. expected, conditions>

## Your hypothesis (test only this one)
<the single hypothesis this agent owns>

## The falsifier
This hypothesis is FALSE if you observe: <the specific observation that would
disprove it>. Actively try to observe that. If you can't, that's meaningful too.

## Ground rules
- Trust only what you observe firsthand in THIS system - the actual source, the
  real logs, a real reproduction. Not docs, not memory, not analogy.
- Separate evidence (raw observation) from inference (your conclusion) in what you
  report. Label them.
- Change one thing at a time; note every input and result.
- Do not fix anything. Do not touch code paths outside what this hypothesis needs.
- If you find strong evidence for a DIFFERENT cause while looking, report it as a
  side finding - don't chase it.

## Return exactly this
1. **Verdict:** ruled out | supported | inconclusive - and the single observation
   that drove it.
2. **Evidence:** the raw observations (commands run, outputs, source lines with
   file:line, log excerpts). Enough that I can retrace it.
3. **Inferences:** what you concluded from the evidence, kept separate from it.
4. **Confidence & gaps:** what would make you more sure; what you couldn't check.
5. **Side findings:** anything else notable (a different candidate cause, a broken
   assumption), clearly marked as not-your-hypothesis.
```

## Converging the results

When the sub-agents return:

- **Re-judge every verdict against its evidence yourself.** A sub-agent reporting
  "supported" is a lead, not a conclusion - the whole point of the method is that
  self-confirmation is the failure mode. Weigh the raw observations, not the
  label.
- **Look for a hypothesis that uniquely survives** - one supported _and_ whose
  competitors were genuinely ruled out (not merely "inconclusive"). If two survive,
  you haven't converged; design the discriminating observation that splits them.
- **Fold side findings into your hypothesis set.** A sub-agent chasing hypothesis
  A that stumbles on evidence for cause C has just widened the space - add C and,
  if it's plausible, test it.
- **For a high-stakes root cause, spawn an adversarial pass:** one more sub-agent
  whose _only_ job is to refute the leading cause, given the evidence so far.
  Accept the cause only if it survives a genuine attempt to break it.
