# Module 12 — Work Audit 2, November 22, 2026

PR #210; source head reviewed: `91b32db091152a6674a3fb45a3acfae195451eea`. Separate THA PR #214 is reviewed against this parent and synchronized after these repairs. Merge order remains #210, then #214. No merge to main or deployment authorized or performed.

## Findings and decisions

| ID | Class | Exact location | Minimum action and resolution |
|---|---|---|---|
| R1 | Required | All four Module 12 pages, status block, line 7 | `Editorial status` made site preparation fail; restore parser-supported `Working draft` and `human authored`, preserving human approval and pending clinical status. Fixed. |
| R2 | Required | Lessons 36–38, Research and Sources; L37 citation 5 | Complete Higson bibliography, repair split table, add missing actual sources and stable IDs, remove unused CODES/AAN entries in L36/L38. Fixed without rewriting teaching. |
| R3 | Required | L36 Supporter, `Voices from other families`, Figures 1–2 | Original spouse/parent excerpts unavailable for independent verification. Preserve exact approved wording; report uncertainty beside source table and in FND-CIT-0355/0356. Access failures do not establish deletion. |
| R4 | Required | L37 Person and Supporter community excerpts; L38 Person and Supporter excerpts | Verified indexed original discussions; add numbered citations and Figure mappings for every display. Exact spelling/punctuation retained. |
| R5 | Required | `research/citation-index.md`, Module 12 current-use map | Record actual lesson usage and resource evidence types; new IDs 0350–0362. Fixed. |
| R6 | Required | THA inventory and generator; stacked PR #214 | Regenerate from each branch's current lessons; exclude adjacent artwork/transitions; rebase copied relative links. Resolve parent conflicts while preserving approved THA regions. See separate THA report. |
| R7 | Required | Current syllabus link and legacy-named psychological-treatment syllabus | Align visible module number, lesson links and Lesson 38 title with approved course; physical syllabus filename retained. Fixed. |
| W1 | Worthwhile | L38 Further reading; L37 CBT definition | Selective existing communication-access Reference Library link and CBT glossary link, with no new teaching paragraphs. |
| W2 | Worthwhile | Curriculum/browser checks; Pages PR trigger | Extend reviewed-module checks to 12 and enable build-only checks on the stacked base branch. Deployment remains main-only. |
| U1 | Unnecessary | All nine audience narratives; L36 `Three questions, not one`; all THA sets | No general stylistic rewrite, extra limitation paragraphs, new warning blocks, or replacement of approved scenes. |
| U2 | Unnecessary | Lesson 38 crossword title | Preserve approved original PDF/clue title “Consent, Trauma, and Recognizing Harm,” filenames and grid. Lesson is correctly titled “Consent and Changing the Treatment Plan”; discrepancy documented by Audit 1, not a broken download. |

No substantive human-authored prose correction is proposed on the evidence reviewed. The initial four editorial decisions and separate eight THA decisions remain binding; these technical repairs do not reopen them.

## Evidence verification ledger

The citations below link to the original publications or authoritative guidance. Abstract-only verification is identified explicitly. Fictional cases illustrate reasoning, not observed clinical outcomes.

| Source | Independently checked; application and limits |
|---|---|
| [CODES, Goldstein 2020](https://doi.org/10.1016/S2215-0366(20)30128-0), FND-CIT-0033 | Original author-deposited full paper read. 368 adults; primary 12-month seizure-frequency difference not significant; seizure-free intervals and work/social functioning were secondary outcomes. L37 retains that distinction, not a cure claim. |
| [CODES HTA report, 2021](https://eprints.whiterose.ac.uk/id/eprint/212117/1/CODES%20FDS%20CBT%20RCT%20.pdf), 0351 | Original full report: 12 sessions plus booster, existing CBT training plus study-specific training/supervision, independent diary/questionnaire eligibility. Graham’s accommodations are fictional individualized proposals, not tested modifications. |
| [Re-PROGRAM, Higson 2026](https://pubmed.ncbi.nlm.nih.gov/42931745/), 0350 | Original abstract: 107 randomized, 96 analyzed; adults with video-EEG-confirmed FS, active epilepsy excluded. Five-session multicomponent intervention. Self-guided versus standard-care seizure rates significant; therapist-guided comparison and direct active-arm comparison not significant. No superiority/equivalence or mechanism proof inferred. PMC full text embargoed until October 26, 2027; complete paper/supplement not independently read. |
| [LaFrance 2014](https://pubmed.ncbi.nlm.nih.gov/24989152/), 0032 | Original abstract: pilot, 38 randomized/34 analyzed, four arms, 16 weeks; within-arm changes. Lesson describes CBT-informed treatment rationale without turning it into broad efficacy proof. |
| [Gutkin 2021](https://jnnp.bmj.com/content/92/1/36), 0077 | Original indexed article: heterogeneous CBT/PDT studies, mostly small/uncontrolled; no therapy ranking established. L36–37 appropriately frame possible benefit and individualized goals. |
| [BPS 2024](https://doi.org/10.53841/bpsrep.2024.rep181), 0078 | Full BPS-authored PDF read from the Infocop-hosted copy; publisher DOI endpoint unavailable. Matched care and collaborative formulation support individualized goals; professional briefing, not trial evidence. |
| [Bennett 2021](https://pubmed.ncbi.nlm.nih.gov/33479065/), 0001; Espay 2018, 0002 | Diagnostic framework: positive clinical features, comorbidity, no required psychological stressor. L36 separates the fictional psychologist’s causal assertion from accepted diagnosis and ongoing migraine care. Brain-network observations are not an individual diagnostic test or a psychological/neurological dividing test. |
| [Moreira 2023](https://doi.org/10.1111/epi.17752), 0352 | Original abstract: injuries occur in FS; observational prevalence estimates have heterogeneous certainty and settings. L37 makes no numerical personal-risk estimate or promise that CBT prevents injury. |
| [Williams 2024](https://pubmed.ncbi.nlm.nih.gov/38382188/), 0353 | Original abstract: eight later-onset participants, mixed-methods accounts of illness representations. Supports distinction between perceived control and reducing impact, not prevalence or universal causation. |
| [Baker 2021](https://doi.org/10.1136/jnnp-2021-326767), 0025 | Original consensus text: concerns about electronic aids in functional mutism. L38 fairly presents that concern as guidance and does not portray withdrawal as proven effective. The paper’s problematic selective-mutism description is not adopted. |
| [ASHA Practice Portal](https://www.asha.org/practice-portal/professional-issues/augmentative-and-alternative-communication/), 0106 | Original professional guidance read: individualized AAC and continued access, across conditions. Not an FND-specific efficacy trial. Relevant existing Reference Library record checked. |
| [CCPA Standards 2021](https://www.ccpa-accp.ca/wp-content/uploads/2021/10/CCPA-Standards-of-Practice-ENG-Sept-29-Web-file.pdf), 0354 | Original PDF pp.18–21 read: informed, accessible, continuing consent and right to withdraw. L38 qualifies age/applicable consent framework; no universal legal claim for all 17-year-olds. |
| [Ludwig 2018](https://pubmed.ncbi.nlm.nih.gov/29526521/), 0079 | Original abstract: case-control meta-analysis, heterogeneous group associations; people without reported stressors. Does not establish individual cause or indication for trauma therapy. |
| [Mcloughlin 2025](https://pubmed.ncbi.nlm.nih.gov/39241111/), 0069 | Original abstract: scoping review plus clinical experience; professional interactions, diagnostic overshadowing and other harm. L38 does not attribute a quantified treatment effect to it. |
| [Oxford workbook](https://academic.oup.com/book/1357), 0361; [Sheffield resources](https://non-epileptic-attacks.sites.sheffield.ac.uk/resources), 0362 | Publisher authors/year/access and university resource listings independently checked. Workbook is Reiter, Andrews, Reiter and LaFrance (2015); Sheffield materials include worksheets, not an asserted complete workbook. |

Clinical safety: existing new-symptom reassessment, coexisting migraine care, uncertain/unresponsive episode assessment, real seizure risk, optional seizure-story skip link, maintained communication access, and revisable consent are preserved. No new material safety omission identified. This is an evidence/editorial audit, not independent clinical review.

## Community quotations

- L36 spouse and parent: **unverified**, as R3. Do not call these independently authenticated or deleted.
- L37 focused-workbook participant and parent: exact retained excerpts recovered in the indexed [original January 30, 2025 thread](https://www.reddit.com/r/FND/comments/1idblzt). Participant describes early personal experience; parent describes comfort without symptom improvement. Format/subtype for the parent’s daughter is unspecified. Same thread, not independent treatment studies.
- L38 lonely/invisible and tiring-typing excerpts, plus adult child’s whiteboard excerpt: exact wording and conversational roles recovered in the indexed [original August 17, 2026 thread](https://www.reddit.com/r/FND/comments/1vpsiic/recently_diagnosed_fnd_complete_speech_loss/). Direct comment permalink not separately resolvable; thread-level context verified. No independent verification of anyone’s diagnosis.
- L37 fictional forum is explicitly fictional; fictional dialogue is not entered as research/community evidence. No scientific quotation requires altered wording.

## Assets and local validation

- Three originals visually inspected against approved captions/alt text; three colouring previews and PDFs match the characters and scenes. Preserve A/A/A placement and captions.
- All **15 PDFs** rendered and inspected: 12 crossword PDFs (three lessons plus module collection, easy/normal/key) and three colouring PDFs. No clipping or missing content observed.
- All **96 placed answers**, **528 grid cells**, crossing consistency, answer-key glyph positions, and **1,056 form widgets across eight editable PDFs** checked against the four source JSON files. Canonical AcroForm field counts agree with page widgets. This does not establish screen-reader usability.
- `prepare_site.py`, existing six curriculum tests extended through Module 12, and source validator pass. Inventory regeneration is deterministic and `--check` passes after repair.
- Browser/CI final-head results and final commit are recorded in the PR completion note after execution. Local runtime has no Ruby/Jekyll; GitHub Actions builds the actual Jekyll artifact and captures desktop/mobile review evidence.

## Outstanding status

Independent clinical review and full assistive-technology acceptance remain pending. Two L36 community sources remain unavailable; Re-PROGRAM full article is not independently reviewed. Lesson 38’s original puzzle title is intentionally retained. Module Audit 3 remains ahead. Nothing has been merged or deployed.
