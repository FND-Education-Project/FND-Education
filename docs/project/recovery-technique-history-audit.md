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
| [Functional Visual Symptoms](../../reference/recovery-techniques/08-functional-visual-symptoms.md) | 9 | 9 | Nine original entries expanded one-to-one; no additional pages. |
| [Functional Speech and Voice Symptoms](../../reference/recovery-techniques/09-functional-speech-and-voice-symptoms.md) | 11 | 11 | Eleven original entries expanded one-to-one; no additional pages. |
| [Functional Swallowing Symptoms and Globus](../../reference/recovery-techniques/10-functional-swallowing-and-globus.md) | 11 | 11 | Eleven original entries expanded one-to-one; the September 16 audit incorrectly reported ten for swallowing. |
| [Functional Cough and Upper-Airway Symptoms](../../reference/recovery-techniques/11-functional-cough-and-upper-airway-symptoms.md) | 10 | 10 | Ten original entries expanded one-to-one; collection overview is an additional navigation document. |
| [Functional Cognitive Disorder](../../reference/recovery-techniques/12-functional-cognitive-disorder.md) | 13 | 13 | Thirteen original entries expanded one-to-one; collection overview and separate FCD background are additional navigation/education documents, not interventions. |
| [Persistent Postural-Perceptual Dizziness](../../reference/recovery-techniques/13-persistent-postural-perceptual-dizziness.md) | 13 | 13 | Thirteen original entries expanded one-to-one; September 16 audit count of twelve corrected. Collection overview is an additional navigation document. |
| [Functional Facial Symptoms](../../reference/recovery-techniques/14-functional-facial-symptoms.md) | 8 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Functional Paralysis](../../reference/recovery-techniques/15-functional-paralysis.md) | 7 | Not yet expanded | Original symptom list remains the baseline for future expansion. |
| [Recovery and Safety Techniques for Functional Drop Attacks](../../reference/recovery-techniques/16-functional-drop-attacks.md) | 7 | Not yet expanded | Original symptom list remains the baseline for future expansion. |

## Original-entry to current-page mapping

## Functional swallowing symptoms and globus

**Correction checked September 18, 2026:** The September 16 table reported ten entries in error. Both the [initial list at a67567b](https://github.com/FND-Education-Project/FND-Education/blob/a67567b/reference/recovery-techniques/10-functional-swallowing-and-globus.md) and the [pre-expansion baseline at 74138f3](https://github.com/FND-Education-Project/FND-Education/blob/74138f34797ae840f794f0c809da64fad30dc401/reference/recovery-techniques/10-functional-swallowing-and-globus.md) contain **eleven**. The immediate pre-expansion list at `17b97f2` also contains eleven. The medication discussion was already original entry 10; restriction review was entry 11. Neither was newly invented to reach a page count.

Eleven original entries map one-to-one to eleven detailed pages. No additional page or omitted entry. The flare guidance remains in the overview and relevant details. Safety wording now explicitly limits the old sip example to assessed intake, and limits external focus to clinician-selected practice rather than conversation with a mouthful.

| Original entry | Detailed coverage | Relationship |
|---|---|---|
| 1. Positive explanation | [Understanding Your Swallowing Assessment and Plan](../../reference/recovery-techniques/functional_swallowing_and_globus/01-understanding-the-assessment.md) | One-to-one expansion; individualized safety limits retained. |
| 2. Comfortable breathing and posture | [Comfortable Breathing and Supported Positioning for Meals](../../reference/recovery-techniques/functional_swallowing_and_globus/02-comfortable-breathing-and-posture.md) | One-to-one expansion; individualized safety limits retained. |
| 3. Jaw, neck and laryngeal release | [Reducing Extra Jaw, Neck and Throat Effort](../../reference/recovery-techniques/functional_swallowing_and_globus/03-jaw-neck-and-laryngeal-release.md) | One-to-one expansion; individualized safety limits retained. |
| 4. Graded food texture or volume | [Practising With Assessed Food Textures and Amounts](../../reference/recovery-techniques/functional_swallowing_and_globus/04-assessed-texture-and-volume-practice.md) | One-to-one expansion; individualized safety limits retained. |
| 5. Graded meal-setting practice | [Making Meals More Manageable in Different Settings](../../reference/recovery-techniques/functional_swallowing_and_globus/05-meal-setting-and-participation.md) | One-to-one expansion; individualized safety limits retained. |
| 6. Reduce repeated checking and dry swallows | [Stepping Back From Repeated Throat Checking](../../reference/recovery-techniques/functional_swallowing_and_globus/06-reducing-test-swallows.md) | One-to-one expansion; individualized safety limits retained. |
| 7. External focus or distraction | [Using a Gentle External Focus During Assessed Practice](../../reference/recovery-techniques/functional_swallowing_and_globus/07-safe-external-focus.md) | One-to-one expansion; individualized safety limits retained. |
| 8. Address fear and avoidance | [Working With Fear of Choking Without Pressure](../../reference/recovery-techniques/functional_swallowing_and_globus/08-fear-and-avoidance-support.md) | One-to-one expansion; individualized safety limits retained. |
| 9. Treat coexisting conditions | [Treating Other Conditions That Make Swallowing Harder](../../reference/recovery-techniques/functional_swallowing_and_globus/09-coexisting-conditions.md) | One-to-one expansion; individualized safety limits retained. |
| 10. Discuss gut–brain neuromodulator medication for assessed globus | [A Prescriber-Led Medication Discussion for Assessed Globus](../../reference/recovery-techniques/functional_swallowing_and_globus/10-globus-medication-review.md) | One-to-one expansion; individualized safety limits retained. |
| 11. Review unnecessary restrictions | [Reviewing Diet and Equipment Restrictions Together](../../reference/recovery-techniques/functional_swallowing_and_globus/11-reviewing-diet-and-equipment-restrictions.md) | One-to-one expansion; individualized safety limits retained. |



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

## Functional tics: post-baseline addition

Added September 17, 2026, after the original sixteen lists. There was no separate functional-tic recovery list in the historical baseline. The first version of [the new overview](../../reference/recovery-techniques/17-functional-tics-and-tic-like-symptoms.md) establishes the following baseline; this implementation commit is its provenance.

1. Positive explanation and a shared plan — treatment/formulation/coordinated care.
2. Brief pattern and context mapping — treatment/formulation/coordinated care.
3. Individually formulated behavioral or psychological treatment — treatment/formulation/coordinated care.
4. Supported return to routines and valued activity — treatment/formulation/coordinated care.
5. Coexisting-condition and medication review — treatment/formulation/coordinated care.
6. Motor and vocal safety and communication planning — supporting safety/access/care planning.
7. Family, school and workplace response planning — supporting safety/access/care planning.
8. Tic-attack, cluster and flare planning — supporting safety/access/care planning.

Eight overview entries; zero detailed technique pages. These are not eight proven treatments. Any later expansion must map splits, combinations and new additions against this list. The historical sixteen-list tables above remain unchanged.

## Functional cough and upper-airway symptoms

Checked September 20, 2026: the initial list at `a67567b`, pre-expansion baseline `74138f34797ae840f794f0c809da64fad30dc401`, and immediate base `7d3cc15` each contain the same ten entries. Ten detailed pages preserve every entry and example; no added interventions, splits, combinations or omissions. The README adds one navigation document, making eleven documents in the folder.

| Original entry | Detailed destination |
| --- | --- |
| 1. Map the earliest urge | [Noticing the Earliest Cough Urge](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/01-noticing-the-earliest-urge.md) |
| 2. Sip and swallow | [Using a Sip and Swallow When It Is Safe](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/02-sip-and-swallow.md) |
| 3. Gentle nasal sniff or clinician-selected substitute | [Choosing One Comfortable Cough Substitute](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/03-clinician-selected-substitute.md) |
| 4. Relaxed-throat breathing | [Finding a Less Effortful Breathing Pattern](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/04-relaxed-throat-breathing.md) |
| 5. Lower-rib or diaphragmatic coordination | [Coordinating Gentle Lower-Rib Breathing](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/05-lower-rib-coordination.md) |
| 6. Reduce habitual throat clearing | [Easing Repeated Throat Clearing](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/06-reducing-throat-clearing.md) |
| 7. Graded trigger exposure | [Returning to Activities With Graded Trigger Practice](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/07-graded-trigger-practice.md) |
| 8. Hydration and laryngeal care | [Making Daily Life Kinder to Your Throat](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/08-hydration-and-laryngeal-care.md) |
| 9. CBT-informed attention and arousal strategies | [Working With Attention, Worry and the Cough Urge](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/09-attention-and-arousal-support.md) |
| 10. Treat coexisting conditions | [Keeping Other Causes and Conditions in the Care Plan](../../reference/recovery-techniques/functional_cough_and_upper_airway_symptoms/10-treating-coexisting-conditions.md) |

## Functional Cognitive Disorder

Checked September 21, 2026: the initial list at `a67567b`, historical baseline `74138f34797ae840f794f0c809da64fad30dc401`, and immediate base `c7dab88` contain the same thirteen entries. Each maps to one detailed page, with no split, combination or omission. Fourteen documents comprise thirteen detailed pages and one navigation README. The newer workbook development report informs original entry 13; it does not add an intervention page. Original examples remain covered; reassurance and testing advice is qualified to preserve necessary information, aids and safety checks.

| Original entry | Detailed destination |
| --- | --- |
| 1. Positive explanation of the cognitive pattern | [Understanding Memory and Thinking Difficulties in FCD](../../reference/recovery-techniques/functional_cognitive_disorder/01-understanding-the-cognitive-pattern.md) |
| 2. Reduce repeated self-testing | [Taking a Break From Repeated Memory Tests](../../reference/recovery-techniques/functional_cognitive_disorder/02-reducing-self-testing.md) |
| 3. Reduce reassurance loops | [Finding Reassurance That Still Helps](../../reference/recovery-techniques/functional_cognitive_disorder/03-reassurance-without-loops.md) |
| 4. Attention retraining | [Giving One Task Your Attention](../../reference/recovery-techniques/functional_cognitive_disorder/04-attending-to-one-task.md) |
| 5. Prediction versus performance | [Comparing What You Expect With What Happens](../../reference/recovery-techniques/functional_cognitive_disorder/05-prediction-and-performance.md) |
| 6. Success record | [Keeping a Small Record of What Helped](../../reference/recovery-techniques/functional_cognitive_disorder/06-noticing-what-helped.md) |
| 7. Graded return to meaningful cognitive tasks | [Returning to Reading, Conversation and Other Valued Tasks](../../reference/recovery-techniques/functional_cognitive_disorder/07-returning-to-meaningful-tasks.md) |
| 8. External memory supports | [Building a Thinking and Memory System You Can Actually Use](../../reference/recovery-techniques/functional_cognitive_disorder/08-external-memory-supports.md) |
| 9. Single-task routines and pacing | [Making the Day Easier With Routines and Pacing](../../reference/recovery-techniques/functional_cognitive_disorder/09-single-task-routines-and-pacing.md) |
| 10. Treat contributors and comorbidity | [Keeping Other Contributors in the Care Plan](../../reference/recovery-techniques/functional_cognitive_disorder/10-contributors-and-coexisting-conditions.md) |
| 11. Online group ACT | [Considering an Online ACT Group](../../reference/recovery-techniques/functional_cognitive_disorder/11-online-group-act.md) |
| 12. CBT- and metacognition-informed digital self-help | [Considering FCD-Specific Digital Self-Help](../../reference/recovery-techniques/functional_cognitive_disorder/12-digital-self-help.md) |
| 13. Individual cognitive rehabilitation | [Planning Individual Cognitive Rehabilitation](../../reference/recovery-techniques/functional_cognitive_disorder/13-individual-cognitive-rehabilitation.md) |

<!-- NAV-CONTEXT:START -->
**Related:** [Recovery collection guide](../../reference/recovery-techniques/collection-guide.md) · [Technique index](../../reference/recovery-techniques/technique-index.md) · [Page maintenance policy](repository-change-and-page-maintenance-policy.md)

**Navigate:** [Home](../../README.md) · [Reference Library](../../reference/README.md) · [Site Map](../../SITEMAP.md)
<!-- NAV-CONTEXT:END -->

## Subsequent expansion — September 16, 2026

### Functional visual symptoms

The nine entries at the common historical baseline also match the pre-expansion overview in commit `8194baf`. Each now has one detailed page, in the same order. The original final entry still contains separate discussions of advanced feedback and brain stimulation; keeping them together does not imply a shared evidence base. Scope and safety wording have been revised without inventing extra list entries.

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Positive explanation using preserved vision | [Positive Explanation of Preserved Vision and Follow-Up](../../reference/recovery-techniques/functional_visual_symptoms/01-positive-explanation-and-follow-up.md) | One-to-one expansion. |
| 2. Notice brief examples of better vision | [Noticing Briefly Better Vision Without Repeated Testing](../../reference/recovery-techniques/functional_visual_symptoms/02-noticing-briefly-better-vision.md) | One-to-one expansion. |
| 3. Orthoptist-guided visual feedback | [Orthoptist-Guided Visual Feedback](../../reference/recovery-techniques/functional_visual_symptoms/03-orthoptist-guided-visual-feedback.md) | One-to-one expansion. |
| 4. Graded visual tasks | [Graded Visual Tasks Linked to Daily Life](../../reference/recovery-techniques/functional_visual_symptoms/04-graded-visual-task-practice.md) | One-to-one expansion. |
| 5. Practise an answer rather than waiting for certainty | [Supported Visual Choice Without Waiting for Certainty](../../reference/recovery-techniques/functional_visual_symptoms/05-supported-choice-without-certainty.md) | One-to-one expansion. |
| 6. Graded light exposure for photophobia | [Photophobia: An Agreed Light and Protection Plan](../../reference/recovery-techniques/functional_visual_symptoms/06-photophobia-light-and-protection-plan.md) | One-to-one expansion. |
| 7. Treat coexisting conditions | [Treatment of Coexisting Eye, Migraine and Neurological Conditions](../../reference/recovery-techniques/functional_visual_symptoms/07-coexisting-eye-migraine-and-neurological-care.md) | One-to-one expansion. |
| 8. Hypnotherapy or therapeutic suggestion | [Hypnotherapy and Transparent Therapeutic Suggestion](../../reference/recovery-techniques/functional_visual_symptoms/08-hypnotherapy-and-therapeutic-suggestion.md) | One-to-one expansion. |
| 9. Specialist feedback or non-invasive brain stimulation | [Advanced Visual Feedback and Non-Invasive Brain Stimulation: Specialist Review](../../reference/recovery-techniques/functional_visual_symptoms/09-advanced-feedback-and-brain-stimulation-review.md) | One-to-one expansion. |

## Subsequent expansion — September 17, 2026

### Functional speech and voice symptoms

The eleven entries at the common historical baseline also match the [pre-expansion overview](https://github.com/FND-Education-Project/FND-Education/blob/7d8c656ab05fe08c967010477c5b33b346683f1b/reference/recovery-techniques/09-functional-speech-and-voice-symptoms.md). Each now has one detailed page, in the same order. No original entry was dropped or combined. The historical “Temporary communication support” label is retained in this map; its page also covers intermittent and ongoing support. Higher-force or specialist procedures are not reproduced as home instructions.

| Original entry | Current detailed coverage | Editorial relationship |
|---|---|---|
| 1. Education and demonstration of preserved communication | [Understanding the Diagnosis and Finding an Easier Starting Point](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/01-understanding-preserved-communication.md) | One-to-one expansion. |
| 2. Reflexive or automatic voice | [Finding a Comfortable Automatic Voice](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/02-comfortable-automatic-voice.md) | One-to-one expansion. |
| 3. Rhythm, singing or automatic sequences | [Using Rhythm, Singing or Familiar Sequences](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/03-rhythm-singing-and-familiar-sequences.md) | One-to-one expansion. |
| 4. Shape an easy sound into speech | [Building an Easier Sound Into Words and Conversation](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/04-building-sound-into-speech.md) | One-to-one expansion. |
| 5. Rate and prosody adjustment | [Finding a Helpful Speech Rate and Pattern](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/05-rate-and-prosody.md) | One-to-one expansion. |
| 6. External-focus communication | [Focusing on the Message and the Listener](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/06-focus-on-the-message.md) | One-to-one expansion. |
| 7. Breathing, posture and muscle-release work | [Making Speech More Comfortable: Breath, Posture and Muscle Release](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/07-breath-posture-and-release.md) | One-to-one expansion. |
| 8. Meaningful communication practice | [Practising the Conversations You Want to Have](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/08-practice-real-conversations.md) | One-to-one expansion. |
| 9. Temporary communication support | [Communication Support When Speech Is Difficult or Unavailable](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/09-communication-support-and-aac.md) | One-to-one expansion. |
| 10. CBT-informed or psychologically informed strategies | [Psychologically Informed Support for Communication](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/10-psychologically-informed-communication-care.md) | One-to-one expansion. |
| 11. Treat coexisting conditions | [Coexisting Conditions and Reassessment of Speech or Voice Changes](../../reference/recovery-techniques/functional_speech_and_voice_symptoms/11-coexisting-conditions-and-reassessment.md) | One-to-one expansion. |

September 21, 2026 clarification: FCD entry 1 is foundational education and care planning, not a memory-training exercise. Its page now explains memory categories and other cognitive functions; the original thirteen-entry mapping and page count are unchanged.

September 21, 2026 background separation: [Everything We Know About FCD](../../reference/functional-cognitive-disorder.md) now holds the fuller conceptual explanation. Original entry 1 applies that explanation to an individual care plan. The thirteen original entries and their numbers remain intact; the collection overview and separate background bring this set to fifteen documents, not fifteen techniques. Recovery families do not imply independent mechanism validation.

## Persistent Postural-Perceptual Dizziness

**Correction checked September 22, 2026:** The September 16 audit incorrectly recorded twelve entries. Both the [initial list at a67567b](https://github.com/FND-Education-Project/FND-Education/blob/a67567b/reference/recovery-techniques/13-persistent-postural-perceptual-dizziness.md) and the [pre-expansion baseline at 74138f3](https://github.com/FND-Education-Project/FND-Education/blob/74138f3/reference/recovery-techniques/13-persistent-postural-perceptual-dizziness.md) contain thirteen. The immediate pre-expansion main commit, `899a7e0`, also contains thirteen. Relapse planning was already entry 13; it was not added to meet a target count.

All thirteen entries expand one-to-one, with no split, merger or omitted intervention. The additional collection overview makes fourteen documents in the detailed folder, not fourteen techniques. Medicine, technology and care-planning entries are not recast as independently validated exercises. Evidence labels are now written out at the end of each description.

| Original entry | Detailed coverage | Relationship |
| --- | --- | --- |
| 1. Individualized vestibular rehabilitation | [Building a Vestibular Rehabilitation Plan That Fits You](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/01-individual-vestibular-plan.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 2. Habituation to head and body motion | [Practising Head and Body Movement in Manageable Steps](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/02-head-and-body-motion.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 3. Graded upright exposure | [Making Sitting, Standing and Walking More Manageable](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/03-upright-activity.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 4. Graded visual-motion exposure | [Making Busy Visual Settings More Manageable](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/04-visual-motion.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 5. Gaze-stability exercise when indicated | [Using Gaze-Stability Exercises Only When They Fit](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/05-gaze-stability.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 6. Balance and gait practice | [Practising Balance and Walking With Appropriate Support](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/06-balance-and-walking.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 7. Graded community activity | [Returning to Places and Activities That Matter](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/07-community-activities.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 8. Psychologically informed vestibular rehabilitation | [Working With Worry and Attention During Vestibular Rehabilitation](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/08-psychologically-informed-rehabilitation.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 9. Treat the precipitant and comorbidity | [Keeping Other Causes of Dizziness in the Care Plan](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/09-coexisting-conditions.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 10. Optokinetic or virtual-reality practice | [Considering Supervised Visual-Motion or Virtual-Reality Practice](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/10-visual-motion-technology.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 11. Specialist neuromodulation or galvanic vestibular stimulation | [Discussing Experimental Stimulation With a Specialist](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/11-specialist-stimulation-review.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 12. SSRI or SNRI discussion | [Discussing an SSRI or SNRI With Your Prescriber](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/12-medication-discussion.md) | One-to-one expansion; individual scope and evidence limits retained. |
| 13. Relapse plan | [Making a Plan for Flares and Changing Dizziness](../../reference/recovery-techniques/persistent_postural_perceptual_dizziness/13-flare-and-review-plan.md) | One-to-one expansion; individual scope and evidence limits retained. |
