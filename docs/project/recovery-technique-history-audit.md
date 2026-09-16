# Recovery Technique Lists: History Audit

**Audit date:** September 16, 2026. This audit concerns list provenance and page counts, not a fresh clinical validation of every intervention. The one restored gait example was checked against the existing physiotherapy consensus source.

## Finding and correction

The collections were not all expanded to twelve pages. However, page totals were presented without consistently distinguishing original numbered entries, split or merged entries, and additional treatment-review or care-planning pages. Functional seizures and functional sensory symptoms each originally listed **10 entries**, not 12. Calling all resulting pages separate recovery techniques was misleading.

The correction preserves useful content and existing links, restores the original grouping in each collection index, separates additional pages in the affected overviews and master index, and labels their role. No page is deleted merely to reach a preferred count. A numbered entry may itself describe several options or general care; neither original-entry counts nor document counts are counts of independently validated treatments.

## Method and historical baseline

The baseline is [commit `74138f3`](https://github.com/FND-Education-Project/FND-Education/commit/74138f34797ae840f794f0c809da64fad30dc401), immediately before [the first detailed limb-weakness expansion](https://github.com/FND-Education-Project/FND-Education/commit/563f1c8a8cfbf8236711667cf4ffe4c1cd9d2367). All seven expanded lists were also compared with the parent of their own expansion commit; their original numbered entries match this common baseline.

Count only the evidence-labelled numbered entries in the main rehabilitation/treatment lists. For seizures, include both the eight treatment/foundation entries and two grounding entries. Exclude numbered steps within flare instructions, source lists, README files, CBT resource-map documents and nested booklet plans. Current page counts include only the directly contained numbered detailed pages.

The first thirteen symptom lists were additionally checked against their initial recovery-reference commit, `a67567b`; their entry counts match the baseline. Facial symptoms, paralysis and drop attacks were added later and are counted from their lists at the common baseline. The table uses the symptom overview rather than the shorter, sometimes combined master-index bullets.

## Original counts for every symptom

| Symptom | Original numbered entries | Current detailed pages | Count explanation |
|---|---:|---:|---|
| [Functional Limb Weakness](../../reference/recovery-techniques/01-functional-limb-weakness.md) | 10 | 12 | 10 original entries became 12 pages by separating backward walking from foot sliding, and mirror feedback from treadmill/body-weight support. No extra list entry was needed. |
| [Functional Tremor](../../reference/recovery-techniques/02-functional-tremor.md) | 8 | 9 | 8 original entries became 9 pages because mirror feedback and surface-EMG feedback were separated. |
| [Functional Jerks or Myoclonus](../../reference/recovery-techniques/03-functional-jerks-and-myoclonus.md) | 8 | 9 | 8 original entries became 9 pages by separating activity/load planning from arousal regulation. The latter also elaborates startle-related selection; it is not a separately established treatment added by the count. |
| [Functional Dystonia or Fixed Posturing](../../reference/recovery-techniques/04-functional-dystonia.md) | 10 | 13 | 10 original entries map to 10 core pages: two merges (positioning with release; sensory contact with desensitization) offset two splits (mirror/EMG; complications/equipment). Three additional review/care pages brought the document total to 13. |
| [Functional Gait Disorder](../../reference/recovery-techniques/05-functional-gait-disorder.md) | 13 | 13 | 13 original entries still map to 13 pages: treadmill/support versus mirror feedback was split, while light-object/hand-task work and dual-task walking share one page. Equal totals therefore do not mean an unchanged one-to-one list. |
| [Functional Seizures](../../reference/recovery-techniques/06-functional-seizures.md) | 10 | 12 | 10 original entries map to 9 core pages after the two overlapping grounding entries were combined. One paediatric programme page and two care-planning pages bring the document total to 12. |
| [Functional Sensory Symptoms](../../reference/recovery-techniques/07-functional-sensory-symptoms.md) | 10 | 12 | The 10 original entries each have one detailed page. Two additional safety/planning pages bring the document total to 12; there were not 12 original techniques. |
| [Functional Visual Symptoms](../../reference/recovery-techniques/08-functional-visual-symptoms.md) | 9 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Speech and Voice Symptoms](../../reference/recovery-techniques/09-functional-speech-and-voice-symptoms.md) | 11 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Swallowing Symptoms and Globus](../../reference/recovery-techniques/10-functional-swallowing-and-globus.md) | 10 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Cough and Upper-Airway Symptoms](../../reference/recovery-techniques/11-functional-cough-and-upper-airway-symptoms.md) | 10 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Cognitive Disorder](../../reference/recovery-techniques/12-functional-cognitive-disorder.md) | 13 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Persistent Postural-Perceptual Dizziness](../../reference/recovery-techniques/13-persistent-postural-perceptual-dizziness.md) | 12 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Facial Symptoms](../../reference/recovery-techniques/14-functional-facial-symptoms.md) | 8 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Paralysis](../../reference/recovery-techniques/15-functional-paralysis.md) | 7 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Recovery and Safety Techniques for Functional Drop Attacks](../../reference/recovery-techniques/16-functional-drop-attacks.md) | 7 | Not yet expanded | Original symptom list remains the baseline for future expansion. |

## Original-entry to current-page mapping

“Split” and “combined” below describe editorial organization. They do not establish separate mechanisms or treatment efficacy. Additional pages are shown separately and excluded from original-entry counts.

### Functional limb weakness

10 original entries became 12 pages by separating backward walking from foot sliding, and mirror feedback from treadmill/body-weight support. No extra list entry was needed.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/01-functional-limb-weakness.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/563f1c8a8cfbf8236711667cf4ffe4c1cd9d2367)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Automatic, task-oriented movement | [Automatic and Task-Oriented Movement for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/01-automatic-and-task-oriented-movement.md) | One-to-one expansion; wording and examples may be updated. |
| 2. External focus or divided attention | [External Focus and Divided Attention for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/02-external-focus-and-divided-attention.md) | One-to-one expansion; wording and examples may be updated. |
| 3. Early supported weight-bearing | [Supported Loading and Weight-Bearing for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/03-supported-loading-and-weight-bearing.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Build a step from weight shift | [Step Initiation From Weight Shift for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/04-step-initiation-from-weight-shift.md) | One-to-one expansion; wording and examples may be updated. |
| 5. Backward walking or foot sliding | [Foot Sliding for Ankle and Leg Weakness](../../reference/recovery-techniques/functional_limb_weakness/05-foot-sliding-for-ankle-and-leg-weakness.md); [Backward Walking as a Bridge to Forward Walking](../../reference/recovery-techniques/functional_limb_weakness/06-backward-walking-as-a-bridge.md) | Split into separately explained components. |
| 6. Treadmill, mirror or body-weight support | [Treadmill and Body-Weight-Supported Walking](../../reference/recovery-techniques/functional_limb_weakness/07-treadmill-and-body-weight-supported-walking.md); [Mirror and Visual Feedback for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/08-mirror-and-visual-feedback.md) | Split into separately explained components. |
| 7. Meaningful arm and two-handed tasks | [Meaningful Upper-Limb and Two-Handed Tasks](../../reference/recovery-techniques/functional_limb_weakness/09-meaningful-upper-limb-and-two-handed-tasks.md) | One-to-one expansion; wording and examples may be updated. |
| 8. Graded activity and reconditioning | [Graded Activity and Reconditioning for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/10-graded-activity-and-reconditioning.md) | One-to-one expansion; wording and examples may be updated. |
| 9. Electrical stimulation as an adjunct | [Electrical Stimulation as a Movement Adjunct](../../reference/recovery-techniques/functional_limb_weakness/11-electrical-stimulation-as-an-adjunct.md) | One-to-one expansion; wording and examples may be updated. |
| 10. Relapse and self-management plan | [Relapse and Self-Management Planning for Functional Limb Weakness](../../reference/recovery-techniques/functional_limb_weakness/12-relapse-and-self-management-planning.md) | One-to-one expansion; wording and examples may be updated. |

### Functional tremor

8 original entries became 9 pages because mirror feedback and surface-EMG feedback were separated.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/02-functional-tremor.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/56164dbaecc20d2839ea4f93a05ddc11f26b7172)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Tremor retrainment | [Voluntary Tremor Retrainment for Functional Tremor](../../reference/recovery-techniques/functional_tremor/01-voluntary-tremor-retraining.md) | One-to-one expansion; wording and examples may be updated. |
| 2. Competing rhythm | [Competing Rhythm and Entrainment Practice for Functional Tremor](../../reference/recovery-techniques/functional_tremor/02-competing-rhythm-and-entrainment-practice.md) | One-to-one expansion; wording and examples may be updated. |
| 3. External-focus task practice | [External Focus and Meaningful-Task Practice for Functional Tremor](../../reference/recovery-techniques/functional_tremor/03-external-focus-and-meaningful-task-practice.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Posture and movement-pattern adjustment | [Posture, Alignment and Movement-Pattern Adjustment for Functional Tremor](../../reference/recovery-techniques/functional_tremor/04-posture-alignment-and-movement-pattern-adjustment.md) | One-to-one expansion; wording and examples may be updated. |
| 5. Contract–release relaxation | [Contract–Release and Muscle Relaxation for Functional Tremor](../../reference/recovery-techniques/functional_tremor/05-contract-release-and-muscle-relaxation.md) | One-to-one expansion; wording and examples may be updated. |
| 6. Mirror or EMG feedback | [Mirror and Visual Feedback for Functional Tremor](../../reference/recovery-techniques/functional_tremor/06-mirror-and-visual-feedback.md); [Surface-EMG Biofeedback for Functional Tremor](../../reference/recovery-techniques/functional_tremor/07-surface-emg-biofeedback.md) | Split into separately explained components. |
| 7. Whole-person treatment | [Individualized Whole-Person Treatment for Functional Tremor](../../reference/recovery-techniques/functional_tremor/08-individualized-whole-person-treatment.md) | One-to-one expansion; wording and examples may be updated. |
| 8. Relapse plan | [Relapse and Self-Management Planning for Functional Tremor](../../reference/recovery-techniques/functional_tremor/09-relapse-and-self-management-planning.md) | One-to-one expansion; wording and examples may be updated. |

### Functional jerks or myoclonus

8 original entries became 9 pages by separating activity/load planning from arousal regulation. The latter also elaborates startle-related selection; it is not a separately established treatment added by the count.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/03-functional-jerks-and-myoclonus.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/3911bb74db1f5a40b6679eeebf6dff9a09731219)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Map the pattern | [Pattern and Warning Mapping for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/01-pattern-and-warning-mapping.md) | One-to-one expansion; wording and examples may be updated. |
| 2. Redirect attention at a familiar warning | [Early Attention Redirection for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/02-early-attention-redirection.md) | One-to-one expansion; wording and examples may be updated. |
| 3. Use a competing or continuous action | [Competing and Continuous Movement for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/03-competing-and-continuous-movement.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Address pain or muscle overactivity before the jerk | [Pain and Muscle-Overactivity Management for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/04-pain-and-muscle-overactivity-management.md) | One-to-one expansion; wording and examples may be updated. |
| 5. Practise function, not repeated jerk suppression | [Meaningful Functional-Task Practice for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/05-meaningful-functional-task-practice.md) | One-to-one expansion; wording and examples may be updated. |
| 6. Graded activity and regulation | [Graded Activity and Load Planning for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/06-graded-activity-and-load-planning.md); [Arousal and Startle Regulation for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/07-arousal-and-startle-regulation.md) | Split into separately explained components. |
| 7. Safety and relapse plan | [Episode Safety and Relapse Planning for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/08-episode-safety-and-relapse-planning.md) | One-to-one expansion; wording and examples may be updated. |
| 8. Multidisciplinary treatment | [Individualized Multidisciplinary Treatment for Functional Jerks](../../reference/recovery-techniques/functional_jerks_and_myoclonus/09-individualized-multidisciplinary-treatment.md) | One-to-one expansion; wording and examples may be updated. |

### Functional dystonia

10 original entries map to 10 core pages: two merges (positioning with release; sensory contact with desensitization) offset two splits (mirror/EMG; complications/equipment). Three additional review/care pages brought the document total to 13.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/04-functional-dystonia.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/f1be50f210c26f2733415eefb2345f538814796b)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Comfortable supported positioning | [Supported Positioning and Non-Forceful Release for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/01-supported-positioning-and-non-forceful-release.md) | Combined with original #7. |
| 2. Alignment away from sustained end range | [Position and Gravity Change for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/02-position-and-gravity-change.md) | Alignment entry broadened to explain changes in position and gravity; prolonged end-range avoidance remains covered. |
| 3. External-focus movement | [External Focus and Automatic Movement for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/03-external-focus-and-automatic-movement.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Graded weight-bearing | [Graded Weight-Bearing and Functional Use for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/04-graded-weight-bearing-and-functional-use.md) | One-to-one expansion; wording and examples may be updated. |
| 5. Return to ordinary sensory experience | [Graded Sensory Reintroduction for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/05-graded-sensory-reintroduction.md) | Combined with original #6. |
| 6. Desensitization | [Graded Sensory Reintroduction for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/05-graded-sensory-reintroduction.md) | Combined with original #5. |
| 7. Reduce protective co-contraction | [Supported Positioning and Non-Forceful Release for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/01-supported-positioning-and-non-forceful-release.md) | Combined with original #1. |
| 8. Mirror or EMG feedback | [Mirror and Visual Feedback for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/06-mirror-and-visual-feedback.md); [Surface-EMG Biofeedback for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/07-surface-emg-biofeedback.md) | Split into separately explained components. |
| 9. Electrical stimulation | [Electrical Stimulation as an Adjunct for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/08-electrical-stimulation-as-an-adjunct.md) | One-to-one expansion; wording and examples may be updated. |
| 10. Pain, contracture and equipment management | [Pain, Skin, Joint-Range and Contracture Management for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/09-pain-skin-joint-and-contracture-management.md); [Splint, Orthosis, Footwear and Mobility-Equipment Review for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/10-equipment-and-orthosis-review.md) | Split into separately explained components. |

**Additional pages, outside the original numbered list:**

- [Specialist Botulinum-Toxin Review for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/11-specialist-botulinum-toxin-review.md) — **Additional specialist treatment review.** New standalone specialist-option page; it was not a numbered original entry. The page states that the small pilot trial does not support routine injection.
- [Episode, Flare and Relapse Planning for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/12-episode-flare-and-relapse-planning.md) — **Additional care-planning guidance.** Develops the original unnumbered episode/flare guidance; it is not an additional distinct rehabilitation technique.
- [Individualized Multidisciplinary Treatment for Functional Dystonia](../../reference/recovery-techniques/functional_dystonia/13-individualized-multidisciplinary-treatment.md) — **Additional coordinated-care guidance.** Develops the original clinician discussion of multidisciplinary care; it is not an additional distinct exercise.

### Functional gait disorder

13 original entries still map to 13 pages: treadmill/support versus mirror feedback was split, while light-object/hand-task work and dual-task walking share one page. Equal totals therefore do not mean an unchanged one-to-one list.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/05-functional-gait-disorder.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/88ef5a9f60d8700abe3d6600359355407096ad6b)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Rhythmic weight shift into steps | [Rhythmic Weight Shift and Step Initiation for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/01-rhythmic-weight-shift-and-step-initiation.md) | One-to-one expansion; wording and examples may be updated. |
| 2. Change speed | [Speed and Continuous-Walking Transformation for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/03-speed-and-continuous-walking-transformation.md) | One-to-one expansion; wording and examples may be updated. |
| 3. Foot sliding or “skiing” | [Foot Sliding or “Skating” Progression for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/02-foot-sliding-or-skating-progression.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Backward or sideways walking | [Backward, Sideways and Direction-Change Walking for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/04-backward-sideways-and-direction-change-walking.md) | One-to-one expansion; wording and examples may be updated. |
| 5. External rhythm | [External Rhythm and Auditory Cueing for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/05-external-rhythm-and-auditory-cueing.md) | One-to-one expansion; wording and examples may be updated. |
| 6. Exaggerated movement | [Exaggerated Movement and Marching for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/06-exaggerated-movement-and-marching.md) | One-to-one expansion; wording and examples may be updated. |
| 7. Light hand weights or another task | [External Focus and Purposeful Dual-Task Walking for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/07-external-focus-and-purposeful-dual-task-walking.md) | Combined with original #10. The specific hand-weight example was omitted during expansion. It is restored within the combined page as an optional clinician-selected variant, with safety selection and the existing consensus citation. |
| 8. Stairs as a bridge | [Stairs as a Supervised Bridge for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/08-stairs-as-a-supervised-bridge.md) | One-to-one expansion; wording and examples may be updated. |
| 9. Treadmill, mirror or body-weight support | [Treadmill and Body-Weight-Supported Walking for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/09-treadmill-and-body-weight-supported-walking.md); [Mirror and Visual Feedback for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/10-mirror-and-visual-feedback.md) | Split into separately explained components. |
| 10. Dual-task walking | [External Focus and Purposeful Dual-Task Walking for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/07-external-focus-and-purposeful-dual-task-walking.md) | Combined with original #7. |
| 11. Graded community walking | [Graded Community Walking and Environmental Complexity for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/11-graded-community-walking-and-environmental-complexity.md) | One-to-one expansion; wording and examples may be updated. |
| 12. Mobility aids and fall planning | [Mobility Aids, Guarding and Fall Planning for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/12-mobility-aids-guarding-and-fall-planning.md) | One-to-one expansion; wording and examples may be updated. |
| 13. FND-informed physiotherapy and relapse planning | [Individualized FND-Informed Rehabilitation and Relapse Planning for Functional Gait Disorder](../../reference/recovery-techniques/functional_gait_disorder/13-individualized-rehabilitation-and-relapse-planning.md) | One-to-one expansion; wording and examples may be updated. |

### Functional seizures

10 original entries map to 9 core pages after the two overlapping grounding entries were combined. One paediatric programme page and two care-planning pages bring the document total to 12.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/06-functional-seizures.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/873e7510736df9f0bc526aeff7999cf9452637b3)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Clear diagnostic explanation and follow-up | [Diagnostic Explanation and Continuing Care for Functional Seizures](../../reference/recovery-techniques/functional_seizures/01-diagnostic-explanation-and-continuing-care.md) | One-to-one expansion; wording and examples may be updated. |
| 2. Individual episode-safety plan | [Individualized Episode Safety Plan for Functional Seizures](../../reference/recovery-techniques/functional_seizures/02-individualized-episode-safety-plan.md) | One-to-one expansion; wording and examples may be updated. |
| 3. Warning, trigger and pattern mapping | [Warning and Pattern Mapping for Functional Seizures](../../reference/recovery-techniques/functional_seizures/03-warning-and-pattern-mapping.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Seizure-focused psychological treatment | [Seizure-Focused Psychological Treatment for Functional Seizures](../../reference/recovery-techniques/functional_seizures/05-seizure-focused-psychological-treatment.md) | One-to-one expansion; wording and examples may be updated. |
| 5. Breathing-control training | [Clinician-Taught Breathing Control for Functional Seizures](../../reference/recovery-techniques/functional_seizures/07-clinician-taught-breathing-control.md) | One-to-one expansion; wording and examples may be updated. |
| 6. Treat coexisting conditions | [Coexisting-Condition and Load Review for Functional Seizures](../../reference/recovery-techniques/functional_seizures/08-coexisting-condition-and-load-review.md) | One-to-one expansion; wording and examples may be updated. |
| 7. Medication review | [Prescriber-Led Medication Review for Functional Seizures](../../reference/recovery-techniques/functional_seizures/09-prescriber-led-medication-review.md) | One-to-one expansion; wording and examples may be updated. |
| 8. Graded return to activity | [Supported Return to Activities for Functional Seizures](../../reference/recovery-techniques/functional_seizures/10-supported-return-to-activities.md) | One-to-one expansion; wording and examples may be updated. |
| 9. Cold or textured sensory grounding at a familiar warning | [Sensory Grounding and an Attention Anchor for Functional Seizures](../../reference/recovery-techniques/functional_seizures/04-sensory-grounding-and-attention-anchor.md) | Combined with original #10. |
| 10. A fixed visual or sensory anchor | [Sensory Grounding and an Attention Anchor for Functional Seizures](../../reference/recovery-techniques/functional_seizures/04-sensory-grounding-and-attention-anchor.md) | Combined with original #9. |

**Additional pages, outside the original numbered list:**

- [ReACT for Children and Adolescents for Functional Seizures](../../reference/recovery-techniques/functional_seizures/06-react-for-children-and-adolescents.md) — **Additional age-specific treatment page.** ReACT is a separately discussed paediatric programme within the psychological-treatment family. It was already mentioned in the CBT resource map, but was not a numbered entry in the original symptom list.
- [Supporter Response Rehearsal for Functional Seizures](../../reference/recovery-techniques/functional_seizures/11-supporter-response-rehearsal.md) — **Additional supporter-planning guidance.** Develops safety planning and supporter guidance; rehearsal is an implementation aid, not a separately proven seizure treatment.
- [Recovery, Cluster and Flare Planning for Functional Seizures](../../reference/recovery-techniques/functional_seizures/12-recovery-cluster-and-flare-planning.md) — **Additional recovery-planning guidance.** Develops the original unnumbered cluster/recovery/flare section; it is not a separately proven seizure treatment.

### Functional sensory symptoms

The 10 original entries each have one detailed page. Two additional safety/planning pages bring the document total to 12; there were not 12 original techniques.

[Original list at the baseline](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/07-functional-sensory-symptoms.md) · [Expansion commit](https://github.com/FND-Education-Project/FND-Education/commit/cc13daf18e4e72c405bb4e5f1cce1fe8f6f3300e)

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Graded sensory stimulation | [Graded Sensory Input for Reduced or Altered Sensation](../../reference/recovery-techniques/functional_sensory_symptoms/01-graded-sensory-input.md) | One-to-one expansion; wording and examples may be updated. |
| 2. Desensitization for hypersensitivity | [Desensitization for Painful Touch and Hypersensitivity](../../reference/recovery-techniques/functional_sensory_symptoms/02-desensitization-for-painful-touch.md) | One-to-one expansion; wording and examples may be updated. |
| 3. Sensory discrimination | [Sensory Discrimination: Texture, Location and Object Recognition](../../reference/recovery-techniques/functional_sensory_symptoms/03-sensory-discrimination.md) | One-to-one expansion; wording and examples may be updated. |
| 4. Pair sensation with meaningful movement | [Pairing Sensation With Meaningful Movement](../../reference/recovery-techniques/functional_sensory_symptoms/04-sensation-with-meaningful-movement.md) | One-to-one expansion; wording and examples may be updated. |
| 5. Graded return to ordinary contact | [Graded Return to Clothing, Footwear and Everyday Contact](../../reference/recovery-techniques/functional_sensory_symptoms/05-ordinary-contact-and-clothing.md) | One-to-one expansion; wording and examples may be updated. |
| 6. Mirror or visual feedback | [Visual and Mirror Feedback for Altered Body Sensation](../../reference/recovery-techniques/functional_sensory_symptoms/06-visual-and-mirror-feedback.md) | One-to-one expansion; wording and examples may be updated. |
| 7. Attention redirection | [External Attention and Task Focus](../../reference/recovery-techniques/functional_sensory_symptoms/07-external-attention-and-task-focus.md) | One-to-one expansion; wording and examples may be updated. |
| 8. Sensory-profile assessment and OT strategies | [Sensory-Profile Assessment and Environmental Adaptation](../../reference/recovery-techniques/functional_sensory_symptoms/08-sensory-profile-and-environment.md) | One-to-one expansion; wording and examples may be updated. |
| 9. TENS or electrical stimulation | [TENS and Electrical Stimulation: Specialist Review and Safety](../../reference/recovery-techniques/functional_sensory_symptoms/09-tens-and-electrical-stimulation-review.md) | One-to-one expansion; wording and examples may be updated. |
| 10. Treat related pain or migraine | [Coexisting Pain, Migraine and Medical Review](../../reference/recovery-techniques/functional_sensory_symptoms/10-coexisting-pain-migraine-and-medical-review.md) | One-to-one expansion; wording and examples may be updated. |

**Additional pages, outside the original numbered list:**

- [Skin, Pressure and Injury Protection](../../reference/recovery-techniques/functional_sensory_symptoms/11-skin-pressure-and-injury-protection.md) — **Additional injury-protection guidance.** Develops skin, burn and pressure precautions from the original page; protective care is not a new sensory-restoration technique.
- [Episode, Flare and Available-Capacity Planning](../../reference/recovery-techniques/functional_sensory_symptoms/12-episode-flare-and-capacity-planning.md) — **Additional flare-planning guidance.** Develops the original unnumbered episode/flare guidance and available-capacity planning; it is not a new sensory-restoration technique.

## Coverage and limits

Every original entry in the seven expanded collections has a current destination. The audit found editorial splits, combinations, broader examples and supplementary pages, rather than evidence that every symptom has the same number of distinct techniques. One specific example had been lost: carrying small hand weights during gait practice. The consensus source was checked and this example has been restored within the existing combined page, with explicit clinician selection and safety boundaries; it does not create another page or claim a separate proven treatment. Original evidence labels are historical labels, not endorsements to restore them: for example, the later grounding evidence correction and TENS safety boundary remain intact.

The added botulinum-toxin and paediatric ReACT pages retain their existing source discussions and population/evidence limits. This audit does not promote their evidence or certify the rest of the clinical content. Clinical and lived-experience review remains pending.

## Rule for future expansion

Begin with the actual original list, record its commit and entry count, and map each entry to its destination. Split only for a clear instructional or clinical distinction; combine overlapping entries transparently. Label any added intervention with its source, evidence limits and reason for inclusion. Put additional safety, access and planning material in a clearly named supporting section. Never choose a target page count. Report original entries, resulting pages and additions separately.

<!-- NAV-CONTEXT:START -->
**Related:** [Recovery collection guide](../../reference/recovery-techniques/collection-guide.md) · [Technique index](../../reference/recovery-techniques/technique-index.md) · [Page maintenance policy](repository-change-and-page-maintenance-policy.md)

**Navigate:** [Home](../../README.md) · [Reference Library](../../reference/README.md) · [Site Map](../../SITEMAP.md)
<!-- NAV-CONTEXT:END -->
