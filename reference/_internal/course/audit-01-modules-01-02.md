# Course–Reference–Glossary Alignment: Audit 1, Batch 01

**Date:** 2026-10-12  
**Branch:** `audit/course-align-m01-m02-archive-and-pass1`  
**Scope:** Course Modules 1–2: their two overview pages and six focused lessons, **eight pages total**.  
**Type:** Initial content/link/terminology assessment, not an exhaustive evidence or clinical validation.  
**Baseline:** Main at `f1427f75d248e6713d124cdfc974f028cde99332`; this review evaluates the generated course replacements proposed in the same PR, not the four archived human-authored manuscripts.

## Purpose and boundary

Use the newly developed 17 symptom diagnostic reviews and other reference material to improve the **course's correctness and useful connections**, without enlarging the course into an encyclopedia. Preserve introductory reading flow, each audience's ability to understand the page independently, positive diagnostic framing, medical reassessment, and the distinction between observed signs and real-world disability.

**Audit 1 determines what changes would help. Audit 2 implements approved changes.** This first batch does not insert new contextual reference or glossary links, does not turn every technical word into a tooltip, and does not revise the clinical content of already-audited reference pages. Do not silently restore human-authored passages from the archive.

## Preservation before audit

The complete source of all four human-authored Module 1 lessons is preserved verbatim in [the repository-only archive](human-authored-module-01-2026-10-12.md). This repository is public even though its `reference/_internal/` folder is excluded from publication.

- Lesson 1: **newly generated provisional replacement**. Original historical source is an authoring *template*, not a finished AI lesson.
- Lesson 2: **newly generated provisional replacement**. Same limitation.
- Lesson 3: older pre-human-edit draft from Git commit `51dd6ec531c0`, with required site breadcrumb, shareable audience anchors, and generated-draft notice restored.
- Lesson 4: older pre-human-edit draft from Git commit `89c276fdfbc6`, with shareable audience anchors and generated-draft notice restored.

The old drafts may contain older evidence framing, citations or formatting. They **must** undergo Audit 1 and later clinical/human review. The two newly generated replacements are not reconstructions of the user's individual original wording.

## Measured starting point, proposed branch

| Module | Page | Words (approximately) | Direct subject-specific Reference links | Direct Glossary links |
|---|---|---:|---:|---:|
| 1 | Overview | 555 | 0 | 0 |
| 1 | What “Functional” Means | 972 | 0 | 0 |
| 1 | Biopsychosocial Model | 939 | 0 | 0 |
| 1 | Remission and Recovery | 1,141 | 0 | 0 |
| 1 | Available Capacity and Spoons | 2,303 | 0 | 0 |
| 2 | Overview | 258 | 0 | 0 |
| 2 | Positive Signs and Examination | 1,916 | 0 | 0 |
| 2 | Tests and Diagnostic Uncertainty | 2,082 | 0 | 0 |

The **general Reference Library navigation link** is present and not counted above. Each of the six focused lessons has the four reader-audience/research sections. All eight pages' relative file links resolve against tracked repository paths at this review. Anchor-level/rendered-site checks and source verification remain for Work mode/CI.

## Page-specific findings and proposed link candidates

### M01 Overview — prioritize compact pathway, not a long reading list

The overview correctly orients to real, involuntary symptoms, positive diagnosis, coexisting illness and individual outcomes. It currently offers only general Reference Library navigation.

- **Content:** Check that its definition of capacity remains descriptive rather than a measurable neural/autonomic state. Keep the “no established cure” and recurrence-not-failure framing.
- **Reference:** Consider *Understanding a Positive FND Diagnosis* (`reference/diagnostic-concepts/01-positive-diagnosis.md`) as one optional deeper-reading link; don't repeat every lesson's links here.
- **Glossary:** Link “functional” on first meaningful use only if that helps more than the already linked first lesson.

### M01 Lesson 1 — What “Functional” Means and How FND Can Appear

**Newly generated interim draft.** Accessible symptom description, variability without intentionality, coexistence, positive diagnosis and function-versus-exam distinction. Shorter and less illustrated than archived human version. Accuracy/evidence, graphics and reading flow require separate review before treating it as equivalent course material.

- **Content:** Verify that explaining “function” does not overclaim a single information-processing mechanism. Clarify that FND is a positive clinical diagnosis; findings differ by symptom and don't measure sustained disability. Do not treat every symptom family mentioned as automatically FND.
- **Reference:** `reference/diagnostic-concepts/01-positive-diagnosis.md`; `reference/diagnostic-signs/README.md` only if a compact symptoms index is helpful.
- **Glossary:** `Functional`, `Positive diagnosis / rule-in diagnosis`, and perhaps `Coexisting condition / comorbidity`, selectively.
- **Validation:** Decide whether one existing image is appropriate; do not copy copyrighted figures or human-written language back from the archive by default.

### M01 Lesson 2 — Biopsychosocial Model and Misconceptions

**Newly generated interim draft.** Diagnoses versus causes versus modifiable barriers are separated. Needs source and teaching review, especially the varied meanings of biological/psychological/social dimensions.

- **Content:** Preserve “not required to have trauma/anxiety” and avoid treating a care framework as an established mechanism. Avoid adding repeated disclaimers around every example.
- **Reference:** `reference/biopsychosocial-experiences/02-mental-health-stigma-and-being-believed.md` (only where disbelief or psychologizing is discussed); consider a course Module 3 link for detailed causal models instead of repeating the material.
- **Glossary:** `Biopsychosocial model`, `Diagnostic overshadowing` if that concept appears in the final wording.
- **Validation:** Verify citations adequately support each substantive claim; prepare any quotation additions only from checked source text.

### M01 Lesson 3 — Remission, Recovery, and What Improvement Can Mean

**Historical pre-human-edit generated draft restored.** Compare its dated evidence framing with newer outcome and life-impact standards. Do not let 'remission' imply the whole disease has been cured.

- **Content:** Inspect remission/recovery definitions, progress in quality of life versus disappearance of symptoms, follow-up and renewed medical assessment. Preserve no-cure and setbacks-not-failure principles.
- **Reference:** `reference/biopsychosocial-experiences/06-recovery-pressure-self-blame-and-feeling-like-you-are-failing.md` where treatment pressure comes up; one canonical recovery-techniques landing page only when genuinely useful.
- **Glossary:** No `Remission` or `Recovery` glossary entry currently exists; prefer a short plain-language definition in the lesson, not a dead link or automatic glossary addition.
- **Validation:** Review historical quotations/citation matching before publication approval.

### M01 Lesson 4 — Available Capacity, Spoons, and Early Action

**Historical generated version restored.** Its length is greater than the other Module 1 drafts and merits a reading-load review rather than arbitrary shortening.

- **Content:** “Capacity” and “spoons” are useful descriptive tools, not a diagnostic biomarker or universal predictor of seizures/flares. Distinguish adaptations, pacing and medical reassessment.
- **Reference:** Consider `reference/diagnostic-concepts/10-assessment-and-everyday-function.md` when explaining repeatability and recovery cost. The detailed pacing module is the canonical course explanation; don't duplicate it here.
- **Glossary:** `Available capacity` and `Spoon theory` at the first useful appearance, without linking all repetitions.
- **Validation:** Confirm restored imagery/links and existing authorship notice after the site build.

### M02 Overview — How Is FND Diagnosed?

Currently has **zero** deep Reference links despite having directly matching cross-cutting references.

- **Content:** Positive clinical evidence, suitable tests and individual uncertainty are all essential; avoid implying a single sign applies to all FND.
- **Reference:** Short “go deeper” pair: `reference/diagnostic-concepts/01-positive-diagnosis.md` and `reference/diagnostic-concepts/03-tests-and-investigations.md`. Link to the diagnostic-signs collection only if there is a separate practical reader need.
- **Glossary:** Introduce `Positive diagnosis / rule-in diagnosis` only if that term is actually explained in the overview rather than repeating the focused lesson.

### M02 Lesson 1 — Positive Signs and the Neurological Examination

The generated lesson already gives useful examples and includes an examination illustration but does not connect to the now-mature diagnostic references.

- **Content:** Cross-check Hoover's sign, tremor distractibility/entrainment, and the limits of each with the evidence review. A positive examination finding must not be equated with full everyday functional capacity or voluntary control.
- **Reference:** `reference/diagnostic-concepts/01-positive-diagnosis.md` and one carefully chosen concrete example, e.g. `reference/diagnostic-signs/functional_limb_weakness/01-hoovers-sign.md`. A broad reader-facing further-reading link may be more appropriate than multiple technical technique links.
- **Glossary:** `Positive clinical sign / positive diagnostic sign`, `Hoover's sign`; optional `Inconsistency` if the lesson uses the term.
- **Validation:** Verify detailed scientific claims and citations; don't replace clear introductory explanations with specialist test parameters.

### M02 Lesson 2 — Tests, Diagnostic Uncertainty, and Coexisting Conditions

Contains useful distinctions about MRI/CT, EEG, neurophysiology, uncertainty and coexisting conditions but no targeted deeper-reading route.

- **Content:** Verify that a normal routine EEG does not rule out epilepsy; clarify what each investigation can and cannot show. Keep the possibility of coexisting diagnoses and concrete reassessment pathways.
- **Reference:** `reference/diagnostic-concepts/03-tests-and-investigations.md`; optionally `reference/diagnostic-concepts/10-assessment-and-everyday-function.md` for the distinction between tests, clinical assessment and daily function.
- **Glossary:** `EEG`, `Differential diagnosis`, `Coexisting condition / comorbidity` if used in the final wording.
- **Validation:** Seek evidence for claims regarding tests and event evaluation; ensure no passage encourages avoiding medical care for a new or substantially changed symptom.

## Site-wide policy to apply in Audit 2

1. **Keep lessons independently useful:** no new link should be required to understand an essential course explanation.
2. **Contextual reference links:** attach selectively to the sentence where detail is needed. Prefer 1–3 distinct deeper-reading destinations in simple lessons, more only when the topics truly justify it.
3. **Further reading:** a compact block near the end of a focused course lesson only when it genuinely helps; avoid repeating every contextual link in the block.
4. **Glossary:** manually select the first meaningful unfamiliar use per page or independent audience; no automated replace-all. Existing entries must match the linked concept and exact anchor. On mobile, links remain accessible without hover.
5. **Source integrity:** reuse the stable IDs and verified citations. Never infer that task performance proves low disability, full recovery or deliberate control.
6. **Human-writing boundary:** do not amend `reference/_internal/course/human-authored-module-01-2026-10-12.md` or copy its sentences back to course pages without the project lead's decision.
7. **Build and reading checks:** verify each public URL, relevant section anchors, Next/Previous positions, plain text before/after links, citations, mobile tap/keyboard operation and accessible link names.

## Work-mode handoff — necessary for deeper evidence review

> In the GitHub repository `FND-Education-Project/FND-Education`, review **only** the eight Module 1–2 course pages listed in `reference/_internal/course/audit-01-modules-01-02.md` on branch `audit/course-align-m01-m02-archive-and-pass1`. Treat this document as the first-pass findings and the four archived human texts as protected source snapshots, not publishable copy.
>
> Complete **Audit 1 only**: compare each lesson to the **current merged** FND Reference Library (diagnostic concepts/signs, recovery, biopsychosocial experiences, and relevant co-occurring material), the glossary and the project's editorial/evidence/navigation policies. For every materially outdated or inaccurate assertion, provide the exact passage, evidence distinction, and verified supporting citations, prioritizing Jon Stone and collaborators without ignoring stronger alternatives. Distinguish factual corrections, missing context, excessive verbosity, useful reference links, glossary candidates and optional refinements; assign **must-fix / worthwhile / unnecessary**. Identify exact existing link destinations and confirm glossary anchors; do not add generic links simply to increase counts. Check 2026-current sources online where material.
>
> **Do not rewrite lessons or change reader-facing links yet.** Update the internal findings document with a concise page-by-page change map, proposed link placement and specific checked sources. Validate compatibility with the 4-section structure, citation convention, source IDs, shareable headings and mobile accessibility. Preserve the human-text archive verbatim. Commit to an **audit-only branch and open a draft PR targeting main**, or, if working within the existing draft PR, confine changes to the findings document. Stop for project-lead review rather than beginning Module 3 or Audit 2.

**Gate:** Do not begin Audit 2 before the lead has reviewed Audit 1 findings. Any content and glossary changes approved later should be built in separate, manageable implementation batches.
