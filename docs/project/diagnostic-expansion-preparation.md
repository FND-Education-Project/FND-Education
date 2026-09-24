# Diagnostic Expansion: Ownership and Migration Plan

[Home](../../README.md) › Project Documentation › **Diagnostic Expansion: Ownership and Migration Plan**

> **Automatically generated editorial preparation — September 24, 2026.** Records the agreed architecture and current repository inventory. Proposed destinations are plans, not published clinical pages. Human review pending.

## Purpose and scope

Prepare the diagnostic expansion before editing the first symptom. The September 23 “Diagnosis Page Structure” discussion established a shared-foundation model, a short Quick Reference, symptom-specific explanation, and clinician-focused technique pages with accessible definitions. This preparation records those decisions; it does not rewrite the functional-weakness page, move its human-authored passages, or publish new examination instructions.

The recovered discussion supplied decision summaries rather than a complete verbatim transcript. The decisions recorded here are the retrieved agreements, supplemented by explicitly labelled implementation choices based on the current repository.

## Agreed content ownership

Use three levels: **shared concept → symptom → technique**. If essentially the same paragraph could appear on three symptom pages, consider the shared concept page its primary home. Keep enough local explanation for each symptom page to make sense without compulsory link-following. Recovery guidance has its own existing collection.

| Content | Primary home | Keep locally on a symptom page | Keep on a technique page |
|---|---|---|---|
| What a positive diagnosis means | Shared positive-diagnosis page | Brief explanation applied to the symptom | What this particular finding contributes |
| Why an examination may use unfamiliar tasks | Shared examination-purpose page | Reassurance and relevant examples | Purpose of each actual manoeuvre |
| What scans, recordings and other tests answer | Shared tests-and-investigations page | Symptom-specific questions, indications and limits | Exact investigation protocol and interpretation if that is the page's subject |
| Understanding positive signs and their limits | Shared positive-signs page | How findings fit this symptom | Positive, negative, indeterminate and confounded results |
| Variability and internal inconsistency | Shared variability page | Actual time course and task-related patterns | The precise comparison; alternative explanations |
| Differential diagnosis | Shared diagnostic-reasoning page | Relevant alternative explanations and how clinicians distinguish them | Confounders and competing explanations for this finding |
| FND alongside other conditions | Shared coexistence page | Relevant coexistence, avoiding either/or reasoning | Why a positive result does not exclude other disease |
| Explaining the diagnosis | Shared explanation page | What was found and what that means for this symptom | A brief example of explaining this result |
| Supporter role before/during/after assessment | Shared supporter page | Symptom-specific observations, access and consent | No separate supporter section; link back to symptom context |
| Lived experience, appearance, symptom impact | Symptom page | Preserve individual voice and qualifiers | Only technique-specific experience needed to explain the examination |
| Possible mechanisms | Symptom page, linked to existing course background | Symptom-specific models, evidence and uncertainty | Relevant anatomy/physiology; do not infer an individual mechanism from a sign |
| How the manoeuvre is performed | Technique page | Short when-use summary and link | Full clinician-oriented sequence, suitability, safety and limits |
| Immediate safety and new/changed symptoms | Symptom page | Enough guidance to stand alone | Examination-specific precautions and stopping criteria |
| Rehabilitation exercises and flare management | Existing recovery pages | Short appropriate link; keep essential immediate safety | Link to recovery where useful; no duplicated recovery programme |
| Evidence | Each page independently | Local numbered citations and source table | Own sources, validation population, methods and limitations |

## Planned shared pages

**Implementation choice:** group foundations in `reference/diagnostic-concepts/`. Do not create empty linked stubs. The folder and its index will be added when real content is ready. Existing reference-landing links continue to lead to available material until their replacements are published.

| Planned filename | Owns | Existing material to consult; not permission to overwrite |
|---|---|---|
| `01-positive-diagnosis.md` | Diagnosis through positive clinical evidence | Module 2 positive-signs lesson; diagnostic collection introduction |
| `02-why-examination-tasks-are-used.md` | Purpose, explanation and consent for unfamiliar tasks | Module 2 examination lesson; repeated technique introductions |
| `03-tests-and-investigations.md` | Questions answered by tests; normal/abnormal results and limits | Module 2 tests and uncertainty lesson |
| `04-understanding-positive-signs.md` | Interpretation, sensitivity/specificity and uncertainty in plain language | Diagnostic index and local evidence notes |
| `05-variability-and-internal-inconsistency.md` | Context-dependent function and competing explanations | Module 3 network/attention material; symptom-specific variability passages |
| `06-differential-diagnosis.md` | Considering and distinguishing explanations | Module 2 tests/uncertainty material |
| `07-fnd-and-other-conditions.md` | Coexistence and avoiding diagnostic overshadowing | Module 2; existing co-occurring-condition collection, linked rather than duplicated |
| `08-explaining-an-fnd-diagnosis.md` | Explaining findings, uncertainty and next steps | Module 2 and existing symptom explanations |
| `09-supporting-someone-through-assessment.md` | Permission, useful observations, communication and access | Existing supporter sections; retain symptom-specific details locally |

These are proposed editorial topics, not a fixed clinical-technique count. Combine shared topics later if substantive duplication remains; record the change.

## First symptom: functional limb weakness

Keep the current path `reference/diagnostic-signs/01-functional-limb-weakness.md` as the symptom page. Proposed technique home: `reference/diagnostic-signs/functional_limb_weakness/`; first page `01-hoovers-sign.md`. Preserve stable incoming symptom anchors or provide deliberate redirects/links when relocating material.

| Existing block | Planned treatment | Preservation/review requirement |
|---|---|---|
| Human-draft banner; Refers to; Scope boundary | Keep at symptom level; refine only through reviewed edits | Preserve attribution and scope distinctions |
| Featured technique; diagnostic method; technique scope | Condense into Quick Reference; transfer full scope to Hoover's page | Do not make Hoover's the whole symptom assessment |
| Sixteen “at a glance” entries | Preserve baseline; classify and link as details are written | Sixteen entries do not automatically mean sixteen new pages |
| Opening lived-experience description and first project-lead quotation | Keep on symptom page | Preserve wording and one-person qualifier |
| “What Hoover’s sign can show” | Move detailed manoeuvre and anatomy to Hoover's page; leave concise explanation/link | Carry citations and limitations with the passage |
| Second project-lead quotation about an arm examination | Keep in symptom explanation of the value of positive findings | Preserve verbatim quotation and the correction that Hoover's is a leg sign; do not imply the described arm task was a validated Hoover variant |
| Episodic/fluctuating weakness | Keep diagnostic time course and reassessment context | Recovery practice belongs in recovery pages; essential safety remains local |
| Supporter sections | Retain assessment preparation, useful observations, consent and explanation | Relocate detailed rehabilitation cues only with traceable mapping to existing recovery coverage |
| Clinician phenotype and upper-limb comparisons | Keep symptom-level clinical reasoning | Do not turn variability alone into a diagnostic test |
| Nine-step Hoover outline, anatomy and accuracy discussion | Transfer together to Hoover's page after source recheck | Preserve confounders, small-study limits, negative-result limits and explanation |
| Media contributor brief | Move to Hoover's page | Retain consent, true sequence, correct side labels and accessible description |
| Citation table | Split by actual claims retained or moved | Both resulting pages stand alone; keep stable central IDs and update current uses |
| Existing audience menus and footer | Symptom page retains audience sections; technique uses topic menus | Navigation must match the different page structures |

### Image provenance

An existing asset is [functional-weakness-hoovers-sign-infografik-09-2027.png](../../assets/images/functional-weakness-hoovers-sign-infografik-09-2027.png). No Markdown reference to its filename was found at the preparation baseline. Do not rename the dated filename. Inspect it against the intended manoeuvre and verify attribution/alt text before attaching it to Hoover's page. There is currently no embedded image in the weakness page to mechanically move.

### Disposition of the sixteen weakness entries

These are editorial routing decisions based on the current inventory, not a new clinical validation.

| Existing entry | Initial destination or action |
|---|---|
| Hoover’s sign | First detailed weakness technique page |
| Hip-abductor sign | Candidate weakness technique page |
| Drift without pronation | Candidate upper-limb weakness technique page |
| Paradoxical wrist flexion | Candidate upper-limb weakness technique page |
| Elbow flex-ex sign | Candidate upper-limb weakness technique page |
| Give-way/collapsing weakness | Limited-specificity observation; preserve cautions in a focused explanation |
| Make-versus-break dynamometry | Instrumented assessment candidate; retain protocol limits |
| Task-related motor inconsistency | Assessment principle with symptom-specific examples; shared concept plus local application |
| Quantitative Hoover testing | Instrumented variant; decide whether subsection or separate page after evidence review |
| Isokinetic strength testing | Specialist/limited-evidence investigation; do not label a routine required test |
| Antagonist co-contraction | Observation; assess overlap with isokinetic evidence before deciding page boundaries |
| Sternocleidomastoid sign | Adjunct axial sign; explain indirect relationship to limb weakness |
| Platysma comparison | Adjunct observation; assess whether it belongs with neck-sign evidence |
| Abduction-finger sign | Canonical detailed home under paralysis; weakness page links with scope boundary |
| Spinal Injuries Center test | Canonical detailed home under paralysis; weakness page links with scope boundary |
| Arm/hand-drop avoidance | Retain caution and link to unresponsiveness discussion; never convert into a weakness manoeuvre tutorial |

## Clinician-awareness addition — September 24, 2026

The [core principles](core-principles.md#write-with-the-whole-clinical-team-in-mind) now also require profession-aware wording, interpretation of assessment limits, and evidence on everyday function, quality of life and mental health. Apply this before the first expansion.

For functional weakness, plan language useful to neurology and general practice as well as occupational therapy, physiotherapy and psychological care. At symptom level, investigate what clinical findings mean for activities, repeated performance, assistance, participation and recovery cost. At Hoover's-sign level, distinguish the diagnostic comparison from measurement of overall disability. Preserve human experience as attributed experience, and obtain sources for broader conclusions.

Shared concepts own recurring assessment-versus-life-impact explanations; symptom pages own their application and related evidence; technique pages retain the specific interpretation limit and a link. Recovery pages should apply the same principles when next edited. This is an addition to the ownership plan, not authorization to infer disability from a single test or to introduce unsupported clinical claims.

## Implementation sequence

1. Review this ownership map and baseline; preserve the current human material and source associations.
2. Draft shared foundations needed by the first symptom, with evidence checks and existing-course cross-links. Publish only complete pages, not placeholders.
3. Prepare the weakness symptom revision and Hoover's page together so relocation leaves no gap. Keep a short Quick Reference at the top; use the structures in the linked authoring document.
4. Compare old/new human passages, citations, image treatment and all sixteen inventory entries. Record every move, split or combination.
5. Repair navigation, indexes, citation uses, `SITEMAP.md` and `sitemap.xml` together; check local files/anchors and rendered structure.
6. Open a reviewable pull request. Do not merge automatically. Continue subsequent techniques/symptoms in reviewable batches without a fixed page target.

## Completion boundary

This preparation is complete when the inventory, ownership map, structures and maintenance rules agree. Clinical-source revalidation, shared educational pages, the weakness rewrite and the Hoover's page remain the next implementation stage. No diagnostic expansion is represented as finished by this preparation.


<!-- NAV-CONTEXT:START -->
**Project:** [Preparation plan](diagnostic-expansion-preparation.md) · [Baseline inventory](diagnostic-expansion-baseline.md) · [Authoring structures](diagnostic-page-authoring-structures.md)

**Navigate:** [Home](../../README.md) · [Course](../../course/README.md) · [Reference Library](../../reference/README.md) · [Site Map](../../SITEMAP.md)
<!-- NAV-CONTEXT:END -->
