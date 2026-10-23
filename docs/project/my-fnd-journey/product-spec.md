# Product specification — My FND Journey

**Status:** Design-stage functional specification, not shipped software. Terms: **Agreed** = explicitly chosen design direction; **Proposed** = implementation recommendation; **Open** = decide/test before development.

## Purpose, audience and voice — Agreed

Create an independent, optional FND education companion useful to people recording symptoms, activities and experiences, and to anyone who wants to learn. Do not demand a medical diagnosis, force a role selection, or claim treatment. Ask three questions: what am I experiencing, how is life affected, and what am I learning?

Support uneven memory, cognitive fatigue, sensory sensitivity, motor symptoms, and variable activity. Reading level should be approachable (roughly age 14 for person-facing help). No punitive streaks, “failed day,” productivity score, diagnostic inference, automatic attribution to FND or unsupported treatment recommendations. Incomplete entries are useful entries.

## Navigation proposal

- **Home**: large Quick check-in, Activity Room, Continue Learning (linked account) / Visit Course (guest), recent note.
- **Symptoms**: typeahead selection from reviewed catalogue, custom terms, tracked list, quick check-in and history.
- **Activity Room**: landscape scene, drawers, move objects, optional per-object check-in, alternatives to dragging.
- **Journal**: timestamped optional text, episode descriptions and conservative reviewable suggestions.
- **Patterns**: factual statistics, observation templates, explicit missing-data context, chosen activity history.
- **Reports**: local, selective appointment summary/print/PDF.
- **More / settings**: scene/list preference, capacity reflection, reminders, backup/import, privacy/security, delete local data, optional lesson-account link.

Navigation can consolidate buttons for narrow screens; never bury delete/export or accessibility controls.

## Quick check-in — Agreed

- Trigger from app, shortcut/widget if technically supported, or optional user-chosen reminder time; **off by default**. Native local notifications and PWA push are materially different.
- Select tracked symptoms through searchable dropdown/typeahead, not an overwhelming all-symptom checklist.
- For each named symptom: **experienced**, **explicitly not experienced**, or **not recorded**; missing is not zero.
- Optional daily impact, meaningful activity and free note. Save as draft and later edit, including dates/times. Avoid frequent prompts.
- Notes/activities/symptoms do not automatically mark course completion.

## Matching and educational cross-links — Agreed direction

Derive a small **human-reviewed symptom catalogue** from approved subjects in `tools/search/subject-index.json`. Exact names, aliases, colloquial phrases, known spellings, and limited typo-tolerant matching run offline. The full website Pagefind subject index contains diagnoses/relationships and is **not** a verified symptom list; use it only to suggest educational discovery. Always offer **Use my own words**. Any link opens canonical site educational content when available. A match is a *suggested label*, never diagnostic confirmation.

## Activity, daily capacity and room — Agreed direction

The picture expresses what someone chose to do or considered, rather than a mandatory task list. Place coloured activity sprites into a PNG scene. Objects can remain crowded and overlap; placement is not a claim of completion. Any associated activity check-in is optional. Rest, support, adaptations and partial participation are meaningful. Offer optional end-of-day and next-morning reflections using a glossary-linked term **available capacity**. Room density can trigger **a neutral optional reflection**, but cannot be treated as a medical measure or a reliable proxy for effort.

Example: “Your room looks busy. How much capacity did you feel you had left?” Never restrict placement or say the person cannot handle another activity. No automatically computed readiness diagnosis or “you shouldn't do this” message. See [Activity Room](activity-room.md).

## Journal suggestions — Proposed

Local text rules may find a term such as “seizure” and *offer* to add a candidate tracked term if it is absent. Check negation, quoted text and references to other people; prefer false negatives over false medical assumptions. Never silently add/tally symptoms or claim diary text proves an event. Journal may record rough episode duration, support needed and recovery observations as optional fields. No automatic emergency triage.

## Insights without AI — Agreed direction

Deterministic on-device aggregations over dates where data exists. Present number of check-in days, symptom recorded days / days explicitly assessed, impact trend with appropriate caveats, and activity/participation changes. **Denominators must be visible**; missing entries never mean no symptoms. Show no finding when data is insufficient. Template-based observations cannot claim causes or predict episodes, even if patterns correlate.

## Appointment reports — Agreed direction

Local preview and choice of sections: date range, number of entries, reported symptoms and denominators, impact observations, meaningful activities, selected quotes/notes and questions for clinician. Print/PDF produced on device. No automatic inclusion of journal text or identifiers without selection; no server email/upload. Label as **self-reported, incomplete and not a diagnosis**.

## Course learning — Agreed

“Continue Learning” opens the actual next unfinished/active lesson from the existing course tracker **once** a supported account-link integration has been securely completed. Guests see a direct public course link. **No reading-mode or audience preference**, no learner role label; the website continues to show all Person, Supporter and Clinician sections. Completion remains an explicit user action on the website with its current confirmation.

## Out of scope for initial release

Cloud symptom sync; AI/LLM diagnosis, interpretation or chatbot; health data monetization; symptoms analytics server; wearable monitoring; real-time caregiver surveillance; clinician dashboard; mandatory app account; unverified Android/iOS widgets; game streaks; background health-risk predictions.

## Acceptance examples

1. Save a one-symptom entry offline, later correct its date; other unassessed symptoms remain “not recorded.”
2. Find “shaky hands” via local search; use a custom phrase if no trustworthy match.
3. Put two coloured objects on a crowded scene, move one partially offscreen, recover/edit it without losing the room; switch to accessible list mode.
4. Miss a month without alerts or loss of the record.
5. Produce an appointment report from only selected content without network access.
6. Without a link, press Visit Course. With a linked learner account, fetch only course data and open the canonical next lesson; errors fall back to the course index.
7. Delete local tracker data without affecting the learner account, or delete the server learner account without implying the local records were erased.
