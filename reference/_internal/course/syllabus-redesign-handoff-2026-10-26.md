# Syllabus redesign handoff — concepts-first 19-module course

**Date:** October 26, 2026  
**Authority:** Project lead approved changing the educational direction and asked for changes in a PR; a follow-up Work review will verify, add material, cite claims and check the site build.  
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
