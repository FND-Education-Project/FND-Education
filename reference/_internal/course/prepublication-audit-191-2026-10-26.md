# PR #191 — publication-readiness audit

**Date:** October 26, 2026 (America/Vancouver). **Draft baseline:** `05f610ae735d25e01d29b367114b69e4a854e93a`. **Main baseline:** `e1d9f85521561fc427a5795f088c7996ce1924b8`.

## Purpose and completion standard

Robert requested an audit complete when #191 can be merged to publish automatically generated lessons while he develops human-authored versions. This supersedes the earlier documentation-only restriction. This is a **prepublication readiness pass**, not either of the two later human-revision audits. No merge was requested or performed.

The existing Module 5 Audit 1 and Audit 2 reports were read to distinguish scope: later Audit 1 reviews the human revision's evidence, safety, omissions, Reference/glossary alignment, quotations, citations, assets and metadata; later Audit 2 applies accepted corrections and reviews voice, pace, clarity, repetition, accessibility and final presentation. Publication requires enough overlap now to prevent unsafe, unsupported, broken or misleading working content, without claiming either later audit completed or rewriting the author's eventual voice.

## Delivered publication set

- 16 complete lessons, overall reading positions 15–30, across new Modules 6–10; **48 audience sections** plus Research and Sources.
- Five module overviews and a current course landing: **19 core modules, 57 focused lessons**.
- New canonical sources under `course/concepts-first/`. Exact source/route/slot mapping: [lesson inventory](publication-191-lessons.json).
- New topics use `/course/v2/m6/` through `/course/v2/m10/`; local lesson suffixes are 1–3 or 1–4. Display position and internal slot are separate.
- Existing 75 lessons, 23 module entry points and all deep anchors remain reachable at original addresses. Nine superseded modules (34 lessons) have an earlier-edition banner and separate navigation; they do not interrupt the current course.
- Retained later modules receive current display positions 11–19, with source prose, original route and identity preserved. Schema and breadcrumb parents use actual routes.
- Total publication inventory: **28 module entry points, 91 focused lessons, 120 course routes and 450 public routes**. These include earlier-edition material, not 28 current modules.
- Original illustrations, puzzles, colouring files and their labels remain with their original content. No old puzzle is relabelled as a new lesson. The new lessons have no artwork/activities yet; that is not an initial-text publication blocker.

## Required fixes completed

| Area | Finding and correction |
|---|---|
| Publication | Internal drafts were not generated publicly. Integrated actual course pages, overviews, landing links and sitemap entries rather than treating a documentation merge as publication. |
| Identity collision | Original `m6-1` means seizure teaching, not attention. New source slots 24–28 and distinct routes prevent collision; no completion transfer, database rename, redirect to unrelated material or unknown-history deletion. |
| Reading sequence | Core navigation is foundations/safety → concepts → symptom description → rehabilitation → pacing → retained later material. Earlier pages use a separate path returning to the current course. |
| Metadata | New lessons remain **automatically generated working drafts**; plain summaries, review dates, source tables, four-link audience menus and three audience-end navigation controls are present. No human-authored label is assigned. |
| Attention | Removed the categorical assertion that nothing is wrong with the reader's eyes or ears. The scene now allows hearing, vision, language and other contributors. General attention and selected tremor evidence remain distinct. |
| Prediction/agency | Models, ordinary examples, group findings and individual uncertainty remain separate. Removed “without exaggeration” from the personal observation prompt; no implication that symptoms are chosen or overcome by belief. |
| Diagnostic interpretation | Entrainment is rhythm adoption, not stopping/suppression. Symptom scenarios remain unresolved and do not offer home diagnostic tests. Awareness, responsiveness and later recall stay distinct. |
| Symptom scope | Preserved specific clinical applications for all 17 library presentation families. PPPD is identified as a defined functional vestibular disorder, not a diagnosis inferred from FND/dizziness. Cough/airway complaints are not automatically FND. |
| Rehabilitation evidence | Physio4FMD retains active comparator and primary-versus-secondary outcome distinctions; CODES and later AAN guidance are not collapsed into one verdict. Neuroplasticity is not programme efficacy or a cure promise. |
| Pacing | Standardized the Lesson 29 title to avoid promising avoidance of all boom-and-bust. Delayed worsening/ME/CFS boundaries remain condition-specific; no fixed increments or provoked crash. |
| Role boundaries | Supporters offer invited adaptations and sustainable assistance. Diagnosis, risky practice, clinical techniques and treatment/medication decisions remain with appropriate professionals. Access support is not conditional on symptom improvement. |
| Links/sources | Replaced GitHub library trees and internal R-key drafting references with public-compatible destinations, numbered citations and permanent citation records. Kept glossary linking selective. |
| Quotations | Checked original public indexed text/context; retained 17 suitable extracts and held seven candidates back from public content. Corrected silently normalized punctuation/wording where necessary. No quote is treated as efficacy evidence. |

## Evidence checks and limits

The [research source register](new-lessons-research-2026-10-26/sources.md) records sources and retrieval limits. Source records already present were reused, including PT 0028, OT 0011, SLT 0025, tremor 0220, FCD 0071, tics 0110, PPPD 0027, Physio4FMD 0029, CODES 0033, AAN 0010 and the Bayesian framework 0242. Seven missing general/mechanistic source records were added (0301–0307). New public community records use 0308–0322 with the duplicate parent-thread allocation removed; the parent thread already registered as 0299 is reused. Unused permanent numbers are not reassigned.

Original abstracts/indexed original text and official guidance were checked for the consequential claims. Specifically rechecked: 2026 cardiac interoception findings (44 mixed-FND/48 controls, different measurement types, nonsignificant heartbeat-counting comparison); Physio4FMD's prespecified endpoint/comparator; CODES' 12-month seizure-frequency endpoint; 2026 AAN “possibly effective” interpretation; NICE ME/CFS fixed-increment restriction; FCD positive features and comorbidity; tic-like phenomena guidance; and Bárány PPPD criteria/scope. Earlier source checks in this PR cover general attention, automaticity, agency, interoception definitions and rehabilitation consensus.

Some journal pages challenge automated access and NICE returned 403 for direct retrieval. Search-indexed original content/abstracts supported the narrow summaries; full-text appraisal of inaccessible material is not claimed. Narrative adaptations and interdisciplinary worked examples remain explicitly illustrative rather than trials of those exact methods. No individual prognosis, uniform causal recipe, treatment dose or guaranteed outcome is supplied. Independent clinical sign-off is not claimed.

## Community source review

[Retained excerpt map](publication-191-quotes.json) records text, destination, role context and use. Accessible original public indexed text was read for exact wording and context, including the parent’s nonreproducible OT encounter, spouse’s appointment consent, memory-timeline account, mobility-aid participation, referral questions, variable activity, caregiver strain and response to cure claims. Unrelated treatment advice, prognosis percentages and causal claims elsewhere in those discussions were not imported. No usernames, child ages or additional identifying details are reproduced in the lesson prose.

Held back: three Supporter candidates (Q048, Q051, Q096) where the exact quoted text was not adequately matched together with speaker context in this pass, and four Person candidates (two walking outcomes, altered boom-and-bust wording, and the boundary-testing quotation). Some held-back wording was found, but exactness/context or suitability was insufficient to justify publication as drafted. Internal draft originals retain them for later editorial work. Distinct excerpts from the same thread are not independent research participants.

## Account compatibility and rollback

No Worker, D1 schema, login, preference, session, CSRF, export/delete, or stored learner row changes are part of this release. Existing original course keys and paths are preserved. New lessons have reserved source slots `m24-*`…`m28-*`, **not accepted API IDs**, and generated `course_progress_eligible: false`. There is no live new-lesson cloud progress integration in this PR. Public reading does not require it. A later #154 implementation must consume this eligibility flag or its equivalent reviewed manifest rule; never infer identity from visible “Module 6.”

The separate #154 source contract still omits original `m4-2`. That bug is not evidence of a live learner-data state and remains account-PR work. No production account/D1 credentials or learner records were accessed. Browser two-account migration acceptance is unnecessary for a release that performs no state/contract migration; it remains mandatory before any later account integration changes. Original routing/identity is directly regression-tested. Earlier offline account checks remain baseline evidence only, not newly claimed live tests.

Rollback is a source/build revert of this publication commit: the original course files, URLs, assets and account data still exist. It may remove access to newly published routes, so do not overwrite later human text without reviewing subsequent commits. No learner-data reverse migration is required because no learner-data migration occurs.

## Verification and follow-up

- Source preparation and validator: 450 public routes, with internal authoring/review documents excluded.
- Five regression tests cover all 75 original lesson URLs/keys, 16 disjoint new identities, eligibility, 19/57 core counts and order, separate earlier navigation, correct schema parents, audience structure and citation anchors.
- New canonical relative paths and glossary/source fragments checked; exact community/source figure mappings checked.
- Original `course/part-*` content, archived human files, glossary, public Reference prose and uploaded artwork/puzzles are unchanged.
- Final clean Jekyll/Pagefind/rendered-artifact build and visual checks are recorded in PR #191 after the final commit. Do not mistake an older build for the final head.
- Relevant open PRs #154, #177 and #178 receive explicit handoffs. #191 is prepared for merge by Robert; no merge/deployment performed by this audit.

Later human-revision audits should begin with the integrated canonical lesson files, not re-integrate the internal drafts or change identity based on display numbering. Recheck claims affected by human edits, new media and quote changes; complete the usual later citation/asset/voice checks at that point.
