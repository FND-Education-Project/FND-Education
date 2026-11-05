# Module 7 content-seeding and overlap review — October 28, 2026

**Branch/PR:** [PR #198](https://github.com/FND-Education-Project/FND-Education/pull/198). **Status:** Working draft for project-lead human authoring, not Audit 1, Audit 2 or independent clinical review.

## Canonical curriculum decision

Merged [PR #191](https://github.com/FND-Education-Project/FND-Education/pull/191) established **one uniform current course** and removed the 34 superseded lessons. Do **not** revive a previous edition, archive, duplicate reading course, `/course/v2/` scheme or progress-preservation migration. The October 28 snapshot added a fifth Module 7 lesson. The October 30 approved curriculum direction now adds a sixth lesson for cognitive difficulties before emotion; current six-lesson sequence:

| Module-local ID | Overall lesson label | Current page | Status |
|---|---|---|---|
| m7-1 | 18 | The Predictive Brain | Generated seed with Person, Supporter and Clinician additions |
| m7-2 | 19 | Interoception, Proprioception, and Outside Senses | Generated seed with Person, Supporter and Clinician additions |
| m7-3 | 20 | Salience, Arousal, and Feedback Loops | Generated seed with Person, Supporter and Clinician additions |
| m7-4 | 21 | Cognitive Difficulties in FND | **New** seeded Person, Supporter and Clinician drafts; no human approval yet |
| m7-5 | 22 | Emotional Regulation and Involuntary Symptoms | **Moved** generated working seed; expanded Person draft in editorial conversation, not yet approved |
| m7-6 | 23 | Agency, Learning, and Your Own Adaptations | **Moved** working seed, old source path deleted; no legacy copy |

The canonical site has **19 modules, 59 lessons**. Overall display labels in Modules 8–10 shift by two compared with the original 57-lesson baseline; module-local IDs outside Module 7 do not. Site generator and tests updated. No cloud Worker/D1 changes or migrations are authorized by this content PR. The separate draft account PR #154 must use the revised **59**-lesson manifest and Module 7 allowlist of **6** before deployment; only testing records exist.

## Distinct learning outcomes and overlap boundaries

| Lesson | The one question it answers | Deliberately leave to the next lesson or elsewhere |
|---|---|---|
| 18 — Prediction | How does normal perception/action anticipate and correct incoming evidence? | Do not teach body sensing in depth, label deliberate thoughts as “priors,” or claim a personal Bayesian FND cause. |
| 19 — Sensing | Where do internal, position and outside signals come from, and how do report, measurement and cause differ? | Do not turn this into a treatment guide for all sensations or an arousal lesson. |
| 20 — Salience/arousal | Which information becomes prioritized, and how can body readiness and experiences influence one another? | Do not equate arousal with emotion or teach conflict regulation here. |
| 21 — Cognition and brief dissociation | Which parts of memory, thinking and language access may be difficult alongside FND, and what distinguishes an FCD diagnosis or dissociative experience? | Emotion-conversation interaction belongs in Lesson 22, and a full clinical dissociation guide belongs in the Reference Library. |
| 22 — Emotion | What is emotional regulation, what does FND group research actually support, and why doesn't symptom timing during conflict prove deliberate avoidance? | Detailed compromise, shared conflict negotiations, couple/family therapy and ongoing relationship strategies belong in **Module 14**. Do not claim one emotion–motor mechanism. |
| 23 — Agency | How do intention, feeling in control, observed ability, and responsibility differ—and what is a careful personal adaptation? | Do not recapitulate each preceding concept in depth or imply individual symptom control on command. |

**Module 6 boundary:** Attention allocation, automatic motor control and task-directed external focus were taught in Lessons 15–17. Module 7 explains anticipation, body signals, prioritization, regulation and agency; avoid repeating the photo/envelope/bookshelf patient scenario as the core case.

**Module 14 boundary:** Shared trust and equal consideration, discussing complicated topics in smaller parts over time, making concessions, respecting both people's limits and preserving communication access are a substantive later relationship lesson. Do not reduce this to “pause the argument and come back later,” and do not present involuntary symptoms as manipulation or as an excuse for coercion.

## Audience-development sequence

Seed content was added/strengthened in the project-lead's preferred authoring order: **Person → Clinician → Supporter**. Published pages retain the site-required reading order **Person → Supporter → Clinician**, followed by Research and Sources. Preserve approved authorship only for lessons actually human-approved. Lesson 18–20 **Person sections are approved**; their other audiences and Lessons 21–23 remain working drafts.

- **Person:** Ordinary scenes paced for a reader around age 14, with one distinct scientific concept, why it matters in FND, explicit uncertainty, and a low-risk reflection/adaptation.
- **Clinician:** Evidence type and limitations → differential clinical questions → profession-specific care or assessment, not an all-purpose mechanism claim.
- **Supporter:** What they may notice → why that could differ from internal experience → collaborative and consent-based assistance → supporter capacity → professional boundaries. A person living without a supporter must not be excluded.

## Community experience and quote review

**New Lesson 21 quote note:** The Person section contains a linked *paraphrase*, not an exact quote, of one individual's reported forgotten telephone call. The original October 30 search-indexed community material supplied by the project lead could not be directly rechecked here; verify full context before treating as an authenticated quotation or source.

User requested Person and Supporter community perspectives. Candidate sources were selected from the project notebook and earlier published source-check registry. **No independent fresh verification of external Reddit wording, speaker identity/role or surrounding context was possible in this editing pass.** Before publication review original public threads and remove any candidate that cannot be verified.

| Lesson | Voice | Quotation / status | Source |
|---|---|---|---|
| 18 | Supporter | Parent describing unpredictable onset; already checked in PR #191 as FND-CIT-0299 | [Discussion](https://www.reddit.com/r/FND/comments/1n8gljg/teenage_son_diagnosed_any_helpful_advicesupport/) |
| 19 | Person | Tingling, numbness and burning; **new candidate**, original context needs checking | [Discussion](https://www.reddit.com/r/FND/comments/1hmedeg/please_explain_your_symptoms_in_detail/) |
| 20 | Person | Sensory overload and seizure risk; **new candidate**, individual experience, not causal proof | [Discussion](https://www.reddit.com/r/FND/comments/1bpx5du/how_many_autistics_are_here/) |
| 22 | Person | Conversation interrupted by functional seizure; **new candidate**, mechanism unknown | [Discussion](https://www.reddit.com/r/FND/comments/1g8ebg3/i_need_advice/) |
| 22 | Supporter perspective | Ground rules before conflict; **new candidate**, exact speaker role and context need special verification | [Discussion](https://www.reddit.com/r/FND/comments/1g8ebg3/i_need_advice/) |
| 23 | Person | Body awareness/adaptation; **new candidate**, no universal outcome | [Discussion](https://www.reddit.com/r/FND/comments/1sedrnt/does_anyone_actually_get_better/) |
| 23 | Supporter | Spouse's consent-based offer to attend an appointment; previously checked FND-CIT-0312 | [Discussion](https://www.reddit.com/r/FND/comments/1o5s0b8/wife_just_diagnosed_with_disassociative_fnd_feels/) |

Do not force a caregiver quotation into Lessons 19 or 20: the old caregiver-bank candidates Q051 and Q096 were held back during PR #191 because speaker context or exact wording could not be adequately corroborated. A real quote gap is preferable to an incorrectly attributed quotation. Distinct remarks from the same discussion are not independent clinical studies.

## Structural and integration notes

- Module 7 has exactly **six** lesson Markdown files plus its overview; m7-4 is Cognition, m7-5 Emotion, m7-6 Agency. Old m7-4 Emotion and m7-5 Agency source paths were deleted; there is no legacy reader-facing copy. Each new/renamed page retains the required audience sections and navigation blocks.
- Local numbered citation references were checked against their table anchors in each of the six lesson files. They are not newly clinically verified.
- Updated course and Module 7 overview, SITEMAP, syllabus and downstream Module 8–10 display labels, course count 59, site generator expectation and curriculum regression tests.
- Old October 26 drafting documents, research briefs and historical source records remain in `reference/_internal/` for provenance. They are **not** a preserved earlier reader-facing course; don't treat their old overall lesson labels as current.
- **Required next:** clean Pages CI run for final commit, generated-source and rendered-site link validation; quote source verification; owner human authoring; later lesson Audit 1 and Audit 2; independent clinical review. Content work and account deployment remain separate.

