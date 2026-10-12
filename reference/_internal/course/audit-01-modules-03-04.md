# Course–Reference–Glossary Audit 1 — Batch 02: Modules 3–4

**Prepared:** 2026-10-12  
**State:** Preliminary repository-based assessment; **external source verification needed in Work mode** before findings are finalized  
**Branch:** `audit/course-align-m03-m04-pass1` (audit-only, independent of draft PR #132)  
**Base:** `main` at `f1427f75d248e6713d124cdfc974f028cde99332`  
**Scope:** Module 3 overview + three lessons; Module 4 overview + one lesson = **six course pages**.  
**No implementation:** No course lessons, Reference Library pages, Glossary, citations, archives, or existing site assets are changed by this batch.

## Separation of work

**Audit 1:** Establish whether the course tells the science accurately, identify meaningful omissions and suitable Reference/Glossary destinations, and classify each action **must-fix / worthwhile / unnecessary**. Check claims and source interpretation. **Do not implement optional content/link improvements now.** Only materially consequential inaccuracies or broken navigation may be separately approved as an exception.

**Audit 2:** Implement the approved content, cross-reference and glossary edits later, after all relevant Audit 1 batches and project-lead review. Do not add links now simply to achieve a count.

PR #132 addresses a different eight-page batch and its five approved must-fix exceptions. It remains separate; do not inherit or repeat its changes in this branch. The Module 1 human-authored archive on that branch remains protected.

## Baseline observations

| Module/page | Approx. length | Specific Reference links | Contextual Glossary links | Initial impression |
|---|---:|---:|---:|---|
| M03 overview — What May Cause or Affect FND? | 534 words | 0 | 0 | Strong terminology/uncertainty framing |
| M03.1 — Causes, Risk Factors, Triggers, and Maintaining Factors | 2,184 words | 0 | 0 | Good causal distinctions; some claims require source checks |
| M03.2 — Brain Networks, Prediction, Attention, and Agency | 2,386 words | 0 | 0 | Highest-priority evidence review because of detailed neuroimaging claims |
| M03.3 — Physical, Psychological, and Social Factors—and How to Judge Claims | ~2,000+ words | 0 | 0 | Good critical-reading framework; could connect to experience references |
| M04 overview — Map Your FND and Other Health Conditions | 407 words | 0 | 0 | Appropriate short entry, avoid extra link list |
| M04.1 — Build and Use Your Personal Symptom Map | 2,323 words | 0 | 0 | Practical structure; preserve distinction between patient aid and validated instrument |

Specific links exclude generic site-wide Reference navigation; these are sample text counts rather than claims about site rendering. Both module overviews already lead to their lessons. The four focused lessons have Person/Supporter/Clinician/Research sections. Source quotations, canonical references and working-draft notices exist. These two modules do not need a wholesale rewrite.

## Candidate priority findings (to be verified)

### Must-check before categorizing as must-fix

These items are **verification questions, not established mistakes**. Work mode should only label one "must-fix" when the original research or policy actually demands correction.

1. **M03.2: narrow structural MRI claim.** The course states that Perez and colleagues studied **26 motor-FND patients and 27 controls**, observed no **whole-brain-corrected** cortical-thickness difference in the full group, reported a **left caudal anterior cingulate** association with somatoform dissociation in specified analysis/subgroups, and a **right lateral occipital cortex** association with depersonalization/derealization. Verify sample, covariates, comparison groups, locations, multiple-comparison correction and what the original paper actually demonstrates. The surrounding paragraph correctly states this is *not* an FCD cohort or a diagnostic biomarker. If any detail is wrong, recommend the smallest correction; if correct, consider whether this much detail belongs in an introductory course rather than in the Reference Library.
2. **M03.2: mechanism and measurement.** Check that descriptions of predictive processing, precision weighting, active inference, attention, salience, interoception and sense of agency distinguish theoretical interpretation from directly measured outcomes. No single proposed predictive-processing or fMRI pattern should become a proven mechanism for each person. Review against appropriate current reviews, not a hand-picked experiment alone.
3. **M03.1 / M03 overview: risk, triggering and maintaining factors.** Verify source attribution where a study of co-occurring experiences or patient self-reports is cited for terminology that might imply *causality*. An association, a retrospectively reported precipitant and a causal mechanism are different forms of evidence. Do not assign a personal psychological cause or a "maintaining factor" without individual evidence.
4. **M03.3: categorizing physical/psychological/social influences.** Check that mental-health, trauma, illness, injury, migraine, sleep and autonomic factors are discussed with the correct level of evidence. "Psychological factors may matter" is not the same as "psychological factors are necessary for FND"; self-management response is not proof of cause.
5. **M04.1: claimed value of symptom mapping.** The page already explicitly calls its one-page map a *project framework*, not a validated diagnostic or therapeutic instrument. Confirm that its supporting citations concern OT communication, individualized outcomes and assessment, not randomized evidence for **this map**. Keep triggers and warning signs separate, and leave medical classification with clinicians.
6. **Community excerpts/illustrations:** Spot-check quotations, source URLs, non-identified personal stories, figure descriptions and citation anchors only where relevant to meaning or safety. Do not reconstruct unrelated community content to satisfy a quota.

### Page-by-page provisional change map

| Page | Priority / reasoning | Possible work for Audit 2 once approved |
|---|---|---|
| **M03 overview** | **Unnecessary** to expand: it already distinguishes cause, trigger, risk, mechanism and maintaining factor, and routes to three lessons. | Retain as a compact course gateway. One contextual glossary link only if truly necessary; don't add a Reference list here. |
| **M03.1 Causes/risk/triggers** | **Worthwhile** if research supports: preserve its helpful definitions and uncertainty; perhaps clarify the difference between *a factor a person notices now* and *something demonstrated to cause FND*, especially when discussing neuroplasticity or self-management. | One targeted Reference link near overload/uncertainty or diagnosis-vs-cause discussion; glossary **Neuroplasticity** `#neuroplasticity` at first definition if it helps. No exhaustive trigger list. |
| **M03.2 Brain networks** | **Highest verification priority.** Detailed Perez neuroimaging paragraph and model terminology warrant original-study verification. Avoid conflating motor-FND data with FCD symptoms or cross-sectional associations with cause. | If needed, shorten the structural-study example and direct interested readers to [History of FND](../../history-of-fnd.md#reading-the-recent-findings-carefully) for methods/history, or the relevant [FCD background](../../functional-cognitive-disorder.md#working-models-not-one-proven-cause) **only when FCD is expressly raised**. Glossary: `#predictive-processing`, `#agency`, perhaps `#interoception`; no automatic linking of every mention of "attention." |
| **M03.3 Physical/psychological/social factors** | **Worthwhile:** excellent signs of weak causal reasoning already present. Preserve its critical-reading checklist and prevent repeating Module 1 biopsychosocial lessons. | Where disbelief or diagnosis-reduction is discussed, consider [Mental Health, Stigma, and Being Believed](../../biopsychosocial-experiences/02-mental-health-stigma-and-being-believed.md). Optionally a second link to [Unpredictability, Overload, and Trusting Your Body](../../biopsychosocial-experiences/05-unpredictability-overload-and-trusting-your-body.md) if there is a genuine practical use; avoid generic cross-link dumping. Glossary: `#biopsychosocial-model` only if the term is used without sufficient local explanation. |
| **M04 overview** | **Unnecessary** to add complexity. Already sends readers directly to a one-page map and distinguishes confirmed, associated and unresolved issues. | Leave overview short; do not add a general References shopping list. |
| **M04.1 Personal symptom map** | **Worthwhile:** clearer routing from practical symptoms to assessment and function, with a caution not to become a surveillance exercise already appropriately included. Research review must preserve the project's "not validated" statement. | Single link to [Understanding Assessment Results and Everyday Function](../../diagnostic-concepts/10-assessment-and-everyday-function.md) by discussion of task ability/repeatability, or to [Unpredictability, Overload, and Trusting Your Body](../../biopsychosocial-experiences/05-unpredictability-overload-and-trusting-your-body.md) if fear of constant monitoring is the actual issue. Possibly glossary `#associated-symptoms`, `#coexisting-condition--comorbidity`; don't link all table categories. |

**Scope note:** The project already has other courses for pacing, safety, cognitive supports and broader treatment. Refer to those canonical lesson homes rather than duplicating their detailed plans here. Do not create new Reference or glossary entries merely because a word occurs in the course.

## Existing destination checks for Work

All these files and section IDs were observed in the repository at preparation:

- `reference/history-of-fnd.md#reading-the-recent-findings-carefully` — historical context and interpretation of recent research, not a new diagnostic technique.
- `reference/functional-cognitive-disorder.md#working-models-not-one-proven-cause` — FCD-specific limits, only if relevant to the already-mentioned FCD comparison.
- `reference/biopsychosocial-experiences/02-mental-health-stigma-and-being-believed.md` — psychiatric comorbidity, belief, diagnosis and credibility.
- `reference/biopsychosocial-experiences/05-unpredictability-overload-and-trusting-your-body.md` — practical overload and non-constant surveillance.
- `reference/diagnostic-concepts/10-assessment-and-everyday-function.md` — measured performance, sustained function, assistance and recovery cost.
- Glossary: `glossary/README.md#neuroplasticity`, `#predictive-processing`, `#agency`, `#interoception`, `#biopsychosocial-model`, `#associated-symptoms`, `#coexisting-condition--comorbidity`.

**Linking policy:** Link an existing target only if it meets the immediate reader's need. Prefer 0–2 genuinely useful deep links on a relatively simple lesson, more only when independently useful. Avoid repeated disclaimers, multiple same-term links, linking common words in every sentence and bulk insertion in overviews.

## Research to prioritize in the evidence-checked continuation

The course currently relies on **FND-CIT-0001/0002/0003/0004/0005/0006**, plus Pick et al., patient survey evidence **FND-CIT-0014**, additional causation/psychology research **0015/0017**, imaging **0190**, outcome/OT **0011/0012/0067**, movement rehab **0028**, and other references. Inspect exact page citation tables rather than assuming these are each appropriate to all claims.

Work mode should:
- Read the **original Perez neuroimaging paper** corresponding to **FND-CIT-0190**; confirm each anatomical location, sample and statistical statement. Identify whether the observation is needed in an introductory lesson.
- Consult appropriate current studies/reviews of FND mechanisms and clarify which results concern motor FND, functional seizures, cognitive symptoms or mixed samples. Prioritize empirical findings and current consensus over attractive theoretical explanations.
- Check **Bègue et al. 2019** (FND-CIT-0004), **Drane et al. 2021** (0006), **Hallett et al. 2022** (0003), **Pick et al. 2019** (0005) against the exact claims. A mechanism review does not establish an individual diagnostic biomarker.
- Check **Butler et al. 2021** (0014) and the relevant non-motor/autonomic sources for what can and cannot be inferred from self-reported experiences and correlations.
- Confirm OT and outcome articles support the proposed *general* use of symptom summaries, not clinical validation of the project's particular one-page map.
- Record full-text/paywall gaps clearly, rather than claim verification based only on abstracts.

No live external research was performed in this preliminary preparation. The evidence-checked continuation needs Work mode with research access before classifying any suspect passage as a factual error.

## Validation and stop point

The current branch was created from untouched `main`, so the six reader-facing pages are unchanged. Confirm through the PR diff that only this new internal audit document has been introduced; do not accidentally include the Module 1 changes from PR #132. Verify all six canonical pages have their expected citations, audience headings, existing links and navigation. Site preparation should exclude this internal path from published pages and Pagefind indexing. Run repository CI and report its result.

**Review gate:** Stop after completing the evidence-checked six-page Audit 1 and updating this report and the draft PR. No Module 5, Audit 2, or reader-facing edits until the project lead reviews the findings.

## Work-mode instruction — Audit 1, Batch 02

> In `FND-Education-Project/FND-Education`, take draft PR for branch `audit/course-align-m03-m04-pass1` targeting `main`. Read `reference/_internal/course/audit-01-modules-03-04.md`, the six Module 3–4 course pages, corresponding Reference Library and glossary entries, central citation index, and editorial/evidence standards.
>
> Complete **evidence-checked Audit 1, Batch 02 only**, with original-paper review and appropriate up-to-date research. Confirm precise imaging assertions about the Perez cohort and named cortical regions, distinguish predictive-processing and agency models from measured effects, verify causal reasoning and questionnaire/observational evidence, and evaluate the practical symptom map without treating it as a validated instrument. Identify only meaningful omissions, clinical inaccuracies and reader-useful Reference or glossary links. Categorize findings as **must-fix, worthwhile or unnecessary**; record passages, sources, access limits, exact link targets and placements. Keep the course accessible without duplicating the Reference Library.
>
> **Do not implement public content or linking suggestions.** Preserve the untouched human archive in separate draft PR #132. Update only this internal audit document and the Batch 02 draft PR; validate paths, structure and build; stop for project-lead review. Do not advance to Module 5 or Audit 2.
