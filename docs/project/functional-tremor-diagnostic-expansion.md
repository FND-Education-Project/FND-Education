# Functional tremor: staged diagnostic expansion

September 27, 2026. Automatically generated implementation record; movement-disorders, neurophysiology, lived-experience and accessibility review pending.

## Scope and branch relationship

The September 27 project review supported the shared-concepts → symptom → technique architecture and separate diagnosis/recovery editorial collections using common minimal layouts. This stage applies the [authoring structures](diagnostic-page-authoring-structures.md) and [ownership plan](diagnostic-expansion-preparation.md) to the next symptom.

This branch is based on `codex/first-diagnostic-expansion` at `e0ee1c6` (PR 83), so it retains the reviewed weakness draft and shared foundations without merging any pull request. The new pull request targets that branch for an incremental review. The `migrate-to-pages` branch has continued course-navigation work through `37dc3a2`; no template or generator changes are included here. Reference Markdown remains canonical, and reference website publishing remains pending. Existing root sitemap URL conventions are preserved.

This stage adds **two detailed diagnostic pages and one preserved inventory**, plus this project record. The two pages explain different clinical comparisons, previously combined in one outline. There is no target of twelve expanded pages and no new symptom category. The repository still has 17 diagnostic symptom overviews and the historical 170-entry baseline; that baseline is unchanged.

## Content ownership and preservation

| Earlier material | Current destination and treatment |
|---|---|
| Scope and symptom appearance | [Functional tremor overview](../../reference/diagnostic-signs/02-functional-tremor.md), with short Quick Reference |
| Time course and clinical phenotype | Retained at symptom level, with differential and everyday-impact context |
| Combined distractibility/entrainment outline | Split into [distractibility](../../reference/diagnostic-signs/functional_tremor/01-distractibility.md) and [entrainment](../../reference/diagnostic-signs/functional_tremor/02-entrainment.md); clarified change versus actual rhythm matching |
| Twelve original inventory descriptions | Copied intact into the [inventory](../../reference/diagnostic-signs/functional_tremor/technique-inventory.md); source numbering 1–13 and old symptom anchors retained |
| Combined media brief | Continuous baseline/task comparison retained on entrainment; separate distractibility scope; accessible transcript and consent added |
| Familiar-flare treatment cues | Linked to the existing [recovery overview](../../reference/recovery-techniques/02-functional-tremor.md), which already covers one agreed cue, practical support and hazardous tasks; no new recovery technique added |
| Supporter role | Expanded around consent, access, useful observations, examination and follow-up |
| Shared recurring explanation | Reuses existing positive-diagnosis, investigations and everyday-function pages; no duplicate foundation pages |

The earlier tremor page was marked automatically generated and contained no attributed human quotation. Existing useful passages were retained or redistributed. No patient quotation was created. Editorial example explanations and practical questions are distinguished from evidence and diagnostic criteria.

## Twelve-entry disposition

| Original entry | Stage completed or pending |
|---|---|
| Variability | Brief inventory retained; contextual interpretation on symptom page; detailed expansion pending |
| Distractibility | Detailed page drafted |
| Entrainment | Detailed page drafted |
| Tapping performance | Retained inventory; feasibility distinguished from entrainment in the detailed page; full component review pending |
| Ballistic-movement interruption | Retained inventory; not relabelled as the general distraction outline |
| Tonic coactivation at onset | Retained laboratory observation; detailed review pending |
| Loading response | Retained specialist comparison; detailed review pending |
| Interlimb coherence | Retained laboratory comparison; detailed review pending |
| Wavelet coherence analysis | Retained specialist method; detailed review pending |
| Combined electrophysiological battery | Retained; battery evidence summarized with scope limits, not expanded into a complete protocol |
| Whack-a-mole sign | Retained optional observation and restraint caution; detailed review pending |
| Suggestibility | Retained limitations and consent boundary; no deceptive or painful provocation tutorial |

## Evidence checked and limits

- Full-text material checked: 2011 Schwingenschuh development study (FND-CIT-0177), 2018 Merchant case report (0154), 2020 Bartl review (0019), 2024 IFCN chapter (0022), Huys attention study (new 0220), Gelauff cohort analysis (new 0221), Murgai/Iskhakova exploratory series (new 0222), and tremor classification consensus (new 0223). NHS stroke advice (0108) checked for the concise emergency boundary.
- The 2016 validation (0178) and June 2026 meta-analysis (new 0224) were available at abstract level. Full main texts were not retrieved. Do not mark the primary-methods or meta-analysis risk-of-bias review complete.
- Use the primary 2016 abstract's **38 functional and 73 comparison participants**. The IFCN review gives discrepant group counts (40 and 72) while reporting the same accuracy figures; this draft follows the primary report and does not repeat the review's counts.
- The 2011 entrainment finding (5/13 versus 0/25) does not make entrainment obligatory or infallible. The later ten-person series has no control group and cannot establish specificity. Apparent rhythm matching may involve mirror movement or coexisting tremor.
- The 2026 meta-analysis searched through February 2025 and reports heterogeneous electrophysiological methods. No pooled number is used as the accuracy of an individual bedside sign. Search/update date here is September 27, 2026; this is a targeted review, not a systematic search of every inventory entry.
- Everyday-function evidence comes from the Gelauff cohort (31 dominant-tremor participants among 160 classifiable cases), not from a diagnostic accuracy score. Selected recruitment, self-report, overlap and small subgroups limit individual inference. Mood or distress is not treated as proof of cause.

## Navigation and maintenance

Reading order: Hoover’s sign → tremor overview → distractibility → entrainment → functional jerks. The tremor inventory is a reference detour. Symptom audience menus and technique topic menus remain different authoring structures. Links are vertically stacked with the Pages-compatible final separator. Reference indexes, the course cross-link, paired recovery navigation, central citations, project records and both root sitemaps are updated.

## Pending review

Clinical reviewers should check source-faithful tasks, feasibility/adaptation boundaries, interpretation of overlapping rhythms and the applicability of limb data. Primary full texts and the 2026 synthesis require further access/review. Lived-experience and accessibility reviewers should assess clarity, comfort and practical relevance. No reference-site deployment or completed clinical approval is claimed.

## Validation completed

- Relative Markdown links and anchors passed across all 19 changed or new files. All earlier tremor heading/citation anchors remain, and the twelve original inventory descriptions are unchanged.
- The symptom has five complete audience menus; each technique has eight complete topic menus, a continuous source table and final collection navigation. Original source numbers 1–13 keep the same stable IDs.
- Sitemap XML parses without duplicate URLs; new pages occur in both maps. New central source IDs are unique. CRLF-aware whitespace checks passed.
- Pandoc rendering checked headings, anchors and source-table structure. Both the branch generator and latest migration generator (`37dc3a2`) prepared all 98 course documents against this content without changing canonical files.
- The generator still sends ungenerated reference links to GitHub `main`; these new draft destinations will therefore be unavailable in a published course until the content is integrated or reference generation is implemented. This PR does not deploy that output. Full Jekyll/browser rendering was not performed.
