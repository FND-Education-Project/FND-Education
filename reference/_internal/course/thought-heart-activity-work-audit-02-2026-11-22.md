# Thought–Heart–Activity PR #214 — Work Audit 2

November 22, 2026. Approved input head: `f4977c6db0c99ba2d4250b3b6791f0d2e0896482`. Reconciled parent: Module 12 PR #210, `5e4c1d41a37ef5f1e4ab7af56423682876b40874`. Merge order remains **#210 first, then #214**. No merge to main or deployment performed.

## Findings and resolution

| Class | Location | Finding and minimum resolution |
|---|---|---|
| Required | Three Module 11 Person reflection blocks; Module 12 handoff | Older stacked parent conflicted with current approved parent. Synchronize parent; preserve the exact #214 THA blocks and the parent’s surrounding lessons, metadata, citations and assets. Both handoff addenda retained. Resolved. |
| Required | `thought-heart-activity-inventory.md` | Full generator check failed: manually maintained snapshot differed from source. Regenerated from reconciled lessons. Resolved. |
| Required | Inventory generator, final Activity extraction (notably L14); copied L26 link | Exclude following artwork/transitions; resolve copied links relative to the inventory, leaving on-page prompts unchanged. Parent repair inherited; generated L26 link now resolves to `reference/README.md`. Resolved. |
| Worthwhile | Rendered-course check | Extend desktop/mobile coverage to all 35 applicable THA sets and require one of each heading in built HTML; capture reflection screenshots. Implemented. |
| Unnecessary | All 105 approved prompts and other audience prose | No further wording correction, additional disclaimer, generic stylistic rewrite, or new citation inside reflective questions is needed. Preserve eight accepted Audit 1 corrections. |

## Evidence and educational scope

All current prompts read. Lesson-specific contexts and relevant existing sources were checked for the potentially clinical questions, especially Lessons 5, 8, 16–22, 25 and 27–29. This is verification of the changed reflection material, not a claim to have freshly re-audited every untouched source in the whole course.

- **L1–14:** Real/involuntary symptoms, positive-sign interpretation, uncertainty and coexisting conditions agree with [Espay 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC7293766/) and [Bennett 2021](https://pubmed.ncbi.nlm.nih.gov/33479065/). L5 does not ask for self-testing. Existing individualized safety plans and assessment of new symptoms take precedence over activities.
- **L15–20:** Attention, automaticity and prediction are teaching concepts, not individualized diagnoses. [Nielsen 2015 consensus](https://jnnp.bmj.com/content/86/10/1113) supports purposeful automatic movement in selected functional-motor rehabilitation; it is not proof that these educational exercises treat all FND. [Drane 2021 perspective](https://pubmed.ncbi.nlm.nih.gov/32883381/) distinguishes candidate constructs and networks from established individual causation. Missing-stair and café examples are fictional illustrations; no deliberately provoked symptom, unsafe movement or aid withdrawal is required.
- **L21–22:** [Ball 2020](https://doi.org/10.1093/brain/awaa224) emphasizes clinical assessment and positive evidence in FCD, not diagnosis from one lapse. Prompt wording explicitly preserves that uncertainty. The angry-message exercise distinguishes a chosen reply from involuntary symptoms and does not prescribe a feeling.
- **L23–29:** Participation, adaptation, neuroplastic learning and treatment evidence remain distinct. Natalie’s blood-pressure change is explicitly a fictional measured finding with an unresolved interpretation, matching the existing Person lesson. No promised cure, inferred mechanism or clinical outcome is added by the prompts.
- **L33–38:** Healthcare barriers, separate purposes of care, meaningful outcomes and continuing consent agree with the current parent lessons. See [Module 12 evidence report](module-12-audit-02-evidence-and-validation-2026-11-22.md) for original treatment/consent/source verification.

No new community or scientific quotation is introduced by #214. All existing quoted material, citation tables and illustrations outside the replaced reflection regions are preserved. A reflection’s use of an existing lesson example does not create a new study, so no spurious new source IDs or duplicate usage records were added.

## Preservation and validation

- **32/32** changed lessons match approved input prompts exactly: Lessons 1–29, 33–35.
- **32/32** have unchanged content outside the replaced reflection blocks relative to the current parent, allowing only blank-line normalization. Legacy prompt headings in Lessons 7, 10 and 11 are recognized as the approved replacement regions.
- **35 sets / 105 prompts** occur once each and in order. All nine Module 12 prompts remain exact.
- Module 10 and Module 12 lesson files match the current audited parent byte-for-byte.
- Full inventory generation and `--check`, six curriculum tests, source preparation and validation pass on the reconciled checkout.
- Browser checks cover the actual GitHub-built site at 1280px and 360px. Final-head results and commit are recorded in the PR completion note after the run.

## Remaining limits

Independent clinical review, screen-reader acceptance and full assistive-technology testing remain pending. These optional reflections are education, not a tested self-treatment programme. After the lead merges #210, #214 must target `main` and its final merge-base checks must remain green. The current synchronization includes all parent changes without publishing either PR.
