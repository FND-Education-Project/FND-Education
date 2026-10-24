# My FND Journey — companion app documentation

**Status:** Design proposal / documentation only (October 23, 2026). No application, API, database, reminder, analytics, or account integration is deployed by this folder. Decisions are tagged **Agreed**, **Proposed**, or **Open**; proposed choices are not implementation approvals.

My FND Journey is a free, optional, privacy-first companion to the FND Education Project. Its core questions:

1. **What am I experiencing?** — symptoms and optional journal.
2. **How is it affecting my life?** — activity/participation and available capacity.
3. **What am I learning?** — patterns, optional educational links, appointment preparation.

Readers can use every feature without a course account. Connecting a learner account offers **Continue Learning** directly to the next lesson, with no role/audience/reading-mode preference. Clinicians are encouraged through course content to read all three existing audience sections; there is **no user-role detection, assignment, or tracking** in the companion app.

## Documents

| File | Purpose |
| --- | --- |
| [Product and acceptance criteria](product-spec.md) | What the app does, principles, screen-by-screen behaviour and exclusions |
| [Technology stack and architecture](architecture-and-stack.md) | Hosting, isolation, data flow, proposed modules/classes, offline and alternatives |
| [Storage and data contracts](data-model.md) | Draft versioned local records, scene coordinates, activity capacity and export |
| [Activity Room interaction spec](activity-room.md) | Drawers, sprites, placement, zoom, stacking, clipping, lists, accessibility |
| [Privacy, security and deletion](privacy-security-deletion.md) | Threat model, encryption choices, account vs device deletion and consent |
| [Course-tracker PR #154 handoff](course-tracker-handoff.md) | Integration requirements, current API constraints, safe change list, tests |
| [Implementation plan and QA](implementation-roadmap.md) | Milestones, test matrix, definition of done, unresolved decisions |

## Design guardrails

- **Agreed:** No project collection of symptom, activity, room, capacity, journal or report data. All such content stays on the device. Export is user-initiated.
- **Agreed:** Tracker/check-ins are optional; no streaks, rankings, pressure, cause claims, or hourly notifications.
- **Agreed:** An object in the Activity Room arrives **already coloured**, and visual clutter is allowed. Activity check-ins are optional.
- **Agreed:** Separate drawers (outside, chores, rest/relaxation, social, and possibly personal positives), with gender-presentation options for social people and inclusive customization.
- **Agreed:** App does not classify a visitor as a person with FND, supporter or clinician. All three website educational sections remain publicly readable.
- **Agreed:** Drawing four/five scene PNGs and final sprites is **last**, after behaviour and data contracts are tested with existing placeholder assets.
- **Proposed:** Installable PWA on an isolated origin, with a purely local database and the existing lesson backend used only for optional learning integration.
- **Open:** Security unlock/passphrase defaults, PWA-versus-native notification requirements, precise scene templates, glossary text, thresholds for optional reflection.

## Existing code to integrate later

- Learner progress is an **unmerged, undeployed draft** in [PR #154](https://github.com/FND-Education-Project/FND-Education/pull/154), not a working production account service.
- The website search vocabulary is [`tools/search/subject-index.json`](../../../tools/search/subject-index.json), but it is broader than an app-specific symptom catalogue. Match suggestions must be reviewed and must not claim a diagnosis.
- Existing project [accessibility standards](../accessibility-standards.md), [safety/editorial rules](../safety-and-editorial-rules.md), and [research policies](../research-and-citation-policy.md) continue to apply.

## Collaboration / handoff

Work on the app in a separate branch and PR; do not merge, deploy, switch DNS, or activate learner accounts implicitly. A code PR should reference its relevant design document, explicitly list any deviations, and run the tests in [implementation-roadmap.md](implementation-roadmap.md). The course-progress maintainer should consult [course-tracker-handoff.md](course-tracker-handoff.md) before changing PR #154.

**No code has been added by this design documentation PR.**
