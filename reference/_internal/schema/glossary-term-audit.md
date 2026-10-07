# Glossary and Structured-Data Audit

**Status:** Internal audit for the `schema-sitewide-glossary` branch.

**Scope:** This audit covers only the site-wide Schema.org graph and the glossary. Page-level `WebPage`, `Article`, `CollectionPage`, `MedicalWebPage`, breadcrumb, citation and audience schema are deliberately deferred.

## Decisions

- Keep the public glossary as one Schema.org `DefinedTermSet`.
- Keep every glossary entry a `DefinedTerm`; do not make the lexical term itself double as a medical condition, symptom, test or treatment.
- Store the semantic classification of what each term refers to in the internal `glossary-type-map.json`.
- Expose a stable `termCode` for each public `DefinedTerm`.
- Require exact agreement between the canonical glossary and the internal type map; unmapped terms and stale map entries fail the build.
- Remove the old visible `Type:` labels from glossary Markdown because they had grown to 45 inconsistent free-text labels across 60 entries.
- Do not require additional schema metadata in public Markdown.
- Use `WebPage` as the conservative future default for page-level schema. `MedicalWebPage` will require an explicit authority signal and is not part of this branch.
- Breadcrumb schema is deferred.

## Glossary audit outcome

The original glossary contained **72 entries**. The audit compared it with the controlled search subject index, diagnostic and recovery indexes, and recurring technical vocabulary in public Course and Reference material.

The final glossary contains **109 entries**.

### Added vocabulary

The 37 added entries are:

- Acceptance and Commitment Therapy (ACT)
- Augmentative and alternative communication (AAC)
- Autonomic arousal
- Automatic and task-oriented movement
- Biofeedback
- Cognitive behavioural therapy (CBT)
- Co-contraction
- Comprehensive Behavioral Intervention for Tics (CBIT) / habit reversal
- Desensitization / graded sensory reintroduction
- Differential diagnosis
- Drift without pronation
- Dual-tasking / dual-task practice
- EEG-EMG and jerk-locked back averaging
- Electromyography (EMG)
- Functional cough and upper-airway symptoms
- Functional dystonia / fixed dystonia
- Functional electrical stimulation (FES)
- Functional jerks / functional myoclonus
- Functional swallowing symptoms / functional dysphagia
- Functional visual symptoms
- Give-way / collapsing weakness
- Globus / globus sensation
- Graded exposure / graded trigger practice
- Grounding
- Habituation
- Optokinetic response / optokinetic testing
- Pacing
- Persistent postural-perceptual dizziness (PPPD)
- Photophobia
- Proprioception
- Scan-negative cauda equina presentation
- Selective serotonin reuptake inhibitor (SSRI) / serotonin-norepinephrine reuptake inhibitor (SNRI)
- Sensory trick
- Swivel-chair assessment
- Transcutaneous electrical nerve stimulation (TENS)
- Vestibulo-ocular reflex (VOR)
- Whack-a-mole sign

### Consolidated or normalized headings

Four existing headings were consolidated or normalized rather than creating duplicate glossary entries:

- `Drop attack` → `Drop attack / functional drop attack`
- `Functional speech or voice symptoms` → `Functional speech and voice symptoms`
- `Functional weakness` → `Functional limb weakness / functional weakness`
- `Functional tic-like symptoms` → `Functional tics / functional tic-like symptoms`

The whole glossary term section was also re-sorted alphabetically; earlier drift had placed some I/M terms inside the F section.

## Terms deliberately not added merely because they are search subjects

The subject index contains broad navigational concepts that remain useful for search but do not need to become glossary entries. Examples include:

- FND diagnosis
- tests and investigations
- recovery techniques
- medical safety and new symptoms
- emergency planning
- daily living with FND
- supporter guidance
- work/school accommodations
- relationships, identity and grief
- reviewing progress
- history of FND

The glossary is therefore a terminology resource, not a duplicate site map or subject index.

## Internal semantic type map

`reference/_internal/schema/glossary-type-map.json` contains **109 mappings across 13 semantic categories**:

- therapy / rehabilitation
- communication access
- neuroscience / research concept
- clinical framework / concept
- positive diagnostic sign
- diagnostic test / assessment
- FND condition / presentation
- other condition / diagnosis
- symptom / clinical feature
- terminology / classification
- medication class
- safety concept / presentation
- community / project language

These categories are intentionally internal. They describe what a term refers to; they are not emitted as extra Schema.org `@type` values on the `DefinedTerm`.

## Site-wide schema implemented

Every normal rendered site page receives one JSON-LD graph containing:

- `Organization` — FND Education Project
- `WebSite` — FND Education Project website
- `MedicalCondition` — one canonical Functional Neurological Disorder entity

The glossary page additionally receives:

- one `DefinedTermSet`
- 109 `DefinedTerm` entries

Stable `@id` values connect the site-wide entities and glossary set.

## Build and rendered-HTML validation

Draft PR #117 was used to run the existing Pages workflow without deploying the branch.

Initial full build result on October 7, 2026:

- site preparation: passed
- generated-source validation: passed
- Jekyll production build: passed
- reviewed subject-search metadata: passed
- Pagefind index: passed
- built-artifact validation: passed
- public routes: 428
- built HTML files checked: 430
- Pagefind pages indexed: 428

The built-artifact validator parses the actual rendered `<script type="application/ld+json">` block. It verifies:

- valid JSON on each normal site page;
- exactly one site-wide `Organization`, `WebSite` and FND `MedicalCondition`;
- stable expected `@id` values;
- glossary schema appears only on `/glossary/`;
- exactly one `DefinedTermSet` on the glossary;
- every glossary member is a `DefinedTerm`;
- every term has a name, description and `termCode`;
- no duplicate term codes;
- every term points back to the same `DefinedTermSet`;
- public term codes exactly match the internal reviewed map.

## Deferred work

The following are intentionally outside this schema round:

- page-level `WebPage` / `Article` / `CollectionPage` classification;
- `MedicalWebPage` authority rules;
- breadcrumb schema;
- page `about` / `mentions`;
- citation / `ScholarlyArticle` relationships;
- audience schema;
- reviewer and medical-review metadata.
