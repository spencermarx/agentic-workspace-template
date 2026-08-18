# Social Image Prompt Build + Review Sub-Skill

Build and validate an image prompt for an organic social post (LinkedIn, Facebook). Runs the three-critic review loop tuned for **editorial photography** that will be **overlaid with text + the workspace logo** in post-processing.

Use this sub-skill when the image will accompany an Unfair Advantages, Builder's Journal, or Product Announcement social post — i.e., posts whose pillar takes the editorial → full overlay path. For Proof Posts, stat-first hooks, or any infographic-style visual, load `infographic.md` instead. For blog images, load `blog.md` instead.

## Inputs (What the Caller Must Provide)

When invoking this sub-skill, the caller must supply:

1. **Post body** — the full text of the social post this image will accompany. The Message Relevance Critic uses this to judge connection.
2. **Concept description** — a 1–3 sentence description of the selected image concept (what the scene is, who/what is in it, the visual idea). Comes from the Image Concept Development section of the post draft file.
3. **Generator** — `openai` (the default for editorial social) or `gemini`. Affects which sub-skill the caller will load to actually generate the image AFTER this loop completes.
4. **Initial draft prompt** — a first-pass prompt the caller has written following Image Generation Guide §8c (Prompt Construction). This sub-skill iterates on the draft — it does not draft from scratch.

## Outputs

After the loop completes, the caller receives one of two outcomes:

### Outcome A: Validated Prompt
A finalized prompt string that has passed all three critics in the same round. The caller proceeds to generate the image using the relevant generator sub-skill (`openai/sub-skills/image-generation.md` or `gemini/sub-skills/image-generation.md`).

### Outcome B: Pivot Recommendation
After 3 failed iterations, the loop returns a structured pivot recommendation containing:
- The criterion(a) that kept failing
- The recurring feedback from the failing critic(s)
- A note that the failure is structural (concept, not prompt) and the caller should rebrainstorm

The caller should then return to concept brainstorming (Image Generation Guide §8) and select a different concept, then re-invoke this sub-skill with the new concept.

## Procedure

### Step 1 — Receive and parse inputs

Hold the post body, concept description, generator, and initial draft prompt in working context. Initialize iteration count to 1.

### Step 2 — Spawn three critic sub-agents in parallel

Use the `Agent` tool with `subagent_type=general-purpose`, sending all three tool calls in a single message so they run concurrently. Each critic receives the post body, the concept description, the current prompt draft, and the critic's exact mandate from the "Critic Mandates" section below.

### Step 3 — Synthesize feedback

Read all three critic responses. The prompt is ready to generate ONLY if all three return PASS in the same round. If any critic returns REVISE, proceed to Step 4.

### Step 4 — Iterate

Rewrite the prompt addressing every REVISE comment. Hold the parts that already passed; change the parts the failing critics flagged. Re-run Step 2 with the revised prompt. Increment iteration count.

### Step 5 — Cap and pivot

**Maximum 3 iterations.** If the prompt still fails any critic on the third iteration, return Outcome B (Pivot Recommendation). Do not iterate a fourth time. A prompt that fails the same critic three times is signaling a structural concept problem, not a writing problem.

### Step 6 — Return

When all three critics PASS in the same round, return Outcome A (the finalized prompt string) to the caller.

## Critic Mandates

Send these EXACT prompts to the three sub-agents. Do not paraphrase, shorten, or merge. The narrow scoping is intentional — each critic must judge ONE criterion only and must NOT comment on the others.

### Critic 1: Scroll-Stop Critic (Social Edition)

```
You are reviewing a draft image prompt for an organic LinkedIn or Facebook post. Your only job is to judge whether the central metaphor or scene — on its own merits — would stop someone scrolling their feed.

Score the described scene 1–5 on visual interest:
- 5: Genuinely arresting. The central metaphor or scene is so striking that a viewer would screenshot or share it. Strong central concept, clean composition, immediate visual hook.
- 4: Distinctive. The central concept is clear and unusual enough to make a viewer pause mid-scroll.
- 3: Competent but forgettable. The central concept is flat or generic. A viewer would scroll past.
- 2: Stock-photo flat. Generic, predictable, "person at desk" energy.
- 1: Boring. No visual tension or interest.

If 4 or 5, return: `PASS — <one-line reason naming what makes the central metaphor strong>`.
If 1–3, return: `REVISE — <specific feedback on what's flat about the CENTRAL CONCEPT itself, with a recommendation to either strengthen the central metaphor or pivot to a different metaphor entirely>`.

CRITICAL RULE — DO NOT recommend bolting on charm elements. Strong metaphors do not need charm add-ons. If the scene feels cold or forgettable, the fix is a stronger central metaphor, NOT garnish (animals, kids, characters, props that aren't already in the concept). Adding an off-concept golden retriever to a weak diptych makes the image cuter but not stronger; it almost always makes the relevance worse by introducing elements unrelated to the post. Never suggest "add a dog/kid/person/object to this panel for charm." If the metaphor is weak, say "the central metaphor is weak — pivot to a stronger metaphor." Let the agent rethink the metaphor itself.

Do NOT comment on relevance to the post or physical accuracy. Judge ONLY visual interest of the central metaphor.

POST BODY:
{post_body}

CONCEPT DESCRIPTION:
{concept_description}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

### Critic 2: Message Relevance Critic (Social Edition)

```
You are reviewing a draft image prompt against the social post it's meant to support. Your only job is to judge whether a viewer will be able to INTUITIVELY connect the concept depicted in the image to the message/concept(s) in the post.

THE BAR IS INTUITIVE CONNECTION, NOT PERFECT METAPHOR DISTILLATION. Abstractions are absolutely fine. Pure metaphors are fine. The metaphor does NOT need to perfectly map every nuance of the post's argument — it just needs to be a concept that, paired with a short overlay text bridging to the post topic, lands intuitively for a scrolling viewer. A previous successful concept (a tiny cat in a cat bed beside a Saint Bernard sprawled around an identical bed) worked even though strictly speaking it expressed "one fits, one doesn't" rather than the post's full argument. That's fine — the viewer intuits the connection.

DO NOT be pedantic about whether the metaphor perfectly captures argument structure (hierarchy vs mutual inadequacy, category errors, etc.). Don't reject concepts for failing to express every facet of the post. The question is simpler: would a normal viewer, glancing at the image with the overlay, intuitively understand that this image is about the post's topic?

PROCEDURE:

1. **Identify the post's central concept(s)** in plain language. (e.g., "different customers need different experiences from one booking page")

2. **Identify the image's central concept** in plain language. (e.g., "one container is the wrong size for two completely different things")

3. **Ask: would a viewer intuitively connect these two concepts?** Imagine a thoughtful but distracted scroll-by reader. Would they see the image, read a short overlay, and think "yeah, that's about [the post's topic]"? Or would they be confused about how the image relates?

If the connection is intuitive, return:
`PASS — Image concept: "<sentence>". Post concept: "<sentence>". Viewer would intuitively connect them.`

If the connection is genuinely unintuitive (the image expresses an entirely different topic, OR the metaphor is so abstract no viewer could decode it, OR the image carries cultural baggage that pulls viewers away from the post topic — e.g., a master-key visual reading as "key fits all locks" / praise when the post is critique), return:
`REVISE — Image concept: "<sentence>". Post concept: "<sentence>". Why a viewer would NOT intuitively connect them: <specific reason>. <Suggested SHAPE of a different metaphor — without prescribing specific props.>`

Reserve REVISE for genuine disconnects, not philosophical objections. If you can imagine a reasonable viewer intuiting the connection in 2 seconds (with the help of a short overlay), it's a PASS. Don't manufacture nuanced reasons to fail concepts that work in practice.

Do NOT comment on visual interest or physical accuracy.

POST BODY:
{post_body}

CONCEPT DESCRIPTION:
{concept_description}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

### Critic 3: Physical Accuracy Critic (Social Edition)

```
You are reviewing a draft image prompt for physical and rendering feasibility. Your only job is to identify anything in the prompt that the AI image model is likely to render incorrectly. The model is an editorial photography image generator (gpt-image-* or gemini-*-flash-image-*); it follows physical priors strongly and will resist requests that violate them.

Check for these failure modes:

1. **Container/contents mismatches.** Does the prompt ask for something to fit INSIDE a container that's smaller than the contents? AI models will scale the container UP to fit, defeating the prompt. (Example failure: "huge dog inside a small cat carrier" — the model will render a larger carrier.) Prefer overflow (object on top of / extending past a smaller surface, body parts visible through existing openings) over compression (object squeezed inside a deformable container).

2. **Scale violations.** Does the prompt ask for an object dramatically smaller or larger than its real-world scale, where the model would default to realistic proportions? Forced perspective and arrangement tricks work; "make this object 50x its normal size" doesn't.

3. **Invented physics or deformation.** Does the prompt require a familiar object to behave in a way no real photograph has shown (compressed, folded, melted, stretched beyond its actual material properties)? The model has no reference for invented deformation.

4. **Anatomical danger zones — apply ZERO TOLERANCE.** AI image models fail anatomy more often than they fail any other element. Every person in the frame is a coin flip on whether the image is shippable. Every multi-person scene compounds the risk. Apply this rigorous check:

   **First question: does the prompt include ANY people?** If yes, ask: *can this metaphor land without people?* If yes, REVISE and recommend removing the people. The default is no people — pure object/scene composition. Single-moment absurdities almost always work better with OBJECTS in the wrong context than with PEOPLE in the wrong context.

   **If people are genuinely required, the prompt MUST include all of these:**
   - Cap the count at 1 person if possible, never more than 3 unless the post specifically requires it
   - Avoid hand-object interactions at the focal point of the image (these are the highest-failure compositions)
   - Required anatomy boilerplate: `physically accurate human anatomy and proportions, naturally proportioned facial features with correctly spaced and aligned eyes, nose, mouth, and ears, correct finger count on visible hands`
   - Explicit expression description ("eyebrows furrowed, mouth slightly open" not "worried expression")
   - Explicit pose description ("right arm extended forward, palm open, fingers slightly curled" not "reaching out")
   - Background people specified as motion-blurred or distant silhouettes, never as detailed faces

   **REVISE the prompt if any of these apply:**
   - The prompt includes people but the metaphor could land without them
   - The prompt has 2+ people in close interaction with both faces detailed
   - The prompt has people performing fiddly hand-object interactions at the focal point
   - The prompt has people but lacks the required anatomy specification boilerplate
   - The prompt uses vague pose/expression language instead of explicit biomechanical/facial description

5. **Text generation requests.** Any expectation that the model will render legible text, labels, signs, screens, or numbers in the image. The image will receive an overlay text in post-processing — the model should NOT be asked to render any text in the scene.

6. **Conflicting style + physics.** "Photorealistic" + "surreal/impossible scene" without naming a known surrealist visual tradition (Magritte, Erik Johansson, concept art, etc.) that gives the model reference. If the concept requires unreality, the prompt should either name a surrealist style OR use forced perspective / overflow / arrangement tricks that don't require inventing physics.

7. **Spatial vs intensity language.** Does the prompt rely on intensity adjectives ("comically tiny," "absurdly huge," "dramatically too small") instead of spatial facts (where things are, how big relative to other things, what extends past what)? Intensity adjectives don't tell the model what to draw — spatial facts do. Flag any prompt that's adjective-heavy and suggest replacing with concrete spatial relationships.

If the prompt is clean of these issues, return: `PASS — <one-line reason>`.
If any issue is present, return: `REVISE — <specific feedback on what won't render correctly and why, plus a suggested rewrite of the problematic phrasing>`.

Do NOT comment on visual interest or message relevance. Those are other critics' jobs. Judge ONLY physical/rendering feasibility.

POST BODY:
{post_body}

CONCEPT DESCRIPTION:
{concept_description}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

## Why Three Critics, Not One

A single generalist reviewer tends to give vague, balanced feedback ("the prompt is good but could be more specific"). Three focused critics each operating on one criterion produce sharper, more actionable feedback. Each critic is forced to commit on their lane and ignore everything else. This catches issues that a generalist would smooth over.

## Why Cap at 3 Iterations

A prompt that fails the same critic three times is not a writing problem. It's a concept problem. The prompt language can be polished indefinitely without fixing a structural issue (e.g., asking the model to render a scale violation it has no training data for, or asking for a connection to a post that the chosen visual fundamentally cannot make). Capping at 3 forces the caller to recognize structural failure and pivot the concept rather than wasting tokens on more rewrites.

## Example Invocation

A caller (e.g., the content-sprint social-drafting workflow) invokes this sub-skill like:

> Run the `image-prompt` skill's social sub-skill (`sub-skills/social.md`) on this prompt before generation:
>
> - Post body: [full text of the social post from the post .md file]
> - Concept: "Two identical small donut cat beds side by side; cat fits perfectly in one, Saint Bernard sprawls across the floor with the other under it"
> - Generator: openai
> - Draft prompt: "Editorial studio photograph on a hardwood floor. Two identical small fluffy gray donut cat beds side by side..."

The sub-skill runs the loop and returns either the validated prompt or a pivot recommendation.
