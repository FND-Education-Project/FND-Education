# Lesson 10 — Audit 1: evidence and alignment

**Date:** October 22, 2026 (America/Vancouver).
**PR:** #174.
**Reviewed head:** `69f0ea4a7aa7559a05a35c497f17b8482038e88e`.
**Scope:** Lesson 10 only, `course/part-1-understanding-fnd/module-04-mapping-your-individual-condition/01-build-and-use-your-personal-symptom-map.md`. Recommendations only. Preserve the accepted human-authored prose and private-source boundaries. Lesson 11, Audit 2 and merge are outside this request.

## Overall assessment

The central teaching is sound: positive evidence for a particular functional presentation does not explain every future symptom; separate disease and FND can coexist. The account distinguishes patient correspondence from independently reviewed records and correctly says that a disc finding alone does not establish the cause of every symptom. Keep the folder and broken-arm analogies, the inclusion of people without supporters, and the balance between missed illness and burdensome care.

Targeted corrections are needed in timing-versus-causation language, audience-specific safety coverage and source presentation. No broad rewrite or removal of the lived-experience example is recommended.

## Must-fix recommendations

| ID | Location | Finding and minimum correction |
|---|---|---|
| M1 | Person: “What happened before, during and after?”; supporter: “Sharing observations without deciding the cause” | The person example calls later exhaustion a consequence, and the supporter definition says something happening afterwards “is a consequence.” Timing alone establishes sequence, not causation. Use “possible consequence” for the example and explain that a consequence results from an episode; something noticed afterwards may need another explanation. Preserve the useful before/during/after structure. |
| M2 | Person: new dizziness “still to be assessed”; “A small place to start” | This audience is encouraged to record an unresolved symptom, but the safety guidance appears only in the supporter/clinician sections. Add one brief statement that new, severe or substantially changed symptoms may need prompt assessment and urgent symptoms should not wait for completing a map or a routine appointment. Link to existing medical-safety material. Preserve the opening supporter paragraph as requested. |
| M3 | Citation table and adjacent references | Remove the blank line between rows 6 and 7 so the bibliography is one Markdown table. Rows 1 and 3 refer to “Figure 1,” but no corresponding scientific quotation/figure exists in this lesson after the split. Replace those mappings with a dash; map the community excerpt to its own source. Citation 5 has no inline use: remove it from this lesson or retain it only if a specific relevant claim is actually supported. Standardize the one singular citation label. Do not remove shared stable records or alter Lesson 11. |
| M4 | Memory quotation and private case provenance | Memory excerpt verified in a reply by lia_bean, not the original post. Use its direct comment permalink, label lived experience, and add a page citation, stable ID and figure mapping. Do not infer confirmed FCD from participation in the thread. For the case, add a minimal anonymous “patient correspondence, adapted with permission; not independently verified” source entry/stable record covering both audience uses. Keep original emails, institutions and identifiers outside the repository. |
| M5 | Central citation index | New lesson uses of FND-CIT-0002, 0068 and 0069 are missing from their source-use table rows. Add Lesson 10 to those records. Other six listed scientific source rows already include the retained path. Remove this lesson from 0028 only if citation 5 is removed and no use remains; preserve the stable ID and other uses. |

## Worthwhile refinements

| ID | Location | Recommendation |
|---|---|---|
| W1 | Supporter medical-visit discussion; clinician diagnostic-overshadowing and examination-safety passages | Add existing [8] and especially [9] at the relevant connected paragraphs. Mcloughlin directly covers diagnostic overshadowing and harm from professional interactions, so it is more directly matched than a general diagnostic review alone. Avoid a citation after every sentence. |
| W2 | Person risk-factor definition | Use “associated with a greater chance” rather than “can make a condition more likely,” to avoid implying that every risk factor is itself causal. Link to the already explained Lesson 7 terms rather than reintroducing a large taxonomy. |
| W3 | Supporter positive-sign definition | Broaden “examination findings” to clinical features from history and examination appropriate to the symptom. This accommodates seizure semiology and keeps the explanation consistent with the clinician section's phenotype-specific approach. |
| W4 | Clinical case, “spinal disc injuries” | Prefer “reported disc findings/herniations” unless their traumatic origin was established in the source. The later T6–T7 paragraph appropriately separates a finding from its explanatory role; use that precision consistently. Do not equate thoracic pathology with cauda equina syndrome. |
| W5 | Course-to-Reference/glossary links | Add a few links using the map below. The lesson currently has no contextual Reference links despite substantial diagnostic reasoning. Keep the author voice and avoid adding an encyclopedic resource list. |

### Selective link map

- Supporter “positive signs” or clinician opening: `reference/diagnostic-concepts/01-positive-diagnosis.md`.
- Clinician “What evidence would change the formulation?”: `reference/diagnostic-concepts/03-tests-and-investigations.md`, particularly the distinction between a finding and its clinical meaning.
- First “coexisting conditions/comorbidities”: `glossary/README.md#coexisting-condition--comorbidity`.
- First diagnostic-overshadowing explanation: `glossary/README.md#diagnostic-overshadowing`.
- Person safety sentence: the existing emergency-information/individual-safety-plans course page in Module 5, linked as further safety guidance. Do not require reading another page before obtaining urgent help.
- Scan-negative cauda equina Reference exists, but is optional and should only be linked for that particular differential. It is not a label for the T6–T7 finding.

## Evidence and provenance checks

| Source | Check and scope |
|---|---|
| Bennett 2021 / Espay 2018, [Bennett original review](https://pmc.ncbi.nlm.nih.gov/articles/PMC7850207/) and [Espay record](https://pubmed.ncbi.nlm.nih.gov/29868890/) | Positive diagnosis, appropriate phenotype and coexistence are consistent with the lesson. These reviews do not certify the correspondence's individual clinical decisions. |
| [Finkelstein 2021](https://onlinelibrary.wiley.com/doi/full/10.1111/acem.14263), [PubMed](https://pubmed.ncbi.nlm.nih.gov/33866653/) | Bibliographic identity and emergency-care review scope checked. Supports acute diagnostic reasoning; not a validated universal triage rule or proof that a particular patient required a particular scan. Complete independent appraisal of every recommendation was not undertaken. |
| [Mcloughlin 2025](https://academic.oup.com/brain/article/148/1/27/7750481), [PubMed](https://pubmed.ncbi.nlm.nih.gov/39241111/) | Original review/abstract explicitly includes diagnostic overshadowing, overdiagnosis, professional interactions and other iatrogenic harms. Correct year, volume and pages. Supports both sides of the assessment discussion, not a judgment of fault in this case. |
| [Rutten 2025](https://link.springer.com/article/10.1007/s00415-025-12912-9) | Original methods/results checked: qualitative interviews with patients, caregivers and professionals. Supports patient-centred outcome domains and perspectives, not validation of this particular one-page map. The lesson explicitly calls the map a course communication aid, which is appropriate. |
| [Pick 2020](https://pubmed.ncbi.nlm.nih.gov/32111637/) and [Nicholson OT consensus](https://jnnp.bmj.com/content/91/10/1037) | Bibliography and original indexed scope checked: outcome-measurement review and professional consensus respectively. They can inform information gathering but do not establish efficacy of this course's map. Keep that boundary. |
| Butler 2021, existing citation 4 | The selected survey is used for coexistence/associated symptoms, with selection limits acknowledged. No new numerical prevalence claim requires expansion here. |
| [Nielsen 2015](https://jnnp.bmj.com/content/86/10/1113) | Motor-physiotherapy consensus, currently not attached to any Lesson 10 claim. Do not stretch it into universal examination guidance merely to retain an inherited bibliography row. |
| [NICE neurological urinary guidance](https://www.nice.org.uk/guidance/cg148/chapter/Recommendations) | Supports assessment of urinary change potentially associated with new/progressive neurological disease. Exact acute imaging decisions remain clinical; a separate trauma-guideline endpoint was inaccessible. No additional scan protocol is proposed. |
| [Memory comment permalink](https://www.reddit.com/r/FND/comments/1mnw4fd/comment/n87y5xt/) | Original reply retrieved October 22. The selected wording matches the passage about difficulty placing events in time. It is an individual report, not evidence of a confirmed diagnosis, universal FCD feature or demonstrated benefit of a map. Keep the quote. |
| Private correspondence case | Assessed only the anonymized lesson wording and PR provenance statement. Original emails and medical records were not independently reviewed during this audit. The narrative consistently presents the account as reported, acknowledges limits, and contains no named facilities/people. Exact chronology, injury causation and clinical fault are not certified by this audit. No private documents were copied or uploaded to the repository. |

## Unnecessary changes

- Removing the accepted case, folder or broken-arm analogies; they teach a useful distinction with appropriate limits.
- Adding prevalence tables, diagnostic criteria for every symptom, mandatory imaging instructions or a lengthy emergency checklist.
- Repeating warnings in every paragraph or implying that every familiar symptom fluctuation needs emergency attendance.
- Changing Lesson 11, its authorship status or the split.
- Rewriting the accepted prose for reading pace in Audit 1; that belongs to Audit 2 after decisions.

## Technical verification and handoff

All existing relative file targets in Lesson 10 were checked against the reviewed-head repository tree; none were missing. All nine numbered citation anchors exist. The blank table break, orphan Figure 1 mappings and unused citation 5 were identified despite the successful build.

The working-draft banner matches the generator's `human authored` classification; the introductory description is plain text. The research heading provides the expected automatic heading anchor; an explicit shareable anchor would be an optional consistency improvement, not a broken link.

Reviewed-head [GitHub workflow 39830379694](https://github.com/FND-Education-Project/FND-Education/actions/runs/39830379694) completed successfully. Local execution became unavailable while restoring the pruned workspace, so no local rerun or rendered desktop/mobile inspection is claimed. Audit-report CI is recorded in the PR separately.

Only this internal audit report and PR notes are changed. **Stop for Robert's review before public fixes or Audit 2. PR remains unmerged.**
