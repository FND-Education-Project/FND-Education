# Lesson 11 — Audit 1: evidence and alignment

**Date:** October 23, 2026 (America/Vancouver).
**PR:** #176.
**Reviewed head:** `3b2a8a616e450594377f2f0aad4196d86298e580`.
**Scope:** Lesson 11 only, `course/part-1-understanding-fnd/module-04-mapping-your-individual-condition/02-building-and-using-your-personal-symptom-map.md`. Findings and recommendations only. Lesson 10, the parked shared-history snippet, Audit 2 and merge are outside this request.

## Overall finding

The core teaching is sound and the accepted human voice should be preserved. The map is patient-owned, optional and explicitly an educational communication aid. The lesson separates established diagnoses from open questions, recognizes participation and support needs, preserves clinician responsibility, and distinguishes useful observations from causal proof. Safety guidance is present for all audiences.

The most consequential corrections are authorship metadata and source traceability. No broad rewrite is recommended.

## Corrections to apply after review

| ID | Location | Finding and minimum correction |
|---|---|---|
| M1 | Working-draft banner and generated metadata | The banner says “Human-authored”; the generator recognizes “human authored” only. Reproduction produced `authorship: unspecified` for `/course/m4/2/`. Use the established unhyphenated banner wording, preserving approved human authorship. The generated description also contains the raw relative Markdown link to Lesson 10. Make the introductory summary plain text and retain the lesson link in the body, or use an explicit supported description. Verify both generated fields. |
| M2 | Four sourced blockquotes and citation table | All four lack the required sequential figure labels. Bennett incorrectly maps to Figure 1; Rutten also maps to Figure 1 despite following three community quotations. Add community Figures 1–3 with numbered page citations; make Rutten Figure 4; set Bennett's Figure cell to a dash. Use the standard plural italicized “citations” label for Rutten. Keep the selected quotations, subject to the small accuracy point below. |
| M3 | Community provenance and quotation precision | Register each community source with a stable ID and full page-level entry. Link the mobility and sensory excerpts to their exact comments, not the parent thread. Memory wording is a shortened excerpt: the first ellipsis is visible, but “My partner has to remind me.” adds a full stop where the original continues into medication reminders. Prefer the exact complete sentence about medication reminders, or visibly mark the trailing omission. Do not imply a verified FCD diagnosis from forum participation. |
| M4 | Central citation index | The Lesson 11 filename appears zero times in the index. Add this lesson to all six scientific source-use records: 0001, 0011, 0012, 0014, 0028 and 0067, subject to any source-use adjustment. Add the three community records and current-use links. IDs through 0289 exist at this head; check current main before allocating the next three IDs. Preserve every existing source and other lesson use. |

After implementation, replace quotation-verification-pending notes with accurate review dates and keep independent clinical review pending. Completing Audit 1 does not complete Audit 2.

## Small refinements worth making

| ID | Location | Recommendation |
|---|---|---|
| W1 | Clinician “Connect the formulation to daily life” | The consensus sources support individualized assessment, but have more qualified equipment guidance than the adjacent aid example might suggest. Add a positive sentence such as: “An individualized equipment review can bring together safety, fit, participation goals and rehabilitation needs.” Keep the community experience and avoid implying that access to needed equipment depends on recovery or treatment success. The lesson does not currently recommend universal aid prescription. |
| W2 | Clinician “Make the clinical reasoning available” | Butler's survey is relevant to coexistence and burden, not demonstrated effectiveness of this map or its continuity benefits. Attach [4] to a clearly limited coexistence statement, or remove it if no such claim remains. Frame the map benefit as its intended purpose, e.g. “The aim is continuity…”. Bennett supports the positive-diagnosis distinction. |
| W3 | Supporter “What another person can add” | “A map works just as well as a personal account” makes an unnecessary equal-effectiveness claim. Prefer “A map can also hold the person's own account.” Preserve independent use and the value of invited supporter observations. |
| W4 | Contextual links | Add a few existing Reference/glossary links, including a compact Further reading line before Continue. Prioritize external memory supports and communication access. A symptom-variability glossary link fits the person section. Link the existing swallowing assessment/safety material beside the sensory anecdote if helpful; keep its present safety explanation. |
| W5 | Research summary | Once sources are registered, state the evidence types clearly: consensus recommendations, qualitative stakeholder views, a systematic outcome-measurement review and individual lived experience. Preserve the explicit lack of validation for this course map. Detailed source-access notes belong in this internal report. |

## Quotation verification ledger

### 1. Mobility aids — verified exact sentence

Source: [JelloAdventurous comment](https://www.reddit.com/r/FND/comments/106utzh/comment/j3m7l9s/).

The selected sentence about mobility aids enabling fuller participation matches the original. It is a comment, not the thread author's post. Retain the limited lesson interpretation: this person's reported participation benefit, not a treatment-effect estimate or prescription for everyone. Do not import other commenters' medical advice.

### 2. Memory and reminders — source verified; punctuation/omission correction

Source: [“Memory issues?” original post](https://www.reddit.com/r/FND/comments/13rzn9o/memory_issues/), liamreee.

The source includes the exact opening clause and then “because of them.” The next sentence continues:
> “My partner has to remind me to take my pills, which ones to take when, and instructions for taking them.”

Use that complete sentence or a transparent omission instead of presenting “My partner has to remind me.” as a complete original sentence. The original post describes recent worsening and additional pain; it does not establish a confirmed FCD diagnosis or show that a map was tested. The lesson appropriately presents one person's memory-related care burden. Initial direct opens failed; the original Reddit page content was subsequently retrieved through search.

### 3. Post-eating sensory experience — excerpt verified with stated ellipsis

Source: [Vellaciraptor comment](https://www.reddit.com/r/FND/comments/1nk6chc/comment/nexcp8l/).

The selected text matches the comment, omitting “by keeping a diary for a bit” at the marked ellipsis. Keeping that short phrase would make the relevance to tracking clearer, but is optional. The direct comment is still visible although the parent post is now marked deleted; attribute only the available comment, not the deleted post author.

The source reports the writer's own interpretation and earplug benefit. It does not demonstrate a mechanism, diagnose dysphagia or establish a choking treatment. Preserve the existing immediate medical-assessment boundary and individual-experience wording. This is not a recommendation to use earplugs for swallowing difficulty.

### 4. Rutten et al. — exact selected wording and context verified

Source: [original 2025 publication, Abstract—Results](https://link.springer.com/article/10.1007/s00415-025-12912-9).

The 13-word selected passage is an exact clause. Its “all” refers to the study participants, not all patients or professionals. The parenthesized qualitative-study context is accurate. The next sentence recognizes additional value from clinician-rated/objective measures, consistent with the surrounding lesson prose. Preserve the quote and context; no replacement needed. This study informs outcome priorities, not validation of the course map.

## Scientific evidence checks

| Source | Verification and applicability |
|---|---|
| [Bennett 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7850207/) | Original indexed text supports diagnosis based on positive findings or seizure features and recognition of coexistence. Appropriate to the clinical distinctions. Full-page access intermittently returned a browser challenge; no claim of complete new full-text appraisal. |
| [Nicholson 2020, author-hosted long version](https://neurosymptoms.org/wp-content/uploads/2020/12/jnnp-2019-322281-inline-supplementary-material-1.pdf) | Original consensus supplement reviewed, including methods, activity/participation scope and aids/adaptations section. It recognizes individualized equipment decisions and benefits for safety, access and quality of life, alongside rehabilitation concerns and follow-up. Supports tailored care, not proven effects of a one-page map. Publisher HTML returned 403. |
| [Rutten 2025](https://link.springer.com/article/10.1007/s00415-025-12912-9) | Original abstract and methods/results reviewed. Qualitative UK stakeholder study; patient priorities and clinical observations both matter. Exact selected clause verified. No population-wide estimate or map efficacy inferred. |
| [Butler 2021, author-institution record](https://kclpure.kcl.ac.uk/portal/en/publications/international-online-survey-of-1048-individuals-with-functional-n/) | Bibliography and online-survey scope checked. A selected self-report survey can inform coexistence/burden, not map effectiveness or individual diagnostic conclusions. No new prevalence figure is proposed. |
| [Nielsen 2015, original publisher record](https://jnnp.bmj.com/content/86/10/1113) | Indexed original text verifies consensus status and the qualified equipment recommendation, including possible independence/quality-of-life benefit with continuing disability. Direct HTML access returned 403 and PMC a challenge; full-text reappraisal was incomplete. Its scope is functional motor rehabilitation, not all FND symptoms. |
| [Pick 2020, original review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7279198/) | Original indexed conclusions and bibliography checked: limited validation of FND-specific measures and need for contextual measurement. This supports the lesson's measurement limits; it does not validate intensive diary use or this map. Full-text retrieval was intermittent. |

## Existing destinations for selective links

- Memory supports: `../../../reference/recovery-techniques/functional_cognitive_disorder/08-external-memory-supports.md`.
- Communication access: `../../../reference/recovery-techniques/functional_speech_and_voice_symptoms/09-communication-support-and-aac.md`.
- Equipment and body care, if needed: `../../../reference/recovery-techniques/functional_paralysis/03-equipment-and-body-care.md` (clearly identify its paralysis scope).
- Symptom variability: `../../../glossary/README.md#symptom-variability`.
- Medical safety: `../../part-2-safety-and-symptoms/module-05-medical-safety-and-new-symptoms/02-emergency-information-and-individual-safety-plans.md`.

These targets exist. Avoid a large list of resources that interrupts the accepted pacing.

## Technical checks and boundaries

- Local site preparation and generated-source validation passed for 429 public routes: 99 course pages and 323 Reference pages.
- All existing relative file links resolve; all six numbered citation anchors and references exist. The bibliography is continuous.
- The metadata issues above are reproduced in generated source despite the passing validator.
- Previous Lesson 10 and next Module 5 navigation are correct. Three audience anchors are retained; the Research heading has its automatic anchor.
- No new image or colouring asset was supplied for this audit. The PR deliberately removed an image; restoring it is not part of Audit 1.
- No rendered desktop/mobile inspection is claimed.
- Only this report and the PR audit summary are changed. All accepted teaching prose, quotations, Lesson 10 and the parked snippet remain unchanged.

**Await Robert's decisions before applying corrections or performing Audit 2. PR remains draft and unmerged.**
