# Audit 1: human-authored Lesson 7 and asset completeness

**Date:** October 20, 2026.  
**PR:** [#159](https://github.com/FND-Education-Project/FND-Education/pull/159).  
**Reviewed human-authored commit:** `bb09e2ad860a9ba1d5ae265068ed62379cfafec4`.  
**Decision:** Strong overall structure; targeted corrections recommended before final publication. Recommendations below are not applied to the author's prose. Clinical review remains pending.

## Scope and preservation

Read all three audience sections and the bibliography against the PR's audit instructions, editorial safety rules and citation policy. Compared the lesson's role with Lessons 6, 8 and 9. Checked the seven cited publications through original publication records, abstracts and available original-source text; access limits are recorded below. This is a targeted educational audit, not a systematic review.

The requested asset integration is implemented: the supplied color PNG is placed after the mechanism explanation in the person-facing section, using the established 60%-width centered figure class (full width on mobile). Its caption identifies the scene as imaginative research symbolism. The existing timeline remains. The supplied PDF is copied unchanged, its first page rendered as the matching thumbnail, and the coloring activity added at the end of the person-facing section, to the selectable puzzle catalog, the no-JavaScript collection and the asset index. PDF links open in a new tab/window and include landscape/fit-to-page printing guidance.

The human-authored lesson text, quotations, banner and review note are otherwise preserved. No Audit 2 rewrite or merge is included.

## Must-fix recommendations

| Location | Finding | Smallest useful correction |
|---|---|---|
| Working-draft banner | The author is correctly described as human, but `Human-authored` is not recognized by the generator, which only detects `human authored`. The generated metadata reads `authorship: unspecified`. | Change the banner's hyphenated phrase to the supported `Human authored` wording, or teach the parser that spelling. Keep clinical review pending. This is a metadata correction, not a change of author. |
| Clinician section, Pick model: “Evidence from the person’s history and assessment shows how relevant those pathways may be for that individual.” Also “a biological explanation grounded in their own findings.” | These formulations risk implying that routine individual history/positive diagnostic signs validate a proposed neural or emotional pathway. They support diagnosis and formulation; they do not establish that specific research mechanism in this person. The final evidence summary already states the appropriate limit, but the clinician section should also make the distinction locally. | Use “helps assess whether the model is relevant to the person's care” and describe the explanation as a clinical account informed by research. Keep positive diagnostic evidence and proposed biological mechanisms distinct. Sources 1–3. |
| Person section: “Many people develop FND through other pathways” | The intended point is sound: stress and trauma need not be present. However, “through other pathways” suggests established alternative causal routes for a quantified broad group, beyond the evidence presented. | Prefer “People can develop FND with or without a history of stress or trauma.” Cite [1] and [2] here. This preserves the positive message without asserting demonstrated individual pathways. |

These are narrow wording/metadata issues. They do not require restructuring the lesson or introducing lengthy cautions.

## Worthwhile recommendations

- **Restore selective deeper links.** The human rewrite removed contextual Reference/glossary links added in the earlier pass. Link the first maintaining-factor explanation to the existing [factor glossary](../../../glossary/README.md#predisposing-precipitating-perpetuating-and-protective-factors), migraine care to the [migraine Reference](../../co-occurring-conditions/01-migraine.md), and unpredictable/sensory experiences to [overload and trusting your body](../../biopsychosocial-experiences/05-unpredictability-overload-and-trusting-your-body.md). Two or three links are enough; retain the generic footer.
- **Keep causal evidence broader than a known mechanism.** The infection example appropriately says timing alone is insufficient. “Evidence showing how it contributed” can be read as requiring a fully known biological mechanism to establish causation. A small refinement to “evidence that it contributed” would keep causal inference distinct from knowing every mechanistic step. This is conceptual precision, not a new medical claim.
- **Match the evidence type to the recommendation.** The clinician paragraph groups pain, migraine and autonomic reviews as supporting “assessment and treatment.” Pain/migraine papers support considering accompanying clinical needs; the autonomic synthesis mainly describes heterogeneous physiology, not a tested treatment pathway. One short distinction would make the scientific teaching more concrete. Source 7 is also not direct evidence for sensory overload maintaining a particular person's symptoms.
- **Reflection progression:** “Pause and think” offers two useful factual questions and “One small step” provides action. The requested thought–heart–action sequence has little explicit room for feelings. An optional brief question about how uncertainty feels could complete it, with permission to skip. Avoid asking readers to search for hidden emotional causes or increasing symptom monitoring.
- **Supporter pacing:** The repeated infection timeline is understandable, but its timing-versus-cause conclusion appears several times. If shortening later, trim repetition rather than the permission, practical-support or assessment points. This is an Audit 2 opportunity, not a mandatory content cut.
- **Chemistry sentence:** The general claim that chemistry is under investigation is reasonable and leads naturally to Lesson 8. A direct Lesson 8 section link would make its evidence easier to find without duplicating spectroscopy detail in this lesson.

## What works and should stay

The cause/trigger/mechanism/risk-factor distinction is easy to follow. The infection scenario remains an example rather than a proven origin story. Present-day care and separate diagnoses receive attention without assigning blame. The 1,048-person survey is correctly identified as self-selected, with no population-prevalence extrapolation. The supporter section keeps consent and the person's priorities central. Treatment response is described tentatively and separated from original cause.

Lessons 6, 8 and 9 have distinct purposes: clinical assessment/coexisting conditions, mechanism research, and practical formulation/claim evaluation. Lesson 7 can retain its brief references to those subjects without repeating their tables or research detail.

Unnecessary additions: a new symptom catalogue, more figures, all mechanism theories, a prevalence table, a third community quotation just to meet a count, or repeated warnings after every example. Preserve the author's slower pace and voice.

## Evidence ledger

The seven bibliography records match their cited titles/years/DOIs. They are not seven primary studies: most are reviews, and Butler is a primary survey. The PR's original “seven numbered primary sources” wording should be understood as the seven cited publications.

| Lesson source | Access checked and conclusion |
|---|---|
| [1] [Espay et al., 2018](https://pubmed.ncbi.nlm.nih.gov/29868890/) | Original PubMed abstract read. Supports a positive diagnosis without requiring psychological stressors, wider possible sensitizing events, and developing biological models. It does not validate an individual mechanism from history alone. |
| [2] [Hallett et al., 2022](https://pubmed.ncbi.nlm.nih.gov/35430029/) | Original abstract and figure descriptions read. Psychological stressors can be absent; FND includes varied presentations and proposed shared mechanisms. Supports the lesson's central distinctions with the small pathway-wording correction above. |
| [3] [Pick et al., 2019](https://pubmed.ncbi.nlm.nih.gov/30455406/) | Original abstract/indexed review text checked. Emotional processing is an integrative model and research agenda. Its possible individual relevance should remain a formulation hypothesis. |
| [4] [Butler et al., 2021](https://pubmed.ncbi.nlm.nih.gov/34245646/) | Indexed original abstract/record and [authors' institutional record](https://kclpure.kcl.ac.uk/portal/en/publications/international-online-survey-of-1048-individuals-with-functional-n/) checked; direct PubMed reopening was intermittent. Sample and selection caveat also verified in the earlier audit. Current interpretation is appropriate; no new numerical inference was added. |
| [5] [Steinruecke et al., 2024](https://jnnp.bmj.com/content/95/9/874) | Indexed publisher results and PubMed methods checked; direct publisher open failed. Review concerns adult chronic pain, comorbidity, timing and treatment response. Supports accompanying pain needs, not proof that pain maintains every individual's FND. |
| [6] [Stone et al., 2025](https://academic.oup.com/braincomms/advance-article/doi/10.1093/braincomms/fcaf288/8221965) | Original publisher abstract and clinical-implications section read. Narrative review identifies limited overlap evidence and reasons to recognize and treat migraine separately; selected treatment observations do not establish individual original causation. |
| [7] [Paredes-Echeverri et al., 2022](https://pubmed.ncbi.nlm.nih.gov/34711069/) | Original abstract/results read. Autonomic/endocrine findings are heterogeneous; inflammation evidence is preliminary. Physiology research does not itself establish a universal cause or a treatment recommendation. |

## Community quotations: both sources now retrieved

This supersedes the earlier Lesson 7 sensory-overload retrieval limitation; it does not claim the outstanding quotations in Lessons 8–9 were rechecked.

- **New tremor:** [Original thread](https://www.reddit.com/r/FND/comments/1dde4p6/my_journey_with_functional_neurological_disorder/). The excerpt appears in a reply about a new resting tremor after earlier convulsions/seizures improved. Words and context match. The lesson stops before the source sentence's remaining clause, replacing the continuation with a period. This is a shortened excerpt with unchanged meaning.
- **Sensory overload:** [Original comment](https://www.reddit.com/r/FND/comments/1bpx5du/comment/kwymlh2/). The author describes autism, sensory-processing difficulty and their own seizure pattern. The lesson's words appear inside the longer sentence beginning “I find that my FND symptoms” and continuing after “sensory overload.” The capitalized opening/terminal punctuation are editorial shortening, not a different substantive claim. A direct comment link and consistent excerpt punctuation would improve traceability if the author wishes.

Neither anecdote is used as population evidence or proof of a cause. No quotation was edited in this task.

## Asset inventory after integration

Scope: all nine lessons currently under active authoring/review, plus target-existence checks for every thumbnail and download in the current puzzle catalog. Global site validation checks remaining linked site assets. “Missing” below means no matching asset found in this repository, not that a supplied upload was lost.

| Lesson | Illustration in lesson | Matching coloring PDF, thumbnail, lesson link and collection entry |
|---|---|---|
| 1 | Present: custom illustration and diagram | All present |
| 2 | Present: custom illustration | All present |
| 3 | Present: custom illustration | All present |
| 4 | Present: `available-capacity.png` | **No matching coloring PDF or thumbnail found**; lesson currently points to the general collection |
| 5 | Present: custom illustration | All present |
| 6 | Present: custom illustration and diagram | All present |
| 7 | Present: new custom illustration and existing timeline | All present after this change |
| 8 | Present: existing network-model SVG | No custom color illustration or matching coloring PDF supplied/found |
| 9 | Present: existing claim-check SVG | No custom color illustration or matching coloring PDF supplied/found |

Therefore, every Lesson 1–9 has a teaching illustration, but the coloring series is **not complete**: Lessons 4, 8 and 9 lack matching coloring assets. Among Lessons 1–7, only Lesson 4 remains outstanding. All supplied coloring PDFs for Lessons 1–3 and 5–7 are linked from their lesson and the collection with matching previews.

## Validation

- Source preparation and structural validation passed: 428 routes, 98 course pages, 323 Reference pages.
- All catalog image/PDF targets exist. Lesson 7 collection query uses the actual supported `collection=colouring&puzzle=lesson-7` parameters.
- Original uploaded color PNG and PDF copied byte-for-byte; PDF remains one unencrypted landscape page. Rendered first-page preview visually checked for clipping and legibility.
- Generated Lesson 7 metadata confirmed the existing human-authored parser issue described above. It is reported, not silently changed during this audit-only review.
- All existing author text preserved; only the requested figure and optional coloring block are inserted in the lesson.
- Rendered build result is recorded by the PR checks. No claim of a local mobile browser visual pass.
