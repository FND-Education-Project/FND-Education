# Lesson 9 — Audit 2 and approved fixes

**Date:** October 21, 2026 (America/Vancouver).  
**PR:** #164.  
**Starting head:** `e28be1e9c399df68cae2fee4adb986abe32b14ed`.  
**Authorization:** Robert reviewed and approved the Audit 1 recommendations and requested implementation followed by Audit 2. No merge authorization.

## Implemented decisions

- M1: restored the exact contiguous clinic quotation proposed in Audit 1.
- M2: described the relationship writer's seizures without asserting confirmed functional seizures; marked the sentence-opening capitalization as `[S]ometimes`. All remaining quoted words are preserved.
- M3: registered the two community sources as FND-CIT-0285 and FND-CIT-0286 (0282–0284 are already allocated on main); added page citations 10–11, Figures 1–2 and the Figure column. Standardized citation labels. The authored clinician dialogue remains illustrative text.
- M4: retained Pick's exact bibliography and stable ID as plain text in this lesson. Its original-paper links remain in the internal Audit 1 source ledger.
- W1: added compact supporting citations to the mental-health paragraph and supporter participation example.
- W2–W4: added selective persistent-pain, everyday-function and biopsychosocial-glossary links; included a short Further reading line before continuation navigation.
- W5: broadened the clinician dialogue to “The clinical findings support your FND diagnosis,” accommodating different presentations without adding a symptom list.
- Preserved human-authored status, recorded current evidence/editorial audit dates, and kept clinical review pending.

## Editorial outcome

The reading/presentation source review is complete. No broad rewrite was needed after the approved human edit.

- Person section: conversational language appropriate to the intended adolescent reading audience; technical terms are introduced through examples. Short paragraphs and the recurring shopper reduce the number of new ideas readers must retain. Kept the softened-lighting classroom example and separate migraine treatment. This is an editorial assessment, not a validated reading-age score.
- Supporters: retained educational explanations, personal choice and flexible participation rather than a list of instructions. The family-gathering example stays consistent with the person and clinician sections.
- Clinicians: preserved professional terminology, finding-to-significance-to-care reasoning, study years and the 1,048 survey sample. Research hypotheses, observational associations and consensus retain their distinct roles.
- Thought/heart/action: retained the four-question exercise, meaningful personal goals, reflection questions and manageable optional next step. No additional workload or universal improvement expectation was introduced.
- Cross-lesson continuity: Lesson 9 applies the framework and evaluates claims, without repeating the earlier causes/mechanisms lessons or expanding into the Reference Library.
- Illustration: existing SVG, descriptive alternative text, caption and four-question correspondence retained. Shared CSS centers the figure at 60% on wide screens and 100% below 48rem, without text wrapping. The same questions appear as ordinary readable headings in the text.
- Navigation/metadata: three audience anchors and Research and Sources links retained; `/course/m3/3/` remains human authored and working-draft, with a clean description, previous Lesson 8 and next Module 4.

## Verification and remaining limits

- Generated-source validation passed for all 428 public routes (98 course and 323 Reference pages).
- Checked all 11 citation anchors, continuous three-column citation table, figure mappings, consistent citation labels, new link destinations and stable IDs; whitespace checks passed.
- Existing lesson artwork and the approved examples are unchanged. No new clinical claims were introduced, so Audit 1 evidence searches were not repeated.
- GitHub CI is the authoritative Jekyll build/artifact-validation gate; its final status is recorded in the PR.
- A local desktop/mobile browser pass could not be completed: Ruby/Bundler and a browser executable are absent, and the attempted browser download returned invalid archives. A substitute Markdown preview was not treated as a verified Jekyll render. Responsive CSS and generated source were inspected, but actual viewport appearance and keyboard interaction remain to be checked. This limitation is separate from the completed editorial review.

**Ready for Robert's content review. Clinical review and the rendered desktop/mobile visual check remain pending. PR remains unmerged.**
