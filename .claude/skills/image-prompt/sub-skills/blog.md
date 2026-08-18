# Blog Image Prompt Build + Review Sub-Skill

Build and validate an image prompt for a blog post (hero or inline). Runs the three-critic review loop tuned for **editorial photography that will be image-cleaned, NOT overlaid** with text or logo. Blog images are unbranded editorial by default.

Use this sub-skill for:
- **Blog hero images** (top of post, becomes the Sanity `mainImage`)
- **Blog inline images** (placed mid-body to break text and reinforce a specific section)

For social images, load `social.md` instead. For infographics / data viz, load `infographic.md` instead.

## How blog differs from social

- **No text overlay.** The image must communicate visually without any added text layer in post-processing. The Scroll-Stop Critic and Message Relevance Critic both judge the visual on its own - there is no overlay safety net.
- **Editorial, unbranded.** The the workspace logo is NOT stamped on blog images. Do not request logo space in the prompt.
- **Inline images relate to a specific section,** not the whole post. When validating an inline image prompt, the relevance critic compares the visual to the surrounding section context, not the entire blog body.

## Inputs (What the Caller Must Provide)

1. **Blog body or section context** - - For a hero image: the full blog body, or at minimum the title + opening (Hook + Agitate sections)
   - For an inline image: the surrounding section text (the H2 the image sits under, and the paragraphs immediately before and after the image's placement)
2. **Concept description** - a 1–3 sentence description of what the scene depicts. For inline images, this comes from the inline image comment in the blog draft (`<!-- INLINE IMAGE: ... -->`).
3. **Image type** - `hero` or `inline`. Affects which context the relevance critic uses.
4. **Generator** - `openai` (the default for editorial blog) or `gemini`.
5. **Initial draft prompt** - a first-pass prompt the caller has written.

## Outputs

After the loop completes, the caller receives one of two outcomes:

### Outcome A: Validated Prompt
A finalized prompt string that has passed all three critics in the same round. The caller proceeds to generate the image using the relevant generator sub-skill, then runs the result through `image-clean` (per `blog-drafting` sub-skill).

### Outcome B: Pivot Recommendation
After 3 failed iterations, the loop returns a structured pivot recommendation. The caller should rebrainstorm the concept (or rewrite the inline image comment in the blog draft) and re-invoke this sub-skill.

## Procedure

### Step 1 - Receive and parse inputs

Hold the blog body (or section context), concept description, image type, generator, and initial draft prompt in working context. Initialize iteration count to 1.

### Step 2 - Spawn three critic sub-agents in parallel

Use the `Agent` tool with `subagent_type=general-purpose`, sending all three tool calls in a single message. Each critic receives the relevant context, the concept description, the current prompt draft, and the critic's exact mandate from the "Critic Mandates" section below.

For **inline images**, pass only the surrounding section context to the relevance critic, not the entire blog body. For **hero images**, pass the full blog body (or at minimum the title + Hook + Agitate sections).

### Step 3 - Synthesize feedback

Read all three critic responses. The prompt is ready to generate ONLY if all three return PASS in the same round. If any critic returns REVISE, proceed to Step 4.

### Step 4 - Iterate

Rewrite the prompt addressing every REVISE comment. Re-run Step 2 with the revised prompt. Increment iteration count.

### Step 5 - Cap and pivot

**Maximum 3 iterations.** If the prompt still fails any critic on the third iteration, return Outcome B (Pivot Recommendation). For inline images, the pivot may also include rewriting the inline image comment in the blog draft.

### Step 6 - Return

When all three critics PASS in the same round, return Outcome A (the finalized prompt string).

## Critic Mandates

Send these EXACT prompts to the three sub-agents.

### Critic 1: Scroll-Stop Critic (Blog Edition)

```
You are reviewing a draft image prompt for a blog post image (hero or inline). Your only job is to judge whether the central metaphor or scene - on its own merits - is visually compelling enough to enrich the reading experience and survive without any text overlay.

Score the central concept 1–5 on visual interest:
- 5: Magazine-quality. The metaphor or scene is so striking that a reader pauses mid-scroll. Strong central concept, intentional composition, immediate visual hook.
- 4: Distinctive. The central concept is clearly more thoughtful than stock photography.
- 3: Competent but generic. Standard B2B blog header energy.
- 2: Stock-photo flat.
- 1: Boring or visually inert.

Important: blog images receive NO text overlay. The scene must be self-explanatory through its central concept alone. Avoid concepts that depend on a caption to make sense.

If 4 or 5, return: `PASS - <one-line reason naming what makes the central concept strong>`.
If 1–3, return: `REVISE - <specific feedback on what's flat about the CENTRAL CONCEPT itself, with a recommendation to either strengthen the core metaphor or pivot to a different metaphor entirely>`.

CRITICAL RULE - DO NOT recommend bolting on charm elements (animals, kids, characters, props) that aren't already in the concept. Strong metaphors do not need garnish. If the central concept is weak, the fix is a stronger central concept, NOT add-ons. Adding an off-concept dog to a weak diptych makes the image cuter but not stronger; it almost always makes the relevance worse by introducing elements that don't relate to the post's message. If the metaphor is weak, say "the central metaphor is weak - pivot to a stronger metaphor." Let the agent rethink the metaphor itself.

Do NOT comment on relevance or physical accuracy. Judge ONLY visual interest of the central concept.

CONTEXT (BLOG BODY OR SURROUNDING SECTION):
{context}

CONCEPT DESCRIPTION:
{concept_description}

IMAGE TYPE:
{image_type}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

### Critic 2: Message Relevance Critic (Blog Edition)

```
You are reviewing a draft image prompt against the blog post (or section) it's meant to support. Your only job is to judge whether the metaphor or scene chosen will visually express the content's CORE MESSAGE clearly enough that a reader can decode it with no overlay text and no caption.

The metaphor does NOT need to literally depict elements from the post. It can be fully abstract or analogical. Pure metaphor is fine if it distills the core message into something a reader can decode in 2 seconds. Frankenstein metaphors (charming but disconnected, or where the visual elements don't add up to ONE legible idea) are not.

PROCEDURE - run all three steps before responding:

1. **Distill the content into one core-message sentence.** For a HERO image, this is the blog's overall thesis. For an INLINE image, this is the surrounding section's specific point. Be specific.

2. **Run the cover test.** Imagine the image with NO caption and NO surrounding text. What core message would a reader with no other context derive from the image alone?

3. **Compare the two.** Does the cover-test reading match the content's core message?

If they match, return:
`PASS - Core message: "<sentence>". Cover-test reading: "<sentence>". Match.`

If they don't match, return:
`REVISE - Core message: "<sentence>". Cover-test reading: "<sentence>". Gap: <what's missing or mismatched>. <Suggestion of the SHAPE of metaphor that would actually distill the core message - but do NOT prescribe specific characters or props; suggest the shape and let the agent pick the instantiation.>`

Failure modes that should trigger REVISE:
- Cover-test reading is vague rather than a specific message
- Cover-test reading expresses a DIFFERENT idea than the content
- Cover-test reading requires the reader to read the surrounding text to make any sense
- Visual elements don't add up to ONE legible idea (Frankenstein metaphor)

Do NOT comment on visual interest or physical accuracy. Judge ONLY whether the metaphor distills the core message.

CONTEXT (BLOG BODY OR SURROUNDING SECTION):
{context}

CONCEPT DESCRIPTION:
{concept_description}

IMAGE TYPE:
{image_type}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

### Critic 3: Physical Accuracy Critic (Blog Edition)

```
You are reviewing a draft image prompt for physical and rendering feasibility. Your only job is to identify anything in the prompt that the AI image model is likely to render incorrectly. The model is an editorial photography image generator; it follows physical priors strongly and will resist requests that violate them.

Check for these failure modes:

1. **Container/contents mismatches.** Does the prompt ask for something to fit INSIDE a container that's smaller than the contents? AI models will scale the container UP to fit, defeating the prompt. Prefer overflow over compression.

2. **Scale violations.** Does the prompt ask for an object dramatically smaller or larger than its real-world scale?

3. **Invented physics or deformation.** Does the prompt require a familiar object to behave in a way no real photograph has shown?

4. **Anatomical danger zones.** Multiple complex hand poses, crowds of 4+ detailed faces, unusual joint positions without biomechanical detail.

5. **Text generation requests.** Any expectation that the model will render legible text, labels, signs, screens, or numbers in the image. Blog images are unbranded editorial - the model should NOT render any text in the scene. Even subtle text on signs or screens will garble.

6. **Conflicting style + physics.** "Photorealistic" + "surreal/impossible scene" without naming a known surrealist visual tradition that gives the model reference.

7. **Spatial vs intensity language.** Does the prompt rely on intensity adjectives ("comically tiny," "absurdly huge") instead of spatial facts (where things are, how big relative to other things, what extends past what)? Flag and suggest replacing with concrete spatial relationships.

If the prompt is clean of these issues, return: `PASS - <one-line reason>`.
If any issue is present, return: `REVISE - <specific feedback on what won't render correctly and why, plus a suggested rewrite>`.

Do NOT comment on visual interest or message relevance. Judge ONLY physical/rendering feasibility.

CONTEXT (BLOG BODY OR SURROUNDING SECTION):
{context}

CONCEPT DESCRIPTION:
{concept_description}

IMAGE TYPE:
{image_type}

CURRENT PROMPT DRAFT:
{prompt_draft}
```

## Why Three Critics, Not One

A single generalist reviewer tends to give vague, balanced feedback. Three focused critics produce sharper, more actionable feedback because each is forced to commit on its lane and ignore everything else.

## Why Cap at 3 Iterations

A prompt that fails the same critic three times is signaling a structural concept problem, not a writing problem. Capping at 3 forces the caller to recognize structural failure and pivot the concept rather than wasting tokens on more rewrites.

## Example Invocation

> Run the `image-prompt` skill's blog sub-skill (`sub-skills/blog.md`) on this prompt before generation:
>
> - Image type: inline
> - Surrounding section context: [paragraph(s) immediately around the inline image placement, including the H2]
> - Concept: "An overhead shot of a contractor's desk with three different invoice templates side by side, two crumpled and one pristine"
> - Generator: openai
> - Draft prompt: "Editorial overhead photograph, contractor's wooden desk, warm overhead lamp light..."

The sub-skill runs the loop and returns either the validated prompt or a pivot recommendation.
