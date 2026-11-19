# Thought, Heart, and Activity — Person lesson authoring standard

**Status:** Internal editorial policy, adopted for future course Person sections November 19, 2026. **Scope:** Every numbered lesson's **For the Person With FND** section. **Project-lead approval controls public wording.** This standard does not authorize changes to already human-authored sections without separate approval.

## Why we use three questions

The questions are not a quiz appended to the lesson. They are a short bridge from **understanding the lesson**, to **recognizing why it matters personally**, to **choosing a manageable way to use the insight**. They can support readiness for appropriate treatment and rehabilitation, but do not constitute CBT, prescribed therapy, or a test of whether a person wants to recover.

- **Thought — “Something to think about”:** Ask a reader to use the lesson's *new central idea* in a specific everyday example. Distinguish what happened from an assumption, prediction or interpretation where relevant. Avoid rote fact recall, and do not assume a specific symptom mechanism applies to that reader.
- **Heart — “How might that feel?”:** Invite recognition of one feeling, hope, value, loss, relationship or need connected to the idea. Leave room for mixed or absent feelings. Asking “how would you feel if recovery happened?” in multiple lessons is weaker than helping readers notice what matters to them in their current circumstances. Never prescribe a “correct” feeling.
- **Activity — “One small step”:** Offer **one** optional, attainable action or thought exercise that follows logically from Thought and Heart. The action may be done mentally, by brief note, by communication, or with trusted help. It should not require journaling, a clinician appointment or symptom improvement. It may be useful simply to *notice*, *prepare*, *ask for support*, or *make a small, safe adjustment*.

The intended progression across lessons is **recognize → relate → experiment gently or choose → review**. The prompts should help readers become more active participants in their lives and care **without placing responsibility for involuntary symptoms on them**.

## When a CBT-informed pattern fits

Later lessons can teach the familiar **situation → thought or expectation → feeling → action** relationship, followed by asking what another reasonable response might be. This is not the claim that thoughts *cause* FND symptoms. A realistic disappointment, legitimate hazard, accessibility barrier or symptom should not be reframed as a “faulty thought” merely to make the exercise work.

A safe, low-pressure Activity can:

1. Pick an ordinary, non-dangerous situation (real, fictional, or imagined) in which something felt difficult.
2. Notice one thought or expectation and one feeling, if either is recognizable; **“I don't know” is valid**.
3. Consider whether there is another possible interpretation *or* a practical support that could change what happens next.
4. Choose a very small optional response, **without deliberately provoking symptoms**, and later notice whether it helped, did not help, or was too demanding.

Do not turn the course into self-directed exposure therapy, trauma processing, seizure-interruption instructions, forced positive thinking, or symptom monitoring that grows burdensome. Do not ask readers to test unsafe walking, ignore medical advice, withdraw communication or mobility aids, or repeat activities that pose injury risk. Reflective action is not proof of rehabilitation or of a psychological cause.

## Quality review for each lesson

Before submitting a Person section for project-lead approval:

1. State the **one central thing** the reader should learn. Would they recognize it through the story without the reflection prompts?
2. Read the preceding lessons' entries in the [course-wide inventory](thought-heart-activity-inventory.md). Compare especially the previous three to five lessons and every lesson in the current module.
3. Check Thought applies *this* lesson's point, Heart connects the point to something personally meaningful rather than guessing a required emotion, and Activity follows naturally from both.
4. Look for repetitive tasks (another list of symptoms, another generic question for a clinician, another hypothetical “how might it feel to improve”). Repetition is acceptable only when the learner gains a genuinely new skill.
5. Use accessible language for roughly age fourteen, short instructions, and one small task. Respect limited memory, capacity, mobility, speech, sensory access and variable symptoms. “You can think about it without writing it down” is often helpful.
6. Preserve the reader's choice. The person can decline, need help, postpone, or have no similar experience. The prompts are optional, not homework, compliance checks or a substitute for clinical care.
7. Have the project lead approve all three **together**, considering the module's teaching progression. Then update the public lesson and refresh the course-wide inventory.

## Maintenance and automated checking

**Canonical source:** The live Person sections are the authority; the inventory is a reproducible record. Its auto-generated region copies the exact prompts, including legacy \`Questions\` labels and empty/missing sections.

After **every** course Person-section change or newly approved lesson:

1. Update the public lesson only with authorized prose.
2. Run \`python tools/course/build_thought_heart_activity_inventory.py\` from a checkout that contains the **latest approved base branch and the proposed lesson changes**.
3. Commit the regenerated [inventory](thought-heart-activity-inventory.md) in the *same PR/commit series* as the lesson. If prompts are deferred by an explicit handoff decision, keep their absence visible and recorded.
4. Run \`python tools/course/build_thought_heart_activity_inventory.py --check\` before handoff or merge. The read-only CI check can use this command on the PR's merged checkout. A regenerated inventory is **not** evidence of human authorship, clinical validation, or publication readiness.

The generator does not edit lessons. It does not automatically invent questions, judge educational quality or infer which generated drafts have been approved.

## Module 12 — special handoff (November 19, 2026)

- **Lesson 36, Nadia:** Understand that a *treatment target* is distinct from an explanation of original causation. Readers may consider what they would want help with, not whether their symptoms are psychologically caused.
- **Lesson 37, Graham:** Consider what a particular treatment would involve, what research can and cannot promise, and what meaningful progress would be in one's actual life. Respect safety and different care needs.
- **Lesson 38, Callum:** Understand continuing consent and collaboration inside treatment. The optional Activity can invite a CBT-informed recognition of an ordinary situation, thought, feeling and possible response, with no requirement to perform a feared action or give up communication support.

**Editorial hold:** No Thought, Heart or Activity prompts have yet been approved for the new Module 12 Person stories. Review the **nine proposed items together** after Lesson 38 Person prose is approved; update all three lessons only after project-lead decisions. Do not resurrect unapproved legacy Lesson 38 questions.
