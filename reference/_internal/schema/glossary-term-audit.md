# Glossary Term Audit — Before Semantic Type Mapping

**Status:** Internal working audit. No public glossary changes are made by this file.

**Purpose:** Check whether the current public glossary contains the terminology readers are likely to need before a one-time semantic type map is created for schema/search use.

## Method

This audit compares the current 72-entry glossary with:

- the 95 reviewed subjects in `tools/search/subject-index.json`;
- the published diagnostic-sign and recovery-technique indexes;
- recurring technical terminology found across public Course and Reference pages;
- terms that are useful because their meaning is specialized, easily misunderstood, abbreviated, or important to FND diagnosis/rehabilitation.

A search subject is not automatically a glossary term. Broad page topics such as daily living, supporter guidance, work accommodations, and history can remain search subjects without becoming glossary entries.

## Existing glossary strengths

The glossary already covers many of the concepts most likely to be misunderstood, including:

- FND and functional neurological symptoms;
- functional weakness, paralysis, tremor, gait, sensory, facial, speech/voice and seizure terminology;
- positive diagnosis, positive signs, inconsistency, incongruence, distractibility, entrainment and Hoover's sign;
- functional/dissociative seizure terminology, PNES, epilepsy and video-EEG;
- agency, attention, interoception, predictive processing and biopsychosocial terminology;
- dissociation, diagnostic overshadowing, malingering/feigning, psychogenic and medically unexplained symptoms;
- rehabilitation, neuroplasticity, relapse/setback, external focus, spoon theory and available capacity;
- functional tic terminology and several related tic terms;
- nociplastic pain, orthostatic intolerance, PEM, insomnia, IBS and tinnitus.

## Recommended additions before the semantic map

These terms are strong candidates because they are important named concepts, symptom groups, diagnostic signs/tests, rehabilitation terms, or abbreviations that readers encounter on the site and may reasonably need defined.

### FND presentations and overlapping conditions

- **Functional jerks / functional myoclonus / myoclonus**
- **Functional dystonia / fixed dystonia**
- **Functional visual symptoms**
- **Functional swallowing symptoms / functional dysphagia**
- **Globus / globus sensation**
- **Functional cough / upper-airway symptoms**
- **Functional drop attacks** — distinct from the existing generic `Drop attack` entry
- **Persistent postural-perceptual dizziness (PPPD)**
- **Scan-negative cauda equina presentation / scan-negative cauda equina syndrome**
- **Photophobia**

### Diagnostic and examination terminology

- **Differential diagnosis**
- **EMG / electromyography**
- **EEG-EMG and jerk-locked back averaging**
- **Swivel-chair assessment**
- **Optokinetic response / optokinetic testing**
- **Drift without pronation**
- **Give-way / collapsing weakness**
- **Whack-a-mole sign**
- **Sensory trick** — with care that this term is used differently across movement disorders
- **Co-contraction**

### Rehabilitation and treatment terminology

- **Pacing**
- **Graded exposure / graded trigger practice**
- **Dual-tasking / dual-task practice**
- **Automatic or task-oriented movement**
- **Grounding**
- **Desensitization / graded sensory reintroduction**
- **Habituation**
- **Biofeedback**
- **Proprioception**
- **AAC / augmentative and alternative communication**
- **CBIT / Comprehensive Behavioral Intervention for Tics**
- **ACT / Acceptance and Commitment Therapy**
- **CBT / cognitive behavioural therapy**
- **TENS / transcutaneous electrical nerve stimulation**
- **FES / functional electrical stimulation**
- **VOR / vestibulo-ocular reflex**

## Possible additions that need an editorial decision

These are valid site concepts, but they may be too broad, too ordinary, or better explained on their dedicated pages rather than in the glossary:

- diagnostic uncertainty;
- diagnostic techniques;
- movement retraining;
- sensory retraining;
- multidisciplinary FND care;
- autonomic arousal;
- migraine;
- fibromyalgia;
- persistent pain;
- fatigue;
- autonomic symptoms;
- sleep problems;
- SSRI and SNRI;
- professional names such as neurologist, physiotherapist, occupational therapist, speech-language pathologist, psychologist, psychiatrist and primary-care clinician;
- accessibility and living terms such as mobility aid, sensory overload, self-advocacy and safety plan.

These should be added only if the glossary is intended to function as a broader vocabulary/search aid, not merely as an unfamiliar-term dictionary.

## Search subjects that should not become glossary entries merely because they exist

The controlled subject index also contains navigational/topic concepts such as:

- FND diagnosis;
- tests and investigations;
- FND recovery and rehabilitation;
- recovery techniques;
- medical safety and new symptoms;
- emergency planning;
- daily living with FND;
- work/school accommodations;
- supporter guidance;
- relationships, identity and grief;
- reviewing progress;
- history of FND.

These are useful search subjects and page groupings, but they are not necessarily vocabulary terms. The glossary should not become a duplicate site map.

## Recommendation

Before creating the semantic type map:

1. Review the **Recommended additions** list and add the terms we want to the canonical glossary.
2. Decide whether the glossary should remain an unfamiliar-term reference or also become a broader controlled vocabulary for search.
3. Only after the term set is stable, create the one-time internal semantic map.
4. Keep every glossary item a Schema.org `DefinedTerm`; the semantic map describes what the term refers to and does not replace `DefinedTerm`.
5. Keep the future map and schema audit under `reference/_internal/schema/`, which is excluded from publication.

## Current counts

- Current glossary entries: **72**
- Controlled search subjects: **95**
- Many subjects do not have a one-to-one glossary entry, by design.
- Current free-text `Type:` labels: **45 distinct labels across 60 tagged entries**; these should be normalized only after the glossary term set is settled.
