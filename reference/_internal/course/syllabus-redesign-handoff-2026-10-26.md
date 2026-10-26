# Syllabus redesign handoff — concepts-first 19-module course

**Date:** October 26, 2026<br>
**Authority:** Project lead approved changing the educational direction and asked for changes in a PR; a follow-up Work review will verify, add material, cite claims and check the site build.<br>
**Status:** Planning/documentation PR. No published course renumbering, redirects, database migrations, assets or user progress changes in this PR.

## Curriculum decisions

1. Keep the existing human-revised Modules 1–5 in place and retain their established teaching.
2. Put two **in-depth concepts modules** immediately after Module 5:
   - New **6: Attention and Automatic Control** (planned lessons 15–17).
   - New **7: Prediction, Body Signals, and Agency** (planned lessons 18–21).
3. Add **8: Recognizing Symptoms and Finding Information** (planned lessons 22–24). Teach observation and descriptive differences between similar experiences, not self-diagnosis. Point to the three-audience diagnostic and recovery Reference Library instead of duplicating symptom-specific pages.
4. Immediately follow with **9: Rehabilitation and Neuroplasticity** (formerly 14; planned lessons 25–27), then **10: Pacing, Activity, and Available Capacity** (formerly 15; planned lessons 28–30).
5. Keep the remaining nine subject areas for now (new Modules 11–19) even if some repetition may later be reduced. The other two of the original eleven later modules—rehabilitation and pacing—have moved forward to Modules 9 and 10.
6. Maintain Person, Supporters and Clinicians sections in every focused course lesson. Reference Library symptom entries already have their own audience sections and will receive human-voice editing after the course.
7. Write at accessible adolescent reading level with paced stories, ordinary examples, non-patronizing humour and no implication of symptom voluntariness.
8. Critical epistemic distinction: general nervous-system processes, empirical FND observations, proposed mechanistic models and individual causal attributions are **not interchangeable**. These concepts are not known to form one universal symptom-producing recipe.

## Numbering crosswalk (proposed only)

| Proposed new module | Topic | Previously |
|---|---|---|
| 1–5 | Established foundations and safety | 1–5 (unchanged) |
| 6 | Attention and Automatic Control | New |
| 7 | Prediction, Body Signals, and Agency | New |
| 8 | Recognizing Symptoms and Finding Information | Replaces symptom-course teaching in 6–12 |
| 9 | Rehabilitation and Neuroplasticity | 14 |
| 10 | Pacing, Activity, and Available Capacity | 15 |
| 11 | Building Your Individual Treatment Team | 13 |
| 12 | Psychological Treatment Without Blame | 16 |
| 13 | Daily Living, Accessibility, and Equipment | 17 |
| 14 | Relationships, Identity, and Grief | 18 |
| 15 | Healthcare Communication and Self-Advocacy | 19 |
| 16 | Work, Disability, and Community Participation | 20 |
| 17 | Setbacks, Relapse, and Changing Symptoms | 21 |
| 18 | Building Your Personal FND Handbook | 22 |
| 19 | Reviewing Progress and Choosing Next Steps | 23 |

The former symptom lessons 6–12 are *superseded as the intended course organization*, **not deleted**. Existing high-value topics should be relocated or linked:
- Event-specific emergency first aid → Module 5 cross-link and appropriate Reference pages.
- Automatic movement and movement retraining → new Modules 6 and 9.
- Sensory, speech and communication access → new Module 13 and Reference pages.
- Cognitive aids and shared-history/memory supports → new Modules 13–14 and FCD Reference.
- Coexisting migraine, pain, fatigue, sleep, autonomic complaints → new Modules 8, 10, 11 and appropriate Reference pages; no blanket FND attribution.
- Clinical differential and individual recovery methods → diagnosis/recovery Reference.

## Work review and implementation tasks (NOT yet executed)

**Curriculum and voice**
- Read this handoff and the newly authored syllabus pages 6–10. Check logical progression from existing Modules 1–5; prevent repetition of Module 3 mechanism introduction and Module 4 symptom mapping.
- Populate chosen lesson structure with Person sections first for human review, then Supporters and Clinicians. Use consent-based, practical scenes and optional reflection; do not force behavioral experiments.
- Verify all technical claims against current appropriate research and cite sources using the established citation index; clearly signal theory versus evidence. Obtain lived-experience and clinical review as applicable.
- Ensure every named concept has a consistent glossary term and links to relevant Reference Library pages.

**Site architecture and preserving learner state**
- Investigate existing learner-account D1 progress keys, API request/response identifiers, database schema and client-side completion semantics before renumbering or moving *any* public lesson.
- Prepare an explicit migration plan mapping **stable old lesson IDs to new IDs**, addressing collisions, legacy completion, deleted/superseded pages, partial work and rollback; do not assume display numbers are safe persistent identifiers.
- Maintain existing URLs as redirects or durable archived entry points, preserve deep anchors, search results and existing external links; replace links only after destination validation.
- Update course landing/navigation, Pagefind indexes, sitemaps, next/previous links, module/lesson selection controls, schema/metadata and build scripts.
- Audit generated crossword PDF/worksheet labels, source spreadsheets/JSON, colouring pages, thumbnail naming and selectors. Reuse materials deliberately; do not silently associate old puzzles with new lessons.
- Decide whether old 6–12 symptom course content has unique material worth migrating into Reference pages and avoid deleting it prematurely.

**Verification and release**
- Confirm every syllabus link, source pointer and new lesson path exists before publication; document future/planned paths without creating dead navigation.
- Run site build, link verification and relevant tests, with checks for stale course counts, generated nav and schema.
- Regression test progress for at least two learner accounts, signed-in/out switching, page refresh, theme settings and migrated legacy completion.
- Require project-lead review of human-authored sections and a separately approved release/migration PR for production changes.
- Do not merge a breaking site/navigation/progress migration as part of this documentation PR.

## Immediate completion criteria for *this* PR

- The detailed syllabus names exactly 19 **proposed** modules and links to new syllabus pages for 6–10.
- Existing Module 1–5 and legacy course pages remain physically untouched.
- New proposed lesson order puts concepts → symptom differentiation/navigation → rehabilitation → pacing.
- Clear migration instructions and risks are captured for Work to verify.

## Work follow-up — October 26, 2026

Planning/evidence review completed; human review and production migration remain pending. Read the [review and source kit](syllabus-redesign-review-2026-10-26.md), [migration plan](syllabus-redesign-migration-plan-2026-10-26.md), [identity inventory](syllabus-redesign-identity-map-2026-10-26.json), and first [Lesson 15 Person-section draft](proposed-lesson-15-attention-person-draft-2026-10-26.md).

Findings: current main has 75 lessons while account PR #154's allowlist has 74 and omits `m4-2`; its numeric `m6-1` key already means old seizure teaching, so new attention content must not inherit it. Overall planned lesson labels 15–30 are not local file numbers or API IDs. The projected 19-module core contains 57 focused lessons if the retained later splits stay unchanged; legacy pages and redirects need separate route counts.

The master syllabus and five proposed module outlines have been refined, with checked sources and exact existing vocabulary/Reference destinations. The first new Person section is internal for voice/depth review; remaining lesson bodies follow that checkpoint. Human Modules 1–5, all legacy course pages, glossary, public assets and runtime code remain untouched.

The architecture review inspected #154 read-only without merging or changing that branch. Source validation, its 34 existing offline Worker tests and one extra review-only synthetic A/B check pass; the final full-build result is recorded in this PR. Live two-account/browser/migrated-D1 acceptance remains a release gate, not a claimed result of documentation review. Keep this PR a draft and do not publish, renumber, migrate or deploy as part of this work.

## Follow-up requested by Robert — remaining lesson research

On October 26 Robert requested researched material for the remaining new lessons for Chat to develop. The [15 research briefs and source register](new-lessons-research-2026-10-26/README.md) now populate proposed Lessons 16–30. This supersedes the earlier decision to leave remaining lesson bodies unpopulated: substantial internal foundations and audience-specific teaching seeds are now available, while final public prose, human editing and clinical/citation review remain pending. The Lesson 15 Person draft is unchanged. Public migration and account changes remain outside this work.

## Person sections drafted (October 26, 2026)

The project lead requested complete **Person with FND sections only** for *all new Modules 6–10*, with the Supporter and Clinician directions to be developed in later passes (both have now been drafted below). The following five internal editorial files now contain the **16 planned lessons 15–30**:

| Proposed module | Person draft | Lessons |
|---|---|---|
| 6 — Attention and Automatic Control | [Read draft](person-drafts-2026-10-26/module-06-attention-and-automatic-control.md) | 15–17 |
| 7 — Prediction, Body Signals, and Agency | [Read draft](person-drafts-2026-10-26/module-07-prediction-interoception-and-agency.md) | 18–21 |
| 8 — Recognizing Symptoms and Finding Information | [Read draft](person-drafts-2026-10-26/module-08-recognizing-symptoms-and-finding-information.md) | 22–24 |
| 9 — Rehabilitation and Neuroplasticity | [Read draft](person-drafts-2026-10-26/module-09-rehabilitation-and-neuroplasticity.md) | 25–27 |
| 10 — Pacing, Activity, and Available Capacity | [Read draft](person-drafts-2026-10-26/module-10-pacing-and-available-capacity.md) | 28–30 |

Each lesson has a full opening scene, an explanation of the concept, its relevance and limitations, a reflective question and one small optional step. The drafts use everyday examples and deliberately **do not assert a universal FND mechanism or substitute symptom matching for diagnosis**. No Supporter or Clinician subsections were included in the **Person-only draft files**; both companion audience sets have since been drafted separately.

**Community quote candidates:** Eight quotations are embedded selectively (one in M6, none in M7, one in M8, four in M9, two in M10). They came from [the internal community quote source notebook](../recovery-techniques/community-experience-quotes.md) and existing source-linked course material; direct public forum wording and context **have not been independently verified for this drafting pass**. Work must inspect the original linked posts/comments and authors/context; recheck wording after truncation, de-identification, appropriateness and possible quote duplication before approving any for publication. In particular, the two rehabilitation reports linked to the same Reddit thread must not be treated as independent study evidence; their authorship should be verified before retaining “another person” wording. Prefer omission over a forced quote. Do not use any account as evidence of treatment effectiveness or a causal mechanism.

**Work's next content review** (before Supporter/Clinician writing):
1. Review all 16 Person drafts with the project lead for voice, pacing, depth, illustrations and whether the optional steps truly promote independent reasoning.
2. Verify factual claims, safety and research; map substantive claims to full source tables with appropriate and precise citation IDs, including POTS/heart/breathing and ME/CFS post-exertional worsening distinctions.
3. Audit referenced terminology against the Glossary and Reference Library; validate every link when moving drafts to live pages.
4. Identify missing concepts or uneven treatment (e.g., prediction research vs established neuroscience; rhythm/external-focus boundaries; diagnostic differential vs everyday observation).
5. **Keep** this PR documentation-only and draft. Do not replace the live Course lessons or renumber user progress before a separate agreed migration and clean build.

## Clinician sections drafted — October 26, 2026

Following the Person drafts, the project lead requested **Clinician content across every proposed lesson, Lessons 15–30**. The broad later Supporter direction is to **work collaboratively with the person on adaptations arising from each lesson**; the detailed Supporter sections are reserved for a separate drafting pass. Five complete internal [clinician drafting files and their coverage index](clinician-drafts-2026-10-26/README.md) have been added:

- [Module 6: Lessons 15–17](clinician-drafts-2026-10-26/module-06-attention-and-automatic-control.md)
- [Module 7: Lessons 18–21](clinician-drafts-2026-10-26/module-07-prediction-interoception-and-agency.md)
- [Module 8: Lessons 22–24](clinician-drafts-2026-10-26/module-08-recognizing-symptoms-and-finding-information.md)
- [Module 9: Lessons 25–27](clinician-drafts-2026-10-26/module-09-rehabilitation-and-neuroplasticity.md)
- [Module 10: Lessons 28–30](clinician-drafts-2026-10-26/module-10-pacing-and-available-capacity.md)

**Scope:** Across Modules 6 and 7, all **17** canonical Diagnostic/Recovery Reference presentations are discussed substantively in relation to appropriate professions and an individualized care/technique-selection question. The coverage index documents the exact primary lesson and professional lens for each; the associated 34 diagnostic/recovery overview files were verified present on this branch. Modules 8–10 then teach clinical differential reasoning, navigating symptom-specific evidence, selecting and assessing interventions, neuroplasticity without cure promises, realistic activity pacing and interdisciplinary review. Other co-occurring and whole-body conditions are discussed without mislabelling them as FND.

**Citation state:** The drafts link to Work's existing research source register using internal `Rxx` keys, plus the appropriate Reference pages. These are **not** final public citations. Work must complete original-paper verification, source-to-claim matching, page-level numbered citations, specialist and accessibility review and accurate evidence qualifiers before the public course is written. Current source checks were performed against repository material; this continuation did not conduct a new independent live-publication evidence search.

**Not done:** No changes to live course pages, lesson numbering, existing links, D1 progress records, puzzles, or Supporter sections. Draft PR remains a planning/editing surface. Do not merge a public rollout until migration and build checks are complete.

**Editorial directions for the next pass:** Preserve the 16 Person drafts, refine the Clinician writing for a clear professional voice, identify overreach or duplicate material, and then develop the separately planned Supporter sections around collaborative, consent-based adaptation, without turning supporters into therapists.

## Supporter sections drafted — October 26, 2026

The project lead has now requested complete **Supporter sections for all new Lessons 15–30**, after the Person and Clinician sections. Five internal [Supporter files, a full lesson index, quote provenance and handoff framework](supporter-drafts-2026-10-26/README.md) have been added:

- [Module 6: Lessons 15–17](supporter-drafts-2026-10-26/module-06-attention-and-automatic-control.md)
- [Module 7: Lessons 18–21](supporter-drafts-2026-10-26/module-07-prediction-interoception-and-agency.md)
- [Module 8: Lessons 22–24](supporter-drafts-2026-10-26/module-08-recognizing-symptoms-and-finding-information.md)
- [Module 9: Lessons 25–27](supporter-drafts-2026-10-26/module-09-rehabilitation-and-neuroplasticity.md)
- [Module 10: Lessons 28–30](supporter-drafts-2026-10-26/module-10-pacing-and-available-capacity.md)

**Teaching direction:** Each Supporter section encourages shared, consent-based environmental or activity adaptations and explicitly identifies when the matter belongs to a practitioner: PT/OT for professionally assessed movement, equipment and daily-task rehabilitation; SLT and medical teams for communication/swallowing/airway risks; psychology for agreed evidence-informed treatment or adjustment; neurology/medical care for diagnosis, differential and new/changed symptoms; prescribers for medication decisions. Professional boundaries vary by symptom and individual need; they should not become a universal rule that every home accommodation requires clinical permission. Supporters are not substitutes for qualified clinicians, nor should they be held responsible for rehabilitation outcomes.

**Community-source bank:** The authoring source is the named **FND-Caregiver-Quotation-Bank-Lessons-13-75.docx** created October 25, with excerpts from publicly linked caregiver experiences. It was explicitly written for the **old** 75-lesson syllabus; our new quotes are selected by **topic fit**, not by old lesson number. The 16 sections presently contain **16 distinct quotation candidates** (one per lesson). The internal Supporter index maps each Q number to the new lesson and exact public thread/comment URL and explains contextual limits. The source DOCX was reviewed and its embedded public URLs extracted, **but the external posts have not been directly reverified during this pass**. Work must verify authorship, exact context, continued public availability and quotation safety before publication. Do not treat these as research findings or force a quote into a lesson if one becomes unsuitable.

**Completion:** All 16 lessons now have internally drafted Person, Supporter and Clinician sections, kept in separate files for coordinated human editorial review. These are **not** yet final public pages: clinical and academic citations, original community quote confirmation, consistency/voice audit, lesson integration, assets, link/build QA and the learner-progress migration still require Work review and project-lead approval. The public course, live accounts and puzzles remain unchanged.
