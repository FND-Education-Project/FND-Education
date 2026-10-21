# Lesson 8 — Audit 1 of the human revision

**Date:** October 20, 2026.  
**PR:** [#160](https://github.com/FND-Education-Project/FND-Education/pull/160).  
**Reviewed head:** `5ff1e777383862e997add081023f64ca711f1c3e`.  
**Status:** Audit complete; recommendations only. Author and clinical review remain pending.

## Scope and decision

Reviewed Lesson 8's three audience sections, research summary, citations, quotation provenance, metadata conventions, assets and links against the repository's evidence, citation, editorial-safety, accessibility, core-principle and page-maintenance standards. No AGENTS.md appears in the reviewed tree.

Keep the lesson's structure and human-authored examples. Its distinction between an observed finding and a proposed mechanism is generally sound. The clinician section now teaches the concepts in manageable steps. The principal corrections are traceability, accurate authorship status and a cross-PR anchor dependency, rather than a wholesale rewrite.

Audit 1 covers evidence, substantive omissions, source attribution, useful Reference/glossary destinations and structural compliance. Audit 2 remains the later readability, pacing, formatting and rendered-experience pass. This commit changes only this report; public lesson text, quotations and assets are untouched.

## Must-fix findings

| ID | Location | Finding and minimum recommendation |
|---|---|---|
| M1 | Supporter paragraph on suggestibility, symptom modelling and entrainment | This newly added scientific explanation has no citation. Cite evidence specifically supporting suggestion responsiveness, and distinguish it from observational modelling and rhythm matching. Wieder et al.'s meta-analysis is suitable for verbal suggestion, not proof that every person with FND is broadly suggestible. Use the existing entrainment Reference and its current clinical source for that definition. If retaining observational modelling, source its particular scope rather than treating the suggestion meta-analysis as evidence for all three concepts. Keep the positive message about involuntary symptoms and individual variation. |
| M2 | Working-draft banner, footer and generated authorship | The banner says the person/supporter sections were revised by the human author, although the PR explicitly identifies the suggestibility paragraph as AI-assisted and awaiting author review. The footer still says human authoring is pending, while the parser only recognizes the exact phrases “human authored” or “automatically generated”; the current banner therefore yields `unspecified`. Make banner, footer and generated metadata agree with the mixed contribution status. Do not label the entire lesson fully human authored before the remaining AI-assisted material is approved. Retain clinical review pending; distinguish the October 17 audit of the earlier version from this new audit. |
| M3 | Brain-chemistry heading and Lesson 7 integration | The approved Lesson 7 commit `0165c226` links to `#could-the-chemicals-in-my-brain-have-changed`. Lesson 8 renamed that heading and has no matching explicit anchor. Preserve this old anchor at the current person-facing chemistry heading. This is an incoming-link issue when the two PRs are combined, not a missing file. Keep the already preserved structural-imaging anchor too. |
| M4 | “What is a brain network?” source cluster | The functional activity/communication paragraph cites [1] and the structural review [2]. Cite [1] and [3], the more direct network/pathophysiology sources. Keep [2] for the structural-imaging discussion. This is a small source-to-claim repair, not a reason to remove the paragraph. |

For M1, the directly relevant candidate is Wieder L, Brown R, Thompson T, Terhune DB. *Suggestibility in functional neurological disorder: a meta-analysis*. JNNP. 2021;92:150–157. [doi:10.1136/jnnp-2020-323706](https://doi.org/10.1136/jnnp-2020-323706). It is not yet listed under that DOI/title in the reviewed central index; allocate a stable ID only during approved implementation. Existing **FND-CIT-0170** is Saranza et al.'s narrower laboratory-supported movement-disorder paper, not this meta-analysis. Entrainment's current clinical source **FND-CIT-0022** is already available.

## Worthwhile, proportionate improvements

| ID | Passage | Recommendation |
|---|---|---|
| W1 | Person-facing brain chemistry | The chemical-messenger analogy immediately precedes metabolite research. Add a short bridge explaining that the scan estimates selected chemicals in a brain region; it does not directly observe messages passing between cells. Keep the current group-average, young-participant and research-uncertainty qualifications. |
| W2 | Person-facing agency | The final phrase “ownership and control” blends related but distinct concepts. Keep agency focused on experiencing oneself as initiating or causing an action, consistent with the existing glossary and clinician definition. |
| W3 | Normal scans and changed movement | Make the explanatory bridge precise: clinical findings guide the functional explanation; a normal scan alone does not establish it. Likewise, the task-change observation supports discussion of automatic versus focused movement but does not map two anatomical “routes.” A small wording adjustment and one Reference link are sufficient. |
| W4 | Reflection sequence | There are useful knowledge questions and an appointment action. An optional short feelings question would complete thought–heart–action, for example how it feels to hear both measured findings and remaining uncertainty. Leave detailed phrasing/pacing to Audit 2. |
| W5 | Optional learning activity | The collection link resolves to an existing Lesson 8 entry and PDF, but “Open the Lesson 8 colouring page (printable PDF)” currently opens the collection page, not the PDF itself. Make that label accurately describe the destination, or offer the standard compact thumbnail/direct PDF link plus collection link used in Lesson 7. Direct PDFs should open in a new tab. |

### Selective link map

Keep existing prediction, agency and functional-seizure links. Add only the links that serve a reader's immediate question:

| Point of need | Existing destination |
|---|---|
| Meaning of a normal scan | [Tests and investigations](../../diagnostic-concepts/03-tests-and-investigations.md) |
| Supporter distinction between one easier movement and daily ability | [Assessment and everyday function](../../diagnostic-concepts/10-assessment-and-everyday-function.md) |
| Entrainment definition / clinician tremor example | [Entrainment Reference](../../diagnostic-signs/functional_tremor/02-entrainment.md) |
| First substantive interoception explanation | [Interoception glossary](../../../glossary/README.md#interoception) |
| Supporter unfamiliar term, if a shorter destination is preferable | [Entrainment glossary](../../../glossary/README.md#entrainment) |

Choose either the glossary or Reference link for the same occurrence of entrainment; do not duplicate links throughout the page. No new glossary article or large resource list is necessary.

## Evidence verification

This was a targeted educational audit, not clinical approval or a systematic review. Original publications, publisher/author institutional records and indexed original-source text were checked. Several full-text opens returned access challenges; those are explicitly distinguished below.

| Lesson source | Check and conclusion |
|---|---|
| [1] [Hallett et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35430029/) | Publication record and indexed original review checked. Supports heterogeneous presentations and developing network/predictive accounts. No reason to replace its overall role. |
| [2] [Bègue et al., 2019](https://www.research.ed.ac.uk/en/publications/structural-alterations-in-functional-neurological-disorder-and-re/) | Original-author institutional record and indexed source checked. Structural scope supports retaining it in the structural section; use a more direct source for functional communication claims (M4). |
| [3] [Drane et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7930164/) | Indexed original perspective and publication record checked; full-text open challenged. The five research constructs and the lesson's proposed-model framing fit. Agency should stay distinct from ownership (W2). |
| [4] [Bennett et al., 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7850207/) | Indexed original review/record checked. Positive clinical evidence, rather than normal investigations alone, supports diagnosis (W3). |
| [5] [Nielsen et al., 2015](https://pubmed.ncbi.nlm.nih.gov/25433033/) | Original abstract and indexed consensus checked. Automatic/task-oriented movement is an appropriate motor-rehabilitation example. The lesson already identifies this as consensus with motor scope; do not expand it into proof of a treatment or mechanism for all symptoms. |
| [6] [Perez et al., 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5747307/) | Original full-text Results and Table 1 checked. **26 motor-FND participants and 27 controls** is correct. The complete groups had no corrected cortical-thickness difference; dissociation-related regional findings arose in specified subgroup/within-group analyses. Current wording and bibliography limitation are appropriate. |
| [7] [Charney et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10825645/) | Indexed original abstract/results and publication record checked; full-text open challenged. **32 young participants with mixed FND and 41 controls**, SMA NAA/Cr and GABA/Cr findings and regional interpretation are consistent with the reported study. Preserve ratios, population and non-causal framing. This is not direct synaptic signalling measurement (W1). |
| [8] [Tolchin et al., AAN guideline](https://www.neurology.org/doi/10.1212/WNL.0000000000214466) | Indexed official recommendations checked: event history, semiology, appropriate video-EEG where feasible and assessment for coexisting epilepsy. The 2026 issue citation is appropriate despite December 2025 online publication. No universal seizure mechanism is inferred. |
| Candidate suggestion source | [Wieder et al., author institutional abstract](https://kclpure.kcl.ac.uk/portal/en/publications/suggestibility-in-functional-neurological-disorder-a-meta-analysi/) read. Measures concern standardized suggestion responses and symptom induction; group differences do not establish an individual's everyday personality, a universal cause, or visual symptom modelling. |

### Community quotation

The sentence about meditation/focusing was verified verbatim in the [original “FND Head Jerking” post](https://www.reddit.com/r/FND/comments/17jx51h/fnd_head_jerking/), in its second paragraph, on October 20. It describes this writer's head movements and their differing experience during relaxation/focus. The current individual-experience label and nearby involuntary-symptom explanation are appropriate. **Keep the quotation unchanged.** This resolves the retrieval gap recorded in the October 17 audit.

## Site and asset checks

- All Markdown-linked repository files in Lesson 8 exist at the reviewed head. All linked local section/citation anchors resolve in source; citation targets [1]–[8] are present once.
- All eight stable citation IDs exist, and their current-use rows include Lesson 8. The earlier missing-use problem is resolved.
- The four audience/research anchors, breadcrumb, Next/Continue navigation and structural-imaging anchor remain present.
- The plain introductory description is suitable; the earlier citation-filled-description issue is not present in this introduction.
- The current illustration exists at `assets/images/module-3-lesson-8-brain-network-workshop.webp`, with responsive `image-60center`, descriptive alt text and a nonliteral caption.
- Lesson 8 coloring PDF and PNG exist; catalog entry `lesson-8` maps Module 3 lesson 2 to `/course/m3/2/` and the correct downloads. No missing Lesson 8 coloring asset was found. This audit does not compare these committed bytes with fresh uploads or claim visual PDF inspection.
- Reviewed-head [GitHub build #377](https://github.com/FND-Education-Project/FND-Education/actions/runs/39468205778) succeeded. Parser inspection still identifies M2, illustrating why CI alone is not an editorial approval.
- The local execution environment was unavailable. Source checks were performed through the repository connector; no local build, mobile preview or full accessibility test is claimed.

## Unnecessary expansion and Audit 2 handoff

Do not add an exhaustive symptom catalogue, new prevalence tables, another mechanism taxonomy or repeated warning paragraphs. Existing seizure and cognitive examples keep the lesson broader than movement alone. The small chemistry and structural examples already provide enough scientific detail for this lesson.

After approval, apply the targeted corrections and chosen links. Audit 2 should then check the long suggestibility paragraph's pacing, consistent source/figure presentation, the optional feelings reflection, resource labels/thumbnails, truthful dates/authorship, and the rendered page. Preserve the author's examples, quoted community words and artwork. **No Audit 2, public-content implementation or merge is included in this Audit 1.**
